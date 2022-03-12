from flask import Flask, render_template, redirect

app = Flask(__name__)

@app.route('/<n>')
def index(n):
    if int(n) > 1:
        return redirect('1')
    return render_template('index.html')

app.run(debug=True)