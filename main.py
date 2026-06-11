#!/usr/bin/env -S uv run --script

import sys

from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class LlamaLaunchApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Llama Launch")
        self.setGeometry(100, 100, 800, 600)

        # Create central widget and set layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Create model selection group
        model_group = QGroupBox("MODEL")
        model_layout = QVBoxLayout()

        # Model choice combo box
        self.model_combo = QComboBox()
        self.model_combo.addItem("Llama 3 8B")
        self.model_combo.addItem("Llama 3 70B")
        self.model_combo.addItem("Llama 2 7B")
        self.model_combo.addItem("Llama 2 13B")
        self.model_combo.addItem("Llama 2 70B")

        # Add model choice to layout
        model_layout.addWidget(QLabel("Choose"))
        model_layout.addWidget(self.model_combo)

        model_group.setLayout(model_layout)

        # Create temperature group
        temp_group = QGroupBox("TEMP")
        temp_layout = QFormLayout()
        temp_layout.addRow("Temp:", QDoubleSpinBox())
        temp_layout.addRow("Top P:", QDoubleSpinBox())
        temp_layout.addRow("Top K:", QDoubleSpinBox())

        # Set initial values
        temp_layout.itemAt(0).widget().setText("0.3")
        temp_layout.itemAt(1).widget().setValue(0.9)
        temp_layout.itemAt(2).widget().setText("40")

        temp_group.setLayout(temp_layout)

        # Create more options group
        more_group = QGroupBox("More Options")
        more_layout = QVBoxLayout()
        more_layout.addWidget(QLabel("More Options..."))
        more_group.setLayout(more_layout)

        # Create launch button
        launch_button = QPushButton("LAUNCH")
        launch_button.clicked.connect(self.launch_model)

        # Create output area
        self.output_edit = QPlainTextEdit()
        self.output_edit.setReadOnly(True)
        self.output_edit.setPlaceholderText("Model output will appear here...")

        # Add widgets to main layout
        main_layout.addWidget(model_group)
        main_layout.addWidget(temp_group)
        main_layout.addWidget(more_group)
        main_layout.addWidget(self.output_edit)
        main_layout.addWidget(launch_button)

        # Add some spacing
        main_layout.addStretch()

        # Set window title
        self.setWindowTitle("Llama Launch")

    def launch_model(self):
        # Get current values
        model = self.model_combo.currentText()
        temp = self.temp_layout.itemAt(0).widget().value()
        top_p = self.temp_layout.itemAt(1).widget().value()
        top_k = self.temp_layout.itemAt(2).widget().value()

        # Simulate model launch
        output = f"Model: {model}\nTemperature: {temp}\nTop P: {top_p}\nTop K: {top_k}\n\nModel launched successfully!"

        # Update output text
        self.output_edit.setPlainText(output)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LlamaLaunchApp()
    window.show()
    sys.exit(app.exec())
