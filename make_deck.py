import pickle, os

print(os.getcwd())

def get_answers():

    with open("cards-against-humanity/answers.txt", "r") as ans:
        answers = ans.read().splitlines()

    with open("cards-against-humanity/answers.pickle", "wb") as f:
        pickle.dump(answers, f)

    return answers

def get_questions():

    with open("cards-against-humanity/questions.txt", "r") as qs:
        questions = qs.read().splitlines()

    with open("cards-against-humanity/questions.pickle", "wb") as f:
        pickle.dump(questions, f)

    return questions

if __name__ == "__main__":

    answers = get_answers()

    print(answers[:5])

    questions = get_questions()

    print(questions[:5])
