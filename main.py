#!/usr/bin/env -S uv run --script
"""Llama model launcher application."""

import sys
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
)

from ui_loader import load_ui


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
        """Load the main window UI from the .ui file.

        All child widgets and layouts are auto-assigned as attributes
        on this instance by their ``objectName`` so that the .ui file
        controls which names are available.
        """
        ui_path = Path(__file__).resolve().parent / "ui" / "llama_launch.ui"
        load_ui(ui_path, self)

    # ------------------------------------------------------------------
    # Signal connections
    # ------------------------------------------------------------------

    def _connect_signals(self) -> None:
        """Connect widget signals to their slot methods."""
        self.select_model_button.clicked.connect(self._select_model)
        self.select_mmproj_button.clicked.connect(self._select_mmproj)
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

    def _select_mmproj(self) -> None:
        """Open a file dialog to select a .gguf mmproj file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Multi-Modal Projector",
            "",
            "GGUF Files (*.gguf)",
        )
        if file_path:
            self._mmproj_path = file_path
            self.mmproj_path_edit.setText(file_path.rsplit("/", 1)[-1])

    def _launch_model(self) -> None:
        """Launch the model with current configuration settings."""
        model_name = self.model_path_edit.text()
        temperature = self.temperature_spinbox.value()
        top_p = self.top_p_spinbox.value()
        top_k = self.top_k_spinbox.value()

        mmproj_name = self.mmproj_path_edit.text()
        no_mmproj_offload = self.no_mmproj_offload_checkbox.isChecked()

        flags = []
        if mmproj_name:
            flags.append(f"--mmproj {mmproj_name}")
            if no_mmproj_offload:
                flags.append("--no-mmproj-offload")

        flag_str = " ".join(flags)
        output = f"Model: {model_name}\nTemperature: {temperature}\nTop P: {top_p}\nTop K: {top_k}\n"
        if flag_str:
            output += f"\nFlags: {flag_str}\n"
        output += "\nModel launched successfully!"

        self.output_display.setPlainText(output)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LlamaLaunchApp()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())
