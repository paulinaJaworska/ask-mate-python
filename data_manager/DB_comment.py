import db_connection

# CREATE #
# READ #
# UPDATE #
# DELETE #


@db_connection.connection_handler
def delete_comment(cursor, comment_id):
    cursor.execute("""DELETE FROM comment 
                    WHERE id =%s;""", comment_id)


@db_connection.connection_handler
def add_comment(cursor, data: dict):
    cursor.execute("""INSERT INTO comment
                      ( question_id, answer_id, message, submission_time, edited_count)
                      VALUES ( %(question_id)s, %(answer_id)s, %(message)s,
                       %(submission_time)s, %(edited_count)s)""", data)

@db_connection.connection_handler
def get_comment_by_id(cursor, _id: str):
    cursor.execute("""SELECT * FROM comment 
                        WHERE id =%s;""", _id)
    comment = cursor.fetchall()
    return comment

@db_connection.connection_handler
def get_comment_by_answer_id(cursor, answer_id):
    cursor.execute("""SELECT * FROM comment 
                    WHERE answer_id =%s;""", answer_id)
    comment = cursor.fetchall()
    return comment


@db_connection.connection_handler
def edit_comment(cursor, data):
    cursor.execute("""UPDATE comment
                      SET message = %(message)s, 
                      edited_count = +1,
                      submission_time = %(submission_time)s
                      WHERE id=%(id)s""", data)

@db_connection.connection_handler
def get_comments_by_question(cursor, question_id: str):
    quest_id = {'question_id': question_id}
    cursor.execute("""SELECT * FROM comment 
                    WHERE question_id = %(question_id)s;""", quest_id)
    comments = cursor.fetchall()
    return comments
