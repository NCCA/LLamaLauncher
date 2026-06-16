#!/usr/bin/env -S uv run --script
"""Llama model launcher application."""

import argparse
import json
import re
import sys
from pathlib import Path

from PySide6.QtCore import QCoreApplication, QProcess, QSettings, Qt, QTimer, QUrl
from PySide6.QtGui import QAction
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile
from PySide6.QtWebEngineWidgets import QWebEngineView  # noqa: F401
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QMenu,
    QMessageBox,
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
        self._load_last_session()
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
        cache_dir = (
            Path(QCoreApplication.applicationDirPath()) / ".cache" / "llama-launcher"
        )
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
        profile.setPersistentCookiesPolicy(
            QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies
        )

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
        self._create_file_menu()

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
    # File menu
    # ------------------------------------------------------------------

    def _create_file_menu(self) -> None:
        """Create the File menu with Save, Save As, and Load actions."""
        file_menu = QMenu("&File", self)

        save_action = QAction("Save Configuration", self)
        save_action.setShortcut("Ctrl+S")
        save_action.setStatusTip("Save current configuration to file")
        save_action.triggered.connect(self._save_config)
        file_menu.addAction(save_action)

        save_as_action = QAction("Save As Configuration...", self)
        save_as_action.setStatusTip("Save current configuration to a new file")
        save_as_action.triggered.connect(self._save_config_as)
        file_menu.addAction(save_as_action)

        load_action = QAction("Load Configuration...", self)
        load_action.setShortcut("Ctrl+O")
        load_action.setStatusTip("Load configuration from file")
        load_action.triggered.connect(self._load_config)
        file_menu.addAction(load_action)

        self.menuBar().addMenu(file_menu)

    # ------------------------------------------------------------------
    # Configuration save/load
    # ------------------------------------------------------------------

    def _save_config(self) -> None:
        """Save current configuration to the last saved file or prompt for path."""
        if not hasattr(self, "_last_config_path"):
            self._save_config_as()
            return
        self._write_config_file(self._last_config_path)

    def _save_config_as(self) -> None:
        """Save current configuration to a user-selected file path."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Configuration",
            "",
            "JSON Files (*.json);;All Files (*)",
        )
        if file_path:
            self._write_config_file(file_path)
            self._last_config_path = file_path

    def _write_config_file(self, file_path: str) -> None:
        """Write the current UI configuration to a JSON file.

        Args:
            file_path: Path to the JSON file to write.
        """
        config = self._collect_config()
        try:
            with open(file_path, "w") as f:
                json.dump(config, f, indent=2)
            self.output_display.appendPlainText(f"Configuration saved to {file_path}")
        except Exception as e:
            QMessageBox.critical(
                self, "Save Error", f"Failed to save configuration:\n{e}"
            )

    def _collect_config(self) -> dict:
        """Collect all UI widget values into a configuration dictionary.

        Returns:
            Dictionary containing all configuration values organized by category.
        """
        config: dict = {"version": "1.0"}

        # Files/Paths
        config["files"] = {
            "model_path": self.model_path_edit.property("fullPath") or "",
            "mmproj_path": self.mmproj_path_edit.property("fullPath") or "",
            "draft_model_path": self.draft_model_line_edit.property("fullPath") or "",
            "json_schema_path": self.json_schema_line_edit.property("fullPath") or "",
        }

        # Server
        config["server"] = {
            "host": self.host_line_edit.text(),
            "port": int(self.port_line_edit.text())
            if self.port_line_edit.text().isdigit()
            else 8080,
            "api_key": self.api_key_line_edit.text(),
        }

        # Sampling parameters
        config["sampling"] = {
            "temperature": {
                "enabled": self.enable_temperature_checkbox.isChecked(),
                "value": self.temperature_spinbox.value(),
            },
            "top_p": {
                "enabled": self.enable_top_p_checkbox.isChecked(),
                "value": self.top_p_spinbox.value(),
            },
            "top_k": {
                "enabled": self.enable_top_k_checkbox.isChecked(),
                "value": self.top_k_spinbox.value(),
            },
            "min_p": {
                "enabled": self.enable_min_p_checkbox.isChecked(),
                "value": self.min_p_spinbox.value(),
            },
            "typical_p": {
                "enabled": self.enable_typical_p_checkbox.isChecked(),
                "value": self.typical_p_spinbox.value(),
            },
            "repeat_penalty": {
                "enabled": self.enable_repeat_penalty_checkbox.isChecked(),
                "value": self.repeat_penalty_spinbox.value(),
            },
            "repeat_last_n": {
                "enabled": self.enable_repeat_last_n_checkbox.isChecked(),
                "value": self.repeat_last_n_spinbox.value(),
            },
            "presence_penalty": {
                "enabled": self.enable_presence_penalty_checkbox.isChecked(),
                "value": self.presence_penalty_spinbox.value(),
            },
            "frequency_penalty": {
                "enabled": self.enable_frequency_penalty_checkbox.isChecked(),
                "value": self.frequency_penalty_spinbox.value(),
            },
            "mirostat": {
                "enabled": self.enable_mirostat_checkbox.isChecked(),
                "value": self.mirostat_spinbox.value(),
            },
            "mirostat_lr": {
                "enabled": self.enable_mirostat_lr_checkbox.isChecked(),
                "value": self.mirostat_lr_spinbox.value(),
            },
            "mirostat_ent": {
                "enabled": self.enable_mirostat_ent_checkbox.isChecked(),
                "value": self.mirostat_ent_spinbox.value(),
            },
        }

        # Performance parameters
        config["performance"] = {
            "gpu_layers": {
                "enabled": self.enable_gpu_layers_checkbox.isChecked(),
                "value": self.gpu_layers_spinbox.value(),
            },
            "threads": {
                "enabled": self.enable_threads_checkbox.isChecked(),
                "value": self.threads_spinbox.value(),
            },
            "threads_batch": {
                "enabled": self.enable_threads_batch_checkbox.isChecked(),
                "value": self.threads_batch_spinbox.value(),
            },
            "batch_size": {
                "enabled": self.enable_batch_size_checkbox.isChecked(),
                "value": self.batch_size_spinbox.value(),
            },
            "ubatch_size": {
                "enabled": self.enable_ubatch_size_checkbox.isChecked(),
                "value": self.ubatch_size_spinbox.value(),
            },
            "n_predict": {
                "enabled": self.enable_n_predict_checkbox.isChecked(),
                "value": self.n_predict_spinbox.value(),
            },
            "parallel": {
                "enabled": self.enable_parallel_checkbox.isChecked(),
                "value": self.parallel_spinbox.value(),
            },
            "flash_attn": self.flash_attn_combobox.currentText(),
            "cache_type_k": {
                "enabled": self.enable_cache_type_k_checkbox.isChecked(),
                "value": self.cache_type_k_combobox.currentText(),
            },
            "cache_type_v": {
                "enabled": self.enable_cache_type_v_checkbox.isChecked(),
                "value": self.cache_type_v_combobox.currentText(),
            },
            "mmap": self.enable_mmap_checkbox.isChecked(),
            "mlock": self.enable_mlock_checkbox.isChecked(),
            "cont_batching": self.enable_cont_batching_checkbox.isChecked(),
        }

        # Advanced Generation parameters
        config["advanced"] = {
            "draft_model": {
                "enabled": self.enable_draft_model_checkbox.isChecked(),
                "path": self.draft_model_line_edit.property("fullPath") or "",
            },
            "spec_draft_n_max": {
                "enabled": self.enable_spec_draft_n_max_checkbox.isChecked(),
                "value": self.spec_draft_n_max_spinbox.value(),
            },
            "seed": {
                "enabled": self.enable_seed_checkbox.isChecked(),
                "value": self.seed_spinbox.value(),
            },
            "grammar": {
                "enabled": self.enable_grammar_checkbox.isChecked(),
                "path": self.grammar_line_edit.property("fullPath") or "",
            },
            "json_schema": {
                "enabled": self.enable_json_schema_checkbox.isChecked(),
                "path": self.json_schema_line_edit.property("fullPath") or "",
            },
            "rope_scaling": {
                "enabled": self.enable_rope_scaling_checkbox.isChecked(),
                "value": self.rope_scaling_combobox.currentText(),
            },
            "rope_freq_base": {
                "enabled": self.enable_rope_freq_base_checkbox.isChecked(),
                "value": self.rope_freq_base_spinbox.value(),
            },
            "rope_freq_scale": {
                "enabled": self.enable_rope_freq_scale_checkbox.isChecked(),
                "value": self.rope_freq_scale_spinbox.value(),
            },
        }

        # Other settings
        config["context_size"] = self.model_context_size.itemData(
            self.model_context_size.currentIndex(), Qt.UserRole
        )
        config["more_options"] = self.more_options_line_edit.text()
        config["no_mmproj_offload"] = self.no_mmproj_offload_checkbox.isChecked()

        return config

    def _load_config(self) -> None:
        """Load configuration from a user-selected JSON file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Configuration",
            "",
            "JSON Files (*.json);;All Files (*)",
        )
        if not file_path:
            return

        try:
            with open(file_path, "r") as f:
                config = json.load(f)
            self._apply_config(config)
            self._last_config_path = file_path
            self.output_display.appendPlainText(
                f"Configuration loaded from {file_path}"
            )
        except json.JSONDecodeError as e:
            QMessageBox.critical(self, "Load Error", f"Invalid JSON format:\n{e}")
        except Exception as e:
            QMessageBox.critical(
                self, "Load Error", f"Failed to load configuration:\n{e}"
            )

    def _apply_config(self, config: dict) -> None:
        """Apply configuration values from a dictionary to the UI widgets.

        Args:
            config: Configuration dictionary to apply.
        """
        # Files/Paths
        if "files" in config:
            files = config["files"]
            self._set_path_field(self.model_path_edit, files.get("model_path", ""))
            self._set_path_field(self.mmproj_path_edit, files.get("mmproj_path", ""))
            self._set_path_field(
                self.draft_model_line_edit, files.get("draft_model_path", "")
            )
            self._set_path_field(
                self.json_schema_line_edit, files.get("json_schema_path", "")
            )

        # Server
        if "server" in config:
            server = config["server"]
            self.host_line_edit.setText(server.get("host", "127.0.0.1"))
            port = server.get("port", 8080)
            self.port_line_edit.setText(str(port))
            self.api_key_line_edit.setText(server.get("api_key", "12345"))

        # Sampling parameters
        if "sampling" in config:
            sampling = config["sampling"]
            self._apply_param(
                sampling,
                "temperature",
                self.enable_temperature_checkbox,
                self.temperature_spinbox,
            )
            self._apply_param(
                sampling, "top_p", self.enable_top_p_checkbox, self.top_p_spinbox
            )
            self._apply_param(
                sampling, "top_k", self.enable_top_k_checkbox, self.top_k_spinbox
            )
            self._apply_param(
                sampling, "min_p", self.enable_min_p_checkbox, self.min_p_spinbox
            )
            self._apply_param(
                sampling,
                "typical_p",
                self.enable_typical_p_checkbox,
                self.typical_p_spinbox,
            )
            self._apply_param(
                sampling,
                "repeat_penalty",
                self.enable_repeat_penalty_checkbox,
                self.repeat_penalty_spinbox,
            )
            self._apply_param(
                sampling,
                "repeat_last_n",
                self.enable_repeat_last_n_checkbox,
                self.repeat_last_n_spinbox,
            )
            self._apply_param(
                sampling,
                "presence_penalty",
                self.enable_presence_penalty_checkbox,
                self.presence_penalty_spinbox,
            )
            self._apply_param(
                sampling,
                "frequency_penalty",
                self.enable_frequency_penalty_checkbox,
                self.frequency_penalty_spinbox,
            )
            self._apply_param(
                sampling,
                "mirostat",
                self.enable_mirostat_checkbox,
                self.mirostat_spinbox,
            )
            self._apply_param(
                sampling,
                "mirostat_lr",
                self.enable_mirostat_lr_checkbox,
                self.mirostat_lr_spinbox,
            )
            self._apply_param(
                sampling,
                "mirostat_ent",
                self.enable_mirostat_ent_checkbox,
                self.mirostat_ent_spinbox,
            )

        # Performance parameters
        if "performance" in config:
            perf = config["performance"]
            self._apply_param(
                perf,
                "gpu_layers",
                self.enable_gpu_layers_checkbox,
                self.gpu_layers_spinbox,
            )
            self._apply_param(
                perf, "threads", self.enable_threads_checkbox, self.threads_spinbox
            )
            self._apply_param(
                perf,
                "threads_batch",
                self.enable_threads_batch_checkbox,
                self.threads_batch_spinbox,
            )
            self._apply_param(
                perf,
                "batch_size",
                self.enable_batch_size_checkbox,
                self.batch_size_spinbox,
            )
            self._apply_param(
                perf,
                "ubatch_size",
                self.enable_ubatch_size_checkbox,
                self.ubatch_size_spinbox,
            )
            self._apply_param(
                perf,
                "n_predict",
                self.enable_n_predict_checkbox,
                self.n_predict_spinbox,
            )
            self._apply_param(
                perf, "parallel", self.enable_parallel_checkbox, self.parallel_spinbox
            )

            if "flash_attn" in perf:
                text = perf["flash_attn"]
                index = self.flash_attn_combobox.findText(text)
                if index >= 0:
                    self.flash_attn_combobox.setCurrentIndex(index)

            self._apply_combo_param(
                perf,
                "cache_type_k",
                self.enable_cache_type_k_checkbox,
                self.cache_type_k_combobox,
            )
            self._apply_combo_param(
                perf,
                "cache_type_v",
                self.enable_cache_type_v_checkbox,
                self.cache_type_v_combobox,
            )

            if "mmap" in perf:
                self.enable_mmap_checkbox.setChecked(bool(perf["mmap"]))
            if "mlock" in perf:
                self.enable_mlock_checkbox.setChecked(bool(perf["mlock"]))
            if "cont_batching" in perf:
                self.enable_cont_batching_checkbox.setChecked(
                    bool(perf["cont_batching"])
                )

        # Advanced Generation parameters
        if "advanced" in config:
            adv = config["advanced"]
            self._apply_param(
                adv,
                "spec_draft_n_max",
                self.enable_spec_draft_n_max_checkbox,
                self.spec_draft_n_max_spinbox,
            )
            self._apply_param(adv, "seed", self.enable_seed_checkbox, self.seed_spinbox)

            # Draft model (path-based)
            if "draft_model" in adv:
                draft = adv["draft_model"]
                self.enable_draft_model_checkbox.setChecked(draft.get("enabled", False))
                self._set_path_field(self.draft_model_line_edit, draft.get("path", ""))

            # Grammar (path-based)
            if "grammar" in adv:
                grammar = adv["grammar"]
                self.enable_grammar_checkbox.setChecked(grammar.get("enabled", False))
                self._set_path_field(self.grammar_line_edit, grammar.get("path", ""))

            # JSON schema (path-based)
            if "json_schema" in adv:
                js = adv["json_schema"]
                self.enable_json_schema_checkbox.setChecked(js.get("enabled", False))
                self._set_path_field(self.json_schema_line_edit, js.get("path", ""))

            self._apply_combo_param(
                adv,
                "rope_scaling",
                self.enable_rope_scaling_checkbox,
                self.rope_scaling_combobox,
            )
            self._apply_param(
                adv,
                "rope_freq_base",
                self.enable_rope_freq_base_checkbox,
                self.rope_freq_base_spinbox,
            )
            self._apply_param(
                adv,
                "rope_freq_scale",
                self.enable_rope_freq_scale_checkbox,
                self.rope_freq_scale_spinbox,
            )

        # Other settings
        if "context_size" in config:
            ctx_size = config["context_size"]
            for i in range(self.model_context_size.count()):
                if int(self.model_context_size.itemData(i, Qt.UserRole)) == ctx_size:
                    self.model_context_size.setCurrentIndex(i)
                    break

        if "more_options" in config:
            self.more_options_line_edit.setText(config["more_options"])

        if "no_mmproj_offload" in config:
            self.no_mmproj_offload_checkbox.setChecked(
                bool(config["no_mmproj_offload"])
            )

    def _set_path_field(self, line_edit, path: str) -> None:
        """Set a path field with full path stored and short filename displayed.

        Args:
            line_edit: The QLineEdit widget to update.
            path: The full file path to set.
        """
        if path:
            line_edit.setProperty("fullPath", path)
            line_edit.setText(path.rsplit("/", 1)[-1])
        else:
            line_edit.setProperty("fullPath", "")
            line_edit.setText("")

    def _apply_param(self, params: dict, name: str, checkbox, spinbox) -> None:
        """Apply an enabled+value parameter pair to a checkbox and spinbox.

        Args:
            params: Dictionary containing the parameter data.
            name: Parameter name key in the dictionary.
            checkbox: The QCheckBox widget.
            spinbox: The QSpinBox/QDoubleSpinBox widget.
        """
        if name in params:
            param = params[name]
            if isinstance(param, dict):
                checkbox.setChecked(param.get("enabled", False))
                spinbox.setValue(param.get("value", spinbox.value()))
            else:
                # Legacy format: just a value
                checkbox.setChecked(True)
                spinbox.setValue(param)

    def _apply_combo_param(self, params: dict, name: str, checkbox, combobox) -> None:
        """Apply an enabled+value parameter pair to a checkbox and combobox.

        Args:
            params: Dictionary containing the parameter data.
            name: Parameter name key in the dictionary.
            checkbox: The QCheckBox widget.
            combobox: The QComboBox widget.
        """
        if name in params:
            param = params[name]
            if isinstance(param, dict):
                checkbox.setChecked(param.get("enabled", False))
                text = param.get("value", "")
                index = combobox.findText(text)
                if index >= 0:
                    combobox.setCurrentIndex(index)
            else:
                # Legacy format: just a value
                checkbox.setChecked(True)
                index = combobox.findText(str(param))
                if index >= 0:
                    combobox.setCurrentIndex(index)

    # ------------------------------------------------------------------
    # Window lifecycle
    # ------------------------------------------------------------------

    def closeEvent(self, event) -> None:
        """Save last session settings when the window is closed.

        Uses QSettings to persist basic connection settings and window
        geometry so they are restored on the next launch.
        """
        self._save_last_session()
        super().closeEvent(event)

    def _save_last_session(self) -> None:
        """Save last-used settings to QSettings for session restoration."""
        settings = QSettings("LLamaLauncher", "LlamaLaunchApp")
        settings.setValue(
            "lastModelPath", self.model_path_edit.property("fullPath") or ""
        )
        settings.setValue("host", self.host_line_edit.text())
        settings.setValue("port", self.port_line_edit.text())
        settings.setValue("windowGeometry", self.saveGeometry())

    def _load_last_session(self) -> None:
        """Restore last-used settings from QSettings.

        Pre-populates the UI with the host, port, and model path
        from the previous session so the user doesn't have to re-enter them.
        """
        settings = QSettings("LLamaLauncher", "LlamaLaunchApp")

        # Restore window geometry if saved
        geometry = settings.value("windowGeometry")
        if geometry:
            self.restoreGeometry(geometry)

        # Restore server settings
        host = settings.value("host", "127.0.0.1")
        port = settings.value("port", "8080")
        self.host_line_edit.setText(host)
        self.port_line_edit.setText(port)

        # Restore model path if available
        last_model_path = settings.value("lastModelPath", "")
        if last_model_path:
            self._set_path_field(self.model_path_edit, last_model_path)

    # ------------------------------------------------------------------
    # Signal connections
    # ------------------------------------------------------------------

    def _connect_signals(self) -> None:
        """Connect widget signals to their slot methods."""
        self.select_model_button.clicked.connect(self._select_model)
        self.select_mmproj_button.clicked.connect(self._select_mmproj)
        self.select_draft_model_button.clicked.connect(self._select_draft_model)
        self.select_json_schema_button.clicked.connect(self._select_json_schema)
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

    def _select_draft_model(self) -> None:
        """Open a file dialog to select a draft model .gguf file.

        Stores the full path as a custom property on the line edit
        (accessible via ``getProperty("fullPath")``) while displaying
        only the short filename in the UI.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Draft Model",
            "",
            "GGUF Files (*.gguf)",
        )
        if file_path:
            self.draft_model_line_edit.setProperty("fullPath", file_path)
            self.draft_model_line_edit.setText(file_path.rsplit("/", 1)[-1])

    def _select_json_schema(self) -> None:
        """Open a file dialog to select a JSON schema file.

        Stores the full path as a custom property on the line edit
        (accessible via ``getProperty("fullPath")``) while displaying
        only the short filename in the UI.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select JSON Schema",
            "",
            "JSON Files (*.json)",
        )
        if file_path:
            self.json_schema_line_edit.setProperty("fullPath", file_path)
            self.json_schema_line_edit.setText(file_path.rsplit("/", 1)[-1])

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
            self.output_display.appendPlainText(
                "Server didn't stop gracefully. Force killing..."
            )
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
        min_p = self.min_p_spinbox.value()
        typical_p = self.typical_p_spinbox.value()
        repeat_penalty = self.repeat_penalty_spinbox.value()
        repeat_last_n = self.repeat_last_n_spinbox.value()
        presence_penalty = self.presence_penalty_spinbox.value()
        frequency_penalty = self.frequency_penalty_spinbox.value()

        mirostat = self.mirostat_spinbox.value()
        mirostat_lr = self.mirostat_lr_spinbox.value()
        mirostat_ent = self.mirostat_ent_spinbox.value()

        # Performance parameters
        gpu_layers = self.gpu_layers_spinbox.value()
        threads = self.threads_spinbox.value()
        threads_batch = self.threads_batch_spinbox.value()
        batch_size = self.batch_size_spinbox.value()
        ubatch_size = self.ubatch_size_spinbox.value()
        n_predict = self.n_predict_spinbox.value()
        parallel = self.parallel_spinbox.value()
        cache_type_k = self.cache_type_k_combobox.currentText()
        cache_type_v = self.cache_type_v_combobox.currentText()

        # Advanced Generation parameters
        spec_draft_n_max = self.spec_draft_n_max_spinbox.value()
        seed = self.seed_spinbox.value()
        rope_scaling = self.rope_scaling_combobox.currentText()
        rope_freq_base = self.rope_freq_base_spinbox.value()
        rope_freq_scale = self.rope_freq_scale_spinbox.value()

        mmproj_path = self.mmproj_path_edit.property("fullPath")
        no_mmproj_offload = self.no_mmproj_offload_checkbox.isChecked()
        api_key = (
            self.api_key_line_edit.text() if self.api_key_line_edit.text() else "12345"
        )

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
        if self.enable_min_p_checkbox.isChecked():
            cmd.extend(["--min-p", str(min_p)])
        if self.enable_typical_p_checkbox.isChecked():
            cmd.extend(["--typical-p", str(typical_p)])
        if self.enable_repeat_penalty_checkbox.isChecked():
            cmd.extend(["--repeat-penalty", str(repeat_penalty)])
        if self.enable_repeat_last_n_checkbox.isChecked():
            cmd.extend(["--repeat-last-n", str(repeat_last_n)])
        if self.enable_presence_penalty_checkbox.isChecked():
            cmd.extend(["--presence-penalty", str(presence_penalty)])
        if self.enable_frequency_penalty_checkbox.isChecked():
            cmd.extend(["--frequency-penalty", str(frequency_penalty)])
        if self.enable_mirostat_checkbox.isChecked():
            cmd.extend(["--mirostat", str(mirostat)])
        if self.enable_mirostat_lr_checkbox.isChecked():
            cmd.extend(["--mirostat-lr", str(mirostat_lr)])
        if self.enable_mirostat_ent_checkbox.isChecked():
            cmd.extend(["--mirostat-ent", str(mirostat_ent)])

        # Performance parameters
        if self.enable_gpu_layers_checkbox.isChecked():
            cmd.extend(["--n-gpu-layers", str(gpu_layers)])
        if self.enable_threads_checkbox.isChecked():
            cmd.extend(["--threads", str(threads)])
        if self.enable_threads_batch_checkbox.isChecked():
            cmd.extend(["--threads-batch", str(threads_batch)])
        if self.enable_batch_size_checkbox.isChecked():
            cmd.extend(["--batch-size", str(batch_size)])
        if self.enable_ubatch_size_checkbox.isChecked():
            cmd.extend(["--ubatch-size", str(ubatch_size)])
        if self.enable_n_predict_checkbox.isChecked():
            cmd.extend(["--n-predict", str(n_predict)])
        # Flash Attention: always pass the selected value (default auto)
        flash_attn = self.flash_attn_combobox.currentText()
        cmd.extend(["--flash-attn", flash_attn])
        if self.enable_cache_type_k_checkbox.isChecked():
            cmd.extend(["--cache-type-k", cache_type_k])
        if self.enable_cache_type_v_checkbox.isChecked():
            cmd.extend(["--cache-type-v", cache_type_v])
        if self.enable_mmap_checkbox.isChecked():
            cmd.append("--mmap")
        if self.enable_mlock_checkbox.isChecked():
            cmd.append("--mlock")
        if self.enable_cont_batching_checkbox.isChecked():
            cmd.append("--cont-batching")
        if self.enable_parallel_checkbox.isChecked():
            cmd.extend(["--parallel", str(parallel)])

        # Advanced Generation parameters
        draft_model_path = self.draft_model_line_edit.property("fullPath")
        if self.enable_draft_model_checkbox.isChecked() and draft_model_path:
            cmd.extend(["--draft-model", draft_model_path])
        if self.enable_spec_draft_n_max_checkbox.isChecked():
            cmd.extend(["--spec-draft-n-max", str(spec_draft_n_max)])
        if self.enable_seed_checkbox.isChecked():
            cmd.extend(["--seed", str(seed)])
        grammar_text = self.grammar_line_edit.text().strip()
        if self.enable_grammar_checkbox.isChecked() and grammar_text:
            cmd.extend(["--grammar", grammar_text])
        json_schema_path = self.json_schema_line_edit.property("fullPath")
        if self.enable_json_schema_checkbox.isChecked() and json_schema_path:
            cmd.extend(["--json-schema", json_schema_path])
        if self.enable_rope_scaling_checkbox.isChecked():
            cmd.extend(["--rope-scaling", rope_scaling])
        if self.enable_rope_freq_base_checkbox.isChecked():
            cmd.extend(["--rope-freq-base", str(rope_freq_base)])
        if self.enable_rope_freq_scale_checkbox.isChecked():
            cmd.extend(["--rope-freq-scale", str(rope_freq_scale)])

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

        # Extra user-supplied flags from the more options line edit
        extra = self.more_options_line_edit.text().strip()
        if extra:
            cmd.extend(extra.split())

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
        data = (
            self._process.readAllStandardOutput()
            .data()
            .decode("utf-8", errors="replace")
        )
        if data:
            self.output_display.appendPlainText(data)
            self._check_and_refresh()

    def _on_stderr(self) -> None:
        """Append stderr from the child process to the output display.

        Also watches for the server URL pattern (http://HOST:PORT) in the
        output and auto-refreshes the web view once the server is ready.
        """
        data = (
            self._process.readAllStandardError()
            .data()
            .decode("utf-8", errors="replace")
        )
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
        self.output_display.appendPlainText(
            f"\n[Server ready — refreshed web view at {self._server_url}]"
        )

    def _on_error(self, error: QProcess.ProcessError) -> None:
        """Called when the process encounters an error (e.g. not found)."""
        msg = f"Error launching process: {error}"
        self.output_display.appendPlainText(msg)
        self._reset_launch_button()

    def _on_finished(self, code: int, status: QProcess.ExitStatus) -> None:
        """Called when the child process exits."""
        if status == QProcess.ExitStatus.NormalExit:
            self.output_display.appendPlainText(
                f"\n--- Process exited with code {code} ---"
            )
        else:
            self.output_display.appendPlainText(
                f"\n--- Process terminated abnormally (code {code}) ---"
            )
        self._reset_launch_button()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Llama model launcher application.")
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host address for the server (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port", type=int, default=8080, help="Port for the server (default: 8080)"
    )
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
    window.show()
    sys.exit(app.exec())
