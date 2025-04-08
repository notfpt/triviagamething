# I hope this is the last version
import time
import random
import threading
import sys
from pynput import keyboard
from os import system, name

class TriviaGame:
    def __init__(self):
        # Game state
        self.running = True
        self.in_menu = True
        self.in_question = False
        self.menu_index = 0
        self.current_score = 0
        self.current_category = ""
        self.current_difficulty = ""
        self.current_question_index = 0
        self.questions_in_round = []
        self.timer_thread = None
        self.time_remaining = 15
        self.halved_timer = False
        self.user_selection = None
        self.last_correct = False
        self.timer_active = False
        self.waiting_for_post_action = False
        
        # Menu options
        self.menu_options = ["Geography", "History", "Science", "Exit"]
        self.difficulty_levels = ["Easy", "Average", "Hard"]
        
        # Questions database
        self.questions = {
            "Geography": {
                "Easy": [
                    {"question": "What is the capital of France?", 
                     "options": ["Berlin", "Paris", "Madrid", "Rome"], 
                     "answer": "Paris"},
                    {"question": "Which ocean is the largest?", 
                     "options": ["Atlantic", "Indian", "Arctic", "Pacific"], 
                     "answer": "Pacific"},
                    {"question": "What is the longest river in the world?", 
                     "options": ["Amazon", "Nile", "Mississippi", "Yangtze"], 
                     "answer": "Nile"},
                    {"question": "Which continent is the largest by land area?", 
                     "options": ["North America", "Europe", "Asia", "Africa"], 
                     "answer": "Asia"},
                    {"question": "What is the capital of Japan?", 
                     "options": ["Tokyo", "Beijing", "Seoul", "Bangkok"], 
                     "answer": "Tokyo"},
                ],
                "Average": [
                    {"question": "Which country has the most islands in the world?", 
                     "options": ["Indonesia", "Philippines", "Sweden", "Greece"], 
                     "answer": "Sweden"},
                    {"question": "What is the smallest country in the world?", 
                     "options": ["Monaco", "Nauru", "Vatican City", "San Marino"], 
                     "answer": "Vatican City"},
                    {"question": "Which mountain range separates Europe from Asia?", 
                     "options": ["Alps", "Himalayas", "Andes", "Urals"], 
                     "answer": "Urals"},
                    {"question": "Which African country was formerly known as Abyssinia?", 
                     "options": ["Ethiopia", "Sudan", "Somalia", "Kenya"], 
                     "answer": "Ethiopia"},
                    {"question": "Which strait separates Asia from North America?", 
                     "options": ["Strait of Gibraltar", "Strait of Magellan", "Bering Strait", "Strait of Malacca"], 
                     "answer": "Bering Strait"},
                ],
                "Hard": [
                    {"question": "What is the world's largest active volcano?", 
                     "options": ["Mount Etna", "Mount Vesuvius", "Mauna Loa", "Mount Fuji"], 
                     "answer": "Mauna Loa"},
                    {"question": "Which country has the most time zones?", 
                     "options": ["Russia", "United States", "France", "Australia"], 
                     "answer": "France"},
                    {"question": "What is the largest desert in the world?", 
                     "options": ["Sahara", "Arabian", "Antarctic", "Gobi"], 
                     "answer": "Antarctic"},
                    {"question": "The city of Timbuktu is located in which country?", 
                     "options": ["Nigeria", "Mali", "Ethiopia", "Chad"], 
                     "answer": "Mali"},
                    {"question": "What percentage of the River Nile runs through Egypt?", 
                     "options": ["22%", "33%", "48%", "75%"], 
                     "answer": "22%"},
                ],
            },
            "History": {
                "Easy": [
                    {"question": "Who was the first President of the United States?", 
                     "options": ["Thomas Jefferson", "Abraham Lincoln", "George Washington", "John Adams"], 
                     "answer": "George Washington"},
                    {"question": "In which year did World War II end?", 
                     "options": ["1943", "1945", "1947", "1950"], 
                     "answer": "1945"},
                    {"question": "Which ancient civilization built the pyramids?", 
                     "options": ["Romans", "Greeks", "Egyptians", "Mayans"], 
                     "answer": "Egyptians"},
                    {"question": "Who was the famous nurse during the Crimean War?", 
                     "options": ["Clara Barton", "Florence Nightingale", "Marie Curie", "Susan B. Anthony"], 
                     "answer": "Florence Nightingale"},
                    {"question": "The Renaissance period began in which country?", 
                     "options": ["France", "Italy", "England", "Spain"], 
                     "answer": "Italy"},
                ],
                "Average": [
                    {"question": "Who was the leader of the Soviet Union during the Cuban Missile Crisis?", 
                     "options": ["Lenin", "Stalin", "Khrushchev", "Gorbachev"], 
                     "answer": "Khrushchev"},
                    {"question": "Which year did the Berlin Wall fall?", 
                     "options": ["1987", "1989", "1991", "1993"], 
                     "answer": "1989"},
                    {"question": "The Battle of Hastings took place in which year?", 
                     "options": ["1066", "1086", "1106", "1166"], 
                     "answer": "1066"},
                    {"question": "Who was the last Pharaoh of Ancient Egypt?", 
                     "options": ["Nefertiti", "Cleopatra", "Hatshepsut", "Ramses"], 
                     "answer": "Cleopatra"},
                    {"question": "Which disease ravaged Europe in the 14th century?", 
                     "options": ["Smallpox", "Black Death", "Cholera", "Typhoid Fever"], 
                     "answer": "Black Death"},
                ],
                "Hard": [
                    {"question": "During which battle was the HMS Victory commanded by Lord Nelson?", 
                     "options": ["Battle of the Nile", "Battle of Trafalgar", "Battle of Copenhagen", "Battle of Cape St. Vincent"], 
                     "answer": "Battle of Trafalgar"},
                    {"question": "Who was the last Emperor of Russia?", 
                     "options": ["Nicholas II", "Alexander III", "Ivan the Terrible", "Peter the Great"], 
                     "answer": "Nicholas II"},
                    {"question": "The Defenestration of Prague helped trigger which conflict?", 
                     "options": ["Seven Years' War", "Hundred Years' War", "Thirty Years' War", "War of Spanish Succession"], 
                     "answer": "Thirty Years' War"},
                    {"question": "Who was the first female Prime Minister of India?", 
                     "options": ["Benazir Bhutto", "Sirimavo Bandaranaike", "Golda Meir", "Indira Gandhi"], 
                     "answer": "Indira Gandhi"},
                    {"question": "Which ancient empire was ruled by Darius I?", 
                     "options": ["Roman", "Greek", "Persian", "Babylonian"], 
                     "answer": "Persian"},
                ],
            },
            "Science": {
                "Easy": [
                    {"question": "What is the chemical symbol for gold?", 
                     "options": ["Gd", "Go", "Au", "Ag"], 
                     "answer": "Au"},
                    {"question": "Which planet is known as the Red Planet?", 
                     "options": ["Jupiter", "Venus", "Mars", "Saturn"], 
                     "answer": "Mars"},
                    {"question": "What is the main component of air?", 
                     "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"], 
                     "answer": "Nitrogen"},
                    {"question": "How many bones are in the adult human body?", 
                     "options": ["106", "206", "306", "406"], 
                     "answer": "206"},
                    {"question": "What is the hardest natural substance on Earth?", 
                     "options": ["Platinum", "Steel", "Diamond", "Titanium"], 
                     "answer": "Diamond"},
                ],
                "Average": [
                    {"question": "What is the speed of light in a vacuum?", 
                     "options": ["299,792 km/s", "199,792 km/s", "399,792 km/s", "499,792 km/s"], 
                     "answer": "299,792 km/s"},
                    {"question": "Which element has the atomic number 1?", 
                     "options": ["Helium", "Hydrogen", "Lithium", "Carbon"], 
                     "answer": "Hydrogen"},
                    {"question": "What is the powerhouse of the cell?", 
                     "options": ["Nucleus", "Ribosome", "Mitochondria", "Endoplasmic reticulum"], 
                     "answer": "Mitochondria"},
                    {"question": "What is the unit of electrical resistance?", 
                     "options": ["Volt", "Ampere", "Watt", "Ohm"], 
                     "answer": "Ohm"},
                    {"question": "Who formulated the theory of relativity?", 
                     "options": ["Isaac Newton", "Albert Einstein", "Niels Bohr", "Galileo Galilei"], 
                     "answer": "Albert Einstein"},
                ],
                "Hard": [
                    {"question": "What is the name of the process by which plants make their food?", 
                     "options": ["Respiration", "Photosynthesis", "Fermentation", "Digestion"], 
                     "answer": "Photosynthesis"},
                    {"question": "Which part of the human brain is responsible for balance and coordination?", 
                     "options": ["Cerebrum", "Cerebellum", "Medulla", "Thalamus"], 
                     "answer": "Cerebellum"},
                    {"question": "What is the half-life of Carbon-14?", 
                     "options": ["3,700 years", "5,730 years", "7,500 years", "10,300 years"], 
                     "answer": "5,730 years"},
                    {"question": "Which scientist discovered penicillin?", 
                     "options": ["Louis Pasteur", "Alexander Fleming", "Joseph Lister", "Robert Koch"], 
                     "answer": "Alexander Fleming"},
                    {"question": "What is the most abundant element in the universe?", 
                     "options": ["Hydrogen", "Helium", "Oxygen", "Carbon"], 
                     "answer": "Hydrogen"},
                ],
            }
        }
        
        # Start keyboard listener
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()
    
    def clear_screen(self):
        """Clear the terminal screen."""
        if name == 'nt':  # for Windows
            _ = system('cls')
        else:  # for Mac and Linux
            _ = system('clear')
    
    def on_key_press(self, key):
        """Handle keyboard input."""
        try:
            # Menu navigation
            if self.in_menu:
                if key == keyboard.Key.right:
                    self.menu_index = (self.menu_index + 1) % len(self.menu_options)
                    self.display_menu()
                elif key == keyboard.Key.enter:
                    selection = self.menu_options[self.menu_index]
                    if selection == "Exit":
                        self.running = False
                    else:
                        self.current_category = selection
                        self.start_category()
            
            # Question answering
            elif self.in_question and self.timer_active:
                if hasattr(key, 'char') and key.char in ['a', 'b', 'c', 'd']:
                    self.user_selection = key.char
                    # Print confirmation of selection
                    print(f"\nYou selected: {key.char}")
                    sys.stdout.flush()
                elif hasattr(key, 'char') and key.char == 'r':  # Restart
                    self.stop_timer()
                    self.restart_game()
                elif key == keyboard.Key.enter:
                    if self.user_selection is not None:
                        self.stop_timer()
                        self.check_answer()
                    else:
                        print("\nPlease select an answer (a, b, c, d) first!")
                        sys.stdout.flush()
            
            # Post-question options
            elif self.waiting_for_post_action:
                if hasattr(key, 'char') and key.char == 'r':  # Restart
                    self.restart_game()
                elif hasattr(key, 'char') and key.char == 'u' and not self.last_correct:  # Redo option
                    self.waiting_for_post_action = False
                    self.redo_question()
                elif key == keyboard.Key.enter:  # Continue
                    self.waiting_for_post_action = False
                    self.next_question()
                    
        except (AttributeError, TypeError) as e:
            print(f"\nKey error: {e}")  # Helpful for debugging
            pass  # Ignore special keys
    
    def display_menu(self):
        """Display the main menu."""
        self.clear_screen()
        print("==== TRIVIA GAME ====")
        print("Navigate using right arrow key, select with Enter\n")
        
        for i, option in enumerate(self.menu_options):
            if i == self.menu_index:
                print(f"> {option} <")
            else:
                print(f"  {option}  ")
    
    def start_category(self):
        """Start playing the selected category."""
        self.in_menu = False
        self.current_score = 0
        
        # Create a list of questions for all difficulty levels
        self.questions_in_round = []
        for difficulty in self.difficulty_levels:
            questions = self.questions[self.current_category][difficulty].copy()
            random.shuffle(questions)
            for question in questions[:5]:  # Take only 5 questions from each difficulty
                question_copy = question.copy()
                question_copy["difficulty"] = difficulty
                self.questions_in_round.append(question_copy)
        
        self.current_question_index = 0
        self.display_question()
    
    def display_question(self):
        """Display a question to the user."""
        self.clear_screen()
        self.in_question = True
        self.user_selection = None
        self.waiting_for_post_action = False
        
        if self.current_question_index >= len(self.questions_in_round):
            self.end_round()
            return
        
        # Get current question
        question_data = self.questions_in_round[self.current_question_index]
        self.current_difficulty = question_data["difficulty"]
        
        # Shuffle options
        options = question_data["options"].copy()
        random.shuffle(options)
        
        # Store the shuffled options to check answer
        self.current_options = options
        self.current_answer = question_data["answer"]
        
        # Display question info
        print(f"==== {self.current_category} - {self.current_difficulty} ====")
        print(f"Question {self.current_question_index + 1}/{len(self.questions_in_round)}")
        print(f"Score: {self.current_score}\n")
        
        # Display question and options
        print(question_data["question"])
        print("a) " + options[0])
        print("b) " + options[1])
        print("c) " + options[2])
        print("d) " + options[3])
        print("\nSelect your answer (a, b, c, d) and press Enter to confirm.")
        print("Time remaining: Starting...", end="")
        sys.stdout.flush()
        
        # Start timer
        self.time_remaining = 15 if not self.halved_timer else 7.5
        self.start_timer()
    
    def start_timer(self):
        """Start the timer for the question."""
        self.timer_active = True
        self.timer_thread = threading.Thread(target=self.countdown_timer)
        self.timer_thread.daemon = True
        self.timer_thread.start()
    
    def stop_timer(self):
        """Stop the timer."""
        self.timer_active = False
        if self.timer_thread and self.timer_thread.is_alive():
            # Let the thread finish naturally
            pass
    
    def countdown_timer(self):
        """Countdown timer for the question with continuous display update."""
        start_time = time.time()
        end_time = start_time + self.time_remaining
        
        while time.time() < end_time and self.timer_active:
            # Calculate remaining time
            self.time_remaining = end_time - time.time()
            
            # Update the display
            self.update_display_during_timer()
            
            # Sleep a short time
            time.sleep(0.1)
        
        if self.timer_active:  # If timer finished naturally (not stopped)
            self.timer_active = False
            self.timeout()
    
    def update_display_during_timer(self):
        """Update the display while the timer is running."""
        self.clear_screen()
        
        # Get current question
        question_data = self.questions_in_round[self.current_question_index]
        
        # Display question info
        print(f"==== {self.current_category} - {self.current_difficulty} ====")
        print(f"Question {self.current_question_index + 1}/{len(self.questions_in_round)}")
        print(f"Score: {self.current_score}\n")
        
        # Display question and options
        print(question_data["question"])
        
        # Show options, highlight selected one if any
        for i, option in enumerate(['a', 'b', 'c', 'd']):
            if option == self.user_selection:
                print(f"▶ {option}) {self.current_options[i]}")
            else:
                print(f"  {option}) {self.current_options[i]}")
        
        print("\nSelect your answer (a, b, c, d) and press Enter to confirm.")
        print(f"Time remaining: {self.time_remaining:.1f} seconds")
        if self.user_selection:
            print(f"Current selection: {self.user_selection}")
        sys.stdout.flush()  # Ensure the display is updated
    
    def timeout(self):
        """Handle timeout for a question."""
        self.clear_screen()
        print("==== Time's up! ====")
        
        question_data = self.questions_in_round[self.current_question_index]
        print(f"\nQuestion: {question_data['question']}")
        print(f"The correct answer was: {self.current_answer}\n")
        
        print(f"Your score: {self.current_score}")
        print("\nOptions:")
        print("r - Restart")
        print("u - Redo this question (time will be halved)")
        print("Enter - Continue to next question")
        
        self.last_correct = False
        self.waiting_for_post_action = True
    
    def check_answer(self):
        """Check the user's answer."""
        self.clear_screen()
        
        # Map user selection to option index
        option_index = ord(self.user_selection) - ord('a')
        selected_option = self.current_options[option_index]
        
        # Get question data
        question_data = self.questions_in_round[self.current_question_index]
        
        # Display the question again
        print(f"\nQuestion: {question_data['question']}")
        
        # Check if answer is correct
        is_correct = selected_option == self.current_answer
        self.last_correct = is_correct
        
        # Update score
        if is_correct:
            points = 5 if self.current_difficulty == "Easy" else (10 if self.current_difficulty == "Average" else 15)
            self.current_score += points
            print("Correct! 🎉")
        else:
            print("Wrong answer!")
            print(f"You selected: {selected_option}")
            print(f"The correct answer was: {self.current_answer}")
        
        print(f"\nYour score: {self.current_score}")
        
        # Reset halved timer flag for next question
        if is_correct:
            self.halved_timer = False
            print("\nOptions:")
            print("r - Restart")
            print("Enter - Continue to next question")
        else:
            print("\nOptions:")
            print("r - Restart")
            print("u - Redo this question (time will be halved)")
            print("Enter - Continue to next question")
        
        self.waiting_for_post_action = True
    
    def redo_question(self):
        """Redo the current question with halved time."""
        self.halved_timer = True
        self.user_selection = None
        self.display_question()
    
    def next_question(self):
        """Move to the next question."""
        self.current_question_index += 1
        self.user_selection = None
        self.halved_timer = False
        self.display_question()
    
    def end_round(self):
        """End the current round."""
        self.clear_screen()
        print(f"==== {self.current_category} Round Complete! ====")
        
        # Calculate maximum possible score
        max_score = 0
        for difficulty in self.difficulty_levels:
            if difficulty == "Easy":
                max_score += 5 * 5  # 5 questions × 5 points
            elif difficulty == "Average":
                max_score += 5 * 10  # 5 questions × 10 points
            else:  # Hard
                max_score += 5 * 15  # 5 questions × 15 points
        
        print(f"Final Score: {self.current_score}/{max_score}")
        print("\nPress Enter to return to the main menu.")
        
        self.waiting_for_post_action = True
        
        # Wait for keyboard input in the listener thread
        while self.waiting_for_post_action and self.running:
            time.sleep(0.1)
        
        self.in_menu = True
        self.display_menu()
    
    def restart_game(self):
        """Restart the game."""
        self.in_menu = True
        self.current_score = 0
        self.current_question_index = 0
        self.halved_timer = False
        self.waiting_for_post_action = False
        self.display_menu()
    
    def run(self):
        """Main game loop."""  # 500 lines anniversary
        self.display_menu()
        
        while self.running:
            time.sleep(0.1)  # Prevent high CPU usage

# Run the game
if __name__ == "__main__":
    game = TriviaGame()
    game.run()
