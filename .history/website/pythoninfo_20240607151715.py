from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # Python variables to be passed to the template
    greeting = "Hello, World!"
    user_name = "John Doe"
    messages = ["Welcome to the site!", "Enjoy your stay!", "Check out our new features!"]
    
    # Render the template with the variables
    return render_template('index.html', greeting=greeting, user_name=user_name, messages=messages)

if __name__ == '__main__':
    app.run(debug=True)