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
    # return f'<h1>{get_friends(247126134)}</h1>'
    return render_template('add_groups.html', request=request, groups=main.load_certified_groups())


app.run(host="0.0.0.0")
