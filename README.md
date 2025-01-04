# Human Emotion Recognition 

## Introduction 


The Emotion Recognition App is an innovative application designed to detect and analyze human emotions in real-time using a live video feed. Built with Python and leveraging powerful libraries such as OpenCV, FER (Facial Emotion Recognition), and PyQt5, this application provides a user-friendly interface for capturing video, processing it to detect emotions, and displaying the results. The app is particularly useful in various domains, including psychology, marketing, and human-computer interaction, where understanding emotional states can provide valuable insights.

## Use Cases

Psychology and Mental Health: Therapists and researchers can use the app to monitor patients' emotional states during therapy sessions or experiments, providing real-time feedback and insights.

Marketing and Advertising: Marketers can analyze viewers' emotional responses to advertisements, helping to tailor content that resonates more effectively with the target audience.

Human-Computer Interaction: Developers can integrate emotion recognition into interactive applications, such as games or virtual assistants, to create more intuitive and responsive user experiences.

Education and Training: Educators can use the app to gauge students' emotional engagement during lectures or training sessions, allowing for more personalized and effective teaching methods.

## Libraries Used

OpenCV: A widely-used computer vision library that provides tools for video capture, image processing, and real-time analysis.

FER (Facial Emotion Recognition): A library specifically designed for detecting emotions from facial expressions. It uses deep learning models to analyze images and classify emotions.

PyQt5: A set of Python bindings for Qt libraries, which are used to create the graphical user interface (GUI) of the application. PyQt5 provides a comprehensive set of tools for building cross-platform applications with a native look and feel.

## Prerequisites

To use the Emotion Recognition App, users need to have the following prerequisites:

Python Environment: Ensure that Python is installed on your system. The application is compatible with Python 3.x.

Required Libraries: Install the necessary libraries using pip. You can install them by running the following commands:

pip install opencv-python
pip install fer
pip install PyQt5

Camera Access: The application requires access to a webcam or any video capture device. Ensure that your system has a functional camera and that it is properly configured.

Operating System: The application is designed to run on Windows, macOS, and Linux. Ensure that your operating system is up-to-date and supports the required libraries.

By meeting these prerequisites, users can easily set up and run the Emotion Recognition App, leveraging its powerful features to detect and analyze emotions in real-time. Whether you are a researcher, marketer, developer, or educator, this application offers a versatile tool for understanding and responding to human emotions.

## Code Explanation 

```python

import cv2
from fer import FER
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer


class EmotionRecognitionApp(QWidget):
    def __init__(self):
        super().__init__()

        # Setup the UI
        self.setWindowTitle("Emotion Recognition")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Video feed
        self.video_label = QLabel(self)
        self.layout.addWidget(self.video_label)

        # Detected emotion
        self.emotion_label = QLabel("Emotion: Detecting...", self)
        self.emotion_label.setStyleSheet("font-size: 20px; color: blue;")
        self.layout.addWidget(self.emotion_label)

        # Start/Stop button
        self.control_button = QPushButton("Start Camera", self)
        self.control_button.clicked.connect(self.toggle_camera)
        self.layout.addWidget(self.control_button)

        # Initialize camera and timer
        self.capture = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.detect_emotion)

        # Initialize FER detector
        self.detector = FER(mtcnn=True)

    def toggle_camera(self):
        if self.capture is None:
            self.capture = cv2.VideoCapture(0)
            self.timer.start(30)
            self.control_button.setText("Stop Camera")
        else:
            self.timer.stop()
            self.capture.release()
            self.capture = None
            self.video_label.clear()
            self.control_button.setText("Start Camera")

    def detect_emotion(self):
        ret, frame = self.capture.read()
        if not ret:
            return

        # Flip the frame horizontally for a mirror-like effect
        frame = cv2.flip(frame, 1)

        # Detect emotions
        results = self.detector.detect_emotions(frame)
        if results:
            emotion = max(results[0]["emotions"], key=results[0]["emotions"].get)
            self.emotion_label.setText(f"Emotion: {emotion}")

        # Convert frame to QImage for PyQt5 display
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        qt_image = QImage(rgb_frame.data, rgb_frame.shape[1], rgb_frame.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        self.video_label.setPixmap(pixmap)

    def closeEvent(self, event):
        if self.capture is not None:
            self.capture.release()
        event.accept()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = EmotionRecognitionApp()
    window.show()
    sys.exit(app.exec_())


```

### Code Snippet Explanation 


python ```

import cv2
from fer import FER
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer

```

import cv2: Imports the OpenCV library, which is used for video capture and image processing.

from fer import FER: Imports the FER (Facial Emotion Recognition) library, which is used to detect emotions from facial expressions.

from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QPushButton, QWidget: Imports various widgets from the PyQt5 library to create the graphical user interface (GUI).

from PyQt5.QtGui import QImage, QPixmap: Imports classes from PyQt5 for handling images and displaying them in the GUI.

from PyQt5.QtCore import QTimer: Imports the QTimer class from PyQt5, which is used to create a timer for periodic tasks.

python ```

class EmotionRecognitionApp(QWidget):
    def __init__(self):
        super().__init__()

```

class EmotionRecognitionApp(QWidget):: Defines a new class EmotionRecognitionApp that inherits from QWidget, making it a PyQt5 widget.

def __init__(self):: Defines the constructor method for the EmotionRecognitionApp class.

super().__init__(): Calls the constructor of the parent class QWidget to initialize the widget.

        # Setup the UI
        self.setWindowTitle("Emotion Recognition")
        self.setGeometry(100, 100, 800, 600)

self.setWindowTitle("Emotion Recognition"): Sets the title of the application window to "Emotion Recognition".

self.setGeometry(100, 100, 800, 600): Sets the position and size of the application window. The window will be positioned at (100, 100) on the screen and will have a size of 800x600 pixels.

        # Main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

self.layout = QVBoxLayout(): Creates a vertical box layout for organizing the widgets in the application.

self.setLayout(self.layout): Sets the created layout as the main layout for the application window.

        # Video feed
        self.video_label = QLabel(self)
        self.layout.addWidget(self.video_label)

self.video_label = QLabel(self): Creates a QLabel widget to display the video feed.

self.layout.addWidget(self.video_label): Adds the video label to the main layout.

        # Detected emotion
        self.emotion_label = QLabel("Emotion: Detecting...", self)
        self.emotion_label.setStyleSheet("font-size: 20px; color: blue;")
        self.layout.addWidget(self.emotion_label)

self.emotion_label = QLabel("Emotion: Detecting...", self): Creates a QLabel widget to display the detected emotion. Initially, it shows "Emotion: Detecting...".

self.emotion_label.setStyleSheet("font-size: 20px; color: blue;"): Sets the style of the emotion label, including font size and color.

self.layout.addWidget(self.emotion_label): Adds the emotion label to the main layout.

        # Start/Stop button
        self.control_button = QPushButton("Start Camera", self)
        self.control_button.clicked.connect(self.toggle_camera)
        self.layout.addWidget(self.control_button)

self.control_button = QPushButton("Start Camera", self): Creates a QPushButton widget with the text "Start Camera".

self.control_button.clicked.connect(self.toggle_camera): Connects the button's click event to the toggle_camera method, which will be called when the button is clicked.

self.layout.addWidget(self.control_button): Adds the control button to the main layout.

        # Initialize camera and timer
        self.capture = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.detect_emotion)

self.capture = None: Initializes the camera capture object to None.

self.timer = QTimer(self): Creates a QTimer object for periodic tasks.

self.timer.timeout.connect(self.detect_emotion): Connects the timer's timeout event to the detect_emotion method, which will be called periodically.

        # Initialize FER detector
        self.detector = FER(mtcnn=True)

self.detector = FER(mtcnn=True): Initializes the FER detector with the MTCNN face detector enabled.

    def toggle_camera(self):
        if self.capture is None:
            self.capture = cv2.VideoCapture(0)
            self.timer.start(30)
            self.control_button.setText("Stop Camera")
        else:
            self.timer.stop()
            self.capture.release()
            self.capture = None
            self.video_label.clear()
            self.control_button.setText("Start Camera")

def toggle_camera(self):: Defines the toggle_camera method, which toggles the camera on and off.

if self.capture is None:: Checks if the camera capture object is None, indicating that the camera is not currently running.

self.capture = cv2.VideoCapture(0): Initializes the camera capture object using the default camera (index 0).

self.timer.start(30): Starts the timer with a 30-millisecond interval.

self.control_button.setText("Stop Camera"): Changes the text of the control button to "Stop Camera".

else:: If the camera is already running.

self.timer.stop(): Stops the timer.

self.capture.release(): Releases the camera capture object.

self.capture = None: Sets the camera capture object to None.

self.video_label.clear(): Clears the video label.

self.control_button.setText("Start Camera"): Changes the text of the control button to "Start Camera".

    def detect_emotion(self):
        ret, frame = self.capture.read()
        if not ret:
            return

def detect_emotion(self):: Defines the detect_emotion method, which detects emotions from the video feed.

ret, frame = self.capture.read(): Reads a frame from the camera capture object.

if not ret:: Checks if the frame was not successfully read.

return: Returns from the method if the frame was not successfully read.

        # Flip the frame horizontally for a mirror-like effect
        frame = cv2.flip(frame, 1)

frame = cv2.flip(frame, 1): Flips the frame horizontally to create a mirror-like effect.

        # Detect emotions
        results = self.detector.detect_emotions(frame)
        if results:
            emotion = max(results[0]["emotions"], key=results[0]["emotions"].get)
            self.emotion_label.setText(f"Emotion: {emotion}")

results = self.detector.detect_emotions(frame): Detects emotions in the frame using the FER detector.

if results:: Checks if emotions were successfully detected.

emotion = max(results[0]["emotions"], key=results[0]["emotions"].get): Finds the emotion with the highest confidence score.

self.emotion_label.setText(f"Emotion: {emotion}"): Updates the emotion label with the detected emotion.

        # Convert frame to QImage for PyQt5 display
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        qt_image = QImage(rgb_frame.data, rgb_frame.shape[1], rgb_frame.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        self.video_label.setPixmap(pixmap)

rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB): Converts the frame from BGR to RGB color format.

qt_image = QImage(rgb_frame.data, rgb_frame.shape[1], rgb_frame.shape[0], QImage.Format_RGB888): Creates a QImage object from the RGB frame.

pixmap = QPixmap.fromImage(qt_image): Creates a QPixmap object from the QImage.

self.video_label.setPixmap(pixmap): Sets the pixmap on the video label to display the frame.

    def closeEvent(self, event):
        if self.capture is not None:
            self.capture.release()
        event.accept()

def closeEvent(self, event):: Defines the closeEvent method, which handles the close event of the application window.

if self.capture is not None:: Checks if the camera capture object is not None.

self.capture.release(): Releases the camera capture object.

event.accept(): Accepts the close event, allowing the window to close.

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = EmotionRecognitionApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":: Checks if the script is being run directly (not imported as a module).

import sys: Imports the sys module.

app = QApplication(sys.argv): Creates a QApplication object, which manages the application's control flow and main settings.

window = EmotionRecognitionApp(): Creates an instance of the EmotionRecognitionApp class.

window.show(): Shows the application window.

sys.exit(app.exec_()): Starts the application's event loop and exits when the loop ends.


## Application View 


![App Screen Shot](https://github.com/user-attachments/assets/848e1836-f4b2-41f7-992a-e18266e69a48)











