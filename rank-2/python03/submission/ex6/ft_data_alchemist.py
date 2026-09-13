import random


def main() -> None:
    print("=== Game Data Alchemist ===")
    players = [
        "Alice",
        "bob",
        "Charlie",
        "dylan",
        "Emma",
        "Gregory",
        "john",
        "kevin",
        "Liam",
    ]
    print(f"Initial list of players: {players}")

    capitalized_players = [player.capitalize() for player in players]
    initially_capitalized = [
        player for player in players if player == player.capitalize()
    ]
    print(f"New list with all names capitalized: {capitalized_players}")
    print(f"New list of capitalized names only: {initially_capitalized}")

    scores = {
        player: random.randint(50, 1000) for player in capitalized_players
    }
    average_score = sum(scores[player] for player in scores) / len(scores)
    high_scores = {
        player: scores[player] for player in scores
        if scores[player] > average_score
    }

    print(f"Score dict: {scores}")
    print(f"Score average is {round(average_score, 2)}")
    print(f"High scores: {high_scores}")


if __name__ == "__main__":
    main()
