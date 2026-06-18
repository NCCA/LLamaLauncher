"""Tests for LlamaLaunchApp signal handlers and UI logic.

Covers _toggle_launch, _stop_model, _force_kill_if_needed,
_reset_launch_button, _on_stdout, _on_stderr, _check_and_refresh,
_refresh_web_view, _on_error, and _on_finished behaviour.
Uses mocks to isolate Qt runtime dependencies.

"""

from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtCore import QProcess

from main import LlamaLaunchApp


# ==================================================================
# Fixtures
# ==================================================================


@pytest.fixture
def mock_app():
    """Create mock LlamaLaunchApp with all attributes needed for signal tests.

    Returns:
        MagicMock configured with mock Qt widgets and process for
        testing signal handler methods.
    """
    app = MagicMock(spec=LlamaLaunchApp)

    # Process
    app._process = MagicMock()
    app._process.state.return_value = QProcess.NotRunning

    # UI widgets
    app.launch_button = MagicMock()
    app.output_display = MagicMock()
    app.server_web_view = MagicMock()

    # Internal state
    app._server_url = "http://127.0.0.1:8080"
    app._auto_refresh_done = False

    # Helper methods (mocked to track calls)
    app._stop_model = MagicMock()
    app._launch_model = MagicMock()
    app._reset_launch_button = MagicMock()

    return app


@pytest.fixture
def mock_app_running(mock_app):
    """Create mock LlamaLaunchApp with process in Running state.

    Args:
        mock_app: Base mock application fixture.

    Returns:
        MagicMock with process state set to Running.
    """
    mock_app._process.state.return_value = QProcess.Running
    return mock_app


@pytest.fixture
def mock_app_with_stdout(mock_app):
    """Create mock LlamaLaunchApp with stdout data available.

    Args:
        mock_app: Base mock application fixture.

    Returns:
        MagicMock with process that returns stdout data.
    """
    mock_process = MagicMock()
    mock_process.state.return_value = QProcess.Running

    # Mock QProcess.ReadOnlyChannelError
    mock_error = MagicMock()
    mock_error.value = 2

    read_all = MagicMock()
    read_all.data.return_value = b"server output\n"

    mock_process.readAllStandardOutput.return_value = read_all
    mock_process.errorString.return_value = "Unknown error"

    app = mock_app
    app._process = mock_process
    return app


@pytest.fixture
def mock_app_with_stderr(mock_app):
    """Create mock LlamaLaunchApp with stderr data available.

    Args:
        mock_app: Base mock application fixture.

    Returns:
        MagicMock with process that returns stderr data.
    """
    mock_process = MagicMock()
    mock_process.state.return_value = QProcess.Running

    read_all = MagicMock()
    read_all.data.return_value = b"error output\n"

    mock_process.readAllStandardError.return_value = read_all

    app = mock_app
    app._process = mock_process
    return app


# ==================================================================
# 5.1 - 5.2: _toggle_launch
# ==================================================================


class TestToggleLaunch:
    """5.x: Testing _toggle_launch method."""

    def test_5_1_calls_stop_model_when_process_running(self, mock_app_running) -> None:
        """5.1: _toggle_launch calls _stop_model when process is running.

        When the QProcess is in Running state, _toggle_launch should
        invoke _stop_model to gracefully shut down the server.
        """
        # Arrange
        mock_app_running._auto_refresh_done = False

        # Act
        LlamaLaunchApp._toggle_launch(mock_app_running)

        # Assert
        mock_app_running._stop_model.assert_called_once()
        mock_app_running._launch_model.assert_not_called()

    def test_5_2_calls_launch_model_when_process_not_running(self, mock_app) -> None:
        """5.2: _toggle_launch calls _launch_model when process is not running.

        When the QProcess is not in Running state, _toggle_launch should
        invoke _launch_model to start the server.
        """
        # Arrange
        mock_app._process.state.return_value = QProcess.NotRunning
        mock_app._auto_refresh_done = False

        # Act
        LlamaLaunchApp._toggle_launch(mock_app)

        # Assert
        mock_app._launch_model.assert_called_once()
        mock_app._stop_model.assert_not_called()


# ==================================================================
# 5.3: _stop_model
# ==================================================================


class TestStopModel:
    """5.3: Testing _stop_model method."""

    def test_5_3_calls_terminate_and_shows_message(self, mock_app) -> None:
        """5.3: _stop_model calls terminate() on process and shows message.

        When stopping the model, the method should:
        - Call QProcess.terminate() to send SIGTERM
        - Append a message to output_display indicating stopping
        - Schedule _force_kill_if_needed after 2 seconds
        """
        # Arrange
        process = MagicMock()
        app = mock_app
        app._process = process
        app.output_display = MagicMock()

        with patch("main.QTimer") as mock_qtimer:
            # Act
            LlamaLaunchApp._stop_model(app)

            # Assert
            process.terminate.assert_called_once()
            app.output_display.appendPlainText.assert_called_once_with(
                "Stopping server... (sent SIGTERM)"
            )
            mock_qtimer.singleShot.assert_called_once_with(
                2000, app._force_kill_if_needed
            )


# ==================================================================
# 5.4: _force_kill_if_needed
# ==================================================================


class TestForceKillIfNeeded:
    """5.4: Testing _force_kill_if_needed method."""

    def test_5_4_calls_kill_when_process_still_running(self, mock_app) -> None:
        """5.4: _force_kill_if_needed calls kill() if process doesn't stop in time.

        When the process is still running after the grace period,
        the method should force kill it and log a message.
        """
        # Arrange
        process = MagicMock()
        process.state.return_value = QProcess.Running
        app = mock_app
        app._process = process
        app.output_display = MagicMock()

        # Act
        LlamaLaunchApp._force_kill_if_needed(app)

        # Assert
        process.kill.assert_called_once()
        app.output_display.appendPlainText.assert_called_once_with(
            "Server didn't stop gracefully. Force killing..."
        )

    def test_5_4_does_nothing_when_process_stopped(self, mock_app) -> None:
        """5.4: _force_kill_if_needed does nothing when process already stopped.

        If the process has exited gracefully within the grace period,
        no kill() call should be made.
        """
        # Arrange
        process = MagicMock()
        process.state.return_value = QProcess.NotRunning
        app = mock_app
        app._process = process
        app.output_display = MagicMock()

        # Act
        LlamaLaunchApp._force_kill_if_needed(app)

        # Assert
        process.kill.assert_not_called()
        app.output_display.appendPlainText.assert_not_called()


# ==================================================================
# 5.5: _reset_launch_button
# ==================================================================


class TestResetLaunchButton:
    """5.5: Testing _reset_launch_button method."""

    def test_5_5_resets_button_text_to_launch(self, mock_app) -> None:
        """5.5: _reset_launch_button resets button text to 'LAUNCH'.

        After the process exits, the launch button should be reset
        to its default 'LAUNCH' state.
        """
        # Arrange
        app = mock_app
        app.launch_button = MagicMock()

        # Act
        LlamaLaunchApp._reset_launch_button(app)

        # Assert
        app.launch_button.setText.assert_called_once_with("LAUNCH")

    def test_5_5_calls_on_model_selection_changed(self, mock_app) -> None:
        """5.5: _reset_launch_button calls _on_model_selection_changed.

        After resetting the button, the method should also update
        the launch button enabled state based on model selection.
        """
        # Arrange
        app = mock_app
        app.launch_button = MagicMock()
        app._on_model_selection_changed = MagicMock()

        # Act
        LlamaLaunchApp._reset_launch_button(app)

        # Assert
        app._on_model_selection_changed.assert_called_once()


# ==================================================================
# 5.6 - 5.7: _on_stdout
# ==================================================================


class TestOnStdout:
    """5.6 - 5.7: Testing _on_stdout method."""

    def test_5_6_reads_stdout_and_appends_to_output_display(
        self, mock_app_with_stdout
    ) -> None:
        """5.6: _on_stdout reads stdout data and appends to output_display.

        When the child process writes to stdout, the method should
        read the data, decode it, and append it to the output display.
        """
        # Arrange
        app = mock_app_with_stdout

        # Act
        LlamaLaunchApp._on_stdout(app)

        # Assert
        app.output_display.appendPlainText.assert_called_once_with("server output\n")

    def test_5_7_calls_check_and_refresh_after_appending_data(
        self, mock_app_with_stdout
    ) -> None:
        """5.7: _on_stdout calls _check_and_refresh after appending data.

        After appending stdout data, the method should check if the
        server URL pattern is present and schedule a web view refresh.
        """
        # Arrange
        app = mock_app_with_stdout
        app._check_and_refresh = MagicMock()

        # Act
        LlamaLaunchApp._on_stdout(app)

        # Assert
        app._check_and_refresh.assert_called_once()

    def test_5_6_does_nothing_when_no_stdout_data(self, mock_app) -> None:
        """5.6: _on_stdout does nothing when there is no stdout data.

        If the process produces no output, the method should not
        append anything to the display.
        """
        # Arrange
        mock_process = MagicMock()
        mock_process.state.return_value = QProcess.Running
        read_all = MagicMock()
        read_all.data.return_value = b""
        mock_process.readAllStandardOutput.return_value = read_all

        app = mock_app
        app._process = mock_process
        app.output_display = MagicMock()
        app._check_and_refresh = MagicMock()

        # Act
        LlamaLaunchApp._on_stdout(app)

        # Assert
        app.output_display.appendPlainText.assert_not_called()


# ==================================================================
# 5.8 - 5.9: _on_stderr
# ==================================================================


class TestOnStderr:
    """5.8 - 5.9: Testing _on_stderr method."""

    def test_5_8_reads_stderr_and_appends_to_output_display(
        self, mock_app_with_stderr
    ) -> None:
        """5.8: _on_stderr reads stderr data and appends to output_display.

        When the child process writes to stderr, the method should
        read the data, decode it, and append it to the output display.
        """
        # Arrange
        app = mock_app_with_stderr

        # Act
        LlamaLaunchApp._on_stderr(app)

        # Assert
        app.output_display.appendPlainText.assert_called_once_with("error output\n")

    def test_5_9_calls_check_and_refresh_after_appending_data(
        self, mock_app_with_stderr
    ) -> None:
        """5.9: _on_stderr calls _check_and_refresh after appending data.

        After appending stderr data, the method should check if the
        server URL pattern is present and schedule a web view refresh.
        """
        # Arrange
        app = mock_app_with_stderr
        app._check_and_refresh = MagicMock()

        # Act
        LlamaLaunchApp._on_stderr(app)

        # Assert
        app._check_and_refresh.assert_called_once()

    def test_5_8_does_nothing_when_no_stderr_data(self, mock_app) -> None:
        """5.8: _on_stderr does nothing when there is no stderr data.

        If the process produces no stderr output, the method should not
        append anything to the display.
        """
        # Arrange
        mock_process = MagicMock()
        mock_process.state.return_value = QProcess.Running
        read_all = MagicMock()
        read_all.data.return_value = b""
        mock_process.readAllStandardError.return_value = read_all

        app = mock_app
        app._process = mock_process
        app.output_display = MagicMock()
        app._check_and_refresh = MagicMock()

        # Act
        LlamaLaunchApp._on_stderr(app)

        # Assert
        app.output_display.appendPlainText.assert_not_called()


# ==================================================================
# 5.10 - 5.12: _check_and_refresh
# ==================================================================


class TestCheckAndRefresh:
    """5.10 - 5.12: Testing _check_and_refresh method."""

    def test_5_10_does_nothing_when_auto_refresh_done(self, mock_app) -> None:
        """5.10: _check_and_refresh does nothing if _auto_refresh_done is True.

        Once the web view has been refreshed, subsequent calls should
        be no-ops to avoid redundant refreshes.
        """
        # Arrange
        app = mock_app
        app._auto_refresh_done = True
        app.output_display = MagicMock()
        app.output_display.toPlainText.return_value = "http://127.0.0.1:8080"

        with patch("main.QTimer") as mock_qtimer:
            # Act
            LlamaLaunchApp._check_and_refresh(app)

            # Assert
            mock_qtimer.singleShot.assert_not_called()

    def test_5_11_schedules_refresh_when_url_pattern_found(self, mock_app) -> None:
        """5.11: _check_and_refresh schedules _refresh_web_view when URL pattern found.

        When the output display contains an HTTP URL pattern, the method
        should mark auto_refresh_done as True and schedule a one-shot
        timer to call _refresh_web_view.
        """
        # Arrange
        app = mock_app
        app._auto_refresh_done = False
        app.output_display = MagicMock()
        app.output_display.toPlainText.return_value = (
            "Loading... http://127.0.0.1:8080 ready"
        )

        with patch("main.QTimer") as mock_qtimer:
            # Act
            LlamaLaunchApp._check_and_refresh(app)

            # Assert
            assert app._auto_refresh_done is True
            mock_qtimer.singleShot.assert_called_once_with(0, app._refresh_web_view)

    def test_5_12_does_nothing_when_no_url_pattern(self, mock_app) -> None:
        """5.12: _check_and_refresh does nothing when no URL pattern found.

        When the output display does not contain an HTTP URL pattern,
        the method should not schedule any refresh.
        """
        # Arrange
        app = mock_app
        app._auto_refresh_done = False
        app.output_display = MagicMock()
        app.output_display.toPlainText.return_value = (
            "Loading model... this is just text"
        )

        with patch("main.QTimer") as mock_qtimer:
            # Act
            LlamaLaunchApp._check_and_refresh(app)

            # Assert
            assert app._auto_refresh_done is False
            mock_qtimer.singleShot.assert_not_called()


# ==================================================================
# 5.13: _refresh_web_view
# ==================================================================


class TestRefreshWebView:
    """5.13: Testing _refresh_web_view method."""

    def test_5_13_sets_web_view_url_and_appends_ready_message(self, mock_app) -> None:
        """5.13: _refresh_web_view sets web view URL and appends ready message.

        When the server is ready, this method should update the web
        view to point to the server URL and log a ready message.
        """
        # Arrange
        from PySide6.QtCore import QUrl

        app = mock_app
        app._server_url = "http://127.0.0.1:8080"
        app.server_web_view = MagicMock()
        app.output_display = MagicMock()

        # Act
        LlamaLaunchApp._refresh_web_view(app)

        # Assert
        app.server_web_view.setUrl.assert_called_once()
        called_url = app.server_web_view.setUrl.call_args[0][0]
        assert isinstance(called_url, QUrl)
        assert called_url.toString() == "http://127.0.0.1:8080"

        # Check that ready message was appended
        call_args = app.output_display.appendPlainText.call_args
        assert "[Server ready" in call_args[0][0]
        assert "http://127.0.0.1:8080" in call_args[0][0]


# ==================================================================
# 5.14: _on_error
# ==================================================================


class TestOnError:
    """5.14: Testing _on_error method."""

    def test_5_14_appends_error_message_and_resets_launch_button(
        self, mock_app
    ) -> None:
        """5.14: _on_error appends error message and resets launch button.

        When the process encounters an error (e.g., binary not found),
        the method should log the error and reset the launch button.
        """
        # Arrange
        from PySide6.QtCore import QProcess

        app = mock_app
        app.output_display = MagicMock()
        app._reset_launch_button = MagicMock()

        # Create a mock ProcessError
        error = QProcess.ProcessError.FailedToStart

        # Act
        LlamaLaunchApp._on_error(app, error)

        # Assert
        app.output_display.appendPlainText.assert_called_once()
        error_msg = app.output_display.appendPlainText.call_args[0][0]
        assert "Error launching process" in error_msg

        app._reset_launch_button.assert_called_once()


# ==================================================================
# 5.15 - 5.17: _on_finished
# ==================================================================


class TestOnFinished:
    """5.15 - 5.17: Testing _on_finished method."""

    def test_5_15_shows_normal_exit_message(self, mock_app) -> None:
        """5.15: _on_finished shows normal exit message.

        When the process exits normally (clean shutdown), the method
        should log the exit code and reset the launch button.
        """
        # Arrange
        from PySide6.QtCore import QProcess

        app = mock_app
        app.output_display = MagicMock()
        app._reset_launch_button = MagicMock()
        status = QProcess.ExitStatus.NormalExit
        code = 0

        # Act
        LlamaLaunchApp._on_finished(app, code, status)

        # Assert
        call_args = app.output_display.appendPlainText.call_args
        assert "Process exited with code" in call_args[0][0]
        assert str(code) in call_args[0][0]

        app._reset_launch_button.assert_called_once()

    def test_5_16_shows_abnormal_termination_message(self, mock_app) -> None:
        """5.16: _on_finished shows abnormal termination message.

        When the process exits abnormally (crash or kill), the method
        should log the abnormal exit and reset the launch button.
        """
        # Arrange
        from PySide6.QtCore import QProcess

        app = mock_app
        app.output_display = MagicMock()
        app._reset_launch_button = MagicMock()
        status = QProcess.ExitStatus.CrashExit
        code = 137  # SIGKILL

        # Act
        LlamaLaunchApp._on_finished(app, code, status)

        # Assert
        call_args = app.output_display.appendPlainText.call_args
        assert "Process terminated abnormally" in call_args[0][0]
        assert str(code) in call_args[0][0]

        app._reset_launch_button.assert_called_once()

    def test_5_17_resets_launch_button_after_process_exits(self, mock_app) -> None:
        """5.17: _on_finished resets launch button after process exits.

        Regardless of exit status (normal or abnormal), the method
        should always reset the launch button to its default state.
        """
        # Arrange
        from PySide6.QtCore import QProcess

        app = mock_app
        app.output_display = MagicMock()
        app._reset_launch_button = MagicMock()

        # Test with NormalExit
        LlamaLaunchApp._on_finished(app, 0, QProcess.ExitStatus.NormalExit)
        app._reset_launch_button.assert_called()

        # Reset mock and test with CrashExit
        app._reset_launch_button.reset_mock()
        LlamaLaunchApp._on_finished(app, 1, QProcess.ExitStatus.CrashExit)
        app._reset_launch_button.assert_called()
