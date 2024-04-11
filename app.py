from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

#The constant is used for consistency in spelling key names to store various objects:

RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route("/")
def show_survey_start():
    """Select a survey."""

    return render_template("survey_start.html", survey=survey)

@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear the session of responses."""

    session[RESPONSES_KEY] = []

    return redirect("/questions/0")

@app.route("/answer", methods=["POST"])
def handle_question():
    """Save response and redirect to next question."""

    #get the response choice 
    choice = request.form['answer']

    # add this response to the session
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if(len(responses) == len(survey.questions)):
        #Once all questions are answered, a way to thank the user:
        return redirect("/complete")
    
    else:
        return redirect("/questions/{len(responses)}")
    
@app.route("/questions/<int:qid>")
def show_question(qid):
    """Display current question."""
    responses = session.get(RESPONSES_KEY)

    if(responses is None):
        #if user tries to access the question page too quickly:
        return redirect("/")
    
    if(len(responses) == len(survey.questions)):
        #If they've answered all questions to thank users:
        return redirect("/complete")
    
    if(len(responses) != qid):
        #If users try to access questions out of order:
        flash("Invalid question id: {qid}.")
        return redirect("/questions/{len(responses)}")
    
    question = survey.questions[qid]
    return render_template(
        "question.html", question_num=qid, question=question)

@app.route("/complete")
def complete():
    """Survey is completed. Show the completion page."""

    return render_template("completion.html")


