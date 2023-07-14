from flask import Flask, render_template, send_from_directory, jsonify
import arb_finder

app = Flask(__name__, template_folder="../client/templates")

# Route to serve the index.html file
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/bundle.js')
def bundle():
    return send_from_directory('bundles', 'bundle.js')

@app.route('/odds')
def bix():
    data = arb_finder.test_sample_arb()
    return jsonify(data)

if __name__ == '__main__':
    app.run()

