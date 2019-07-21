import db_connection


# CREATE #

@db_connection.connection_handler
def add(cursor, data: dict):
    cursor.execute("""INSERT INTO comment
                      ( question_id, answer_id, message, submission_time, edited_count)
                      VALUES ( %(question_id)s, %(answer_id)s, %(message)s,
                       %(submission_time)s, %(edited_count)s)""", data)


# READ #

@db_connection.connection_handler
def get_by_id(cursor, _id: str):
    comment_id = {'id': _id}
    cursor.execute("""SELECT * FROM comment 
                        WHERE id =%(id)s;""", comment_id)
    comment = cursor.fetchone()
    return comment


@db_connection.connection_handler
def get_all(cursor):
    cursor.execute("""SELECT * FROM comment""")
    comments = cursor.fetchall()
    return comments


@db_connection.connection_handler
def get_by_answer_id(cursor, answer_id):
    cursor.execute("""SELECT * FROM comment 
                    WHERE answer_id =%s;""", answer_id)
    comment = cursor.fetchall()
    return comment


@db_connection.connection_handler
def get_by_question_id(cursor, question_id: str):
    quest_id = {'question_id': question_id}
    cursor.execute("""SELECT * FROM comment 
                    WHERE question_id = %(question_id)s;""", quest_id)
    comments = cursor.fetchall()
    return comments


@db_connection.connection_handler
def get_edited_count(cursor, comment_id: str):
    comm_id = {'id': comment_id}
    cursor.execute("""SELECT edited_count FROM comment
                    WHERE id=%(id)s;""", comm_id)
    edited_count = cursor.fetchone()
    return edited_count


# UPDATE #

@db_connection.connection_handler
def edit(cursor, data):
    cursor.execute("""UPDATE comment
                      SET message = %(message)s, 
                      edited_count = %(edited_count)s,
                      submission_time = %(submission_time)s
                      WHERE id=%(id)s""", data)


# DELETE #

@db_connection.connection_handler
def delete(cursor, comment_id):
    comm_id = {'id':comment_id}
    cursor.execute("""DELETE FROM comment 
                    WHERE id =%(id)s;""", comm_id)
