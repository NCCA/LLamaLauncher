import json
import sys

import requests
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QGroupBox, QHBoxLayout, QMainWindow, QPlainTextEdit, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LLamaLauncher GUI")
        self.setGeometry(100, 100, 800, 600)

        # Create central widget and set layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a main vertical layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Create a group box for input
        input_group = QGroupBox("Input")
        input_layout = QVBoxLayout()
        input_group.setLayout(input_layout)

        # Add a text edit for input
        self.input_edit = QPlainTextEdit()
        input_layout.addWidget(self.input_edit)

        # Add the group box to main layout
        main_layout.addWidget(input_group)

        # Create a group box for output
        output_group = QGroupBox("Output")
        output_layout = QVBoxLayout()
        output_group.setLayout(output_layout)

        # Add a text edit for output
        self.output_edit = QPlainTextEdit()
        output_layout.addWidget(self.output_edit)

        # Add the group box to main layout
        main_layout.addWidget(output_group)

        # Create a button to trigger action
        self.action_button = QPushButton("Action")
        self.action_button.clicked.connect(self.on_action)

        # Create a horizontal layout for the button
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.action_button)

        # Add button layout to main layout
        main_layout.addLayout(button_layout)

        # Add a separator
        main_layout.addStretch()

        # Set output text to read-only
        self.output_edit.setReadOnly(True)

    def on_action(self):
        # Get input text
        input_text = self.input_edit.toPlainText()

        # Simple example: append some text to the output
        output_text = "Hello from LLamaLauncher!\n"
        self.output_edit.appendPlainText(output_text)

        # Simulate LLM interaction
        self.handle_llm_interaction(input_text)

    def handle_llm_interaction(self, input_text):
        # This is a placeholder for actual LLM interaction
        # For now, we'll simulate a response
        if input_text == "":
            return

        # Simulate API call
        try:
            # For demonstration, we'll use a placeholder API endpoint
            # In a real application, you'd replace this with your actual LLM API
            response = requests.post("http://localhost:8000/api/v1/generate", data=json.dumps({"prompt": input_text}))
            if response.status_code == 200:
                result = response.json()
                # Append the result to output
                self.output_edit.appendPlainText(f"LLM Response: {result.get('response', '')}\n")
            else:
                self.output_edit.appendPlainText(f"Error: {response.status_code} - {response.text}\n")
        except Exception as e:
            self.output_edit.appendPlainText(f"Error: {str(e)}\n")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
