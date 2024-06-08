import cv2
from detection import AccidentDetectionModel
import numpy as np
import os
#from twilio.rest import Client
from werkzeug.utils import secure_filename
from flask import Flask, render_template, Response, request, redirect, url_for, make_response

# Twilio account credentials
account_sid = 'ACe3be24cb4996f6abc9271916693a35fa'
auth_token = '4993f6fe8fae7d356882749fd5f288e8'
twilio_phone_number = '+15075007115'
recipient_phone_number = '+918269787561'

# Initialize Twilio client
#client = Client(account_sid, auth_token)

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
sender='pakkisrisaibhaskar.20.csd@anits.edu.in'
receiver='bhaskar.pakki09@gmail.com'
subject = 'accident detected'
message = 'accident detected at cam 001'
password = 'mroctcukcyryiafo'






# Initialize accident detection model and font
model = AccidentDetectionModel(r"C:\Users\Pakki Bhaskar\Downloads\Real_Time_Accident_detection_Alerts\detection\model (3).json", r"C:\Users\Pakki Bhaskar\Downloads\Real_Time_Accident_detection_Alerts\detection\model_weights (3).h5")
font = cv2.FONT_HERSHEY_SIMPLEX

# Initialize Flask app
app = Flask(__name__)

# Define video capture function
def video_stream():
    video = cv2.VideoCapture(r"C:\Users\Pakki Bhaskar\Downloads\Real_Time_Accident_detection_Alerts\detection\static\uploads\temp.mp4")
    while True:
        ret, frame = video.read()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        roi = cv2.resize(gray_frame, (250, 250))

        pred, prob = model.predict_accident(roi[np.newaxis, :, :])
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

        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Define home route
@app.route('/')
def index():
    return render_template('index.html')

# Define route for real-time detection page
@app.route('/real_time_detection')
def real_time_detection():
    return Response(video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Define video feed route
@app.route('/video_detection')
def video_feed():
    return redirect(url_for('real_time_detection'))

# Define image upload route
@app.route('/image_upload', methods=['GET', 'POST'])
def image_upload():
    if request.method == 'POST':
        file = request.files['image']
        img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        roi = cv2.resize(gray_img, (250, 250))

        pred, prob = model.predict_accident(roi[np.newaxis, :, :])
        if pred == "Accident":
            prob = round(prob[0][0]*100, 2)
            result_text = pred + " " + str(prob) + "%"
            result_color = (0, 0, 255)  # red
        else:
            result_text = "No Accident"
            result_color = (0, 255, 0)  # green

        # Draw result on image
        cv2.putText(img, result_text, (20, 30), font, 1, result_color, 2)

        # Save image with detection result
        cv2.imwrite("static/results.jpg", img)

        # Render HTML template with detection result image
        return render_template('results.html', result_image='results.jpg')

    # Render HTML template with image upload form
    return render_template('image_upload.html')

# Define image upload route
@app.route('/vedio_upload', methods=['GET', 'POST'])
def video_upload():
    if request.method == 'POST':
        file = request.files['video']

        print(file)

        file.save(r"C:\Users\Pakki Bhaskar\Downloads\Real_Time_Accident_detection_Alerts\detection\static\uploads\temp.mp4")

        # Render HTML template with detection result image
        #return render_template('index.html')
        return redirect(url_for('real_time_detection'))

    # Render HTML template with image upload form
    return render_template('vedio_upload.html')


if __name__ == '__main__':
    app.run(debug=True)