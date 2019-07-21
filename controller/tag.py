import time            # first import foreign libraries
import datetime

from data_manager import DB_answer, DB_comment, DB_question, DB_tag # project modules




def new_tag_id():
    last_id = DB_tag.get_last_id()
    return last_id + 1


def get_tags_by_question_id(question_id):
    tags_for_question = DB_tag.get_by_question_id(question_id)

    return tags_for_question


def add_new_tag(form, question_id):
    del form['image']

    tag_data = {}
    tag_data['id'] = new_tag_id()
    print(tag_data)
    tag_names_dict = DB_tag.get_unique_names()
    print(tag_names_dict)

    names = []

    for i in tag_names_dict:
        names.append(i['name'])
    print(names)
    print(form['message'])
    if form['message'] in names:  ###
        DB_tag.add(question_id)
    else:
        tag_data['name'] = form['message'].lower()  ###
        DB_tag.add_to_question(tag_data, question_id)


def delete_question_tag_by_question_id(question_id, tag_id):
    DB_tag.delete(question_id, tag_id)


def get_unique_tag_names():
    unique_tag_names = DB_tag.get_unique_names()

    return unique_tag_names


def get_tags_ids_related_to_question(question_id):
    ids = DB_tag.get_id_by_question_id(question_id)
    return ids


def get_ids_related_to_question(question_id):
    data ={}
    answers_ids = []
    comments_ids = []
    comments_for_answers = []

    a = get_answers_by_question_id(question_id)
    for item in a:
        answers_ids.append(item['id'])


    c = get_comment_by_question_id(question_id)
    for item in c:
        comments_ids.append(item['id'])

    for item in answers_ids:
        for i in get_comment_by_answer_id(str(item)):
            comments_for_answers.append(i['id'])

    data['question_id'] = question_id
    data['answer_id'] = answers_ids
    data['comment_id'] = comments_ids
    data['tag_id'] = get_tags_ids_related_to_question(question_id)[0]
    data['comments_for_answers'] = comments_for_answers
    return data