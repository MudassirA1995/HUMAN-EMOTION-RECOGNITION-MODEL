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


