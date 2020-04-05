import os
import webapp2
import jinja2

from graph import GraphPublishHandler, GraphImageUploadHandler, ServeGraphHandler, GraphBuildingPoll

jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname('resources/templates/')))

# Truly this is a silly function
def get_navigation_links(current):
  navs = [
    {'title': 'Home', 'url': '/', 'classes': ''},
    {'title': 'Examples', 'url': '/example', 'classes': ''},
    {'title': 'Reference', 'url': '/reference', 'classes': ''},
    {'title': 'Make a Graph', 'url': '/graph', 'classes': ''},
    {'title': 'About this Site', 'url': '/about', 'classes': ''},
    {'title': 'Related Links', 'url': '/links', 'classes': ''},
    {'title': 'Contact Me', 'url': '/contact', 'classes': ''},
  ]

  for n in navs:
    if current == 'index' and n['title'] == 'Home':
      n['classes'] = 'active'
    if current in n['url']:
      n['classes'] = 'active'

  return navs

class StaticPageHandler(webapp2.RequestHandler):
  def get(self, name): 
    template_values = {}
    template_values['main_nav'] = get_navigation_links(name)
    template = jinja_environment.get_template('%s.html' % name)
    self.response.cache_control = 'public'
    self.response.cache_control.max_age = 86400
    self.response.out.write(template.render(template_values))

APP = webapp2.WSGIApplication([
    webapp2.Route(r'/', StaticPageHandler, name='index', defaults={'name': 'index'}),
    webapp2.Route(r'/index.html', StaticPageHandler, name='index_html', defaults={'name': 'index'}),
    webapp2.Route(r'/about', StaticPageHandler, name='about', defaults={'name': 'about'}),
    webapp2.Route(r'/contact', StaticPageHandler, name='contact', defaults={'name': 'contact'}),
    webapp2.Route(r'/links', StaticPageHandler, name='links', defaults={'name': 'links'}),
    webapp2.Route(r'/example', StaticPageHandler, name='example', defaults={'name': 'example'}),
    webapp2.Route(r'/example.html', StaticPageHandler, name='example_html', defaults={'name': 'example'}),
    webapp2.Route(r'/reference', StaticPageHandler, name='reference', defaults={'name': 'reference'}),
    webapp2.Route(r'/reference.html', StaticPageHandler, name='reference_html', defaults={'name': 'reference'}),
    webapp2.Route(r'/graph', GraphPublishHandler, name='graph'),
    webapp2.Route(r'/graph/<graph_id:\d+>', GraphPublishHandler, name='graph_view'),
    webapp2.Route(r'/complete_upload/<graph_id:\d+>', GraphImageUploadHandler, name='graph_upload'),
    webapp2.Route(r'/graph/images/<graph_id:\d+>', ServeGraphHandler, name='graph_download'),
    webapp2.Route(r'/poll/<graph_id:\d+>', GraphBuildingPoll, name='graph_poll'),
], debug=True)

