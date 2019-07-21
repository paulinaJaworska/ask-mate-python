from flask import Flask, redirect, render_template, request, url_for
from controller import answer, question, comment, tag

app = Flask(__name__)
app.static_folder = 'static'


@app.route('/')
def route_latest_questions():
    latest_questions = question.get_latest_five()
    return render_template('list.html',
                           form_url=url_for('route_latest_questions'),
                           latest_questions=latest_questions)


@app.route('/list')
def index():
    questions = question.get_all()

    return render_template('list.html',
                           form_url=url_for('index'),
                           questions=questions)


@app.route("/add-question", methods=['GET'])
def route_new_question():                              # zamiast route użyć show lub display

    return render_template('edit.html',
                           form_url=url_for('route_new_question'),            # takie rzeczy wrzycać w słownik w route
                           edit_question={'title': ''},
                           button_title='Add Question',
                           )


@app.route("/add-question", methods=['POST'])
def new_question():
    form = request.form.to_dict()
    question = question.new_question(form)
    question_id = question['id']

    return redirect('/question/%s' % question_id)


@app.route('/question/<int:question_id>')    # tworzyć też zabespieczenie typu zmiennnej na wysokości route int:question id
def question_page(question_id):                                 # wprowadzić try: expect: np. na TypeError
    question = question.get_question_by_id(question_id)
    answers = answer.get_by_question(question_id)
    tags = tag.get_tags_by_question_id(question_id)
    question_comments = comment.get_question_comments_by_question_id(question_id)

    return render_template('question.html',
                           question=question,
                           answers=answers,
                           question_comments=question_comments,
                           tags=tags)


@app.route('/question/<question_id>/edit', methods=['GET'])
def route_edit_question(question_id):
    question = question.get_question_by_id(question_id)

    return render_template('edit.html',
                           form_url=url_for('route_edit_question',
                                            question_id=question_id),
                           edit_question=question,
                           button_title='Save Changes',
                           edition=True)


@app.route('/question/<question_id>/edit', methods=['POST'])
def edit_question(question_id):
    new_data = request.form.to_dict()
    message = new_data["message"]
    title = new_data["title"]
    image = new_data["image"]

    question.edit(question_id, message, title, image)

    return redirect('/question/%s' % question_id)


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    question.delete(question_id)

    return redirect('/')


# ANSWERS


@app.route('/answer/<answer_id>/edit', methods=['GET'])
def route_edit_answer(answer_id):
    answer = answer.get_answer_by_id(answer_id)

    return render_template('edit.html',
                           form_url=url_for('route_edit_answer',
                                            answer_id=answer_id),
                           edit=answer,
                           button_title='Save Changes',
                           edition=True)


@app.route('/answer/<answer_id>/edit', methods=['POST'])
def edit_answer(answer_id):
    new_data = request.form.to_dict()
    message = new_data["message"]
    question_id = question.get_question_id_by_answer_id(answer_id)
    image = new_data["image"]
    answer.edit(answer_id, message, image)

    return redirect('/question/%s' % question_id)


@app.route("/<question_id>/new-answer", methods=['GET'])
def route_new_answer(question_id: str):
    question = question.get_question_by_id(question_id)

    return render_template('edit.html',
                           question=question,
                           button_title='Add Answer')


@app.route("/<question_id>/new-answer", methods=['POST'])
def new_answer(question_id):
    # save it to file
    form = request.form.to_dict()
    answer.add(form, question_id)

    return redirect("/question/%s" % question_id)


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id: str):
    question_id = answer.get_by_answer(answer_id)
    answer.delete(answer_id)

    return redirect('/question/%s' % question_id)


@app.route("/sorted/")
def sorted_condition():
    sort_by = request.args.get('sort_by')
    order = request.args.get('order')
    questions = question.get_sorted(sort_by, order)

    return render_template('list.html',
                           questions=questions,
                           sort_by=sort_by,
                           order=order)


@app.route("/search/", methods=['POST'])
def search():
    phrase = request.form['phrase']
    question_search = question.search(phrase)

    return render_template('list.html',
                           question_search=question_search)


# COMMENTS


@app.route('/question/<question_id>/new-comment', methods=['GET'])
def route_add_comment_to_question(question_id: str):
    question = question.get_question_by_id(question_id)

    return render_template('edit.html',
                           question=question,
                           button_title='Add Comment')


@app.route('/question/<question_id>/new-comment', methods=['POST'])
def new_question_comment(question_id):
    comment = request.form.to_dict()
    comment.add_comment(comment, question_id)

    return redirect("/question/%s" % question_id)


@app.route('/answer/<answer_id>/new-comment', methods=['GET'])
def route_add_comment_to_answer():

    return render_template('edit.html')


@app.route('/answer/<answer_id>/new-comment', methods=['POST'])
def add_comment_to_answer(answer_id):
    comment = request.form.to_dict()
    question_id = question.get_question_id_by_answer_id(answer_id)
    comment.add_comment_to_answer(comment, answer_id, question_id)

    return redirect("/question/%s" % question_id)


@app.route('/comments/<comment_id>/edit', methods=['GET'])
def route_edit_comment(comment_id):
    comment = comment.get_comment_by_id(comment_id)

    return render_template('edit.html',
                           edit_comment=comment)


@app.route('/comments/<comment_id>/edit', methods=['POST'])
def edit_comment(comment_id):
    edited_count = comment.get_edited_count() + 1

    new_comment = request.form.to_dict()
    answer_id = comment.get_comment_by_id(comment_id)['answer_id']  #
    question_id = question.get_question_id_by_answer_id(answer_id)
    comment.edit_comment(comment_id, new_comment, edited_count)

    return redirect("/question/%s" % question_id)


# TAGS

@app.route('/question/<question_id>/new-tag', methods=['GET'])
def route_new_tag(question_id):
    all_tags = tag.get_unique_tag_names()

    return render_template('edit.html',
                           form_url=url_for('route_new_tag',
                                            question_id=question_id),
                           tags=all_tags,
                           button_title='Add Tag')


@app.route('/question/<question_id>/new-tag', methods=['POST'])
def new_tag(question_id):
    tag = request.form.to_dict()
    tag.add_new_tag(tag, question_id)

    return redirect("/question/%s" % question_id)


@app.route('/question/<question_id>/tag/<tag_id>/delete', methods=['POST'])
def delete_question_tag(question_id, tag_id):
    tag.delete_question_tag_by_question_id(question_id, tag_id)

    return redirect("/question/%s" % question_id)


if __name__ == "__main__":
    app.run(debug=True,
            port=5000)
