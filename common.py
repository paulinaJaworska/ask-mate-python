import data_manager

sample_data_question = 'sample_data/question.csv'

# answer_data = data_manager.import_data(####)
question_data = data_manager.import_data(sample_data_question)

def date_generator():
    time_stamp = time.time()
    return int(time_stamp)


def prepate_data_for_questions_data(question_data):
    next_id = id_generator()
    submission_time = date_generator()

    question_data.update({'id': next_id}, {"submission_time": submission_time})    # we can insert multiple items with update, add date generator


def prepate_data_for_answerss_data(question_data)