import os
import datetime
from datetime import date

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash



def apology (message, code=400):
    return render_template("apology.html", top=code, bottom=message)



# def get_random_question ():
#     return ??


# #
# def joker ():
#     return ??

# def fifty ():
#     return ??

# def double ():
#     return??


