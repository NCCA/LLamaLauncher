"""Tests for file dialog selection methods in LlamaLaunchApp.

These methods open file dialogs via QFileDialog.getOpenFileName and set
properties on line edit widgets. Each test mocks the file dialog to return
a controlled path and verifies the correct side effects.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Ensure production module is importable
_project_root = str(Path(__file__).resolve().parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from PySide6.QtCore import QProcess  # noqa: E402
from PySide6.QtWidgets import QApplication, QLineEdit  # noqa: E402

from main import LlamaLaunchApp  # noqa: E402


@pytest.fixture()
def mock_line_edit():
    """Provide a mock QLineEdit for testing path display logic."""
    edit = MagicMock(spec=QLineEdit)
    edit.property.return_value = None
    return edit


@pytest.fixture()
def app_with_line_edits(mock_line_edit):
    """Provide a LlamaLaunchApp with line edits replaced by mocks.

    This fixture creates a minimal app instance and replaces the line
    edit attributes that file selection methods interact with, allowing
    us to verify property and text calls without a full UI.
    """
    _app = QApplication.instance() or QApplication([])
    window = LlamaLaunchApp.__new__(LlamaLaunchApp)

    # Mock the process attribute
    window._process = MagicMock(spec=QProcess)
    window._process.state.return_value = QProcess.NotRunning  # type: ignore

    # Replace line edits with mocks
    window.model_path_edit = mock_line_edit
    window.mmproj_path_edit = MagicMock(spec=QLineEdit)
    window.mmproj_path_edit.property.return_value = None
    window.draft_model_line_edit = MagicMock(spec=QLineEdit)
    window.draft_model_line_edit.property.return_value = None
    window.json_schema_line_edit = MagicMock(spec=QLineEdit)
    window.json_schema_line_edit.property.return_value = None

    # Mock launch button
    window.launch_button = MagicMock()

    # Private path attributes
    window._model_path = ""
    window._mmproj_path = ""

    return window


class TestSelectModel:
    """Tests for _select_model file dialog method.

    Target: main.py lines 762-779
    """

    def test_select_model_sets_fullpath_on_model_path_edit(self, app_with_line_edits):
        """_select_model stores the full path as a custom property on model_path_edit."""
        fake_path = "/models/llama.gguf"

        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=(fake_path, ""),
        ):
            app_with_line_edits._select_model()

        app_with_line_edits.model_path_edit.setProperty.assert_called_once_with("fullPath", fake_path)

    def test_select_model_sets_short_filename_on_model_path_edit(self, app_with_line_edits):
        """_select_model displays only the short filename in the line edit."""
        fake_path = "/models/llama.gguf"

        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=(fake_path, ""),
        ):
            app_with_line_edits._select_model()

        app_with_line_edits.model_path_edit.setText.assert_called_once_with("llama.gguf")

    def test_select_model_stores_full_path_in_private_attribute(self, app_with_line_edits):
        """_select_model stores the full path in _model_path."""
        fake_path = "/models/llama.gguf"

        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=(fake_path, ""),
        ):
            app_with_line_edits._select_model()

        assert app_with_line_edits._model_path == fake_path

    def test_select_model_calls_on_model_selection_changed(self, app_with_line_edits):
        """_select_model triggers _on_model_selection_changed after setting path."""
        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=("/models/llama.gguf", ""),
        ):
            with patch.object(
                app_with_line_edits,
                "_on_model_selection_changed",
            ) as mock_callback:
                app_with_line_edits._select_model()

                mock_callback.assert_called_once()

    def test_select_model_does_nothing_on_cancel(self, app_with_line_edits):
        """_select_model does nothing when the user cancels the dialog."""
        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=("", ""),
        ):
            app_with_line_edits._select_model()

        app_with_line_edits.model_path_edit.setProperty.assert_not_called()
        app_with_line_edits.model_path_edit.setText.assert_not_called()


class TestSelectMmproj:
    """Tests for _select_mmproj file dialog method.

    Target: main.py lines 781-797
    """

    def test_select_mmproj_sets_fullpath_on_mmproj_path_edit(self, app_with_line_edits):
        """_select_mmproj stores the full path as a custom property on mmproj_path_edit."""
        fake_path = "/models/multi-modal.gguf"

        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=(fake_path, ""),
        ):
            app_with_line_edits._select_mmproj()

        app_with_line_edits.mmproj_path_edit.setProperty.assert_called_once_with("fullPath", fake_path)

    def test_select_mmproj_sets_short_filename_on_mmproj_path_edit(self, app_with_line_edits):
        """_select_mmproj displays only the short filename in the line edit."""
        fake_path = "/models/multi-modal.gguf"

        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=(fake_path, ""),
        ):
            app_with_line_edits._select_mmproj()

        app_with_line_edits.mmproj_path_edit.setText.assert_called_once_with("multi-modal.gguf")

    def test_select_mmproj_stores_full_path_in_private_attribute(self, app_with_line_edits):
        """_select_mmproj stores the full path in _mmproj_path."""
        fake_path = "/models/multi-modal.gguf"

        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=(fake_path, ""),
        ):
            app_with_line_edits._select_mmproj()

        assert app_with_line_edits._mmproj_path == fake_path

    def test_select_mmproj_does_nothing_on_cancel(self, app_with_line_edits):
        """_select_mmproj does nothing when the user cancels the dialog."""
        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=("", ""),
        ):
            app_with_line_edits._select_mmproj()

        app_with_line_edits.mmproj_path_edit.setProperty.assert_not_called()
        app_with_line_edits.mmproj_path_edit.setText.assert_not_called()


class TestSelectDraftModel:
    """Tests for _select_draft_model file dialog method.

    Target: main.py lines 799-814
    """

    def test_select_draft_model_sets_fullpath_on_draft_model_line_edit(self, app_with_line_edits):
        """_select_draft_model stores the full path as a custom property on draft_model_line_edit."""
        fake_path = "/models/draft-model.gguf"

        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=(fake_path, ""),
        ):
            app_with_line_edits._select_draft_model()

        app_with_line_edits.draft_model_line_edit.setProperty.assert_called_once_with("fullPath", fake_path)

    def test_select_draft_model_sets_short_filename_on_draft_model_line_edit(self, app_with_line_edits):
        """_select_draft_model displays only the short filename in the line edit."""
        fake_path = "/models/draft-model.gguf"

        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=(fake_path, ""),
        ):
            app_with_line_edits._select_draft_model()

        app_with_line_edits.draft_model_line_edit.setText.assert_called_once_with("draft-model.gguf")

    def test_select_draft_model_does_nothing_on_cancel(self, app_with_line_edits):
        """_select_draft_model does nothing when the user cancels the dialog."""
        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=("", ""),
        ):
            app_with_line_edits._select_draft_model()

        app_with_line_edits.draft_model_line_edit.setProperty.assert_not_called()
        app_with_line_edits.draft_model_line_edit.setText.assert_not_called()


class TestSelectJsonSchema:
    """Tests for _select_json_schema file dialog method.

    Target: main.py lines 816-831
    """

    def test_select_json_schema_sets_fullpath_on_json_schema_line_edit(self, app_with_line_edits):
        """_select_json_schema stores the full path as a custom property on json_schema_line_edit."""
        fake_path = "/schemas/schema.json"

        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=(fake_path, ""),
        ):
            app_with_line_edits._select_json_schema()

        app_with_line_edits.json_schema_line_edit.setProperty.assert_called_once_with("fullPath", fake_path)

    def test_select_json_schema_sets_short_filename_on_json_schema_line_edit(self, app_with_line_edits):
        """_select_json_schema displays only the short filename in the line edit."""
        fake_path = "/schemas/schema.json"

        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=(fake_path, ""),
        ):
            app_with_line_edits._select_json_schema()

        app_with_line_edits.json_schema_line_edit.setText.assert_called_once_with("schema.json")

    def test_select_json_schema_does_nothing_on_cancel(self, app_with_line_edits):
        """_select_json_schema does nothing when the user cancels the dialog."""
        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=("", ""),
        ):
            app_with_line_edits._select_json_schema()

        app_with_line_edits.json_schema_line_edit.setProperty.assert_not_called()
        app_with_line_edits.json_schema_line_edit.setText.assert_not_called()


class TestOnModelSelectionChanged:
    """Tests for _on_model_selection_changed method.

    Target: main.py lines 833-837
    """

    def test_on_model_selection_changed_enables_launch_button_when_model_selected(self, app_with_line_edits):
        """_on_model_selection_changed enables the launch button when a model path exists."""
        app_with_line_edits.model_path_edit.property.return_value = "/models/llama.gguf"

        app_with_line_edits._on_model_selection_changed()

        app_with_line_edits.launch_button.setEnabled.assert_called_once_with(True)

    def test_on_model_selection_changed_disables_launch_button_when_no_model(self, app_with_line_edits):
        """_on_model_selection_changed disables the launch button when no model is selected."""
        app_with_line_edits.model_path_edit.property.return_value = None

        app_with_line_edits._on_model_selection_changed()

        app_with_line_edits.launch_button.setEnabled.assert_called_once_with(False)

    def test_on_model_selection_changed_disables_launch_button_when_process_running(self, app_with_line_edits):
        """_on_model_selection_changed disables the launch button when process is running."""
        from PySide6.QtCore import QProcess

        app_with_line_edits.model_path_edit.property.return_value = "/models/llama.gguf"
        app_with_line_edits._process.state.return_value = QProcess.Running  # type: ignore

        app_with_line_edits._on_model_selection_changed()

        app_with_line_edits.launch_button.setEnabled.assert_called_once_with(False)
