import random
import json
from game_data import data


DATA_STR_NAME = "name"
DATA_STR_COUNT = "follower_count"
DATA_STR_DESC = "description"
DATA_STR_COUNTRY = "country"

# if you don't want to see the score, set TEST_MODEL to False
TEST_MODEL = True


def read_game_data(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


def pick_two_numbers(data):
    return random.sample(data, 2)


def print_comparison(num1, num2):
    print(
        f"Compare\n"
        f"A: {num1[DATA_STR_NAME]} ({num1[DATA_STR_DESC]}) from {num1[DATA_STR_COUNTRY]}"
        f"{' (Test:' + str(num1[DATA_STR_COUNT]) + ')' if TEST_MODEL else ''}"
        f"\nwith\n"
        f"B: {num2[DATA_STR_NAME]} ({num2[DATA_STR_DESC]}) from {num2[DATA_STR_COUNTRY]}"
        f"{' (Test:' + str(num2[DATA_STR_COUNT]) + ')' if TEST_MODEL else ''}"
    )


def compare_numbers(num1, num2, choice):
    if choice == "A":
        return num1[DATA_STR_COUNT] > num2[DATA_STR_COUNT]
    return num2[DATA_STR_COUNT] > num1[DATA_STR_COUNT]


def main():
    score = 0
    available_items = data.copy()
    num1, num2 = pick_two_numbers(available_items)
    available_items.remove(num1)
    available_items.remove(num2)
    while True:
        print_comparison(num1, num2)

        choice = (
            input("Who has the higher value? Type 'A', 'B' or 'Q' to quit: ")
            .strip()
            .upper()
        )
        if choice == "Q":
            print(f"Thanks for playing! Your final score is {score}.")
            break

        if choice not in {"A", "B"}:
            print("Invalid choice! Please type 'A', 'B' or 'Q' to quit.")
            continue

        if compare_numbers(num1, num2, choice):
            score += 1
            print(f"Correct! Your score is {score}.")

            # check if all records are used
            if not available_items:
                print("No more items to choose from. You've seen all options!")
                print(f"Thanks for playing! Your final score is {score}.")
                break

            num1 = num2
            num2 = random.choice(available_items)
            available_items.remove(num2)

        else:
            print(f"Wrong! Game over. Your final score is {score}.")
            break


if __name__ == "__main__":
    main()
