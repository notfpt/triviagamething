# balls version
import os
import time
import random
from pynput import keyboard
import queue
import threading

# Define the questions for each category and difficulty level
questions = {
    'Geography': {
        'easy': [
            {'question': 'What is the capital of France?', 'options': ['a) Paris', 'b) London', 'c) Berlin', 'd) Madrid'], 'answer': 'a'},
            {'question': 'Which continent is the largest?', 'options': ['a) Asia', 'b) Africa', 'c) North America', 'd) Europe'], 'answer': 'a'},
            {'question': 'What ocean is the largest?', 'options': ['a) Pacific', 'b) Atlantic', 'c) Indian', 'd) Arctic'], 'answer': 'a'},
            {'question': 'What is the capital of Brazil?', 'options': ['a) Rio', 'b) São Paulo', 'c) Brasília', 'd) Salvador'], 'answer': 'c'},
            {'question': 'Which country has the most deserts?', 'options': ['a) Australia', 'b) Egypt', 'c) Canada', 'd) Brazil'], 'answer': 'a'}
        ],
        'average': [
            {'question': 'What is the longest river?', 'options': ['a) Nile', 'b) Amazon', 'c) Yangtze', 'd) Mississippi'], 'answer': 'a'},
            {'question': 'Which country has the most population?', 'options': ['a) India', 'b) China', 'c) USA', 'd) Russia'], 'answer': 'b'},
            {'question': 'What is the capital of Japan?', 'options': ['a) Osaka', 'b) Kyoto', 'c) Tokyo', 'd) Hiroshima'], 'answer': 'c'},
            {'question': 'Which continent has the most countries?', 'options': ['a) Asia', 'b) Africa', 'c) Europe', 'd) South America'], 'answer': 'b'},
            {'question': 'What sea borders Turkey?', 'options': ['a) Black Sea', 'b) Red Sea', 'c) Caspian Sea', 'd) Yellow Sea'], 'answer': 'a'}
        ],
        'hard': [
            {'question': 'What is the smallest country by area?', 'options': ['a) Vatican City', 'b) Monaco', 'c) Nauru', 'd) San Marino'], 'answer': 'a'},
            {'question': 'Which country has the longest coastline?', 'options': ['a) Canada', 'b) Russia', 'c) Australia', 'd) USA'], 'answer': 'a'},
            {'question': 'What is the highest mountain?', 'options': ['a) Everest', 'b) K2', 'c) Kangchenjunga', 'd) Lhotse'], 'answer': 'a'},
            {'question': 'Which desert is the largest?', 'options': ['a) Sahara', 'b) Gobi', 'c) Antarctic', 'd) Arabian'], 'answer': 'c'},
            {'question': 'What river flows through Egypt?', 'options': ['a) Nile', 'b) Congo', 'c) Amazon', 'd) Euphrates'], 'answer': 'a'}
        ]
    },
    'History': {
        'easy': [
            {'question': 'First US President?', 'options': ['a) Washington', 'b) Jefferson', 'c) Lincoln', 'd) Adams'], 'answer': 'a'},
            {'question': 'Who discovered America?', 'options': ['a) Columbus', 'b) Magellan', 'c) Drake', 'd) Cook'], 'answer': 'a'},
            {'question': 'When did WWI start?', 'options': ['a) 1914', 'b) 1918', 'c) 1939', 'd) 1945'], 'answer': 'a'},
            {'question': 'Who built the pyramids?', 'options': ['a) Egyptians', 'b) Romans', 'c) Greeks', 'd) Persians'], 'answer': 'a'},
            {'question': 'What empire fell in 1453?', 'options': ['a) Byzantine', 'b) Roman', 'c) Ottoman', 'd) Mongol'], 'answer': 'a'}
        ],
        'average': [
            {'question': 'WWII end year?', 'options': ['a) 1945', 'b) 1939', 'c) 1918', 'd) 1960'], 'answer': 'a'},
            {'question': 'Who wrote the Declaration?', 'options': ['a) Jefferson', 'b) Washington', 'c) Franklin', 'd) Adams'], 'answer': 'a'},
            {'question': 'What year was the French Revolution?', 'options': ['a) 1789', 'b) 1812', 'c) 1756', 'd) 1848'], 'answer': 'a'},
            {'question': 'Who was Cleopatra?', 'options': ['a) Queen of Egypt', 'b) Roman Empress', 'c) Greek Philosopher', 'd) Persian Ruler'], 'answer': 'a'},
            {'question': 'What war ended in 1865?', 'options': ['a) Civil War', 'b) Revolutionary War', 'c) WWI', 'd) WWII'], 'answer': 'a'}
        ],
        'hard': [
            {'question': 'Longest-reigning monarch?', 'options': ['a) Elizabeth II', 'b) Victoria', 'c) George III', 'd) Henry VIII'], 'answer': 'a'},
            {'question': 'Who ended feudalism in Japan?', 'options': ['a) Meiji', 'b) Tokugawa', 'c) Hideyoshi', 'd) Nobunaga'], 'answer': 'a'},
            {'question': 'What treaty ended WWI?', 'options': ['a) Versailles', 'b) Trianon', 'c) Brest-Litovsk', 'd) Paris'], 'answer': 'a'},
            {'question': 'Who was the first Roman Emperor?', 'options': ['a) Augustus', 'b) Nero', 'c) Julius Caesar', 'd) Tiberius'], 'answer': 'a'},
            {'question': 'What year did the Berlin Wall fall?', 'options': ['a) 1989', 'b) 1991', 'c) 1975', 'd) 1961'], 'answer': 'a'}
        ]
    },
    'Science': {
        'easy': [
            {'question': 'Water’s chemical symbol?', 'options': ['a) H2O', 'b) CO2', 'c) O2', 'd) NaCl'], 'answer': 'a'},
            {'question': 'What gas do we breathe?', 'options': ['a) Oxygen', 'b) Nitrogen', 'c) Carbon Dioxide', 'd) Helium'], 'answer': 'a'},
            {'question': 'What planet is closest to the sun?', 'options': ['a) Mercury', 'b) Venus', 'c) Earth', 'd) Mars'], 'answer': 'a'},
            {'question': 'What is 2 + 2?', 'options': ['a) 4', 'b) 3', 'c) 5', 'd) 6'], 'answer': 'a'},
            {'question': 'What force pulls objects down?', 'options': ['a) Gravity', 'b) Magnetism', 'c) Friction', 'd) Pressure'], 'answer': 'a'}
        ],
        'average': [
            {'question': 'Speed of light?', 'options': ['a) 300,000 km/s', 'b) 150,000 km/s', 'c) 450,000 km/s', 'd) 600,000 km/s'], 'answer': 'a'},
            {'question': 'What element is diamond?', 'options': ['a) Carbon', 'b) Silicon', 'c) Gold', 'd) Iron'], 'answer': 'a'},
            {'question': 'Who proposed relativity?', 'options': ['a) Einstein', 'b) Newton', 'c) Galileo', 'd) Hawking'], 'answer': 'a'},
            {'question': 'What is the largest organ?', 'options': ['a) Skin', 'b) Liver', 'c) Heart', 'd) Brain'], 'answer': 'a'},
            {'question': 'What gas is most in the atmosphere?', 'options': ['a) Nitrogen', 'b) Oxygen', 'c) CO2', 'd) Argon'], 'answer': 'a'}
        ],
        'hard': [
            {'question': 'Heisenberg Principle?', 'options': ['a) Position and momentum', 'b) Energy and time', 'c) Both', 'd) None'], 'answer': 'c'},
            {'question': 'What particle has no charge?', 'options': ['a) Neutron', 'b) Proton', 'c) Electron', 'd) Photon'], 'answer': 'a'},
            {'question': 'What’s the strongest fundamental force?', 'options': ['a) Strong nuclear', 'b) Electromagnetic', 'c) Weak nuclear', 'd) Gravity'], 'answer': 'a'},
            {'question': 'Who discovered penicillin?', 'options': ['a) Fleming', 'b) Pasteur', 'c) Lister', 'd) Salk'], 'answer': 'a'},
            {'question': 'What is E=mc²?', 'options': ['a) Mass-energy equivalence', 'b) Force equation', 'c) Momentum', 'd) Kinetic energy'], 'answer': 'a'}
        ]
    }
}

# Points for each difficulty level
points_per_difficulty = {'easy': 5, 'average': 10, 'hard': 15}

# Global variables for input handling
input_queue = queue.Queue()
restart_flag = False

# Keyboard listener callback
def on_press(key):
    global restart_flag
    try:
        char = key.char
        if char == 'r':
            restart_flag = True
        elif char in ['a', 'b', 'c', 'd', 'u']:
            input_queue.put(char)
    except AttributeError:
        if key == keyboard.Key.right:
            input_queue.put('right')
        elif key == keyboard.Key.enter:
            input_queue.put('enter')

# Start the keyboard listener
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Function to clear the screen
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to display the menu with highlighting
def print_menu(selected):
    options = ['Geography', 'History', 'Science', 'Exit']
    for i, option in enumerate(options):
        if i == selected:
            print(f'\033[1;32m> {option}\033[0m')  # Highlighted in green
        else:
            print(f'  {option}')

# Menu system
def menu():
    global restart_flag
    current_selection = 0
    options = ['Geography', 'History', 'Science', 'Exit']
    while True:
        if restart_flag:
            restart_flag = False
            return 'restart'
        os.system('cls' if os.name == 'nt' else 'clear')
        print_menu(current_selection)
        key = input_queue.get()  # Wait for key press
        if key == 'right':
            current_selection = (current_selection + 1) % 4
        elif key == 'enter':
            return options[current_selection]

# Function to ask a question with timer
def ask_question(question, difficulty, timer_duration, penalty_time=0):
    cls()
    print(question['question'])
    for option in question['options']:
        print(option)

    start_time = time.time()
    answer_selected = None
    timer_expired = False
    stop_timer = threading.Event()  # Event to signal the timer to stop

    def countdown():
        nonlocal timer_expired
        while not stop_timer.is_set():
            elapsed_time = time.time() - start_time
            remaining_time = timer_duration - penalty_time - elapsed_time
            if remaining_time <= 0:
                timer_expired = True
                print("\rTime remaining: 0 seconds", end="", flush=True)
                break
            print(f"Time remaining: {int(remaining_time)} seconds\r", end="\r")
            time.sleep(1)
        if timer_expired:
            print("\nTime's up! Moving to the next question.")

    # Start the countdown timer in a separate thread
    timer_thread = threading.Thread(target=countdown)
    timer_thread.start()

    # Handle user input
    while not timer_expired:
        if restart_flag:
            stop_timer.set()  # Stop the timer
            timer_thread.join()  # Wait for the timer thread to finish
            return 'restart', 0
        if not input_queue.empty():
            key = input_queue.get()
            if key in ['a', 'b', 'c', 'd']:
                answer_selected = key
            elif key == 'enter' and answer_selected is not None:
                stop_timer.set()  # Stop the timer
                timer_thread.join()  # Wait for the timer thread to finish
                if answer_selected == question['answer']:
                    points = points_per_difficulty[difficulty]
                    return True, points
                else:
                    return False, 0
        time.sleep(0.01)  # Prevent busy waiting

    # If the timer expires, return a timeout result
    stop_timer.set()  # Ensure the timer stops
    timer_thread.join()  # Ensure the timer thread finishes
    return False, 0  # Timeout

# Post-question feedback and options
def post_question(correct, score, question):
    cls()
    print(f"{'Correct!' if correct else 'Wrong!'} Score: {score}")
    print(f"The correct answer was: {question['answer']}")
    if not correct:
        print("Press 'u' to redo (half-time penalty), 'r' to restart, or Enter to continue")
    else:
        print("Press 'r' to restart or Enter to continue")
    while True:
        if restart_flag:
            return 'restart'
        key = input_queue.get()
        if key == 'r':
            return 'restart'
        elif key == 'enter':
            return 'continue'
        elif key == 'u' and not correct:
            return 'redo'

# Run the quiz for a selected category
def run_quiz(category):
    global restart_flag
    # Shuffle questions within each difficulty
    easy = questions[category]['easy'][:]
    random.shuffle(easy)
    average = questions[category]['average'][:]
    random.shuffle(average)
    hard = questions[category]['hard'][:]
    random.shuffle(hard)
    all_questions = [(q, 'easy') for q in easy] + [(q, 'average') for q in average] + [(q, 'hard') for q in hard]
    score = 0
    penalty_time = 0  # Initialize penalty time
    for question, difficulty in all_questions:
        if restart_flag:
            return 'restart'
        result, points = ask_question(question, difficulty, 15, penalty_time)
        if result == 'restart':
            return 'restart'
        score += points
        action = post_question(result, score, question)
        if action == 'restart':
            return 'restart'
        elif action == 'redo':
            redo_result, redo_points = ask_question(question, difficulty, 15, penalty_time=7.5)
            if redo_result == 'restart':
                return 'restart'
            score += redo_points
            penalty_time = 7.5  # Apply half-time penalty for the next question
        else:
            penalty_time = 0  # Reset penalty time if no redo
    # After all questions
    print(f"Final score: {score}")
    if score == 150:
        print("Congratulations! You are a geography/history/science master!")
    elif score >= 100:
        print("Great job! You have a good grasp of geography/history/science.")
    elif score >= 50:
        print("I know this is intentional")
    else:
        print("Cool")
    print("Press Enter to return to menu or 'r' to restart")
    while True:
        if restart_flag:
            return 'restart'
        key = input_queue.get()
        if key == 'enter':
            
            break
        elif key == 'r':
            return 'restart'
        elif key == 'u':
            return 'redo'

# Main game loop
def main():
    while True:
        result = menu()
        if result == 'exit':
            listener.stop()
            break
        elif result == 'restart':
            continue
        else:
            category = result
            quiz_result = run_quiz(category)
            if quiz_result == 'restart':
                continue

if __name__ == '__main__':
    main()
