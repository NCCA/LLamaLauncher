#!/usr/bin/env -S uv run --script
"""Llama model launcher application."""

import sys
from pathlib import Path

from PySide6.QtCore import QObject
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
)


class LlamaLaunchApp(QMainWindow):
    """Main application window for the Llama model launcher.

    Loads its UI from a .ui file via QUiLoader and wires up all
    signals and slots to preserve existing behaviour.
    """

    def __init__(self) -> None:
        super().__init__()
        self._setup_ui()
        self._connect_signals()

    # ------------------------------------------------------------------
    # UI loading
    # ------------------------------------------------------------------

    def _setup_ui(self) -> None:
        """Load the main window UI from the .ui file."""
        loader = QUiLoader()
        ui_path = Path(__file__).resolve().parent / "ui" / "llama_launch.ui"
        ui_instance = loader.load(ui_path)

        self.setCentralWidget(ui_instance.centralwidget)

        # Store references to every interactive widget by the names used
        # in the .ui file so that other methods can access them.
        central = ui_instance.centralwidget
        self.model_path_edit = central.findChild(QObject, "model_path_edit")
        self.select_model_button = central.findChild(QObject, "select_model_button")
        self.temperature_spinbox = central.findChild(QObject, "temperature_spinbox")
        self.top_p_spinbox = central.findChild(QObject, "top_p_spinbox")
        self.top_k_spinbox = central.findChild(QObject, "top_k_spinbox")
        self.output_display = central.findChild(QObject, "output_display")
        self.launch_button = central.findChild(QObject, "launch_button")

    # ------------------------------------------------------------------
    # Signal connections
    # ------------------------------------------------------------------

    def _connect_signals(self) -> None:
        """Connect widget signals to their slot methods."""
        self.select_model_button.clicked.connect(self._select_model)
        self.launch_button.clicked.connect(self._launch_model)

    # ------------------------------------------------------------------
    # Slots
    # ------------------------------------------------------------------

    def _select_model(self) -> None:
        """Open a file dialog to select a .gguf model file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select GGUF Model",
            "",
            "GGUF Files (*.gguf)",
        )
        if file_path:
            self._model_path = file_path
            self.model_path_edit.setText(file_path.rsplit("/", 1)[-1])

    def _launch_model(self) -> None:
        """Launch the model with current configuration settings."""
        model_name = self.model_path_edit.text()
        temperature = self.temperature_spinbox.value()
        top_p = self.top_p_spinbox.value()
        top_k = self.top_k_spinbox.value()

        output = (
            f"Model: {model_name}\n"
            f"Temperature: {temperature}\n"
            f"Top P: {top_p}\n"
            f"Top K: {top_k}\n"
            f"\nModel launched successfully!"
        )

        self.output_display.setPlainText(output)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LlamaLaunchApp()
    window.show()
    sys.exit(app.exec())
