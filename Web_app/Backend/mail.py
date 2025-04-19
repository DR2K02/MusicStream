from flask_mail import Message
from .mail_flask import mail
from jinja2 import Environment,FileSystemLoader

def sendMail(RECEIVER_ADDRESS,SUBJECT,MESSAGE,ATTACHMENT=None,mime_type="application/pdf",formatted_report_data=None):
    try:
        msg=Message(recipients=[RECEIVER_ADDRESS],
                    sender='amarbose1897@gmail.com',
                    body=MESSAGE,
                    subject=SUBJECT)
        if ATTACHMENT:
            with open(ATTACHMENT,'rb')as fp:
                if mime_type=="application/pdf":
                    msg.attach(f"{RECEIVER_ADDRESS}_report.pdf",mime_type,fp.read())
                elif mime_type=="application/x-zip":
                    msg.attach(f"{RECEIVER_ADDRESS}_exported.zip",mime_type,fp.read())
                elif mime_type=="text/csv":
                    msg.attach(f"{RECEIVER_ADDRESS}_data.csv",mime_type,fp.read())

        if formatted_report_data:
            env=Environment(loader=FileSystemLoader('./BACKEND/templates'))

            template=env.get_template('report.html')

            rendered_html=template.render(formatted_report_data=formatted_report_data)
            msg.html=rendered_html

        mail.send(msg)
        return True
    except Exception as e:
        print(e)
        return False

