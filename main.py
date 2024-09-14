import requests
from collections import Counter

def get_friends(user_id):
    url = f"https://friends.roblox.com/v1/users/{user_id}/friends"
    response = requests.get(url)
    if response.status_code == 200:
        return [friend['id'] for friend in response.json()['data']]
    else:
        print(f"uh oh problem fetching friends for user {user_id}: {response.status_code}")
        return []

def rank_shared_friends(user_ids):
    all_friends = []
    for user_id in user_ids:
        all_friends.extend(get_friends(user_id))

    friend_counts = Counter(all_friends)
    shared_friends = [friend for friend, count in friend_counts.items() if count > 1]

    ranked_friends = sorted(shared_friends, key=lambda x: friend_counts[x], reverse=True)
    return ranked_friends, friend_counts

def main():
    user_ids = ["576194135", "1056339846", "296069534", "44499829", "1576722220"]

    ranked_shared_friends, friend_counts = rank_shared_friends(user_ids)

    print("\nRanked shared friends:")
    for i, friend_id in enumerate(ranked_shared_friends, 1):
        print(f"{i}. User ID: {friend_id}, Shared by: {friend_counts[friend_id]} users")

if __name__ == "__main__":
    main()