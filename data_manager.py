import csv
import os
import time

question_labels = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
answer_labels = ["id", "submission_time", "vote_number", "question_id", "message", "image"]
# parameters to call the import data: filename = "data/answers.csv" or filename = "data/questions.csv"

def import_data(filename):
    exists = os.path.isfile(filename)
    if not exists:
        return None
    else:
        with open(filename, 'r') as f:
            result = csv.DictReader(f)  # spr co zwraca
            return result


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
    return time_stamp


def save_user_stories(filename, labels, some_data_do_add):
    exists = os.path.isfile(filename)
    #next_id = id_generator()
    #story.update({'id': next_id})    # we can insert multiple items with update, add date generator
    with open(filename, "a+") as f:
        writer = csv.DictWriter(f, fieldnames=labels, delimiter=',')
        if not exists:
            writer.writeheader()
        writer.writerow(some_data_to_add)


def prepate_data_for_questions_data(question_data):
    next_id = id_generator()
    submission_time = date_generator()

    question_data.update({'id': next_id}, {"submission_time": submission_time})    # we can insert multiple items with update, add date generator
