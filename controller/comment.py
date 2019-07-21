import time            # first import foreign libraries
import datetime

from data_manager import DB_answer, DB_comment, DB_question, DB_tag # project modules


def add_comment(message : dict, question_id = None, answer_id = None):
    comment = {}
    comment['submission_time'] = date_generator()
    comment['message'] = message['message']
    comment['question_id'] = question_id
    comment['answer_id'] = answer_id
    comment['vote_number'] = 0
    comment['edited_count'] = 0
    DB_comment.add(comment)


def delete_comment(comment_id):
    DB_comment.delete(comment_id)


def get_comment_by_id(_id):
    data = DB_comment.get_by_id(_id)
    return data


def get_comment_by_question_id(_id):
    data = DB_comment.get_comment_by_question_id(_id)
    return data


def get_comment_by_answer_id(_id: str):
    data = DB_comment.get_by_answer_id(_id)
    return data


def edit_comment(_id: str, message: str):
    data = {}
    data['id'] = _id
    data['message']= message
    data['submission_time'] = date_generator()
    print(data)
    DB_comment.edit(data)

def get_question_comments_by_question_id(question_id: str):
    return DB_comment.get_by_question_id(question_id)
