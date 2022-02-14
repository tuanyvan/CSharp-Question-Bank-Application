#! python3

import csv
import random

class Question:
    def __init__(self, id:int, row_data):
        self.id = id
        self.question = row_data['question'].replace('~', '\n')
        self.answers = row_data['answers'].replace('~', '\n')
        self.correct_answer = row_data['correct_answer']

class QuestionPrompt:
    def __init__(self, question_data):
        self.question = question_data.question
        self.answers = question_data.answers if question_data.answers != '' else 'True or False?'
        self.correct_answer = question_data.correct_answer
        pass

class main():
    def __init__(self):

        # Read the CSV and parse the row data into a list.
        question_bank = []

        with open('questions.csv', newline='') as questions_csv:
            reader = csv.DictReader(questions_csv)
            for id, row in enumerate(reader):
                question_bank.append(Question(id, row))

        # Make a record of user score.
        user_score = 0
        questions_answered = 0
        wants_to_leave = False

        # Store response output strings.
        correct_response = ["That's right!", "Good job!", "Right on!", "Correctomundo!", "Very nice!", "Keep it up!", "Fantastic!", "You're doing great!", "Do a barrel roll!", "Woohoo!"]
        wrong_response = ["Not quite.", "You missed that one, try another!", "Keep trying.", "You can do well, friend.", "We'll get them next time...", "No cigar.", "Give it another shot, champ."]

        # Introduce the quiz, for fun.
        print("Welcome to the COMP1098 Midterm Practice, the gameshow where we make a worksheet a game.\n\nYou will be given a question and the prompts for that question. Answer with a, b, c, d, e, true, false, t, or f.\n\nWhen you've had enough quizzing for the day, type 'quit' or 'q' to leave the show. Good luck!\n")

        input("Press any key to continue... hmm, the any key?")

        # Start the quiz game.
        while True:
            # Get a random question from the CSV.
            random.seed()
            random_question_index = random.randint(0, len(question_bank) - 1)
            currentQuestion = QuestionPrompt(question_bank[random_question_index])

            # Show the user the question and prompts for the question.
            print(f"\nQuestion #{questions_answered + 1}\n{currentQuestion.question}\n{currentQuestion.answers}")

            # Get user input, reject if not one of (a,b,c,d,e,true,false,t,f)
            is_input_valid = False
            while not is_input_valid:
                try:
                    user_answer = input("Your answer: ").lower()[0]
                    if user_answer not in ('a','b','c','d','e','true','false','t','f'):
                        if user_answer in ('quit', 'q'):
                            wants_to_leave = True
                            break
                        else:
                            print("That is not a valid input. Please answer one of the prompts a, b, c, d, e, true, false, t, or f.")
                    else:
                        is_input_valid = True;
                except IndexError:
                    print("Please provide an answer to the question.")

            # If input was one of ('quit', 'q'), leave the program.
            if wants_to_leave:
                break

            questions_answered += 1
            # If the user got the answer right, add one to score
            if user_answer == currentQuestion.correct_answer[0].lower():

                user_score += 1
                print('\n' + correct_response[random.randint(0, len(correct_response) - 1)])

                # If it was a true false with an explanation...
                if len(currentQuestion.correct_answer) > 6:
                    print(f'\nExplanation: {currentQuestion.correct_answer}')

            # Otherwise, if the user got it wrong, tell them the right answer.
            else:
                print('\n' + wrong_response[random.randint(0, len(wrong_response) - 1)])
                print(f'Answer: {currentQuestion.correct_answer}')

            print(f'You have gotten {user_score} correct {"answers" if user_score != 1 else "answer"} out of {questions_answered} {"questions" if questions_answered != 1 else "question"}.')

            input("\nPress any key...")
        print(f'\nGood work today. You scored {user_score} correct {"answers" if user_score != 1 else "answer"} out of {questions_answered} {"questions" if questions_answered != 1 else "question"}.')
        input("\nPress any key to continue...")

if __name__ == '__main__':
    main()