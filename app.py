from flask import Flask, render_template, request
import main

app = Flask(__name__)

@app.route('/')
def hello():
    # return f'<h1>{get_friends(247126134)}</h1>'
    return render_template('index.html')


@app.route('/add_groups', methods=['GET', 'POST'])
def add_groups():
    if request.method == 'POST':
        groupIds = request.form["groupIds"].split(",")
        for groupId in groupIds:
            try:
                int(groupId)
                main.add_certified_group(groupId)
            except:
                print("Non-Int")
        
        return render_template('add_groups.html',
                               request=request,
                               groups=main.load_certified_groups())

    return render_template('add_groups.html', request=request, groups=main.load_certified_groups())

@app.route('/add_accounts', methods=['GET', 'POST'])
def add_accounts():
    if request.method == 'POST':
        accountIds = request.form["accountIds"].split(",")
        for accountId in accountIds:
            try:
                int(accountId)
                main.add_certified_baddy(accountId)
            except:
                print("Non-Int")

        return render_template('add_accounts.html',
                               request=request,
                               accounts=main.load_certified_baddies())

    return render_template('add_accounts.html', request=request, accounts=main.load_certified_baddies())

@app.route('/analyse_groups', methods=['GET', 'POST'])
def analyse_groups():
    sorted_rank_data = []
    result_found = False
    if request.method == 'POST':
        # Handle the "Run it" button submission
        if 'runButton' in request.form:
            group_ids = main.load_certified_groups()
            if group_ids:
                ranked_shared_members, member_counts = main.rank_shared_members(group_ids)
                for i, member_id in enumerate(ranked_shared_members, 1):
                    sorted_rank_data.append((member_id, member_counts[member_id]))
                result_found = True  # Result is ready, show the form and button

        # Handle form submission (flagThreshold and form submission)
        elif 'submitButton' in request.form and 'flagThreshold' in request.form:
            flag_threshold = int(request.form["flagThreshold"])
            print(f"Flag Threshold: {flag_threshold}")
    
            # Parse the ranked_accounts from the form data
            ranked_accounts = []
            i = 0
            while f'member_id_{i}' in request.form and f'count_{i}' in request.form:
                member_id = request.form[f'member_id_{i}']
                count = int(request.form[f'count_{i}'])
                ranked_accounts.append((member_id, count))
                i += 1
    
            # Limit the ranked_accounts to the flag_threshold
            flagged_accounts = ranked_accounts[:flag_threshold]
    
            # Print the ranked_accounts
            print("Ranked accounts:")
            for account in flagged_accounts:
                print(f"Member ID: {account[0]}, Count: {account[1]}")

                main.add_sus_baddy(account[0])
    
            # Set result_found to True so the form and results table are displayed again
            result_found = True
            sorted_rank_data = ranked_accounts

    # Render the template and pass whether results were found or not
    return render_template('analyse_groups.html',
                           request=request,
                           ranked_accounts=sorted_rank_data,
                           result_found=result_found)

@app.route('/analyse_accounts', methods=['GET', 'POST'])
def analyse_accounts():
    sorted_rank_data = []
    result_found = False
    if request.method == 'POST':
        # Handle the "Run it" button submission
        if 'runButton' in request.form:
            account_ids = main.load_certified_baddies()
            if account_ids:
                ranked_shared_friends, friend_counts = main.rank_shared_friends(account_ids)
                for i, account_id in enumerate(ranked_shared_friends, 1):
                    sorted_rank_data.append((account_id, friend_counts[account_id]))
                result_found = True  # Result is ready, show the form and button

        # Handle form submission (flagThreshold and form submission)
        elif 'submitButton' in request.form and 'flagThreshold' in request.form:
            flag_threshold = int(request.form["flagThreshold"])
            print(f"Flag Threshold: {flag_threshold}")

            # Parse the ranked_accounts from the form data
            ranked_accounts = []
            i = 0
            while f'account_id_{i}' in request.form and f'count_{i}' in request.form:
                account_id = request.form[f'account_id_{i}']
                count = int(request.form[f'count_{i}'])
                ranked_accounts.append((account_id, count))
                i += 1

            # Limit the ranked_accounts to the flag_threshold
            flagged_accounts = ranked_accounts[:flag_threshold]

            # Print the ranked_accounts
            print("Ranked accounts:")
            for account in flagged_accounts:
                print(f"Account ID: {account[0]}, Count: {account[1]}")

                main.add_sus_baddy(account[0])

            # Set result_found to True so the form and results table are displayed again
            result_found = True
            sorted_rank_data = ranked_accounts

    # Render the template and pass whether results were found or not
    return render_template('analyse_accounts.html',
                           request=request,
                           ranked_accounts=sorted_rank_data,
                           result_found=result_found)

app.run(host="0.0.0.0")
