"""Tests for ProcessCommandBuilder - building llama-server command line.

Phase 3: Process Command Building

Tests the logic that constructs the llama-server command from configuration
collected by ConfigCollector. Each test verifies one aspect of command building.

Following the Testing.md Phase 3 plan:
- 3.1 Base Command (llama-server + --model + --api-key)
- 3.2 Sampling Parameters (conditional inclusion based on checkbox state)
"""

from typing import Any
from unittest.mock import MagicMock

from process_command import ProcessCommandBuilder

from .test_config import (
    MockCheckBox,
    MockComboBox,
    MockLineEdit,
    MockPathEdit,
    MockSpinBox,
    _make_collector,
)

# ==================================================================
# 3.1 Base Command
# ==================================================================


class TestBaseCommand:
    """3.1: Base command construction with llama-server and required flags."""

    def test_base_command_includes_llama_server_and_model(self) -> None:
        """3.1.1: Base command includes llama-server and --model flags."""
        config = _make_collector(
            model_path_edit=MockPathEdit(_full_path="/models/llama.gguf"),
        ).collect_config()
        builder = ProcessCommandBuilder(config)
        cmd = builder.build_command()

        assert "llama-server" in cmd
        assert "--model" in cmd
        model_idx = cmd.index("--model")
        assert cmd[model_idx + 1] == "/models/llama.gguf"

    def test_base_command_includes_api_key_default_when_empty(self) -> None:
        """3.1.2a: Base command includes --api-key with default when empty."""
        config = _make_collector(
            api_key_line_edit=MockLineEdit(""),
        ).collect_config()
        builder = ProcessCommandBuilder(config)
        cmd = builder.build_command()

        assert "--api-key" in cmd
        api_key_idx = cmd.index("--api-key")
        assert cmd[api_key_idx + 1] == "12345"

    def test_base_command_includes_custom_api_key(self) -> None:
        """3.1.2b: Base command includes --api-key with custom value when set."""
        config = _make_collector(
            api_key_line_edit=MockLineEdit("my-secret-key"),
        ).collect_config()
        builder = ProcessCommandBuilder(config)
        cmd = builder.build_command()

        assert "--api-key" in cmd
        api_key_idx = cmd.index("--api-key")
        assert cmd[api_key_idx + 1] == "my-secret-key"


# ==================================================================
# 3.2 Sampling Parameters (Conditional)
# ==================================================================
# Each sampling param is gated by its checkbox. Test enabled/disabled pairs.


class TestTemperatureParameter:
    """3.2.1-3.2.2: Temperature parameter toggling."""

    def test_includes_temp_when_temperature_enabled(self) -> None:
        """3.2.1: Includes --temp when temperature checkbox is checked."""
        config = _make_collector(
            enable_temperature_checkbox=MockCheckBox(True),
            temperature_spinbox=MockSpinBox(0.7),
        ).collect_config()
        builder = ProcessCommandBuilder(config)
        cmd = builder.build_command()

        assert "--temp" in cmd
        temp_idx = cmd.index("--temp")
        assert cmd[temp_idx + 1] == "0.7"

    def test_omits_temp_when_temperature_disabled(self) -> None:
        """3.2.2: Omits --temp when temperature checkbox is unchecked."""
        config = _make_collector(
            enable_temperature_checkbox=MockCheckBox(False),
            temperature_spinbox=MockSpinBox(0.7),
        ).collect_config()
        builder = ProcessCommandBuilder(config)
        cmd = builder.build_command()

        assert "--temp" not in cmd


class TestTopPParameter:
    """3.2.3: Top-p parameter toggling."""

    def test_includes_top_p_when_enabled(self) -> None:
        """3.2.3: Includes --top-p when top_p checkbox is checked."""
        config = _make_collector(
            enable_top_p_checkbox=MockCheckBox(True),
            top_p_spinbox=MockSpinBox(0.9),
        ).collect_config()
        builder = ProcessCommandBuilder(config)
        cmd = builder.build_command()

        assert "--top-p" in cmd
        top_p_idx = cmd.index("--top-p")
        assert cmd[top_p_idx + 1] == "0.9"

    def test_omits_top_p_when_disabled(self) -> None:
        """3.2.3: Omits --top-p when top_p checkbox is unchecked."""
        config = _make_collector(
            enable_top_p_checkbox=MockCheckBox(False),
            top_p_spinbox=MockSpinBox(0.9),
        ).collect_config()
        builder = ProcessCommandBuilder(config)
        cmd = builder.build_command()

        assert "--top-p" not in cmd


class TestTopKParameter:
    """3.2.4: Top-k parameter toggling."""

    def test_includes_top_k_when_enabled(self) -> None:
        """3.2.4: Includes --top-k when top_k checkbox is checked."""
        config = _make_collector(
            enable_top_k_checkbox=MockCheckBox(True),
            top_k_spinbox=MockSpinBox(40),
        ).collect_config()
        builder = ProcessCommandBuilder(config)
        cmd = builder.build_command()

        assert "--top-k" in cmd
        top_k_idx = cmd.index("--top-k")
        assert cmd[top_k_idx + 1] == "40"

    def test_omits_top_k_when_disabled(self) -> None:
        """3.2.4: Omits --top-k when top_k checkbox is unchecked."""
        config = _make_collector(
            enable_top_k_checkbox=MockCheckBox(False),
            top_k_spinbox=MockSpinBox(40),
        ).collect_config()
        builder = ProcessCommandBuilder(config)
        cmd = builder.build_command()

        assert "--top-k" not in cmd


class TestMinPParameter:
    """3.2.5: Min-p parameter toggling."""

    def test_includes_min_p_when_enabled(self) -> None:
        """3.2.5: Includes --min-p when min_p checkbox is checked."""
        config = _make_collector(
            enable_min_p_checkbox=MockCheckBox(True),
            min_p_spinbox=MockSpinBox(0.05),
        ).collect_config()
        builder = ProcessCommandBuilder(config)
        cmd = builder.build_command()

        assert "--min-p" in cmd
        min_p_idx = cmd.index("--min-p")
        assert cmd[min_p_idx + 1] == "0.05"

    def test_omits_min_p_when_disabled(self) -> None:
        """3.2.5: Omits --min-p when min_p checkbox is unchecked."""
        config = _make_collector(
            enable_min_p_checkbox=MockCheckBox(False),
            min_p_spinbox=MockSpinBox(0.05),
        ).collect_config()
        builder = ProcessCommandBuilder(config)
        cmd = builder.build_command()

        assert "--min-p" not in cmd


class TestTypicalPParameter:
    """3.2.6: Typical-p parameter toggling."""

    def test_includes_typical_p_when_enabled(self) -> None:
        """3.2.6: Includes --typical-p when typical_p checkbox is checked."""
        config = _make_collector(
            enable_typical_p_checkbox=MockCheckBox(True),
            typical_p_spinbox=MockSpinBox(1.0),
        ).collect_config()
        builder = ProcessCommandBuilder(config)
        cmd = builder.build_command()

        assert "--typical-p" in cmd
        typical_p_idx = cmd.index("--typical-p")
        assert cmd[typical_p_idx + 1] == "1.0"

    def test_omits_typical_p_when_disabled(self) -> None:
        """3.2.6: Omits --typical-p when typical_p checkbox is unchecked."""
        config = _make_collector(
            enable_typical_p_checkbox=MockCheckBox(False),
            typical_p_spinbox=MockSpinBox(1.0),
        ).collect_config()
        builder = ProcessCommandBuilder(config)
        cmd = builder.build_command()

        assert "--typical-p" not in cmd


class TestRepeatPenaltyParameter:
    """3.2.7: Repeat penalty parameter toggling."""

    def test_includes_repeat_penalty_when_enabled(self) -> None:
        """3.2.7: Includes --repeat-penalty when repeat_penalty checkbox is checked."""
        config = _make_collector(
            enable_repeat_penalty_checkbox=MockCheckBox(True),
            repeat_penalty_spinbox=MockSpinBox(1.1),
        ).collect_config()
        builder = ProcessCommandBuilder(config)
        cmd = builder.build_command()

        assert "--repeat-penalty" in cmd
        rp_idx = cmd.index("--repeat-penalty")
        assert cmd[rp_idx + 1] == "1.1"

    def test_omits_repeat_penalty_when_disabled(self) -> None:
        """3.2.7: Omits --repeat-penalty when repeat_penalty checkbox is unchecked."""
        config = _make_collector(
            enable_repeat_penalty_checkbox=MockCheckBox(False),
            repeat_penalty_spinbox=MockSpinBox(1.1),
        ).collect_config()
        builder = ProcessCommandBuilder(config)
        cmd = builder.build_command()

        assert "--repeat-penalty" not in cmd


class TestRepeatLastNParameter:
    """3.2.8: Repeat last N parameter toggling."""

    def test_includes_repeat_last_n_when_enabled(self) -> None:
        """3.2.8: Includes --repeat-last-n when repeat_last_n checkbox is checked."""
        config = _make_collector(
            enable_repeat_last_n_checkbox=MockCheckBox(True),
            repeat_last_n_spinbox=MockSpinBox(64),
        ).collect_config()
        builder = ProcessCommandBuilder(config)
        cmd = builder.build_command()

        assert "--repeat-last-n" in cmd
        rln_idx = cmd.index("--repeat-last-n")
        assert cmd[rln_idx + 1] == "64"

    def test_omits_repeat_last_n_when_disabled(self) -> None:
        """3.2.8: Omits --repeat-last-n when repeat_last_n checkbox is unchecked."""
        config = _make_collector(
            enable_repeat_last_n_checkbox=MockCheckBox(False),
            repeat_last_n_spinbox=MockSpinBox(64),
        ).collect_config()
        builder = ProcessCommandBuilder(config)
        cmd = builder.build_command()

        assert "--repeat-last-n" not in cmd


class TestPresencePenaltyParameter:
    """3.2.9: Presence penalty parameter toggling."""

    def test_includes_presence_penalty_when_enabled(self) -> None:
        """3.2.9: Includes --presence-penalty when presence_penalty checkbox is checked."""
        config = _make_collector(
            enable_presence_penalty_checkbox=MockCheckBox(True),
            presence_penalty_spinbox=MockSpinBox(0.5),
        ).collect_config()
        builder = ProcessCommandBuilder(config)
        cmd = builder.build_command()

        assert "--presence-penalty" in cmd
        pp_idx = cmd.index("--presence-penalty")
        assert cmd[pp_idx + 1] == "0.5"

    def test_omits_presence_penalty_when_disabled(self) -> None:
        """3.2.9: Omits --presence-penalty when presence_penalty checkbox is unchecked."""
        config = _make_collector(
            enable_presence_penalty_checkbox=MockCheckBox(False),
            presence_penalty_spinbox=MockSpinBox(0.5),
        ).collect_config()
        builder = ProcessCommandBuilder(config)
        cmd = builder.build_command()

        assert "--presence-penalty" not in cmd


class TestFrequencyPenaltyParameter:
    """3.2.10: Frequency penalty parameter toggling."""

    def test_includes_frequency_penalty_when_enabled(self) -> None:
        """3.2.10: Includes --frequency-penalty when frequency_penalty checkbox is checked."""
        config = _make_collector(
            enable_frequency_penalty_checkbox=MockCheckBox(True),
            frequency_penalty_spinbox=MockSpinBox(0.3),
        ).collect_config()
        builder = ProcessCommandBuilder(config)
        cmd = builder.build_command()

        assert "--frequency-penalty" in cmd
        fp_idx = cmd.index("--frequency-penalty")
        assert cmd[fp_idx + 1] == "0.3"

    def test_omits_frequency_penalty_when_disabled(self) -> None:
        """3.2.10: Omits --frequency-penalty when frequency_penalty checkbox is unchecked."""
        config = _make_collector(
            enable_frequency_penalty_checkbox=MockCheckBox(False),
            frequency_penalty_spinbox=MockSpinBox(0.3),
        ).collect_config()
        builder = ProcessCommandBuilder(config)
        cmd = builder.build_command()

        assert "--frequency-penalty" not in cmd


class TestMirostatParameters:
    """3.2.11: Mirostat parameters toggling (three related params)."""

    def test_includes_all_mirostat_params_when_enabled(self) -> None:
        """3.2.11a: Includes --mirostat, --mirostat-lr, --mirostat-ent when all mirostat checkboxes are checked."""
        config = _make_collector(
            enable_mirostat_checkbox=MockCheckBox(True),
            mirostat_spinbox=MockSpinBox(2),
            enable_mirostat_lr_checkbox=MockCheckBox(True),
            mirostat_lr_spinbox=MockSpinBox(0.05),
            enable_mirostat_ent_checkbox=MockCheckBox(True),
            mirostat_ent_spinbox=MockSpinBox(5.0),
        ).collect_config()
        builder = ProcessCommandBuilder(config)
        cmd = builder.build_command()

        assert "--mirostat" in cmd
        assert "--mirostat-lr" in cmd
        assert "--mirostat-ent" in cmd

    def test_omits_mirostat_when_disabled(self) -> None:
        """3.2.11b: Omits --mirostat when mirostat checkbox is unchecked."""
        config = _make_collector(
            enable_mirostat_checkbox=MockCheckBox(False),
            mirostat_spinbox=MockSpinBox(2),
        ).collect_config()
        builder = ProcessCommandBuilder(config)
        cmd = builder.build_command()

        assert "--mirostat" not in cmd

    def test_omits_mirostat_lr_when_disabled(self) -> None:
        """3.2.11c: Omits --mirostat-lr when mirostat_lr checkbox is unchecked."""
        config = _make_collector(
            enable_mirostat_lr_checkbox=MockCheckBox(False),
            mirostat_lr_spinbox=MockSpinBox(0.05),
        ).collect_config()
        builder = ProcessCommandBuilder(config)
        cmd = builder.build_command()

        assert "--mirostat-lr" not in cmd

    def test_omits_mirostat_ent_when_disabled(self) -> None:
        """3.2.11d: Omits --mirostat-ent when mirostat_ent checkbox is unchecked."""
        config = _make_collector(
            enable_mirostat_ent_checkbox=MockCheckBox(False),
            mirostat_ent_spinbox=MockSpinBox(5.0),
        ).collect_config()
        builder = ProcessCommandBuilder(config)
        cmd = builder.build_command()

        assert "--mirostat-ent" not in cmd


# ==================================================================
# 3.5 Server and Model Parameters
# ==================================================================


class TestServerHostPort:
    """3.5.1-3.5.3: Server host and port parameter handling."""

    def test_uses_host_from_config(self) -> None:
        """3.5.1: Uses host from config or falls back to default _host."""
        config = _make_collector(
            host_line_edit=MockLineEdit("0.0.0.0"),
        ).collect_config()
        builder = ProcessCommandBuilder(config)
        cmd = builder.build_command()

        assert "--host" in cmd
        host_idx = cmd.index("--host")
        assert cmd[host_idx + 1] == "0.0.0.0"

    def test_uses_port_from_config(self) -> None:
        """3.5.2: Uses port from config or falls back to default _port."""
        config = _make_collector(
            port_line_edit=MockLineEdit("3000"),
        ).collect_config()
        builder = ProcessCommandBuilder(config)
        cmd = builder.build_command()

        assert "--port" in cmd
        port_idx = cmd.index("--port")
        assert cmd[port_idx + 1] == "3000"

    def test_handles_invalid_port_falls_back_to_default(self) -> None:
        """3.5.3: Handles invalid port text (ValueError) by falling back to default."""
        config = _make_collector(
            port_line_edit=MockLineEdit("not_a_number"),
        ).collect_config()
        builder = ProcessCommandBuilder(config)
        cmd = builder.build_command()

        assert "--port" in cmd
        port_idx = cmd.index("--port")
        # Should fall back to default port 8080
        assert cmd[port_idx + 1] == "8080"


class TestMmprojParameters:
    """3.5.4-3.5.5: MMProj model parameters."""

    def test_includes_mmproj_when_path_set(self) -> None:
        """3.5.4: Includes --mmproj when mmproj_path is set."""
        config = _make_collector(
            mmproj_path_edit=MockPathEdit(_full_path="/models/mmproj.bin"),
        ).collect_config()
        builder = ProcessCommandBuilder(config)
        cmd = builder.build_command()

        assert "--mmproj" in cmd
        mmproj_idx = cmd.index("--mmproj")
        assert cmd[mmproj_idx + 1] == "/models/mmproj.bin"

    def test_includes_no_mmproj_offload_when_mmproj_and_checkbox_checked(self) -> None:
        """3.5.5: Includes --no-mmproj-offload when mmproj is set AND checkbox is checked."""
        config = _make_collector(
            mmproj_path_edit=MockPathEdit(_full_path="/models/mmproj.bin"),
            no_mmproj_offload_checkbox=MockCheckBox(True),
        ).collect_config()
        builder = ProcessCommandBuilder(config)
        cmd = builder.build_command()

        assert "--mmproj" in cmd
        assert "--no-mmproj-offload" in cmd

    def test_omits_no_mmproj_offload_when_checkbox_unchecked(self) -> None:
        """3.5.5b: Omits --no-mmproj-offload when mmproj is set but checkbox is unchecked."""
        config = _make_collector(
            mmproj_path_edit=MockPathEdit(_full_path="/models/mmproj.bin"),
            no_mmproj_offload_checkbox=MockCheckBox(False),
        ).collect_config()
        builder = ProcessCommandBuilder(config)
        cmd = builder.build_command()

        assert "--mmproj" in cmd
        assert "--no-mmproj-offload" not in cmd


class TestExtraFlags:
    """3.5.6: Extra flags parsing."""

    def test_parses_extra_flags_from_more_options(self) -> None:
        """3.5.6: Parses extra flags from more_options line edit via .split()."""
        config = _make_collector(
            more_options_line_edit=MockLineEdit("--log-id test --verbose"),
        ).collect_config()
        builder = ProcessCommandBuilder(config)
        cmd = builder.build_command()

        assert "--log-id" in cmd
        assert "test" in cmd
        assert "--verbose" in cmd

    def test_omits_extra_flags_when_empty(self) -> None:
        """3.5.6b: Omits extra flags when more_options is empty."""
        config = _make_collector(
            more_options_line_edit=MockLineEdit(""),
        ).collect_config()
        builder = ProcessCommandBuilder(config)
        cmd = builder.build_command()

        # No extra flags from empty more_options
        assert "--log-id" not in cmd


class TestContextSize:
    """3.5.7-3.5.8: Context size parameter."""

    def test_includes_ctx_size_when_greater_than_zero(self) -> None:
        """3.5.7: Includes --ctx-size only when context size > 0."""
        config = _make_collector(
            model_context_size=MockComboBox(
                _current_text="4096",
                _items=[("512", 512), ("2048", 2048), ("4096", 4096), ("8192", 8192)],
            ),
        ).collect_config()
        builder = ProcessCommandBuilder(config)
        cmd = builder.build_command()

        assert "--ctx-size" in cmd
        ctx_idx = cmd.index("--ctx-size")
        assert cmd[ctx_idx + 1] == "4096"

    def test_omits_ctx_size_when_zero(self) -> None:
        """3.5.8: Omits --ctx-size when context size is 0 (Auto)."""
        config = _make_collector(
            model_context_size=MockComboBox(
                _current_text="Auto",
                _items=[("Auto", 0), ("512", 512), ("2048", 2048), ("4096", 4096)],
            ),
        ).collect_config()
        builder = ProcessCommandBuilder(config)
        cmd = builder.build_command()

        assert "--ctx-size" not in cmd


# ==================================================================
# 3.6 Process Launch Side Effects
# ==================================================================


def _make_launch_app(**overrides: Any) -> MagicMock:
    """Build a mock LlamaLaunchApp ready for _launch_model testing.

    All widgets are configured with default values that represent
    a minimal valid configuration (model selected, defaults for everything else).

    Args:
        **overrides: Named widget overrides replace defaults.

    Returns:
        MagicMock configured as a LlamaLaunchApp instance.
    """
    app = MagicMock()

    # Required: model path must be set (otherwise _launch_model returns early)
    model_path = overrides.get("model_path", "/models/llama.gguf")
    app.model_path_edit = MagicMock()
    app.model_path_edit.property.return_value = model_path

    # Server widgets
    host = overrides.get("host", "127.0.0.1")
    port_str = overrides.get("port", "8080")
    app.host_line_edit = MagicMock()
    app.host_line_edit.text.return_value = host
    app.port_line_edit = MagicMock()
    app.port_line_edit.text.return_value = port_str
    app._host = overrides.get("_host", host)
    app._port = overrides.get("_port", int(port_str))

    # API key
    app.api_key_line_edit = MagicMock()
    app.api_key_line_edit.text.return_value = overrides.get("api_key", "")

    # All spinboxes - default to 0
    spinbox_params = [
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
        "gpu_layers",
        "threads",
        "threads_batch",
        "batch_size",
        "ubatch_size",
        "n_predict",
        "parallel",
        "spec_draft_n_max",
        "seed",
        "rope_freq_base",
        "rope_freq_scale",
    ]
    for param in spinbox_params:
        sb = MagicMock()
        sb.value.return_value = overrides.get(f"{param}_value", 0)
        setattr(app, f"{param}_spinbox", sb)

    # All checkboxes - default to unchecked
    checkbox_params = [
        "enable_temperature",
        "enable_top_p",
        "enable_top_k",
        "enable_min_p",
        "enable_typical_p",
        "enable_repeat_penalty",
        "enable_repeat_last_n",
        "enable_presence_penalty",
        "enable_frequency_penalty",
        "enable_mirostat",
        "enable_mirostat_lr",
        "enable_mirostat_ent",
        "enable_gpu_layers",
        "enable_threads",
        "enable_threads_batch",
        "enable_batch_size",
        "enable_ubatch_size",
        "enable_n_predict",
        "enable_parallel",
        "enable_mmap",
        "enable_mlock",
        "enable_cont_batching",
        "enable_draft_model",
        "enable_spec_draft_n_max",
        "enable_seed",
        "enable_grammar",
        "enable_json_schema",
        "enable_rope_scaling",
        "enable_rope_freq_base",
        "enable_rope_freq_scale",
        "enable_cache_type_k",
        "enable_cache_type_v",
    ]
    for cb in checkbox_params:
        cb_mock = MagicMock()
        cb_mock.isChecked.return_value = overrides.get(f"{cb}_checked", False)
        setattr(app, cb, cb_mock)

    # Comboboxes
    app.flash_attn_combobox = MagicMock()
    app.flash_attn_combobox.currentText.return_value = overrides.get("flash_attn", "auto")
    app.cache_type_k_combobox = MagicMock()
    app.cache_type_k_combobox.currentText.return_value = overrides.get("cache_type_k", "f32")
    app.cache_type_v_combobox = MagicMock()
    app.cache_type_v_combobox.currentText.return_value = overrides.get("cache_type_v", "f32")
    app.rope_scaling_combobox = MagicMock()
    app.rope_scaling_combobox.currentText.return_value = overrides.get("rope_scaling", "linear")

    # Path widgets
    mmproj_path = overrides.get("mmproj_path", None)
    app.mmproj_path_edit = MagicMock()
    app.mmproj_path_edit.property.return_value = mmproj_path
    app.draft_model_line_edit = MagicMock()
    app.draft_model_line_edit.property.return_value = None
    app.json_schema_line_edit = MagicMock()
    app.json_schema_line_edit.property.return_value = None
    app.grammar_line_edit = MagicMock()
    app.grammar_line_edit.text.return_value = ""

    # More options
    app.more_options_line_edit = MagicMock()
    app.more_options_line_edit.text.return_value = ""

    # Context size - default to Auto (no ctx-size)
    app.model_context_size = MagicMock()
    app.model_context_size.currentIndex.return_value = 0
    app.model_context_size.itemData.return_value = None

    # No mmproj offload checkbox
    app.no_mmproj_offload_checkbox = MagicMock()
    app.no_mmproj_offload_checkbox.isChecked.return_value = False

    # Side-effect widgets (captured by tests)
    app.output_display = MagicMock()
    app.launch_button = MagicMock()
    app.server_web_view = MagicMock()
    app._process = MagicMock()

    return app


class TestLaunchModelSideEffects:
    """3.6: Testing side effects of _launch_model method."""

    def test_3_6_1_sets_server_url(self) -> None:
        """3.6.1: Sets _server_url after building command.

        After constructing the command, the method should set
        ``_server_url`` to ``http://{host}:{port}``.
        """
        # Arrange
        from main import LlamaLaunchApp

        app = _make_launch_app()

        # Act
        LlamaLaunchApp._launch_model(app)

        # Assert
        assert app._server_url == "http://127.0.0.1:8080"

    def test_3_6_2_clears_output_display_before_launching(self) -> None:
        """3.6.2: Clears output_display before launching.

        The method should call ``output_display.clear()`` to wipe
        previous output before writing the new launch message.
        """
        # Arrange
        from main import LlamaLaunchApp

        app = _make_launch_app()

        # Act
        LlamaLaunchApp._launch_model(app)

        # Assert
        app.output_display.clear.assert_called_once()

    def test_3_6_3_appends_launch_command_to_output_display(self) -> None:
        """3.6.3: Appends launch command to output_display.

        After clearing, the method should append a line starting with
        ``Launching: `` followed by the full command joined with spaces.
        """
        # Arrange
        from main import LlamaLaunchApp

        app = _make_launch_app()

        # Act
        LlamaLaunchApp._launch_model(app)

        # Assert
        call_args = app.output_display.appendPlainText.call_args
        output_text = call_args[0][0]
        assert output_text.startswith("Launching: ")
        assert "llama-server" in output_text
        assert "/models/llama.gguf" in output_text

    def test_3_6_4_calls_process_start_with_program_and_args(self) -> None:
        """3.6.4: Calls _process.start() with correct program and args list.

        The two-argument form of ``QProcess.start`` is used:
        first argument is the program, second is a list of arguments
        (the program itself must NOT be in the list).
        """
        # Arrange
        from main import LlamaLaunchApp

        app = _make_launch_app()

        # Act
        LlamaLaunchApp._launch_model(app)

        # Assert
        app._process.start.assert_called_once()
        call_args = app._process.start.call_args
        program = call_args[0][0]
        args = call_args[0][1]
        assert program == "llama-server"
        assert "llama-server" not in args
        assert "--model" in args
        assert "/models/llama.gguf" in args
        assert "--host" in args
        assert "127.0.0.1" in args
        assert "--port" in args
        assert "8080" in args

    def test_3_6_5_updates_launch_button_text_to_stop(self) -> None:
        """3.6.5: Updates launch_button text to STOP.

        After starting the process, the button label should change
        from its default to ``STOP`` so the user can stop the server.
        """
        # Arrange
        from main import LlamaLaunchApp

        app = _make_launch_app()

        # Act
        LlamaLaunchApp._launch_model(app)

        # Assert
        app.launch_button.setText.assert_called_once_with("STOP")

    def test_3_6_6_updates_web_view_url_after_launch(self) -> None:
        """3.6.6: Updates web view URL after launch.

        The server web view should be pointed at the new server URL
        so that users can immediately interact with the running server.
        """
        # Arrange
        from main import LlamaLaunchApp

        app = _make_launch_app()

        # Act
        LlamaLaunchApp._launch_model(app)

        # Assert
        app.server_web_view.setUrl.assert_called_once()
        called_url = app.server_web_view.setUrl.call_args[0][0]
        assert called_url == "http://127.0.0.1:8080"
