"""Tests for LlamaLaunchApp configuration methods.

Covers _write_config_file and _apply_config behaviour: JSON output,
UI feedback, error handling, and configuration application to widgets.
Uses mocks to isolate the methods from Qt runtime dependencies.
"""

import json
from pathlib import Path
from unittest.mock import MagicMock, call, patch

import pytest

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


# ==================================================================
# Fixtures for _apply_config tests
# ==================================================================


@pytest.fixture
def mock_app():
    """Create a mock LlamaLaunchApp with all required widget attributes.

    Returns:
        MagicMock configured with mock Qt widgets for _apply_config testing.
    """
    app = MagicMock()

    # Files/Paths widgets
    app.model_path_edit = MagicMock()
    app.mmproj_path_edit = MagicMock()
    app.draft_model_line_edit = MagicMock()
    app.json_schema_line_edit = MagicMock()

    # Server widgets
    app.host_line_edit = MagicMock()
    app.port_line_edit = MagicMock()
    app.api_key_line_edit = MagicMock()

    # Sampling parameters widgets (12 params)
    sampling_params = [
        "temperature",
        "top_p",
        "top_k",
        "min_p",
        "typical_p",
        "repeat_penalty",
        "repeat_last_n",
        "presence_penalty",
        "frequency_penalty",
        "mirostat",
        "mirostat_lr",
        "mirostat_ent",
    ]
    for param in sampling_params:
        checkbox = MagicMock()
        spinbox = MagicMock()
        setattr(app, f"enable_{param}_checkbox", checkbox)
        setattr(app, f"{param}_spinbox", spinbox)

    # Performance parameters widgets (7 params)
    perf_params = [
        "gpu_layers",
        "threads",
        "threads_batch",
        "batch_size",
        "ubatch_size",
        "n_predict",
        "parallel",
    ]
    for param in perf_params:
        checkbox = MagicMock()
        spinbox = MagicMock()
        setattr(app, f"enable_{param}_checkbox", checkbox)
        setattr(app, f"{param}_spinbox", spinbox)

    # Performance comboboxes
    app.flash_attn_combobox = MagicMock()
    app.cache_type_k_combobox = MagicMock()
    app.cache_type_v_combobox = MagicMock()

    # Boolean checkboxes for performance
    app.enable_mmap_checkbox = MagicMock()
    app.enable_mlock_checkbox = MagicMock()
    app.enable_cont_batching_checkbox = MagicMock()

    # Advanced parameters widgets
    advanced_params = ["spec_draft_n_max", "seed", "rope_freq_base", "rope_freq_scale"]
    for param in advanced_params:
        checkbox = MagicMock()
        spinbox = MagicMock()
        setattr(app, f"enable_{param}_checkbox", checkbox)
        setattr(app, f"{param}_spinbox", spinbox)

    # Advanced path widgets
    app.grammar_line_edit = MagicMock()

    # Advanced boolean checkboxes
    app.enable_draft_model_checkbox = MagicMock()
    app.enable_grammar_checkbox = MagicMock()
    app.enable_json_schema_checkbox = MagicMock()

    # Advanced comboboxes
    app.rope_scaling_combobox = MagicMock()

    # Context size widget
    app.model_context_size = MagicMock()

    # Other widgets
    app.more_options_line_edit = MagicMock()
    app.no_mmproj_offload_checkbox = MagicMock()

    # Helper methods (mocked to track calls)
    app._set_path_field = MagicMock()
    app._apply_param = MagicMock()
    app._apply_combo_param = MagicMock()

    return app


# ==================================================================
# 2.4 Configuration Application (_apply_config)
# ==================================================================


class TestApplyConfig:
    """2.4: Testing _apply_config method."""

    def test_2_4_1_applies_files_section(self, mock_app):
        """2.4.1: Applies files section (model_path, mmproj_path,
        draft_model_path, json_schema_path).
        """
        config = {
            "files": {
                "model_path": "/path/to/model.gguf",
                "mmproj_path": "/path/to/mmproj.bin",
                "draft_model_path": "/path/to/draft.gguf",
                "json_schema_path": "/path/to/schema.json",
            },
        }

        LlamaLaunchApp._apply_config(mock_app, config)

        mock_app._set_path_field.assert_has_calls(
            [
                call(mock_app.model_path_edit, "/path/to/model.gguf"),
                call(mock_app.mmproj_path_edit, "/path/to/mmproj.bin"),
                call(mock_app.draft_model_line_edit, "/path/to/draft.gguf"),
                call(mock_app.json_schema_line_edit, "/path/to/schema.json"),
            ]
        )
        assert mock_app._set_path_field.call_count == 4

    def test_2_4_1_empty_files_section(self, mock_app):
        """2.4.1: Calls _set_path_field with empty string for missing file keys."""
        config = {"files": {}}

        LlamaLaunchApp._apply_config(mock_app, config)

        mock_app._set_path_field.assert_has_calls(
            [
                call(mock_app.model_path_edit, ""),
                call(mock_app.mmproj_path_edit, ""),
                call(mock_app.draft_model_line_edit, ""),
                call(mock_app.json_schema_line_edit, ""),
            ]
        )

    def test_2_4_2_applies_server_section_with_defaults(self, mock_app):
        """2.4.2: Applies server section (host, port, api_key) with defaults."""
        config = {"server": {}}

        LlamaLaunchApp._apply_config(mock_app, config)

        mock_app.host_line_edit.setText.assert_called_once_with("127.0.0.1")
        mock_app.port_line_edit.setText.assert_called_once_with("8080")
        mock_app.api_key_line_edit.setText.assert_called_once_with("12345")

    def test_2_4_2_applies_server_section_with_custom_values(self, mock_app):
        """2.4.2: Applies server section with custom values."""
        config = {
            "server": {
                "host": "0.0.0.0",
                "port": 8000,
                "api_key": "secret-key",
            },
        }

        LlamaLaunchApp._apply_config(mock_app, config)

        mock_app.host_line_edit.setText.assert_called_once_with("0.0.0.0")
        mock_app.port_line_edit.setText.assert_called_once_with("8000")
        mock_app.api_key_line_edit.setText.assert_called_once_with("secret-key")

    def test_2_4_3_applies_sampling_parameters(self, mock_app):
        """2.4.3: Applies all sampling parameters via _apply_param."""
        config = {
            "sampling": {
                "temperature": {"enabled": True, "value": 0.8},
                "top_p": {"enabled": False, "value": 0.95},
                "top_k": {"enabled": True, "value": 40},
                "min_p": {"enabled": True, "value": 0.1},
                "typical_p": {"enabled": True, "value": 1.0},
                "repeat_penalty": {"enabled": True, "value": 1.1},
                "repeat_last_n": {"enabled": True, "value": 64},
                "presence_penalty": {"enabled": False, "value": 0.0},
                "frequency_penalty": {"enabled": False, "value": 0.0},
                "mirostat": {"enabled": False, "value": 0},
                "mirostat_lr": {"enabled": False, "value": 0.1},
                "mirostat_ent": {"enabled": False, "value": 5.0},
            },
        }

        LlamaLaunchApp._apply_config(mock_app, config)

        assert mock_app._apply_param.call_count == 12

        # Verify a representative sample of calls
        mock_app._apply_param.assert_any_call(
            config["sampling"],
            "temperature",
            mock_app.enable_temperature_checkbox,
            mock_app.temperature_spinbox,
        )
        mock_app._apply_param.assert_any_call(
            config["sampling"],
            "mirostat_ent",
            mock_app.enable_mirostat_ent_checkbox,
            mock_app.mirostat_ent_spinbox,
        )

    def test_2_4_3_sampling_with_legacy_scalar_values(self, mock_app):
        """2.4.3: Sampling parameters with legacy scalar (non-dict) values."""
        config = {
            "sampling": {
                "temperature": 0.7,
                "top_p": 0.9,
            },
        }

        LlamaLaunchApp._apply_config(mock_app, config)

        # _apply_config calls _apply_param for ALL sampling params (12),
        # but only params present in the dict are actually applied.
        assert mock_app._apply_param.call_count == 12
        mock_app._apply_param.assert_any_call(
            config["sampling"],
            "temperature",
            mock_app.enable_temperature_checkbox,
            mock_app.temperature_spinbox,
        )
        mock_app._apply_param.assert_any_call(
            config["sampling"],
            "top_p",
            mock_app.enable_top_p_checkbox,
            mock_app.top_p_spinbox,
        )

    def test_2_4_4_applies_performance_parameters(self, mock_app):
        """2.4.4: Applies performance parameters (gpu_layers, threads, etc.)."""
        config = {
            "performance": {
                "gpu_layers": {"enabled": True, "value": 35},
                "threads": {"enabled": True, "value": 8},
                "threads_batch": {"enabled": False, "value": -1},
                "batch_size": {"enabled": True, "value": 512},
                "ubatch_size": {"enabled": True, "value": 512},
                "n_predict": {"enabled": True, "value": 512},
                "parallel": {"enabled": False, "value": 4},
            },
        }

        LlamaLaunchApp._apply_config(mock_app, config)

        assert mock_app._apply_param.call_count == 7

        mock_app._apply_param.assert_any_call(
            config["performance"],
            "gpu_layers",
            mock_app.enable_gpu_layers_checkbox,
            mock_app.gpu_layers_spinbox,
        )
        mock_app._apply_param.assert_any_call(
            config["performance"],
            "parallel",
            mock_app.enable_parallel_checkbox,
            mock_app.parallel_spinbox,
        )

    def test_2_4_5_applies_flash_attn_combobox(self, mock_app):
        """2.4.5: Applies flash_attn combobox selection."""
        mock_app.flash_attn_combobox.findText.return_value = 1

        config = {"performance": {"flash_attn": "false"}}

        LlamaLaunchApp._apply_config(mock_app, config)

        mock_app.flash_attn_combobox.findText.assert_called_once_with("false")
        mock_app.flash_attn_combobox.setCurrentIndex.assert_called_once_with(1)

    def test_2_4_5_flash_attn_not_found(self, mock_app):
        """2.4.5: flash_attn not found in combobox - no setCurrentIndex call."""
        mock_app.flash_attn_combobox.findText.return_value = -1

        config = {"performance": {"flash_attn": "unknown_value"}}

        LlamaLaunchApp._apply_config(mock_app, config)

        mock_app.flash_attn_combobox.findText.assert_called_once_with("unknown_value")
        mock_app.flash_attn_combobox.setCurrentIndex.assert_not_called()

    def test_2_4_6_applies_cache_type_combo_params(self, mock_app):
        """2.4.6: Applies cache_type_k/v combo params via _apply_combo_param."""
        config = {
            "performance": {
                "cache_type_k": {"enabled": True, "value": "f16"},
                "cache_type_v": {"enabled": True, "value": "f16"},
            },
        }

        LlamaLaunchApp._apply_config(mock_app, config)

        mock_app._apply_combo_param.assert_any_call(
            config["performance"],
            "cache_type_k",
            mock_app.enable_cache_type_k_checkbox,
            mock_app.cache_type_k_combobox,
        )
        mock_app._apply_combo_param.assert_any_call(
            config["performance"],
            "cache_type_v",
            mock_app.enable_cache_type_v_checkbox,
            mock_app.cache_type_v_combobox,
        )

    def test_2_4_7_applies_boolean_performance_params(self, mock_app):
        """2.4.7: Applies mmap, mlock, cont_batching booleans."""
        config = {
            "performance": {
                "mmap": True,
                "mlock": False,
                "cont_batching": True,
            },
        }

        LlamaLaunchApp._apply_config(mock_app, config)

        mock_app.enable_mmap_checkbox.setChecked.assert_called_once_with(True)
        mock_app.enable_mlock_checkbox.setChecked.assert_called_once_with(False)
        mock_app.enable_cont_batching_checkbox.setChecked.assert_called_once_with(True)

    def test_2_4_8_applies_advanced_section(self, mock_app):
        """2.4.8: Applies advanced section (spec_draft_n_max, seed)."""
        config = {
            "advanced": {
                "spec_draft_n_max": {"enabled": True, "value": 4},
                "seed": {"enabled": False, "value": -1},
            },
        }

        LlamaLaunchApp._apply_config(mock_app, config)

        # _apply_config calls _apply_param for ALL advanced params (4),
        # including rope_freq_base and rope_freq_scale.
        assert mock_app._apply_param.call_count == 4

        mock_app._apply_param.assert_any_call(
            config["advanced"],
            "spec_draft_n_max",
            mock_app.enable_spec_draft_n_max_checkbox,
            mock_app.spec_draft_n_max_spinbox,
        )
        mock_app._apply_param.assert_any_call(
            config["advanced"],
            "seed",
            mock_app.enable_seed_checkbox,
            mock_app.seed_spinbox,
        )

    def test_2_4_9_applies_draft_model_path_based_params(self, mock_app):
        """2.4.9: Applies draft_model path-based params (enabled + path)."""
        config = {
            "advanced": {
                "draft_model": {
                    "enabled": True,
                    "path": "/path/to/draft-model.gguf",
                },
            },
        }

        LlamaLaunchApp._apply_config(mock_app, config)

        mock_app.enable_draft_model_checkbox.setChecked.assert_called_once_with(True)
        mock_app._set_path_field.assert_called_once_with(
            mock_app.draft_model_line_edit,
            "/path/to/draft-model.gguf",
        )

    def test_2_4_9_draft_model_disabled(self, mock_app):
        """2.4.9: draft_model with enabled=False sets checkbox accordingly."""
        config = {
            "advanced": {
                "draft_model": {"enabled": False, "path": "/path/to/draft.gguf"},
            },
        }

        LlamaLaunchApp._apply_config(mock_app, config)

        mock_app.enable_draft_model_checkbox.setChecked.assert_called_once_with(False)

    def test_2_4_10_applies_grammar_path_based_params(self, mock_app):
        """2.4.10: Applies grammar path-based params."""
        config = {
            "advanced": {
                "grammar": {
                    "enabled": True,
                    "path": "/path/to/grammar.json",
                },
            },
        }

        LlamaLaunchApp._apply_config(mock_app, config)

        mock_app.enable_grammar_checkbox.setChecked.assert_called_once_with(True)
        mock_app._set_path_field.assert_called_once_with(
            mock_app.grammar_line_edit,
            "/path/to/grammar.json",
        )

    def test_2_4_11_applies_json_schema_path_based_params(self, mock_app):
        """2.4.11: Applies json_schema path-based params."""
        config = {
            "advanced": {
                "json_schema": {
                    "enabled": True,
                    "path": "/path/to/schema.json",
                },
            },
        }

        LlamaLaunchApp._apply_config(mock_app, config)

        mock_app.enable_json_schema_checkbox.setChecked.assert_called_once_with(True)
        mock_app._set_path_field.assert_called_once_with(
            mock_app.json_schema_line_edit,
            "/path/to/schema.json",
        )

    def test_2_4_12_applies_rope_scaling_combo_param(self, mock_app):
        """2.4.12: Applies rope_scaling combo param."""
        config = {
            "advanced": {
                "rope_scaling": {"enabled": True, "value": "linear"},
            },
        }

        LlamaLaunchApp._apply_config(mock_app, config)

        mock_app._apply_combo_param.assert_called_once_with(
            config["advanced"],
            "rope_scaling",
            mock_app.enable_rope_scaling_checkbox,
            mock_app.rope_scaling_combobox,
        )

    def test_2_4_13_applies_context_size_selection(self, mock_app):
        """2.4.13: Applies context_size selection."""
        # Simulate combobox with options: 512, 2048, 4096, 8192
        mock_app.model_context_size.count.return_value = 4
        mock_app.model_context_size.itemData.side_effect = [512, 2048, 4096, 8192]

        config = {"context_size": 4096}

        LlamaLaunchApp._apply_config(mock_app, config)

        mock_app.model_context_size.setCurrentIndex.assert_called_once_with(2)

    def test_2_4_13_context_size_not_found(self, mock_app):
        """2.4.13: context_size not found - no setCurrentIndex call."""
        mock_app.model_context_size.count.return_value = 3
        mock_app.model_context_size.itemData.side_effect = [2048, 4096, 8192]

        config = {"context_size": 16384}  # Not in the list

        LlamaLaunchApp._apply_config(mock_app, config)

        mock_app.model_context_size.setCurrentIndex.assert_not_called()

    def test_2_4_14_applies_more_options_and_no_mmproj_offload(self, mock_app):
        """2.4.14: Applies more_options and no_mmproj_offload."""
        config = {
            "more_options": "--log-disable",
            "no_mmproj_offload": True,
        }

        LlamaLaunchApp._apply_config(mock_app, config)

        mock_app.more_options_line_edit.setText.assert_called_once_with("--log-disable")
        mock_app.no_mmproj_offload_checkbox.setChecked.assert_called_once_with(True)

    def test_2_4_14_no_mmproj_offload_false(self, mock_app):
        """2.4.14: no_mmproj_offload with False value."""
        config = {"no_mmproj_offload": False}

        LlamaLaunchApp._apply_config(mock_app, config)

        mock_app.no_mmproj_offload_checkbox.setChecked.assert_called_once_with(False)

    def test_2_4_15_handles_missing_config_sections_gracefully(self, mock_app):
        """2.4.15: Handles missing config sections gracefully (no errors)."""
        # Empty config should not raise any exceptions
        LlamaLaunchApp._apply_config(mock_app, {})

        # Config with unknown keys should not raise any exceptions
        LlamaLaunchApp._apply_config(mock_app, {"unknown_key": "value"})

    def test_2_4_15_handles_empty_sections_gracefully(self, mock_app):
        """2.4.15: Handles empty config sections gracefully."""
        config = {
            "files": {},
            "server": {},
            "sampling": {},
            "performance": {},
            "advanced": {},
        }

        # Should not raise any exceptions
        LlamaLaunchApp._apply_config(mock_app, config)

    def test_2_4_applies_all_sections_together(self, mock_app):
        """Integration: Applies all config sections together without errors."""
        mock_app.flash_attn_combobox.findText.return_value = 0
        mock_app.cache_type_k_combobox.findText.return_value = 0
        mock_app.cache_type_v_combobox.findText.return_value = 0
        mock_app.rope_scaling_combobox.findText.return_value = 0
        mock_app.model_context_size.count.return_value = 2
        mock_app.model_context_size.itemData.side_effect = [4096, 8192]

        config = {
            "files": {"model_path": "/path/to/model.gguf"},
            "server": {"host": "0.0.0.0", "port": 8000, "api_key": "key"},
            "sampling": {"temperature": {"enabled": True, "value": 0.8}},
            "performance": {
                "gpu_layers": {"enabled": True, "value": 35},
                "flash_attn": "false",
                "cache_type_k": {"enabled": True, "value": "f16"},
                "mmap": True,
            },
            "advanced": {
                "seed": {"enabled": False, "value": -1},
                "draft_model": {"enabled": True, "path": "/draft.gguf"},
                "rope_scaling": {"enabled": False, "value": "none"},
            },
            "context_size": 4096,
            "more_options": "--log-disable",
            "no_mmproj_offload": True,
        }

        # Should not raise any exceptions
        LlamaLaunchApp._apply_config(mock_app, config)

    def test_2_4_sampling_with_disabled_params(self, mock_app):
        """2.4.3: Sampling parameters with disabled flag."""
        config = {
            "sampling": {
                "temperature": {"enabled": False, "value": 0.8},
            },
        }

        LlamaLaunchApp._apply_config(mock_app, config)

        # _apply_config calls _apply_param for ALL sampling params (12),
        # but only temperature is present in the config.
        assert mock_app._apply_param.call_count == 12

        # Verify the specific call for temperature is correct
        mock_app._apply_param.assert_any_call(
            config["sampling"],
            "temperature",
            mock_app.enable_temperature_checkbox,
            mock_app.temperature_spinbox,
        )

    def test_2_4_advanced_with_rope_params(self, mock_app):
        """2.4.8: Applies rope_freq_base and rope_freq_scale via _apply_param."""
        config = {
            "advanced": {
                "rope_freq_base": {"enabled": True, "value": 1000000},
                "rope_freq_scale": {"enabled": True, "value": 1.0},
            },
        }

        LlamaLaunchApp._apply_config(mock_app, config)

        # Should have 4 calls: spec_draft_n_max, seed, rope_freq_base, rope_freq_scale
        assert mock_app._apply_param.call_count == 4

        mock_app._apply_param.assert_any_call(
            config["advanced"],
            "rope_freq_base",
            mock_app.enable_rope_freq_base_checkbox,
            mock_app.rope_freq_base_spinbox,
        )
        mock_app._apply_param.assert_any_call(
            config["advanced"],
            "rope_freq_scale",
            mock_app.enable_rope_freq_scale_checkbox,
            mock_app.rope_freq_scale_spinbox,
        )
