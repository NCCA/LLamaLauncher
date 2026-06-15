#!/usr/bin/env -S uv run --script
"""Llama model launcher application."""

import argparse
import re
import sys
from pathlib import Path

from PySide6.QtCore import QCoreApplication, QProcess, Qt, QTimer, QUrl
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile
from PySide6.QtWebEngineWidgets import QWebEngineView  # noqa: F401
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

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 8080,
        ctx_size: int | None = None,
    ) -> None:
        super().__init__()
        self._process = QProcess(self)
        self._process.readyReadStandardOutput.connect(self._on_stdout)
        self._process.readyReadStandardError.connect(self._on_stderr)
        self._process.finished.connect(self._on_finished)
        self._process.errorOccurred.connect(self._on_error)
        self._host = host
        self._port = port
        self._server_url: str = f"http://{host}:{port}"
        self._auto_refresh_done: bool = False
        self._cache_dir: Path = self._create_cache_dir()
        self._profile: QWebEngineProfile = self._create_persistent_profile()
        self._ctx_size: int | None = ctx_size
        self._setup_ui()
        self._connect_signals()
        self._init_web_view()

    # ------------------------------------------------------------------
    # UI loading and initialization
    # ------------------------------------------------------------------

    def _create_cache_dir(self) -> Path:
        """Create and return a cache directory for persistent web storage.

        Returns:
            Path to the cache directory (created if it does not exist).
        """
        cache_dir = Path(QCoreApplication.applicationDirPath()) / ".cache" / "llama-launcher"
        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir

    def _create_persistent_profile(self) -> QWebEngineProfile:
        """Create a QWebEngineProfile with disk-backed persistent storage.

        This ensures localStorage, sessionStorage, cookies, and IndexedDB
        survive across application restarts so the chat UI remembers
        API keys and conversation history.

        Returns:
            Configured QWebEngineProfile instance.
        """
        profile = QWebEngineProfile("llama-launcher-profile", self)

        # Persist localStorage, sessionStorage, and IndexedDB to disk
        profile.setPersistentStoragePath(str(self._cache_dir))

        # Persist cookies to disk (not session-only)
        profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies)

        # Enable disk HTTP cache for faster page loads
        cache_subdir = self._cache_dir / "cache"
        cache_subdir.mkdir(parents=True, exist_ok=True)
        profile.setHttpCacheType(QWebEngineProfile.DiskHttpCache)
        profile.setHttpCacheMaximumSize(100 * 1024 * 1024)  # 100 MB

        return profile

    def _init_web_view(self) -> None:
        """Initialize the QWebEngineView in the Server tab.

        Creates a QWebEnginePage with the persistent profile so that
        localStorage, cookies, and IndexedDB are restored from disk.
        """
        page = QWebEnginePage(self._profile, self.server_web_view)
        self.server_web_view.setPage(page)
        url = f"http://{self._host}:{self._port}"
        self.server_web_view.setUrl(url)

    def _setup_ui(self) -> None:
        """Load the main window UI from the .ui file.

        All child widgets and layouts are auto-assigned as attributes
        on this instance by their ``objectName`` so that the .ui file
        controls which names are available.
        """
        ui_path = Path(__file__).resolve().parent / "ui" / "llama_launch.ui"
        load_ui(ui_path, self)
        self._setup_context_size_combo()

    def _setup_context_size_combo(self) -> None:
        """Populate the model context size combobox with options and tooltips.

        Each item stores its numeric value (used as ``--ctx-size``) in the
        user data role so the launch method can retrieve it later.
        """
        self.model_context_size.clear()

        context_options = [
            ("Auto (model default)", 0, "Recommended default; uses GGUF model context"),
            ("2K", 2048, "Very small models / low memory"),
            ("4K", 4096, "Basic chat, small coding tasks"),
            ("8K", 8192, "General purpose"),
            ("16K", 16384, "Better coding/chat history"),
            ("32K", 32768, "Large files, coding assistants"),
            ("64K", 65536, "Long documents, repo context"),
            ("128K", 131072, "Modern long-context models"),
        ]

        for display_name, value, tooltip in context_options:
            self.model_context_size.addItem(display_name, value)
            index = self.model_context_size.count() - 1
            self.model_context_size.setItemData(index, tooltip, Qt.ToolTipRole)

        # Pre-select from CLI if provided, otherwise default to 16K
        if self._ctx_size is not None:
            target = self._ctx_size
        else:
            target = 16384  # 16K default

        for i in range(self.model_context_size.count()):
            if int(self.model_context_size.itemData(i, Qt.UserRole)) == target:
                self.model_context_size.setCurrentIndex(i)
                break

    # ------------------------------------------------------------------
    # Signal connections
    # ------------------------------------------------------------------

    def _connect_signals(self) -> None:
        """Connect widget signals to their slot methods."""
        self.select_model_button.clicked.connect(self._select_model)
        self.select_mmproj_button.clicked.connect(self._select_mmproj)
        self.model_path_edit.textChanged.connect(self._on_model_selection_changed)
        self.launch_button.clicked.connect(self._toggle_launch)

    # ------------------------------------------------------------------
    # Slots
    # ------------------------------------------------------------------

    def _select_model(self) -> None:
        """Open a file dialog to select a .gguf model file.

        Stores the full path as a custom property on the line edit
        (accessible via ``getProperty("fullPath")``) while displaying
        only the short filename in the UI.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select GGUF Model",
            "",
            "GGUF Files (*.gguf)",
        )
        if file_path:
            self._model_path = file_path
            self.model_path_edit.setProperty("fullPath", file_path)
            self.model_path_edit.setText(file_path.rsplit("/", 1)[-1])
            self._on_model_selection_changed()

    def _select_mmproj(self) -> None:
        """Open a file dialog to select a .gguf mmproj file.

        Stores the full path as a custom property on the line edit
        (accessible via ``getProperty("fullPath")``) while displaying
        only the short filename in the UI.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Multi-Modal Projector",
            "",
            "GGUF Files (*.gguf)",
        )
        if file_path:
            self._mmproj_path = file_path
            self.mmproj_path_edit.setProperty("fullPath", file_path)
            self.mmproj_path_edit.setText(file_path.rsplit("/", 1)[-1])

    def _on_model_selection_changed(self) -> None:
        """Enable launch button when a model is selected, disable otherwise."""
        has_model = bool(self.model_path_edit.property("fullPath"))
        is_running = self._process.state() == QProcess.Running
        self.launch_button.setEnabled(has_model and not is_running)

    def _toggle_launch(self) -> None:
        """Launch or stop the llama-server based on current process state."""
        if self._process.state() == QProcess.Running:
            self._stop_model()
        else:
            self._launch_model()

    def _stop_model(self) -> None:
        """Stop the llama-server gracefully.

        Sends SIGTERM (like pressing Ctrl+C) so the server can shut down
        cleanly. If it does not stop within 2 seconds, falls back to
        SIGKILL.
        """
        self._process.terminate()
        self.output_display.appendPlainText("Stopping server... (sent SIGTERM)")
        QTimer.singleShot(2000, self._force_kill_if_needed)

    def _force_kill_if_needed(self) -> None:
        """Force kill the process if graceful termination did not work."""
        if self._process.state() == QProcess.Running:
            self.output_display.appendPlainText("Server didn't stop gracefully. Force killing...")
            self._process.kill()

    def _reset_launch_button(self) -> None:
        """Reset the launch button to its default state."""
        self.launch_button.setText("LAUNCH")
        self._on_model_selection_changed()

    def _launch_model(self) -> None:
        """Launch the llama-server binary with current configuration.

        Builds the command-line arguments from the UI fields and starts
        ``llama-server`` via QProcess.  Live stdout/stderr output is
        streamed into ``output_display``.
        """
        model_path = self.model_path_edit.property("fullPath")
        if not model_path:
            self.output_display.appendPlainText("Error: no model selected.")
            return

        temperature = self.temperature_spinbox.value()
        top_p = self.top_p_spinbox.value()
        top_k = self.top_k_spinbox.value()

        mmproj_path = self.mmproj_path_edit.property("fullPath")
        no_mmproj_offload = self.no_mmproj_offload_checkbox.isChecked()
        api_key = self.api_key_line_edit.text() if self.api_key_line_edit.text() else "12345"

        # Build command: llama-server --model ... (conditional sampling params) ...
        cmd = [
            "llama-server",
            "--model",
            model_path,
            "--api-key",
            api_key,
        ]

        if self.enable_temperature_checkbox.isChecked():
            cmd.extend(["--temp", str(temperature)])
        if self.enable_top_p_checkbox.isChecked():
            cmd.extend(["--top-p", str(top_p)])
        if self.enable_top_k_checkbox.isChecked():
            cmd.extend(["--top-k", str(top_k)])

        host = self.host_line_edit.text() or self._host
        port_str = self.port_line_edit.text() or str(self._port)
        try:
            port = int(port_str)
        except ValueError:
            port = self._port

        if mmproj_path:
            cmd.extend(["--mmproj", mmproj_path])
            if no_mmproj_offload:
                cmd.append("--no-mmproj-offload")

        # Context size: only pass --ctx-size when a specific value is selected
        ctx_size = self.model_context_size.itemData(
            self.model_context_size.currentIndex(),
            Qt.UserRole,
        )
        if ctx_size is not None and int(ctx_size) > 0:
            cmd.extend(["--ctx-size", str(ctx_size)])

        cmd.extend(["--host", host, "--port", str(port)])

        self._server_url = f"http://{host}:{port}"
        self._auto_refresh_done = False

        self.output_display.clear()
        self.output_display.appendPlainText(f"Launching: {' '.join(cmd)}\n---\n")

        # Use two-argument form: program + arguments list (args must NOT include the program)
        self._process.start(cmd[0], cmd[1:])
        self.launch_button.setText("STOP")

        # Update web view to point to the server
        server_url = f"http://{host}:{port}"
        self.server_web_view.setUrl(server_url)

    # ------------------------------------------------------------------
    # QProcess output slots
    # ------------------------------------------------------------------

    def _on_stdout(self) -> None:
        """Append stdout from the child process to the output display.

        Also watches for the server URL pattern (http://HOST:PORT) in the
        output and auto-refreshes the web view once the server is ready.
        """
        data = self._process.readAllStandardOutput().data().decode("utf-8", errors="replace")
        if data:
            self.output_display.appendPlainText(data)
            self._check_and_refresh()

    def _on_stderr(self) -> None:
        """Append stderr from the child process to the output display.

        Also watches for the server URL pattern (http://HOST:PORT) in the
        output and auto-refreshes the web view once the server is ready.
        """
        data = self._process.readAllStandardError().data().decode("utf-8", errors="replace")
        if data:
            self.output_display.appendPlainText(data)
            self._check_and_refresh()

    def _check_and_refresh(self) -> None:
        """Check output for server URL and refresh web view once ready.

        Scans the full text of the output display for an HTTP URL pattern.
        When found (and not already refreshed), schedules a one-shot timer
        to reload the web view so the Qt event loop is not blocked.
        """
        if self._auto_refresh_done:
            return

        text = self.output_display.toPlainText()
        match = re.search(r"http://[\w.-]+:\d+", text)
        if match:
            self._auto_refresh_done = True
            QTimer.singleShot(0, self._refresh_web_view)

    def _refresh_web_view(self) -> None:
        """Reload the server web view to fetch the freshly started server."""
        url = QUrl(self._server_url)
        self.server_web_view.setUrl(url)
        self.output_display.appendPlainText(f"\n[Server ready — refreshed web view at {self._server_url}]")

    def _on_error(self, error: QProcess.ProcessError) -> None:
        """Called when the process encounters an error (e.g. not found)."""
        msg = f"Error launching process: {error}"
        self.output_display.appendPlainText(msg)
        self._reset_launch_button()

    def _on_finished(self, code: int, status: QProcess.ExitStatus) -> None:
        """Called when the child process exits."""
        if status == QProcess.ExitStatus.NormalExit:
            self.output_display.appendPlainText(f"\n--- Process exited with code {code} ---")
        else:
            self.output_display.appendPlainText(f"\n--- Process terminated abnormally (code {code}) ---")
        self._reset_launch_button()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Llama model launcher application.")
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host address for the server (default: 127.0.0.1)",
    )
    parser.add_argument("--port", type=int, default=8080, help="Port for the server (default: 8080)")
    parser.add_argument(
        "-c",
        "--ctx-size",
        type=int,
        default=None,
        help="Model context size in tokens (e.g. 4096, 8192, 32768). Overrides the UI combo box.",
    )
    args = parser.parse_args()

    app = QApplication(sys.argv)
    window = LlamaLaunchApp(host=args.host, port=args.port, ctx_size=args.ctx_size)
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())
