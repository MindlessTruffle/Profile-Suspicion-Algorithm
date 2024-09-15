import requests, time
import json
from collections import Counter

CERTIFIED_BADDIES_FILE = 'certified_baddies.json'
SUS_BADDIES_FILE = 'sus_baddies.json'

CERTIFIED_GROUPS_FILE = 'certified_groups.json'

# ----------- Certified Baddies Functions -----------z


def load_certified_baddies():
    try:
        with open(CERTIFIED_BADDIES_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_certified_baddies(user_ids):
    with open(CERTIFIED_BADDIES_FILE, 'w') as f:
        json.dump(user_ids, f, indent=4)


def add_certified_baddy(user_id):
    user_id = str(user_id)  # Ensure ID is stored as a string
    user_ids = load_certified_baddies()
    if user_id not in user_ids:
        user_ids.append(user_id)
        save_certified_baddies(user_ids)
        print(f"User ID {user_id} added to Certified Baddies.")
    else:
        print(f"User ID {user_id} already exists in Certified Baddies.")


def move_sus_to_certified(user_id):
    user_id = str(user_id)  # Ensure ID is treated as a string
    sus_baddies = load_sus_baddies()
    certified_baddies = load_certified_baddies()

    if user_id in sus_baddies:
        sus_baddies.remove(user_id)
        save_sus_baddies(sus_baddies)
        add_certified_baddy(user_id)
        print(
            f"User ID {user_id} moved from Sus Baddies to Certified Baddies.")
    else:
        print(f"User ID {user_id} not found in Sus Baddies.")


# ----------- Sus Baddies Functions -----------


def load_sus_baddies():
    try:
        with open(SUS_BADDIES_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_sus_baddies(user_ids):
    with open(SUS_BADDIES_FILE, 'w') as f:
        json.dump(user_ids, f, indent=4)


def add_sus_baddy(user_id):
    user_id = str(user_id)  # Ensure ID is stored as a string
    user_ids = load_sus_baddies()
    if user_id not in user_ids:
        user_ids.append(user_id)
        save_sus_baddies(user_ids)
        print(f"User ID {user_id} added to Sus Baddies.")
    else:
        print(f"User ID {user_id} already exists in Sus Baddies.")


# ----------- Certified Groups Functions -----------
def load_certified_groups():
    try:
        with open(CERTIFIED_GROUPS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_certified_groups(group_ids):
    with open(CERTIFIED_GROUPS_FILE, 'w') as f:
        json.dump(group_ids, f, indent=4)

def add_certified_group(group_id):
    group_id = str(group_id)  # Ensure ID is stored as a string
    group_ids = load_certified_groups()
    if group_id not in group_ids:
        group_ids.append(group_id)
        save_certified_groups(group_ids)
        print(f"Group ID {group_id} added to Certified Groups.")
    else:
        print(f"Group ID {group_id} already exists in Certified Groups.")

# ----------- Friend Ranking and Fetching -----------
def get_friends(user_id):
    url = f"https://friends.roblox.com/v1/users/{user_id}/friends"
    response = requests.get(url)
    if response.status_code == 200:
        friends = response.json().get('data', [])
        return [
            str(friend['id']) for friend in friends 
            if not friend.get('isBanned', False) and not friend.get('isDeleted', False)
        ]
    else:
        print(f"Problem fetching friends for user {user_id}: {response.status_code}")
        return []

def rank_shared_friends(user_ids):
    all_friends = []
    for user_id in user_ids:
        all_friends.extend(get_friends(user_id))

    friend_counts = Counter(all_friends)
    shared_friends = [
        friend for friend, count in friend_counts.items() if count > 1
    ]

    ranked_friends = sorted(shared_friends,
                            key=lambda x: friend_counts[x],
                            reverse=True)
    return ranked_friends, friend_counts


# ----------- Group Ranking and Fetching -----------
def get_group_members(group_id, limit=None):
    members = []
    cursor = ""
    while True:
        # url = f"https://groups.roblox.com/v1/groups/{group_id}/users?limit=100&sortOrder=Asc&cursor={cursor}"
        url = f"https://groups.roblox.com/v1/groups/{group_id}/users?limit={limit}&sortOrder=Dsc&cursor={cursor}"

        response = requests.get(url)
        data = response.json()

        new_members = [member['user']['userId'] for member in data['data']]
        members.extend(new_members)

        if limit and len(members) >= limit:
            return members[:limit]

        if data['nextPageCursor'] is None:
            break
        cursor = data['nextPageCursor']

    return members

def rank_shared_members(group_ids):
    all_members = []
    for group_id in group_ids:
        all_members.extend(get_group_members(group_id))

    member_counts = Counter(all_members)
    shared_members = [
        member for member, count in member_counts.items() if count > 1
    ]

    ranked_members = sorted(shared_members,
                            key=lambda x: member_counts[x],
                            reverse=True)

    print("Total Members (temp):", len(all_members))
    
    return ranked_members, member_counts

# ----------- Main Command Panel pre-frontend -----------
def main():
    while True:
        print("\nCommands:")
        print("1. Add user ID to Certified Baddies")
        print("2. Show ranked shared friends (Certified Baddies only)")
        print("3. Move a user ID from Sus Baddies to Certified Baddies")
        print("4. Add group ID to Certified Groups")
        print("5. Show ranked shared members (Certified Groups only)")

        command = input("Enter a command (1, 2, 3, 4, 5): ")

        if command == '1':
            user_id = input("Enter the user ID to add to Certified Baddies: ")
            add_certified_baddy(user_id)

        elif command == '2':
            user_ids = load_certified_baddies()
            if user_ids:
                ranked_shared_friends, friend_counts = rank_shared_friends(user_ids)
                print("\nRanked shared friends (Certified Baddies):")
                for i, friend_id in enumerate(ranked_shared_friends, 1):
                    print(
                        f"{i}. User ID: {friend_id}, Shared by: {friend_counts[friend_id]} users"
                    )
                
                move_to_sus_baddies = input("\nDo you want to add the top ranked users to Sus Baddies? (yes/no): ").lower()
                if move_to_sus_baddies == 'yes':
                    try:
                        x = int(input("How many of the top ranked users would you like to add?: "))
                        top_users = ranked_shared_friends[:x]
                        for user in top_users:
                            add_sus_baddy(user)
                    except ValueError:
                        print("Invalid number entered. Returning to the menu.")
            else:
                print("No Certified Baddies found. Please add some first.")

        elif command == '3':
            user_id = input(
                "Enter the user ID to move from Sus Baddies to Certified Baddies: "
            )
            move_sus_to_certified(user_id)

        elif command == '4':
            group_id = input("Enter the group ID to add to Certified Groups: ")
            add_certified_group(group_id)

        elif command == '5':
            group_ids = load_certified_groups()
            if group_ids:
                ranked_shared_members, member_counts = rank_shared_members(group_ids)
                print("\nRanked shared members (Certified Groups):")
                for i, member_id in enumerate(ranked_shared_members, 1):
                    print(f"{i}. User ID: {member_id}, Shared by: {member_counts[member_id]} users")

                move_to_sus_baddies = input("\nDo you want to add the top ranked users to Sus Baddies, to be manually reviewed? (yes/no): ").lower()
                if move_to_sus_baddies == 'yes':
                    try:
                        x = int(input("How many of the top ranked users would you like to add?: "))
                        top_users = ranked_shared_members[:x]
                        for user in top_users:
                            add_sus_baddy(user)
                    except ValueError:
                        print("Invalid number entered. Returning to the menu.")
                
        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()
