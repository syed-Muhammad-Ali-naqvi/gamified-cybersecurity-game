import sys
import random
from dataclasses import dataclass
from typing import List, Dict, Any

from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication, QWidget, QStackedWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QScrollArea, QFrame, QLineEdit, QSlider
)
import json

def load_questions(path="bank.json") -> List[Dict[str, Any]]:
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        filtered = [q for q in data if all(k in q for k in ("question", "options", "answer", "explanation"))]
        random.shuffle(filtered)
        return filtered
    except Exception as e:
        print(f"Error loading questions: {e}")
        return [{
            "question": "Is HTTPS more secure than HTTP?",
            "options": ["Yes", "No"],
            "answer": "Yes",
            "explanation": "HTTPS encrypts traffic; HTTP does not."
        }]

# ---------------- Helpers ----------------
def h1(text: str) -> QLabel:
    lbl = QLabel(text)
    f = QFont()
    f.setPointSize(20)
    f.setBold(True)
    lbl.setFont(f)
    lbl.setStyleSheet("color: white;")
    return lbl

def body(text: str, rich: bool = True) -> QLabel:
    lbl = QLabel()
    if rich:
        lbl.setTextFormat(Qt.TextFormat.RichText)
    lbl.setText(text)
    lbl.setWordWrap(True)
    lbl.setStyleSheet("color: #e7e7ea;")
    return lbl

def card() -> QFrame:
    frame = QFrame()
    frame.setStyleSheet("""
        QFrame { background-color: #353a45; border-radius: 12px; }
    """)
    layout = QVBoxLayout(frame)
    layout.setContentsMargins(16,16,16,16)
    layout.setSpacing(8)
    return frame

def primary_button(text: str) -> QPushButton:
    btn = QPushButton(text)
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    btn.setStyleSheet("""
        QPushButton {
            background-color: #b44cf5; color: white; border: none;
            border-radius: 10px; padding: 10px 14px; font-weight: 600;
        }
        QPushButton:hover { background-color: #eb6372; }
        QPushButton:pressed { background-color: #400e73; }
    """)
    return btn

def secondary_button(text: str) -> QPushButton:
    btn = QPushButton(text)
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    btn.setStyleSheet("""
        QPushButton {
            background-color: #2a2e36; color: white; border: none;
            border-radius: 10px; padding: 10px 14px;
        }
        QPushButton:hover { background-color: #343946; }
        QPushButton:pressed { background-color: #1f2229; }
    """)
    return btn

# ---------------- Screens ----------------
class HomeScreen(QWidget):
    def __init__(self, on_start):
        super().__init__()
        self.setObjectName("root")
        self.setStyleSheet("#root { background-color: #363d47; }")
        v = QVBoxLayout(self)
        v.setContentsMargins(20,20,20,20)
        v.setSpacing(20)
        v.addWidget(h1("Gamified CyberSecurity Awareness Quiz Game"))
        v.addWidget(body("Level up your cyber knowledge and stay secure!"))

        name_layout = QHBoxLayout()
        name_layout.addWidget(body("Enter your name:"))
        self.name_input = QLineEdit()
        name_layout.addWidget(self.name_input)
        v.addLayout(name_layout)

        # Slider for number of questions
        slider_layout = QHBoxLayout()
        slider_layout.addWidget(body("Number of Questions:"))
        self.num_questions_label = QLabel("25")
        self.num_questions_slider = QSlider(Qt.Orientation.Horizontal)
        self.num_questions_slider.setRange(1, 50)  # Set range to 50 based on updated bank.json
        self.num_questions_slider.setValue(25)
        self.num_questions_slider.valueChanged.connect(lambda value: self.num_questions_label.setText(str(value)))
        self.num_questions_slider.setFixedWidth(400)  # Increased width to 400 pixels
        self.num_questions_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 8px;  /* Thickness of the track */
                background: #2a2e36;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #b0b1b5;
                border: 2px solid #353740;
                width: 16px;  /* Wider handle */
                height: 16px;  /* Taller handle */
                border-radius: 8px;
                margin: -4px 0;  /* Center handle vertically */
            }
            QSlider::handle:horizontal:hover {
                background: #eb6372;
            }
        """)
        slider_layout.addWidget(self.num_questions_slider)
        slider_layout.addWidget(self.num_questions_label)
        v.addLayout(slider_layout)

        v.addStretch(1)

        start = primary_button("Start Game")
        start.clicked.connect(lambda: on_start(self.name_input.text(), self.num_questions_slider.value()))
        quitb = secondary_button("Quit")
        quitb.clicked.connect(QApplication.instance().quit)
        v.addWidget(start)
        v.addWidget(quitb)

class ChallengeScreen(QWidget):
    def __init__(self, on_submit, on_skip, get_score):
        super().__init__()
        self.on_submit = on_submit
        self.get_score = get_score
        self.setObjectName("root")
        self.setStyleSheet("#root { background-color: #121417; }")
        self.attempts = 0  # Track attempts per challenge

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20,20,20,20)
        self.layout.setSpacing(10)

        self.score_lbl = QLabel()
        self.score_lbl.setStyleSheet("color: white; font-weight: 600;")
        self.layout.addWidget(self.score_lbl, alignment=Qt.AlignmentFlag.AlignLeft)

        self.title_lbl = h1("Challenge")
        self.layout.addWidget(self.title_lbl)

        # Scenario card
        self.scenario_frame = card()
        self.lbl_scenario = body("", True)
        self.scenario_frame.layout().addWidget(self.lbl_scenario)
        self.layout.addWidget(self.scenario_frame)

        self.question_lbl = body("")
        self.layout.addWidget(self.question_lbl)

        self.options_box = QVBoxLayout()
        self.options_box.setSpacing(8)
        self.layout.addLayout(self.options_box)

        bottom = QHBoxLayout()
        skip = secondary_button("Skip")
        skip.clicked.connect(on_skip)
        bottom.addStretch(1)
        bottom.addWidget(skip)
        self.layout.addLayout(bottom)

        self.update_score()

    def update_score(self):
        self.score_lbl.setText(f"Score: <b>{self.get_score()}</b>")

    def set_challenge(self, ch: Dict[str, Any]):
        # Clear old widgets
        while self._take_from_layout(self.options_box):
            pass

        self.current = ch
        self.attempts = 0
        self.title_lbl.setText("Challenge")
        self.lbl_scenario.setText(ch.get("content",""))
        self.scenario_frame.setVisible(True)
        self.question_lbl.setText(ch.get("question",""))

        for opt in ch.get("options",[]):
            btn = secondary_button(opt)
            # bind current option properly
            btn.clicked.connect(lambda _, o=opt: self.submit_answer(o))
            self.options_box.addWidget(btn)
        self.update_score()

    def submit_answer(self, user_answer):
        self.attempts += 1
        self.on_submit(user_answer, self.attempts)

    def _take_from_layout(self, layout):
        item = layout.takeAt(0)
        if not item:
            return False
        w = item.widget()
        if w:
            w.deleteLater()
        else:
            child_layout = item.layout()
            if child_layout:
                while self._take_from_layout(child_layout):
                    pass
        return True

class FeedbackScreen(QWidget):
    def __init__(self, on_next, on_home):
        super().__init__()
        self.setObjectName("root")
        self.setStyleSheet("#root { background-color: #121417; }")
        v = QVBoxLayout(self)
        v.setContentsMargins(20,20,20,20)
        v.setSpacing(10)

        self.title = h1("Result")
        v.addWidget(self.title)

        self.detail = body("")
        v.addWidget(self.detail)

        self.expl = body("", True)
        v.addWidget(self.expl)

        row = QHBoxLayout()
        nextb = primary_button("Next Challenge")
        homeb = secondary_button("Home")
        nextb.clicked.connect(on_next)
        homeb.clicked.connect(on_home)
        row.addWidget(nextb)
        row.addWidget(homeb)
        v.addLayout(row)

    def set_feedback(self, title: str, detail: str, explanation: str):
        self.title.setText(title)
        self.detail.setText(detail)
        self.expl.setText(f"<b>Explanation:</b> {explanation}")

class ReportScreen(QWidget):
    def __init__(self, on_home, player_name, total_questions, correct_answers, wrong_answers):
        super().__init__()
        self.setObjectName("root")
        self.setStyleSheet("#root { background-color: #121417; }")
        v = QVBoxLayout(self)
        v.setContentsMargins(20, 20, 20, 20)
        v.setSpacing(10)

        v.addWidget(h1(f"Report for {player_name}"))
        v.addWidget(body(f"Total Questions Attempted: {total_questions}"))
        v.addWidget(body(f"Correct Answers: {correct_answers}"))
        v.addWidget(body(f"Wrong Answers: {wrong_answers}"))

        # Calculate percentage and determine level of understanding
        percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        level = "Beginner"
        if percentage >= 80:
            level = "Expert"
        elif percentage >= 60:
            level = "Intermediate"
        elif percentage >= 40:
            level = "Novice"
        v.addWidget(body(f"Level of Understanding: {level} ({percentage:.1f}%)"))

        v.addStretch(1)

        homeb = primary_button("Return to Home")
        homeb.clicked.connect(on_home)
        v.addWidget(homeb)

# ---------------- Main Game ----------------
class Game(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cybersecurity Awareness Game")
        self.setMinimumSize(720, 520)

        self.questions = load_questions()
        self.score = 0
        self.current = {}
        self.selected_questions = []  # To store the selected number of questions
        self.current_index = 0
        self.player_name = "Player"  # Default name

        self.stack = QStackedWidget()
        layout = QVBoxLayout(self)
        layout.addWidget(self.stack)

        self.home = HomeScreen(on_start=self.start_game)
        self.challenge = ChallengeScreen(on_submit=self.submit_answer,
                                        on_skip=self.next_challenge,
                                        get_score=lambda: self.score)
        self.feedback = FeedbackScreen(on_next=self.next_challenge,
                                      on_home=self.goto_home)
        self.report = ReportScreen(on_home=self.goto_home,
                                 player_name=self.player_name,
                                 total_questions=0,
                                 correct_answers=0,
                                 wrong_answers=0)

        self.stack.addWidget(self.home)
        self.stack.addWidget(self.challenge)
        self.stack.addWidget(self.feedback)
        self.stack.addWidget(self.report)
        self.apply_fade(self.stack.currentWidget())

    def goto_home(self):
        self.stack.setCurrentWidget(self.home)
        self.apply_fade(self.home)

    def start_game(self, player_name, num_questions):
        self.player_name = player_name if player_name else "Player"
        self.score = 0
        self.current_index = 0
        # Select a random sample of questions based on the slider value, capped by available questions
        max_questions = min(num_questions, len(self.questions))
        self.selected_questions = random.sample(self.questions, max_questions) if max_questions > 0 else self.questions[:1]
        self.next_challenge()

    def choose_random(self):
        if self.current_index >= len(self.selected_questions):
            return None
        return self.selected_questions[self.current_index]

    def next_challenge(self):
        self.current = self.choose_random()
        if self.current is None:
            # Generate report when all questions are done
            total_questions = len(self.selected_questions)
            correct_answers = self.score
            wrong_answers = total_questions - self.score
            self.report = ReportScreen(on_home=self.goto_home,
                                     player_name=self.player_name,
                                     total_questions=total_questions,
                                     correct_answers=correct_answers,
                                     wrong_answers=wrong_answers)
            self.stack.addWidget(self.report)
            self.stack.setCurrentWidget(self.report)
            self.apply_fade(self.report)
            return
        self.challenge.set_challenge(self.current)
        self.stack.setCurrentWidget(self.challenge)
        self.current_index += 1
        self.apply_fade(self.challenge)

    def submit_answer(self, user_answer, attempts):
        ch = self.current
        correct = str(ch.get("answer","")).strip().lower()
        user_norm = str(user_answer).strip().lower()
        is_correct = user_norm == correct

        if is_correct:
            self.score += 1
            title = "✅ Correct!"
            detail = f"Your answer: {user_answer}\nScore: {self.score}"
        else:
            if attempts >= 3:
                title = "💥 System Compromised!"
                detail = f"Too many wrong attempts. Challenge failed.\nScore: {self.score}"
            else:
                title = "❌ Not Quite"
                detail = f"Your answer: {user_answer}\nAttempts: {attempts}/3\nScore: {self.score}"

        explanation = ch.get("explanation","—")
        self.feedback.set_feedback(title, detail, explanation)
        self.stack.setCurrentWidget(self.feedback)
        self.apply_fade(self.feedback)

    def apply_fade(self, widget: QWidget):
        widget.setWindowOpacity(0.0)
        anim = QPropertyAnimation(widget, b"windowOpacity", self)
        anim.setDuration(180)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self._anim = anim
        anim.start()

def main():
    app = QApplication(sys.argv)
    g = Game()
    g.show()
    sys.exit(app.exec())

if __name__ == "__main__":

    main()
