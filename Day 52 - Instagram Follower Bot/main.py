
# Day 52 - Instagram Follower Bot
# Safe practice version: sample data only

import json
from pathlib import Path


# Namoonay ke account ke followers
sample_followers = [
    "ali_python",
    "sara_codes",
    "ahmed_dev",
    "fatima_design",
    "usman_learning",
]


def find_followers(followers, search_text=""):
    """Follower list mein se naam dhoondein."""
    results = []

    for username in followers:
        if search_text.lower() in username.lower():
            results.append(username)

    return results


def save_followers(followers):
    """Followers ko JSON file mein save karein."""
    file_path = Path(__file__).parent / "followers.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(followers, file, indent=4)

    print(f"\nFollowers save ho gaye: {file_path.name}")


def main():
    print("Day 52 - Follower Finder Practice")
    print("---------------------------------")

    search_text = input(
        "Kis lafz se username dhoondna hai? "
        "(sab dekhne ke liye Enter dabayein): "
    ).strip()

    results = find_followers(sample_followers, search_text)

    print(f"\nKul matching followers: {len(results)}")

    for username in results:
        print("@", username)

    save_followers(results)

    print("\nPractice mukammal ho gayi.")


if __name__ == "__main__":
    main()
