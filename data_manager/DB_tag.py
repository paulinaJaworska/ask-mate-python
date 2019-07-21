import db_connection

# CREATE #
# READ #
# UPDATE #
# DELETE #


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
