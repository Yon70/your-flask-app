from flask import Flask, render_template, request, redirect, url_for
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# 구글 시트와 연결
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open("Phonics Quiz Results").sheet1

@app.route('/')
def quiz():
    return render_template('quiz.html')

@app.route('/submit', methods=['POST'])
def submit():
    student_name = request.form['student_name']
    answer1 = request.form['answer1'].lower()
    answer2 = request.form['answer2'].lower()
    answer3 = request.form['answer3'].lower()

    # 정답 확인
    correct_answers = {'1': 'b', '2': 'c', '3': 'd'}
    score = sum([1 if correct_answers[str(i+1)] == answer else 0 for i, answer in enumerate([answer1, answer2, answer3])])
    accuracy = (score / 3) * 100

    # 구글 시트에 답안 저장
    sheet.append_row([student_name, answer1, answer2, answer3, accuracy])

    # 정답률이 60% 이하일 경우 재시험 요청
    if accuracy <= 60:
        return render_template('retry.html', accuracy=accuracy)
    else:
        return redirect(url_for('success', accuracy=accuracy))

@app.route('/success')
def success():
    accuracy = request.args.get('accuracy')
    return f'퀴즈 통과! 정답률: {accuracy}%'

@app.route('/retry')
def retry():
    accuracy = request.args.get('accuracy')
    return f'재시험 필요. 정답률: {accuracy}%'

if __name__ == '__main__':
    app.run(debug=True)
