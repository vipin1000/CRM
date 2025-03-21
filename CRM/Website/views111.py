import cv2             #type: ignore
import face_recognition #type: ignore
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse
import os
import numpy as np #type: ignore
from .forms import SignUpForm

REGISTERED_FACES_DIR = "registered_faces"  # Directory to save registered face images

# Ensure the directory exists
if not os.path.exists(REGISTERED_FACES_DIR):
    os.makedirs(REGISTERED_FACES_DIR)

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            
            # Initialize the webcam
            video_capture = cv2.VideoCapture(0)

            # Capture the face image
            ret, frame = video_capture.read()
            if ret:
                # Convert the image to RGB
                image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(image_rgb)
                face_encodings = face_recognition.face_encodings(image_rgb, face_locations)

                if len(face_encodings) > 0:
                    face_encoding = face_encodings[0]
                    face_image_path = os.path.join(REGISTERED_FACES_DIR, f"{username}.jpg")
                    cv2.imwrite(face_image_path, frame)

                    # Store the face encoding and username in the database
                    # You can save the encoding in the model (perhaps with a JSONField or a BinaryField)
                    # For simplicity, you can also store it as a file or in a database directly
                    messages.success(request, "You are Registered and Face is Captured!")
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, "No face detected! Please try again.")
            else:
                messages.error(request, "Failed to capture the face.")
            
            video_capture.release()

    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Initialize webcam
            video_capture = cv2.VideoCapture(0)
            
            # Capture the face image
            ret, frame = video_capture.read()
            if ret:
                image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(image_rgb)
                face_encodings = face_recognition.face_encodings(image_rgb, face_locations)

                if len(face_encodings) > 0:
                    captured_face_encoding = face_encodings[0]
                    
                    # Load the stored face encoding for this user
                    registered_face_image_path = os.path.join(REGISTERED_FACES_DIR, f"{username}.jpg")
                    
                    if os.path.exists(registered_face_image_path):
                        registered_face_image = face_recognition.load_image_file(registered_face_image_path)
                        registered_face_encoding = face_recognition.face_encodings(registered_face_image)[0]

                        # Compare the captured face with the stored face
                        matches = face_recognition.compare_faces([registered_face_encoding], captured_face_encoding)
                        
                        if True in matches:
                            login(request, user)
                            messages.success(request, f"Welcome {username}, you are logged in!")
                            return redirect('home')
                        else:
                            messages.error(request, "Face mismatch, try again.")
                    else:
                        messages.error(request, "No registered face found for this user.")
                else:
                    messages.error(request, "No face detected during login.")
            else:
                messages.error(request, "Failed to capture face.")

            video_capture.release()

        else:
            messages.error(request, "Invalid credentials.")

    return render(request, 'login.html')




# <video id="webcam" width="320" height="240" autoplay></video>
# <button id="capture">Capture Face</button>

# <script>
#     const video = document.getElementById('webcam');

#     // Request access to the webcam
#     navigator.mediaDevices.getUserMedia({ video: true })
#         .then(stream => {
#             video.srcObject = stream;
#         })
#         .catch(err => {
#             console.log("Error accessing webcam: ", err);
#         });

#     document.getElementById('capture').addEventListener('click', function() {
#         // Capture the image from the video feed
#         const canvas = document.createElement('canvas');
#         canvas.width = video.videoWidth;
#         canvas.height = video.videoHeight;
#         const ctx = canvas.getContext('2d');
#         ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
#         const dataUrl = canvas.toDataURL();

#         // Send the captured image to the server (using AJAX or form submission)
#         // You can use this data URL to save the image on the server
#         console.log(dataUrl);
#     });
# </script>
