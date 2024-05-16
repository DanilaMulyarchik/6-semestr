from g4f.client import Client
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from db import *
import json, os

app = Flask(__name__)
SAVE_FOLDER = "C:\\Users\\USER\\Documents\\Python\\eazis\\saves"
app.config['SAVE_FOLDER'] = SAVE_FOLDER

# Отображение страницы чата
@app.route('/')
def index():
    info = select_all_chats()
    return render_template('main.html', info=info)


@app.route('/create')
def create():
    id = create_chat()
    print(id)
    return redirect(url_for('chat', id=id))


@app.route('/chat/<int:id>')
def chat(id):
    info = select_chat(id)
    return render_template("chat.html", info=info, id=id)


@app.route('/delete/<int:id>')
def delete(id):
    drop_chat(id)
    return redirect('/')


@app.route('/save')
def save():
    output()
    file_path = os.path.join('chat.json')
    return send_from_directory(app.config['SAVE_FOLDER'], file_path, as_attachment=True)


def output():
    data = select_output_info()

    # Преобразование данных в формат JSON
    json_data = json.dumps(data, ensure_ascii=False)

    if os.path.exists(f'{SAVE_FOLDER}/chat.json'):
        os.remove(f'{SAVE_FOLDER}/chat.json')
    # Сохранение данных в файл JSON с кодировкой UTF-8
    with open(f'{SAVE_FOLDER}/chat.json', 'w', encoding='utf-8') as file:
        file.write(json_data)
        file.close()


@app.route('/clear', methods=["GET", "POST"])
def clear_all():
    clear_table()
    return redirect('/')


@app.route('/ask/<int:id>', methods=["GET", "POST"])
def create_answer(id):
    print(0)
    if request.method == "POST":
        print(1)
        question = request.form.get("message-input")
        print(question)
        if select_name(id) == "Пустой чат":
            print(5)
            insert_name(id, question)
        if question.replace(' ', '') != '':
            answer = ask(question, 'ru')
            print(answer)
            while answer == '':
                answer = ask(question, 'ru')
            add_message(id, question, answer)

        return redirect(url_for('chat', id=id))


def ask(question: str, language: str) -> str:
    client = Client()
    print(question)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": question}],
        language=language
    )
    return response.choices[0].message.content


if __name__ == '__main__':
    app.run(debug=True)
