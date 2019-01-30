import data_manager


question_labels = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
answer_labels = ["id", "submission_time", "vote_number", "question_id", "message", "image"]
# parameters to call the import data: filename = "data/answers.csv" or filename = "data/questions.csv"


sample_data_question = 'sample_data/question.csv'
sample_data_answer = 'sample_data/answer.csv'
last_question_id = data_manager.get_last_question_id()
print (last_question_id)



### SORTING  ###
def sort_list_of_dict(list_of_dictionaries, sort_by, order):
    '''
    Sorts list of dictionaies by given parameter in ascending or descending order.
    :param list_of_dictionaries:
    :param sort_by: key by which we want to sort by
    :param order: boolean (True or False)  True = descending
    :return: sorted list of dicts
    '''
    return sorted(list_of_dictionaries, key=lambda i: i[str(sort_by)], reverse=order)


###  FUNCTIONS READING CSV FILES AND   ###
not_sorted_question_data = data_manager.import_data(sample_data_question)
question_data = sort_list_of_dict(not_sorted_question_data, "submission_time", True )

answer_data = data_manager.import_data(sample_data_answer)



### Pulling from database  ###



###   WRITING TO CSV   ###

def id_generator(filename):
    exists = os.path.isfile(filename)
    if not exists:
        return 1
    else:
        with open(filename, 'r') as f:
            result = csv.DictReader(f)
            for row in result:
                result = row["id"]
            return result + 1

def date_generator():
    time_stamp = time.time()
    return int(time_stamp)


def prepare_data_for_questions_data(question_data_from_form):
    """
    Append necessary data, which is not enter by user, to data from question form filled by user.
    :param question_data_from_form: dictionary
    :return: dictionary
    """
    next_id = id_generator()
    submission_time = date_generator()
    view_number = "not implemented"
    vote_number = "not implemented"
    image = "no image"
    generated_automatically = {'id': next_id, "submission_time": submission_time, "view_number": view_number,
                               "vote_number": vote_number, "image": image}
    question_data_from_form.update(generated_automatically)
    return question_data_from_form


def prepare_answer_to_be_saved_in_csv(question_data):
    next_id = id_generator()
    submission_time = date_generator()

def get_question_by_id(_id):
    _id = str(_id)
    for item in question_data:
        if item['id'] == _id:
            return item


def get_answers_by_question_id(_id):
    _id = str(_id)
    answers = []
    for item in answer_data:
        if item['question_id'] == _id:
            answers.append(item)
    return answers