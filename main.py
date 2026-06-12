#!/usr/bin/env -S uv run --script
"""Llama model launcher application."""

import sys
from pathlib import Path
from typing import List

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (
    QApplication,
    QDoubleSpinBox,
    QFileDialog,
    QLineEdit,
    QMainWindow,
    QPlainTextEdit,
    QPushButton,
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

        # Auto-discover interactive widgets by type.
        # For types with a single instance we unpack directly.
        # For types with multiple instances we sort by objectName()
        # so the assignment order is deterministic (alphabetical).
        central = ui_instance.centralwidget
        line_edits: List[QLineEdit] = central.findChildren(QLineEdit)
        push_buttons: List[QPushButton] = sorted(
            central.findChildren(QPushButton), key=lambda w: w.objectName()
        )
        spinboxes: List[QDoubleSpinBox] = sorted(
            central.findChildren(QDoubleSpinBox), key=lambda w: w.objectName()
        )
        plain_text_edits: List[QPlainTextEdit] = central.findChildren(QPlainTextEdit)

        if len(line_edits) != 1:
            raise RuntimeError(f"Expected 1 QLineEdit, found {len(line_edits)}")
        if len(push_buttons) != 2:
            raise RuntimeError(f"Expected 2 QPushButton, found {len(push_buttons)}")
        if len(spinboxes) != 3:
            raise RuntimeError(f"Expected 3 QDoubleSpinBox, found {len(spinboxes)}")
        if len(plain_text_edits) != 1:
            raise RuntimeError(
                f"Expected 1 QPlainTextEdit, found {len(plain_text_edits)}"
            )

        self.model_path_edit = line_edits[0]
        # Alphabetical order: launch_button < select_model_button
        self.launch_button, self.select_model_button = push_buttons
        # Alphabetical order: temperature < top_k < top_p
        self.temperature_spinbox, self.top_k_spinbox, self.top_p_spinbox = spinboxes
        self.output_display = plain_text_edits[0]

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
