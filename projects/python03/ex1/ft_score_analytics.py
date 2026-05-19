import sys


def parse_scores(arguments: list[str]) -> list[int]:
    scores: list[int] = []
    for argument in arguments:
        try:
            scores.append(int(argument))
        except ValueError:
            print(f"Invalid parameter: '{argument}'")
    return scores


def print_usage() -> None:
    print(
        "No scores provided. Usage: "
        "python3 ft_score_analytics.py <score1> <score2> ..."
    )


def main() -> None:
    print("=== Player Score Analytics ===")
    scores = parse_scores(sys.argv[1:])
    if len(scores) == 0:
        print_usage()
        return

    total_score = sum(scores)
    high_score = max(scores)
    low_score = min(scores)
    print(f"Scores processed: {scores}")
    print(f"Total players: {len(scores)}")
    print(f"Total score: {total_score}")
    print(f"Average score: {total_score / len(scores)}")
    print(f"High score: {high_score}")
    print(f"Low score: {low_score}")
    print(f"Score range: {high_score - low_score}")


if __name__ == "__main__":
    main()
