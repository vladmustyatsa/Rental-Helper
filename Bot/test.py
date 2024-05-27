from flask import Flask, render_template, redirect


app = Flask(__name__)

@app.route('/<city>/<k>')
def index(city, k):
    if int(k) > 1:
        return redirect('/not-found')
    return render_template('index.html')

@app.route('/not-found')
def not_found_page():
    return "<h1>Not Found 404<\h1>", 404


if __name__ == '__main__':
    app.run(debug=True, port=8888)