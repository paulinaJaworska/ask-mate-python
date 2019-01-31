from flask import Flask, flash, redirect, render_template, \
     request, url_for
import common


app = Flask(__name__)


@app.route('/')
@app.route('/list')
def index():
    questions = common.get_question_data()
    return render_template('list.html', questions=questions)


@app.route('/question/<question_id>')
def question_page(question_id):
    question = common.get_question_by_id(str(question_id))
    answers = common.get_answers_by_question_id(str(question_id))
    return render_template('question.html', question=question, answers=answers)


@app.route("/add-question", methods=['GET'])
def new_question():
    return render_template('new_question.html')


@app.route("/add-question", methods=['POST'])
def post_new_question():
    form = request.form.to_dict()
    common.save_new_question(form)
    identity = common.last_question_id()
    return redirect("/question/%s" % identity)


@app.route("/<question_id>/new-answer", methods=['GET'])
def post_new_answer(question_id):
    question = common.get_question_by_id(str(question_id))
    answers = common.get_answers_by_question_id(str(question_id))
    return render_template('new_answer.html', question=question, answers=answers)



@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    common.delete_question(question_id)
    redirect('/')


@app.route("/sorted/")
def sorted_condition():
    sort_by = request.args.get('condition')
    order = request.args.get('order')
    questions = common.sort_questions(sort_by, order)
    return render_template('list.html', questions = questions)


if __name__ == "__main__":
    app.run(debug=True,
            port=5000)
