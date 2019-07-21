import time            # najpierw zewnętrzne
import datetime
                        # spacja
import data_manager         # zewnętrzne  # atosować aliasy
# questions


def get_question_by_id(_id: str):         # funkcje, które używany wielokrotnie w całym programie wydzielić w utility
    question = data_manager.get_question_by_id(_id) # wyrzucić by_id - zwykle z defaultu szukamy po id w innych przypadkach by_...
    return question[0]


def delete_question(_id: str):
    _id = str(_id)
    dicified_id = {'question_id': _id}
    data_manager.delete_question(dicified_id)


def sort_questions(sort_by, order):
    question_data = data_manager.sort_questions(sort_by, order)
    return question_data


def get_questions():
    questions = data_manager.get_question_data()
    return questions


def new_question_id():
    last_id = data_manager.last_question_id()
    return last_id + 1


def edit_question(_id, message, title, image):
    item = get_question_by_id(_id)
    item['message'] = message  # Don't change
    item['title'] = title
    item['image'] = image

    data_manager.edit_question(item)


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
    data_manager.save_new_question(question)
    return question


def get_latest_questions():
    latest_five_questions = data_manager.get_latest_five_questions()
    return latest_five_questions


# ANSWERS                              # podzielić logikę data manager na oddzielne pliki dla question, answer itd.
                                    # dzięki temu możemy tworzyć nazwy metod typu question.delete


def new_answer_id():
    last_id = data_manager.last_answer_id()
    return last_id + 1


def get_answer_by_id(_id):
    answer = data_manager.get_answer_by_id(_id)
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
    data_manager.save_new_answer(answer)


def get_answer_by_question_id(question_id: str):
    answer = data_manager.get_answers_by_question_id(question_id)
    return answer


def delete_answer(_id):
    data_manager.delete_answer(_id)


def get_question_id_by_answer_id(answer_id):
    question_id_dict = data_manager.get_question_id_by_answer_id(answer_id)
    question_id = question_id_dict[0]['question_id']
    return question_id


def edit_answer(_id, message, image=None):
    item = get_answer_by_id(_id)
    item['message'] = message
    item['image'] = image
    data_manager.edit_answer(item)
    item['message'] = message
    data_manager.edit_answer(item)


def search(data: str):
    questions = []
    q = (data_manager.search_in_questions(data))
    for i in q:
        questions.append(i)
    answers = data_manager.search_in_answers(data)
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
    data_manager.add_comment(comment)


def delete_comment(comment_id):
    data_manager.delete_comment(comment_id)


def get_comment_by_id(_id):
    data = data_manager.get_comment_by_id(_id)
    return data


def get_comment_by_question_id(_id):
    data = data_manager.get_comment_by_question_id(_id)
    return data


def get_comment_by_answer_id(_id: str):
    data = data_manager.get_comment_by_answer_id(_id)
    return data


def edit_comment(_id: str, message: str):
    data = {}
    data['id'] = _id
    data['message']= message
    data['submission_time'] = date_generator()
    print(data)
    data_manager.edit_comment(data)

### TAGS
def new_tag_id():
    last_id = data_manager.last_tag_id()
    return last_id + 1


def get_tags_by_question_id(question_id):
    tags_for_question = data_manager.get_tags_by_question_id(question_id)

    return tags_for_question


def add_new_tag(form, question_id):
    del form['image']
    tag_data = {}
    tag_data['id'] = new_tag_id()
    print(tag_data)
    tag_names_dict = data_manager.get_unique_tag_names()
    print(tag_names_dict)

    names = []
    for i in tag_names_dict:
        names.append(i['name'])
    print(names)
    print(form['message'])
    if form['message'] in names:  ###
        data_manager.save_new_question_tag(question_id)
    else:
        tag_data['name'] = form['message'].lower()  ###
        data_manager.save_new_tag_and_question_tag(tag_data, question_id)


def delete_question_tag_by_question_id(question_id, tag_id):
    data_manager.delete_question_tag(question_id, tag_id)


def get_unique_tag_names():
    unique_tag_names = data_manager.get_unique_tag_names()

    return unique_tag_names


def get_tags_ids_reated_to_question(question_id):
    ids = data_manager.get_tags_id_realted_to_question(question_id)
    return ids


def get_ids_related_to_question(question_id):
    data ={}
    answers_ids = []
    comments_ids = []
    comments_for_answers = []

    a = get_answer_by_question_id(question_id)
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
    data['tag_id'] = get_tags_ids_reated_to_question(question_id)[0]
    data['comments_for_answers'] = comments_for_answers
    return data


