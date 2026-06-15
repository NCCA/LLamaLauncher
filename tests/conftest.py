"""Shared pytest fixtures for the LLamaLauncher test suite."""

import os
import tempfile
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture(scope="session")
def qapp():
    """Provide a QApplication singleton for the test session.

    This fixture ensures only one QApplication instance is created
    across all Qt tests in the session.
    """
    from PySide6.QtWidgets import QApplication

    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    # Cleanup is handled by QApplication at session end


@pytest.fixture()
def temp_dir():
    """Provide a temporary directory that is cleaned up after each test.

    Returns the path to the temporary directory and removes it afterward.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture()
def mock_qprocess():
    """Provide a mocked QProcess for testing process-related code.

    Returns a MagicMock configured to mimic basic QProcess behavior.
    """
    with patch("PySide6.QtCore.QProcess") as mock:
        process = MagicMock()
        process.state.return_value = 0  # NotRunning
        process.readAllStandardOutput.return_value = b""
        process.readAllStandardError.return_value = b""
        mock.return_value = process
        yield process
