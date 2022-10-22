from flask import Flask, request, render_template,  redirect, flash,  jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import *


app = Flask(__name__)

app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []
title = satisfaction_survey.title
instructions = satisfaction_survey.instructions
questions = satisfaction_survey.questions


@app.route('/')
def home_page():
    """Shows home page"""

    if len(responses) != 0 and len(responses) != 4:
        flash('You are trying to access an invalid question')
        return redirect(f'/questions/{len(responses)}')

    return render_template('home.html', title=title,
                           instructions=instructions)


@app.route('/questions/<int:q_number>')
def survey_page(q_number):
    """Shows survey questions"""

    if q_number != len(responses):
        if len(responses) == 4:
            return redirect('/thanks')
        flash('You are trying to access an invalid question')
        return redirect(f'/questions/{len(responses)}')

    question = questions[(q_number)]
    return render_template('questions.html', title=title,
                           instructions=instructions, question=question)


@app.route('/thanks')
def thank_you_page():
    """Shows thank you page after survey"""

    if len(responses) != 4:
        flash('You are trying to access an invalid question')
        return redirect(f'/questions/{len(responses)}')

    return render_template('thanks.html')


@app.route('/questions/answer', methods=["POST"])
def add_answer():
    """handles survey question post, redirects user to either
        next quesion or the thank-you page"""

    if request.form.get('choice'):
        answer = request.form.get('choice')
        responses.append(answer)
        q_number = len(responses)

        if len(responses) == len(questions):
            return redirect('/thanks')

    else:
        flash('Select an option')
        q_number = len(responses)

    return redirect(f'/questions/{q_number}')
