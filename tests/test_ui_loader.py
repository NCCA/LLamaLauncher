"""Tests for ui_loader.load_ui().

Covers error handling, widget attribute assignment, parent type setup,
and path type support.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QDialog, QLayout, QMainWindow, QWidget

from ui_loader import load_ui


@pytest.fixture
def mock_file_open_failure():
    """1.2.1/1.2.2: Patch QFile to simulate open() failure.

    Returns the patched QFile class mock for tests that expect
    RuntimeError when the UI file cannot be opened.
    """
    with patch("ui_loader.QFile") as mock_qfile_cls:
        mock_qfile = MagicMock()
        mock_qfile_cls.return_value = mock_qfile
        mock_qfile.open.return_value = False
        yield mock_qfile_cls


@pytest.fixture
def mock_qt():
    """Module-level fixture for successful UI loading scenarios.

    Patches QFile, QUiLoader, and QVBoxLayout, then yields a factory
    function that creates fresh mock instances per test. This ensures
    each test gets isolated mocks with no shared mutable state.

    Yields:
        make_mocks: callable that returns a namespace with:
            - mock_qfile_cls: the patched QFile class mock
            - mock_loader_cls: the patched QUiLoader class mock
            - mock_vbox_cls: the patched QVBoxLayout class mock
            - mock_ui: a fresh MagicMock for the loaded UI
            - mock_loader: a fresh QUiLoader instance mock
            - mock_container: a fresh QVBoxLayout instance mock
    """
    with (
        patch("ui_loader.QFile") as mock_qfile_cls,
        patch("ui_loader.QUiLoader") as mock_loader_cls,
        patch("ui_loader.QVBoxLayout") as mock_vbox_cls,
    ):

        def make_mocks():
            """Create a fresh set of mock instances for one test."""
            mock_qfile = MagicMock()
            mock_qfile_cls.return_value = mock_qfile
            mock_qfile.open.return_value = True

            mock_ui = MagicMock()
            mock_ui.layout.return_value = None
            mock_ui.windowTitle.return_value = ""
            mock_ui.size.return_value = QSize(0, 0)

            mock_loader = mock_loader_cls.return_value
            mock_loader.load.return_value = mock_ui

            mock_container = mock_vbox_cls.return_value

            return MagicMock(
                mock_qfile_cls=mock_qfile_cls,
                mock_loader_cls=mock_loader_cls,
                mock_vbox_cls=mock_vbox_cls,
                mock_ui=mock_ui,
                mock_loader=mock_loader,
                mock_container=mock_container,
            )

        yield make_mocks


class TestLoadUIFileErrors:
    """1.2.1-1.2.3: Error handling when UI files cannot be loaded."""

    def test_load_ui_raises_when_file_does_not_exist(self, mock_file_open_failure):
        """1.2.1: load_ui() raises RuntimeError when UI file does not exist."""
        parent = QWidget()
        with pytest.raises(RuntimeError, match="Cannot open UI file"):
            load_ui("/nonexistent/path.ui", parent)

    def test_load_ui_raises_when_file_open_fails(self, mock_file_open_failure):
        """1.2.2: load_ui() raises RuntimeError when UI file fails to open."""
        parent = QWidget()
        with pytest.raises(RuntimeError, match="Cannot open UI file"):
            load_ui(Path("/restricted/path.ui"), parent)

    def test_load_ui_raises_when_file_is_invalid(self, mock_qt):
        """1.2.3: load_ui() raises RuntimeError when UI file is invalid/empty."""
        mocks = mock_qt()
        mocks.mock_loader.load.return_value = None

        parent = QWidget()
        with pytest.raises(RuntimeError, match="Failed to load UI file"):
            load_ui("/invalid/ui.ui", parent)


class TestLoadUIWidgetAttributeAssignment:
    """1.2.4-1.2.6: Widget and layout attribute assignment by objectName."""

    def test_load_ui_assigns_widget_attributes_by_object_name(self, mock_qt):
        """1.2.4: load_ui() assigns widget attributes by objectName (QWidget)."""
        mocks = mock_qt()

        mock_button = MagicMock(spec=QWidget)
        mock_button.objectName.return_value = "myButton"

        mock_label = MagicMock(spec=QWidget)
        mock_label.objectName.return_value = "myLabel"

        mocks.mock_ui.findChildren.return_value = [mock_button, mock_label]

        parent = QWidget()
        load_ui("/test/ui.ui", parent)

        assert parent.myButton is mock_button
        assert parent.myLabel is mock_label

    def test_load_ui_assigns_layout_attributes_by_object_name(self, mock_qt):
        """1.2.5: load_ui() assigns layout attributes by objectName."""
        mocks = mock_qt()

        mock_layout = MagicMock(spec=QLayout)
        mock_layout.objectName.return_value = "mainLayout"

        def find_children(cls):
            if cls == QLayout:
                return [mock_layout]
            return []

        mocks.mock_ui.findChildren.side_effect = find_children

        parent = QWidget()
        load_ui("/test/ui.ui", parent)

        assert parent.mainLayout is mock_layout

    def test_load_ui_captures_top_level_layout_not_in_find_children(self, mock_qt):
        """1.2.6: load_ui() captures top-level layout when not found by findChildren."""
        mocks = mock_qt()

        mock_main_layout = MagicMock(spec=QLayout)
        mock_main_layout.objectName.return_value = "topLevelLayout"

        mocks.mock_ui.findChildren.return_value = []
        mocks.mock_ui.layout.return_value = mock_main_layout

        parent = QWidget()
        load_ui("/test/ui.ui", parent)

        assert parent.topLevelLayout is mock_main_layout


class TestLoadUISetupByParentType:
    """1.2.7-1.2.9: Widget setup for different parent widget types."""

    def test_load_ui_sets_up_dialog_correctly(self, mock_qt):
        """1.2.7: load_ui() sets up QDialog correctly (layout, title, size)."""
        mocks = mock_qt()

        mock_layout = MagicMock()
        mock_layout.objectName.return_value = ""

        mocks.mock_ui.layout.return_value = mock_layout
        mocks.mock_ui.windowTitle.return_value = "My Dialog"
        mocks.mock_ui.size.return_value = QSize(400, 300)

        parent = QDialog()
        parent.setLayout = MagicMock()
        parent.setWindowTitle = MagicMock()
        parent.resize = MagicMock()
        load_ui("/test/dialog.ui", parent)

        parent.setLayout.assert_called_with(mock_layout)
        parent.setWindowTitle.assert_called_with("My Dialog")
        parent.resize.assert_called_with(QSize(400, 300))

    def test_load_ui_sets_up_main_window_correctly(self, mock_qt):
        """1.2.8: load_ui() sets up QMainWindow correctly (central widget, title, size)."""
        mocks = mock_qt()

        mocks.mock_ui.windowTitle.return_value = "My Window"
        mocks.mock_ui.size.return_value = QSize(800, 600)

        parent = QMainWindow()
        parent.setCentralWidget = MagicMock()
        parent.setWindowTitle = MagicMock()
        parent.resize = MagicMock()
        load_ui("/test/window.ui", parent)

        parent.setCentralWidget.assert_called_with(mocks.mock_ui)
        parent.setWindowTitle.assert_called_with("My Window")
        parent.resize.assert_called_with(QSize(800, 600))

    def test_load_ui_embeds_widget_via_zero_margin_layout(self, mock_qt):
        """1.2.9: load_ui() embeds QWidget via zero-margin layout."""
        mocks = mock_qt()

        mocks.mock_ui.windowTitle.return_value = "Embedded UI"
        mocks.mock_ui.size.return_value = QSize(300, 200)

        parent = QWidget()
        parent.setWindowTitle = MagicMock()
        parent.resize = MagicMock()
        load_ui("/test/embed.ui", parent)

        mocks.mock_vbox_cls.assert_called_with(parent)
        mocks.mock_container.setContentsMargins.assert_called_with(0, 0, 0, 0)
        mocks.mock_container.addWidget.assert_called_with(mocks.mock_ui)
        parent.setWindowTitle.assert_called_with("Embedded UI")
        parent.resize.assert_called_with(QSize(300, 200))


class TestLoadUIPathSupport:
    """1.2.10: Path type acceptance."""

    def test_load_ui_accepts_path_object(self, mock_qt):
        """1.2.10: load_ui() accepts both str and Path for ui_file_path."""
        mocks = mock_qt()

        parent = QWidget()
        result = load_ui(Path("/test/path.ui"), parent)

        mocks.mock_qfile_cls.assert_called_with(Path("/test/path.ui"))
        assert result is mocks.mock_ui
