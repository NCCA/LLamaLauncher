"""Phase 6: Tests for initialization and lifecycle methods."""

import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Import production modules from project root in tests
_project_root = str(Path(__file__).resolve().parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)


class _QtSignal:
    """Minimal simulation of a Qt signal for testing.

    Supports both connection verification (via recorded calls) and
    signal emission to verify that connected slots are invoked.
    """

    def __init__(self):
        self._callbacks = []
        self.connect = MagicMock()
        self.connect.side_effect = self._record_connect

    def _record_connect(self, callback):
        self._callbacks.append(callback)
        return callback

    def emit(self, *args, **kwargs):
        """Emit the signal, invoking all connected slots."""
        for callback in self._callbacks:
            callback(*args, **kwargs)


class _MockWidget:
    """Minimal mock widget with QtSignal-based signals."""

    def __init__(self):
        self.clicked = _QtSignal()
        self.textChanged = _QtSignal()


@pytest.fixture()
def temp_dir():
    """Provide temporary cleaned up directory.

    Returns a Path to a temporary directory that removes itself afterward.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


class TestCreateCacheDir:
    """Test _create_cache_dir creates cache directory and returns Path."""

    def test_6_1_creates_cache_directory_and_returns_path(self, qapp):
        """_create_cache_dir creates the cache directory on disk and returns it as a Path.

        The returned path should exist and be a valid directory.
        """
        from main import LlamaLaunchApp

        app = LlamaLaunchApp(host="127.0.0.1", port=8080)

        assert isinstance(app._cache_dir, Path)
        assert app._cache_dir.exists()
        assert app._cache_dir.is_dir()
        assert "llama-launcher" in str(app._cache_dir)


class TestSaveConfig:
    """Test _save_config behavior."""

    def test_6_8_calls_save_config_as_when_no_last_config_path(self, qapp):
        """_save_config calls _save_config_as when _last_config_path does not exist.

        When there is no previously saved config path, save should prompt
        the user for a location via _save_config_as.
        """
        from main import LlamaLaunchApp

        app = LlamaLaunchApp(host="127.0.0.1", port=8080)
        app._save_config_as = MagicMock()
        app._write_config_file = MagicMock()

        assert not hasattr(app, "_last_config_path")
        app._save_config()

        app._save_config_as.assert_called_once()
        app._write_config_file.assert_not_called()

    def test_6_9_writes_to_last_saved_path_when_exists(self, qapp):
        """_save_config writes to _last_config_path when it exists.

        When a previous config path is available, save should write directly
        to that path without prompting.
        """
        from main import LlamaLaunchApp

        app = LlamaLaunchApp(host="127.0.0.1", port=8080)
        app._last_config_path = Path("/tmp/test-config.json")
        app._save_config_as = MagicMock()
        app._write_config_file = MagicMock()

        app._save_config()

        app._write_config_file.assert_called_once_with(app._last_config_path)
        app._save_config_as.assert_not_called()


class TestSaveLastSession:
    """Test _save_last_session saves settings to QSettings."""

    def test_6_11_saves_model_path_host_port_and_geometry(self, qapp):
        """_save_last_session saves model path, host, port, and window geometry.

        All four values should be written to QSettings with the correct keys.
        """
        from main import LlamaLaunchApp

        # Mock QSettings: configure value() for _load_last_session (called in __init__)
        # and capture setValue() calls from _save_last_session
        mock_settings_instance = MagicMock()
        mock_settings_instance.value.return_value = None  # no saved geometry

        with patch("main.QSettings", return_value=mock_settings_instance):
            app = LlamaLaunchApp(host="127.0.0.1", port=8080)

            # Configure widget mocks with expected values
            app.model_path_edit = MagicMock()
            app.model_path_edit.property.return_value = "/models/test.gguf"
            app.host_line_edit = MagicMock()
            app.host_line_edit.text.return_value = "192.168.1.100"
            app.port_line_edit = MagicMock()
            app.port_line_edit.text.return_value = "9000"
            app.saveGeometry = MagicMock(return_value=b"geometry-data")

            app._save_last_session()

            # Verify all four values were saved
            calls = mock_settings_instance.setValue.call_args_list
            assert len(calls) == 4

            call_keys = {call[0][0] for call in calls}
            assert "lastModelPath" in call_keys
            assert "host" in call_keys
            assert "port" in call_keys
            assert "windowGeometry" in call_keys

            # Verify specific values
            mock_settings_instance.setValue.assert_any_call("lastModelPath", "/models/test.gguf")
            mock_settings_instance.setValue.assert_any_call("host", "192.168.1.100")
            mock_settings_instance.setValue.assert_any_call("port", "9000")
            mock_settings_instance.setValue.assert_any_call("windowGeometry", b"geometry-data")

    def test_6_11_saves_empty_model_path_when_none(self, qapp):
        """_save_last_session saves empty string when model path is None.

        If the model path property returns None, an empty string should be saved.
        """
        from main import LlamaLaunchApp

        mock_settings_instance = MagicMock()
        mock_settings_instance.value.return_value = None  # no saved geometry
        with patch("main.QSettings", return_value=mock_settings_instance):
            app = LlamaLaunchApp(host="127.0.0.1", port=8080)

            app.model_path_edit = MagicMock()
            app.model_path_edit.property.return_value = None
            app.host_line_edit = MagicMock()
            app.host_line_edit.text.return_value = "127.0.0.1"
            app.port_line_edit = MagicMock()
            app.port_line_edit.text.return_value = "8080"
            app.saveGeometry = MagicMock(return_value=b"")

            app._save_last_session()

            mock_settings_instance.setValue.assert_any_call("lastModelPath", "")


class TestCloseEvent:
    """Test closeEvent lifecycle behavior."""

    def test_6_14_calls_save_last_session_before_closing(self, qapp):
        """closeEvent calls _save_last_session before delegating to parent.

        The session must be saved before the window closes so settings
        are persisted on disk.
        """
        from PySide6.QtGui import QCloseEvent

        from main import LlamaLaunchApp

        app = LlamaLaunchApp(host="127.0.0.1", port=8080)
        app._save_last_session = MagicMock()

        close_event = QCloseEvent()
        app.closeEvent(close_event)

        app._save_last_session.assert_called_once()
        # super().closeEvent() accepts the event by default
        assert close_event.isAccepted()


class TestCreateFileMenu:
    """Test _create_file_menu creates File menu with correct actions."""

    def test_6_7_creates_file_menu_with_save_save_as_load_actions(self, qapp):
        """_create_file_menu creates a File menu with Save, Save As, and Load actions.

        The File menu should be added to the menu bar and contain three actions
        that are connected to their respective slot methods.
        """
        from main import LlamaLaunchApp

        app = LlamaLaunchApp(host="127.0.0.1", port=8080)

        # Verify the File menu exists in the menu bar
        # QMenuBar.actions() returns QActions that represent menus
        file_menu = None
        for action in app.menuBar().actions():
            menu = action.menu()
            if menu is not None and "File" in menu.title():
                file_menu = menu
                break

        assert file_menu is not None, "File menu should exist in menu bar"

        # Verify the menu has three actions
        actions = file_menu.actions()
        assert len(actions) == 3

        action_texts = [action.text() for action in actions]
        assert any("Save Configuration" in text for text in action_texts)
        assert any("Save As" in text for text in action_texts)
        assert any("Load Configuration" in text for text in action_texts)

    def test_6_7_save_action_connected_to_save_config(self, qapp):
        """The Save action is connected to _save_config method."""
        from main import LlamaLaunchApp

        app = LlamaLaunchApp(host="127.0.0.1", port=8080)
        app._save_config = MagicMock()

        # Find and trigger the Save action in File menu
        for action in app.menuBar().actions():
            menu = action.menu()
            if menu is not None and "File" in menu.title():
                for submenu_action in menu.actions():
                    if "Save Configuration" in submenu_action.text():
                        submenu_action.trigger()
                        break
                break

        app._save_config.assert_called_once()

    def test_6_7_load_action_connected_to_load_config(self, qapp):
        """The Load action is connected to _load_config method."""
        from main import LlamaLaunchApp

        app = LlamaLaunchApp(host="127.0.0.1", port=8080)
        app._load_config = MagicMock()

        # Find and trigger the Load action in File menu
        for action in app.menuBar().actions():
            menu = action.menu()
            if menu is not None and "File" in menu.title():
                for submenu_action in menu.actions():
                    if "Load Configuration" in submenu_action.text():
                        submenu_action.trigger()
                        break
                break

        app._load_config.assert_called_once()


class TestLoadLastSession:
    """Test _load_last_session restores settings from QSettings."""

    def test_6_12_restores_host_port_and_model_path(self, qapp):
        """_load_last_session restores host, port, and model path from QSettings.

        When values are saved in QSettings, they should be restored to the
        corresponding UI widgets on application startup.
        """
        from main import LlamaLaunchApp

        # Mock QSettings to return saved values
        mock_settings_instance = MagicMock()
        mock_settings_instance.value.side_effect = lambda key, default="": {
            "windowGeometry": None,
            "host": "192.168.1.50",
            "port": "9999",
            "lastModelPath": "/models/previously-used.gguf",
        }.get(key, default)

        with patch("main.QSettings", return_value=mock_settings_instance):
            app = LlamaLaunchApp(host="127.0.0.1", port=8080)

            # Replace widgets with mocks to verify setText calls
            app.host_line_edit = MagicMock()
            app.port_line_edit = MagicMock()
            app.model_path_edit = MagicMock()
            app._set_path_field = MagicMock()

            # Re-run _load_last_session with the mocked widgets
            app._load_last_session()

            # Verify host and port were set
            app.host_line_edit.setText.assert_called_with("192.168.1.50")
            app.port_line_edit.setText.assert_called_with("9999")

            # Verify model path was restored via _set_path_field
            app._set_path_field.assert_called_once_with(app.model_path_edit, "/models/previously-used.gguf")

    def test_6_12_uses_defaults_when_no_saved_values(self, qapp):
        """_load_last_session uses default values when nothing is saved.

        When QSettings has no saved values, the method should use the
        hardcoded defaults (host=127.0.0.1, port=8080).
        """
        from main import LlamaLaunchApp

        # Mock QSettings to return None for keys with no saved data,
        # but respect default parameters for host/port lookups
        mock_settings_instance = MagicMock()

        def mock_value(key, default=""):
            # No saved data, so always return the default
            return default

        mock_settings_instance.value.side_effect = mock_value

        with patch("main.QSettings", return_value=mock_settings_instance):
            app = LlamaLaunchApp(host="127.0.0.1", port=8080)

            # Replace widgets with mocks to verify setText calls
            app.host_line_edit = MagicMock()
            app.port_line_edit = MagicMock()
            app.model_path_edit = MagicMock()
            app._set_path_field = MagicMock()

            app._load_last_session()

            # Verify defaults were used
            app.host_line_edit.setText.assert_called_with("127.0.0.1")
            app.port_line_edit.setText.assert_called_with("8080")

            # Model path should not be set when empty
            app._set_path_field.assert_not_called()


class TestSetupContextSizeCombo:
    """Test _setup_context_size_combo populates combobox with options."""

    def test_6_4_populates_all_8_context_size_options(self, qapp):
        """_setup_context_size_combo populates the combobox with 8 context size options.

        Each option should have a display name, numeric value in user data role,
        and a tooltip.
        """
        from PySide6.QtCore import Qt

        from main import LlamaLaunchApp

        app = LlamaLaunchApp(host="127.0.0.1", port=8080)

        # Verify 8 options were added
        combo = app.model_context_size
        assert combo.count() == 8

        # Verify expected display names and values
        expected_options = [
            ("Auto (model default)", 0),
            ("2K", 2048),
            ("4K", 4096),
            ("8K", 8192),
            ("16K", 16384),
            ("32K", 32768),
            ("64K", 65536),
            ("128K", 131072),
        ]

        for i, (display_name, value) in enumerate(expected_options):
            assert combo.itemText(i) == display_name
            assert int(combo.itemData(i, Qt.UserRole)) == value

        # Verify tooltips are set
        for i in range(combo.count()):
            tooltip = combo.itemData(i, Qt.ToolTipRole)
            assert tooltip is not None
            assert len(str(tooltip)) > 0

    def test_6_5_pre_selects_from_cli_ctx_size(self, qapp):
        """_setup_context_size_combo pre-selects the option matching CLI ctx_size.

        When _ctx_size is provided during initialization, the combobox should
        select the matching option.
        """
        from PySide6.QtCore import Qt

        from main import LlamaLaunchApp

        # Create app with ctx_size=8192 (8K option)
        app = LlamaLaunchApp(host="127.0.0.1", port=8080, ctx_size=8192)

        combo = app.model_context_size
        # 8K is the 4th option (index 3)
        assert combo.currentIndex() == 3
        assert int(combo.itemData(combo.currentIndex(), Qt.UserRole)) == 8192

    def test_6_6_defaults_to_16k_when_no_ctx_size(self, qapp):
        """_setup_context_size_combo defaults to 16K when no CLI ctx_size provided.

        When _ctx_size is None, the combobox should default to 16K (16384).
        """
        from PySide6.QtCore import Qt

        from main import LlamaLaunchApp

        # Create app without ctx_size (defaults to None)
        app = LlamaLaunchApp(host="127.0.0.1", port=8080)

        combo = app.model_context_size
        # 16K is the 5th option (index 4)
        assert combo.currentIndex() == 4
        assert int(combo.itemData(combo.currentIndex(), Qt.UserRole)) == 16384


class TestConnectSignals:
    """Test _connect_signals wires up widget signals to slot methods."""

    def test_6_15_wires_up_all_button_clicks_and_signals(self, qapp):
        """_connect_signals connects all widget signals to their slot methods.

        Each button's clicked signal and the model path edit's textChanged signal
        should be connected to their respective handler methods.
        """
        from main import LlamaLaunchApp

        # Create a mock app with mock widgets and mock slots
        app = MagicMock(spec=LlamaLaunchApp)

        # Set up mock widgets with MagicMock signals
        app.select_model_button = MagicMock()
        app.select_mmproj_button = MagicMock()
        app.select_draft_model_button = MagicMock()
        app.select_json_schema_button = MagicMock()
        app.model_path_edit = MagicMock()
        app.launch_button = MagicMock()

        # Set up mock slot methods
        app._select_model = MagicMock()
        app._select_mmproj = MagicMock()
        app._select_draft_model = MagicMock()
        app._select_json_schema = MagicMock()
        app._on_model_selection_changed = MagicMock()
        app._toggle_launch = MagicMock()

        # Call _connect_signals (bound to the mock instance)
        LlamaLaunchApp._connect_signals(app)

        # Verify each signal was connected to its slot
        app.select_model_button.clicked.connect.assert_called_once_with(app._select_model)
        app.select_mmproj_button.clicked.connect.assert_called_once_with(app._select_mmproj)
        app.select_draft_model_button.clicked.connect.assert_called_once_with(app._select_draft_model)
        app.select_json_schema_button.clicked.connect.assert_called_once_with(app._select_json_schema)
        app.model_path_edit.textChanged.connect.assert_called_once_with(app._on_model_selection_changed)
        app.launch_button.clicked.connect.assert_called_once_with(app._toggle_launch)

    def test_6_15_signals_trigger_correct_slots(self, qapp):
        """Triggered signals call the correct slot methods.

        When a widget signal is emitted (e.g., button clicked), the connected
        slot method should be invoked.
        """
        from main import LlamaLaunchApp

        # Create a mock app with mock widgets and mock slots
        app = MagicMock(spec=LlamaLaunchApp)

        # Set up ALL mock widgets (required by _connect_signals)
        app.select_model_button = _MockWidget()
        app.select_mmproj_button = _MockWidget()
        app.select_draft_model_button = _MockWidget()
        app.select_json_schema_button = _MockWidget()
        app.model_path_edit = _MockWidget()
        app.launch_button = _MockWidget()

        # Set up mock slot methods
        app._select_model = MagicMock()
        app._select_mmproj = MagicMock()
        app._select_draft_model = MagicMock()
        app._select_json_schema = MagicMock()
        app._on_model_selection_changed = MagicMock()
        app._toggle_launch = MagicMock()

        # Connect signals to slots
        LlamaLaunchApp._connect_signals(app)

        # Emit specific signals
        app.select_model_button.clicked.emit()
        app.launch_button.clicked.emit()

        # Verify only the triggered slots were called
        app._select_model.assert_called_once()
        app._toggle_launch.assert_called_once()
        # Other slots should not have been called
        app._select_mmproj.assert_not_called()
        app._select_draft_model.assert_not_called()
        app._select_json_schema.assert_not_called()
        app._on_model_selection_changed.assert_not_called()
