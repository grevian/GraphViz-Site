import os
import requests
import webapp2
import jinja2
import json

from google.appengine.ext import blobstore
from google.appengine.ext import deferred
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers

import index as nav

jinja_environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname('resources/templates/')))

class UserGraph(ndb.Model):
  dot = ndb.TextProperty(indexed=False,required=True)
  image = ndb.BlobKeyProperty(indexed=False, required=False)
  created = ndb.DateTimeProperty(auto_now_add=True)
  building = ndb.BooleanProperty(indexed=True, required=True)
  error = ndb.TextProperty(indexed=False, required=False)

def build_graph(graph_id):
  g = UserGraph.get_by_id(graph_id)
  FINISH_URL = '/complete_upload/%s' % graph_id
  blobstore_url = blobstore.create_upload_url(FINISH_URL)

  url = 'https://chart.googleapis.com/chart'
  data = {
    'cht': 'gv:dot',
    'chl': g.dot,
    'chof': 'png'
  }

  result = requests.post(url, params=data)
  
  if result.status_code != 200:
    # g.error = result.text
    # I really wish Google would provide more meaningful feedback when this fails
    g.error = 'Failed to generate your graph (Error [%s]), perhaps a syntax error?' % result.status_code
    g.building = False
    g.put()
  else:
    image_content = result.content

    files = { 'file': ('%s.png' % graph_id, image_content) }
    result = requests.post(blobstore_url, files=files)
    if result.status_code != 200:
      raise Exception('Could not save %s.png to blob storage, [%s] %s' % (graph_id, result.status_code, result.text))
  
class GraphImageUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
  def post(self, graph_id):
    g = UserGraph.get_by_id(int(graph_id))
    if not g:
      raise LookupError('Could not find referenced Graph')
    if not g.building:
      raise ValueError('Cannot update a graph that has already been built')

    upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
    blob_info = upload_files[0]

    g.building = False
    g.image = blob_info.key()
    g.put()

    self.response.out.write('OK!')

class ServeGraphHandler(blobstore_handlers.BlobstoreDownloadHandler):
  def get(self, graph_id):
    g = UserGraph.get_by_id(int(graph_id))
    self.send_blob(g.image)

class GraphBuildingPoll(webapp2.RequestHandler):
  def get(self, graph_id):
    results = {}
    g = UserGraph.get_by_id(int(graph_id))

    if not g:
      raise LookupError("Graph Not Found")
      
    results['building'] = g.building
    if g.error:
      results['error'] = g.error
    else:
      results['error'] = ''
    
    self.response.out.write(json.dumps(results))

class GraphPublishHandler(webapp2.RequestHandler):
  def get(self, graph_id=None):
    template_values = {}
    template_values['main_nav'] = nav.get_navigation_links('graph')
    if graph_id:
      g = UserGraph.get_by_id(int(graph_id))
      if not g:
        raise LookupError('404, Graph not Found')

      template_values['graph_id'] = graph_id
      template_values['dot'] = g.dot
      # Tells JS whether to keep polling/refreshing or not
      template_values['building'] = g.building

      if g.error:
        template_values['error'] = g.error

    template = jinja_environment.get_template('graph.html')
    self.response.out.write(template.render(template_values))

  def post(self):
    dot = self.request.get('dot').strip()
    g = UserGraph(building=True, dot=dot)
    g.put()

    deferred.defer(build_graph, g.key.id())

    # Redirect to a page where the javascript can poll until the graph is completed
    # Alternatively, Just submit this and activate the polling code on the same page
    self.redirect('/graph/%s' % g.key.id())
    
