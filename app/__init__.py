from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta

app = Flask(__name__, template_folder='../templates', static_folder='../static')

app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(seconds=300)

from . import login, predict, verify, success, update_password