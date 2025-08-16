# Gamified CyberSecurity Awareness Game

Welcome to the **Gamified CyberSecurity Awareness Game**, an interactive educational tool designed to enhance your understanding of cybersecurity concepts through engaging challenges. Built using PyQt6, this application offers a fun way to test and improve your knowledge of secure practices, phishing detection, and more.

## Description
This game presents users with a series of scenario-based questions drawn from a JSON database (`bank.json`). Players can select the number of questions (up to 50) via a slider on the homepage, enter their name, and start the game. Each challenge includes multiple-choice options, with feedback provided after each answer. At the end, a report summarizes the total questions attempted, correct and wrong answers, and a level of understanding (Beginner, Novice, Intermediate, or Expert) based on the score.

## Features
- **Interactive Challenges**: Scenario-based questions with realistic cybersecurity scenarios.
- **Customizable Gameplay**: Adjust the number of questions (1-50) using a slider.
- **Personalized Experience**: Enter your name to personalize your report.
- **Real-Time Feedback**: Immediate feedback with explanations for each answer.
- **End-of-Game Report**: Detailed stats including total questions, correct/wrong answers, and skill level.
- **Smooth UI**: Modern design with fade animations and responsive layouts.

## Requirements
To run this project, you need the following:

- **Python**: Version 3.6 or higher.
- **Dependencies**:
  - `PyQt6`: For the graphical user interface (install via `pip install PyQt6`).
- **Files**:
  - `bank.json`: A JSON file containing the question bank (a sample with 50 questions is included).

### Installation
1. **Clone the Repository**:
   Use the following `.git` URL to clone the repository to your local machine:
   ```bash
   git clone https://github.com/syed-Muhammad-Ali-naqvi/gamified-cybersecurity-game.git
   cd gamified-cybersecurity-game
