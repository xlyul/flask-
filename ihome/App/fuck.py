from flask import Blueprint, redirect, url_for

fuck = Blueprint('fuck', __name__)


@fuck.route('/')
def shit():
    return redirect(url_for('house.index'))
