from controller import utils
from data_manager import DB_answer, DB_question


def add(form: dict):
    question = {'id': get_new_id(), 'submission_time': utils.date_generator(), 'title': form['title'],
                'message': form['message'], 'image': form['image'], 'view_number': 0, 'vote_number': 0}
    DB_question.add(question)
    return question


def get(_id: str):  # we usually get things by id by default do we add by_sth only otherwise
    return DB_question.get_by_id(_id)[0]


def get_all():
    return DB_question.get_all()


def get_sorted(sort_by, order):
    return DB_question.sort(sort_by, order)


def get_latest_five():
    return DB_question.get_latest_five()


def get_id_by_answer(answer_id):
    question_id_dict = DB_question.get_by_answer_id(answer_id)
    return question_id_dict[0]['question_id']


def search(data: str):
    questions_found = []
    questions = (DB_question.search_by_text(data))
    for i in questions:
        questions_found.append(i)
    answers = DB_answer.search_by_text(data)
    for i in answers:
        answer_id = i['id']
        questions_found.append(get(answer_id))

    return questions_found


def edit(_id, message, title, image):
    item = get(_id)
    item['message'] = message  # Don't change
    item['title'] = title
    item['image'] = image

    DB_question.edit(item)


def delete(_id: str):
    _id = str(_id)
    dict_id = {'question_id': _id}
    DB_question.delete(dict_id)


def get_new_id():
    return DB_question.get_last_id() + 1
