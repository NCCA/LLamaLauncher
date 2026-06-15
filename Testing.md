# Testing Plan for LLamaLauncher

## Overview

This document outlines the phased approach to achieving >90% test coverage on the LLamaLauncher project. Tests should be written **before** implementation code following TDD principles (Red-Green-Refactor).

### Current State

| Metric | Value |
|--------|-------|
| Total source files | 2 (`main.py`, `ui_loader.py`) |
| Lines of code | ~950 (main.py: 880, ui_loader.py: 69) |
| Existing tests | None |
| Test framework | pytest (in dev dependencies) |
| Target coverage | >90% |

### Prerequisites

Before writing any tests, install the required testing dependencies:

```bash
uv add --dev pytest-qt pytest-cov
```

- **pytest-qt**: Provides fixtures and utilities for Qt application testing
- **pytest-cov**: Generates coverage reports

---

## Phase 1: Foundation (Week 1)

### Goal: Establish test infrastructure and test the smallest, most isolated module first.

### 1.1 Project Setup

- [ x] Create `tests/` directory with `__init__.py`
- [ x] Create `tests/conftest.py` with shared fixtures:
  - `qapp`: QApplication singleton (pytest-qt)
  - `temp_dir`: Temporary directory for test files
  - `mock_qprocess`: Patched QProcess for process tests
- [ x] Configure `pyproject.toml` for pytest and coverage:
  ```toml
  [tool.pytest.ini_options]
  testpaths = ["tests"]
  qt_api = "pyside6"

  [tool.coverage.run]
  source = ["src", "."]
  omit = ["tests/**", "**/conftest.py"]

  [tool.coverage.report]
  exclude_lines = [
      "pragma: no cover",
      "def __repr__",
      "raise NotImplementedError",
      "if TYPE_CHECKING:",
      "@abstractmethod",
  ]
  fail_under = 90
  ```
- [ x] Create `tests/files/` directory for test fixtures (sample JSON configs, etc.)

### 1.2 Test `ui_loader.py` (Priority: Highest)

**Why first?** Small module (69 lines), pure utility function, minimal Qt coupling, easy to mock.

**File:** `tests/test_ui_loader.py`

| # | Test Case | Target Lines | Difficulty |
|---|-----------|-------------|------------|
| 1.2.1 | `load_ui()` raises `RuntimeError` when UI file does not exist | L24-26 | Easy |
| 1.2.2 | `load_ui()` raises `RuntimeError` when UI file fails to open | L24-26 | Medium |
| 1.2.3 | `load_ui()` raises `RuntimeError` when UI file is invalid/empty | L31-32 | Medium |
| 1.2.4 | `load_ui()` assigns widget attributes by `objectName` (QWidget) | L34-37 | Medium |
| 1.2.5 | `load_ui()` assigns layout attributes by `objectName` | L39-42 | Medium |
| 1.2.6 | `load_ui()` captures top-level layout when not found by `findChildren` | L44-49 | Medium |
| 1.2.7 | `load_ui()` sets up QDialog correctly (layout, title, size) | L51-55 | Medium |
| 1.2.8 | `load_ui()` sets up QMainWindow correctly (central widget, title, size) | L56-59 | Medium |
| 1.2.9 | `load_ui()` embeds QWidget via zero-margin layout for non-dialog/mainwindow parents | L60-67 | Medium |
| 1.2.10 | `load_ui()` accepts both `str` and `Path` for `ui_file_path` | L11 | Easy |

**Estimated coverage from this module:** ~7% of total LOC

---

## Phase 2: Configuration Logic (Week 2)

### Goal: Test the pure data transformation logic for configuration save/load.

**Strategy:** Extract configuration methods into a separate testable class or test them by creating a minimal mock widget that mimics the Qt widget interface. This is the highest-value testing work because configuration handling is pure logic with no external side effects.

**File:** `tests/test_config.py`

### 2.1 Configuration Collection (`_collect_config`)

**Target:** Lines 218-291 in main.py

This method collects UI widget values into a dictionary. Test by creating mock widgets.

| # | Test Case | Target Lines | Difficulty |
|---|-----------|-------------|------------|
| 2.1.1 | Collects version string as `"1.0"` | L224 | Easy |
| 2.1.2 | Collects model_path from `fullPath` property | L227-232 | Medium |
| 2.1.3 | Collects mmproj_path, draft_model_path, json_schema_path | L228-232 | Medium |
| 2.1.4 | Handles empty paths as empty strings (not `None`) | L228-232 | Easy |
| 2.1.5 | Collects server host, port (as int), api_key | L235-239 | Medium |
| 2.1.6 | Handles invalid port text (non-digit) as default 8080 | L237 | Medium |
| 2.1.7 | Collects sampling parameters with enabled+value dict format | L242-255 | Hard |
| 2.1.8 | Collects all 11 sampling params (temperature, top_p, top_k, min_p, typical_p, repeat_penalty, repeat_last_n, presence_penalty, frequency_penalty, mirostat, mirostat_lr, mirostat_ent) | L242-255 | Hard |
| 2.1.9 | Collects performance parameters with enabled+value format | L258-272 | Hard |
| 2.1.10 | Collects flash_attn combobox text | L266 | Easy |
| 2.1.11 | Collects mmap, mlock, cont_batching booleans | L269-272 | Easy |
| 2.1.12 | Collects advanced params (draft_model, spec_draft_n_max, seed, grammar, json_schema) | L275-284 | Hard |
| 2.1.13 | Collects rope_scaling combobox text | L281 | Easy |
| 2.1.14 | Collects context_size from UserRole | L287 | Medium |
| 2.1.15 | Collects more_options and no_mmproj_offload | L288-289 | Easy |

### 2.2 Configuration Writing (`_write_config_file`)

**Target:** Lines 204-216

| # | Test Case | Target Lines | Difficulty |
|---|-----------|-------------|------------|
| 2.2.1 | Writes valid JSON to file path | L204-216 | Medium |
| 2.2.2 | Appends success message to output_display | L214 | Easy |
| 2.2.3 | Shows QMessageBox.critical on write failure (permission denied) | L215-216 | Hard (requires mocking filesystem) |

### 2.3 Configuration Loading (`_load_config`)

**Target:** Lines 293-313

| # | Test Case | Target Lines | Difficulty |
|---|-----------|-------------|------------|
| 2.3.1 | Loads valid JSON config and calls `_apply_config` | L293-313 | Hard |
| 2.3.2 | Handles json.JSONDecodeError with error dialog | L310-311 | Medium |
| 2.3.3 | Handles general file read errors with error dialog | L312-313 | Easy |

### 2.4 Configuration Application (`_apply_config`)

**Target:** Lines 315-420

This is a large method (~105 lines). Break into focused tests:

| # | Test Case | Target Lines | Difficulty |
|---|-----------|-------------|------------|
| 2.4.1 | Applies files section (model_path, mmproj_path, draft_model_path, json_schema_path) | L322-327 | Medium |
| 2.4.2 | Applies server section (host, port, api_key) with defaults | L330-335 | Medium |
| 2.4.3 | Applies all sampling parameters via `_apply_param` | L338-351 | Hard |
| 2.4.4 | Applies performance parameters (gpu_layers, threads, etc.) | L354-362 | Hard |
| 2.4.5 | Applies flash_attn combobox selection | L364-368 | Easy |
| 2.4.6 | Applies cache_type_k/v combo params via `_apply_combo_param` | L370-371 | Medium |
| 2.4.7 | Applies mmap, mlock, cont_batching booleans | L373-378 | Easy |
| 2.4.8 | Applies advanced section (spec_draft_n_max, seed) | L381-384 | Medium |
| 2.4.9 | Applies draft_model path-based params (enabled + path) | L386-390 | Medium |
| 2.4.10 | Applies grammar path-based params | L392-396 | Medium |
| 2.4.11 | Applies json_schema path-based params | L398-402 | Medium |
| 2.4.12 | Applies rope_scaling combo param | L404 | Easy |
| 2.4.13 | Applies context_size selection | L409-414 | Medium |
| 2.4.14 | Applies more_options and no_mmproj_offload | L416-420 | Easy |
| 2.4.15 | Handles missing config sections gracefully (no errors) | L322, L330, etc. | Easy |

### 2.5 Helper Methods

**Target:** Lines 422-477

| # | Test Case | Target Lines | Difficulty |
|---|-----------|-------------|------------|
| 2.5.1 | `_set_path_field` sets fullPath property and displays short filename | L422-434 | Easy |
| 2.5.2 | `_set_path_field` handles empty path (clears field) | L432-434 | Easy |
| 2.5.3 | `_apply_param` applies enabled+value dict format | L436-453 | Medium |
| 2.5.4 | `_apply_param` handles legacy format (just a value, not dict) | L450-453 | Medium |
| 2.5.5 | `_apply_combo_param` applies enabled+value dict format for combobox | L455-477 | Medium |
| 2.5.6 | `_apply_combo_param` handles legacy format for combobox | L472-477 | Easy |

**Estimated coverage from this phase:** ~30% of total LOC (cumulative: ~37%)

---

## Phase 3: Process Command Building (Week 3)

### Goal: Test the logic that constructs the `llama-server` command line.

**File:** `tests/test_process.py`

This is one of the most critical parts of the application. The `_launch_model` method (L647-818) builds a complex command with conditional parameters based on UI state.

### 3.1 Base Command

| # | Test Case | Target Lines | Difficulty |
|---|-----------|-------------|------------|
| 3.1.1 | Base command includes `llama-server` and `--model` | L697-699 | Easy |
| 3.1.2 | Base command includes `--api-key` | L700-701 | Easy |

### 3.2 Sampling Parameters (Conditional)

Each sampling param is gated by its checkbox. Test enabled/disabled pairs:

| # | Test Case | Target Lines | Difficulty |
|---|-----------|-------------|------------|
| 3.2.1 | Includes `--temp` when temperature checkbox is checked | L704-705 | Medium |
| 3.2.2 | Omits `--temp` when temperature checkbox is unchecked | L704-705 | Medium |
| 3.2.3 | Includes `--top-p` when top_p checkbox is checked | L706-707 | Medium |
| 3.2.4 | Includes `--top-k` when top_k checkbox is checked | L708-709 | Medium |
| 3.2.5 | Includes `--min-p` when min_p checkbox is checked | L710-711 | Medium |
| 3.2.6 | Includes `--typical-p` when typical_p checkbox is checked | L712-713 | Medium |
| 3.2.7 | Includes `--repeat-penalty` when repeat_penalty checkbox is checked | L714-715 | Medium |
| 3.2.8 | Includes `--repeat-last-n` when repeat_last_n checkbox is checked | L716-717 | Medium |
| 3.2.9 | Includes `--presence-penalty` when presence_penalty checkbox is checked | L718-719 | Medium |
| 3.2.10 | Includes `--frequency-penalty` when frequency_penalty checkbox is checked | L720-721 | Medium |
| 3.2.11 | Includes `--mirostat`, `--mirostat-lr`, `--mirostat-ent` when mirostat params are checked | L722-727 | Hard |

### 3.3 Performance Parameters (Conditional)

| # | Test Case | Target Lines | Difficulty |
|---|-----------|-------------|------------|
| 3.3.1 | Includes `--n-gpu-layers` when gpu_layers checkbox is checked | L730-731 | Medium |
| 3.3.2 | Includes `--threads` when threads checkbox is checked | L732-733 | Medium |
| 3.3.3 | Includes `--threads-batch` when threads_batch checkbox is checked | L734-735 | Medium |
| 3.3.4 | Includes `--batch-size` when batch_size checkbox is checked | L736-737 | Medium |
| 3.3.5 | Includes `--ubatch-size` when ubatch_size checkbox is checked | L738-739 | Medium |
| 3.3.6 | Includes `--n-predict` when n_predict checkbox is checked | L740-741 | Medium |
| 3.3.7 | Always includes `--flash-attn` with selected value (default auto) | L743-744 | Medium |
| 3.3.8 | Includes `--cache-type-k` when cache_type_k checkbox is checked | L745-746 | Medium |
| 3.3.9 | Includes `--cache-type-v` when cache_type_v checkbox is checked | L747-748 | Medium |
| 3.3.10 | Includes `--mmap` flag when mmap checkbox is checked | L749-750 | Medium |
| 3.3.11 | Includes `--mlock` flag when mlock checkbox is checked | L751-752 | Medium |
| 3.3.12 | Includes `--cont-batching` flag when cont_batching checkbox is checked | L753-754 | Medium |
| 3.3.13 | Includes `--parallel` when parallel checkbox is checked | L755-756 | Medium |

### 3.4 Advanced Generation Parameters (Conditional)

| # | Test Case | Target Lines | Difficulty |
|---|-----------|-------------|------------|
| 3.4.1 | Includes `--draft-model` when draft model checkbox is checked AND path is set | L759-761 | Medium |
| 3.4.2 | Omits `--draft-model` when draft model path is empty | L760 | Medium |
| 3.4.3 | Includes `--spec-draft-n-max` when checkbox is checked | L762-763 | Medium |
| 3.4.4 | Includes `--seed` when seed checkbox is checked | L764-765 | Medium |
| 3.4.5 | Includes `--grammar` when grammar checkbox is checked AND text is provided | L766-768 | Medium |
| 3.4.6 | Omits `--grammar` when grammar text is empty | L767 | Medium |
| 3.4.7 | Includes `--json-schema` when json_schema checkbox is checked AND path is set | L769-771 | Medium |
| 3.4.8 | Omits `--json-schema` when json_schema path is empty | L770 | Medium |
| 3.4.9 | Includes `--rope-scaling` when checkbox is checked | L772-773 | Medium |
| 3.4.10 | Includes `--rope-freq-base` when checkbox is checked | L774-775 | Medium |
| 3.4.11 | Includes `--rope-freq-scale` when checkbox is checked | L776-777 | Medium |

### 3.5 Server and Model Parameters

| # | Test Case | Target Lines | Difficulty |
|---|-----------|-------------|------------|
| 3.5.1 | Uses host from line_edit or falls back to default `_host` | L779 | Easy |
| 3.5.2 | Uses port from line_edit or falls back to default `_port` | L780-784 | Medium |
| 3.5.3 | Handles invalid port text (ValueError) by falling back to default | L781-784 | Medium |
| 3.5.4 | Includes `--mmproj` when mmproj_path is set | L786-787 | Medium |
| 3.5.5 | Includes `--no-mmproj-offload` when mmproj is set AND checkbox is checked | L788-789 | Medium |
| 3.5.6 | Parses extra flags from more_options line edit via `.split()` | L792-794 | Easy |
| 3.5.7 | Includes `--ctx-size` only when context size > 0 | L797-802 | Medium |
| 3.5.8 | Omits `--ctx-size` when context size is 0 (Auto) | L801 | Easy |
| 3.5.9 | Includes `--host` and `--port` at end of command | L804 | Easy |

### 3.6 Process Launch Side Effects

| # | Test Case | Target Lines | Difficulty |
|---|-----------|-------------|------------|
| 3.6.1 | Sets `_server_url` after building command | L806 | Easy |
| 3.6.2 | Clears output_display before launching | L809 | Easy |
| 3.6.3 | Appends launch command to output_display | L810 | Easy |
| 3.6.4 | Calls `_process.start()` with correct program and args list | L813 | Medium |
| 3.6.5 | Updates launch_button text to "STOP" | L814 | Easy |
| 3.6.6 | Updates web view URL after launch | L817-818 | Easy |

**Estimated coverage from this phase:** ~25% of total LOC (cumulative: ~62%)

---

## Phase 4: Path Selection Methods (Week 4)

### Goal: Test the file dialog selection methods.

**File:** `tests/test_file_selection.py`

These methods open file dialogs and set properties on line edits. They can be tested by mocking `QFileDialog.getOpenFileName`.

**Target:** Lines 541-610 in main.py

| # | Test Case | Target Lines | Difficulty |
|---|-----------|-------------|------------|
| 4.1 | `_select_model` opens dialog and sets fullPath + short filename on model_path_edit | L541-558 | Medium |
| 4.2 | `_select_mmproj` opens dialog and sets fullPath + short filename on mmproj_path_edit | L560-576 | Medium |
| 4.3 | `_select_draft_model` opens dialog and sets fullPath + short filename on draft_model_line_edit | L578-593 | Medium |
| 4.4 | `_select_json_schema` opens dialog and sets fullPath + short filename on json_schema_line_edit | L595-610 | Medium |
| 4.5 | `_on_model_selection_changed` enables launch button when model is selected | L612-616 | Easy |
| 4.6 | `_on_model_selection_changed` disables launch button when no model or process running | L614-616 | Medium |

**Estimated coverage from this phase:** ~5% of total LOC (cumulative: ~67%)

---

## Phase 5: Signal Handling and UI Logic (Week 5)

### Goal: Test the remaining signal handlers and UI logic.

**File:** `tests/test_signals.py`

| # | Test Case | Target Lines | Difficulty |
|---|-----------|-------------|------------|
| 5.1 | `_toggle_launch` calls `_stop_model` when process is running | L618-621 | Easy |
| 5.2 | `_toggle_launch` calls `_launch_model` when process is not running | L622-623 | Easy |
| 5.3 | `_stop_model` calls `terminate()` on process and shows message | L625-634 | Medium |
| 5.4 | `_force_kill_if_needed` calls `kill()` if process doesn't stop in time | L636-640 | Hard (requires timing) |
| 5.5 | `_reset_launch_button` resets button text to "LAUNCH" | L642-645 | Easy |
| 5.6 | `_on_stdout` reads stdout data and appends to output_display | L824-833 | Medium |
| 5.7 | `_on_stdout` calls `_check_and_refresh` after appending data | L833 | Easy |
| 5.8 | `_on_stderr` reads stderr data and appends to output_display | L835-844 | Medium |
| 5.9 | `_on_stderr` calls `_check_and_refresh` after appending data | L844 | Easy |
| 5.10 | `_check_and_refresh` does nothing if `_auto_refresh_done` is True | L853-854 | Easy |
| 5.11 | `_check_and_refresh` schedules `_refresh_web_view` when URL pattern found | L856-860 | Medium |
| 5.12 | `_check_and_refresh` does nothing when no URL pattern found | L857-858 | Easy |
| 5.13 | `_refresh_web_view` sets web view URL and appends ready message | L862-866 | Medium |
| 5.14 | `_on_error` appends error message and resets launch button | L868-872 | Easy |
| 5.15 | `_on_finished` shows normal exit message | L874-880 | Medium |
| 5.16 | `_on_finished` shows abnormal termination message | L876-879 | Medium |
| 5.17 | `_on_finished` resets launch button after process exits | L880 | Easy |

**Estimated coverage from this phase:** ~20% of total LOC (cumulative: ~87%)

---

## Phase 6: Initialization and Lifecycle (Week 6)

### Goal: Test initialization methods and window lifecycle.

**File:** `tests/test_lifecycle.py`

| # | Test Case | Target Lines | Difficulty |
|---|-----------|-------------|------------|
| 6.1 | `_create_cache_dir` creates cache directory and returns Path | L60-68 | Easy |
| 6.2 | `_create_persistent_profile` creates QWebEngineProfile with correct settings | L70-94 | Hard (requires Qt event loop) |
| 6.3 | `_init_web_view` creates QWebEnginePage with profile and sets URL | L96-105 | Medium |
| 6.4 | `_setup_context_size_combo` populates all 8 context size options | L119-152 | Hard |
| 6.5 | `_setup_context_size_combo` pre-selects from CLI ctx_size if provided | L144-152 | Medium |
| 6.6 | `_setup_context_size_combo` defaults to 16K when no CLI ctx_size | L146-152 | Medium |
| 6.7 | `_create_file_menu` creates File menu with Save, Save As, Load actions | L158-179 | Medium |
| 6.8 | `_save_config` calls `_save_config_as` when no `_last_config_path` exists | L186-190 | Easy |
| 6.9 | `_save_config` writes to last saved path when it exists | L187-190 | Medium |
| 6.10 | `_save_config_as` prompts for path and writes config | L192-202 | Hard (requires mocking file dialog) |
| 6.11 | `_save_last_session` saves model path, host, port, window geometry | L492-498 | Medium |
| 6.12 | `_load_last_session` restores host, port, model path from QSettings | L500-522 | Medium |
| 6.13 | `_load_last_session` restores window geometry | L508-511 | Hard (requires Qt) |
| 6.14 | `closeEvent` calls `_save_last_session` before closing | L483-490 | Easy |
| 6.15 | `_connect_signals` wires up all button clicks and signals | L528-535 | Medium |

**Estimated coverage from this phase:** ~8% of total LOC (cumulative: ~95%)

---

## Phase 7: Edge Cases and Error Handling (Week 7)

### Goal: Test error paths, edge cases, and robustness.

**File:** `tests/test_edge_cases.py`

| # | Test Case | Target Lines | Difficulty |
|---|-----------|-------------|------------|
| 7.1 | `_launch_model` handles missing model file gracefully (process will fail, but command is still built) | L647-818 | Medium |
| 7.2 | API key defaults to `"12345"` when line edit is empty | L693 | Easy |
| 7.3 | `_apply_param` uses spinbox default value when config dict lacks "value" key | L449 | Medium |
| 7.4 | `_apply_combo_param` does nothing when combobox doesn't find text match | L469-471 | Medium |
| 7.5 | `_collect_config` handles missing optional sections without error | L218-291 | Easy |
| 7.6 | `_on_stdout` handles empty data (no append) | L830-831 | Easy |
| 7.7 | `_on_stderr` handles empty data (no append) | L841-842 | Easy |
| 7.8 | `_check_and_refresh` regex matches various URL formats | L857 | Medium |
| 7.9 | `__init__` initializes `_process` with correct signal connections | L32-54 | Hard |

---

## Phase 8: Integration Tests (Week 8)

### Goal: End-to-end tests that exercise multiple components together.

**File:** `tests/test_integration.py`

These tests require a full Qt application context and will be the slowest to run.

| # | Test Case | Target Lines | Difficulty |
|---|-----------|-------------|------------|
| 8.1 | Full config round-trip: collect -> save -> load -> verify values match | L218-420 | Hard |
| 8.2 | Legacy config format (pre-v1.0) is handled gracefully on load | L315-420 | Hard |
| 8.3 | Application starts with CLI host/port overrides | L32-54 | Hard |
| 8.4 | Launch sequence: model selected -> launch -> process started -> button updates | L612-818 | Very Hard |
| 8.5 | Stop sequence: process running -> stop -> SIGTERM sent -> button resets | L618-645 | Very Hard |

---

## Summary of Estimated Coverage

| Phase | Module/Feature | Estimated LOC Coverage | Cumulative |
|-------|---------------|----------------------|------------|
| 1 | ui_loader.py | ~7% | ~7% |
| 2 | Configuration logic | ~30% | ~37% |
| 3 | Process command building | ~25% | ~62% |
| 4 | Path selection methods | ~5% | ~67% |
| 5 | Signal handling | ~20% | ~87% |
| 6 | Initialization and lifecycle | ~8% | ~95% |
| 7 | Edge cases | ~3% | ~98% |
| 8 | Integration tests | N/A (behavioral) | - |

**Total estimated coverage: ~95%** (exceeds the >90% target)

---

## Testing Strategy Notes

### What to Test First

Follow this priority order:

1. **Pure functions first** (config collection, command building) - easiest to test, highest ROI
2. **Small utilities second** (ui_loader.py) - quick wins, establishes testing patterns
3. **Signal handlers third** - requires Qt fixtures but no external dependencies
4. **Integration last** - slowest, most fragile, lowest ROI per hour spent

### How to Test Qt Code

Since this is a PySide6 application with heavy GUI coupling:

1. **Use pytest-qt fixtures**: `qapp`, `qtbot` for widget interaction testing
2. **Mock QFileDialog**: Use `unittest.mock.patch` for file dialog methods
3. **Mock QProcess**: Mock `.start()`, `.state()`, `.terminate()`, `.kill()` methods
4. **Mock QSettings**: Use `unittest.mock.patch` or a fake implementation
5. **Test data flow, not UI pixels**: Verify that widget values are read/written correctly, not visual appearance

### Refactoring Recommendations for Testability

The current codebase has significant testability challenges. Consider these refactors during testing:

1. **Extract ConfigurationManager class** (from `_collect_config`, `_apply_config`, `_write_config_file`, `_load_config`) - currently 200+ lines of pure logic mixed with Qt widgets
2. **Extract CommandBuilder class** (from `_launch_model` command construction) - currently 150+ lines of conditional logic
3. **Extract SessionManager class** (from `_save_last_session`, `_load_last_session`) - QSettings interaction

These refactors would:
- Increase testability dramatically (pure classes vs. QMainWindow)
- Reduce coupling between UI and business logic
- Make TDD much easier going forward
- Not change any external behavior

### Coverage Measurement

Run coverage after each phase:

```bash
uv run pytest --cov=. --cov-report=term-missing
```

Review the output to identify untested lines and adjust test priorities accordingly.

---

## Test File Structure

```
tests/
├── __init__.py
├── conftest.py                    # Shared fixtures (qapp, temp_dir, mocks)
├── files/                         # Test fixtures (sample configs, etc.)
│   ├── sample_config.json
│   └── invalid_config.json
├── test_ui_loader.py              # Phase 1
├── test_config.py                 # Phase 2
├── test_process.py                # Phase 3
├── test_file_selection.py         # Phase 4
├── test_signals.py                # Phase 5
├── test_lifecycle.py              # Phase 6
├── test_edge_cases.py             # Phase 7
└── test_integration.py            # Phase 8
```

---

## Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage report
uv run pytest --cov=. --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_ui_loader.py -v

# Run specific test case
uv run pytest tests/test_config.py::test_collects_version -v

# Run tests matching pattern
uv run pytest -k "sampling" -v

# Watch mode (re-run on changes)
uv run pytest --watch
```

---

## Notes for TDD Implementation

When implementing each test case above:

1. **Write the failing test first** - Do not write production code before the test fails
2. **Verify the test fails correctly** - Ensure it fails for the expected reason (feature missing, not a typo)
3. **Write minimal code to pass** - Only what's needed for this specific test
4. **Verify all tests still pass** - No regressions
5. **Refactor if needed** - Clean up duplication, improve names
6. **Move to next test case**

For existing code (not new features), write tests that capture current behavior first, then use those tests as a safety net for any refactoring.

---

## Future Enhancements (Post-Coverage)

Once >90% coverage is achieved:

- [ ] Add CI pipeline with automated test running
- [ ] Add snapshot testing for UI appearance (if needed)
- [ ] Add performance benchmarks for config handling
- [ ] Consider migrating to pytest-bdd for behavior-driven tests
- [ ] Add integration tests with actual llama-server (in separate CI job)
