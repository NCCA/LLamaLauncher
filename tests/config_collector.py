"""Pure configuration collection logic.

Extracted from main.py to enable unit testing without Qt dependencies.
Accepts widget-like objects through dependency injection and returns
a plain dictionary suitable for JSON serialization.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ConfigCollector:
    """Collect configuration values from UI widget-like objects.

    Each widget attribute is a simple object with methods like .text(),
    .isChecked(), .value(), .property(), .currentText(), .currentIndex(),
    and .itemData() that mirror the Qt widget interface.

    Attributes:
        version_edit: Widget providing the version string via .text().
        model_path_edit: Path edit with .property("fullPath").
        mmproj_path_edit: Path edit for mmproj model path.
        draft_model_line_edit: Path edit for draft model path.
        json_schema_line_edit: Path edit for JSON schema path.
        host_line_edit: Widget providing server host via .text().
        port_line_edit: Widget providing server port text (digits or fallback).
        api_key_line_edit: Widget providing API key via .text().
        enable_temperature_checkbox / temperature_spinbox: Sampling param.
        enable_top_p_checkbox / top_p_spinbox: Sampling param.
        enable_top_k_checkbox / top_k_spinbox: Sampling param.
        enable_min_p_checkbox / min_p_spinbox: Sampling param.
        enable_typical_p_checkbox / typical_p_spinbox: Sampling param.
        enable_repeat_penalty_checkbox / repeat_penalty_spinbox: Sampling param.
        enable_repeat_last_n_checkbox / repeat_last_n_spinbox: Sampling param.
        enable_presence_penalty_checkbox / presence_penalty_spinbox: Sampling param.
        enable_frequency_penalty_checkbox / frequency_penalty_spinbox: Sampling param.
        enable_mirostat_checkbox / mirostat_spinbox: Sampling param.
        enable_mirostat_lr_checkbox / mirostat_lr_spinbox: Sampling param.
        enable_mirostat_ent_checkbox / mirostat_ent_spinbox: Sampling param.
        enable_gpu_layers_checkbox / gpu_layers_spinbox: Performance param.
        enable_threads_checkbox / threads_spinbox: Performance param.
        enable_threads_batch_checkbox / threads_batch_spinbox: Performance param.
        enable_batch_size_checkbox / batch_size_spinbox: Performance param.
        enable_ubatch_size_checkbox / ubatch_size_spinbox: Performance param.
        enable_n_predict_checkbox / n_predict_spinbox: Performance param.
        enable_parallel_checkbox / parallel_spinbox: Performance param.
        flash_attn_combobox: Combobox for flash attention setting text.
        enable_cache_type_k_checkbox / cache_type_k_combobox: Performance param.
        enable_cache_type_v_checkbox / cache_type_v_combobox: Performance param.
        enable_mmap_checkbox: Boolean mmap setting.
        enable_mlock_checkbox: Boolean mlock setting.
        enable_cont_batching_checkbox: Boolean cont_batching setting.
        enable_draft_model_checkbox / draft_model_line_edit: Advanced path+enabled.
        enable_spec_draft_n_max_checkbox / spec_draft_n_max_spinbox: Advanced param.
        enable_seed_checkbox / seed_spinbox: Advanced param.
        enable_grammar_checkbox / grammar_line_edit: Advanced path+enabled.
        enable_json_schema_checkbox / json_schema_line_edit: Advanced path+enabled.
        enable_rope_scaling_checkbox / rope_scaling_combobox: Advanced combobox.
        enable_rope_freq_base_checkbox / rope_freq_base_spinbox: Advanced param.
        enable_rope_freq_scale_checkbox / rope_freq_scale_spinbox: Advanced param.
        model_context_size: Combobox providing context size via .itemData(index, role).
        more_options_line_edit: Widget providing extra options text.
        no_mmproj_offload_checkbox: Boolean no_mmproj_offload setting.
    """

    # Files/Paths
    version_edit: Any = field(default=None)
    model_path_edit: Any = field(default=None)
    mmproj_path_edit: Any = field(default=None)
    draft_model_line_edit: Any = field(default=None)
    json_schema_line_edit: Any = field(default=None)

    # Server
    host_line_edit: Any = field(default=None)
    port_line_edit: Any = field(default=None)
    api_key_line_edit: Any = field(default=None)

    # Sampling parameters (12 pairs)
    enable_temperature_checkbox: Any = field(default=None)
    temperature_spinbox: Any = field(default=None)
    enable_top_p_checkbox: Any = field(default=None)
    top_p_spinbox: Any = field(default=None)
    enable_top_k_checkbox: Any = field(default=None)
    top_k_spinbox: Any = field(default=None)
    enable_min_p_checkbox: Any = field(default=None)
    min_p_spinbox: Any = field(default=None)
    enable_typical_p_checkbox: Any = field(default=None)
    typical_p_spinbox: Any = field(default=None)
    enable_repeat_penalty_checkbox: Any = field(default=None)
    repeat_penalty_spinbox: Any = field(default=None)
    enable_repeat_last_n_checkbox: Any = field(default=None)
    repeat_last_n_spinbox: Any = field(default=None)
    enable_presence_penalty_checkbox: Any = field(default=None)
    presence_penalty_spinbox: Any = field(default=None)
    enable_frequency_penalty_checkbox: Any = field(default=None)
    frequency_penalty_spinbox: Any = field(default=None)
    enable_mirostat_checkbox: Any = field(default=None)
    mirostat_spinbox: Any = field(default=None)
    enable_mirostat_lr_checkbox: Any = field(default=None)
    mirostat_lr_spinbox: Any = field(default=None)
    enable_mirostat_ent_checkbox: Any = field(default=None)
    mirostat_ent_spinbox: Any = field(default=None)

    # Performance parameters
    enable_gpu_layers_checkbox: Any = field(default=None)
    gpu_layers_spinbox: Any = field(default=None)
    enable_threads_checkbox: Any = field(default=None)
    threads_spinbox: Any = field(default=None)
    enable_threads_batch_checkbox: Any = field(default=None)
    threads_batch_spinbox: Any = field(default=None)
    enable_batch_size_checkbox: Any = field(default=None)
    batch_size_spinbox: Any = field(default=None)
    enable_ubatch_size_checkbox: Any = field(default=None)
    ubatch_size_spinbox: Any = field(default=None)
    enable_n_predict_checkbox: Any = field(default=None)
    n_predict_spinbox: Any = field(default=None)
    enable_parallel_checkbox: Any = field(default=None)
    parallel_spinbox: Any = field(default=None)
    flash_attn_combobox: Any = field(default=None)
    enable_cache_type_k_checkbox: Any = field(default=None)
    cache_type_k_combobox: Any = field(default=None)
    enable_cache_type_v_checkbox: Any = field(default=None)
    cache_type_v_combobox: Any = field(default=None)
    enable_mmap_checkbox: Any = field(default=None)
    enable_mlock_checkbox: Any = field(default=None)
    enable_cont_batching_checkbox: Any = field(default=None)

    # Advanced generation parameters
    enable_draft_model_checkbox: Any = field(default=None)
    enable_spec_draft_n_max_checkbox: Any = field(default=None)
    spec_draft_n_max_spinbox: Any = field(default=None)
    enable_seed_checkbox: Any = field(default=None)
    seed_spinbox: Any = field(default=None)
    enable_grammar_checkbox: Any = field(default=None)
    grammar_line_edit: Any = field(default=None)
    enable_json_schema_checkbox: Any = field(default=None)
    json_schema_line_edit: Any = field(default=None)
    enable_rope_scaling_checkbox: Any = field(default=None)
    rope_scaling_combobox: Any = field(default=None)
    enable_rope_freq_base_checkbox: Any = field(default=None)
    rope_freq_base_spinbox: Any = field(default=None)
    enable_rope_freq_scale_checkbox: Any = field(default=None)
    rope_freq_scale_spinbox: Any = field(default=None)

    # Other settings
    model_context_size: Any = field(default=None)
    more_options_line_edit: Any = field(default=None)
    no_mmproj_offload_checkbox: Any = field(default=None)

    def _path(self, widget: Any) -> str:
        """Get path string from a path edit widget, returning "" for empty."""
        val = widget.property("fullPath")
        return val if val else ""

    def _port(self, widget: Any) -> int:
        """Get port as int, falling back to 8080 for non-digit text."""
        text = widget.text()
        return int(text) if text.isdigit() else 8080

    def _param(self, checkbox: Any, spinbox: Any) -> dict[str, Any]:
        """Build an enabled+value parameter dict from checkbox and spinbox."""
        return {
            "enabled": checkbox.isChecked(),
            "value": spinbox.value(),
        }

    def _combo_param(self, checkbox: Any, combobox: Any) -> dict[str, Any]:
        """Build an enabled+text parameter dict from checkbox and combobox."""
        return {
            "enabled": checkbox.isChecked(),
            "value": combobox.currentText(),
        }

    def collect_config(self) -> dict[str, Any]:
        """Collect all UI widget values into a configuration dictionary.

        Returns:
            Dictionary containing all configuration values organized by category.
        """
        config: dict[str, Any] = {"version": "1.0"}

        # Files/Paths
        config["files"] = {
            "model_path": self._path(self.model_path_edit),
            "mmproj_path": self._path(self.mmproj_path_edit),
            "draft_model_path": self._path(self.draft_model_line_edit),
            "json_schema_path": self._path(self.json_schema_line_edit),
        }

        # Server
        config["server"] = {
            "host": self.host_line_edit.text(),
            "port": self._port(self.port_line_edit),
            "api_key": self.api_key_line_edit.text(),
        }

        # Sampling parameters
        config["sampling"] = {
            "temperature": self._param(
                self.enable_temperature_checkbox, self.temperature_spinbox
            ),
            "top_p": self._param(self.enable_top_p_checkbox, self.top_p_spinbox),
            "top_k": self._param(self.enable_top_k_checkbox, self.top_k_spinbox),
            "min_p": self._param(self.enable_min_p_checkbox, self.min_p_spinbox),
            "typical_p": self._param(
                self.enable_typical_p_checkbox, self.typical_p_spinbox
            ),
            "repeat_penalty": self._param(
                self.enable_repeat_penalty_checkbox, self.repeat_penalty_spinbox
            ),
            "repeat_last_n": self._param(
                self.enable_repeat_last_n_checkbox, self.repeat_last_n_spinbox
            ),
            "presence_penalty": self._param(
                self.enable_presence_penalty_checkbox, self.presence_penalty_spinbox
            ),
            "frequency_penalty": self._param(
                self.enable_frequency_penalty_checkbox, self.frequency_penalty_spinbox
            ),
            "mirostat": self._param(
                self.enable_mirostat_checkbox, self.mirostat_spinbox
            ),
            "mirostat_lr": self._param(
                self.enable_mirostat_lr_checkbox, self.mirostat_lr_spinbox
            ),
            "mirostat_ent": self._param(
                self.enable_mirostat_ent_checkbox, self.mirostat_ent_spinbox
            ),
        }

        # Performance parameters
        config["performance"] = {
            "gpu_layers": self._param(
                self.enable_gpu_layers_checkbox, self.gpu_layers_spinbox
            ),
            "threads": self._param(self.enable_threads_checkbox, self.threads_spinbox),
            "threads_batch": self._param(
                self.enable_threads_batch_checkbox, self.threads_batch_spinbox
            ),
            "batch_size": self._param(
                self.enable_batch_size_checkbox, self.batch_size_spinbox
            ),
            "ubatch_size": self._param(
                self.enable_ubatch_size_checkbox, self.ubatch_size_spinbox
            ),
            "n_predict": self._param(
                self.enable_n_predict_checkbox, self.n_predict_spinbox
            ),
            "parallel": self._param(
                self.enable_parallel_checkbox, self.parallel_spinbox
            ),
            "flash_attn": self.flash_attn_combobox.currentText(),
            "cache_type_k": self._combo_param(
                self.enable_cache_type_k_checkbox, self.cache_type_k_combobox
            ),
            "cache_type_v": self._combo_param(
                self.enable_cache_type_v_checkbox, self.cache_type_v_combobox
            ),
            "mmap": self.enable_mmap_checkbox.isChecked(),
            "mlock": self.enable_mlock_checkbox.isChecked(),
            "cont_batching": self.enable_cont_batching_checkbox.isChecked(),
        }

        # Advanced Generation parameters
        config["advanced"] = {
            "draft_model": {
                "enabled": self.enable_draft_model_checkbox.isChecked(),
                "path": self._path(self.draft_model_line_edit),
            },
            "spec_draft_n_max": self._param(
                self.enable_spec_draft_n_max_checkbox, self.spec_draft_n_max_spinbox
            ),
            "seed": self._param(self.enable_seed_checkbox, self.seed_spinbox),
            "grammar": {
                "enabled": self.enable_grammar_checkbox.isChecked(),
                "path": self._path(self.grammar_line_edit),
            },
            "json_schema": {
                "enabled": self.enable_json_schema_checkbox.isChecked(),
                "path": self._path(self.json_schema_line_edit),
            },
            "rope_scaling": self._combo_param(
                self.enable_rope_scaling_checkbox, self.rope_scaling_combobox
            ),
            "rope_freq_base": self._param(
                self.enable_rope_freq_base_checkbox, self.rope_freq_base_spinbox
            ),
            "rope_freq_scale": self._param(
                self.enable_rope_freq_scale_checkbox, self.rope_freq_scale_spinbox
            ),
        }

        # Other settings
        config["context_size"] = self.model_context_size.itemData(
            self.model_context_size.currentIndex(), None
        )
        config["more_options"] = self.more_options_line_edit.text()
        config["no_mmproj_offload"] = self.no_mmproj_offload_checkbox.isChecked()

        return config
