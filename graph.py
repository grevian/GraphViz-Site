import requests
import json

from flask import render_template, abort, redirect, request
from google.cloud import datastore, storage, tasks

datastore_client = datastore.Client()
storage_client = storage.Client()
tasks_client = tasks.CloudTasksClient()

CLOUD_STORAGE_BUCKET = 'grevian-graphviz-graphs'


def post_graph():
    dot = request.form['dot'].strip()
    gvt = request.form['method'].strip()

    key = datastore_client.key('UserGraph')
    graph = datastore.Entity(key)

    graph['dot'] = dot
    graph['graph_type'] = gvt
    graph['building'] = True

    datastore_client.put(graph)

    parent = tasks_client.queue_path("grevian-graphviz", "us-central1", "default")

    task = {
        'app_engine_http_request': {
            'app_engine_routing': {
                'version': 'py38'
            },
            'http_method': 'POST',
            'relative_uri': '/build_graph',
            'body': str(graph.key.id).encode()
        },
    }

    tasks_client.create_task(parent, task)

    # Redirect to a page where the javascript can poll until the graph is completed
    # Alternatively, Just submit this and activate the polling code on the same page
    return redirect('/graph/%s' % graph.key.id)


def build_graph():
    graph_id = request.get_data() or '(empty payload)'
    key = datastore_client.key('UserGraph', int(graph_id))
    graph = datastore_client.get(key)

    if not graph:
        abort(404)

    url = 'https://gv-renderer-tad6oyng7q-uc.a.run.app/chart'
    data = {
        'cht': 'gv:%s' % graph['graph_type'],
        'chl': graph['dot'],
        'chof': 'png'
    }

    result = requests.post(url, params=data)

    if result.status_code != 200:
        graph['error'] = 'Failed to generate your graph (Error [%s]): %s' % (result.status_code, result.text)
    else:
        image_content = result.content
        bucket = storage_client.get_bucket(CLOUD_STORAGE_BUCKET)
        blob = bucket.blob(str(graph.id))
        blob.upload_from_string(image_content, 'image/png')

    graph['building'] = False
    datastore_client.put(graph)


def graph_render(graph_id):
    key = datastore_client.key('UserGraph', int(graph_id))
    graph = datastore_client.get(key)

    if not graph:
        abort(404)

    template_values = {
        'graph_id': graph_id,
        'dot': graph['dot'],
        'method': graph['graph_type'],
        'building': graph['building']
    }

    if 'error' in graph and graph['error'] != '':
        template_values['error'] = graph['error']

    return render_template('graph.html', **template_values)


def serve_graph(graph_id):
    url = 'https://storage.googleapis.com/%s/%s' % (CLOUD_STORAGE_BUCKET, graph_id)
    return redirect(url)


def graph_poll(graph_id):
    results = {}

    key = datastore_client.key('UserGraph', int(graph_id))
    graph = datastore_client.get(key)

    if not graph:
        abort(404)

    results['building'] = graph['building']
    if 'error' in graph:
        results['error'] = graph['error']
    else:
        results['error'] = ''

    return json.dumps(results)
