"""Tests for configuration writing in LlamaLaunchApp.

Covers _write_config_file behaviour: JSON output, UI feedback, and error handling.
Uses mocks to isolate the method from Qt runtime dependencies.
"""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from main import LlamaLaunchApp

# ==================================================================
# 2.2 Configuration Writing (_write_config_file)
# ==================================================================


class TestWriteConfigFile:
    """2.2: Testing _write_config_file method."""

    def test_writes_valid_json_to_file_path(self, tmp_path: Path) -> None:
        """2.2.1: Writes valid JSON to file path.

        The method should call _collect_config(), write the result as
        indented JSON to the specified file path, and leave a parseable
        file on disk.
        """
        # Arrange
        app = MagicMock(spec=LlamaLaunchApp)
        app._collect_config.return_value = {
            "version": "1.0",
            "server": {"host": "127.0.0.1", "port": 8080},
        }
        app.output_display = MagicMock()

        file_path = tmp_path / "config.json"

        # Act
        LlamaLaunchApp._write_config_file(app, str(file_path))

        # Assert - file exists and contains valid JSON matching the config
        assert file_path.exists()
        with open(file_path) as f:
            data = json.load(f)
        assert data == {
            "version": "1.0",
            "server": {"host": "127.0.0.1", "port": 8080},
        }

    def test_appends_success_message_to_output_display(self, tmp_path: Path) -> None:
        """2.2.2: Appends success message to output_display.

        After a successful write the method should call
        output_display.appendPlainText with a message that includes the
        file path.
        """
        # Arrange
        app = MagicMock(spec=LlamaLaunchApp)
        app._collect_config.return_value = {"test_key": "test_value"}
        app.output_display = MagicMock()

        file_path = tmp_path / "saved.json"

        # Act
        LlamaLaunchApp._write_config_file(app, str(file_path))

        # Assert
        expected_message = f"Configuration saved to {file_path}"
        app.output_display.appendPlainText.assert_called_once_with(expected_message)

    def test_shows_qmessagebox_critical_on_write_failure(self) -> None:
        """2.2.3: Shows QMessageBox.critical on write failure (permission denied).

        When the file system raises an exception during writing the method
        should catch it and display a critical dialog with the error message.
        """
        # Arrange
        app = MagicMock(spec=LlamaLaunchApp)
        app._collect_config.return_value = {"should_not_be_written": True}

        file_path = "/nonexistent/path/config.json"

        # Mock open to raise PermissionError (simulates permission denied)
        with patch("builtins.open", side_effect=PermissionError("Permission denied")):
            with patch.object(LlamaLaunchApp, "__module__", "main"):
                # QMessageBox is imported into main's namespace at line 19
                with patch("main.QMessageBox") as mock_qmsgbox:
                    # Act
                    LlamaLaunchApp._write_config_file(app, file_path)

                    # Assert - critical dialog was shown
                    mock_qmsgbox.critical.assert_called_once()
                    call_args = mock_qmsgbox.critical.call_args
                    positional = call_args[0]

                    assert positional[0] == app  # parent widget
                    assert positional[1] == "Save Error"  # title
                    assert "Failed to save configuration" in positional[2]  # message
                    assert "Permission denied" in positional[2]  # error detail
