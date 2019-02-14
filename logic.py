import data_manager
import time
import datetime

# questions

def get_question_by_id(_id):
    question = data_manager.get_question_by_id(_id)
    return question


def delete_question(_id: str):
    data_manager.delete_question(_id)
    data_manager.delete_answers_related_to_question(_id)
    return None


def sort_questios(sort_by, order):
    question_data = data_manager.sort_questions(sort_by, order)
    return question_data


def get_questions():
    questions = data_manager.get_question_data()
    return questions


def new_question_id():
    last_id = data_manager.last_question_id()
    return last_id + 1


def edit_question(_id, message, title):
    item = get_question_by_id(_id)
    for i in item:
        i['message'] = message
        i['title'] = title
    return i


def date_generator():
    time_stamp = time.time()
    st = datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
    return str(st)

print(date_generator())

def new_question(title, message, image=None):
    question = {}
    question['id'] = new_question_id()
    question['submission_time'] = date_generator()
    question['title'] = title
    question['message'] = message
    question['image'] = image
    data_manager.save_new_question(question)


new_question('testowy', 'powinno byc ok')
# ANSWERS


def new_answer_id():
    last_id = data_manager.last_answer_id()
    return last_id + 1


def new_answer(title, message, question_id: str):
    answer = {}
    answer['id'] = new_answer_id()
    answer['submission_time'] = date_generator()
    answer['title'] = title
    answer['message'] = message
    answer['question_id'] = question_id
    data_manager.save_new_answer(answer)


def get_answer_by_question_id(_id: str):
    answer = data_manager.get_answers_by_question_id(_id)
    return answer


def delete_answer(_id):
    data_manager.delete_answer(_id)
