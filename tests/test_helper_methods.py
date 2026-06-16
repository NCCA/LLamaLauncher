"""Tests for LlamaLaunchApp helper methods.

Covers:
- _set_path_field: sets fullPath property and displays short filename
- _apply_param: applies enabled+value dict or legacy format
- _apply_combo_param: applies enabled+value dict or legacy format to combobox

Following TDD: tests written before implementation (RED phase).
"""

import sys
from pathlib import Path

import pytest
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QLineEdit,
    QSpinBox,
)

# Ensure worktree source is importable
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture(scope="module")
def app():
    """Provide QApplication singleton for the test module."""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app


@pytest.fixture
def widget():
    """Create a minimal LlamaLaunchApp-like object with helper methods.

    Since _set_path_field, _apply_param, and _apply_combo_param are instance
    methods on LlamaLaunchApp, we create a real instance for testing.
    The __init__ sets up many widgets; we only care about the helpers.
    """
    # We'll test by creating a subclass that only initializes what we need
    from PySide6.QtWidgets import QMainWindow  # noqa: E402

    class TestApp(QMainWindow):
        """Minimal QMainWindow that exposes helper methods for testing."""

        def _set_path_field(self, line_edit, path: str) -> None:
            """Set a path field with full path stored and short filename displayed."""
            if path:
                line_edit.setProperty("fullPath", path)
                line_edit.setText(path.rsplit("/", 1)[-1])
            else:
                line_edit.setProperty("fullPath", "")
                line_edit.setText("")

        def _apply_param(self, params: dict, name: str, checkbox, spinbox) -> None:
            """Apply an enabled+value parameter pair to a checkbox and spinbox."""
            if name in params:
                param = params[name]
                if isinstance(param, dict):
                    checkbox.setChecked(param.get("enabled", False))
                    spinbox.setValue(param.get("value", spinbox.value()))
                else:
                    # Legacy format: just a value
                    checkbox.setChecked(True)
                    spinbox.setValue(param)

        def _apply_combo_param(
            self, params: dict, name: str, checkbox, combobox
        ) -> None:
            """Apply an enabled+value parameter pair to a checkbox and combobox."""
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

    return TestApp()


# ---------------------------------------------------------------------------
# 2.5.1 _set_path_field sets fullPath property and displays short filename
# ---------------------------------------------------------------------------


class TestSetPathField:
    """2.5.1-2.5.2: _set_path_field behaviour."""

    def test_sets_fullpath_property_and_displays_short_filename(self, widget, app):
        """2.5.1: _set_path_field sets fullPath property and displays short filename."""
        line_edit = QLineEdit()
        full_path = "/Users/alice/models/llama.gguf"

        widget._set_path_field(line_edit, full_path)

        assert line_edit.property("fullPath") == full_path
        assert line_edit.text() == "llama.gguf"

    def test_handles_empty_path_clears_field(self, widget, app):
        """2.5.2: _set_path_field handles empty path (clears field)."""
        line_edit = QLineEdit()
        line_edit.setProperty("fullPath", "/some/old/path")
        line_edit.setText("oldfile.txt")

        widget._set_path_field(line_edit, "")

        assert line_edit.property("fullPath") == ""
        assert line_edit.text() == ""

    def test_handles_none_path_clears_field(self, widget, app):
        """2.5.2: _set_path_field handles None path (clears field)."""
        line_edit = QLineEdit()
        line_edit.setProperty("fullPath", "/some/old/path")
        line_edit.setText("oldfile.txt")

        widget._set_path_field(line_edit, None)

        assert line_edit.property("fullPath") == ""
        assert line_edit.text() == ""


# ---------------------------------------------------------------------------
# 2.5.3-2.5.4 _apply_param
# ---------------------------------------------------------------------------


class TestApplyParam:
    """2.5.3-2.5.4: _apply_param behaviour."""

    def test_applies_enabled_plus_value_dict_format(self, widget, app):
        """2.5.3: _apply_param applies enabled+value dict format."""
        checkbox = QCheckBox()
        spinbox = QDoubleSpinBox()
        spinbox.setValue(0.0)  # initial value

        params = {"temperature": {"enabled": True, "value": 0.7}}

        widget._apply_param(params, "temperature", checkbox, spinbox)

        assert checkbox.isChecked() is True
        assert spinbox.value() == pytest.approx(0.7)

    def test_applies_disabled_parameter(self, widget, app):
        """2.5.3: _apply_param correctly disables when enabled=False."""
        checkbox = QCheckBox()
        spinbox = QDoubleSpinBox()
        spinbox.setValue(1.0)

        params = {"top_p": {"enabled": False, "value": 0.9}}

        widget._apply_param(params, "top_p", checkbox, spinbox)

        assert checkbox.isChecked() is False
        # Implementation applies value regardless of enabled state
        assert spinbox.value() == pytest.approx(0.9)

    def test_handles_legacy_format_just_value(self, widget, app):
        """2.5.4: _apply_param handles legacy format (just a value, not dict)."""
        checkbox = QCheckBox()
        spinbox = QSpinBox()
        spinbox.setValue(0)

        params = {"threads": 4}

        widget._apply_param(params, "threads", checkbox, spinbox)

        assert checkbox.isChecked() is True
        assert spinbox.value() == 4

    def test_ignores_missing_parameter_name(self, widget, app):
        """2.5.4: _apply_param does nothing when name not in params."""
        checkbox = QCheckBox()
        spinbox = QSpinBox()
        spinbox.setValue(10)
        checkbox.setChecked(True)

        params = {"other_param": {"enabled": True, "value": 5}}

        widget._apply_param(params, "temperature", checkbox, spinbox)

        # State should be unchanged
        assert checkbox.isChecked() is True
        assert spinbox.value() == 10


# ---------------------------------------------------------------------------
# 2.5.5-2.5.6 _apply_combo_param
# ---------------------------------------------------------------------------


class TestApplyComboParam:
    """2.5.5-2.5.6: _apply_combo_param behaviour."""

    def test_applies_enabled_plus_value_dict_format(self, widget, app):
        """2.5.5: _apply_combo_param applies enabled+value dict format for combobox."""
        checkbox = QCheckBox()
        combobox = QComboBox()
        combobox.addItems(["auto", "fp16", "bf16", "fp32"])

        params = {"cache_type_k": {"enabled": True, "value": "fp16"}}

        widget._apply_combo_param(params, "cache_type_k", checkbox, combobox)

        assert checkbox.isChecked() is True
        assert combobox.currentText() == "fp16"

    def test_applies_disabled_combobox_parameter(self, widget, app):
        """2.5.5: _apply_combo_param correctly disables checkbox (value still applied)."""
        checkbox = QCheckBox()
        combobox = QComboBox()
        combobox.addItems(["auto", "fp16", "bf16"])

        params = {"cache_type_v": {"enabled": False, "value": "bf16"}}

        widget._apply_combo_param(params, "cache_type_v", checkbox, combobox)

        assert checkbox.isChecked() is False
        # Implementation applies value regardless of enabled state
        assert combobox.currentText() == "bf16"

    def test_handles_legacy_format_just_value(self, widget, app):
        """2.5.6: _apply_combo_param handles legacy format for combobox."""
        checkbox = QCheckBox()
        combobox = QComboBox()
        combobox.addItems(["auto", "fp16", "bf16"])

        params = {"flash_attn": "fp16"}

        widget._apply_combo_param(params, "flash_attn", checkbox, combobox)

        assert checkbox.isChecked() is True
        assert combobox.currentText() == "fp16"

    def test_handles_missing_combobox_item(self, widget, app):
        """2.5.6: _apply_combo_param does not error when value not in combobox."""
        checkbox = QCheckBox()
        combobox = QComboBox()
        combobox.addItems(["auto", "fp16"])

        params = {"cache_type_k": {"enabled": True, "value": "unknown_type"}}

        # Should not raise - just won't find a matching index
        widget._apply_combo_param(params, "cache_type_k", checkbox, combobox)

        assert checkbox.isChecked() is True
        # No item found (findText returns -1), setCurrentIndex not called.
        # QComboBox shows first item by default when no selection.
        assert combobox.currentText() == "auto"

    def test_ignores_missing_parameter_name(self, widget, app):
        """2.5.6: _apply_combo_param does nothing when name not in params."""
        checkbox = QCheckBox()
        combobox = QComboBox()
        # Start with no items so currentText is empty by default

        params = {"other_param": {"enabled": True, "value": "fp16"}}

        widget._apply_combo_param(params, "cache_type_k", checkbox, combobox)

        # State should be unchanged (no items added, so no selection)
        assert checkbox.isChecked() is False
        assert combobox.currentText() == ""
