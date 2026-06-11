#!/usr/bin/env -S uv run --script
"""Llama model launcher application."""

import sys

from PySide6.QtWidgets import (
    QApplication,
    QDoubleSpinBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ModelSelector(QWidget):
    """Widget for selecting a GGUF model file via dialog.

    Attributes:
        model_path: Full filesystem path of the selected model file.
    """

    def __init__(self) -> None:
        super().__init__()
        self.model_path = ""
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.addWidget(QLabel("Choose"))
        layout.addStretch()

        self._path_edit = QLineEdit()
        self._path_edit.setReadOnly(True)
        layout.addWidget(self._path_edit)

        select_button = QPushButton("Select Model...")
        select_button.clicked.connect(self._select_file)
        layout.addWidget(select_button)

    def _select_file(self) -> None:
        """Open a file dialog to select a .gguf model file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select GGUF Model",
            "",
            "GGUF Files (*.gguf)",
        )
        if file_path:
            self.model_path = file_path
            self._path_edit.setText(file_path.rsplit("/", 1)[-1])

    @property
    def selected_name(self) -> str:
        """Return the currently displayed model filename."""
        return self._path_edit.text()


class TemperatureConfig(QWidget):
    """Widget for configuring model generation parameters.

    Attributes:
        temperature_spinbox: Controls model temperature.
        top_p_spinbox: Controls nucleus sampling threshold.
        top_k_spinbox: Controls top-k sampling threshold.
    """

    def __init__(self) -> None:
        super().__init__()
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QFormLayout(self)

        self.temperature_spinbox = QDoubleSpinBox()
        self.top_p_spinbox = QDoubleSpinBox()
        self.top_k_spinbox = QDoubleSpinBox()

        layout.addRow("Temp:", self.temperature_spinbox)
        layout.addRow("Top P:", self.top_p_spinbox)
        layout.addRow("Top K:", self.top_k_spinbox)

        self._set_initial_values()

    def _set_initial_values(self) -> None:
        """Set default parameter values."""
        self.temperature_spinbox.setValue(0.3)
        self.top_p_spinbox.setValue(0.9)
        self.top_k_spinbox.setValue(40)


class OutputDisplay(QPlainTextEdit):
    """Read-only text area for displaying model output."""

    def __init__(self, placeholder_text: str = "Model output will appear here...") -> None:
        super().__init__()
        self.setReadOnly(True)
        self.setPlaceholderText(placeholder_text)


class MoreOptions(QWidget):
    """Placeholder widget for additional configuration options."""

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("More Options..."))


class LlamaLaunchApp(QMainWindow):
    """Main application window for the Llama model launcher."""

    WINDOW_TITLE = "Llama Launch"
    WINDOW_GEOMETRY = (100, 100, 800, 600)

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setGeometry(*self.WINDOW_GEOMETRY)
        self._setup_ui()

    def _setup_ui(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        layout.addWidget(self._create_model_group())
        layout.addWidget(self._create_temperature_group())
        layout.addWidget(self._create_more_options_group())
        layout.addWidget(self._create_output_area())
        layout.addWidget(self._create_launch_button())
        layout.addStretch()

    def _create_model_group(self) -> QGroupBox:
        group = QGroupBox("MODEL")
        self._model_selector = ModelSelector()
        group_layout = QVBoxLayout(group)
        group_layout.addWidget(self._model_selector)
        return group

    def _create_temperature_group(self) -> QGroupBox:
        group = QGroupBox("TEMP")
        self._temp_config = TemperatureConfig()
        group_layout = QVBoxLayout(group)
        group_layout.addWidget(self._temp_config)
        return group

    def _create_more_options_group(self) -> QGroupBox:
        group = QGroupBox("More Options")
        group_layout = QVBoxLayout(group)
        group_layout.addWidget(MoreOptions())
        return group

    def _create_output_area(self) -> OutputDisplay:
        output = OutputDisplay()
        self._output_display = output
        return output

    def _create_launch_button(self) -> QPushButton:
        button = QPushButton("LAUNCH")
        button.clicked.connect(self._launch_model)
        return button

    def _launch_model(self) -> None:
        """Launch the model with current configuration settings."""
        model_name = self._model_selector.selected_name
        temperature = self._temp_config.temperature_spinbox.value()
        top_p = self._temp_config.top_p_spinbox.value()
        top_k = self._temp_config.top_k_spinbox.value()

        output = (
            f"Model: {model_name}\n"
            f"Temperature: {temperature}\n"
            f"Top P: {top_p}\n"
            f"Top K: {top_k}\n"
            f"\nModel launched successfully!"
        )

        self._output_display.setPlainText(output)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LlamaLaunchApp()
    window.show()
    sys.exit(app.exec())
