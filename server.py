from flask import Flask, flash, redirect, render_template, \
     request, url_for
import logic


app = Flask(__name__)


@app.route('/')
def route_latest_questions():
    latest_questions = logic.get_latest_questions()
    return render_template('list.html', questions=latest_questions)


@app.route('/list')
def index():
    questions = logic.get_question_data()
    return render_template('list.html', questions=questions)


@app.route('/question/<question_id>')
def question_page(question_id):
    question = logic.get_question_by_id(str(question_id))
    answers = logic.get_answers_by_question_id(str(question_id))
    return render_template('question.html', question=question, answers=answers)


@app.route('/question/<question_id>/edit', methods=['GET'])
def route_edit_question(question_id):
    question_details = logic.get_question_by_id(question_id)
    return render_template('new_question.html', question=question_details, edition=True)


@app.route('/question/<question_id>/edit', methods=['POST'])
def edit_question(question_id):
    logic.edit_question(question_id)
    return redirect('/question/<question_id>')


@app.route("/add-question", methods=['GET'])
def new_question():
    return render_template('new_question.html')


@app.route("/add-question", methods=['POST'])
def post_new_question():
    form = request.form.to_dict()
    logic.save_new_question(form)
    identity = logic.last_question_id()
    return redirect("/question/%s" % identity)


@app.route("/<question_id>/new-answer", methods=['GET'])
def new_answer(question_id):
    question = logic.get_question_by_id(str(question_id))
    answers = logic.get_answers_by_question_id(str(question_id))
    return render_template('new_answer.html', question=question, answers=answers)


@app.route("/<question_id>/new-answer", methods=['POST'])
def post_new_answer(question_id):
    # save it to file
    form = request.form.to_dict()
    logic.save_new_answer(form, question_id)
    return redirect("/question/%s" % question_id)


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    logic.delete_question(question_id)
    return redirect('/')


@app.route("/sorted/")
def sorted_condition():
    sort_by = request.args.get('condition')
    order = request.args.get('order')
    questions = logic.sort_questions(sort_by, order)
    return render_template('list.html', questions=questions)


if __name__ == "__main__":
    app.run(debug=True,
            port=5000)
