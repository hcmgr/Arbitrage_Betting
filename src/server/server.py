from flask import Flask, render_template, send_from_directory

app = Flask(__name__, template_folder="../client/templates")

# Route to serve the index.html file
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/bundle.js')
def bundle():
    return send_from_directory('dist', 'bundle.js')

@app.route('/bix')
def bix():
    return 'bix'

if __name__ == '__main__':
    app.run()

