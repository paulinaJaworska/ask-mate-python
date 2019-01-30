import data_manager


question_labels = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
answer_labels = ["id", "submission_time", "vote_number", "question_id", "message", "image"]
# parameters to call the import data: filename = "data/answers.csv" or filename = "data/questions.csv"


sample_data_question = 'sample_data/question.csv'
sample_data_answer = 'sample_data/answer.csv'

###  FUNCTIONS READING CSV FILES AND   ###
not_sorted_question_data = data_manager.import_data(sample_data_question)
question_data = sort_list_of_dict(not_sorted_question_data, "submission_time", True )

answer_data = data_manager.import_data(sample_data_answer)


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



### Pulling from database  ###

def get_row_by_id(list_of_dictionaries, specified_id):
    for row in list_of_dictionaries:



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


def prepate_data_for_questions_data(question_data_from_form):
    next_id = id_generator()
    submission_time = date_generator()
    view_number = "jeszcze_nic"
    question_data_from_form.update({'id': next_id}, {"submission_time": submission_time}, {"view_number": view_number})



def prepate_data_for_questions_data(question_data):
    next_id = id_generator()
    submission_time = date_generator()

    question_data.update({'id': next_id}, {
        "submission_time": submission_time})  # we can insert multiple items with update, add date generator

def prepate_data_for_answerss_data(question_data):
    next_id = id_generator()
    submission_time = date_generator()