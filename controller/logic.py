import time            # najpierw zewnętrzne
import datetime
                        # spacja
from data_manager import DB_answer, DB_comment, DB_question, DB_tag


# questions


def get_question_by_id(_id: str):         # funkcje, które używany wielokrotnie w całym programie wydzielić w utility
    question = DB_question.get_by_id(_id) # wyrzucić by_id - zwykle z defaultu szukamy po id w innych przypadkach by_...
    return question[0]


def delete_question(_id: str):
    _id = str(_id)
    dicified_id = {'question_id': _id}
    DB_question.delete(dicified_id)


def sort_questions(sort_by, order):
    question_data = DB_question.sort(sort_by, order)
    return question_data


def get_questions():
    questions = DB_question.get_all()
    return questions


def new_question_id():
    last_id = DB_question.get_last_id()
    return last_id + 1


def edit_question(_id, message, title, image):
    item = get_question_by_id(_id)
    item['message'] = message  # Don't change
    item['title'] = title
    item['image'] = image

    DB_question.edit(item)


def date_generator():
    time_stamp = time.time()
    st = datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
    return str(st)


def new_question(form: dict):
    question = {}
    question['id'] = new_question_id()
    question['submission_time'] = date_generator()
    question['title'] = form['title']
    question['message'] = form['message']
    question['image'] = form['image']
    question['view_number'] = 0
    question['vote_number'] = 0
    DB_question.add(question)
    return question


def get_latest_questions():
    latest_five_questions = DB_question.get_latest_five()
    return latest_five_questions


# ANSWERS                              # podzielić logikę data manager na oddzielne pliki dla question, answer itd.
                                    # dzięki temu możemy tworzyć nazwy metod typu question.delete


def new_answer_id():
    last_id = DB_answer.get_last_id()
    return last_id + 1


def get_answer_by_id(_id):
    answer = DB_answer.get_by_id(_id)
    return answer[0]


def new_answer(form, question_id: str, image=None):
    answer = {}
    answer['id'] = new_answer_id()
    answer['submission_time'] = date_generator()
    answer['message'] = form['message']
    answer['question_id'] = question_id
    answer['vote_number'] = 0
    answer['image'] = form['image']
                                             # oddzielać definicje zmiennych od metod
    DB_answer.add(answer)


def get_answers_by_question_id(question_id: str):
    answer = DB_answer.get_by_question_id(question_id)
    return answer


def delete_answer(_id):
    DB_answer.delete(_id)


def get_question_id_by_answer_id(answer_id):
    question_id_dict = DB_question.get_by_answer_id(answer_id)
    question_id = question_id_dict[0]['question_id']
    return question_id


def edit_answer(_id, message, image=None):
    item = get_answer_by_id(_id)
    item['message'] = message
    item['image'] = image
    DB_answer.edit(item)
    item['message'] = message
    DB_answer.edit(item)


def search(data: str):
    questions = []
    q = (DB_question.search_by_text(data))
    for i in q:
        questions.append(i)
    answers = DB_answer.search_by_text(data)
    for i in answers:
        answer_id = i['id']
        questions.append(get_question_by_id(answer_id))
    return questions


# COMMENT


def add_comment(message : dict, question_id = None, answer_id = None):
    comment = {}
    comment['submission_time'] = date_generator()
    comment['message'] = message['message']
    comment['question_id'] = question_id
    comment['answer_id'] = answer_id
    comment['vote_number'] = 0
    comment['edited_count'] = 0
    DB_comment.add(comment)


def delete_comment(comment_id):
    DB_comment.delete(comment_id)


def get_comment_by_id(_id):
    data = DB_comment.get_by_id(_id)
    return data


def get_comment_by_question_id(_id):
    data = DB_comment.get_comment_by_question_id(_id)
    return data


def get_comment_by_answer_id(_id: str):
    data = DB_comment.get_by_answer_id(_id)
    return data


def edit_comment(_id: str, message: str):
    data = {}
    data['id'] = _id
    data['message']= message
    data['submission_time'] = date_generator()
    print(data)
    DB_comment.edit(data)

def get_question_comments_by_question_id(question_id: str):
    return DB_comment.get_by_question_id(question_id)
### TAGS


def new_tag_id():
    last_id = DB_tag.get_last_id()
    return last_id + 1


def get_tags_by_question_id(question_id):
    tags_for_question = DB_tag.get_by_question_id(question_id)

    return tags_for_question


def add_new_tag(form, question_id):
    del form['image']

    tag_data = {}
    tag_data['id'] = new_tag_id()
    print(tag_data)
    tag_names_dict = DB_tag.get_unique_names()
    print(tag_names_dict)

    names = []

    for i in tag_names_dict:
        names.append(i['name'])
    print(names)
    print(form['message'])
    if form['message'] in names:  ###
        DB_tag.add(question_id)
    else:
        tag_data['name'] = form['message'].lower()  ###
        DB_tag.add_to_question(tag_data, question_id)


def delete_question_tag_by_question_id(question_id, tag_id):
    DB_tag.delete(question_id, tag_id)


def get_unique_tag_names():
    unique_tag_names = DB_tag.get_unique_names()

    return unique_tag_names


def get_tags_ids_related_to_question(question_id):
    ids = DB_tag.get_id_by_question_id(question_id)
    return ids


def get_ids_related_to_question(question_id):
    data ={}
    answers_ids = []
    comments_ids = []
    comments_for_answers = []

    a = get_answers_by_question_id(question_id)
    for item in a:
        answers_ids.append(item['id'])


    c = get_comment_by_question_id(question_id)
    for item in c:
        comments_ids.append(item['id'])

    for item in answers_ids:
        for i in get_comment_by_answer_id(str(item)):
            comments_for_answers.append(i['id'])

    data['question_id'] = question_id
    data['answer_id'] = answers_ids
    data['comment_id'] = comments_ids
    data['tag_id'] = get_tags_ids_related_to_question(question_id)[0]
    data['comments_for_answers'] = comments_for_answers
    return data