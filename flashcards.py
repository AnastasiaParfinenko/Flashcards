import io
import logging
import re
import random
import argparse


class Flashcards:
    def __init__(self, import_file, export_file):
        self.cards = {}
        self.on = True
        self.buffer = io.StringIO()
        self.import_file = import_file
        self.export_file = export_file

    def app_print(self, text):
        self.buffer.write(text + "\n")
        print(text)

    def app_input(self):
        text = input()
        self.buffer.write(text + "\n")
        return text

    def get_file_name(self):
        self.app_print("File name:")
        return self.app_input()

    def user_add(self):
        self.app_print("The card:")
        while (term := self.app_input()) in self.cards:
            self.app_print(f'The card "{term}" already exists. Try again:')

        self.app_print("The definition of the card:")
        while (term_def := self.app_input()) in {v[0] for v in self.cards.values()}:
            self.app_print(f'The definition "{term_def}" already exists. Try again:')

        self.cards[term] = [term_def, 0]
        self.app_print(f'The pair("{term}": "{term_def}") has been added.')

    def user_remove(self):
        self.app_print("Which card?")
        term = self.app_input()

        if term in self.cards:
            del self.cards[term]
            self.app_print("The card has been removed.")
        else:
            self.app_print(f"""Can't remove "{term}": there is no such card." """)

    def user_import(self):
        file_name = self.import_file or self.get_file_name()

        try:
            with open(file_name, "r", encoding="utf-8") as file:
                pattern = r'"(.*?)":"(.*?)"\s(\d+)'
                matches = re.findall(pattern, file.read().strip())
                new_cards = {term: [term_def, int(mis)] for term, term_def, mis in matches}
            self.cards.update(new_cards)
            self.app_print(f"{len(new_cards)} cards have been loaded.")
        except FileNotFoundError:
            self.app_print("File not found.")

    def user_export(self):
        file_name = self.export_file or self.get_file_name()

        with open(file_name, "a", encoding="utf-8") as file:
            content = "".join(f'"{term}":"{self.cards[term][0]}" {self.cards[term][1]}' for term in self.cards)
            file.write(content)

        self.app_print(f"{len(self.cards)} cards have been saved.")

    def user_ask(self):
        self.app_print("How many times to ask?")
        n = int(self.app_input())
        terms = random.choices(list(self.cards), k=n)

        for term in terms:
            self.app_print(f'Print the definition of "{term}":')
            user_answer = self.app_input()
            correct_answer = self.cards[term][0]

            if user_answer == correct_answer:
                self.app_print("Correct!")
            else:
                self.cards[term][1] += 1
                right_term = next((k for k, v in self.cards.items() if v[0] == user_answer), None)
                if right_term:
                    self.app_print(f'Wrong. The right answer is "{correct_answer}", but your definition is correct for "{right_term}"')
                else:
                    self.app_print(f'Wrong. The right answer is "{correct_answer}".')

    def user_exit(self):
        self.app_print("Bye bye!")
        self.on = False

    def user_log(self):
        self.app_print("File name:")
        file_name = self.app_input()

        handler = logging.FileHandler(file_name, mode='a', encoding='utf-8')
        handler.setFormatter(logging.Formatter('%(message)s'))

        logger = logging.getLogger("FlashcardsLogger")
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)

        self.buffer.seek(0)
        content = self.buffer.read()
        logger.debug(content)

        handler.close()
        self.app_print('The log has been saved.')

    def user_hardest(self):
        max_mistakes = max((card[1] for card in self.cards.values()), default=0)
        if max_mistakes == 0:
            self.app_print("There are no cards with errors.")
            return

        hardest_cards = [term for term in self.cards if self.cards[term][1] == max_mistakes]
        term_list = '", "'.join(hardest_cards)
        if len(hardest_cards) == 1:
            self.app_print(f'The hardest card is "{term_list}". You have {max_mistakes} errors answering it.')
        else:
            self.app_print(f'The hardest cards are "{term_list}". You have {max_mistakes} errors answering them.')

    def user_reset(self):
        for value in self.cards.values():
            value[1] = 0
        self.app_print('Card statistics have been reset.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Input and output files")
    parser.add_argument("--import_from")
    parser.add_argument("--export_to")
    files = parser.parse_args()

    flashcards = Flashcards(files.import_from, files.export_to)
    if flashcards.import_file:
        flashcards.user_import()

    while flashcards.on:
        flashcards.app_print("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):")
        action = flashcards.app_input()
        getattr(flashcards, f"user_{action.split()[0]}", None)()

    if flashcards.export_file:
        flashcards.user_export()
