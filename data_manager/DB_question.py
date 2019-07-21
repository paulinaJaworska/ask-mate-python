import db_connection


# CREATE #

@db_connection.connection_handler
def add(cursor, question_data: dict):
    cursor.execute("""INSERT INTO question
                      (id, submission_time, view_number, vote_number, title, message, image)
                      VALUES (%(id)s, %(submission_time)s, %(view_number)s,
                       %(vote_number)s, %(title)s, %(message)s, %(image)s)""", question_data)


# READ #

@db_connection.connection_handler
def get_last_id(cursor):
    cursor.execute("""SELECT MAX(id) FROM question;""")
    latest_id_dict = cursor.fetchall()
    latest_id = latest_id_dict[0]['max']
    return latest_id


@db_connection.connection_handler
def get_all(cursor):
    cursor.execute("""SELECT * FROM question""")
    question_data = cursor.fetchall()
    return question_data


@db_connection.connection_handler
def sort(cursor, sort_by: str, order: bool):
    if order == 'True':
        order = 'DESC'
    else:
        order = 'ASC'
    cursor.execute("""SELECT * FROM question
                      ORDER BY """ + sort_by + " " + order)
    ordered_table = cursor.fetchall()
    return ordered_table


@db_connection.connection_handler
def get_by_id(cursor, _id: str):
    question_id = {'question_id': _id}
    cursor.execute("""
                       SELECT * FROM question
                       WHERE id=%(question_id)s""", question_id)
    question = cursor.fetchall()
    return question


@db_connection.connection_handler
def get_by_answer_id(cursor, answer_id: str):
    question_id = get_id_by_answer_id(answer_id)
    cursor.execute("""
                    SELECT * FROM question
                     WHERE id=%s""", question_id)
    questions = cursor.fetchall()
    return questions


@db_connection.connection_handler
def get_id_by_answer_id(cursor, answer_id):
    answer_id = {'answer_id': answer_id}
    cursor.execute("""
                    SELECT question_id FROM answer
                     WHERE id=%(answer_id)s""", answer_id)
    question_id = cursor.fetchone()
    return question_id


@db_connection.connection_handler
def get_id_by_comment(cursor, comment_id):
    comment_id = {'id': comment_id}
    cursor.execute("""
                    SELECT question_id FROM comment
                    WHERE id=%(id)s""", comment_id)
    question_id = cursor.fetchone()
    return question_id


@db_connection.connection_handler
def get_latest_five(cursor):
    cursor.execute("""SELECT * FROM question
                    ORDER BY submission_time DESC
                    LIMIT 5;""")
    latest_five_question = cursor.fetchall()
    return latest_five_question


# UPDATE #

@db_connection.connection_handler
def search_by_text(cursor, data):
    cursor.execute("""SELECT * FROM question
                    WHERE title ILIKE""" "'%" + data + "%' or message ILIKE '%" + data + "%';")
    questions = cursor.fetchall()
    return questions


# DELETE #

@db_connection.connection_handler
def edit(cursor, question_data: dict):
    cursor.execute("""UPDATE question
                      SET message = %(message)s, title = %(title)s, image = %(image)s
                      WHERE id=%(id)s""", question_data)


@db_connection.connection_handler
def delete(cursor, question_id: dict):
    cursor.execute("""
                      DELETE from QUESTION
                      WHERE id = %(question_id)s;
                      """, question_id)
# @db_connection.connection_handler
# def delete(cursor, question_id):
#     cursor.execute("""DELETE FROM question
#                       WHERE id=%s""", question_id)
