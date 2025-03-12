class Flashcards:
    def __init__(self):
        self.cards = {}
        self.on = True

    def user_add(self):
        print("The card:")
        while True:
            term = input()
            if term in self.cards:
                print(f'The card "{term}" already exists. Try again:')
            else:
                break

        print("The definition of the card:")
        while True:
            term_def = input()
            if term_def in self.cards.values():
                print(f'The definition "{term_def}" already exists. Try again:')
            else:
                break

        self.cards[term] = term_def
        print(f'The pair("{term}": "{term_def}") has been added.')

    def user_remove(self):
        print("Which card?")
        term = input()
        if term in self.cards:
            del self.cards[term]
            print("The card has been removed.")
        else:
            print(f"""Can't remove "{term}": there is no such card." """)

    def user_import(self):
        print("File name:")
        file_name = input()

        try:
            with open(file_name, "r", encoding="utf-8") as file:
                new_cards = {}
                cards_list = file.readline().strip().split('""')
                for card in cards_list:
                    term, term_def = card.strip('"').split(''":"'', 1)
                    new_cards[term] = term_def
            self.cards = self.cards | new_cards
            print(f"{len(new_cards)} cards have been loaded.")
        except FileNotFoundError:
            print("File not found.")

    def user_export(self):
        print("File name:")
        file_name = input()

        with open(file_name, "a", encoding="utf-8") as file:
            new_str = ''
            for term in self.cards:
                new_str += f'"{term}":"{self.cards[term]}"'

            file.write(new_str)

        print(f"{len(self.cards)} cards have been saved.")

    def user_ask(self):
        import random

        print("How many times to ask?")
        n = int(input())
        terms = random.choices(list(self.cards.keys()), k=n)
        for term in terms:
            print(f'Print the definition of "{term}":')
            user_answer = input()
            if user_answer == self.cards[term]:
                print("Correct!")
            else:
                right_term = next((k for k, v in self.cards.items() if v == user_answer), None)
                if right_term:
                    print(f'Wrong. The right answer is "{self.cards[term]}", but your definition is correct for "{right_term}"')
                else:
                    print(f'Wrong. The right answer is "{self.cards[term]}".')

    def user_exit(self):
        print("Bye bye!")
        self.on = False


if __name__ == "__main__":
    flashcards = Flashcards()
    while flashcards.on:
        print("Input the action (add, remove, import, export, ask, exit):")
        action = input().strip()
        getattr(flashcards, f"user_{action}", None)()
