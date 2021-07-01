from flask import Flask, render_template, request, send_file, render_template_string

app = Flask(__name__)

# scary names!!
blacklist1 = '_[]\'\"\\%'
blacklist2 = ['mro', 'config', 'base', 'join', 'os', 'subprocess']

@app.route('/')
def root():
    name = request.args.get('name')

    if name: 
        name = name.lower()
        if any([c in blacklist1 for c in name]) or any([b in name for b in blacklist2]):
            name = 'stop it :('

    index = render_template('index.html', name=name)
    return render_template_string(index)

@app.route('/src', methods=['GET'])
def src():
    return send_file('server.py')

# todo run NOPs
