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


@pytest.mark.file_errors
def test_load_ui_raises_when_file_does_not_exist():
    """1.2.1: load_ui() raises RuntimeError when UI file does not exist.

    QFile.open() returns False for non-existent paths, triggering
    the RuntimeError at ui_loader.py L24-26.
    """
    with patch("ui_loader.QFile") as mock_qfile_cls:
        mock_qfile = MagicMock()
        mock_qfile_cls.return_value = mock_qfile
        mock_qfile.open.return_value = False

        parent = QWidget()

        with pytest.raises(RuntimeError, match="Cannot open UI file"):
            load_ui("/nonexistent/path.ui", parent)


@pytest.mark.file_errors
def test_load_ui_raises_when_file_open_fails():
    """1.2.2: load_ui() raises RuntimeError when UI file fails to open.

    Even when the path exists, opening may fail (e.g. permissions).
    QFile.open() returns False, triggering RuntimeError at L24-26.
    """
    with patch("ui_loader.QFile") as mock_qfile_cls:
        mock_qfile = MagicMock()
        mock_qfile_cls.return_value = mock_qfile
        mock_qfile.open.return_value = False

        parent = QWidget()

        with pytest.raises(RuntimeError, match="Cannot open UI file"):
            load_ui(Path("/restricted/path.ui"), parent)


@pytest.mark.file_errors
def test_load_ui_raises_when_file_is_invalid():
    """1.2.3: load_ui() raises RuntimeError when UI file is invalid/empty.

    QUiLoader.load() returns None for malformed XML, triggering
    the RuntimeError at ui_loader.py L31-32.
    """
    with patch("ui_loader.QFile") as mock_qfile_cls, patch("ui_loader.QUiLoader") as mock_loader_cls:
        mock_qfile = MagicMock()
        mock_qfile_cls.return_value = mock_qfile
        mock_qfile.open.return_value = True

        mock_loader = MagicMock()
        mock_loader_cls.return_value = mock_loader
        mock_loader.load.return_value = None

        parent = QWidget()

        with pytest.raises(RuntimeError, match="Failed to load UI file"):
            load_ui("/invalid/ui.ui", parent)


@pytest.mark.widget_assignment
def test_load_ui_assigns_widget_attributes_by_object_name():
    """1.2.4: load_ui() assigns widget attributes by objectName (QWidget).

    Widgets returned by findChildren(QWidget) with non-empty objectName
    are set as attributes on the parent widget.
    """
    with (
        patch("ui_loader.QFile") as mock_qfile_cls,
        patch("ui_loader.QUiLoader") as mock_loader_cls,
        patch("ui_loader.QVBoxLayout") as mock_vbox_cls,
    ):
        mock_qfile = MagicMock()
        mock_qfile_cls.return_value = mock_qfile
        mock_qfile.open.return_value = True

        # Create mock widgets with objectNames
        mock_button = MagicMock(spec=QWidget)
        mock_button.objectName.return_value = "myButton"

        mock_label = MagicMock(spec=QWidget)
        mock_label.objectName.return_value = "myLabel"

        mock_ui = MagicMock()
        mock_ui.findChildren.return_value = [mock_button, mock_label]
        mock_ui.layout.return_value = None
        mock_ui.windowTitle.return_value = ""
        mock_ui.size.return_value = QSize(0, 0)

        mock_loader_instance = mock_loader_cls.return_value
        mock_loader_instance.load.return_value = mock_ui

        parent = QWidget()
        load_ui("/test/ui.ui", parent)

        assert parent.myButton is mock_button
        assert parent.myLabel is mock_label


@pytest.mark.widget_assignment
def test_load_ui_assigns_layout_attributes_by_object_name():
    """1.2.5: load_ui() assigns layout attributes by objectName.

    Layouts returned by findChildren(QLayout) with non-empty objectName
    are set as attributes on the parent widget.
    """
    with (
        patch("ui_loader.QFile") as mock_qfile_cls,
        patch("ui_loader.QUiLoader") as mock_loader_cls,
        patch("ui_loader.QVBoxLayout") as mock_vbox_cls,
    ):
        mock_qfile = MagicMock()
        mock_qfile_cls.return_value = mock_qfile
        mock_qfile.open.return_value = True

        mock_layout = MagicMock(spec=QLayout)
        mock_layout.objectName.return_value = "mainLayout"

        mock_ui = MagicMock()

        def find_children(cls):
            if cls == QLayout:
                return [mock_layout]
            return []

        mock_ui.findChildren.side_effect = find_children
        mock_ui.layout.return_value = None
        mock_ui.windowTitle.return_value = ""
        mock_ui.size.return_value = QSize(0, 0)

        mock_loader_instance = mock_loader_cls.return_value
        mock_loader_instance.load.return_value = mock_ui

        parent = QWidget()
        load_ui("/test/ui.ui", parent)

        assert parent.mainLayout is mock_layout


@pytest.mark.widget_assignment
def test_load_ui_captures_top_level_layout_not_in_find_children():
    """1.2.6: load_ui() captures top-level layout when not found by findChildren.

    The main layout from loaded_ui.layout() is captured as an attribute
    when it has a name and isn't already set via findChildren.
    """
    with (
        patch("ui_loader.QFile") as mock_qfile_cls,
        patch("ui_loader.QUiLoader") as mock_loader_cls,
        patch("ui_loader.QVBoxLayout") as mock_vbox_cls,
    ):
        mock_qfile = MagicMock()
        mock_qfile_cls.return_value = mock_qfile
        mock_qfile.open.return_value = True

        mock_main_layout = MagicMock(spec=QLayout)
        mock_main_layout.objectName.return_value = "topLevelLayout"

        mock_ui = MagicMock()
        mock_ui.findChildren.return_value = []  # Not found by findChildren
        mock_ui.layout.return_value = mock_main_layout
        mock_ui.windowTitle.return_value = ""
        mock_ui.size.return_value = QSize(0, 0)

        mock_loader_instance = mock_loader_cls.return_value
        mock_loader_instance.load.return_value = mock_ui

        parent = QWidget()
        load_ui("/test/ui.ui", parent)

        assert parent.topLevelLayout is mock_main_layout


@pytest.mark.parent_type_setup
def test_load_ui_sets_up_dialog_correctly():
    """1.2.7: load_ui() sets up QDialog correctly (layout, title, size).

    When parent is a QDialog:
    - loaded_ui.layout() is set on the dialog
    - window title is applied from loaded_ui
    - size is applied from loaded_ui
    """
    with patch("ui_loader.QFile") as mock_qfile_cls, patch("ui_loader.QUiLoader") as mock_loader_cls:
        mock_qfile = MagicMock()
        mock_qfile_cls.return_value = mock_qfile
        mock_qfile.open.return_value = True

        mock_layout = MagicMock()
        mock_layout.objectName.return_value = ""  # skip top-level capture step

        mock_ui = MagicMock()
        mock_ui.layout.return_value = mock_layout
        mock_ui.windowTitle.return_value = "My Dialog"
        mock_ui.size.return_value = QSize(400, 300)

        mock_loader_instance = mock_loader_cls.return_value
        mock_loader_instance.load.return_value = mock_ui

        parent = QDialog()
        parent.setLayout = MagicMock()
        parent.setWindowTitle = MagicMock()
        parent.resize = MagicMock()
        load_ui("/test/dialog.ui", parent)

        parent.setLayout.assert_called_with(mock_layout)
        parent.setWindowTitle.assert_called_with("My Dialog")
        parent.resize.assert_called_with(QSize(400, 300))


@pytest.mark.parent_type_setup
def test_load_ui_sets_up_main_window_correctly():
    """1.2.8: load_ui() sets up QMainWindow correctly (central widget, title, size).

    When parent is a QMainWindow:
    - loaded_ui becomes the central widget
    - window title is applied from loaded_ui
    - size is applied from loaded_ui
    """
    with patch("ui_loader.QFile") as mock_qfile_cls, patch("ui_loader.QUiLoader") as mock_loader_cls:
        mock_qfile = MagicMock()
        mock_qfile_cls.return_value = mock_qfile
        mock_qfile.open.return_value = True

        mock_ui = MagicMock()
        mock_ui.layout.return_value = None
        mock_ui.windowTitle.return_value = "My Window"
        mock_ui.size.return_value = QSize(800, 600)

        mock_loader_instance = mock_loader_cls.return_value
        mock_loader_instance.load.return_value = mock_ui

        parent = QMainWindow()
        parent.setCentralWidget = MagicMock()
        parent.setWindowTitle = MagicMock()
        parent.resize = MagicMock()
        load_ui("/test/window.ui", parent)

        parent.setCentralWidget.assert_called_with(mock_ui)
        parent.setWindowTitle.assert_called_with("My Window")
        parent.resize.assert_called_with(QSize(800, 600))


@pytest.mark.parent_type_setup
def test_load_ui_embeds_widget_via_zero_margin_layout():
    """1.2.9: load_ui() embeds QWidget via zero-margin layout for non-dialog/mainwindow parents.

    When parent is a plain QWidget (not QDialog or QMainWindow):
    - QVBoxLayout is created with parent and zero contents margins
    - loaded_ui is added to that layout
    - window title and size are applied from loaded_ui
    """
    with (
        patch("ui_loader.QFile") as mock_qfile_cls,
        patch("ui_loader.QUiLoader") as mock_loader_cls,
        patch("ui_loader.QVBoxLayout") as mock_vbox_cls,
    ):
        mock_qfile = MagicMock()
        mock_qfile_cls.return_value = mock_qfile
        mock_qfile.open.return_value = True

        mock_ui = MagicMock()
        mock_ui.layout.return_value = None
        mock_ui.windowTitle.return_value = "Embedded UI"
        mock_ui.size.return_value = QSize(300, 200)

        mock_loader_instance = mock_loader_cls.return_value
        mock_loader_instance.load.return_value = mock_ui

        mock_container = MagicMock()
        mock_vbox_cls.return_value = mock_container

        parent = QWidget()
        parent.setWindowTitle = MagicMock()
        parent.resize = MagicMock()
        load_ui("/test/embed.ui", parent)

        mock_vbox_cls.assert_called_with(parent)
        mock_container.setContentsMargins.assert_called_with(0, 0, 0, 0)
        mock_container.addWidget.assert_called_with(mock_ui)
        parent.setWindowTitle.assert_called_with("Embedded UI")
        parent.resize.assert_called_with(QSize(300, 200))


@pytest.mark.path_support
def test_load_ui_accepts_path_object():
    """1.2.10: load_ui() accepts both str and Path for ui_file_path.

    The function should work with pathlib.Path objects as well as strings,
    passing them through to QFile constructor unchanged.
    """
    with (
        patch("ui_loader.QFile") as mock_qfile_cls,
        patch("ui_loader.QUiLoader") as mock_loader_cls,
        patch("ui_loader.QVBoxLayout") as mock_vbox_cls,
    ):
        mock_qfile = MagicMock()
        mock_qfile_cls.return_value = mock_qfile
        mock_qfile.open.return_value = True

        mock_ui = MagicMock()
        mock_ui.layout.return_value = None
        mock_ui.windowTitle.return_value = ""
        mock_ui.size.return_value = QSize(0, 0)

        mock_loader = MagicMock()
        mock_loader.load.return_value = mock_ui
        mock_loader_cls.return_value = mock_loader

        parent = QWidget()
        result = load_ui(Path("/test/path.ui"), parent)

        # Verify QFile was called with the Path object
        mock_qfile_cls.assert_called_with(Path("/test/path.ui"))
        assert result is mock_ui
