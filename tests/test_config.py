"""Tests for configuration collection logic.

Covers the pure data transformation logic for collecting widget values
into a configuration dictionary and loading that configuration back.
Uses simple dataclass widgets to avoid Qt dependencies in the test layer.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .config_collector import ConfigCollector

# ------------------------------------------------------------------
# Simple widget data classes (no Qt dependencies)
# ------------------------------------------------------------------


@dataclass(slots=True)
class MockLineEdit:
    """Minimal QLineEdit replacement for testing."""

    _text: str = ""

    def text(self) -> str:
        return self._text


@dataclass(slots=True)
class MockPathEdit:
    """Minimal path line edit with fullPath property."""

    _text: str = ""
    _full_path: str = ""

    def text(self) -> str:
        return self._text

    def property(self, name: str) -> str | None:
        if name == "fullPath":
            return self._full_path if self._full_path else None
        return None

    def setProperty(self, name: str, value: str) -> None:
        if name == "fullPath":
            self._full_path = value


@dataclass(slots=True)
class MockCheckBox:
    """Minimal QCheckBox replacement for testing."""

    _checked: bool = False

    def isChecked(self) -> bool:
        return self._checked


@dataclass(slots=True)
class MockSpinBox:
    """Minimal QSpinBox/QDoubleSpinBox replacement for testing."""

    _value: float = 0.0

    def value(self) -> float:
        return self._value


@dataclass(slots=True)
class MockComboBox:
    """Minimal QComboBox replacement for testing."""

    _current_text: str = ""
    _items: list[tuple[str, Any]] = field(default_factory=list)
    _current_index: int = 0

    def __post_init__(self) -> None:
        # Auto-resolve current index from text if items exist and index not set
        if self._items and self._current_text:
            for i, (text, _) in enumerate(self._items):
                if text == self._current_text:
                    self._current_index = i
                    break

    def currentText(self) -> str:
        return self._current_text

    def currentIndex(self) -> int:
        return self._current_index

    def itemData(self, index: int, role: Any) -> Any | None:
        if 0 <= index < len(self._items):
            return self._items[index][1]
        return None


# ------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------


def _make_collector(**overrides: Any) -> ConfigCollector:
    """Build a ConfigCollector with default mock widgets, then override specific ones.

    Args:
        **overrides: Named widget overrides to replace defaults.

    Returns:
        ConfigCollector instance ready for testing.
    """
    defaults = {
        "version_edit": MockLineEdit("1.0"),
        "model_path_edit": MockPathEdit(_full_path="/models/llama.gguf"),
        "mmproj_path_edit": MockPathEdit(_full_path="/models/mmproj.bin"),
        "draft_model_line_edit": MockPathEdit(_full_path="/models/draft.gguf"),
        "json_schema_line_edit": MockPathEdit(_full_path="/schemas/schema.json"),
        "host_line_edit": MockLineEdit("127.0.0.1"),
        "port_line_edit": MockLineEdit("8080"),
        "api_key_line_edit": MockLineEdit("secret-key"),
        "enable_temperature_checkbox": MockCheckBox(True),
        "temperature_spinbox": MockSpinBox(0.7),
        "enable_top_p_checkbox": MockCheckBox(True),
        "top_p_spinbox": MockSpinBox(0.9),
        "enable_top_k_checkbox": MockCheckBox(False),
        "top_k_spinbox": MockSpinBox(40),
        "enable_min_p_checkbox": MockCheckBox(False),
        "min_p_spinbox": MockSpinBox(0.05),
        "enable_typical_p_checkbox": MockCheckBox(False),
        "typical_p_spinbox": MockSpinBox(1.0),
        "enable_repeat_penalty_checkbox": MockCheckBox(False),
        "repeat_penalty_spinbox": MockSpinBox(1.1),
        "enable_repeat_last_n_checkbox": MockCheckBox(False),
        "repeat_last_n_spinbox": MockSpinBox(64),
        "enable_presence_penalty_checkbox": MockCheckBox(False),
        "presence_penalty_spinbox": MockSpinBox(0.0),
        "enable_frequency_penalty_checkbox": MockCheckBox(False),
        "frequency_penalty_spinbox": MockSpinBox(0.0),
        "enable_mirostat_checkbox": MockCheckBox(False),
        "mirostat_spinbox": MockSpinBox(0),
        "enable_mirostat_lr_checkbox": MockCheckBox(False),
        "mirostat_lr_spinbox": MockSpinBox(0.001),
        "enable_mirostat_ent_checkbox": MockCheckBox(False),
        "mirostat_ent_spinbox": MockSpinBox(5.0),
        "enable_gpu_layers_checkbox": MockCheckBox(True),
        "gpu_layers_spinbox": MockSpinBox(33),
        "enable_threads_checkbox": MockCheckBox(True),
        "threads_spinbox": MockSpinBox(8),
        "enable_threads_batch_checkbox": MockCheckBox(False),
        "threads_batch_spinbox": MockSpinBox(512),
        "enable_batch_size_checkbox": MockCheckBox(False),
        "batch_size_spinbox": MockSpinBox(512),
        "enable_ubatch_size_checkbox": MockCheckBox(False),
        "ubatch_size_spinbox": MockSpinBox(512),
        "enable_n_predict_checkbox": MockCheckBox(False),
        "n_predict_spinbox": MockSpinBox(4096),
        "enable_parallel_checkbox": MockCheckBox(False),
        "parallel_spinbox": MockSpinBox(4),
        "flash_attn_combobox": MockComboBox("false"),
        "enable_cache_type_k_checkbox": MockCheckBox(False),
        "cache_type_k_combobox": MockComboBox("f32"),
        "enable_cache_type_v_checkbox": MockCheckBox(False),
        "cache_type_v_combobox": MockComboBox("f32"),
        "enable_mmap_checkbox": MockCheckBox(True),
        "enable_mlock_checkbox": MockCheckBox(False),
        "enable_cont_batching_checkbox": MockCheckBox(True),
        "enable_draft_model_checkbox": MockCheckBox(True),
        "enable_spec_draft_n_max_checkbox": MockCheckBox(False),
        "spec_draft_n_max_spinbox": MockSpinBox(4),
        "enable_seed_checkbox": MockCheckBox(False),
        "seed_spinbox": MockSpinBox(0),
        "enable_grammar_checkbox": MockCheckBox(False),
        "grammar_line_edit": MockPathEdit(_full_path="/grammars/json.gbnf"),
        "enable_json_schema_checkbox": MockCheckBox(True),
        "enable_rope_scaling_checkbox": MockCheckBox(False),
        "rope_scaling_combobox": MockComboBox("none"),
        "enable_rope_freq_base_checkbox": MockCheckBox(False),
        "rope_freq_base_spinbox": MockSpinBox(0.0),
        "enable_rope_freq_scale_checkbox": MockCheckBox(False),
        "rope_freq_scale_spinbox": MockSpinBox(1.0),
        "model_context_size": MockComboBox(
            _current_text="4096",
            _items=[("512", 512), ("2048", 2048), ("4096", 4096), ("8192", 8192)],
        ),
        "more_options_line_edit": MockLineEdit(""),
        "no_mmproj_offload_checkbox": MockCheckBox(False),
    }
    defaults.update(overrides)
    return ConfigCollector(**defaults)


# ==================================================================
# 2.1 Version string
# ==================================================================


class TestVersionString:
    """2.1.1: Collects version string as "1.0"."""

    def test_collects_version_string_as_1_0(self) -> None:
        """2.1.1: Version is always collected as the literal "1.0"."""
        collector = _make_collector(version_edit=MockLineEdit("1.0"))
        config = collector.collect_config()

        assert config["version"] == "1.0"


# ==================================================================
# 2.2 Files/Paths
# ==================================================================


class TestFilePaths:
    """2.1.2-2.1.4: Collecting file paths from widget properties."""

    def test_collects_model_path_from_fullPath_property(self) -> None:
        """2.1.2: model_path comes from the fullPath property of the path edit."""
        collector = _make_collector(model_path_edit=MockPathEdit(_full_path="/models/llama.gguf"))
        config = collector.collect_config()

        assert config["files"]["model_path"] == "/models/llama.gguf"

    def test_collects_mmproj_and_draft_and_json_schema_paths(self) -> None:
        """2.1.3: mmproj_path, draft_model_path, json_schema_path are collected."""
        collector = _make_collector(
            mmproj_path_edit=MockPathEdit(_full_path="/models/mmproj.bin"),
            draft_model_line_edit=MockPathEdit(_full_path="/models/draft.gguf"),
            json_schema_line_edit=MockPathEdit(_full_path="/schemas/schema.json"),
        )
        config = collector.collect_config()

        assert config["files"]["mmproj_path"] == "/models/mmproj.bin"
        assert config["files"]["draft_model_path"] == "/models/draft.gguf"
        assert config["files"]["json_schema_path"] == "/schemas/schema.json"

    def test_handles_empty_paths_as_empty_strings_not_none(self) -> None:
        """2.1.4: Empty paths become empty strings, not None."""
        collector = _make_collector(
            model_path_edit=MockPathEdit(_full_path=""),
            mmproj_path_edit=MockPathEdit(),
            draft_model_line_edit=MockPathEdit(),
            json_schema_line_edit=MockPathEdit(),
        )
        config = collector.collect_config()

        for key in (
            "model_path",
            "mmproj_path",
            "draft_model_path",
            "json_schema_path",
        ):
            assert config["files"][key] == ""
            assert config["files"][key] is not None


# ==================================================================
# 2.3 Server settings
# ==================================================================


class TestServerSettings:
    """2.1.5-2.1.6: Collecting server host, port, and API key."""

    def test_collects_server_host_port_api_key(self) -> None:
        """2.1.5: Server host, port (as int), and api_key are collected correctly."""
        collector = _make_collector(
            host_line_edit=MockLineEdit("0.0.0.0"),
            port_line_edit=MockLineEdit("8080"),
            api_key_line_edit=MockLineEdit("my-api-key"),
        )
        config = collector.collect_config()

        assert config["server"]["host"] == "0.0.0.0"
        assert config["server"]["port"] == 8080
        assert isinstance(config["server"]["port"], int)
        assert config["server"]["api_key"] == "my-api-key"

    def test_handles_invalid_port_text_as_default_8080(self) -> None:
        """2.1.6: Non-digit port text falls back to default 8080."""
        collector = _make_collector(port_line_edit=MockLineEdit("not-a-port"))
        config = collector.collect_config()

        assert config["server"]["port"] == 8080

    def test_handles_empty_port_text_as_default_8080(self) -> None:
        """2.1.6: Empty port text falls back to default 8080."""
        collector = _make_collector(port_line_edit=MockLineEdit(""))
        config = collector.collect_config()

        assert config["server"]["port"] == 8080


# ==================================================================
# 2.4 Sampling parameters
# ==================================================================


class TestSamplingParameters:
    """2.1.7-2.1.8: Collecting sampling parameters with enabled+value format."""

    def test_sampling_param_has_enabled_and_value_format(self) -> None:
        """2.1.7: Each sampling param is a dict with 'enabled' (bool) and 'value' (float)."""
        collector = _make_collector(
            enable_temperature_checkbox=MockCheckBox(True),
            temperature_spinbox=MockSpinBox(0.85),
        )
        config = collector.collect_config()

        temp = config["sampling"]["temperature"]
        assert isinstance(temp, dict)
        assert temp["enabled"] is True
        assert temp["value"] == 0.85

    def test_collects_all_sampling_params(self) -> None:
        """2.1.8: All 11 sampling parameters are present in the config."""
        collector = _make_collector()
        config = collector.collect_config()

        expected_keys = {
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
        }
        assert set(config["sampling"].keys()) == expected_keys


# ==================================================================
# 2.5 Performance parameters
# ==================================================================


class TestPerformanceParameters:
    """2.1.9-2.1.11: Collecting performance parameters."""

    def test_performance_params_have_enabled_value_format(self) -> None:
        """2.1.9: Performance params use enabled+value dict format."""
        collector = _make_collector(
            enable_gpu_layers_checkbox=MockCheckBox(True),
            gpu_layers_spinbox=MockSpinBox(33),
        )
        config = collector.collect_config()

        gpu = config["performance"]["gpu_layers"]
        assert isinstance(gpu, dict)
        assert gpu["enabled"] is True
        assert gpu["value"] == 33

    def test_collects_flash_attn_combobox_text(self) -> None:
        """2.1.10: flash_attn collects the combobox current text."""
        collector = _make_collector(
            flash_attn_combobox=MockComboBox("true"),
        )
        config = collector.collect_config()

        assert config["performance"]["flash_attn"] == "true"

    def test_collects_mmap_mlock_cont_batching_booleans(self) -> None:
        """2.1.11: mmap, mlock, cont_batching are boolean values from checkboxes."""
        collector = _make_collector(
            enable_mmap_checkbox=MockCheckBox(True),
            enable_mlock_checkbox=MockCheckBox(False),
            enable_cont_batching_checkbox=MockCheckBox(True),
        )
        config = collector.collect_config()

        assert config["performance"]["mmap"] is True
        assert config["performance"]["mlock"] is False
        assert config["performance"]["cont_batching"] is True


# ==================================================================
# 2.6 Advanced parameters
# ==================================================================


class TestAdvancedParameters:
    """2.1.12-2.1.13: Collecting advanced generation parameters."""

    def test_collects_advanced_params(self) -> None:
        """2.1.12: draft_model, spec_draft_n_max, seed, grammar, json_schema collected."""
        collector = _make_collector(
            enable_draft_model_checkbox=MockCheckBox(True),
            draft_model_line_edit=MockPathEdit(_full_path="/models/draft.gguf"),
            enable_spec_draft_n_max_checkbox=MockCheckBox(True),
            spec_draft_n_max_spinbox=MockSpinBox(8),
            enable_seed_checkbox=MockCheckBox(True),
            seed_spinbox=MockSpinBox(42),
            enable_grammar_checkbox=MockCheckBox(True),
            grammar_line_edit=MockPathEdit(_full_path="/grammars/json.gbnf"),
            enable_json_schema_checkbox=MockCheckBox(False),
        )
        config = collector.collect_config()

        assert config["advanced"]["draft_model"]["enabled"] is True
        assert config["advanced"]["draft_model"]["path"] == "/models/draft.gguf"
        assert config["advanced"]["spec_draft_n_max"]["enabled"] is True
        assert config["advanced"]["spec_draft_n_max"]["value"] == 8
        assert config["advanced"]["seed"]["enabled"] is True
        assert config["advanced"]["seed"]["value"] == 42
        assert config["advanced"]["grammar"]["enabled"] is True
        assert config["advanced"]["grammar"]["path"] == "/grammars/json.gbnf"
        assert config["advanced"]["json_schema"]["enabled"] is False

    def test_collects_rope_scaling_combobox_text(self) -> None:
        """2.1.13: rope_scaling collects the combobox current text."""
        collector = _make_collector(
            enable_rope_scaling_checkbox=MockCheckBox(True),
            rope_scaling_combobox=MockComboBox("linear"),
        )
        config = collector.collect_config()

        assert config["advanced"]["rope_scaling"]["enabled"] is True
        assert config["advanced"]["rope_scaling"]["value"] == "linear"


# ==================================================================
# 2.7 Other settings
# ==================================================================


class TestOtherSettings:
    """2.1.14-2.1.15: context_size, more_options, no_mmproj_offload."""

    def test_collects_context_size_from_user_role(self) -> None:
        """2.1.14: context_size is read from the combobox UserRole data."""
        ctx_size_combo = MockComboBox(
            _current_text="8192",
            _items=[("512", 512), ("2048", 2048), ("4096", 4096), ("8192", 8192)],
        )
        collector = _make_collector(model_context_size=ctx_size_combo)
        config = collector.collect_config()

        assert config["context_size"] == 8192

    def test_collects_more_options_and_no_mmproj_offload(self) -> None:
        """2.1.15: more_options text and no_mmproj_offload boolean collected."""
        collector = _make_collector(
            more_options_line_edit=MockLineEdit("--log-disable"),
            no_mmproj_offload_checkbox=MockCheckBox(True),
        )
        config = collector.collect_config()

        assert config["more_options"] == "--log-disable"
        assert config["no_mmproj_offload"] is True


# ==================================================================
# 2.8 End-to-end: complete config collection
# ==================================================================


class TestEndToEnd:
    """Integration: verify a full config round-trip."""

    def test_collect_config_returns_all_expected_keys(self) -> None:
        """Full collect_config returns version, files, server, sampling,
        performance, advanced, context_size, more_options, no_mmproj_offload.
        """
        collector = _make_collector()
        config = collector.collect_config()

        expected_keys = {
            "version",
            "files",
            "server",
            "sampling",
            "performance",
            "advanced",
            "context_size",
            "more_options",
            "no_mmproj_offload",
        }
        assert set(config.keys()) == expected_keys

    def test_config_round_trip_save_and_load(self, tmp_path: Path) -> None:
        """Config can be serialized to JSON and deserialized back."""
        collector = _make_collector(
            model_path_edit=MockPathEdit(_full_path="/models/llama.gguf"),
            host_line_edit=MockLineEdit("0.0.0.0"),
            port_line_edit=MockLineEdit("9999"),
            enable_temperature_checkbox=MockCheckBox(True),
            temperature_spinbox=MockSpinBox(0.8),
            model_context_size=MockComboBox(
                _current_text="4096",
                _items=[("512", 512), ("2048", 2048), ("4096", 4096)],
            ),
        )
        config = collector.collect_config()

        # Save to JSON
        json_path = tmp_path / "config.json"
        with open(json_path, "w") as f:
            json.dump(config, f, indent=2)

        # Load back
        with open(json_path, "r") as f:
            loaded = json.load(f)

        assert loaded["version"] == "1.0"
        assert loaded["files"]["model_path"] == "/models/llama.gguf"
        assert loaded["server"]["port"] == 9999
        assert loaded["sampling"]["temperature"]["enabled"] is True
        assert loaded["sampling"]["temperature"]["value"] == 0.8
        assert loaded["context_size"] == 4096
