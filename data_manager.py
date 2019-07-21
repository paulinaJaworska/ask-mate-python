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
    cursor.execute("""DELETE FROM question
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
def save_new_answer(cursor, answer_data: dict):
    cursor.execute("""INSERT INTO answer
                      (id, submission_time, vote_number, question_id, message, image)
                      VALUES (%(id)s, %(submission_time)s, %(vote_number)s, %(question_id)s,
                       %(message)s, %(image)s)""", answer_data)


@db_connection.connection_handler
def edit_question(cursor, question_data: dict):
    cursor.execute("""UPDATE question
                      SET message = %(message)s, title = %(title)s, image = %(image)s
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
    latest_five_question = cursor.fetchall()
    return latest_five_question


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

# COMMENT
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


## TAGS


@db_connection.connection_handler
def last_tag_id(cursor):
    cursor.execute(""" SELECT MAX(id) FROM tag;""")
    latest_id_dict = cursor.fetchall()
    latest_id = latest_id_dict[0]['max']
    return latest_id


@db_connection.connection_handler
def get_unique_tag_names(cursor):
    cursor.execute("""SELECT DISTINCT(name) FROM tag;""")
    unique_tags_names_dict = cursor.fetchall()
    return unique_tags_names_dict


@db_connection.connection_handler
def get_tags_by_question_id(cursor, question_id):
    question_id = {'question_id': question_id}
    cursor.execute("""SELECT * FROM tag
                      WHERE id IN (SELECT tag_id FROM question_tag
                                    WHERE question_id = %(question_id)s);""", question_id)
    tags_data = cursor.fetchall()

    return tags_data


@db_connection.connection_handler
def save_new_tag_and_question_tag(cursor, tag_data: dict, quest_id: str):
    tag_data['question_id'] = quest_id
    cursor.execute(""" INSERT INTO tag (id, name)
                        VALUES (%(id)s, %(name)s);
                        INSERT INTO question_tag (question_id, tag_id)
                        VALUES (%(question_id)s, %(id)s);  
                        """, tag_data)


@db_connection.connection_handler
def save_new_question_tag(cursor, tag_data: dict, question_id):
    cursor.execute("""INSERT INTO question_tag (question_id, tag_id)
                        VALUES (%(question_id)s, %(tag_id)s);
                        """, question_id, tag_data)



@db_connection.connection_handler
def delete_question_tag(cursor, question_id, tag_id):
    cursor.execute("""DELETE FROM question_tag
                      WHERE question_id = %(question_id)s 
                        AND tag_id = %(tag_id)s;""", question_id, tag_id)

@db_connection.connection_handler
def get_tags_id_realted_to_question(cursor, question_id):
    cursor.execute("""SELECT tag_id FROM question_tag
                        WHERE question_id =%s""", question_id)
    tags_id = cursor.fetchall()
    return tags_id

@db_connection.connection_handler
def get_ids_related_to_question(cursor, question_id):
    cursor.execute("""SELECT question_tag.tag_id, answer.id as answer_id, comment.id AS comment_id 
    from question_tag 
    inner join answer on question_tag.question_id=answer.question_id 
    inner join comment  on question_tag.question_id = comment.question_id
    WHERE answer.question_id =%s""", question_id)
    data = cursor.fetchall()
    return data

