from flask import Flask, render_template
from graph import graph_render, serve_graph, post_graph, build_graph, graph_poll

app = Flask(__name__, template_folder='resources/templates')


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/links')
def links():
    return render_template('links.html')


@app.route('/example')
def example():
    return render_template('example.html')


@app.route('/reference')
def reference():
    return render_template('reference.html')


@app.route('/graph', methods=['GET'])
def graph_static():
    return render_template('graph.html')


@app.route('/graph/images/<graph_id>', methods=['GET'])
def graph_content(graph_id):
    return serve_graph(graph_id)


@app.route('/graph/<graph_id>', methods=['GET'])
def graph_view(graph_id):
    return graph_render(graph_id)


@app.route('/graph', methods=['POST'])
@app.route('/graph/<graph_id>', methods=['POST'])
def create_graph():
    return post_graph()


@app.route('/build_graph', methods=['POST'])
def build():
    return build_graph()


@app.route('/poll/<graph_id>', methods=['GET'])
def poll(graph_id):
    return graph_poll(graph_id)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
