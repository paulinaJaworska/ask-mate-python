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
def last_answer_id(cursor):
    cursor.execute("""SELECT MAX(id) FROM answer;""")
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

    if order == 'True':
        order = 'DESC'
    else:
        order = 'ASC'
    print(order)
    cursor.execute("""SELECT * FROM question
                      ORDER BY """ + sort_by + " " + order)
    ordered_table = cursor.fetchall()
    return ordered_table


@db_connection.connection_handler
def get_question_by_id(cursor, _id: str):
    question_id = {'question_id': _id}
    cursor.execute("""
                       SELECT * FROM question
                       WHERE id=%(question_id)s""", question_id)
    question = cursor.fetchall()
    return question


@db_connection.connection_handler
def get_answer_by_id(cursor, _id: str):
    cursor.execute("""
                       SELECT * FROM answer
                       WHERE id=%s""", _id)
    answer = cursor.fetchall()
    return answer


@db_connection.connection_handler
def get_question_id_by_answer_id(cursor, answer_id: str):
    cursor.execute("""
                    SELECT question_id FROM answer
                     WHERE id=%s""", answer_id)
    question_id = cursor.fetchall()
    return question_id


@db_connection.connection_handler
def get_answers_by_question_id(cursor, question_id: str):
    quest_id = {'question_id': question_id}
    cursor.execute("""
                           SELECT * FROM answer
                           WHERE question_id=%(question_id)s""", quest_id)
    answer = cursor.fetchall()
    return answer


@db_connection.connection_handler
def delete_question(cursor, question_id):
    cursor.execute("""DELETE * FROM question
                      WHERE id=%s""", question_id)


@db_connection.connection_handler
def delete_answer(cursor, _id: str):
    cursor.execute("""DELETE FROM answer
                      WHERE id=%s""", _id)


@db_connection.connection_handler
def save_new_question(cursor, question_data: dict):
    cursor.execute("""INSERT INTO question
                      (id, submission_time, view_number, vote_number, title, message, image)
                      VALUES (%(id)s, %(submission_time)s, %(view_number)s,
                       %(vote_number)s, %(title)s, %(message)s, %(image)s)""", question_data)


@db_connection.connection_handler
def save_new_answer(cursor, answer_data):
    cursor.execute("""INSERT INTO answer
                      (id, submission_time, vote_number, question_id, message, image)
                      VALUES (%(id)s, %(submission_time)s, %(vote_number)s, %(question_id)s,
                       %(message)s, %(image)s)""", answer_data)


@db_connection.connection_handler
def edit_question(cursor, question_data: dict):
    cursor.execute("""UPDATE question
                      SET message =%(message)s, title =%(title)s
                      WHERE id=%(id)s""", question_data)


@db_connection.connection_handler
def delete_question(cursor, question_id: dict):
    cursor.execute("""
                      DELETE from QUESTION
                      WHERE id = %(question_id)s;
                      """, question_id)


@db_connection.connection_handler
def get_latest_five_questions(cursor):
    cursor.execute("""SELECT * FROM question
                    ORDER BY submission_time DESC
                    LIMIT 5;""")


@db_connection.connection_handler
def edit_answer(cursor, answer_data: dict):
    cursor.execute("""UPDATE answer
                      SET message =%(message)s
                      WHERE id=%(id)s""", answer_data)


@db_connection.connection_handler
def search_in_questions(cursor, data):
    cursor.execute("""SELECT * FROM question
                    WHERE title ILIKE""" "'%" + data + "%' or message ILIKE '%"+ data + "%';")
    questions = cursor.fetchall()
    return questions


@db_connection.connection_handler
def search_in_answers(cursor, data):
    cursor.execute("""SELECT * FROM answer
                    WHERE message ILIKE """+"'%"+ data + "%';")
    answers = cursor.fetchall()
    return answers



