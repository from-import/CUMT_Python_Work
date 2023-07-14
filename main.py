import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.text import LabelBase
from kivy.uix.popup import Popup

# 注册新的字体
LabelBase.register(name='STFANGSO', fn_regular='C:/Windows/Fonts/STFANGSO.TTF')


class Quiz:
    def __init__(self):
        self.questions = []
        self.options = []
        self.answers = []

    def load_questions(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for i in range(0, len(lines), 6):
                question = lines[i].strip()
                options = [line.strip() for line in lines[i + 1:i + 5]]
                answer = lines[i + 5].strip()
                self.questions.append(question)
                self.options.append(options)
                self.answers.append(answer)

    def generate_quiz(self, num_questions):
        quiz_indices = random.sample(range(len(self.questions)), num_questions)
        quiz_questions = [self.questions[i] for i in quiz_indices]
        quiz_options = [self.options[i] for i in quiz_indices]
        quiz_answers = [self.answers[i] for i in quiz_indices]
        return quiz_questions, quiz_options, quiz_answers


class QuizApp(App):
    def build(self):
        self.quiz = Quiz()
        self.quiz.load_questions('quiz_questions.txt')  # 从文件加载题库
        num_questions = 5  # 要出的题目数量
        self.quiz_questions, self.quiz_options, self.quiz_answers = self.quiz.generate_quiz(num_questions)
        self.layout = BoxLayout(orientation='vertical')
        self.question_index = 0
        self.question = Label(text=self.quiz_questions[self.question_index], font_name='STFANGSO', font_size=50)
        self.layout.add_widget(self.question)
        self.buttons = []
        for i in range(4):
            button = Button(text=self.quiz_options[self.question_index][i], font_name='STFANGSO', font_size=50)
            button.bind(on_release=self.answer_question)
            self.layout.add_widget(button)
            self.buttons.append(button)
        self.score = 0  # Initialize the score variable
        return self.layout


    def answer_question(self, instance):
        print(f"Clicked option: {instance.text}, Correct answer: {self.quiz_answers[self.question_index]}")
        if instance.text == self.quiz_answers[self.question_index]:
            print("Correct!")
            self.score += 1
        else:
            print("Incorrect!")

        self.question_index += 1
        if self.question_index < len(self.quiz_questions):
            self.question.text = self.quiz_questions[self.question_index]
            for i in range(4):
                self.buttons[i].text = self.quiz_options[self.question_index][i]
        else:
            print("Quiz finished")
            self.show_score_popup(self.score)

    def show_score_popup(self, score):
        content = BoxLayout(orientation='vertical')
        label = Label(text=f"Total Score: {score}/{len(self.quiz_questions)}", font_name='STFANGSO', font_size=50)
        button = Button(text='OK', font_name='STFANGSO', font_size=50, size_hint=(1, 0.5))
        content.add_widget(label)
        content.add_widget(button)

        popup = Popup(title='Quiz Score', content=content, size_hint=(None, None), size=(400, 200))
        button.bind(on_release=self.close_program)
        popup.open()

    def close_program(self, instance):
        self.stop()


if __name__ == '__main__':
    QuizApp().run()
