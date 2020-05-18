from flask import current_app, render_template, Flask
from flask_mail import Message
from . import mail, create_app
from threading import Thread


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, attachments=None, sync=False, **kwargs):
    """Using thread to handle the email sending tasks , using the app context to avoid passing it as an argument
     the flask send-email lib is used to send the message. In order to add different templates for email , add the text
     body and html page to the templates/email folder."""
    app = current_app._get_current_object()
    msg = Message(subject,
                  sender=app.config['MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    if attachments:
        for attachment in attachments:
            msg.attach(*attachment)
    if sync:
        mail.send(msg)
    else:
        Thread(target=send_async_email,
               args=(current_app._get_current_object(), msg)).start()
