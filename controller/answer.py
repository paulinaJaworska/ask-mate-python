import time            # first import foreign libraries
import datetime

from data_manager import DB_answer, DB_comment, DB_question, DB_tag # project modules





# ANSWERS                              # podzielić logikę data manager na oddzielne pliki dla question, answer itd.
# dzięki temu możemy tworzyć nazwy metod typu question.delete


def new_answer_id():
    last_id = DB_answer.get_last_id()
    return last_id + 1


def get_answer_by_id(_id):
    answer = DB_answer.get_by_id(_id)
    return answer[0]


def new_answer(form, question_id: str, image=None):
    answer = {}
    answer['id'] = new_answer_id()
    answer['submission_time'] = date_generator()
    answer['message'] = form['message']
    answer['question_id'] = question_id
    answer['vote_number'] = 0
    answer['image'] = form['image']
    # oddzielać definicje zmiennych od metod
    DB_answer.add(answer)


def get_answers_by_question_id(question_id: str):
    answer = DB_answer.get_by_question_id(question_id)
    return answer


def delete_answer(_id):
    DB_answer.delete(_id)


def get_question_id_by_answer_id(answer_id):
    question_id_dict = DB_question.get_by_answer_id(answer_id)
    question_id = question_id_dict[0]['question_id']
    return question_id


def edit_answer(_id, message, image=None):
    item = get_answer_by_id(_id)
    item['message'] = message
    item['image'] = image
    DB_answer.edit(item)
    item['message'] = message
    DB_answer.edit(item)

