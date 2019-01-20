import pickle, sys
from sentiment_analyses.azure_sentiment import azure_sentiment_score
from sentiment_analyses.google_sentiment import GCP as google_sentiment_score
from sentiment_analyses.amazon_sentiment import AWS_SWAG as amazon_sentiment_score
from random import shuffle

class GameState:
    """Store the gamestate."""


    def __init__(self, n_human_players=1, n_ai_players=1, n_cards=10):
        """Initialise the gamestate and players."""

        # Load the answers
        with open("cards-against-humanity/answers.pickle", 'rb') as ans:
            self.answer_cards = pickle.load(ans)
            shuffle(self.answer_cards)
        self.used_answers = 0

        # Load the questions
        with open("cards-against-humanity/questions.pickle", 'rb') as qs:
            self.question_cards = pickle.load(qs)
            shuffle(self.question_cards)
        self.used_questions = 0

        # Make the human players
        self.human_players = []
        for _ in range(n_human_players):
            self.human_players.append(HumanPlayer(Player(self, n_cards)))

        # Make the AI players
        self.ai_players = []
        for _ in range(n_ai_players):
            self.ai_players.append(AIPlayer(Player(self, n_cards)))

    def pop_ans(self, n_cards):
        """Pop the top n cards"""

        cards = self.answer_cards[self.used_answers : self.used_answers + n_cards]
        self.used_answers += n_cards

        return cards

    def pop_q(self):
        """Pop the next question card"""

        card = self.question_cards[self.used_questions]
        self.used_questions += 1

        self.current_question = card

        return card

class Player:
    """Contains common functions"""
    def __init__(self, game, n_cards):
        self.card_strings = game.pop_ans(n_cards)

    def display_cards(self):
        for i in range(len(self.card_strings)):
            print(str(i+1) + ".", self.card_strings[i])

class HumanPlayer(Player):
    """Human player state"""
    def __init__(self, parent):
        self.player = parent

class AIPlayer(Player):
    def __init__(self, parent):
        self.player = parent


if __name__ == "__main__":

    game = GameState(n_human_players=1, n_ai_players=1, n_cards=10)

    q = game.pop_q()

    print("Current questions:", game.current_question)

    print("Human cards:")
    print(game.human_players[0].player.display_cards())

    blanks = q.count("_")
    if blanks == 1:
        phrase = q.replace("_", game.human_players[0].player.card_strings[2])
    else:
        print("Not ready!")
        sys.exit()

    print("Random Phrase:")
    print(phrase)

    print("azure analysis:")
    print(azure_sentiment_score(phrase))

    print("amazon analysis:")
    print(amazon_sentiment_score(phrase))

    print("google analysis:")
    print(google_sentiment_score(phrase))
