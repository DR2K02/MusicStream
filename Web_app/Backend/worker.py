from celery import Celery,Task,shared_task
from celery.schedules import crontab
from . import models
from .mail import sendMail
import csv
from datetime import date
from sqlalchemy.sql import func
from .database import db

#making celery app
def create_celery_app(app):
    class FlaskTask(Task):
        def __call__(self,*args,**kwargs):
            with app.app_context():
                return self.run(*args,**kwargs)

    celery_app=Celery(
        app.name,
        broker="redis://127.0.0.1:6379/1",
        backend="redis://127.0.0.1:6379/2",
        task_cls=FlaskTask,
        broker_connection_retry_on_startup=True,
        timezone='Asia/Kolkata')

    celery_app.conf.beat_schedule={
        'send-monthly-creator-report':{
            'task':'Scheduled Job',
            'schedule':120,
        },
        'daily-reminder':{
            'task':'Daily Reminder',
            'schedule':120,
        },
    }

    celery_app.set_default()
    return celery_app

#Reminder job to send daily reminder to the users for the visiting the page
@shared_task(name="Daily Reminder")
def send_daily_remainder_emails():
    try:
        #Get the current date
        # current_date=date.today()

        #Query users who haven't made any opened the app on the current day

        user_without_activity=(
            db.session.query(models.User)
            .filter(~models.User.is_admin)
            .all()
        
        ) 
        # Send reminder emails
        for user in user_without_activity:
            subject="Daily Reminder"
            message=f"Dear {user.name}, Please visit the app to stay updated."
            sendMail(user.email,subject,message)

        return True
    except Exception as e:
        print(e)
        return False
 
    
@shared_task(name="Scheduled Job")
def setup_periodic_tasks():
    try:

        users=models.User.query.filter_by(is_creator=True).all()

        for user in users:
            creator_monthly_report(user)

        return True
    except Exception as e:
        print(e)
        return False

def creator_monthly_report(creator):
    try:
        # Get albums created by the creator
        albums_created = models.Album.query.filter_by(creator=creator.user_id).all()

        # Prepare formatted data for the report
        formatted_report_data = {
            "albums_created": [],
            "songs_created": [],
        }

        # Extract songs from each album
        for album in albums_created:
            formatted_album = {
                "album_id": album.album_id,
                "album_name": album.album_name,
                "album_artist": album.album_artist,
                "songs": []
            }

            # Extract songs associated with the album
            songs_in_album = models.Song.query.filter_by(collection=album.album_id).all()
            for song in songs_in_album:
                formatted_song = {
                    "song_id": song.song_id,
                    "song_name": song.song_name,
                    "lyrics": song.lyrics,
                    "genre": song.genre,
                    "duration": song.duration,
                    "date_created": song.date_created
                }
                formatted_album["songs"].append(formatted_song)
                formatted_report_data["songs_created"].append(formatted_song)

            formatted_report_data["albums_created"].append(formatted_album)
            print(formatted_report_data)

        # Send the email to the creator
        res = sendMail(creator.email, "Monthly Creator Report", "The monthly report of your creations is attached below.", formatted_report_data=formatted_report_data)
        return res

    except Exception as e:
        print(e)
        return False



@shared_task(name="Export Job")
def export_data(album_id):
    try:

        res = export_album_data(album_id=album_id)
        return res
    except Exception as e:
        print(e)
        return False
            
    


def export_album_data(album_id):
    try:
        #get the Albums to export
        album=models.Album.query.get(int(album_id))

        #get the admin from database
        admin=models.User.query.get(int(album.creator))

        file_path="album_export.csv"

        with open(file_path,'w',newline='') as csv_file:
            fieldnames=['album_id','album_name','album_artist']
            writer=csv.DictWriter(csv_file,fieldnames=fieldnames)

            writer.writerow({
                'album_id':album.album_id,
                'album_name':album.album_name,
                'album_artist':album.album_artist,
            })

        res = sendMail(admin.email,"Albums Exports","The ALbum info has been exported and attached below in CSV file format.",file_path,"text/csv")
        return res
    except Exception as e:
        print(e)
        return False
    
