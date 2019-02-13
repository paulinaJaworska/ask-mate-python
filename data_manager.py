import db_connection
import time


# returns last question id as integer
@db_connection.connection_handler
def last_question_id(cursor):
    cursor.execute("""SELECT MAX(id) FROM question;""")
    latest_id_dict = cursor.fetchall()
    latest_id = latest_id_dict[0]['max']
    return latest_id


@db_connection.connection_handler
def get_question_data(cursor):
    cursor.execute("""SELECT * FROM question""")
    question_data = cursor.fetchall()
    return question_data


@db_connection.connection_handler
def sort_questions(cursor, sort_by: str, order: bool):
    '''
    Sorts list of dictionaies by given parameter in ascending or descending order.
    :param list_of_dictionaries:
    :param sort_by: key by which we want to sort by
    :param order: boolean (True or False)  True = descending
    :return: sorted list of dicts
    '''

    if order:
        order = 'DESC'
    else:
        order = 'ASC'
    print(order)
    cursor.execute("""SELECT * FROM question
                      ORDER BY """ + sort_by + " " + order)
    ordered_table = cursor.fetchall()
    return ordered_table


@db_connection.connection_handler
def get_question_by_id(cursor, question_id: str):
    cursor.execute("""
                       SELECT * FROM question
                       WHERE id=%s""", question_id)
    question = cursor.fetchall()
    return question


@db_connection.connection_handler
def get_answers_by_question_id(cursor, question_id: str):
    cursor.execute("""
                           SELECT * FROM answer
                           WHERE question_id=%s""", question_id)
    answer = cursor.fetchall()
    return answer


@db_connection.connection_handler
def delete_question(cursor, question_id):
    cursor.execute("""DELETE * FROM question
                      WHERE id=%s""", question_id)


@db_connection.connection_handler
def save_new_question(cursor, question_data: dict):
    cursor.execute("""INSERT INTO question
                      (id, submission_time, view_number, vote_number, title, message, image)
                      VALUES (%(id)s, %(id)s, %(id)s, %(id)s, %(id)s, %(id)s, %(id)s)""", question_data)


def save_new_answer(answer_data, question_id):
    global ANSWER_LABELS
    global ANSWER_FILE
    filled_answer_data = prepare_data_for_answer_data(answer_data, question_id)
    csv_data_manager.export_data(ANSWER_FILE, ANSWER_LABELS, filled_answer_data)


def delete_answers_related_to_question(question_id):
    '''
    Deletes answers retated to question from csv
    :param question_id:
    :param filename:
    :return: nothing
    '''
    filename = 'sample_data/answer.csv'
    answers = csv_data_manager.import_data(filename)
    for answer in answers:
        if answer["question_id"] == question_id:
            answers.remove(answer)
    global ANSWER_LABELS
    csv_data_manager.update_data(filename, ANSWER_LABELS, answers)


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
    questions = csv_data_manager.import_data(filename)
    for question in questions:
        if question["id"] in id_:
            questions.remove(question)
    global QUESTION_LABELS
    csv_data_manager.update_data(filename, QUESTION_LABELS, questions)
    delete_answers_related_to_question(id_)