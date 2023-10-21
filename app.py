from flask import Flask, render_template, request

app = Flask(__name__)

# Define the correct answers (for scoring)
correct_answers = {
    'q1': 'a',
    'q2': 'b',
    'q3': 'b',
    'q4': 'c',
    'q5': 'c',
    'q6': 'a',
    'q7': 'b',
    'q8': 'a',
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_exam():
    score = 0
    total_questions = len(correct_answers)

    for question, correct_answer in correct_answers.items():
        user_answer = request.form.get(question)
        if user_answer == correct_answer:
            score += 1

    return f'Your score: {score} out of {total_questions}'

if __name__ == '__main__':
    app.run()
