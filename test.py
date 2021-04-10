
# import cv2
# import sys

# cascPath = sys.argv[1]
# faceCascade = cv2.CascadeClassifier(cascPath)

# video_capture = cv2.VideoCapture(0)

# while True:
#     # Capture frame-by-frame
#     ret, frame = video_capture.read()

#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     faces = faceCascade.detectMultiScale(
#         gray,
#         scaleFactor=1.1,
#         minNeighbors=5,
#         minSize=(30, 30),
#         flags=cv2.CASCADE_SCALE_IMAGE
#     )

#     # Draw a rectangle around the faces
#     for (x, y, w, h) in faces:
#         cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

#     # Display the resulting frame
#     cv2.imshow('Video', frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # When everything is done, release the capture
# video_capture.release()
# cv2.destroyAllWindows()


import cv2
from fer import FER
import matplotlib.pyplot as plt 

video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detector = FER(mtcnn=True)
    # detector = FER()
    emotion, score = detector.top_emotion(frame)
    print("LAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", str(emotion), str(score))
    # print(detector.detect_emotions(frame))
    # cv2.imshow("frame", frame)

    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()

# img = plt.imread("happy.jpg")