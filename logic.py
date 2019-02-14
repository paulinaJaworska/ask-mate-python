import data_manager
import time


def sort_questios(sort_by, order):
    question_data = data_manager.sort_questions(sort_by, order)
    return question_data


def get_questions():
    questions = data_manager.get_question_data()
    return questions


def new_question_id():
    last_id = data_manager.last_question_id()
    return last_id + 1


def date_generator():
    time_stamp = time.time()
    return int(time_stamp)


def new_question(title, message, image=None):
    question = {}
    question['id'] = new_question_id()
    question['submission_time'] = date_generator()
    question['title'] = title
    question['message'] = message
    question['image'] = image
    data_manager.save_new_question(question)

def get_latest_questions():    ###
    latest_five_questions = data_manager.get_latest_five_questions()
    return latest_five_questions


# ANSWERS

def get_question_by_id(_id):
    question = data_manager.get_question_by_id(_id)
    return question


def delete_question(_id: str):
    data_manager.delete_question(_id)
    data_manager.delete_answers_related_to_question(_id)
    return None

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
