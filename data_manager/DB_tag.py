import db_connection


# CREATE #

@db_connection.connection_handler
def add_to_question(cursor, tag_data: dict, quest_id: str):
    tag_data['question_id'] = quest_id
    cursor.execute(""" INSERT INTO tag (id, name)
                        VALUES (%(id)s, %(name)s);
                        INSERT INTO question_tag (question_id, tag_id)
                        VALUES (%(question_id)s, %(id)s);  
                        """, tag_data)


@db_connection.connection_handler
def add(cursor, tag_data: dict, question_id):
    cursor.execute("""INSERT INTO question_tag (question_id, tag_id)
                        VALUES (%(question_id)s, %(tag_id)s);
                        """, question_id, tag_data)


# READ #

@db_connection.connection_handler
def get_last_id(cursor):
    cursor.execute(""" SELECT MAX(id) FROM tag;""")
    latest_id_dict = cursor.fetchall()
    latest_id = latest_id_dict[0]['max']
    return latest_id


@db_connection.connection_handler
def get_unique_names(cursor):
    cursor.execute("""SELECT DISTINCT(name) FROM tag;""")
    unique_tags_names_dict = cursor.fetchall()
    return unique_tags_names_dict


@db_connection.connection_handler
def get_by_question_id(cursor, question_id):
    question_id = {'question_id': question_id}
    cursor.execute("""SELECT * FROM tag
                      WHERE id IN (SELECT tag_id FROM question_tag
                                    WHERE question_id = %(question_id)s);""", question_id)
    tags_data = cursor.fetchall()

    return tags_data


@db_connection.connection_handler
def get_id_by_question_id(cursor, question_id):
    cursor.execute("""SELECT tag_id FROM question_tag
                        WHERE question_id =%s""", question_id)
    tags_id = cursor.fetchall()
    return tags_id


# UPDATE #


# DELETE #

@db_connection.connection_handler
def delete(cursor, question_id, tag_id):
    cursor.execute("""DELETE FROM question_tag
                      WHERE question_id = %(question_id)s 
                        AND tag_id = %(tag_id)s;""", question_id, tag_id)
