from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # render your html template
    return render_template('index.html')

@app.route('/my-link/')
def do_something():
    # when the button was clicked, 
    # the code below will be execute.
    print 'do something here'
    return 'click'

if __name__ == '__main__':
    app.run(debug=True)