import cv2
from detection import AccidentDetectionModel
import numpy as np
import os
#from twilio.rest import Client
from werkzeug.utils import secure_filename
from flask import Flask, render_template, Response, request, redirect, url_for, make_response

import time 
import smtplib
from email.mime.text import MIMEText


def send_email(subject, message, sender_email, receiver_email, password):
    # Create a plain text message
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send the email via Gmail's SMTP server, or use another server as needed
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
sender = 'pakkisrisaibhaskar.20.csd@anits.edu.in'
receiver = 'bhaskar.pakki09@gmail.com'
subject = 'accident detected'
message = 'accident detected at cam 001'
password = 'mroctcukcyryiafo'


# Twilio account credentials
account_sid = 'ACe3be24cb4996f6abc9271916693a35fa'
auth_token = '4993f6fe8fae7d356882749fd5f288e8'
twilio_phone_number = '+15075007115'
recipient_phone_number = '+918269787561'

model = AccidentDetectionModel(r"C:\Users\Pakki Bhaskar\Downloads\Real_Time_Accident_detection_Alerts\detection\model (3).json", r"C:\Users\Pakki Bhaskar\Downloads\Real_Time_Accident_detection_Alerts\detection\model_weights (3).h5")
font = cv2.FONT_HERSHEY_SIMPLEX


# import cv2 
# video = cv2.VideoCapture(0)
# while True:
#     ret, frame = video.read()
#     # gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     # roi = cv2.resize(gray_frame, (250, 250))

#     # pred, prob = model.predict_accident(roi[np.newaxis, :, :])
#     # if pred == "Accident":
#     #     prob = round(prob[0][0]*100, 2)
#     #     if prob > 97:
#     #         # message = client.messages.create(
#     #         #     body="An accident has been detected at the Medi-Caps University location: Google map link :- https://goo.gl/maps/MBc96nsoWdw41mMa9. with probability " + str(prob) + "%",
#     #         #     from_=twilio_phone_number,
#     #         #     to=recipient_phone_number
#     #         # )
#     #         import winsound

#     #         # Set the frequency (in Hertz) and duration (in milliseconds)
#     #         frequency = 2500
#     #         duration = 1000  # 1 second

#     #         # Make the computer beep
#     #         winsound.Beep(frequency, duration)

#     #         print("accident")


#     #         try:
#     #             send_email(subject, message, sender, receiver,password)
#     #             time.sleep(1)
#     #         except Exception as exp:
#     #             print("oops ", exp)
#     #             pass 


#     #     cv2.rectangle(frame, (0, 0), (280, 40), (0, 0, 0), -1)
#     #     cv2.putText(frame, pred+" "+str(prob), (20, 30), font, 1, (255, 255, 0), 2)
#     # else:
#     #     cv2.rectangle(frame, (0, 0), (280, 40), (0, 0, 0), -1)
#     #     cv2.putText(frame, "No Accident", (20, 30), font, 1, (255, 255, 0), 2)

#     # ret, jpeg = cv2.imencode('.jpg', frame)
#     # frame = jpeg.tobytes()

#     cv2.imshow('frame', frame)


import cv2

video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    roi = cv2.resize(gray_frame, (250, 250))
    pred, prob = model.predict_accident(roi[np.newaxis, :, :])
    print(pred)

    if pred == "Accident":
        prob = round(prob[0][0]*100, 2)
        if prob > 97:
            # message = client.messages.create(
            #     body="An accident has been detected at the Medi-Caps University location: Google map link :- https://goo.gl/maps/MBc96nsoWdw41mMa9. with probability " + str(prob) + "%",
            #     from_=twilio_phone_number,
            #     to=recipient_phone_number
            # )
            import winsound

            # Set the frequency (in Hertz) and duration (in milliseconds)
            frequency = 2500
            duration = 1000  # 1 second

            # Make the computer beep
            winsound.Beep(frequency, duration)

            print("accident")


            try:
                send_email(subject, message, sender, receiver,password)
                time.sleep(1)
            except Exception as exp:
                print("oops ", exp)
                pass 


        cv2.rectangle(frame, (0, 0), (280, 40), (0, 0, 0), -1)
        cv2.putText(frame, pred+" "+str(prob), (20, 30), font, 1, (255, 255, 0), 2)
    else:
        cv2.rectangle(frame, (0, 0), (280, 40), (0, 0, 0), -1)
        cv2.putText(frame, "No Accident", (20, 30), font, 1, (255, 255, 0), 2)


    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
