import data_manager
import os
import csv
import time

QUESTION_LABELS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWER_LABELS = ["id", "submission_time", "vote_number", "question_id", "message", "image"]
# parameters to call the import data: filename = "data/answers.csv" or filename = "data/questions.csv"


QUESTION_FILE = 'sample_data/question.csv'
ANSWER_FILE = 'sample_data/answer.csv'


def last_question_id():
    return data_manager.get_last_question_id()


### SORTING  ###
def sort_questions(sort_by, order):
    '''
    Sorts list of dictionaies by given parameter in ascending or descending order.
    :param list_of_dictionaries:
    :param sort_by: key by which we want to sort by
    :param order: boolean (True or False)  True = descending
    :return: sorted list of dicts
    '''
    if order == "desc":
        order = True
    else:
        order = False

    global QUESTION_FILE
    list_of_dictionaries = data_manager.import_data(QUESTION_FILE)
    return sorted(list_of_dictionaries, key=lambda i: i[str(sort_by)], reverse=order)


###  FUNCTIONS READING CSV FILES AND   ###sample


def get_question_data():
    question_data = sort_questions("submission_time", True)
    return question_data


### Pulling from database  ###


###   WRITING TO CSV   ###

def id_generator(filename):
    exists = os.path.isfile(filename)
    if not exists:
        return 1
    else:
        with open(filename, 'r') as f:
            result = csv.DictReader(f)
            for row in result:
                result = row["id"]
            return int(result) + 1


def date_generator():
    time_stamp = time.time()
    return int(time_stamp)


def prepare_data_for_questions_data(question_data_from_form):
    """
    Append necessary data, which is not enter by user, to data from question form filled by user.
    :param question_data_from_form: dictionary
    :return: dictionary
    """

    next_id = id_generator('sample_data/question.csv')
    submission_time = date_generator()
    view_number = "not implemented"
    vote_number = "not implemented"
    image = "no image"
    generated_automatically = {'id': next_id, "submission_time": submission_time, "view_number": view_number,
                               "vote_number": vote_number, "image": image}
    question_data_from_form.update(generated_automatically)
    return question_data_from_form


def prepare_data_for_answer_data(answer_data_form_form, question_id):
    # "id", "submission_time", "vote_number", "question_id", "message", "image"
    next_id = id_generator('sample_data/answer.csv')
    submission_time = date_generator()
    vote_number = "not implemented"
    image = "no image"
    message = list(answer_data_form_form.values())

    generated_automatically = {'id': next_id, "submission_time": submission_time,
                               "vote_number": vote_number, "question_id": question_id,
                               "message": message[0], "image": image}
    return generated_automatically


def get_question_by_id(_id):
    _id = str(_id)
    question_data = get_question_data()
    for item in question_data:
        if item['id'] == _id:
            return item


def get_answers_by_question_id(_id):
    global ANSWER_FILE
    answer_data = data_manager.import_data(ANSWER_FILE)
    _id = str(_id)
    answers = []
    for item in answer_data:
        if item['question_id'] == _id:
            answers.append(item)
    return answers


def delete_question(_id):
    delete_question(_id)
    delete_answers_related_to_question(_id)


# !!! Function that should be used to save question in the csv file.
def save_new_question(question_data):
    global QUESTION_LABELS
    global QUESTION_FILE
    filled_question_data = prepare_data_for_questions_data(question_data)
    # used to add id and time to dictionary
    data_manager.export_data(QUESTION_FILE, QUESTION_LABELS, filled_question_data)


def save_new_answer(answer_data, question_id):
    global ANSWER_LABELS
    global ANSWER_FILE
    filled_answer_data = prepare_data_for_answer_data(answer_data, question_id)
    data_manager.export_data(ANSWER_FILE, ANSWER_LABELS, filled_answer_data)


def delete_answers_related_to_question(question_id):
    '''
    Deletes answers retated to question from csv
    :param question_id:
    :param filename:
    :return: nothing
    '''
    filename = 'sample_data/answer.csv'
    answers = data_manager.import_data(filename)
    for answer in answers:
        if answer["question_id"] == question_id:
            answers.remove(answer)
    global ANSWER_LABELS
    data_manager.update_data(filename, ANSWER_LABELS, answers)


def delete_question(id_):
    '''
    1. Delete question form list of dictionaries
    2. write it to file
    3. Delete answers retated to question from csv
    :param id_: str - id of question record to be deleted
    :param filename: str
    :return: nothing
    '''
    filename = 'sample_data/question.csv'
    questions = data_manager.import_data(filename)
    for question in questions:
        if question["id"] in id_:
            questions.remove(question)
    global QUESTION_LABELS
    data_manager.update_data(filename, QUESTION_LABELS, questions)
    delete_answers_related_to_question(id_)
