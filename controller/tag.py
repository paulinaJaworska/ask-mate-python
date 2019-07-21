from data_manager import DB_tag
from controller import answer, comment


def add(form, question_id):
    del form['image']

    tag_data = {'id': new_tag_id()}
    tag_names_dict = DB_tag.get_unique_names()

    names = []

    for i in tag_names_dict:
        names.append(i['name'])
    if form['message'] in names:
        DB_tag.add(question_id)
    else:
        tag_data['name'] = form['message'].lower()
        DB_tag.add_to_question(tag_data, question_id)


def get_by_question(question_id):
    return DB_tag.get_by_question_id(question_id)


def delete_by_id_and_question_id(question_id, tag_id):  # todo: refactor to use only tag_id
    DB_tag.delete(question_id, tag_id)


def get_unique_names():
    return DB_tag.get_unique_names()


def get_ids_by_question(question_id):
    return DB_tag.get_id_by_question_id(question_id)


def get_ids_related_to_question(question_id):
    data = {}
    answers_ids = []
    comments_ids = []
    comments_for_answers = []

    answers = answer.get_by_question(question_id)
    for item in answers:
        answers_ids.append(item['id'])

    comments = comment.get_comment_by_question_id(question_id)
    for item in comments:
        comments_ids.append(item['id'])

    for item in answers_ids:
        for i in comment.get_comment_by_answer_id(str(item)):
            comments_for_answers.append(i['id'])

    data['question_id'] = question_id
    data['answer_id'] = answers_ids
    data['comment_id'] = comments_ids
    data['tag_id'] = get_ids_by_question(question_id)[0]  # todo: remove magic numbers
    data['comments_for_answers'] = comments_for_answers

    return data


def new_tag_id():
    return DB_tag.get_last_id() + 1
