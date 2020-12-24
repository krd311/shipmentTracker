from flask import Flask, redirect, url_for, render_template,request
import main

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/", methods = ["POST"])
def enterTracker():
    text = request.form["u"]
    processed_text = main.main(text)
    processed_text[0] += "\n"
    return render_template("index.html", status =f"Tracking history for {text.strip()}:<br><br>" + processed_text[1].replace("\n","<br><br>") + processed_text[0].replace("\n","<br>") + '<br>')

if __name__ == "__main__":
    app.run()
