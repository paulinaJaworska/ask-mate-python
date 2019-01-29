from flask import Flask, flash, redirect, render_template, \
     request, url_for

getcounter=0
postcounter=0

app = Flask(__name__)



@app.route('/')
@app.route('/list')
def index():
    return render_template('list.html', questions = questions)


    
if __name__ == "__main__":
    app.run(debug=True,
            port = 5000)