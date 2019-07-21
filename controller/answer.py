from controller import utils
from data_manager import DB_answer, DB_question

def add(form, question_id: str, image=None):
    answer = {'id': get_new_id(), 'submission_time': utils.date_generator(), 'message': form['message'],
              'question_id': question_id, 'vote_number': 0, 'image': form['image']}

    DB_answer.add(answer) # put an empty line between variables declaration and methods


def get(_id):
    return DB_answer.get_by_id(_id)[0]


def get_by_question(question_id: str):
    return DB_answer.get_by_question_id(question_id)


def edit(_id, message, image=None):
    item = get(_id)
    item['message'] = message
    item['image'] = image
    DB_answer.edit(item)
    item['message'] = message
    DB_answer.edit(item)


def delete(_id):
    DB_answer.delete(_id)


def get_new_id():
    return DB_answer.get_last_id() + 1