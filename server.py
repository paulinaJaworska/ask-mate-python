from flask import Flask, flash, redirect, render_template, \
     request, url_for
import csv_common


app = Flask(__name__)


@app.route('/')
@app.route('/list')
def index():
    questions = csv_common.get_question_data()
    return render_template('list.html', questions=questions)


@app.route('/question/<question_id>')
def question_page(question_id):
    question = csv_common.get_question_by_id(str(question_id))
    answers = csv_common.get_answers_by_question_id(str(question_id))
    return render_template('question.html', question=question, answers=answers)


@app.route("/add-question", methods=['GET'])
def new_question():
    return render_template('new_question.html')


@app.route("/add-question", methods=['POST'])
def post_new_question():
    form = request.form.to_dict()
    csv_common.save_new_question(form)
    identity = csv_common.last_question_id()
    return redirect("/question/%s" % identity)


@app.route("/<question_id>/new-answer", methods=['GET'])
def new_answer(question_id):
    question = csv_common.get_question_by_id(str(question_id))
    answers = csv_common.get_answers_by_question_id(str(question_id))
    return render_template('new_answer.html', question=question, answers=answers)


@app.route("/<question_id>/new-answer", methods=['POST'])
def post_new_answer(question_id):
    # save it to file
    form = request.form.to_dict()
    csv_common.save_new_answer(form, question_id)
    return redirect("/question/%s" % question_id)


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    csv_common.delete_question(question_id)
    return redirect('/')


@app.route("/sorted/")
def sorted_condition():
    sort_by = request.args.get('condition')
    order = request.args.get('order')
    questions = csv_common.sort_questions(sort_by, order)
    return render_template('list.html', questions=questions)


if __name__ == "__main__":
    app.run(debug=True,
            port=5000)
