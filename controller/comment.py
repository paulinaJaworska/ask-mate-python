from controller import utils
from data_manager import DB_comment


def add(message: dict, question_id=None, answer_id=None):
    comment = {'submission_time': utils.date_generator(), 'message': message['message'], 'question_id': question_id,
               'answer_id': answer_id, 'vote_number': 0, 'edited_count': 0}
    DB_comment.add(comment)


def get_by_id(_id):
    return DB_comment.get_by_id(_id)


def get_by_question(_id):
    return DB_comment.get_by_question_id(_id)


def get_by_answer_id(_id: str):
    return DB_comment.get_by_answer_id(_id)


def edit(_id: str, message: str):
    data = {'id': _id, 'message': message, 'submission_time': utils.date_generator()}
    print(data)
    DB_comment.edit(data)


def delete(comment_id):
    DB_comment.delete(comment_id)
