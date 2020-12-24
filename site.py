from flask import Flask, redirect, url_for, render_template,request
import main
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", content="Testing")

@app.route("/", methods = ["POST"])
def enterTracker():
    text = request.form["u"]
    processed_text = main.main(text)
    processed_text += "\n"
    return render_template("index.html", status = f"Tracking history for <strong>{text}</strong>:<br><br>" + processed_text.replace("\n","<br>"))

if __name__ == "__main__":
    app.run()
