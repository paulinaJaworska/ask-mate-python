from flask import Flask, flash, redirect, render_template, \
     request, url_for
import common
getcounter = 0
postcounter = 0

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def index():
    questions= common.question_data
    return render_template('list.html', questions =questions)


@app.route('/question/<question_id>')
def question_page(id):
    return render_template ('question.html', id=id )


if __name__ == "__main__":
    app.run(debug=True,
            port = 5000)
