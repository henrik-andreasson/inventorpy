from flask import current_app
import click
from pprint import pprint
from rocketchat_API.rocketchat import RocketChat
from sqlalchemy import func
import time
from app import db


def register(app):
    @app.cli.group()
    def chat():
        """chat commands."""
        pass

    @chat.command()
    @click.argument('start')
    @click.argument('stop')
    def send(start, stop):
        """send who works today."""
        print("start: %s stop: %s" % (start, stop))
# #        today = datetime.utcnow()
#
#         # display_month = '{:02d}'.format(today.month)
#         # display_year = '{:02d}'.format(today.year)
#         # display_day = '{:02d}'.format(today.day)
#
#         # date_min = "%s-%s-%s 00:00" % (display_year, display_month,
#         #                                   display_day)
#         # date_max = "%s-%s-%s 12:31" % (display_year, display_month,
#         #                                   display_day)
#
#         work = Work.query.filter(func.datetime(Work.start) > start,
#                                  func.datetime(Work.stop) < stop).all()
#
#         rocket = RocketChat(current_app.config['ROCKET_USER'],
#                             current_app.config['ROCKET_PASS'],
#                             server_url=current_app.config['ROCKET_URL'])
#
#         for w in work:
#             msg = 'about to work: %s\t%s\t%s\t@%s ' % (w.start, w.stop,
#                                                        w.service, w.username)
#             pprint(rocket.chat_post_message(msg, channel=current_app.
#                                             config['ROCKET_CHANNEL']).json())
#             time.sleep(1)

    @app.cli.group()
    def user():
        """chat commands."""
        pass

    @user.command()
    @click.argument('username')
    @click.argument('password')
    @click.argument('email')
    def new(username, password, email):
        """create new user."""
        from app.models import User
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

    @user.command()
    @click.argument('username')
    @click.argument('password')
    def passwd(username, password):
        """set password user."""
        from app.models import User
        user = User.query.filter_by(username=username).first()
        if user is None:
            print("User not found")
        else:
            user.set_password(password)
            db.session.commit()

    @app.cli.group()
    def dbmgmt():
        """db commands."""
        pass

    @dbmgmt.command()
    def reindex():
        """update index."""
        from app import search
        search.delete_index()
        search.create_index()
