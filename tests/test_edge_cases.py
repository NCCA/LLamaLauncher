"""Phase 7: Edge Cases and Error Handling tests.

Covers error paths, edge cases, and robustness for LlamaLaunchApp:

- _launch_model handles missing model file gracefully
- API key defaults when line edit is empty
- _apply_param uses spinbox default value
- _apply_combo_param does nothing on no text match
- _collect_config handles missing optional sections
- _on_stdout/_on_stderr handle empty data
- _check_and_refresh regex matches various URL formats
- __init__ initializes _process with correct signal connections

TDD: tests written before implementation (RED phase).
"""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from PySide6.QtCore import QByteArray, QProcess
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QSpinBox,
)

# Ensure worktree
sys.path.insert(0, str(Path(__file__).parent.parent))


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def app():
    """Provide QApplication singleton for test module."""
    application = QApplication.instance()
    if application is None:
        application = QApplication(sys.argv)
    yield application


@pytest.fixture
def launch_app(app):
    """Provide a LlamaLaunchApp instance for testing.

    Since full UI initialization is expensive, we create the app and
    patch widgets that tests don't interact with.
    """
    from main import LlamaLaunchApp

    instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
    yield instance
    instance.close()


@pytest.fixture
def minimal_app(app):
    """Minimal LlamaLaunchApp-like class for testing helper methods.

    Since _apply_param and _apply_combo_param are instance methods on
    LlamaLaunchApp, we create a minimal subclass that only initializes
    the widgets we care about.
    """

    class TestApp(QApplication):  # type: ignore[misc]
        """Minimal app for testing helper method behavior."""

        pass

    return app


# ---------------------------------------------------------------------------
# 7.1: _launch_model handles missing model file gracefully
# ---------------------------------------------------------------------------


class TestLaunchModelMissingFile:
    """7.1: _launch_model handles missing model file (command still built)."""

    def test_7_1_appends_error_when_no_model_selected(self, launch_app):
        """7.1: _launch_model appends error message when no model is selected."""
        # Clear any existing output
        launch_app.output_display.clear()
        # Ensure model path is empty
        launch_app.model_path_edit.setProperty("fullPath", "")
        launch_app.model_path_edit.setText("")

        launch_app._launch_model()

        # Should show error message, not crash
        output = launch_app.output_display.toPlainText()
        assert "Error" in output or "no model" in output.lower()


# ---------------------------------------------------------------------------
# 7.2: API key defaults to "12345" when line edit is empty
# ---------------------------------------------------------------------------


class TestApiKeyDefault:
    """7.2: API key defaults to '12345' when line edit is empty."""

    def test_7_2_api_key_defaults_to_12345_when_empty(self, launch_app):
        """7.2: _collect_config returns '12345' when api_key_line_edit is empty."""
        # Ensure the line edit is empty
        launch_app.api_key_line_edit.setText("")

        config = launch_app._collect_config()

        assert config["server"]["api_key"] == "12345"

    def test_7_2_api_key_uses_line_edit_value_when_not_empty(self, launch_app):
        """7.2: _collect_config uses line edit value when not empty."""
        launch_app.api_key_line_edit.setText("my-secret-key")

        config = launch_app._collect_config()

        assert config["server"]["api_key"] == "my-secret-key"


# ---------------------------------------------------------------------------
# 7.3: _apply_param uses spinbox default when config lacks "value" key
# ---------------------------------------------------------------------------


class TestApplyParamEdgeCases:
    """7.3: _apply_param edge cases with main.py implementation."""

    def test_7_3_uses_spinbox_default_when_value_key_missing(self, launch_app):
        """7.3: _apply_param falls back to spinbox.value() when 'value' key absent."""
        checkbox = QCheckBox()
        spinbox = QSpinBox()
        spinbox.setValue(42)  # Initial value as "default"

        # Dict with "enabled" but no "value" key
        params = {"temperature": {"enabled": True}}

        launch_app._apply_param(params, "temperature", checkbox, spinbox)

        assert checkbox.isChecked() is True
        assert spinbox.value() == 42  # Kept the initial value

    def test_7_3_applies_value_when_present(self, launch_app):
        """7.3: _apply_param applies 'value' when present in dict."""
        checkbox = QCheckBox()
        spinbox = QDoubleSpinBox()
        spinbox.setValue(0)

        params = {"temperature": {"enabled": True, "value": 0.7}}

        launch_app._apply_param(params, "temperature", checkbox, spinbox)

        assert checkbox.isChecked() is True
        assert spinbox.value() == 0.7

    def test_7_3_defaults_enabled_to_false(self, launch_app):
        """7.3: _apply_param defaults enabled to False when key missing."""
        checkbox = QCheckBox()
        checkbox.setChecked(True)  # Start checked
        spinbox = QDoubleSpinBox()

        params = {"temperature": {"value": 0.5}}

        launch_app._apply_param(params, "temperature", checkbox, spinbox)

        assert checkbox.isChecked() is False
        assert spinbox.value() == 0.5


# ---------------------------------------------------------------------------
# 7.4: _apply_combo_param does nothing when combobox doesn't find text match
# ---------------------------------------------------------------------------


class TestApplyComboParamEdgeCases:
    """7.4: _apply_combo_param edge cases with main.py implementation."""

    def test_7_4_no_change_when_text_not_in_combobox(self, launch_app):
        """7.4: _apply_combo_param leaves combobox unchanged when text not found."""
        checkbox = QCheckBox()
        combobox = QComboBox()
        combobox.addItems(["auto", "fp16", "bf16"])
        combobox.setCurrentText("auto")
        initial_index = combobox.currentIndex()

        params = {"cache_type_k": {"enabled": True, "value": "nonexistent"}}

        launch_app._apply_combo_param(params, "cache_type_k", checkbox, combobox)

        # Checkbox should be checked but combobox index unchanged
        assert checkbox.isChecked() is True
        assert combobox.currentIndex() == initial_index

    def test_7_4_applies_when_text_found(self, launch_app):
        """7.4: _apply_combo_param sets combobox when text matches."""
        checkbox = QCheckBox()
        combobox = QComboBox()
        combobox.addItems(["auto", "fp16", "bf16"])

        params = {"cache_type_k": {"enabled": True, "value": "bf16"}}

        launch_app._apply_combo_param(params, "cache_type_k", checkbox, combobox)

        assert checkbox.isChecked() is True
        assert combobox.currentText() == "bf16"


# ---------------------------------------------------------------------------
# 7.5: _collect_config handles missing optional sections without error
# ---------------------------------------------------------------------------


class TestCollectConfigMissingSections:
    """7.5: _apply_config handles incomplete/missing config sections."""

    def test_7_5_applies_minimal_config(self, launch_app):
        """7.5: _apply_config handles file with only required sections."""
        minimal_config = {
            "version": "1.0",
            "server": {"host": "127.0.0.1", "port": 8080},
        }

        # Should not raise, should use defaults for missing sections
        launch_app._apply_config(minimal_config)

        # Server values should be applied
        assert launch_app.host_line_edit.text() == "127.0.0.1"
        assert launch_app.port_line_edit.text() == "8080"

    def test_7_5_applies_empty_config(self, launch_app):
        """7.5: _apply_config handles empty JSON object without error."""

        # Should not raise
        launch_app._apply_config({})


# ---------------------------------------------------------------------------
# 7.6: _on_stdout handles empty data (no append)
# ---------------------------------------------------------------------------


class TestOnStdoutEmptyData:
    """7.6: _on_stdout handles empty data gracefully."""

    def test_7_6_does_not_append_when_stdout_empty(self, launch_app):
        """7.6: _on_stdout does nothing when process has no stdout data."""
        launch_app.output_display.clear()

        # Patch readAllStandardOutput to return a QByteArray that decodes to empty string
        with patch.object(
            launch_app._process,
            "readAllStandardOutput",
            return_value=QByteArray(b""),
        ):
            launch_app._on_stdout()

        output = launch_app.output_display.toPlainText()
        assert output == ""


# ---------------------------------------------------------------------------
# 7.7: _on_stderr handles empty data (no append)
# ---------------------------------------------------------------------------


class TestOnStderrEmptyData:
    """7.7: _on_stderr handles empty data gracefully."""

    def test_7_7_does_not_append_when_stderr_empty(self, launch_app):
        """7.7: _on_stderr does nothing when process has no stderr data."""
        launch_app.output_display.clear()

        # Patch readAllStandardError to return a QByteArray that decodes to empty string
        with patch.object(
            launch_app._process,
            "readAllStandardError",
            return_value=QByteArray(b""),
        ):
            launch_app._on_stderr()

        output = launch_app.output_display.toPlainText()
        assert output == ""


# ---------------------------------------------------------------------------
# 7.8: _check_and_refresh regex matches various URL formats
# ---------------------------------------------------------------------------


class TestCheckAndRefreshRegex:
    """7.8: _check_and_refresh regex handles various URL formats."""

    def test_7_8_matches_standard_url(self, launch_app):
        """7.8: Regex matches http://host:port format."""
        launch_app.output_display.clear()
        launch_app._auto_refresh_done = False
        launch_app.output_display.appendPlainText(
            "Loading models...\nhttp://127.0.0.1:8080"
        )

        launch_app._check_and_refresh()

        assert launch_app._auto_refresh_done is True

    def test_7_8_matches_domain_url(self, launch_app):
        """7.8: Regex matches http://domain.com:port format."""
        launch_app.output_display.clear()
        launch_app._auto_refresh_done = False
        launch_app.output_display.appendPlainText("Server at http://localhost:3000")

        launch_app._check_and_refresh()

        assert launch_app._auto_refresh_done is True

    def test_7_8_no_match_for_non_url_text(self, launch_app):
        """7.8: Regex does not match text without URL pattern."""
        launch_app.output_display.clear()
        launch_app._auto_refresh_done = False
        launch_app.output_display.appendPlainText("No server URL here")

        launch_app._check_and_refresh()

        assert launch_app._auto_refresh_done is False

    def test_7_8_no_refresh_when_already_done(self, launch_app):
        """7.8: _check_and_refresh returns early when already refreshed."""
        launch_app._auto_refresh_done = True
        # Should return immediately without scanning
        launch_app._check_and_refresh()
        assert launch_app._auto_refresh_done is True


# ---------------------------------------------------------------------------
# 7.9: __init__ initializes _process with correct signal connections
# ---------------------------------------------------------------------------


class TestInitProcessSetup:
    """7.9: __init__ initializes _process with correct signal connections."""

    def test_7_9_process_is_qprocess_instance(self, app):
        """7.9: __init__ creates _process as QProcess instance."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            assert isinstance(instance._process, QProcess)
        finally:
            instance.close()

    def test_7_9_process_parent_is_app(self, app):
        """7.9: _process has the app instance as parent (auto-cleanup)."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            assert instance._process.parent() is instance
        finally:
            instance.close()

    def test_7_9_stdout_signal_connected(self, app):
        """7.9: _process.readyReadStandardOutput connected to _on_stdout."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            # Verify slot exists and is callable (indirect connection verification)
            assert hasattr(instance, "_on_stdout")
            assert callable(instance._on_stdout)
            # Emit the signal and verify the slot was called
            with patch.object(
                instance, "_on_stdout", wraps=instance._on_stdout
            ) as mock:
                instance._process.readyReadStandardOutput.emit()
                mock.assert_called_once()
        finally:
            instance.close()

    def test_7_9_stderr_signal_connected(self, app):
        """7.9: _process.readyReadStandardError connected to _on_stderr."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            assert hasattr(instance, "_on_stderr")
            assert callable(instance._on_stderr)
            with patch.object(
                instance, "_on_stderr", wraps=instance._on_stderr
            ) as mock:
                instance._process.readyReadStandardError.emit()
                mock.assert_called_once()
        finally:
            instance.close()

    def test_7_9_finished_signal_connected(self, app):
        """7.9: _process.finished connected to _on_finished."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            assert hasattr(instance, "_on_finished")
            assert callable(instance._on_finished)
            with patch.object(
                instance, "_on_finished", wraps=instance._on_finished
            ) as mock:
                instance._process.finished.emit(0, QProcess.ExitStatus.NormalExit)
                mock.assert_called_once()
        finally:
            instance.close()

    def test_7_9_error_signal_connected(self, app):
        """7.9: _process.errorOccurred connected to _on_error."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            assert hasattr(instance, "_on_error")
            assert callable(instance._on_error)
            with patch.object(instance, "_on_error", wraps=instance._on_error) as mock:
                instance._process.errorOccurred.emit(QProcess.ProcessError.UnknownError)
                mock.assert_called_once()
        finally:
            instance.close()
