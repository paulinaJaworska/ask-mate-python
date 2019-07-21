import db_connection


# CREATE #

@db_connection.connection_handler
def add(cursor, answer_data: dict):
    cursor.execute("""INSERT INTO answer
                      (id, submission_time, vote_number, question_id, message, image)
                      VALUES (%(id)s, %(submission_time)s, %(vote_number)s, %(question_id)s,
                       %(message)s, %(image)s)""", answer_data)


# READ #

@db_connection.connection_handler
def get_last_id(cursor):
    cursor.execute("""SELECT MAX(id) FROM answer;""")
    latest_id_dict = cursor.fetchall()
    latest_id = latest_id_dict[0]['max']
    return latest_id


@db_connection.connection_handler
def get_by_id(cursor, _id:str):
    answer_id = {'id': _id}
    cursor.execute("""
                       SELECT * FROM answer
                       WHERE id=%(id)s""", answer_id)
    answer = cursor.fetchall()
    return answer


@db_connection.connection_handler
def get_by_question_id(cursor, question_id: str):
    quest_id = {'question_id': question_id}
    cursor.execute("""
                           SELECT * FROM answer
                           WHERE question_id=%(question_id)s""", quest_id)
    answer = cursor.fetchall()
    return answer


@db_connection.connection_handler
def get_by_question_with_comments(cursor, question_id: str):
    quest_id = {'question_id': question_id}
    cursor.execute("""SELECT * FROM answer a LEFT JOIN comment c on a.id = c.answer_id
                    WHERE a.question_id=%(question_id)s""", quest_id)
    answers_with_comments = cursor.fetchall()
    return answers_with_comments


@db_connection.connection_handler
def search_by_text(cursor, data):
    cursor.execute("""SELECT * FROM answer
                    WHERE message ILIKE """ + "'%" + data + "%';")
    answers = cursor.fetchall()
    return answers


# UPDATE #

@db_connection.connection_handler
def edit(cursor, answer_data: dict):
    cursor.execute("""UPDATE answer
                      SET message = %(message)s
                      WHERE id=%(id)s""", answer_data)


# DELETE #

@db_connection.connection_handler
def delete(cursor, _id: str):
    id = {'id': _id}
    cursor.execute("""DELETE FROM answer
                      WHERE id=%(id)s""", id)
