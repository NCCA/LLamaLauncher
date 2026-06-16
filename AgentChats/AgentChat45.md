## User

[@test-driven-development](zed:///agent/skill?name=test-driven-development&source=LLamaLauncher&path=%2FVolumes%2Fteaching%2FCode%2FLLamaLauncher%2F.agents%2Fskills%2Ftest-driven-development%2FSKILL.md) [@pytest-best-practices](zed:///agent/skill?name=pytest-best-practices&source=LLamaLauncher&path=%2FVolumes%2Fteaching%2FCode%2FLLamaLauncher%2F.agents%2Fskills%2Fpytest-best-practices%2FSKILL.md) [@Testing.md (260:270)](file:///Volumes/teaching/Code/LLamaLauncher/Testing.md#L260:270) implement the tests

## Assistant

<thinking>
I need to understand the task better by reading the Testing.md file and the source code to see what needs to be tested. Let me start by reading the relevant sections.

</thinking>

Let me start by understanding the context - the testing requirements and the source code that needs tests.



**Tool Call: Read file**
Status: Failed

```json
{
  "Text": "Path Volumes/teaching/Code/LLamaLauncher/Testing.md is not in the project"
}
```

**Tool Call: Search files for regex `class.*ServerManager|def _build_command|def launch_server|def stop_server|_server_url|output_display|launch_button|web_view`**
Status: Completed

Showing matches 1-20 (there were more matches found; use offset: 20 to see next page):

## Matches in LLamaLauncher/.worktrees/process-command-builder/main.py

### class LlamaLaunchApp › def __init__ › L38-48
```
        super().__init__()
        self._process = QProcess(self)
        self._process.readyReadStandardOutput.connect(self._on_stdout)
        self._process.readyReadStandardError.connect(self._on_stderr)
        self._process.finished.connect(self._on_finished)
        self._process.errorOccurred.connect(self._on_error)
        self._host = host
        self._port = port
        self._server_url: str = f"http://{host}:{port}"
        self._auto_refresh_done: bool = False
        self._cache_dir: Path = self._create_cache_dir()
```

6 lines remaining in ancestor node. Read the file to see all.

### class LlamaLaunchApp › def __init__ › L52-56
```
        self._load_last_session()
        self._connect_signals()
        self._init_web_view()

    # ------------------------------------------------------------------
```

### class LlamaLaunchApp › def _init_web_view › L98-109
```
        return profile

    def _init_web_view(self) -> None:
        """Initialize the QWebEngineView in the Server tab.

        Creates a QWebEnginePage with the persistent profile so that
        localStorage, cookies, and IndexedDB are restored from disk.
        """
        page = QWebEnginePage(self._profile, self.server_web_view)
        self.server_web_view.setPage(page)
        url = f"http://{self._host}:{self._port}"
        self.server_web_view.setUrl(url)
```

### class LlamaLaunchApp › def _write_config_file › L216-218
```
            with open(file_path, "w") as f:
                json.dump(config, f, indent=2)
            self.output_display.appendPlainText(f"Configuration saved to {file_path}")
```

### class LlamaLaunchApp › def _load_config › L402-408
```
            with open(file_path, "r") as f:
                config = json.load(f)
            self._apply_config(config)
            self._last_config_path = file_path
            self.output_display.appendPlainText(
                f"Configuration loaded from {file_path}"
            )
```

### class LlamaLaunchApp › def _connect_signals › L750-756
```
        """Connect widget signals to their slot methods."""
        self.select_model_button.clicked.connect(self._select_model)
        self.select_mmproj_button.clicked.connect(self._select_mmproj)
        self.select_draft_model_button.clicked.connect(self._select_draft_model)
        self.select_json_schema_button.clicked.connect(self._select_json_schema)
        self.model_path_edit.textChanged.connect(self._on_model_selection_changed)
        self.launch_button.clicked.connect(self._toggle_launch)
```

### class LlamaLaunchApp › def _on_model_selection_changed › L834-837
```
        """Enable launch button when a model is selected, disable otherwise."""
        has_model = bool(self.model_path_edit.property("fullPath"))
        is_running = self._process.state() == QProcess.Running
        self.launch_button.setEnabled(has_model and not is_running)
```

### class LlamaLaunchApp › def _stop_model › L847-855
```
        """Stop the llama-server gracefully.

        Sends SIGTERM (like pressing Ctrl+C) so the server can shut down
        cleanly. If it does not stop within 2 seconds, falls back to
        SIGKILL.
        """
        self._process.terminate()
        self.output_display.appendPlainText("Stopping server... (sent SIGTERM)")
        QTimer.singleShot(2000, self._force_kill_if_needed)
```

### class LlamaLaunchApp › def _force_kill_if_needed › L859-868
```
        if self._process.state() == QProcess.Running:
            self.output_display.appendPlainText(
                "Server didn't stop gracefully. Force killing..."
            )
            self._process.kill()

    def _reset_launch_button(self) -> None:
        """Reset the launch button to its default state."""
        self.launch_button.setText("LAUNCH")
        self._on_model_selection_changed()
```

### class LlamaLaunchApp › def _launch_model › L871-876
```
        """Launch the llama-server binary with current configuration.

        Builds the command-line arguments from the UI fields and starts
        ``llama-server`` via QProcess.  Live stdout/stderr output is
        streamed into ``output_display``.
        """
```

### class LlamaLaunchApp › def _launch_model › L878-880
```
        if not model_path:
            self.output_display.appendPlainText("Error: no model selected.")
            return
```

### class LlamaLaunchApp › def _launch_model › L1029-1045
```
        cmd.extend(["--host", host, "--port", str(port)])

        self._server_url = f"http://{host}:{port}"
        self._auto_refresh_done = False

        self.output_display.clear()
        self.output_display.appendPlainText(f"Launching: {' '.join(cmd)}\n---\n")

        # Use two-argument form: program + arguments list (args must NOT include the program)
        self._process.start(cmd[0], cmd[1:])
        self.launch_button.setText("STOP")

        # Update web view to point to the server
        server_url = f"http://{host}:{port}"
        self.server_web_view.setUrl(server_url)

    # ------------------------------------------------------------------
```

### class LlamaLaunchApp › def _on_stdout › L1060-1062
```
        if data:
            self.output_display.appendPlainText(data)
            self._check_and_refresh()
```

### class LlamaLaunchApp › def _on_stderr › L1075-1077
```
        if data:
            self.output_display.appendPlainText(data)
            self._check_and_refresh()
```

### class LlamaLaunchApp › def _check_and_refresh › L1080-1090
```
        """Check output for server URL and refresh web view once ready.

        Scans the full text of the output display for an HTTP URL pattern.
        When found (and not already refreshed), schedules a one-shot timer
        to reload the web view so the Qt event loop is not blocked.
        """
        if self._auto_refresh_done:
            return

        text = self.output_display.toPlainText()
        match = re.search(r"http://[\w.-]+:\d+", text)
```

3 lines remaining in ancestor node. Read the file to see all.

### class LlamaLaunchApp › def _check_and_refresh › L1092-1101
```
            self._auto_refresh_done = True
            QTimer.singleShot(0, self._refresh_web_view)

    def _refresh_web_view(self) -> None:
        """Reload the server web view to fetch the freshly started server."""
        url = QUrl(self._server_url)
        self.server_web_view.setUrl(url)
        self.output_display.appendPlainText(
            f"\n[Server ready — refreshed web view at {self._server_url}]"
        )
```

### class LlamaLaunchApp › def _on_error › L1104-1107
```
        """Called when the process encounters an error (e.g. not found)."""
        msg = f"Error launching process: {error}"
        self.output_display.appendPlainText(msg)
        self._reset_launch_button()
```

### class LlamaLaunchApp › def _on_finished › L1111-1119
```
        if status == QProcess.ExitStatus.NormalExit:
            self.output_display.appendPlainText(
                f"\n--- Process exited with code {code} ---"
            )
        else:
            self.output_display.appendPlainText(
                f"\n--- Process terminated abnormally (code {code}) ---"
            )
        self._reset_launch_button()
```

## Matches in LLamaLauncher/.worktrees/process-command-builder/tests/test_main.py

### class TestWriteConfigFile › def test_writes_valid_json_to_file_path › L35-39
```
            "server": {"host": "127.0.0.1", "port": 8080},
        }
        app.output_display = MagicMock()

        file_path = tmp_path / "config.json"
```

### class TestWriteConfigFile › def test_appends_success_message_to_output_display › L51-64
```
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

```


## Assistant

<thinking>
The Testing.md file is not in the project at that path. Let me find it properly. Also, I need to look at the main.py file more carefully and understand the structure of the tests directory.

</thinking>

Let me find the correct paths for these files:



**Tool Call: 4 matches**
Status: Completed

file:///Volumes/teaching/Code/LLamaLauncher/.worktrees/process-command-builder/Testing.md

file:///Volumes/teaching/Code/LLamaLauncher/.worktrees/test-launch-model-cmd/Testing.md

file:///Volumes/teaching/Code/LLamaLauncher/.worktrees/test-launch-model-params/Testing.md

file:///Volumes/teaching/Code/LLamaLauncher/Testing.md

**Tool Call: List the `LLamaLauncher` directory's contents**
Status: Completed

# Folders:
LLamaLauncher/.agents
LLamaLauncher/.pytest_cache
LLamaLauncher/.ruff_cache
LLamaLauncher/.venv
LLamaLauncher/.worktrees
LLamaLauncher/AgentChats
LLamaLauncher/__pycache__
LLamaLauncher/docs
LLamaLauncher/tests
LLamaLauncher/ui

# Files:
LLamaLauncher/.gitignore
LLamaLauncher/.python-version
LLamaLauncher/AGENTS.md
LLamaLauncher/README.md
LLamaLauncher/SmallModel.json
LLamaLauncher/TODO.md
LLamaLauncher/Testing.md
LLamaLauncher/headroom_memory.db
LLamaLauncher/main.py
LLamaLauncher/process_command.py
LLamaLauncher/pyproject.toml
LLamaLauncher/pytest-best-practices.md
LLamaLauncher/test.json
LLamaLauncher/ui_loader.py
LLamaLauncher/uv.lock


## Assistant

<thinking>
Good, now I can see the project structure. Let me read the Testing.md file from the correct path and also look at the main.py file to understand what needs to be tested for section 3.6.

</thinking>

Good, now let me read the Testing.md file and the relevant sections of main.py:



**Tool Call: Read file `Testing.md` (lines 250-280)**
Status: Completed

```LLamaLauncher/Testing.md
   250	| 3.5.1 | Uses host from line_edit or falls back to default `_host` | L779 | Easy |
   251	| 3.5.2 | Uses port from line_edit or falls back to default `_port` | L780-784 | Medium |
   252	| 3.5.3 | Handles invalid port text (ValueError) by falling back to default | L781-784 | Medium |
   253	| 3.5.4 | Includes `--mmproj` when mmproj_path is set | L786-787 | Medium |
   254	| 3.5.5 | Includes `--no-mmproj-offload` when mmproj is set AND checkbox is checked | L788-789 | Medium |
   255	| 3.5.6 | Parses extra flags from more_options line edit via `.split()` | L792-794 | Easy |
   256	| 3.5.7 | Includes `--ctx-size` only when context size > 0 | L797-802 | Medium |
   257	| 3.5.8 | Omits `--ctx-size` when context size is 0 (Auto) | L801 | Easy |
   258	| 3.5.9 | Includes `--host` and `--port` at end of command | L804 | Easy |
   259	
   260	### 3.6 Process Launch Side Effects
   261	
   262	| # | Test Case | Target Lines | Difficulty |
   263	|---|-----------|-------------|------------|
   264	| 3.6.1 | Sets `_server_url` after building command | L806 | Easy |
   265	| 3.6.2 | Clears output_display before launching | L809 | Easy |
   266	| 3.6.3 | Appends launch command to output_display | L810 | Easy |
   267	| 3.6.4 | Calls `_process.start()` with correct program and args list | L813 | Medium |
   268	| 3.6.5 | Updates launch_button text to "STOP" | L814 | Easy |
   269	| 3.6.6 | Updates web view URL after launch | L817-818 | Easy |
   270	
   271	**Estimated coverage from this phase:** ~25% of total LOC (cumulative: ~62%)
   272	
   273	---
   274	
   275	## Phase 4: Path Selection Methods (Week 4)
   276	
   277	### Goal: Test the file dialog selection methods.
   278	
   279	**File:** `tests/test_file_selection.py`
   280	

```


**Tool Call: List the `LLamaLauncher/tests` directory's contents**
Status: Completed

# Folders:
LLamaLauncher/tests/__pycache__
LLamaLauncher/tests/files

# Files:
LLamaLauncher/tests/__init__.py
LLamaLauncher/tests/config_collector.py
LLamaLauncher/tests/conftest.py
LLamaLauncher/tests/test_config.py
LLamaLauncher/tests/test_helper_methods.py
LLamaLauncher/tests/test_main.py
LLamaLauncher/tests/test_process.py
LLamaLauncher/tests/test_ui_loader.py


## Assistant

<thinking>
Now I need to read the Testing.md file to see what tests need to be implemented, and also look at the main.py source code to understand what I'm testing. Let me also check if there's a conftest.py and existing test files to understand the project structure.

Let me read:
1. The Testing.md file (the full test plan)
2. The main.py file around lines 800-820 to see the code being tested
3. The existing test_main.py to see current test patterns
4. conftest.py for fixtures

</thinking>

Let me read the Testing.md file and the relevant source code sections:



**Tool Call: Read file `Testing.md`**
Status: Completed

```
SUCCESS: File outline retrieved. This file is too large to read all at once, so the outline below shows the file's structure with line numbers.

IMPORTANT: Do NOT retry this call without line numbers - you will get the same outline.
Instead, use the line numbers below to read specific sections by calling this tool again with start_line and end_line parameters.

# File outline for /Volumes/teaching/Code/LLamaLauncher/Testing.md

# Testing Plan for LLamaLauncher [L1-527]
 ## Overview [L3-30]
  ### Current State [L7-17]
  ### Prerequisites [L17-30]
 ## Phase 1: Foundation (Week 1) [L30-86]
  ### Goal: Establish test infrastructure and test the smallest, most isolated module first. [L32-34]
  ### 1.1 Project Setup [L34-63]
   tool.pytest.ini_options [L43-47]
    testpaths [L44]
    qt_api [L45]
   tool.coverage.run [L47-51]
    source [L48]
    omit [L49]
   tool.coverage.report [L51-60]
    exclude_lines [L52-58]
    fail_under [L59]
  ### 1.2 Test `ui_loader.py` (Priority: Highest) [L63-86]
 ## Phase 2: Configuration Logic (Week 2) [L86-179]
  ### Goal: Test the pure data transformation logic for configuration save/load. [L88-94]
  ### 2.1 Configuration Collection (`_collect_config`) [L94-118]
  ### 2.2 Configuration Writing (`_write_config_file`) [L118-128]
  ### 2.3 Configuration Loading (`_load_config`) [L128-138]
  ### 2.4 Configuration Application (`_apply_config`) [L138-162]
  ### 2.5 Helper Methods [L162-179]
 ## Phase 3: Process Command Building (Week 3) [L179-275]
  ### Goal: Test the logic that constructs the `llama-server` command line. [L181-187]
  ### 3.1 Base Command [L187-194]
  ### 3.2 Sampling Parameters (Conditional) [L194-212]
  ### 3.3 Performance Parameters (Conditional) [L212-230]
  ### 3.4 Advanced Generation Parameters (Conditional) [L230-246]
  ### 3.5 Server and Model Parameters [L246-260]
  ### 3.6 Process Launch Side Effects [L260-275]
 ## Phase 4: Path Selection Methods (Week 4) [L275-298]
  ### Goal: Test the file dialog selection methods. [L277-298]
 ## Phase 5: Signal Handling and UI Logic (Week 5) [L298-328]
  ### Goal: Test the remaining signal handlers and UI logic. [L300-328]
 ## Phase 6: Initialization and Lifecycle (Week 6) [L328-356]
  ### Goal: Test initialization methods and window lifecycle. [L330-356]
 ## Phase 7: Edge Cases and Error Handling (Week 7) [L356-376]
  ### Goal: Test error paths, edge cases, and robustness. [L358-376]
 ## Phase 8: Integration Tests (Week 8) [L376-394]
  ### Goal: End-to-end tests that exercise multiple components together. [L378-394]
 ## Summary of Estimated Coverage [L394-411]
 ## Testing Strategy Notes [L411-458]
  ### What to Test First [L413-422]
  ### How to Test Qt Code [L422-432]
  ### Refactoring Recommendations for Testability [L432-446]
  ### Coverage Measurement [L446-458]
 ## Test File Structure [L458-479]
 ## Running Tests [L479-503]
 ## Notes for TDD Implementation [L503-518]
 ## Future Enhancements (Post-Coverage) [L518-527]

Showing symbols 1-52 (total symbols: 52)


NEXT STEPS: To read a specific symbol's implementation, call read_file with the same path plus start_line and end_line from the outline above.
For example, to read a function shown as [L100-150], use start_line: 100 and end_line: 150.
```


**Tool Call: Read file `tests/conftest.py`**
Status: Completed

```LLamaLauncher/tests/conftest.py
     1	"""Shared pytest fixtures LLamaLauncher test suite."""
     2	
     3	import sys
     4	import tempfile
     5	from pathlib import Path
     6	from unittest.mock import MagicMock, patch
     7	
     8	import pytest
     9	
    10	# Allow importing production modules from project root in tests
    11	_project_root = str(Path(__file__).resolve().parent.parent)
    12	if _project_root not in sys.path:
    13	    sys.path.insert(0, _project_root)
    14	
    15	
    16	@pytest.fixture(scope="session", autouse=True)
    17	def qapp():
    18	    """Provide a QApplication singleton for the test session.
    19	
    20	    This fixture ensures only one QApplication instance is created
    21	    across all Qt tests in the session.
    22	    """
    23	    from PySide6.QtWidgets import QApplication
    24	
    25	    app = QApplication.instance()
    26	    if app is None:
    27	        app = QApplication([])
    28	    yield app
    29	    # Cleanup is handled by QApplication at session end
    30	
    31	
    32	@pytest.fixture()
    33	def temp_dir():
    34	    """Provide a temporary directory that is cleaned up after each test.
    35	
    36	    Returns the path to the temporary directory and removes it afterward.
    37	    """
    38	    with tempfile.TemporaryDirectory() as tmpdir:
    39	        yield tmpdir
    40	
    41	
    42	@pytest.fixture()
    43	def mock_qprocess():
    44	    """Provide a mocked QProcess for testing process-related code.
    45	
    46	    Returns a MagicMock configured to mimic basic QProcess behavior.
    47	    """
    48	    with patch("PySide6.QtCore.QProcess") as mock:
    49	        process = MagicMock()
    50	        process.state.return_value = 0  # NotRunning
    51	        process.readAllStandardOutput.return_value = b""
    52	        process.readAllStandardError.return_value = b""
    53	        mock.return_value = process
    54	        yield process

```


**Tool Call: Read file `tests/test_main.py`**
Status: Completed

```
SUCCESS: File outline retrieved. This file is too large to read all at once, so the outline below shows the file's structure with line numbers.

IMPORTANT: Do NOT retry this call without line numbers - you will get the same outline.
Instead, use the line numbers below to read specific sections by calling this tool again with start_line and end_line parameters.

# File outline for /Volumes/teaching/Code/LLamaLauncher/tests/test_main.py

class TestWriteConfigFile [L21-102]
 def test_writes_valid_json_to_file_path [L24-51]
 def test_appends_success_message_to_output_display [L53-72]
 def test_shows_qmessagebox_critical_on_write_failure [L74-102]
def mock_app [L111-208]
class TestApplyConfig [L216-699]
 def test_2_4_1_applies_files_section [L219-242]
 def test_2_4_1_empty_files_section [L244-257]
 def test_2_4_2_applies_server_section_with_defaults [L259-267]
 def test_2_4_2_applies_server_section_with_custom_values [L269-283]
 def test_2_4_3_applies_sampling_parameters [L285-320]
 def test_2_4_3_sampling_with_legacy_scalar_values [L322-347]
 def test_2_4_4_applies_performance_parameters [L349-378]
 def test_2_4_5_applies_flash_attn_combobox [L380-389]
 def test_2_4_5_flash_attn_not_found [L391-400]
 def test_2_4_6_applies_cache_type_combo_params [L402-424]
 def test_2_4_7_applies_boolean_performance_params [L426-440]
 def test_2_4_8_applies_advanced_section [L442-468]
 def test_2_4_9_applies_draft_model_path_based_params [L470-487]
 def test_2_4_9_draft_model_disabled [L489-499]
 def test_2_4_10_applies_grammar_path_based_params [L501-518]
 def test_2_4_11_applies_json_schema_path_based_params [L520-537]
 def test_2_4_12_applies_rope_scaling_combo_param [L539-554]
 def test_2_4_13_applies_context_size_selection [L556-566]
 def test_2_4_13_context_size_not_found [L568-577]
 def test_2_4_14_applies_more_options_and_no_mmproj_offload [L579-589]
 def test_2_4_14_no_mmproj_offload_false [L591-597]
 def test_2_4_15_handles_missing_config_sections_gracefully [L599-605]
 def test_2_4_15_handles_empty_sections_gracefully [L607-618]
 def test_2_4_applies_all_sections_together [L620-650]
 def test_2_4_sampling_with_disabled_params [L652-672]
 def test_2_4_advanced_with_rope_params [L674-699]

Showing symbols 1-32 (total symbols: 32)


NEXT STEPS: To read a specific symbol's implementation, call read_file with the same path plus start_line and end_line from the outline above.
For example, to read a function shown as [L100-150], use start_line: 100 and end_line: 150.
```


## Assistant

<thinking>
Now I need to understand the structure better. Let me read the Testing.md file for section 3.6 details, and also read the main.py file around lines 800-820 to see the code that needs to be tested.

</thinking>

Now let me read the specific sections I need - the Testing.md phase 3.6 section and the main.py source code around lines 800-820:



**Tool Call: Read file `Testing.md` (lines 260-275)**
Status: Completed

```LLamaLauncher/Testing.md
   260	### 3.6 Process Launch Side Effects
   261	
   262	| # | Test Case | Target Lines | Difficulty |
   263	|---|-----------|-------------|------------|
   264	| 3.6.1 | Sets `_server_url` after building command | L806 | Easy |
   265	| 3.6.2 | Clears output_display before launching | L809 | Easy |
   266	| 3.6.3 | Appends launch command to output_display | L810 | Easy |
   267	| 3.6.4 | Calls `_process.start()` with correct program and args list | L813 | Medium |
   268	| 3.6.5 | Updates launch_button text to "STOP" | L814 | Easy |
   269	| 3.6.6 | Updates web view URL after launch | L817-818 | Easy |
   270	
   271	**Estimated coverage from this phase:** ~25% of total LOC (cumulative: ~62%)
   272	
   273	---
   274	
   275	## Phase 4: Path Selection Methods (Week 4)

```


**Tool Call: Read file `main.py` (lines 790-830)**
Status: Completed

```LLamaLauncher/main.py
   790	            "Select Multi-Modal Projector",
   791	            "",
   792	            "GGUF Files (*.gguf)",
   793	        )
   794	        if file_path:
   795	            self._mmproj_path = file_path
   796	            self.mmproj_path_edit.setProperty("fullPath", file_path)
   797	            self.mmproj_path_edit.setText(file_path.rsplit("/", 1)[-1])
   798	
   799	    def _select_draft_model(self) -> None:
   800	        """Open a file dialog to select a draft model .gguf file.
   801	
   802	        Stores the full path as a custom property on the line edit
   803	        (accessible via ``getProperty("fullPath")``) while displaying
   804	        only the short filename in the UI.
   805	        """
   806	        file_path, _ = QFileDialog.getOpenFileName(
   807	            self,
   808	            "Select Draft Model",
   809	            "",
   810	            "GGUF Files (*.gguf)",
   811	        )
   812	        if file_path:
   813	            self.draft_model_line_edit.setProperty("fullPath", file_path)
   814	            self.draft_model_line_edit.setText(file_path.rsplit("/", 1)[-1])
   815	
   816	    def _select_json_schema(self) -> None:
   817	        """Open a file dialog to select a JSON schema file.
   818	
   819	        Stores the full path as a custom property on the line edit
   820	        (accessible via ``getProperty("fullPath")``) while displaying
   821	        only the short filename in the UI.
   822	        """
   823	        file_path, _ = QFileDialog.getOpenFileName(
   824	            self,
   825	            "Select JSON Schema",
   826	            "",
   827	            "JSON Files (*.json)",
   828	        )
   829	        if file_path:
   830	            self.json_schema_line_edit.setProperty("fullPath", file_path)

```


## Assistant

<thinking>
The user wants me to implement tests for section 3.6 (Process Launch Side Effects) from the Testing.md plan. Let me first understand the code structure by reading the main.py file around the relevant lines, then read the existing test patterns in test_main.py.

I need to:
1. Read the _launch_model method and related code in main.py (around lines 870-900 based on the earlier grep results)
2. Read the existing test_main.py to understand the testing patterns
3. Read the conftest.py for fixtures
4. Then write the tests following TDD principles

Let me first read the relevant source code sections and existing test patterns.

</thinking>

I need to read more context - the actual `_launch_model` method and the existing test patterns in `test_main.py`. Let me gather that information first.



**Tool Call: Read file `tests/test_main.py` (lines 1-220)**
Status: Completed

```LLamaLauncher/tests/test_main.py
     1	"""Tests for LlamaLaunchApp configuration methods.
     2	
     3	Covers _write_config_file and _apply_config behaviour: JSON output,
     4	UI feedback, error handling, and configuration application to widgets.
     5	Uses mocks to isolate the methods from Qt runtime dependencies.
     6	"""
     7	
     8	import json
     9	from pathlib import Path
    10	from unittest.mock import MagicMock, call, patch
    11	
    12	import pytest
    13	
    14	from main import LlamaLaunchApp
    15	
    16	# ==================================================================
    17	# 2.2 Configuration Writing (_write_config_file)
    18	# ==================================================================
    19	
    20	
    21	class TestWriteConfigFile:
    22	    """2.2: Testing _write_config_file method."""
    23	
    24	    def test_writes_valid_json_to_file_path(self, tmp_path: Path) -> None:
    25	        """2.2.1: Writes valid JSON to file path.
    26	
    27	        The method should call _collect_config(), write the result as
    28	        indented JSON to the specified file path, and leave a parseable
    29	        file on disk.
    30	        """
    31	        # Arrange
    32	        app = MagicMock(spec=LlamaLaunchApp)
    33	        app._collect_config.return_value = {
    34	            "version": "1.0",
    35	            "server": {"host": "127.0.0.1", "port": 8080},
    36	        }
    37	        app.output_display = MagicMock()
    38	
    39	        file_path = tmp_path / "config.json"
    40	
    41	        # Act
    42	        LlamaLaunchApp._write_config_file(app, str(file_path))
    43	
    44	        # Assert - file exists and contains valid JSON matching the config
    45	        assert file_path.exists()
    46	        with open(file_path) as f:
    47	            data = json.load(f)
    48	        assert data == {
    49	            "version": "1.0",
    50	            "server": {"host": "127.0.0.1", "port": 8080},
    51	        }
    52	
    53	    def test_appends_success_message_to_output_display(self, tmp_path: Path) -> None:
    54	        """2.2.2: Appends success message to output_display.
    55	
    56	        After a successful write the method should call
    57	        output_display.appendPlainText with a message that includes the
    58	        file path.
    59	        """
    60	        # Arrange
    61	        app = MagicMock(spec=LlamaLaunchApp)
    62	        app._collect_config.return_value = {"test_key": "test_value"}
    63	        app.output_display = MagicMock()
    64	
    65	        file_path = tmp_path / "saved.json"
    66	
    67	        # Act
    68	        LlamaLaunchApp._write_config_file(app, str(file_path))
    69	
    70	        # Assert
    71	        expected_message = f"Configuration saved to {file_path}"
    72	        app.output_display.appendPlainText.assert_called_once_with(expected_message)
    73	
    74	    def test_shows_qmessagebox_critical_on_write_failure(self) -> None:
    75	        """2.2.3: Shows QMessageBox.critical on write failure (permission denied).
    76	
    77	        When the file system raises an exception during writing the method
    78	        should catch it and display a critical dialog with the error message.
    79	        """
    80	        # Arrange
    81	        app = MagicMock(spec=LlamaLaunchApp)
    82	        app._collect_config.return_value = {"should_not_be_written": True}
    83	
    84	        file_path = "/nonexistent/path/config.json"
    85	
    86	        # Mock open to raise PermissionError (simulates permission denied)
    87	        with patch("builtins.open", side_effect=PermissionError("Permission denied")):
    88	            with patch.object(LlamaLaunchApp, "__module__", "main"):
    89	                # QMessageBox is imported into main's namespace at line 19
    90	                with patch("main.QMessageBox") as mock_qmsgbox:
    91	                    # Act
    92	                    LlamaLaunchApp._write_config_file(app, file_path)
    93	
    94	                    # Assert - critical dialog was shown
    95	                    mock_qmsgbox.critical.assert_called_once()
    96	                    call_args = mock_qmsgbox.critical.call_args
    97	                    positional = call_args[0]
    98	
    99	                    assert positional[0] == app  # parent widget
   100	                    assert positional[1] == "Save Error"  # title
   101	                    assert "Failed to save configuration" in positional[2]  # message
   102	                    assert "Permission denied" in positional[2]  # error detail
   103	
   104	
   105	# ==================================================================
   106	# Fixtures for _apply_config tests
   107	# ==================================================================
   108	
   109	
   110	@pytest.fixture
   111	def mock_app():
   112	    """Create a mock LlamaLaunchApp with all required widget attributes.
   113	
   114	    Returns:
   115	        MagicMock configured with mock Qt widgets for _apply_config testing.
   116	    """
   117	    app = MagicMock()
   118	
   119	    # Files/Paths widgets
   120	    app.model_path_edit = MagicMock()
   121	    app.mmproj_path_edit = MagicMock()
   122	    app.draft_model_line_edit = MagicMock()
   123	    app.json_schema_line_edit = MagicMock()
   124	
   125	    # Server widgets
   126	    app.host_line_edit = MagicMock()
   127	    app.port_line_edit = MagicMock()
   128	    app.api_key_line_edit = MagicMock()
   129	
   130	    # Sampling parameters widgets (12 params)
   131	    sampling_params = [
   132	        "temperature",
   133	        "top_p",
   134	        "top_k",
   135	        "min_p",
   136	        "typical_p",
   137	        "repeat_penalty",
   138	        "repeat_last_n",
   139	        "presence_penalty",
   140	        "frequency_penalty",
   141	        "mirostat",
   142	        "mirostat_lr",
   143	        "mirostat_ent",
   144	    ]
   145	    for param in sampling_params:
   146	        checkbox = MagicMock()
   147	        spinbox = MagicMock()
   148	        setattr(app, f"enable_{param}_checkbox", checkbox)
   149	        setattr(app, f"{param}_spinbox", spinbox)
   150	
   151	    # Performance parameters widgets (7 params)
   152	    perf_params = [
   153	        "gpu_layers",
   154	        "threads",
   155	        "threads_batch",
   156	        "batch_size",
   157	        "ubatch_size",
   158	        "n_predict",
   159	        "parallel",
   160	    ]
   161	    for param in perf_params:
   162	        checkbox = MagicMock()
   163	        spinbox = MagicMock()
   164	        setattr(app, f"enable_{param}_checkbox", checkbox)
   165	        setattr(app, f"{param}_spinbox", spinbox)
   166	
   167	    # Performance comboboxes
   168	    app.flash_attn_combobox = MagicMock()
   169	    app.cache_type_k_combobox = MagicMock()
   170	    app.cache_type_v_combobox = MagicMock()
   171	
   172	    # Boolean checkboxes for performance
   173	    app.enable_mmap_checkbox = MagicMock()
   174	    app.enable_mlock_checkbox = MagicMock()
   175	    app.enable_cont_batching_checkbox = MagicMock()
   176	
   177	    # Advanced parameters widgets
   178	    advanced_params = ["spec_draft_n_max", "seed", "rope_freq_base", "rope_freq_scale"]
   179	    for param in advanced_params:
   180	        checkbox = MagicMock()
   181	        spinbox = MagicMock()
   182	        setattr(app, f"enable_{param}_checkbox", checkbox)
   183	        setattr(app, f"{param}_spinbox", spinbox)
   184	
   185	    # Advanced path widgets
   186	    app.grammar_line_edit = MagicMock()
   187	
   188	    # Advanced boolean checkboxes
   189	    app.enable_draft_model_checkbox = MagicMock()
   190	    app.enable_grammar_checkbox = MagicMock()
   191	    app.enable_json_schema_checkbox = MagicMock()
   192	
   193	    # Advanced comboboxes
   194	    app.rope_scaling_combobox = MagicMock()
   195	
   196	    # Context size widget
   197	    app.model_context_size = MagicMock()
   198	
   199	    # Other widgets
   200	    app.more_options_line_edit = MagicMock()
   201	    app.no_mmproj_offload_checkbox = MagicMock()
   202	
   203	    # Helper methods (mocked to track calls)
   204	    app._set_path_field = MagicMock()
   205	    app._apply_param = MagicMock()
   206	    app._apply_combo_param = MagicMock()
   207	
   208	    return app
   209	
   210	
   211	# ==================================================================
   212	# 2.4 Configuration Application (_apply_config)
   213	# ==================================================================
   214	
   215	
   216	class TestApplyConfig:
   217	    """2.4: Testing _apply_config method."""
   218	
   219	    def test_2_4_1_applies_files_section(self, mock_app):
   220	        """2.4.1: Applies files section (model_path, mmproj_path,

```


**Tool Call: Read file `main.py` (lines 870-920)**
Status: Completed

```LLamaLauncher/main.py
   870	    def _launch_model(self) -> None:
   871	        """Launch the llama-server binary with current configuration.
   872	
   873	        Builds the command-line arguments from the UI fields and starts
   874	        ``llama-server`` via QProcess.  Live stdout/stderr output is
   875	        streamed into ``output_display``.
   876	        """
   877	        model_path = self.model_path_edit.property("fullPath")
   878	        if not model_path:
   879	            self.output_display.appendPlainText("Error: no model selected.")
   880	            return
   881	
   882	        temperature = self.temperature_spinbox.value()
   883	        top_p = self.top_p_spinbox.value()
   884	        top_k = self.top_k_spinbox.value()
   885	        min_p = self.min_p_spinbox.value()
   886	        typical_p = self.typical_p_spinbox.value()
   887	        repeat_penalty = self.repeat_penalty_spinbox.value()
   888	        repeat_last_n = self.repeat_last_n_spinbox.value()
   889	        presence_penalty = self.presence_penalty_spinbox.value()
   890	        frequency_penalty = self.frequency_penalty_spinbox.value()
   891	
   892	        mirostat = self.mirostat_spinbox.value()
   893	        mirostat_lr = self.mirostat_lr_spinbox.value()
   894	        mirostat_ent = self.mirostat_ent_spinbox.value()
   895	
   896	        # Performance parameters
   897	        gpu_layers = self.gpu_layers_spinbox.value()
   898	        threads = self.threads_spinbox.value()
   899	        threads_batch = self.threads_batch_spinbox.value()
   900	        batch_size = self.batch_size_spinbox.value()
   901	        ubatch_size = self.ubatch_size_spinbox.value()
   902	        n_predict = self.n_predict_spinbox.value()
   903	        parallel = self.parallel_spinbox.value()
   904	        cache_type_k = self.cache_type_k_combobox.currentText()
   905	        cache_type_v = self.cache_type_v_combobox.currentText()
   906	
   907	        # Advanced Generation parameters
   908	        spec_draft_n_max = self.spec_draft_n_max_spinbox.value()
   909	        seed = self.seed_spinbox.value()
   910	        rope_scaling = self.rope_scaling_combobox.currentText()
   911	        rope_freq_base = self.rope_freq_base_spinbox.value()
   912	        rope_freq_scale = self.rope_freq_scale_spinbox.value()
   913	
   914	        mmproj_path = self.mmproj_path_edit.property("fullPath")
   915	        no_mmproj_offload = self.no_mmproj_offload_checkbox.isChecked()
   916	        api_key = (
   917	            self.api_key_line_edit.text() if self.api_key_line_edit.text() else "12345"
   918	        )
   919	
   920	        # Build command: llama-server --model ... (conditional sampling params) ...

```


## Assistant

<thinking>
Now I need to see the full `_launch_model` method to understand all the side effects being tested. Let me read more of main.py around lines 920-1050 to see the complete method.

</thinking>

Let me continue reading the rest of the `_launch_model` method and also check the Testing.md for the detailed test descriptions:



**Tool Call: Read file `main.py` (lines 920-1050)**
Status: Completed

```LLamaLauncher/main.py
   920	        # Build command: llama-server --model ... (conditional sampling params) ...
   921	        cmd = [
   922	            "llama-server",
   923	            "--model",
   924	            model_path,
   925	            "--api-key",
   926	            api_key,
   927	        ]
   928	
   929	        if self.enable_temperature_checkbox.isChecked():
   930	            cmd.extend(["--temp", str(temperature)])
   931	        if self.enable_top_p_checkbox.isChecked():
   932	            cmd.extend(["--top-p", str(top_p)])
   933	        if self.enable_top_k_checkbox.isChecked():
   934	            cmd.extend(["--top-k", str(top_k)])
   935	        if self.enable_min_p_checkbox.isChecked():
   936	            cmd.extend(["--min-p", str(min_p)])
   937	        if self.enable_typical_p_checkbox.isChecked():
   938	            cmd.extend(["--typical-p", str(typical_p)])
   939	        if self.enable_repeat_penalty_checkbox.isChecked():
   940	            cmd.extend(["--repeat-penalty", str(repeat_penalty)])
   941	        if self.enable_repeat_last_n_checkbox.isChecked():
   942	            cmd.extend(["--repeat-last-n", str(repeat_last_n)])
   943	        if self.enable_presence_penalty_checkbox.isChecked():
   944	            cmd.extend(["--presence-penalty", str(presence_penalty)])
   945	        if self.enable_frequency_penalty_checkbox.isChecked():
   946	            cmd.extend(["--frequency-penalty", str(frequency_penalty)])
   947	        if self.enable_mirostat_checkbox.isChecked():
   948	            cmd.extend(["--mirostat", str(mirostat)])
   949	        if self.enable_mirostat_lr_checkbox.isChecked():
   950	            cmd.extend(["--mirostat-lr", str(mirostat_lr)])
   951	        if self.enable_mirostat_ent_checkbox.isChecked():
   952	            cmd.extend(["--mirostat-ent", str(mirostat_ent)])
   953	
   954	        # Performance parameters
   955	        if self.enable_gpu_layers_checkbox.isChecked():
   956	            cmd.extend(["--n-gpu-layers", str(gpu_layers)])
   957	        if self.enable_threads_checkbox.isChecked():
   958	            cmd.extend(["--threads", str(threads)])
   959	        if self.enable_threads_batch_checkbox.isChecked():
   960	            cmd.extend(["--threads-batch", str(threads_batch)])
   961	        if self.enable_batch_size_checkbox.isChecked():
   962	            cmd.extend(["--batch-size", str(batch_size)])
   963	        if self.enable_ubatch_size_checkbox.isChecked():
   964	            cmd.extend(["--ubatch-size", str(ubatch_size)])
   965	        if self.enable_n_predict_checkbox.isChecked():
   966	            cmd.extend(["--n-predict", str(n_predict)])
   967	        # Flash Attention: always pass the selected value (default auto)
   968	        flash_attn = self.flash_attn_combobox.currentText()
   969	        cmd.extend(["--flash-attn", flash_attn])
   970	        if self.enable_cache_type_k_checkbox.isChecked():
   971	            cmd.extend(["--cache-type-k", cache_type_k])
   972	        if self.enable_cache_type_v_checkbox.isChecked():
   973	            cmd.extend(["--cache-type-v", cache_type_v])
   974	        if self.enable_mmap_checkbox.isChecked():
   975	            cmd.append("--mmap")
   976	        if self.enable_mlock_checkbox.isChecked():
   977	            cmd.append("--mlock")
   978	        if self.enable_cont_batching_checkbox.isChecked():
   979	            cmd.append("--cont-batching")
   980	        if self.enable_parallel_checkbox.isChecked():
   981	            cmd.extend(["--parallel", str(parallel)])
   982	
   983	        # Advanced Generation parameters
   984	        draft_model_path = self.draft_model_line_edit.property("fullPath")
   985	        if self.enable_draft_model_checkbox.isChecked() and draft_model_path:
   986	            cmd.extend(["--draft-model", draft_model_path])
   987	        if self.enable_spec_draft_n_max_checkbox.isChecked():
   988	            cmd.extend(["--spec-draft-n-max", str(spec_draft_n_max)])
   989	        if self.enable_seed_checkbox.isChecked():
   990	            cmd.extend(["--seed", str(seed)])
   991	        grammar_text = self.grammar_line_edit.text().strip()
   992	        if self.enable_grammar_checkbox.isChecked() and grammar_text:
   993	            cmd.extend(["--grammar", grammar_text])
   994	        json_schema_path = self.json_schema_line_edit.property("fullPath")
   995	        if self.enable_json_schema_checkbox.isChecked() and json_schema_path:
   996	            cmd.extend(["--json-schema", json_schema_path])
   997	        if self.enable_rope_scaling_checkbox.isChecked():
   998	            cmd.extend(["--rope-scaling", rope_scaling])
   999	        if self.enable_rope_freq_base_checkbox.isChecked():
  1000	            cmd.extend(["--rope-freq-base", str(rope_freq_base)])
  1001	        if self.enable_rope_freq_scale_checkbox.isChecked():
  1002	            cmd.extend(["--rope-freq-scale", str(rope_freq_scale)])
  1003	
  1004	        host = self.host_line_edit.text() or self._host
  1005	        port_str = self.port_line_edit.text() or str(self._port)
  1006	        try:
  1007	            port = int(port_str)
  1008	        except ValueError:
  1009	            port = self._port
  1010	
  1011	        if mmproj_path:
  1012	            cmd.extend(["--mmproj", mmproj_path])
  1013	            if no_mmproj_offload:
  1014	                cmd.append("--no-mmproj-offload")
  1015	
  1016	        # Extra user-supplied flags from the more options line edit
  1017	        extra = self.more_options_line_edit.text().strip()
  1018	        if extra:
  1019	            cmd.extend(extra.split())
  1020	
  1021	        # Context size: only pass --ctx-size when a specific value is selected
  1022	        ctx_size = self.model_context_size.itemData(
  1023	            self.model_context_size.currentIndex(),
  1024	            Qt.UserRole,
  1025	        )
  1026	        if ctx_size is not None and int(ctx_size) > 0:
  1027	            cmd.extend(["--ctx-size", str(ctx_size)])
  1028	
  1029	        cmd.extend(["--host", host, "--port", str(port)])
  1030	
  1031	        self._server_url = f"http://{host}:{port}"
  1032	        self._auto_refresh_done = False
  1033	
  1034	        self.output_display.clear()
  1035	        self.output_display.appendPlainText(f"Launching: {' '.join(cmd)}\n---\n")
  1036	
  1037	        # Use two-argument form: program + arguments list (args must NOT include the program)
  1038	        self._process.start(cmd[0], cmd[1:])
  1039	        self.launch_button.setText("STOP")
  1040	
  1041	        # Update web view to point to the server
  1042	        server_url = f"http://{host}:{port}"
  1043	        self.server_web_view.setUrl(server_url)
  1044	
  1045	    # ------------------------------------------------------------------
  1046	    # QProcess output slots
  1047	    # ------------------------------------------------------------------
  1048	
  1049	    def _on_stdout(self) -> None:
  1050	        """Append stdout from the child process to the output display.

```


**Tool Call: Search files for regex `3\.6\.\d.*#.*def|3\.6\.\d.*Test.*launch|def test_3_6`**
Status: Completed

No matches found

## Assistant

<thinking>
Now I have a good understanding of the code and what needs to be tested. Let me read the Testing.md file more carefully to see if there are detailed test descriptions for section 3.6, and also check the existing test patterns in test_main.py to understand how to structure these tests.

Let me search for more details about phase 3.6 in the Testing.md file:

</thinking>

Now I have a clear picture. Let me read the Testing.md file more carefully to see if there are detailed test descriptions for section 3.6, and also check the mock_app fixture and existing patterns:



**Tool Call: Search files for regex `### 3\.6|3\.6\.\d.*#|test_3_6`**
Status: Completed

Found 19 matches:

## Matches in LLamaLauncher/.worktrees/process-command-builder/AgentChats/AgentChat31.md

### # Files: › ## Phase 3: Process Command Building (Week 3) › ### 3.5 Server and Model Parameters › L2294-2295
```
### 3.6 Process Launch Side Effects

```

## Matches in LLamaLauncher/.worktrees/process-command-builder/AgentChats/AgentChat32.md

### # Folders: › ## Assistant › L533-537
```
  ### 3.4 Advanced Generation Parameters (Conditional) [L230-246]
  ### 3.5 Server and Model Parameters [L246-260]
  ### 3.6 Process Launch Side Effects [L260-275]
 ## Phase 4: Path Selection Methods (Week 4) [L275-298]
  ### Goal: Test the file dialog selection methods. [L277-298]
```

## Matches in LLamaLauncher/.worktrees/process-command-builder/AgentChats/AgentChat41.md

### ## Assistant › L863-867
```
  ### 3.4 Advanced Generation Parameters (Conditional) [L230-246]
  ### 3.5 Server and Model Parameters [L246-260]
  ### 3.6 Process Launch Side Effects [L260-275]
 ## Phase 4: Path Selection Methods (Week 4) [L275-298]
  ### Goal: Test the file dialog selection methods. [L277-298]
```

## Matches in LLamaLauncher/.worktrees/process-command-builder/Testing.md

### # Testing Plan for LLamaLauncher › ## Phase 3: Process Command Building (Week 3) › ### 3.5 Server and Model Parameters › L260-261
```
### 3.6 Process Launch Side Effects

```

## Matches in LLamaLauncher/.worktrees/test-launch-model-cmd/AgentChats/AgentChat31.md

### # Files: › ## Phase 3: Process Command Building (Week 3) › ### 3.5 Server and Model Parameters › L2294-2295
```
### 3.6 Process Launch Side Effects

```

## Matches in LLamaLauncher/.worktrees/test-launch-model-cmd/AgentChats/AgentChat32.md

### # Folders: › ## Assistant › L533-537
```
  ### 3.4 Advanced Generation Parameters (Conditional) [L230-246]
  ### 3.5 Server and Model Parameters [L246-260]
  ### 3.6 Process Launch Side Effects [L260-275]
 ## Phase 4: Path Selection Methods (Week 4) [L275-298]
  ### Goal: Test the file dialog selection methods. [L277-298]
```

## Matches in LLamaLauncher/.worktrees/test-launch-model-cmd/AgentChats/AgentChat41.md

### ## Assistant › L863-867
```
  ### 3.4 Advanced Generation Parameters (Conditional) [L230-246]
  ### 3.5 Server and Model Parameters [L246-260]
  ### 3.6 Process Launch Side Effects [L260-275]
 ## Phase 4: Path Selection Methods (Week 4) [L275-298]
  ### Goal: Test the file dialog selection methods. [L277-298]
```

## Matches in LLamaLauncher/.worktrees/test-launch-model-cmd/Testing.md

### # Testing Plan for LLamaLauncher › ## Phase 3: Process Command Building (Week 3) › ### 3.5 Server and Model Parameters › L260-261
```
### 3.6 Process Launch Side Effects

```

## Matches in LLamaLauncher/.worktrees/test-launch-model-params/AgentChats/AgentChat31.md

### # Files: › ## Phase 3: Process Command Building (Week 3) › ### 3.5 Server and Model Parameters › L2294-2295
```
### 3.6 Process Launch Side Effects

```

## Matches in LLamaLauncher/.worktrees/test-launch-model-params/AgentChats/AgentChat32.md

### # Folders: › ## Assistant › L533-537
```
  ### 3.4 Advanced Generation Parameters (Conditional) [L230-246]
  ### 3.5 Server and Model Parameters [L246-260]
  ### 3.6 Process Launch Side Effects [L260-275]
 ## Phase 4: Path Selection Methods (Week 4) [L275-298]
  ### Goal: Test the file dialog selection methods. [L277-298]
```

## Matches in LLamaLauncher/.worktrees/test-launch-model-params/AgentChats/AgentChat41.md

### ## Assistant › L863-867
```
  ### 3.4 Advanced Generation Parameters (Conditional) [L230-246]
  ### 3.5 Server and Model Parameters [L246-260]
  ### 3.6 Process Launch Side Effects [L260-275]
 ## Phase 4: Path Selection Methods (Week 4) [L275-298]
  ### Goal: Test the file dialog selection methods. [L277-298]
```

## Matches in LLamaLauncher/.worktrees/test-launch-model-params/AgentChats/AgentChat43.md

### ## Assistant › L854-858
```
   258	| 3.5.9 | Includes `--host` and `--port` at end of command | L804 | Easy |
   259	
   260	### 3.6 Process Launch Side Effects

```
```

## Matches in LLamaLauncher/.worktrees/test-launch-model-params/Testing.md

### # Testing Plan for LLamaLauncher › ## Phase 3: Process Command Building (Week 3) › ### 3.5 Server and Model Parameters › L260-261
```
### 3.6 Process Launch Side Effects

```

## Matches in LLamaLauncher/AgentChats/AgentChat31.md

### # Files: › ## Phase 3: Process Command Building (Week 3) › ### 3.5 Server and Model Parameters › L2294-2295
```
### 3.6 Process Launch Side Effects

```

## Matches in LLamaLauncher/AgentChats/AgentChat32.md

### # Folders: › ## Assistant › L533-537
```
  ### 3.4 Advanced Generation Parameters (Conditional) [L230-246]
  ### 3.5 Server and Model Parameters [L246-260]
  ### 3.6 Process Launch Side Effects [L260-275]
 ## Phase 4: Path Selection Methods (Week 4) [L275-298]
  ### Goal: Test the file dialog selection methods. [L277-298]
```

## Matches in LLamaLauncher/AgentChats/AgentChat41.md

### ## Assistant › L863-867
```
  ### 3.4 Advanced Generation Parameters (Conditional) [L230-246]
  ### 3.5 Server and Model Parameters [L246-260]
  ### 3.6 Process Launch Side Effects [L260-275]
 ## Phase 4: Path Selection Methods (Week 4) [L275-298]
  ### Goal: Test the file dialog selection methods. [L277-298]
```

## Matches in LLamaLauncher/AgentChats/AgentChat43.md

### ## Assistant › L854-858
```
   258	| 3.5.9 | Includes `--host` and `--port` at end of command | L804 | Easy |
   259	
   260	### 3.6 Process Launch Side Effects

```
```

## Matches in LLamaLauncher/AgentChats/AgentChat44.md

### ## Assistant › L56-60
```
   258	| 3.5.9 | Includes `--host` and `--port` at end of command | L804 | Easy |
   259	
   260	### 3.6 Process Launch Side Effects
   261	
   262	| # | Test Case | Target Lines | Difficulty |
```

## Matches in LLamaLauncher/Testing.md

### # Testing Plan for LLamaLauncher › ## Phase 3: Process Command Building (Week 3) › ### 3.5 Server and Model Parameters › L260-261
```
### 3.6 Process Launch Side Effects

```


**Tool Call: Read file `Testing.md` (lines 179-260)**
Status: Completed

```LLamaLauncher/Testing.md
   179	## Phase 3: Process Command Building (Week 3)
   180	
   181	### Goal: Test the logic that constructs the `llama-server` command line.
   182	
   183	**File:** `tests/test_process.py`
   184	
   185	This is one of the most critical parts of the application. The `_launch_model` method (L647-818) builds a complex command with conditional parameters based on UI state.
   186	
   187	### 3.1 Base Command
   188	
   189	| # | Test Case | Target Lines | Difficulty |
   190	|---|-----------|-------------|------------|
   191	| 3.1.1 | Base command includes `llama-server` and `--model` | L697-699 | Easy |
   192	| 3.1.2 | Base command includes `--api-key` | L700-701 | Easy |
   193	
   194	### 3.2 Sampling Parameters (Conditional)
   195	
   196	Each sampling param is gated by its checkbox. Test enabled/disabled pairs:
   197	
   198	| # | Test Case | Target Lines | Difficulty |
   199	|---|-----------|-------------|------------|
   200	| 3.2.1 | Includes `--temp` when temperature checkbox is checked | L704-705 | Medium |
   201	| 3.2.2 | Omits `--temp` when temperature checkbox is unchecked | L704-705 | Medium |
   202	| 3.2.3 | Includes `--top-p` when top_p checkbox is checked | L706-707 | Medium |
   203	| 3.2.4 | Includes `--top-k` when top_k checkbox is checked | L708-709 | Medium |
   204	| 3.2.5 | Includes `--min-p` when min_p checkbox is checked | L710-711 | Medium |
   205	| 3.2.6 | Includes `--typical-p` when typical_p checkbox is checked | L712-713 | Medium |
   206	| 3.2.7 | Includes `--repeat-penalty` when repeat_penalty checkbox is checked | L714-715 | Medium |
   207	| 3.2.8 | Includes `--repeat-last-n` when repeat_last_n checkbox is checked | L716-717 | Medium |
   208	| 3.2.9 | Includes `--presence-penalty` when presence_penalty checkbox is checked | L718-719 | Medium |
   209	| 3.2.10 | Includes `--frequency-penalty` when frequency_penalty checkbox is checked | L720-721 | Medium |
   210	| 3.2.11 | Includes `--mirostat`, `--mirostat-lr`, `--mirostat-ent` when mirostat params are checked | L722-727 | Hard |
   211	
   212	### 3.3 Performance Parameters (Conditional)
   213	
   214	| # | Test Case | Target Lines | Difficulty |
   215	|---|-----------|-------------|------------|
   216	| 3.3.1 | Includes `--n-gpu-layers` when gpu_layers checkbox is checked | L730-731 | Medium |
   217	| 3.3.2 | Includes `--threads` when threads checkbox is checked | L732-733 | Medium |
   218	| 3.3.3 | Includes `--threads-batch` when threads_batch checkbox is checked | L734-735 | Medium |
   219	| 3.3.4 | Includes `--batch-size` when batch_size checkbox is checked | L736-737 | Medium |
   220	| 3.3.5 | Includes `--ubatch-size` when ubatch_size checkbox is checked | L738-739 | Medium |
   221	| 3.3.6 | Includes `--n-predict` when n_predict checkbox is checked | L740-741 | Medium |
   222	| 3.3.7 | Always includes `--flash-attn` with selected value (default auto) | L743-744 | Medium |
   223	| 3.3.8 | Includes `--cache-type-k` when cache_type_k checkbox is checked | L745-746 | Medium |
   224	| 3.3.9 | Includes `--cache-type-v` when cache_type_v checkbox is checked | L747-748 | Medium |
   225	| 3.3.10 | Includes `--mmap` flag when mmap checkbox is checked | L749-750 | Medium |
   226	| 3.3.11 | Includes `--mlock` flag when mlock checkbox is checked | L751-752 | Medium |
   227	| 3.3.12 | Includes `--cont-batching` flag when cont_batching checkbox is checked | L753-754 | Medium |
   228	| 3.3.13 | Includes `--parallel` when parallel checkbox is checked | L755-756 | Medium |
   229	
   230	### 3.4 Advanced Generation Parameters (Conditional)
   231	
   232	| # | Test Case | Target Lines | Difficulty |
   233	|---|-----------|-------------|------------|
   234	| 3.4.1 | Includes `--draft-model` when draft model checkbox is checked AND path is set | L759-761 | Medium |
   235	| 3.4.2 | Omits `--draft-model` when draft model path is empty | L760 | Medium |
   236	| 3.4.3 | Includes `--spec-draft-n-max` when checkbox is checked | L762-763 | Medium |
   237	| 3.4.4 | Includes `--seed` when seed checkbox is checked | L764-765 | Medium |
   238	| 3.4.5 | Includes `--grammar` when grammar checkbox is checked AND text is provided | L766-768 | Medium |
   239	| 3.4.6 | Omits `--grammar` when grammar text is empty | L767 | Medium |
   240	| 3.4.7 | Includes `--json-schema` when json_schema checkbox is checked AND path is set | L769-771 | Medium |
   241	| 3.4.8 | Omits `--json-schema` when json_schema path is empty | L770 | Medium |
   242	| 3.4.9 | Includes `--rope-scaling` when checkbox is checked | L772-773 | Medium |
   243	| 3.4.10 | Includes `--rope-freq-base` when checkbox is checked | L774-775 | Medium |
   244	| 3.4.11 | Includes `--rope-freq-scale` when checkbox is checked | L776-777 | Medium |
   245	
   246	### 3.5 Server and Model Parameters
   247	
   248	| # | Test Case | Target Lines | Difficulty |
   249	|---|-----------|-------------|------------|
   250	| 3.5.1 | Uses host from line_edit or falls back to default `_host` | L779 | Easy |
   251	| 3.5.2 | Uses port from line_edit or falls back to default `_port` | L780-784 | Medium |
   252	| 3.5.3 | Handles invalid port text (ValueError) by falling back to default | L781-784 | Medium |
   253	| 3.5.4 | Includes `--mmproj` when mmproj_path is set | L786-787 | Medium |
   254	| 3.5.5 | Includes `--no-mmproj-offload` when mmproj is set AND checkbox is checked | L788-789 | Medium |
   255	| 3.5.6 | Parses extra flags from more_options line edit via `.split()` | L792-794 | Easy |
   256	| 3.5.7 | Includes `--ctx-size` only when context size > 0 | L797-802 | Medium |
   257	| 3.5.8 | Omits `--ctx-size` when context size is 0 (Auto) | L801 | Easy |
   258	| 3.5.9 | Includes `--host` and `--port` at end of command | L804 | Easy |
   259	
   260	### 3.6 Process Launch Side Effects

```


## Assistant

<thinking>
The user wants me to implement the tests for section 3.6 (Process Launch Side Effects) from the Testing.md plan. Let me understand what I need to do:

1. First, I need to read the Testing.md file more carefully to see if there are detailed descriptions for the 3.6 test cases
2. Read the existing test patterns in test_main.py and test_process.py
3. Understand the _launch_model method in main.py (lines ~870-1043)
4. Create a git worktree before editing
5. Write tests following TDD principles

Let me start by:
1. Reading more of Testing.md to see if there are detailed test descriptions for 3.6


2. Checking the existing test files in test_main.py and test_process.py to understand the current test structure and patterns being used
3. Reviewing main.py around lines 870-1043 to see the _launch_model method implementation

The Testing.md only has a table for 3.6 with basic descriptions, so I'll need to infer what each test should verify based on the method signature and the test case descriptions provided.

</thinking>

Let me read more context - the Testing.md for detailed test descriptions and the existing test patterns:



**Tool Call: Read file `Testing.md` (lines 370-520)**
Status: Completed

````LLamaLauncher/Testing.md
   370	| 7.7 | `_on_stderr` handles empty data (no append) | L841-842 | Easy |
   371	| 7.8 | `_check_and_refresh` regex matches various URL formats | L857 | Medium |
   372	| 7.9 | `__init__` initializes `_process` with correct signal connections | L32-54 | Hard |
   373	
   374	---
   375	
   376	## Phase 8: Integration Tests (Week 8)
   377	
   378	### Goal: End-to-end tests that exercise multiple components together.
   379	
   380	**File:** `tests/test_integration.py`
   381	
   382	These tests require a full Qt application context and will be the slowest to run.
   383	
   384	| # | Test Case | Target Lines | Difficulty |
   385	|---|-----------|-------------|------------|
   386	| 8.1 | Full config round-trip: collect -> save -> load -> verify values match | L218-420 | Hard |
   387	| 8.2 | Legacy config format (pre-v1.0) is handled gracefully on load | L315-420 | Hard |
   388	| 8.3 | Application starts with CLI host/port overrides | L32-54 | Hard |
   389	| 8.4 | Launch sequence: model selected -> launch -> process started -> button updates | L612-818 | Very Hard |
   390	| 8.5 | Stop sequence: process running -> stop -> SIGTERM sent -> button resets | L618-645 | Very Hard |
   391	
   392	---
   393	
   394	## Summary of Estimated Coverage
   395	
   396	| Phase | Module/Feature | Estimated LOC Coverage | Cumulative |
   397	|-------|---------------|----------------------|------------|
   398	| 1 | ui_loader.py | ~7% | ~7% |
   399	| 2 | Configuration logic | ~30% | ~37% |
   400	| 3 | Process command building | ~25% | ~62% |
   401	| 4 | Path selection methods | ~5% | ~67% |
   402	| 5 | Signal handling | ~20% | ~87% |
   403	| 6 | Initialization and lifecycle | ~8% | ~95% |
   404	| 7 | Edge cases | ~3% | ~98% |
   405	| 8 | Integration tests | N/A (behavioral) | - |
   406	
   407	**Total estimated coverage: ~95%** (exceeds the >90% target)
   408	
   409	---
   410	
   411	## Testing Strategy Notes
   412	
   413	### What to Test First
   414	
   415	Follow this priority order:
   416	
   417	1. **Pure functions first** (config collection, command building) - easiest to test, highest ROI
   418	2. **Small utilities second** (ui_loader.py) - quick wins, establishes testing patterns
   419	3. **Signal handlers third** - requires Qt fixtures but no external dependencies
   420	4. **Integration last** - slowest, most fragile, lowest ROI per hour spent
   421	
   422	### How to Test Qt Code
   423	
   424	Since this is a PySide6 application with heavy GUI coupling:
   425	
   426	1. **Use pytest-qt fixtures**: `qapp`, `qtbot` for widget interaction testing
   427	2. **Mock QFileDialog**: Use `unittest.mock.patch` for file dialog methods
   428	3. **Mock QProcess**: Mock `.start()`, `.state()`, `.terminate()`, `.kill()` methods
   429	4. **Mock QSettings**: Use `unittest.mock.patch` or a fake implementation
   430	5. **Test data flow, not UI pixels**: Verify that widget values are read/written correctly, not visual appearance
   431	
   432	### Refactoring Recommendations for Testability
   433	
   434	The current codebase has significant testability challenges. Consider these refactors during testing:
   435	
   436	1. **Extract ConfigurationManager class** (from `_collect_config`, `_apply_config`, `_write_config_file`, `_load_config`) - currently 200+ lines of pure logic mixed with Qt widgets
   437	2. **Extract CommandBuilder class** (from `_launch_model` command construction) - currently 150+ lines of conditional logic
   438	3. **Extract SessionManager class** (from `_save_last_session`, `_load_last_session`) - QSettings interaction
   439	
   440	These refactors would:
   441	- Increase testability dramatically (pure classes vs. QMainWindow)
   442	- Reduce coupling between UI and business logic
   443	- Make TDD much easier going forward
   444	- Not change any external behavior
   445	
   446	### Coverage Measurement
   447	
   448	Run coverage after each phase:
   449	
   450	```bash
   451	uv run pytest --cov=. --cov-report=term-missing
   452	```
   453	
   454	Review the output to identify untested lines and adjust test priorities accordingly.
   455	
   456	---
   457	
   458	## Test File Structure
   459	
   460	```
   461	tests/
   462	├── __init__.py
   463	├── conftest.py                    # Shared fixtures (qapp, temp_dir, mocks)
   464	├── files/                         # Test fixtures (sample configs, etc.)
   465	│   ├── sample_config.json
   466	│   └── invalid_config.json
   467	├── test_ui_loader.py              # Phase 1
   468	├── test_config.py                 # Phase 2
   469	├── test_process.py                # Phase 3
   470	├── test_file_selection.py         # Phase 4
   471	├── test_signals.py                # Phase 5
   472	├── test_lifecycle.py              # Phase 6
   473	├── test_edge_cases.py             # Phase 7
   474	└── test_integration.py            # Phase 8
   475	```
   476	
   477	---
   478	
   479	## Running Tests
   480	
   481	```bash
   482	# Run all tests
   483	uv run pytest
   484	
   485	# Run with coverage report
   486	uv run pytest --cov=. --cov-report=term-missing
   487	
   488	# Run specific test file
   489	uv run pytest tests/test_ui_loader.py -v
   490	
   491	# Run specific test case
   492	uv run pytest tests/test_config.py::test_collects_version -v
   493	
   494	# Run tests matching pattern
   495	uv run pytest -k "sampling" -v
   496	
   497	# Watch mode (re-run on changes)
   498	uv run pytest --watch
   499	```
   500	
   501	---
   502	
   503	## Notes for TDD Implementation
   504	
   505	When implementing each test case above:
   506	
   507	1. **Write the failing test first** - Do not write production code before the test fails
   508	2. **Verify the test fails correctly** - Ensure it fails for the expected reason (feature missing, not a typo)
   509	3. **Write minimal code to pass** - Only what's needed for this specific test
   510	4. **Verify all tests still pass** - No regressions
   511	5. **Refactor if needed** - Clean up duplication, improve names
   512	6. **Move to next test case**
   513	
   514	For existing code (not new features), write tests that capture current behavior first, then use those tests as a safety net for any refactoring.
   515	
   516	---
   517	
   518	## Future Enhancements (Post-Coverage)
   519	
   520	Once >90% coverage is achieved:

````


**Tool Call: Read file `tests/test_process.py`**
Status: Completed

```
SUCCESS: File outline retrieved. This file is too large to read all at once, so the outline below shows the file's structure with line numbers.

IMPORTANT: Do NOT retry this call without line numbers - you will get the same outline.
Instead, use the line numbers below to read specific sections by calling this tool again with start_line and end_line parameters.

# File outline for /Volumes/teaching/Code/LLamaLauncher/tests/test_process.py

class TestBaseCommand [L29-67]
 def test_base_command_includes_llama_server_and_model [L32-43]
 def test_base_command_includes_api_key_default_when_empty [L45-55]
 def test_base_command_includes_custom_api_key [L57-67]
class TestTemperatureParameter [L76-101]
 def test_includes_temp_when_temperature_enabled [L79-90]
 def test_omits_temp_when_temperature_disabled [L92-101]
class TestTopPParameter [L104-129]
 def test_includes_top_p_when_enabled [L107-118]
 def test_omits_top_p_when_disabled [L120-129]
class TestTopKParameter [L132-157]
 def test_includes_top_k_when_enabled [L135-146]
 def test_omits_top_k_when_disabled [L148-157]
class TestMinPParameter [L160-185]
 def test_includes_min_p_when_enabled [L163-174]
 def test_omits_min_p_when_disabled [L176-185]
class TestTypicalPParameter [L188-213]
 def test_includes_typical_p_when_enabled [L191-202]
 def test_omits_typical_p_when_disabled [L204-213]
class TestRepeatPenaltyParameter [L216-241]
 def test_includes_repeat_penalty_when_enabled [L219-230]
 def test_omits_repeat_penalty_when_disabled [L232-241]
class TestRepeatLastNParameter [L244-269]
 def test_includes_repeat_last_n_when_enabled [L247-258]
 def test_omits_repeat_last_n_when_disabled [L260-269]
class TestPresencePenaltyParameter [L272-297]
 def test_includes_presence_penalty_when_enabled [L275-286]
 def test_omits_presence_penalty_when_disabled [L288-297]
class TestFrequencyPenaltyParameter [L300-325]
 def test_includes_frequency_penalty_when_enabled [L303-314]
 def test_omits_frequency_penalty_when_disabled [L316-325]
class TestMirostatParameters [L328-379]
 def test_includes_all_mirostat_params_when_enabled [L331-346]
 def test_omits_mirostat_when_disabled [L348-357]
 def test_omits_mirostat_lr_when_disabled [L359-368]
 def test_omits_mirostat_ent_when_disabled [L370-379]
class TestServerHostPort [L387-425]
 def test_uses_host_from_config [L390-400]
 def test_uses_port_from_config [L402-412]
 def test_handles_invalid_port_falls_back_to_default [L414-425]
class TestMmprojParameters [L428-465]
 def test_includes_mmproj_when_path_set [L431-441]
 def test_includes_no_mmproj_offload_when_mmproj_and_checkbox_checked [L443-453]
 def test_omits_no_mmproj_offload_when_checkbox_unchecked [L455-465]
class TestExtraFlags [L468-492]
 def test_parses_extra_flags_from_more_options [L471-481]
 def test_omits_extra_flags_when_empty [L483-492]
class TestContextSize [L495-524]
 def test_includes_ctx_size_when_greater_than_zero [L498-511]
 def test_omits_ctx_size_when_zero [L513-524]

Showing symbols 1-50 (total symbols: 50)


NEXT STEPS: To read a specific symbol's implementation, call read_file with the same path plus start_line and end_line from the outline above.
For example, to read a function shown as [L100-150], use start_line: 100 and end_line: 150.
```


## Assistant

<thinking>
Now I have a clear understanding of the task. I need to implement tests for section 3.6 (Process Launch Side Effects) in the test_process.py file. Let me first create a git worktree as required by the project rules, then read more of the test_process.py to understand the patterns used.

The 6 tests I need to write are:
1. 3.6.1 - Sets `_server_url` after building command (L806/1031)
2. 3.6.2 - Clears output_display before launching (L809/1034)
3. 3.6.3 - Appends launch command to output_display (L810/1035)


4. 3.6.4 - Calls `_process.start()` with correct program and args list (L813/1038)
5. 3.6.5 - Updates launch_button text to "STOP" (L814/1039)
6. 3.6.6 - Updates web view URL after launch (L817-818/1042-1043)

Looking at the actual code in main.py lines 1031-1043, I can see these are side effects that happen after the command is built - the server URL gets set, output display clears and appends the launch command, the process starts with the correct arguments, the launch button text updates to "STOP", and finally the web view URL gets refreshed.

The tests should follow the same pattern as test_process.py, using MagicMock for the app fixture to mock out all the widget dependencies since these are pure side effects after command construction.

</thinking>

Now I have a clear picture of what needs to be done. Let me read the full test_process.py to understand the exact testing patterns used:



**Tool Call: Read file `tests/test_process.py`**
Status: Completed

```
SUCCESS: File outline retrieved. This file is too large to read all at once, so the outline below shows the file's structure with line numbers.

IMPORTANT: Do NOT retry this call without line numbers - you will get the same outline.
Instead, use the line numbers below to read specific sections by calling this tool again with start_line and end_line parameters.

# File outline for /Volumes/teaching/Code/LLamaLauncher/tests/test_process.py

class TestBaseCommand [L29-67]
 def test_base_command_includes_llama_server_and_model [L32-43]
 def test_base_command_includes_api_key_default_when_empty [L45-55]
 def test_base_command_includes_custom_api_key [L57-67]
class TestTemperatureParameter [L76-101]
 def test_includes_temp_when_temperature_enabled [L79-90]
 def test_omits_temp_when_temperature_disabled [L92-101]
class TestTopPParameter [L104-129]
 def test_includes_top_p_when_enabled [L107-118]
 def test_omits_top_p_when_disabled [L120-129]
class TestTopKParameter [L132-157]
 def test_includes_top_k_when_enabled [L135-146]
 def test_omits_top_k_when_disabled [L148-157]
class TestMinPParameter [L160-185]
 def test_includes_min_p_when_enabled [L163-174]
 def test_omits_min_p_when_disabled [L176-185]
class TestTypicalPParameter [L188-213]
 def test_includes_typical_p_when_enabled [L191-202]
 def test_omits_typical_p_when_disabled [L204-213]
class TestRepeatPenaltyParameter [L216-241]
 def test_includes_repeat_penalty_when_enabled [L219-230]
 def test_omits_repeat_penalty_when_disabled [L232-241]
class TestRepeatLastNParameter [L244-269]
 def test_includes_repeat_last_n_when_enabled [L247-258]
 def test_omits_repeat_last_n_when_disabled [L260-269]
class TestPresencePenaltyParameter [L272-297]
 def test_includes_presence_penalty_when_enabled [L275-286]
 def test_omits_presence_penalty_when_disabled [L288-297]
class TestFrequencyPenaltyParameter [L300-325]
 def test_includes_frequency_penalty_when_enabled [L303-314]
 def test_omits_frequency_penalty_when_disabled [L316-325]
class TestMirostatParameters [L328-379]
 def test_includes_all_mirostat_params_when_enabled [L331-346]
 def test_omits_mirostat_when_disabled [L348-357]
 def test_omits_mirostat_lr_when_disabled [L359-368]
 def test_omits_mirostat_ent_when_disabled [L370-379]
class TestServerHostPort [L387-425]
 def test_uses_host_from_config [L390-400]
 def test_uses_port_from_config [L402-412]
 def test_handles_invalid_port_falls_back_to_default [L414-425]
class TestMmprojParameters [L428-465]
 def test_includes_mmproj_when_path_set [L431-441]
 def test_includes_no_mmproj_offload_when_mmproj_and_checkbox_checked [L443-453]
 def test_omits_no_mmproj_offload_when_checkbox_unchecked [L455-465]
class TestExtraFlags [L468-492]
 def test_parses_extra_flags_from_more_options [L471-481]
 def test_omits_extra_flags_when_empty [L483-492]
class TestContextSize [L495-524]
 def test_includes_ctx_size_when_greater_than_zero [L498-511]
 def test_omits_ctx_size_when_zero [L513-524]

Showing symbols 1-50 (total symbols: 50)


NEXT STEPS: To read a specific symbol's implementation, call read_file with the same path plus start_line and end_line from the outline above.
For example, to read a function shown as [L100-150], use start_line: 100 and end_line: 150.
```


## Assistant

<thinking>
The user wants me to implement the tests for section 3.6 (Process Launch Side Effects) from the Testing.md plan. Let me understand what I need to do:

1. Create a git worktree before editing (per project rules)
2. Write tests following TDD principles (write test first, watch it fail, write minimal code to pass)
3. The tests are for the `_launch_model` method side effects in main.py

Let me first read the full test_process.py file to understand the testing patterns used, then create the worktree and implement the tests.

From the outline, I can see:
- Tests use classes like `TestBaseCommand`, `TestTemperatureParameter`, etc.


- Each test class has 1-2 test methods
- The pattern seems to be testing `_launch_model` by creating a mock app and calling the method

Now I need to check if there's an existing worktree for this task and look at the full test_process.py file structure to understand how these tests are organized.

</thinking>

I'll implement the tests for section 3.6 (Process Launch Side Effects). Let me first create a git worktree as required by project rules, then read the full test patterns in test_process.py.



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher && git branch --show-current**
Status: Completed

Terminal:
```
main




```


## Assistant

<thinking>
The user is on the `main` branch. According to project rules, I need to create a git worktree before editing. Let me first read the full test_process.py file to understand the testing patterns, then create the worktree and implement the tests.

Let me read the full test_process.py to understand how tests are structured.

</thinking>

Let me read the full test_process.py file to understand the exact testing patterns used:



**Tool Call: Read file `tests/test_process.py` (lines 1-100)**
Status: Completed

```LLamaLauncher/tests/test_process.py
     1	"""Tests for ProcessCommandBuilder - building llama-server command line.
     2	
     3	Phase 3: Process Command Building
     4	
     5	Tests the logic that constructs the llama-server command from configuration
     6	collected by ConfigCollector. Each test verifies one aspect of command building.
     7	
     8	Following the Testing.md Phase 3 plan:
     9	- 3.1 Base Command (llama-server + --model + --api-key)
    10	- 3.2 Sampling Parameters (conditional inclusion based on checkbox state)
    11	"""
    12	
    13	from process_command import ProcessCommandBuilder
    14	
    15	from .test_config import (
    16	    MockCheckBox,
    17	    MockComboBox,
    18	    MockLineEdit,
    19	    MockPathEdit,
    20	    MockSpinBox,
    21	    _make_collector,
    22	)
    23	
    24	# ==================================================================
    25	# 3.1 Base Command
    26	# ==================================================================
    27	
    28	
    29	class TestBaseCommand:
    30	    """3.1: Base command construction with llama-server and required flags."""
    31	
    32	    def test_base_command_includes_llama_server_and_model(self) -> None:
    33	        """3.1.1: Base command includes llama-server and --model flags."""
    34	        config = _make_collector(
    35	            model_path_edit=MockPathEdit(_full_path="/models/llama.gguf"),
    36	        ).collect_config()
    37	        builder = ProcessCommandBuilder(config)
    38	        cmd = builder.build_command()
    39	
    40	        assert "llama-server" in cmd
    41	        assert "--model" in cmd
    42	        model_idx = cmd.index("--model")
    43	        assert cmd[model_idx + 1] == "/models/llama.gguf"
    44	
    45	    def test_base_command_includes_api_key_default_when_empty(self) -> None:
    46	        """3.1.2a: Base command includes --api-key with default when empty."""
    47	        config = _make_collector(
    48	            api_key_line_edit=MockLineEdit(""),
    49	        ).collect_config()
    50	        builder = ProcessCommandBuilder(config)
    51	        cmd = builder.build_command()
    52	
    53	        assert "--api-key" in cmd
    54	        api_key_idx = cmd.index("--api-key")
    55	        assert cmd[api_key_idx + 1] == "12345"
    56	
    57	    def test_base_command_includes_custom_api_key(self) -> None:
    58	        """3.1.2b: Base command includes --api-key with custom value when set."""
    59	        config = _make_collector(
    60	            api_key_line_edit=MockLineEdit("my-secret-key"),
    61	        ).collect_config()
    62	        builder = ProcessCommandBuilder(config)
    63	        cmd = builder.build_command()
    64	
    65	        assert "--api-key" in cmd
    66	        api_key_idx = cmd.index("--api-key")
    67	        assert cmd[api_key_idx + 1] == "my-secret-key"
    68	
    69	
    70	# ==================================================================
    71	# 3.2 Sampling Parameters (Conditional)
    72	# ==================================================================
    73	# Each sampling param is gated by its checkbox. Test enabled/disabled pairs.
    74	
    75	
    76	class TestTemperatureParameter:
    77	    """3.2.1-3.2.2: Temperature parameter toggling."""
    78	
    79	    def test_includes_temp_when_temperature_enabled(self) -> None:
    80	        """3.2.1: Includes --temp when temperature checkbox is checked."""
    81	        config = _make_collector(
    82	            enable_temperature_checkbox=MockCheckBox(True),
    83	            temperature_spinbox=MockSpinBox(0.7),
    84	        ).collect_config()
    85	        builder = ProcessCommandBuilder(config)
    86	        cmd = builder.build_command()
    87	
    88	        assert "--temp" in cmd
    89	        temp_idx = cmd.index("--temp")
    90	        assert cmd[temp_idx + 1] == "0.7"
    91	
    92	    def test_omits_temp_when_temperature_disabled(self) -> None:
    93	        """3.2.2: Omits --temp when temperature checkbox is unchecked."""
    94	        config = _make_collector(
    95	            enable_temperature_checkbox=MockCheckBox(False),
    96	            temperature_spinbox=MockSpinBox(0.7),
    97	        ).collect_config()
    98	        builder = ProcessCommandBuilder(config)
    99	        cmd = builder.build_command()
   100	

```


## Assistant

<thinking>
The user is waiting for me to continue with implementing the tests. Let me first create a git worktree as required by project rules, then read more of the test_process.py file to understand the testing patterns, and finally implement the tests for section 3.6.

Let me start by:
1. Creating a git worktree
2. Reading more of test_process.py to understand the full pattern
3. Understanding what I need to test for section 3.6

The tests I need to write are for `_launch_model` side effects in main.py, which is different from the ProcessCommandBuilder tests in test_process.py. The section 3.6 tests need to verify that when `_launch_model` is called:
1. `_server_url` is set
2. `output_display` is cleared


3. Launch command is appended to output_display
4. `_process.start()` is called with correct arguments
5. `launch_button` text is updated to "STOP"
6. Web view URL is updated

These are side effects of the `_launch_model` method, so I'll need to mock the app and call the method directly. Let me create the worktree first, then read more test patterns.

</thinking>

I'll implement the tests for section 3.6 (Process Launch Side Effects). Let me start by creating a git worktree as required by project rules, then read the full test patterns to understand how to structure these tests.



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher && git worktree add .worktrees/test-process-launch-side-effects -b test/process-launch-side-effects**
Status: Completed

Terminal:
```
Preparing worktree (new branch 'test/process-launch-side-effects')
HEAD is now at 4805554 more tests added


```


## Assistant

<thinking>
The user wants me to continue with implementing the tests for section 3.6 (Process Launch Side Effects). I've created a git worktree. Now I need to:

1. Read more of test_process.py to understand the full testing patterns
2. Understand the _launch_model method in main.py (lines 870-1043)
3. Write tests following TDD principles

Let me read more of the test_process.py file and the conftest.py to understand the patterns used.

</thinking>

Good, worktree created. Now let me read more of the test files to understand the testing patterns before writing the tests for section 3.6.



**Tool Call: Read file `tests/test_process.py` (lines 100-250)**
Status: Completed

```LLamaLauncher/tests/test_process.py
   100	
   101	        assert "--temp" not in cmd
   102	
   103	
   104	class TestTopPParameter:
   105	    """3.2.3: Top-p parameter toggling."""
   106	
   107	    def test_includes_top_p_when_enabled(self) -> None:
   108	        """3.2.3: Includes --top-p when top_p checkbox is checked."""
   109	        config = _make_collector(
   110	            enable_top_p_checkbox=MockCheckBox(True),
   111	            top_p_spinbox=MockSpinBox(0.9),
   112	        ).collect_config()
   113	        builder = ProcessCommandBuilder(config)
   114	        cmd = builder.build_command()
   115	
   116	        assert "--top-p" in cmd
   117	        top_p_idx = cmd.index("--top-p")
   118	        assert cmd[top_p_idx + 1] == "0.9"
   119	
   120	    def test_omits_top_p_when_disabled(self) -> None:
   121	        """3.2.3: Omits --top-p when top_p checkbox is unchecked."""
   122	        config = _make_collector(
   123	            enable_top_p_checkbox=MockCheckBox(False),
   124	            top_p_spinbox=MockSpinBox(0.9),
   125	        ).collect_config()
   126	        builder = ProcessCommandBuilder(config)
   127	        cmd = builder.build_command()
   128	
   129	        assert "--top-p" not in cmd
   130	
   131	
   132	class TestTopKParameter:
   133	    """3.2.4: Top-k parameter toggling."""
   134	
   135	    def test_includes_top_k_when_enabled(self) -> None:
   136	        """3.2.4: Includes --top-k when top_k checkbox is checked."""
   137	        config = _make_collector(
   138	            enable_top_k_checkbox=MockCheckBox(True),
   139	            top_k_spinbox=MockSpinBox(40),
   140	        ).collect_config()
   141	        builder = ProcessCommandBuilder(config)
   142	        cmd = builder.build_command()
   143	
   144	        assert "--top-k" in cmd
   145	        top_k_idx = cmd.index("--top-k")
   146	        assert cmd[top_k_idx + 1] == "40"
   147	
   148	    def test_omits_top_k_when_disabled(self) -> None:
   149	        """3.2.4: Omits --top-k when top_k checkbox is unchecked."""
   150	        config = _make_collector(
   151	            enable_top_k_checkbox=MockCheckBox(False),
   152	            top_k_spinbox=MockSpinBox(40),
   153	        ).collect_config()
   154	        builder = ProcessCommandBuilder(config)
   155	        cmd = builder.build_command()
   156	
   157	        assert "--top-k" not in cmd
   158	
   159	
   160	class TestMinPParameter:
   161	    """3.2.5: Min-p parameter toggling."""
   162	
   163	    def test_includes_min_p_when_enabled(self) -> None:
   164	        """3.2.5: Includes --min-p when min_p checkbox is checked."""
   165	        config = _make_collector(
   166	            enable_min_p_checkbox=MockCheckBox(True),
   167	            min_p_spinbox=MockSpinBox(0.05),
   168	        ).collect_config()
   169	        builder = ProcessCommandBuilder(config)
   170	        cmd = builder.build_command()
   171	
   172	        assert "--min-p" in cmd
   173	        min_p_idx = cmd.index("--min-p")
   174	        assert cmd[min_p_idx + 1] == "0.05"
   175	
   176	    def test_omits_min_p_when_disabled(self) -> None:
   177	        """3.2.5: Omits --min-p when min_p checkbox is unchecked."""
   178	        config = _make_collector(
   179	            enable_min_p_checkbox=MockCheckBox(False),
   180	            min_p_spinbox=MockSpinBox(0.05),
   181	        ).collect_config()
   182	        builder = ProcessCommandBuilder(config)
   183	        cmd = builder.build_command()
   184	
   185	        assert "--min-p" not in cmd
   186	
   187	
   188	class TestTypicalPParameter:
   189	    """3.2.6: Typical-p parameter toggling."""
   190	
   191	    def test_includes_typical_p_when_enabled(self) -> None:
   192	        """3.2.6: Includes --typical-p when typical_p checkbox is checked."""
   193	        config = _make_collector(
   194	            enable_typical_p_checkbox=MockCheckBox(True),
   195	            typical_p_spinbox=MockSpinBox(1.0),
   196	        ).collect_config()
   197	        builder = ProcessCommandBuilder(config)
   198	        cmd = builder.build_command()
   199	
   200	        assert "--typical-p" in cmd
   201	        typical_p_idx = cmd.index("--typical-p")
   202	        assert cmd[typical_p_idx + 1] == "1.0"
   203	
   204	    def test_omits_typical_p_when_disabled(self) -> None:
   205	        """3.2.6: Omits --typical-p when typical_p checkbox is unchecked."""
   206	        config = _make_collector(
   207	            enable_typical_p_checkbox=MockCheckBox(False),
   208	            typical_p_spinbox=MockSpinBox(1.0),
   209	        ).collect_config()
   210	        builder = ProcessCommandBuilder(config)
   211	        cmd = builder.build_command()
   212	
   213	        assert "--typical-p" not in cmd
   214	
   215	
   216	class TestRepeatPenaltyParameter:
   217	    """3.2.7: Repeat penalty parameter toggling."""
   218	
   219	    def test_includes_repeat_penalty_when_enabled(self) -> None:
   220	        """3.2.7: Includes --repeat-penalty when repeat_penalty checkbox is checked."""
   221	        config = _make_collector(
   222	            enable_repeat_penalty_checkbox=MockCheckBox(True),
   223	            repeat_penalty_spinbox=MockSpinBox(1.1),
   224	        ).collect_config()
   225	        builder = ProcessCommandBuilder(config)
   226	        cmd = builder.build_command()
   227	
   228	        assert "--repeat-penalty" in cmd
   229	        rp_idx = cmd.index("--repeat-penalty")
   230	        assert cmd[rp_idx + 1] == "1.1"
   231	
   232	    def test_omits_repeat_penalty_when_disabled(self) -> None:
   233	        """3.2.7: Omits --repeat-penalty when repeat_penalty checkbox is unchecked."""
   234	        config = _make_collector(
   235	            enable_repeat_penalty_checkbox=MockCheckBox(False),
   236	            repeat_penalty_spinbox=MockSpinBox(1.1),
   237	        ).collect_config()
   238	        builder = ProcessCommandBuilder(config)
   239	        cmd = builder.build_command()
   240	
   241	        assert "--repeat-penalty" not in cmd
   242	
   243	
   244	class TestRepeatLastNParameter:
   245	    """3.2.8: Repeat last N parameter toggling."""
   246	
   247	    def test_includes_repeat_last_n_when_enabled(self) -> None:
   248	        """3.2.8: Includes --repeat-last-n when repeat_last_n checkbox is checked."""
   249	        config = _make_collector(
   250	            enable_repeat_last_n_checkbox=MockCheckBox(True),

```


**Tool Call: Read file `tests/test_config.py` (lines 1-150)**
Status: Completed

```LLamaLauncher/tests/test_config.py
     1	"""Tests for configuration collection logic.
     2	
     3	Covers the pure data transformation logic for collecting widget values
     4	into a configuration dictionary and loading that configuration back.
     5	Uses simple dataclass widgets to avoid Qt dependencies in the test layer.
     6	"""
     7	
     8	import json
     9	from dataclasses import dataclass, field
    10	from pathlib import Path
    11	from typing import Any
    12	
    13	from .config_collector import ConfigCollector
    14	
    15	# ------------------------------------------------------------------
    16	# Simple widget data classes (no Qt dependencies)
    17	# ------------------------------------------------------------------
    18	
    19	
    20	@dataclass(slots=True)
    21	class MockLineEdit:
    22	    """Minimal QLineEdit replacement for testing."""
    23	
    24	    _text: str = ""
    25	
    26	    def text(self) -> str:
    27	        return self._text
    28	
    29	
    30	@dataclass(slots=True)
    31	class MockPathEdit:
    32	    """Minimal path line edit with fullPath property."""
    33	
    34	    _text: str = ""
    35	    _full_path: str = ""
    36	
    37	    def text(self) -> str:
    38	        return self._text
    39	
    40	    def property(self, name: str) -> str | None:
    41	        if name == "fullPath":
    42	            return self._full_path if self._full_path else None
    43	        return None
    44	
    45	    def setProperty(self, name: str, value: str) -> None:
    46	        if name == "fullPath":
    47	            self._full_path = value
    48	
    49	
    50	@dataclass(slots=True)
    51	class MockCheckBox:
    52	    """Minimal QCheckBox replacement for testing."""
    53	
    54	    _checked: bool = False
    55	
    56	    def isChecked(self) -> bool:
    57	        return self._checked
    58	
    59	
    60	@dataclass(slots=True)
    61	class MockSpinBox:
    62	    """Minimal QSpinBox/QDoubleSpinBox replacement for testing."""
    63	
    64	    _value: float = 0.0
    65	
    66	    def value(self) -> float:
    67	        return self._value
    68	
    69	
    70	@dataclass(slots=True)
    71	class MockComboBox:
    72	    """Minimal QComboBox replacement for testing."""
    73	
    74	    _current_text: str = ""
    75	    _items: list[tuple[str, Any]] = field(default_factory=list)
    76	    _current_index: int = 0
    77	
    78	    def __post_init__(self) -> None:
    79	        # Auto-resolve current index from text if items exist and index not set
    80	        if self._items and self._current_text:
    81	            for i, (text, _) in enumerate(self._items):
    82	                if text == self._current_text:
    83	                    self._current_index = i
    84	                    break
    85	
    86	    def currentText(self) -> str:
    87	        return self._current_text
    88	
    89	    def currentIndex(self) -> int:
    90	        return self._current_index
    91	
    92	    def itemData(self, index: int, role: Any) -> Any | None:
    93	        if 0 <= index < len(self._items):
    94	            return self._items[index][1]
    95	        return None
    96	
    97	
    98	# ------------------------------------------------------------------
    99	# Fixtures
   100	# ------------------------------------------------------------------
   101	
   102	
   103	def _make_collector(**overrides: Any) -> ConfigCollector:
   104	    """Build a ConfigCollector with default mock widgets, then override specific ones.
   105	
   106	    Args:
   107	        **overrides: Named widget overrides to replace defaults.
   108	
   109	    Returns:
   110	        ConfigCollector instance ready for testing.
   111	    """
   112	    defaults = {
   113	        "version_edit": MockLineEdit("1.0"),
   114	        "model_path_edit": MockPathEdit(_full_path="/models/llama.gguf"),
   115	        "mmproj_path_edit": MockPathEdit(_full_path="/models/mmproj.bin"),
   116	        "draft_model_line_edit": MockPathEdit(_full_path="/models/draft.gguf"),
   117	        "json_schema_line_edit": MockPathEdit(_full_path="/schemas/schema.json"),
   118	        "host_line_edit": MockLineEdit("127.0.0.1"),
   119	        "port_line_edit": MockLineEdit("8080"),
   120	        "api_key_line_edit": MockLineEdit("secret-key"),
   121	        "enable_temperature_checkbox": MockCheckBox(True),
   122	        "temperature_spinbox": MockSpinBox(0.7),
   123	        "enable_top_p_checkbox": MockCheckBox(True),
   124	        "top_p_spinbox": MockSpinBox(0.9),
   125	        "enable_top_k_checkbox": MockCheckBox(False),
   126	        "top_k_spinbox": MockSpinBox(40),
   127	        "enable_min_p_checkbox": MockCheckBox(False),
   128	        "min_p_spinbox": MockSpinBox(0.05),
   129	        "enable_typical_p_checkbox": MockCheckBox(False),
   130	        "typical_p_spinbox": MockSpinBox(1.0),
   131	        "enable_repeat_penalty_checkbox": MockCheckBox(False),
   132	        "repeat_penalty_spinbox": MockSpinBox(1.1),
   133	        "enable_repeat_last_n_checkbox": MockCheckBox(False),
   134	        "repeat_last_n_spinbox": MockSpinBox(64),
   135	        "enable_presence_penalty_checkbox": MockCheckBox(False),
   136	        "presence_penalty_spinbox": MockSpinBox(0.0),
   137	        "enable_frequency_penalty_checkbox": MockCheckBox(False),
   138	        "frequency_penalty_spinbox": MockSpinBox(0.0),
   139	        "enable_mirostat_checkbox": MockCheckBox(False),
   140	        "mirostat_spinbox": MockSpinBox(0),
   141	        "enable_mirostat_lr_checkbox": MockCheckBox(False),
   142	        "mirostat_lr_spinbox": MockSpinBox(0.001),
   143	        "enable_mirostat_ent_checkbox": MockCheckBox(False),
   144	        "mirostat_ent_spinbox": MockSpinBox(5.0),
   145	        "enable_gpu_layers_checkbox": MockCheckBox(True),
   146	        "gpu_layers_spinbox": MockSpinBox(33),
   147	        "enable_threads_checkbox": MockCheckBox(True),
   148	        "threads_spinbox": MockSpinBox(8),
   149	        "enable_threads_batch_checkbox": MockCheckBox(False),
   150	        "threads_batch_spinbox": MockSpinBox(512),

```


## Assistant

<thinking>
Now I have a clear picture of the project structure and testing patterns. Let me understand what I need to do:

1. The user wants me to implement tests for section 3.6 (Process Launch Side Effects) from Testing.md
2. These tests are for the `_launch_model` method in main.py (lines ~870-1043)
3. The tests need to verify side effects after building the command:
   - 3.6.1: Sets `_server_url` after building command
   - 3.6.2: Clears output_display before launching
   - 3.6.3: Appends launch command to output_display
   - 3.6.4: Calls `_process.start()` with correct program and args list
   - 3.6.5: Updates launch_button text to "STOP"
   - 3.6.6: Updates web view URL after launch

The existing tests in test_process.py use a ProcessCommandBuilder class that reads from ConfigCollector, but the actual code I'm testing is in main.py's `_launch_model` method which directly reads from UI widgets and calls QProcess.start(). I need to create mock widgets similar to what's in config_collector.py and test_main.py, then set up a mock app with those widgets to call `_launch_model` and verify the side effects.

I'm realizing the TDD approach means writing failing tests first before implementing the production code, but since `_launch_model` already exists, I'll write tests that capture its current behavior instead. Looking at the actual method in main.py, it reads model_path from a property, validates it exists, and then continues with launching the server.

The method extracts numerous widget values for various parameters like temperature, top_p, sampling settings, performance configurations (gpu_layers, threads, batch_size), and advanced generation options, then constructs and executes the launch command.

Now I'm seeing how the remaining parameters get assembled—mirostat settings, draft model selection, grammar and JSON schema paths, rope scaling configurations, host/port bindings, mmproj options, and user-provided flags all feed into the command list before it gets executed. The `_server_url` attribute gets set to track the server location for later use.

The output display clears and logs the launch command, then QProcess starts with the program and arguments. The button text updates to "STOP" to reflect the running state, and the web view navigates to the server URL.

Now I'm planning out the test structure—I'll create a `TestLaunchModelSideEffects` class in test_process.py to verify each side effect: that `_server_url` gets set correctly, `output_display` clears before launch, the command gets logged, QProcess.start() receives the right arguments, the button text changes, and the web view updates to show the server.

For the mocks, I need a basic QApplication fixture from conftest.py and a mock_app with all the necessary widget attributes set up properly.

</thinking>

Now I have a clear picture of the project structure and testing patterns. Let me understand what needs to be done:

1. Implement tests for section 3.6 (Process Launch Side Effects) from Testing.md
2. These tests verify side effects of the `_launch_model` method in main.py
3. The tests need to mock the app and its widgets, then verify the side effects

Let me first read more of the existing test patterns and understand the full _launch_model method:



**Tool Call: Read file `tests/test_main.py` (lines 105-220)**
Status: Completed

```LLamaLauncher/tests/test_main.py
   105	# ==================================================================
   106	# Fixtures for _apply_config tests
   107	# ==================================================================
   108	
   109	
   110	@pytest.fixture
   111	def mock_app():
   112	    """Create a mock LlamaLaunchApp with all required widget attributes.
   113	
   114	    Returns:
   115	        MagicMock configured with mock Qt widgets for _apply_config testing.
   116	    """
   117	    app = MagicMock()
   118	
   119	    # Files/Paths widgets
   120	    app.model_path_edit = MagicMock()
   121	    app.mmproj_path_edit = MagicMock()
   122	    app.draft_model_line_edit = MagicMock()
   123	    app.json_schema_line_edit = MagicMock()
   124	
   125	    # Server widgets
   126	    app.host_line_edit = MagicMock()
   127	    app.port_line_edit = MagicMock()
   128	    app.api_key_line_edit = MagicMock()
   129	
   130	    # Sampling parameters widgets (12 params)
   131	    sampling_params = [
   132	        "temperature",
   133	        "top_p",
   134	        "top_k",
   135	        "min_p",
   136	        "typical_p",
   137	        "repeat_penalty",
   138	        "repeat_last_n",
   139	        "presence_penalty",
   140	        "frequency_penalty",
   141	        "mirostat",
   142	        "mirostat_lr",
   143	        "mirostat_ent",
   144	    ]
   145	    for param in sampling_params:
   146	        checkbox = MagicMock()
   147	        spinbox = MagicMock()
   148	        setattr(app, f"enable_{param}_checkbox", checkbox)
   149	        setattr(app, f"{param}_spinbox", spinbox)
   150	
   151	    # Performance parameters widgets (7 params)
   152	    perf_params = [
   153	        "gpu_layers",
   154	        "threads",
   155	        "threads_batch",
   156	        "batch_size",
   157	        "ubatch_size",
   158	        "n_predict",
   159	        "parallel",
   160	    ]
   161	    for param in perf_params:
   162	        checkbox = MagicMock()
   163	        spinbox = MagicMock()
   164	        setattr(app, f"enable_{param}_checkbox", checkbox)
   165	        setattr(app, f"{param}_spinbox", spinbox)
   166	
   167	    # Performance comboboxes
   168	    app.flash_attn_combobox = MagicMock()
   169	    app.cache_type_k_combobox = MagicMock()
   170	    app.cache_type_v_combobox = MagicMock()
   171	
   172	    # Boolean checkboxes for performance
   173	    app.enable_mmap_checkbox = MagicMock()
   174	    app.enable_mlock_checkbox = MagicMock()
   175	    app.enable_cont_batching_checkbox = MagicMock()
   176	
   177	    # Advanced parameters widgets
   178	    advanced_params = ["spec_draft_n_max", "seed", "rope_freq_base", "rope_freq_scale"]
   179	    for param in advanced_params:
   180	        checkbox = MagicMock()
   181	        spinbox = MagicMock()
   182	        setattr(app, f"enable_{param}_checkbox", checkbox)
   183	        setattr(app, f"{param}_spinbox", spinbox)
   184	
   185	    # Advanced path widgets
   186	    app.grammar_line_edit = MagicMock()
   187	
   188	    # Advanced boolean checkboxes
   189	    app.enable_draft_model_checkbox = MagicMock()
   190	    app.enable_grammar_checkbox = MagicMock()
   191	    app.enable_json_schema_checkbox = MagicMock()
   192	
   193	    # Advanced comboboxes
   194	    app.rope_scaling_combobox = MagicMock()
   195	
   196	    # Context size widget
   197	    app.model_context_size = MagicMock()
   198	
   199	    # Other widgets
   200	    app.more_options_line_edit = MagicMock()
   201	    app.no_mmproj_offload_checkbox = MagicMock()
   202	
   203	    # Helper methods (mocked to track calls)
   204	    app._set_path_field = MagicMock()
   205	    app._apply_param = MagicMock()
   206	    app._apply_combo_param = MagicMock()
   207	
   208	    return app
   209	
   210	
   211	# ==================================================================
   212	# 2.4 Configuration Application (_apply_config)
   213	# ==================================================================
   214	
   215	
   216	class TestApplyConfig:
   217	    """2.4: Testing _apply_config method."""
   218	
   219	    def test_2_4_1_applies_files_section(self, mock_app):
   220	        """2.4.1: Applies files section (model_path, mmproj_path,

```


**Tool Call: Read file `main.py` (lines 870-920)**
Status: Completed

```LLamaLauncher/main.py
   870	    def _launch_model(self) -> None:
   871	        """Launch the llama-server binary with current configuration.
   872	
   873	        Builds the command-line arguments from the UI fields and starts
   874	        ``llama-server`` via QProcess.  Live stdout/stderr output is
   875	        streamed into ``output_display``.
   876	        """
   877	        model_path = self.model_path_edit.property("fullPath")
   878	        if not model_path:
   879	            self.output_display.appendPlainText("Error: no model selected.")
   880	            return
   881	
   882	        temperature = self.temperature_spinbox.value()
   883	        top_p = self.top_p_spinbox.value()
   884	        top_k = self.top_k_spinbox.value()
   885	        min_p = self.min_p_spinbox.value()
   886	        typical_p = self.typical_p_spinbox.value()
   887	        repeat_penalty = self.repeat_penalty_spinbox.value()
   888	        repeat_last_n = self.repeat_last_n_spinbox.value()
   889	        presence_penalty = self.presence_penalty_spinbox.value()
   890	        frequency_penalty = self.frequency_penalty_spinbox.value()
   891	
   892	        mirostat = self.mirostat_spinbox.value()
   893	        mirostat_lr = self.mirostat_lr_spinbox.value()
   894	        mirostat_ent = self.mirostat_ent_spinbox.value()
   895	
   896	        # Performance parameters
   897	        gpu_layers = self.gpu_layers_spinbox.value()
   898	        threads = self.threads_spinbox.value()
   899	        threads_batch = self.threads_batch_spinbox.value()
   900	        batch_size = self.batch_size_spinbox.value()
   901	        ubatch_size = self.ubatch_size_spinbox.value()
   902	        n_predict = self.n_predict_spinbox.value()
   903	        parallel = self.parallel_spinbox.value()
   904	        cache_type_k = self.cache_type_k_combobox.currentText()
   905	        cache_type_v = self.cache_type_v_combobox.currentText()
   906	
   907	        # Advanced Generation parameters
   908	        spec_draft_n_max = self.spec_draft_n_max_spinbox.value()
   909	        seed = self.seed_spinbox.value()
   910	        rope_scaling = self.rope_scaling_combobox.currentText()
   911	        rope_freq_base = self.rope_freq_base_spinbox.value()
   912	        rope_freq_scale = self.rope_freq_scale_spinbox.value()
   913	
   914	        mmproj_path = self.mmproj_path_edit.property("fullPath")
   915	        no_mmproj_offload = self.no_mmproj_offload_checkbox.isChecked()
   916	        api_key = (
   917	            self.api_key_line_edit.text() if self.api_key_line_edit.text() else "12345"
   918	        )
   919	
   920	        # Build command: llama-server --model ... (conditional sampling params) ...

```


## Assistant

<thinking>
The user wants me to continue with implementing the tests for section 3.6 (Process Launch Side Effects). I've already:
1. Created a git worktree `.worktrees/test-process-launch-side-effects` on branch `test/process-launch-side-effects`
2. Read the Testing.md file for the test specifications
3. Read the main.py source code to understand the `_launch_model` method
4. Read existing test patterns in test_main.py and test_process.py

Now I need to:
1. Read the full _launch_model method to understand all the side effects
2. Write the tests following TDD principles
3. Run the tests to verify they pass

Let me first read the complete _launch_model method and then write the tests.

The tests I need to write are for section 3.6 (Process Launch Side Effects):
- 3.6.1: Sets `_server_url` after building command
- 3.6.2: Clears output_display before launching
- 3.6.3: Appends launch command to output_display
- 3.6.4: Calls `_process.start()` with correct program and args list
- 3.6.5: Updates launch_button text to "STOP"
- 3.6.6: Updates web view URL after launch

Looking at the code in main.py around lines 870-1043, I can see the `_launch_model` method which builds a command and then performs these side effects.

Let me now read more of the _launch_model method to get the full picture, then write the tests.

</thinking>

Now I have a clear picture of the project structure and testing patterns. Let me understand what needs to be done:

1. Implement tests for section 3.6 (Process Launch Side Effects) from Testing.md
2. These tests verify side effects of the `_launch_model` method in main.py
3. The tests need to mock the app and its widgets, then verify the side effects

Let me first read more of the existing test patterns and understand the full _launch_model method:



**Tool Call: Read file `main.py` (lines 870-920)**
Status: Completed

```LLamaLauncher/main.py
   870	    def _launch_model(self) -> None:
   871	        """Launch the llama-server binary with current configuration.
   872	
   873	        Builds the command-line arguments from the UI fields and starts
   874	        ``llama-server`` via QProcess.  Live stdout/stderr output is
   875	        streamed into ``output_display``.
   876	        """
   877	        model_path = self.model_path_edit.property("fullPath")
   878	        if not model_path:
   879	            self.output_display.appendPlainText("Error: no model selected.")
   880	            return
   881	
   882	        temperature = self.temperature_spinbox.value()
   883	        top_p = self.top_p_spinbox.value()
   884	        top_k = self.top_k_spinbox.value()
   885	        min_p = self.min_p_spinbox.value()
   886	        typical_p = self.typical_p_spinbox.value()
   887	        repeat_penalty = self.repeat_penalty_spinbox.value()
   888	        repeat_last_n = self.repeat_last_n_spinbox.value()
   889	        presence_penalty = self.presence_penalty_spinbox.value()
   890	        frequency_penalty = self.frequency_penalty_spinbox.value()
   891	
   892	        mirostat = self.mirostat_spinbox.value()
   893	        mirostat_lr = self.mirostat_lr_spinbox.value()
   894	        mirostat_ent = self.mirostat_ent_spinbox.value()
   895	
   896	        # Performance parameters
   897	        gpu_layers = self.gpu_layers_spinbox.value()
   898	        threads = self.threads_spinbox.value()
   899	        threads_batch = self.threads_batch_spinbox.value()
   900	        batch_size = self.batch_size_spinbox.value()
   901	        ubatch_size = self.ubatch_size_spinbox.value()
   902	        n_predict = self.n_predict_spinbox.value()
   903	        parallel = self.parallel_spinbox.value()
   904	        cache_type_k = self.cache_type_k_combobox.currentText()
   905	        cache_type_v = self.cache_type_v_combobox.currentText()
   906	
   907	        # Advanced Generation parameters
   908	        spec_draft_n_max = self.spec_draft_n_max_spinbox.value()
   909	        seed = self.seed_spinbox.value()
   910	        rope_scaling = self.rope_scaling_combobox.currentText()
   911	        rope_freq_base = self.rope_freq_base_spinbox.value()
   912	        rope_freq_scale = self.rope_freq_scale_spinbox.value()
   913	
   914	        mmproj_path = self.mmproj_path_edit.property("fullPath")
   915	        no_mmproj_offload = self.no_mmproj_offload_checkbox.isChecked()
   916	        api_key = (
   917	            self.api_key_line_edit.text() if self.api_key_line_edit.text() else "12345"
   918	        )
   919	
   920	        # Build command: llama-server --model ... (conditional sampling params) ...

```


## Assistant

<thinking>
The user wants me to continue with implementing the tests for section 3.6 (Process Launch Side Effects). I've already:

1. Created a git worktree `.worktrees/test-process-launch-side-effects` on branch `test/process-launch-side-effects`
2. Read the Testing.md file for the test specifications
3. Read the main.py source code to understand the `_launch_model` method
4. Read existing test patterns in test_main.py and test_process.py

Now I need to:
1. Read the full _launch_model method to understand all the side effects
2. Write the tests following TDD principles
3. Run the tests to verify they pass

Let me first read the complete _launch_model method to get the full picture, then write the tests.

The tests I need to write are for section 3.6 (Process Launch Side Effects):
- 3.6.1: Sets `_server_url` after building command
- 3.6.2: Clears output_display before launching
- 3.6.3: Appends launch command to output_display
- 3.6.4: Calls `_process.start()` with correct program and args list
- 3.6.5: Updates launch_button text to "STOP"
- 3.6.6: Updates web view URL after launch

Looking at the code in main.py around lines 870-1043, I can see the `_launch_model` method which builds a command and then performs these side effects.

Let me first read more of the _launch_model method to get the full picture, then write the tests.

</thinking>

Good, worktree created. Now let me continue reading the full `_launch_model` method to understand all the side effects I need to test:



**Tool Call: Read file `main.py` (lines 920-1045)**
Status: Completed

```LLamaLauncher/main.py
   920	        # Build command: llama-server --model ... (conditional sampling params) ...
   921	        cmd = [
   922	            "llama-server",
   923	            "--model",
   924	            model_path,
   925	            "--api-key",
   926	            api_key,
   927	        ]
   928	
   929	        if self.enable_temperature_checkbox.isChecked():
   930	            cmd.extend(["--temp", str(temperature)])
   931	        if self.enable_top_p_checkbox.isChecked():
   932	            cmd.extend(["--top-p", str(top_p)])
   933	        if self.enable_top_k_checkbox.isChecked():
   934	            cmd.extend(["--top-k", str(top_k)])
   935	        if self.enable_min_p_checkbox.isChecked():
   936	            cmd.extend(["--min-p", str(min_p)])
   937	        if self.enable_typical_p_checkbox.isChecked():
   938	            cmd.extend(["--typical-p", str(typical_p)])
   939	        if self.enable_repeat_penalty_checkbox.isChecked():
   940	            cmd.extend(["--repeat-penalty", str(repeat_penalty)])
   941	        if self.enable_repeat_last_n_checkbox.isChecked():
   942	            cmd.extend(["--repeat-last-n", str(repeat_last_n)])
   943	        if self.enable_presence_penalty_checkbox.isChecked():
   944	            cmd.extend(["--presence-penalty", str(presence_penalty)])
   945	        if self.enable_frequency_penalty_checkbox.isChecked():
   946	            cmd.extend(["--frequency-penalty", str(frequency_penalty)])
   947	        if self.enable_mirostat_checkbox.isChecked():
   948	            cmd.extend(["--mirostat", str(mirostat)])
   949	        if self.enable_mirostat_lr_checkbox.isChecked():
   950	            cmd.extend(["--mirostat-lr", str(mirostat_lr)])
   951	        if self.enable_mirostat_ent_checkbox.isChecked():
   952	            cmd.extend(["--mirostat-ent", str(mirostat_ent)])
   953	
   954	        # Performance parameters
   955	        if self.enable_gpu_layers_checkbox.isChecked():
   956	            cmd.extend(["--n-gpu-layers", str(gpu_layers)])
   957	        if self.enable_threads_checkbox.isChecked():
   958	            cmd.extend(["--threads", str(threads)])
   959	        if self.enable_threads_batch_checkbox.isChecked():
   960	            cmd.extend(["--threads-batch", str(threads_batch)])
   961	        if self.enable_batch_size_checkbox.isChecked():
   962	            cmd.extend(["--batch-size", str(batch_size)])
   963	        if self.enable_ubatch_size_checkbox.isChecked():
   964	            cmd.extend(["--ubatch-size", str(ubatch_size)])
   965	        if self.enable_n_predict_checkbox.isChecked():
   966	            cmd.extend(["--n-predict", str(n_predict)])
   967	        # Flash Attention: always pass the selected value (default auto)
   968	        flash_attn = self.flash_attn_combobox.currentText()
   969	        cmd.extend(["--flash-attn", flash_attn])
   970	        if self.enable_cache_type_k_checkbox.isChecked():
   971	            cmd.extend(["--cache-type-k", cache_type_k])
   972	        if self.enable_cache_type_v_checkbox.isChecked():
   973	            cmd.extend(["--cache-type-v", cache_type_v])
   974	        if self.enable_mmap_checkbox.isChecked():
   975	            cmd.append("--mmap")
   976	        if self.enable_mlock_checkbox.isChecked():
   977	            cmd.append("--mlock")
   978	        if self.enable_cont_batching_checkbox.isChecked():
   979	            cmd.append("--cont-batching")
   980	        if self.enable_parallel_checkbox.isChecked():
   981	            cmd.extend(["--parallel", str(parallel)])
   982	
   983	        # Advanced Generation parameters
   984	        draft_model_path = self.draft_model_line_edit.property("fullPath")
   985	        if self.enable_draft_model_checkbox.isChecked() and draft_model_path:
   986	            cmd.extend(["--draft-model", draft_model_path])
   987	        if self.enable_spec_draft_n_max_checkbox.isChecked():
   988	            cmd.extend(["--spec-draft-n-max", str(spec_draft_n_max)])
   989	        if self.enable_seed_checkbox.isChecked():
   990	            cmd.extend(["--seed", str(seed)])
   991	        grammar_text = self.grammar_line_edit.text().strip()
   992	        if self.enable_grammar_checkbox.isChecked() and grammar_text:
   993	            cmd.extend(["--grammar", grammar_text])
   994	        json_schema_path = self.json_schema_line_edit.property("fullPath")
   995	        if self.enable_json_schema_checkbox.isChecked() and json_schema_path:
   996	            cmd.extend(["--json-schema", json_schema_path])
   997	        if self.enable_rope_scaling_checkbox.isChecked():
   998	            cmd.extend(["--rope-scaling", rope_scaling])
   999	        if self.enable_rope_freq_base_checkbox.isChecked():
  1000	            cmd.extend(["--rope-freq-base", str(rope_freq_base)])
  1001	        if self.enable_rope_freq_scale_checkbox.isChecked():
  1002	            cmd.extend(["--rope-freq-scale", str(rope_freq_scale)])
  1003	
  1004	        host = self.host_line_edit.text() or self._host
  1005	        port_str = self.port_line_edit.text() or str(self._port)
  1006	        try:
  1007	            port = int(port_str)
  1008	        except ValueError:
  1009	            port = self._port
  1010	
  1011	        if mmproj_path:
  1012	            cmd.extend(["--mmproj", mmproj_path])
  1013	            if no_mmproj_offload:
  1014	                cmd.append("--no-mmproj-offload")
  1015	
  1016	        # Extra user-supplied flags from the more options line edit
  1017	        extra = self.more_options_line_edit.text().strip()
  1018	        if extra:
  1019	            cmd.extend(extra.split())
  1020	
  1021	        # Context size: only pass --ctx-size when a specific value is selected
  1022	        ctx_size = self.model_context_size.itemData(
  1023	            self.model_context_size.currentIndex(),
  1024	            Qt.UserRole,
  1025	        )
  1026	        if ctx_size is not None and int(ctx_size) > 0:
  1027	            cmd.extend(["--ctx-size", str(ctx_size)])
  1028	
  1029	        cmd.extend(["--host", host, "--port", str(port)])
  1030	
  1031	        self._server_url = f"http://{host}:{port}"
  1032	        self._auto_refresh_done = False
  1033	
  1034	        self.output_display.clear()
  1035	        self.output_display.appendPlainText(f"Launching: {' '.join(cmd)}\n---\n")
  1036	
  1037	        # Use two-argument form: program + arguments list (args must NOT include the program)
  1038	        self._process.start(cmd[0], cmd[1:])
  1039	        self.launch_button.setText("STOP")
  1040	
  1041	        # Update web view to point to the server
  1042	        server_url = f"http://{host}:{port}"
  1043	        self.server_web_view.setUrl(server_url)
  1044	
  1045	    # ------------------------------------------------------------------

```


## Assistant

<thinking>
The user wants me to implement the tests for section 3.6 (Process Launch Side Effects) from the Testing.md plan. I've already:

1. Created a git worktree `.worktrees/test-process-launch-side-effects` on branch `test/process-launch-side-effects`
2. Read the Testing.md file for the test specifications
3. Read the main.py source code to understand the `_launch_model` method
4. Read existing test patterns in test_main.py and test_process.py

Now I have the full picture of the `_launch_model` method (lines 870-1043). The tests I need to write are:
- 3.6.1: Sets `_server_url` after building command
- 3.6.2: Clears output_display before launching
- 3.6.3: Appends launch command to output_display
- 3.6.4: Calls `_process.start()` with correct program and args list
- 3.6.5: Updates launch_button text to "STOP"
- 3.6.6: Updates web view URL after launch

Looking at the code, these tests need to verify side effects of calling `_launch_model`. The method reads from various UI widgets and then performs these side effects. I need to create a mock app with all the necessary widget attributes and call the method directly.

The best approach is to:
1. Create a fixture that sets up a mock app with all the necessary widgets (similar to `mock_app` in test_main.py but with more configuration)
2. Write tests that call `_launch_model` on this mock app and verify the side effects

Let me read the existing test_main.py file more carefully to understand the pattern used for testing methods that have side effects.

Now I need to implement the tests for section 3.6 (Process Launch Side Effects). Based on my analysis:

1. The tests should go in `tests/test_process.py` (as specified in Testing.md Phase 3)
2. I need to create a fixture that provides a mock app with all necessary widgets configured
3. Each test should verify one specific side effect of the `_launch_model` method

The key insight is that these tests are for the side effects after building the command, not for the command building itself. So I need to:
1. Create a mock app with all widgets properly configured
2. Call `_launch_model` on this mock app
3. Verify the side effects (e.g., `_server_url` is set, `output_display.clear()` is called, etc.)

Let me now write the tests following the TDD approach - first write the test, then run it to see it fail, then implement the minimal code to make it pass.

Since the `_launch_model` method already exists in main.py, I'll write tests that capture its current behavior. The tests will use mocks to isolate the method under test.

Let me create the tests now.

</thinking>

Now I have the full picture of the `_launch_model` method (lines 870-1043). Let me implement the tests for section 3.6 (Process Launch Side Effects). These tests verify side effects after building the command.

Based on my analysis:
- Tests should go in `tests/test_process.py` (as specified in Testing.md Phase 3)
- I need to create a fixture that provides a mock app with all necessary widgets configured
- Each test verifies one specific side effect of calling `_launch_model`

Let me first check the current state of test_process.py to see where to append the new tests:



**Tool Call: Read file `tests/test_process.py` (lines 450-550)**
Status: Completed

```LLamaLauncher/tests/test_process.py
   450	        cmd = builder.build_command()
   451	
   452	        assert "--mmproj" in cmd
   453	        assert "--no-mmproj-offload" in cmd
   454	
   455	    def test_omits_no_mmproj_offload_when_checkbox_unchecked(self) -> None:
   456	        """3.5.5b: Omits --no-mmproj-offload when mmproj is set but checkbox is unchecked."""
   457	        config = _make_collector(
   458	            mmproj_path_edit=MockPathEdit(_full_path="/models/mmproj.bin"),
   459	            no_mmproj_offload_checkbox=MockCheckBox(False),
   460	        ).collect_config()
   461	        builder = ProcessCommandBuilder(config)
   462	        cmd = builder.build_command()
   463	
   464	        assert "--mmproj" in cmd
   465	        assert "--no-mmproj-offload" not in cmd
   466	
   467	
   468	class TestExtraFlags:
   469	    """3.5.6: Extra flags parsing."""
   470	
   471	    def test_parses_extra_flags_from_more_options(self) -> None:
   472	        """3.5.6: Parses extra flags from more_options line edit via .split()."""
   473	        config = _make_collector(
   474	            more_options_line_edit=MockLineEdit("--log-id test --verbose"),
   475	        ).collect_config()
   476	        builder = ProcessCommandBuilder(config)
   477	        cmd = builder.build_command()
   478	
   479	        assert "--log-id" in cmd
   480	        assert "test" in cmd
   481	        assert "--verbose" in cmd
   482	
   483	    def test_omits_extra_flags_when_empty(self) -> None:
   484	        """3.5.6b: Omits extra flags when more_options is empty."""
   485	        config = _make_collector(
   486	            more_options_line_edit=MockLineEdit(""),
   487	        ).collect_config()
   488	        builder = ProcessCommandBuilder(config)
   489	        cmd = builder.build_command()
   490	
   491	        # No extra flags from empty more_options
   492	        assert "--log-id" not in cmd
   493	
   494	
   495	class TestContextSize:
   496	    """3.5.7-3.5.8: Context size parameter."""
   497	
   498	    def test_includes_ctx_size_when_greater_than_zero(self) -> None:
   499	        """3.5.7: Includes --ctx-size only when context size > 0."""
   500	        config = _make_collector(
   501	            model_context_size=MockComboBox(
   502	                _current_text="4096",
   503	                _items=[("512", 512), ("2048", 2048), ("4096", 4096), ("8192", 8192)],
   504	            ),
   505	        ).collect_config()
   506	        builder = ProcessCommandBuilder(config)
   507	        cmd = builder.build_command()
   508	
   509	        assert "--ctx-size" in cmd
   510	        ctx_idx = cmd.index("--ctx-size")
   511	        assert cmd[ctx_idx + 1] == "4096"
   512	
   513	    def test_omits_ctx_size_when_zero(self) -> None:
   514	        """3.5.8: Omits --ctx-size when context size is 0 (Auto)."""
   515	        config = _make_collector(
   516	            model_context_size=MockComboBox(
   517	                _current_text="Auto",
   518	                _items=[("Auto", 0), ("512", 512), ("2048", 2048), ("4096", 4096)],
   519	            ),
   520	        ).collect_config()
   521	        builder = ProcessCommandBuilder(config)
   522	        cmd = builder.build_command()
   523	
   524	        assert "--ctx-size" not in cmd

```


## Assistant

<thinking>
Now I have a clear picture of what needs to be done. I need to implement the tests for section 3.6 (Process Launch Side Effects) from the Testing.md plan. 

The tests should go at the end of `tests/test_process.py` and need to verify the side effects of calling `_launch_model`. Since these are side effects (not command building), I need to:

1. Create a mock app with all necessary widgets configured
2. Call `_launch_model` on this mock app
3. Verify the side effects

Let me read the end of test_process.py to see where to append, then write the tests.

</thinking>

Now I have a clear picture. Let me check the very end of test_process.py to see where to append the new tests:



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher && wc -l tests/test_process.py**
Status: Completed

Terminal:
```
     524 tests/test_process.py




```


## Assistant

<thinking>
Now I have a clear picture of what needs to be done. I need to implement the tests for section 3.6 (Process Launch Side Effects) from the Testing.md plan. 

The tests should go at the end of `tests/test_process.py` and need to verify the side effects of calling `_launch_model`. Since these are side effects (not command building), I need to:

1. Create a mock app with all necessary widgets configured
2. Call `_launch_model` on this mock app
3. Verify the side effects

Let me write the tests following TDD principles - first write the test, then run it to see it fail, then implement the minimal code to make it pass.

The 6 tests I need to write are:
1. 3.6.1 - Sets `_server_url` after building command
2. 3.6.2 - Clears output_display before launching
3. 3.6.3 - Appends launch command to output_display
4. 3.6.4 - Calls `_process.start()` with correct program and args list
5. 3.6.5 - Updates launch_button text to "STOP"
6. 3.6.6 - Updates web view URL after launch

I need to understand the structure of _launch_model better. Looking at the code:
- It reads from various UI widgets (model_path_edit, host_line_edit, port_line_edit, etc.)
- It builds a command list
- It sets side effects:
  - `self._server_url = f"http://{host}:{port}"` (line 1031)
  - `self.output_display.clear()` (line 1034)
  - `self.output_display.appendPlainText(...)` (line 1035)
  - `self._process.start(cmd[0], cmd[1:])` (line 1038)
  - `self.launch_button.setText("STOP")` (line 1039)
  - `self.server_web_view.setUrl(server_url)` (line 1043)

For these tests, I need to:
1. Create a mock app with all necessary widgets
2. Call `_launch_model` on this mock app
3. Verify the side effects

The key challenge is that _launch_model reads from many widgets and builds a command before setting the side effects. I need to set up the mock app so that:
- model_path_edit.property("fullPath") returns a valid path (otherwise the method returns early)
- All other widgets are configured appropriately

Let me write the tests now. I'll create a fixture that provides a fully configured mock app, then write each test to verify one side effect.

Actually, looking at the Testing.md more carefully, I see that the tests for 3.6 are specifically about side effects, not about command building. So the tests should:
1. Set up a mock app with all necessary widgets
2. Call `_launch_model` on this mock app
3. Verify the specific side effect

Let me write these tests now.

</thinking>

Now I have a complete understanding of the task. Let me implement the tests for section 3.6 (Process Launch Side Effects). I'll add them to the end of `tests/test_process.py`.

First, let me read the very end of the file to understand where to append:



**Tool Call: Read file `tests/test_process.py` (lines 510-524)**
Status: Completed

```LLamaLauncher/tests/test_process.py
   510	        ctx_idx = cmd.index("--ctx-size")
   511	        assert cmd[ctx_idx + 1] == "4096"
   512	
   513	    def test_omits_ctx_size_when_zero(self) -> None:
   514	        """3.5.8: Omits --ctx-size when context size is 0 (Auto)."""
   515	        config = _make_collector(
   516	            model_context_size=MockComboBox(
   517	                _current_text="Auto",
   518	                _items=[("Auto", 0), ("512", 512), ("2048", 2048), ("4096", 4096)],
   519	            ),
   520	        ).collect_config()
   521	        builder = ProcessCommandBuilder(config)
   522	        cmd = builder.build_command()
   523	
   524	        assert "--ctx-size" not in cmd

```


## Assistant

<thinking>
Now I have a complete understanding of the task. Let me implement the tests for section 3.6 (Process Launch Side Effects). 

Looking at the code, I need to understand that:
1. The existing tests in test_process.py use `ProcessCommandBuilder` and `ConfigCollector` - these are pure logic classes
2. The section 3.6 tests are about side effects of `_launch_model` method in main.py
3. These side effects happen AFTER the command is built

The key insight is that section 3.6 tests need to verify the side effects after the command is built, not the command building itself. So I need to:
1. Create a mock app with all necessary widgets configured
2. Call `_launch_model` on this mock app  
3. Verify the side effects

But wait - looking at the Testing.md more carefully, I see that phase 3 is about "Process Command Building" and the tests are in test_process.py. The section 3.6 is about "Process Launch Side Effects" which are the side effects that happen after building the command in `_launch_model`.

Looking at the actual code in main.py lines 1031-1043, these are the side effects:
1. `self._server_url = f"http://{host}:{port}"` - Sets server URL
2. `self.output_display.clear()` - Clears output display
3. `self.output_display.appendPlainText(f"Launching: {' '.join(cmd)}\n---\n")` - Appends launch command
4. `self._process.start(cmd[0], cmd[1:])` - Starts the process
5. `self.launch_button.setText("STOP")` - Updates button text
6. `self.server_web_view.setUrl(server_url)` - Updates web view URL

To test these, I need to:
1. Create a mock app with all necessary widgets configured
2. Call `_launch_model` on this mock app
3. Verify each side effect

The challenge is that `_launch_model` reads from many widgets and builds a command before setting the side effects. I need to set up the mock app so that:
- `model_path_edit.property("fullPath")` returns a valid path (otherwise the method returns early with an error)
- All other widgets are configured appropriately

Let me write the tests now. I'll add them to test_process.py at the end.

Actually, looking at the Testing.md more carefully, I see that the tests for 3.6 are specifically about side effects of the `_launch_model` method. The existing tests in test_process.py use `ProcessCommandBuilder` and `ConfigCollector`, which are different classes.

Wait, let me re-read the code structure. Looking at the grep results earlier:
- `main.py` contains `LlamaLaunchApp` class with `_launch_model` method
- `process_command.py` contains `ProcessCommandBuilder` class
- `config_collector.py` contains `ConfigCollector` class

The tests in test_process.py test `ProcessCommandBuilder`, but section 3.6 is about the side effects of `_launch_model` in main.py. So I need to:
1. Import `LlamaLaunchApp` from main
2. Create a mock app with all necessary widgets
3. Call `_launch_model` on this mock app
4. Verify the side effects

Let me write these tests now. I'll create a fixture that provides a fully configured mock app, then write each test to verify one side effect.

Looking at the mock_app fixture in test_main.py, it creates a MagicMock with all the necessary widget attributes. I can use a similar approach but configure it specifically for _launch_model testing.

Let me write the tests now:

```python
# ==================================================================
# 3.6 Process Launch Side Effects
# ==================================================================


class TestLaunchModelSideEffects:
    """3.6: Testing side effects of _launch_model method."""

    def test_3_6_1_sets_server_url(self, qapp) -> None:
        """3.6.1: Sets _server_url after building command."""
        # Arrange
        from main import LlamaLaunchApp
        
        app = MagicMock()
        app.model_path_edit = MagicMock()
        app.model_path_edit.property.return_value = "/models/llama.gguf"
        app.host_line_edit = MagicMock()
        app.host_line_edit.text.return_value = "127.0.0.1"
        app.port_line_edit = MagicMock()
        app.port_line_edit.text.return_value = "8080"
        app._host = "127.0.0.1"
        app._port = 8080
        
        # All checkbox widgets
        for param in ["temperature", "top_p", "top_k", "min_p", "typical_p",
                      "repeat_penalty", "repeat_last_n", "presence_penalty",
                      "frequency_penalty", "mirostat", "mirostat_lr", "mirostat_ent",
                      "gpu_layers", "threads", "threads_batch", "batch_size",
                      "ubatch_size", "n_predict", "parallel",
                      "enable_mmap", "enable_mlock", "enable_cont_batching"]:
            pass
        
        # Actually, I need to set up all the widgets that _launch_model reads.
        # This is getting complex. Let me think about a simpler approach.
```

Actually, looking at this more carefully, I realize that the tests for 3.6 need to verify side effects of calling `_launch_model`. The method reads from many widgets and builds a command before setting the side effects. 

The simplest approach is to:
1. Create a mock app with all necessary widgets configured
2. Call `_launch_model` on this mock app
3. Verify each side effect

But I need to be careful about which widgets are read by `_launch_model`. Let me trace through the code:

1. `model_path = self.model_path_edit.property("fullPath")` - needs a valid path
2. Many spinbox values (temperature, top_p, etc.)
3. Many checkbox isChecked() calls
4. Combobox currentText() calls
5. LineEdit text() calls
6. ComboBox itemData() and currentIndex() calls

The key insight is that I only need to configure the widgets that affect the side effects. Since the side effects happen AFTER the command is built, I need to make sure the command is built successfully (i.e., model_path is not empty).

Let me write a fixture that provides a fully configured mock app, then write each test to verify one side effect.

Actually, looking at this more carefully, I think the best approach is to:
1. Create a fixture in conftest.py or directly in test_process.py that provides a mock app with all necessary widgets
2. Write each test to verify one specific side effect

Let me write the tests now. I'll add them to the end of test_process.py.

First, let me trace through all the widgets that _launch_model reads:

From lines 870-1043:
1. `self.model_path_edit.property("fullPath")` - line 877
2. `self.temperature_spinbox.value()` - line 882
3. `self.top_p_spinbox.value()` - line 883
4. `self.top_k_spinbox.value()` - line 884
5. `self.min_p_spinbox.value()` - line 885
6. `self.typical_p_spinbox.value()` - line 886
7. `self.repeat_penalty_spinbox.value()` - line 887
8. `self.repeat_last_n_spinbox.value()` - line 888
9. `self.presence_penalty_spinbox.value()` - line 889
10. `self.frequency_penalty_spinbox.value()` - line 890
11. `self.mirostat_spinbox.value()` - line 892
12. `self.mirostat_lr_spinbox.value()` - line 893
13. `self.mirostat_ent_spinbox.value()` - line 894
14. `self.gpu_layers_spinbox.value()` - line 897
15. `self.threads_spinbox.value()` - line 898
16. `self.threads_batch_spinbox.value()` - line 899
17. `self.batch_size_spinbox.value()` - line 900
18. `self.ubatch_size_spinbox.value()` - line 901
19. `self.n_predict_spinbox.value()` - line 902
20. `self.parallel_spinbox.value()` - line 903
21. `self.cache_type_k_combobox.currentText()` - line 904
22. `self.cache_type_v_combobox.currentText()` - line 905
23. `self.spec_draft_n_max_spinbox.value()` - line 907 (from outline)
24. `self.seed_spinbox.value()` - line 909 (from outline)
25. `self.rope_scaling_combobox.currentText()` - line 908 (from outline)
26. `self.rope_freq_base_spinbox.value()` - line 910 (from outline)
27. `self.rope_freq_scale_spinbox.value()` - line 911 (from outline)
28. `self.enable_temperature_checkbox.isChecked()` - line 929
29. ... many more checkboxes
30. `self.draft_model_line_edit.property("fullPath")` - line 984
31. `self.grammar_line_edit.text().strip()` - line 991
32. `self.json_schema_line_edit.property("fullPath")` - line 994
33. `self.host_line_edit.text()` - line 1004
34. `self.port_line_edit.text()` - line 1005
35. `self.mmproj_path_edit.property("fullPath")` - line 1011 (from earlier grep)
36. `self.no_mmproj_offload_checkbox.isChecked()` - line 1013 (from earlier grep)
37. `self.more_options_line_edit.text().strip()` - line 1017
38. `self.model_context_size.itemData(...)` - line 1022-1024
39. `self.enable_draft_model_checkbox.isChecked()` - line 985
40. `self.enable_spec_draft_n_max_checkbox.isChecked()` - line 987
41. `self.enable_seed_checkbox.isChecked()` - line 989
42. `self.enable_grammar_checkbox.isChecked()` - line 992
43. `self.enable_json_schema_checkbox.isChecked()` - line 995
44. `self.enable_rope_scaling_checkbox.isChecked()` - line 997
45. `self.enable_rope_freq_base_checkbox.isChecked()` - line 999
46. `self.enable_rope_freq_scale_checkbox.isChecked()` - line 1001
47. `self.flash_attn_combobox.currentText()` - line 968

And the side effects:
1. `self._server_url = f"http://{host}:{port}"` - line 1031
2. `self._auto_refresh_done = False` - line 1032
3. `self.output_display.clear()` - line 1034
4. `self.output_display.appendPlainText(...)` - line 1035
5. `self._process.start(cmd[0], cmd[1:])` - line 1038
6. `self.launch_button.setText("STOP")` - line 1039
7. `self.server_web_view.setUrl(server_url)` - line 1043

This is a lot of widgets to configure. Let me write a helper function or fixture that creates a fully configured mock app.

Actually, I think the best approach is to create a fixture in test_process.py (similar to how _make_collector works) that provides a mock app with all necessary widgets configured for _launch_model testing.

Let me write this now:

```python
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
    app.model_path_edit = MagicMock()
    app.model_path_edit.property.return_value = overrides.get("model_path", "/models/llama.gguf")
    
    # Server widgets
    app.host_line_edit = MagicMock(text=MagicMock(return_value=overrides.get("host", "127.0.0.1")))
    app.port_line_edit = MagicMock(text=MagicMock(return_value=overrides.get("port", "8080")))
    app._host = overrides.get("_host", "127.0.0.1")
    app._port = overrides.get("_port", 8080)
    
    # API key
    app.api_key_line_edit = MagicMock(text=MagicMock(return_value=overrides.get("api_key", "")))
    
    # All spinboxes
    for param in ["temperature", "top_p", "top_k", "min_p", "typical_p",
                  "repeat_penalty", "repeat_last_n", "presence_penalty",
                  "frequency_penalty", "mirostat", "mirostat_lr", "mirostat_ent",
                  "gpu_layers", "threads", "threads_batch", "batch_size",
                  "ubatch_size", "n_predict", "parallel",
                  "spec_draft_n_max", "seed", "rope_freq_base", "rope_freq_scale"]:
        app.__setattr__(f"{param}_spinbox", MagicMock(value=MagicMock(return_value=overrides.get(f"{param}_value", 0))))
    
    # All checkboxes - default to unchecked
    all_checkboxes = [
        "enable_temperature", "enable_top_p", "enable_top_k", "enable_min_p",
        "enable_typical_p", "enable_repeat_penalty", "enable_repeat_last_n",
        "enable_presence_penalty", "enable_frequency_penalty", "enable_mirostat",
        "enable_mirostat_lr", "enable_mirostat_ent", "enable_gpu_layers",
        "enable_threads", "enable_threads_batch", "enable_batch_size",
        "enable_ubatch_size", "enable_n_predict", "enable_parallel",
        "enable_mmap", "enable_mlock", "enable_cont_batching",
        "enable_draft_model", "enable_spec_draft_n_max", "enable_seed",
        "enable_grammar", "enable_json_schema", "enable_rope_scaling",
        "enable_rope_freq_base", "enable_rope_freq_scale", "enable_cache_type_k",
        "enable_cache_type_v"
    ]
    
    for cb in all_checkboxes:
        app.__setattr__(cb, MagicMock(isChecked=MagicMock(return_value=overrides.get(f"{cb}_checked", False))))
    
    # Comboboxes
    app.flash_attn_combobox = MagicMock(currentText=MagicMock(return_value=overrides.get("flash_attn", "auto")))
    app.cache_type_k_combobox = MagicMock(currentText=MagicMock(return_value=overrides.get("cache_type_k", "f32")))
    app.cache_type_v_combobox = MagicMock(currentText=MagicMock(return_value=overrides.get("cache_type_v", "f32")))
    app.rope_scaling_combobox = MagicMock(currentText=MagicMock(return_value=overrides.get("rope_scaling", "linear")))
    
    # Path widgets
    app.mmproj_path_edit = MagicMock(property=MagicMock(return_value=overrides.get("mmproj_path", None)))
    app.draft_model_line_edit = MagicMock(property=MagicMock(return_value=None))
    app.json_schema_line_edit = MagicMock(property=MagicMock(return_value=None))
    app.grammar_line_edit = MagicMock(text=MagicMock(return_value=""))
    
    # More options
    app.more_options_line_edit = MagicMock(text=MagicMock(return_value=""))
    
    # Context size
    app.model_context_size = MagicMock(
        itemData=MagicMock(return_value=None),
        currentIndex=MagicMock(return_value=0)
    )
    
    # No mmproj offload
    app.no_mmproj_offload_checkbox = MagicMock(isChecked=MagicMock(return_value=False))
    
    # Output/display widgets (side effects)
    app.output_display = MagicMock()
    app.launch_button = MagicMock()
    app.server_web_view = MagicMock()
    
    # Process
    app._process = MagicMock()
    
    return app
```

Wait, this is getting very complex. Let me think about a simpler approach.

Actually, looking at the Testing.md more carefully, I see that the tests for 3.6 are specifically about side effects. The key insight is that these tests need to verify that when `_launch_model` is called:
1. `_server_url` is set correctly
2. `output_display.clear()` is called
3. `output_display.appendPlainText(...)` is called with the launch command
4. `_process.start(...)` is called with the correct program and args
5. `launch_button.setText("STOP")` is called
6. `server_web_view.setUrl(...)` is called

The challenge is that `_launch_model` reads from many widgets before setting these side effects. If any widget is not configured correctly, the method might fail or behave unexpectedly.

I think the best approach is to:
1. Create a fixture that provides a mock app with all necessary widgets configured
2. Write each test to verify one specific side effect
3. Use pytest.raises or other mechanisms to handle cases where the method might fail

Let me simplify my approach. I'll create a fixture that provides a mock app with minimal configuration (just enough to get past the early return), then write each test to verify one side effect.

Actually, looking at this more carefully, I think the simplest approach is to:
1. Create a helper function that builds a mock app with default values
2. Allow overriding specific widgets for each test
3. Call `_launch_model` and verify the side effects

Let me write this now. I'll add the tests to the end of test_process.py.

Actually, I realize I need to be more careful about how I set up the mocks. Looking at the _launch_model code:

```python
model_path = self.model_path_edit.property("fullPath")
if not model_path:
    self.output_display.appendPlainText("Error: no model selected.")
    return
```

So I need to make sure `model_path_edit.property("fullPath")` returns a non-empty string. If it doesn't, the method will return early and the side effects won't happen.

Let me write the tests now. I'll create a fixture that provides a mock app with all necessary widgets configured, then write each test to verify one side effect.

Here's my plan:
1. Create a `_make_launch_app` helper function (similar to `_make_collector`)
2. Add the tests for 3.6 at the end of test_process.py
3. Run the tests to verify they pass

Let me write this now.

</thinking>

Now I have the complete picture. Let me implement the tests for section 3.6 (Process Launch Side Effects). I'll add them to the end of `tests/test_process.py`.



**Tool Call: tests/test\_process.py**
Status: Completed

Diff: tests/test_process.py
```
"""Tests for ProcessCommandBuilder - building llama-server command line.

Phase 3: Process Command Building

Tests the logic that constructs the llama-server command from configuration
collected by ConfigCollector. Each test verifies one aspect of command building.

Following the Testing.md Phase 3 plan:
- 3.1 Base Command (llama-server + --model + --api-key)
- 3.2 Sampling Parameters (conditional inclusion based on checkbox state)
"""

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


from unittest.mock import Any, MagicMock


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

```


## Assistant

<thinking>
The user seems to be waiting for me to continue with implementing the tests for section 3.6 (Process Launch Side Effects). I've already:

1. Created a git worktree `.worktrees/test-process-launch-side-effects` on branch `test/process-launch-side-effects`
2. Read the Testing.md file for the test specifications
3. Read the main.py source code to understand the `_launch_model` method
4. Read existing test patterns in test_main.py and test_process.py
5. Started implementing the tests by adding them to test_process.py

Now I need to complete the implementation by:
1. Finishing writing all 6 tests (3.6.1 through 3.6.6)
2. Running the tests to verify they pass
3. Running linting and formatting

Let me continue with the implementation. The tests I need to write are:
- 3.6.1: Sets `_server_url` after building command
- 3.6.2: Clears output_display before launching
- 3.6.3: Appends launch command to output_display
- 3.6.4: Calls `_process.start()` with correct program and args list
- 3.6.5: Updates launch_button text to "STOP"
- 3.6.6: Updates web view URL after launch

I need to understand the _launch_model method better to write proper tests. Let me read the full method first, then write the tests following TDD principles.

</thinking>

I'll continue with implementing the tests for section 3.6 (Process Launch Side Effects). Let me first create a git worktree and read the relevant code sections to understand what needs to be tested.



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher && git worktree add .worktrees/test-process-launch-side-effects -b test/process-launch-side-effects 2>/dev/null || git checkout test/process-launch-side-effects**
Status: Completed

Terminal:
```
fatal: 'test/process-launch-side-effects' is already checked out at '/Volumes/teaching/Code/LLamaLauncher/.worktrees/test-process-launch-side-effects'


```


## Assistant

<thinking>
The user wants me to continue implementing the tests for section 3.6 (Process Launch Side Effects). I've already:

1. Created a git worktree `.worktrees/test-process-launch-side-effects` on branch `test/process-launch-side-effects`
2. Read the Testing.md file for the test specifications
3. Read the main.py source code to understand the `_launch_model` method
4. Read existing test patterns in test_main.py and test_process.py
5. Started implementing the tests by adding them to test_process.py

But it looks like my last edit_file call didn't actually apply successfully - I need to check if the changes were applied or if I need to redo them.

Let me first check the current state of the file, then continue with implementing the tests properly.

Actually, looking at the terminal output, it seems like my previous edit_file call did work (it showed a successful diff). But I need to verify this and then run the tests to see if they pass.

Let me check the current state of test_process.py and then run the tests.

</thinking>

The worktree already exists from earlier. Let me check the current state of my changes and continue with the implementation.



**Tool Call: Read file `tests/test_process.py` (lines 520-560)**
Status: Completed

```LLamaLauncher/tests/test_process.py
   520	        ).collect_config()
   521	        builder = ProcessCommandBuilder(config)
   522	        cmd = builder.build_command()
   523	
   524	        assert "--ctx-size" not in cmd
   525	
   526	
   527	# ==================================================================
   528	# 3.6 Process Launch Side Effects
   529	# ==================================================================
   530	
   531	
   532	from unittest.mock import Any, MagicMock
   533	
   534	
   535	def _make_launch_app(**overrides: Any) -> MagicMock:
   536	    """Build a mock LlamaLaunchApp ready for _launch_model testing.
   537	
   538	    All widgets are configured with default values that represent
   539	    a minimal valid configuration (model selected, defaults for everything else).
   540	
   541	    Args:
   542	        **overrides: Named widget overrides replace defaults.
   543	
   544	    Returns:
   545	        MagicMock configured as a LlamaLaunchApp instance.
   546	    """
   547	    app = MagicMock()
   548	
   549	    # Required: model path must be set (otherwise _launch_model returns early)
   550	    model_path = overrides.get("model_path", "/models/llama.gguf")
   551	    app.model_path_edit = MagicMock()
   552	    app.model_path_edit.property.return_value = model_path
   553	
   554	    # Server widgets
   555	    host = overrides.get("host", "127.0.0.1")
   556	    port_str = overrides.get("port", "8080")
   557	    app.host_line_edit = MagicMock()
   558	    app.host_line_edit.text.return_value = host
   559	    app.port_line_edit = MagicMock()
   560	    app.port_line_edit.text.return_value = port_str

```


## Assistant

<thinking>
The user wants me to continue implementing the tests for section 3.6 (Process Launch Side Effects). I've already started adding the tests to test_process.py. Let me check the current state of the file and see if the tests were fully written, then run them to verify they pass.

Let me read more of the file to see what's been written so far.

</thinking>

Good, I can see my previous edits were applied. Let me check the full extent of what was written:



**Tool Call: Read file `tests/test_process.py` (lines 560-810)**
Status: Completed

```LLamaLauncher/tests/test_process.py
   560	    app.port_line_edit.text.return_value = port_str
   561	    app._host = overrides.get("_host", host)
   562	    app._port = overrides.get("_port", int(port_str))
   563	
   564	    # API key
   565	    app.api_key_line_edit = MagicMock()
   566	    app.api_key_line_edit.text.return_value = overrides.get("api_key", "")
   567	
   568	    # All spinboxes - default to 0
   569	    spinbox_params = [
   570	        "temperature",
   571	        "top_p",
   572	        "top_k",
   573	        "min_p",
   574	        "typical_p",
   575	        "repeat_penalty",
   576	        "repeat_last_n",
   577	        "presence_penalty",
   578	        "frequency_penalty",
   579	        "mirostat",
   580	        "mirostat_lr",
   581	        "mirostat_ent",
   582	        "gpu_layers",
   583	        "threads",
   584	        "threads_batch",
   585	        "batch_size",
   586	        "ubatch_size",
   587	        "n_predict",
   588	        "parallel",
   589	        "spec_draft_n_max",
   590	        "seed",
   591	        "rope_freq_base",
   592	        "rope_freq_scale",
   593	    ]
   594	    for param in spinbox_params:
   595	        sb = MagicMock()
   596	        sb.value.return_value = overrides.get(f"{param}_value", 0)
   597	        setattr(app, f"{param}_spinbox", sb)
   598	
   599	    # All checkboxes - default to unchecked
   600	    checkbox_params = [
   601	        "enable_temperature",
   602	        "enable_top_p",
   603	        "enable_top_k",
   604	        "enable_min_p",
   605	        "enable_typical_p",
   606	        "enable_repeat_penalty",
   607	        "enable_repeat_last_n",
   608	        "enable_presence_penalty",
   609	        "enable_frequency_penalty",
   610	        "enable_mirostat",
   611	        "enable_mirostat_lr",
   612	        "enable_mirostat_ent",
   613	        "enable_gpu_layers",
   614	        "enable_threads",
   615	        "enable_threads_batch",
   616	        "enable_batch_size",
   617	        "enable_ubatch_size",
   618	        "enable_n_predict",
   619	        "enable_parallel",
   620	        "enable_mmap",
   621	        "enable_mlock",
   622	        "enable_cont_batching",
   623	        "enable_draft_model",
   624	        "enable_spec_draft_n_max",
   625	        "enable_seed",
   626	        "enable_grammar",
   627	        "enable_json_schema",
   628	        "enable_rope_scaling",
   629	        "enable_rope_freq_base",
   630	        "enable_rope_freq_scale",
   631	        "enable_cache_type_k",
   632	        "enable_cache_type_v",
   633	    ]
   634	    for cb in checkbox_params:
   635	        cb_mock = MagicMock()
   636	        cb_mock.isChecked.return_value = overrides.get(f"{cb}_checked", False)
   637	        setattr(app, cb, cb_mock)
   638	
   639	    # Comboboxes
   640	    app.flash_attn_combobox = MagicMock()
   641	    app.flash_attn_combobox.currentText.return_value = overrides.get("flash_attn", "auto")
   642	    app.cache_type_k_combobox = MagicMock()
   643	    app.cache_type_k_combobox.currentText.return_value = overrides.get("cache_type_k", "f32")
   644	    app.cache_type_v_combobox = MagicMock()
   645	    app.cache_type_v_combobox.currentText.return_value = overrides.get("cache_type_v", "f32")
   646	    app.rope_scaling_combobox = MagicMock()
   647	    app.rope_scaling_combobox.currentText.return_value = overrides.get("rope_scaling", "linear")
   648	
   649	    # Path widgets
   650	    mmproj_path = overrides.get("mmproj_path", None)
   651	    app.mmproj_path_edit = MagicMock()
   652	    app.mmproj_path_edit.property.return_value = mmproj_path
   653	    app.draft_model_line_edit = MagicMock()
   654	    app.draft_model_line_edit.property.return_value = None
   655	    app.json_schema_line_edit = MagicMock()
   656	    app.json_schema_line_edit.property.return_value = None
   657	    app.grammar_line_edit = MagicMock()
   658	    app.grammar_line_edit.text.return_value = ""
   659	
   660	    # More options
   661	    app.more_options_line_edit = MagicMock()
   662	    app.more_options_line_edit.text.return_value = ""
   663	
   664	    # Context size - default to Auto (no ctx-size)
   665	    app.model_context_size = MagicMock()
   666	    app.model_context_size.currentIndex.return_value = 0
   667	    app.model_context_size.itemData.return_value = None
   668	
   669	    # No mmproj offload checkbox
   670	    app.no_mmproj_offload_checkbox = MagicMock()
   671	    app.no_mmproj_offload_checkbox.isChecked.return_value = False
   672	
   673	    # Side-effect widgets (captured by tests)
   674	    app.output_display = MagicMock()
   675	    app.launch_button = MagicMock()
   676	    app.server_web_view = MagicMock()
   677	    app._process = MagicMock()
   678	
   679	    return app
   680	
   681	
   682	class TestLaunchModelSideEffects:
   683	    """3.6: Testing side effects of _launch_model method."""
   684	
   685	    def test_3_6_1_sets_server_url(self) -> None:
   686	        """3.6.1: Sets _server_url after building command.
   687	
   688	        After constructing the command, the method should set
   689	        ``_server_url`` to ``http://{host}:{port}``.
   690	        """
   691	        # Arrange
   692	        from main import LlamaLaunchApp
   693	
   694	        app = _make_launch_app()
   695	
   696	        # Act
   697	        LlamaLaunchApp._launch_model(app)
   698	
   699	        # Assert
   700	        assert app._server_url == "http://127.0.0.1:8080"
   701	
   702	    def test_3_6_2_clears_output_display_before_launching(self) -> None:
   703	        """3.6.2: Clears output_display before launching.
   704	
   705	        The method should call ``output_display.clear()`` to wipe
   706	        previous output before writing the new launch message.
   707	        """
   708	        # Arrange
   709	        from main import LlamaLaunchApp
   710	
   711	        app = _make_launch_app()
   712	
   713	        # Act
   714	        LlamaLaunchApp._launch_model(app)
   715	
   716	        # Assert
   717	        app.output_display.clear.assert_called_once()
   718	
   719	    def test_3_6_3_appends_launch_command_to_output_display(self) -> None:
   720	        """3.6.3: Appends launch command to output_display.
   721	
   722	        After clearing, the method should append a line starting with
   723	        ``Launching: `` followed by the full command joined with spaces.
   724	        """
   725	        # Arrange
   726	        from main import LlamaLaunchApp
   727	
   728	        app = _make_launch_app()
   729	
   730	        # Act
   731	        LlamaLaunchApp._launch_model(app)
   732	
   733	        # Assert
   734	        call_args = app.output_display.appendPlainText.call_args
   735	        output_text = call_args[0][0]
   736	        assert output_text.startswith("Launching: ")
   737	        assert "llama-server" in output_text
   738	        assert "/models/llama.gguf" in output_text
   739	
   740	    def test_3_6_4_calls_process_start_with_program_and_args(self) -> None:
   741	        """3.6.4: Calls _process.start() with correct program and args list.
   742	
   743	        The two-argument form of ``QProcess.start`` is used:
   744	        first argument is the program, second is a list of arguments
   745	        (the program itself must NOT be in the list).
   746	        """
   747	        # Arrange
   748	        from main import LlamaLaunchApp
   749	
   750	        app = _make_launch_app()
   751	
   752	        # Act
   753	        LlamaLaunchApp._launch_model(app)
   754	
   755	        # Assert
   756	        app._process.start.assert_called_once()
   757	        call_args = app._process.start.call_args
   758	        program = call_args[0][0]
   759	        args = call_args[0][1]
   760	        assert program == "llama-server"
   761	        assert "llama-server" not in args
   762	        assert "--model" in args
   763	        assert "/models/llama.gguf" in args
   764	        assert "--host" in args
   765	        assert "127.0.0.1" in args
   766	        assert "--port" in args
   767	        assert "8080" in args
   768	
   769	    def test_3_6_5_updates_launch_button_text_to_stop(self) -> None:
   770	        """3.6.5: Updates launch_button text to STOP.
   771	
   772	        After starting the process, the button label should change
   773	        from its default to ``STOP`` so the user can stop the server.
   774	        """
   775	        # Arrange
   776	        from main import LlamaLaunchApp
   777	
   778	        app = _make_launch_app()
   779	
   780	        # Act
   781	        LlamaLaunchApp._launch_model(app)
   782	
   783	        # Assert
   784	        app.launch_button.setText.assert_called_once_with("STOP")
   785	
   786	    def test_3_6_6_updates_web_view_url_after_launch(self) -> None:
   787	        """3.6.6: Updates web view URL after launch.
   788	
   789	        The server web view should be pointed at the new server URL
   790	        so that users can immediately interact with the running server.
   791	        """
   792	        # Arrange
   793	        from main import LlamaLaunchApp
   794	
   795	        app = _make_launch_app()
   796	
   797	        # Act
   798	        LlamaLaunchApp._launch_model(app)
   799	
   800	        # Assert
   801	        app.server_web_view.setUrl.assert_called_once()
   802	        called_url = app.server_web_view.setUrl.call_args[0][0]
   803	        assert called_url == "http://127.0.0.1:8080"

```


## Assistant

<thinking>
The user wants me to continue with implementing the tests for section 3.6 (Process Launch Side Effects). Looking at my previous work, I can see that I've already:

1. Created a git worktree `.worktrees/test-process-launch-side-effects` on branch `test/process-launch-side-effects`
2. Added the `_make_launch_app` helper function to test_process.py
3. Added all 6 tests (3.6.1 through 3.6.6) to test_process.py

The tests are now fully written! Let me verify this by reading the end of the file, then run the tests to see if they pass.

Looking at the file content I just read, it ends at line 803 with the last test `test_3_6_6_updates_web_view_url_after_launch`. This looks complete - all 6 tests are there:
- test_3_6_1_sets_server_url
- test_3_6_2_clears_output_display_before_launching
- test_3_6_3_appends_launch_command_to_output_display
- test_3_6_4_calls_process_start_with_program_and_args
- test_3_6_5_updates_launch_button_text_to_stop
- test_3_6_6_updates_web_view_url_after_launch

Now I need to:
1. Run the tests to verify they pass
2. Fix any issues if they fail
3. Run linting and formatting as required by project rules

Let me first run just the new tests to see if they work.

</thinking>

Good - I can see all 6 tests for section 3.6 have been added to `test_process.py`. The file ends at line 803 with `test_3_6_6_updates_web_view_url_after_launch`. Now let me run the tests to verify they pass.



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher && uv run pytest tests/test_process.py::TestLaunchModelSideEffects -v 2>&1**
Status: Completed

Terminal:
```
================= test session starts ==================
platform darwin -- Python 3.14.0, pytest-9.1.0, pluggy-1.6.0 -- /Volumes/teaching/Code/LLamaLauncher/.venv/bin/python3
cachedir: .pytest_cache
PySide6 6.11.1 -- Qt runtime 6.11.1 -- Qt compiled 6.11.1
rootdir: /Volumes/teaching/Code/LLamaLauncher
configfile: pyproject.toml
plugins: cov-7.1.0, qt-4.5.0
collected 0 items / 1 error

======================== ERRORS ========================
________ ERROR collecting tests/test_process.py ________
ImportError while importing test module '/Volumes/teaching/Code/LLamaLauncher/tests/test_process.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Users/jmacey/.local/share/uv/python/cpython-3.14.0-macos-aarch64-none/lib/python3.14/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/test_process.py:532: in <module>
    from unittest.mock import Any, MagicMock
E   ImportError: cannot import name 'Any' from 'unittest.mock' (/Users/jmacey/.local/share/uv/python/cpython-3.14.0-macos-aarch64-none/lib/python3.14/unittest/mock.py)
=============== short test summary info ================
ERROR tests/test_process.py
=================== 1 error in 0.05s ===================
ERROR: found no collectors for /Volumes/teaching/Code/LLamaLauncher/tests/test_process.py::TestLaunchModelSideEffects


```


## Assistant

<thinking>
The user's tests failed because I imported `Any` from `unittest.mock`, but `Any` is actually from the `typing` module, not `unittest.mock`. I need to fix this import error.

Let me fix the import statement in test_process.py.

</thinking>

I need to fix the import - `Any` comes from `typing`, not `unittest.mock`.



**Tool Call: tests/test\_process.py**
Status: Completed

Diff: tests/test_process.py
```
"""Tests for ProcessCommandBuilder - building llama-server command line.

Phase 3: Process Command Building

Tests the logic that constructs the llama-server command from configuration
collected by ConfigCollector. Each test verifies one aspect of command building.

Following the Testing.md Phase 3 plan:
- 3.1 Base Command (llama-server + --model + --api-key)
- 3.2 Sampling Parameters (conditional inclusion based on checkbox state)
"""

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


from typing import Any
from unittest.mock import MagicMock


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

```


## Assistant

<thinking>
The user's tests failed because I imported `Any` from `unittest.mock`, but `Any` is actually from the `typing` module. I've already fixed this import error. Now I need to run the tests again to see if they pass.

</thinking>

Now let me run the tests again:



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher && uv run pytest tests/test_process.py::TestLaunchModelSideEffects -v 2>&1**
Status: Completed

Terminal:
```
================= test session starts ==================
platform darwin -- Python 3.14.0, pytest-9.1.0, pluggy-1.6.0 -- /Volumes/teaching/Code/LLamaLauncher/.venv/bin/python3
cachedir: .pytest_cache
PySide6 6.11.1 -- Qt runtime 6.11.1 -- Qt compiled 6.11.1
rootdir: /Volumes/teaching/Code/LLamaLauncher
configfile: pyproject.toml
plugins: cov-7.1.0, qt-4.5.0
collected 6 items

tests/test_process.py::TestLaunchModelSideEffects::test_3_6_1_sets_server_url PASSED [ 16%]
tests/test_process.py::TestLaunchModelSideEffects::test_3_6_2_clears_output_display_before_launching PASSED [ 33%]
tests/test_process.py::TestLaunchModelSideEffects::test_3_6_3_appends_launch_command_to_output_display PASSED [ 50%]
tests/test_process.py::TestLaunchModelSideEffects::test_3_6_4_calls_process_start_with_program_and_args PASSED [ 66%]
tests/test_process.py::TestLaunchModelSideEffects::test_3_6_5_updates_launch_button_text_to_stop PASSED [ 83%]
tests/test_process.py::TestLaunchModelSideEffects::test_3_6_6_updates_web_view_url_after_launch PASSED [100%]

================== 6 passed in 0.68s ===================

```


## Assistant

<thinking>
The user's tests all passed! All 6 tests for section 3.6 (Process Launch Side Effects) are now passing:
- test_3_6_1_sets_server_url PASSED
- test_3_6_2_clears_output_display_before_launching PASSED
- test_3_6_3_appends_launch_command_to_output_display PASSED
- test_3_6_4_calls_process_start_with_program_and_args PASSED
- test_3_6_5_updates_launch_button_text_to_stop PASSED
- test_3_6_6_updates_web_view_url_after_launch PASSED

Now I need to:
1. Run linting (ruff check)
2. Run formatting (ruff format)
3. Run the full test suite to ensure no regressions
4. Follow the git workflow requirements (commit, etc.)

Let me run these steps now.

</thinking>

All 6 tests pass. Now let me run linting, formatting, and the full test suite as required by the project rules.



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher && uv run ruff check tests/test_process.py 2>&1**
Status: Completed

Terminal:
```
warning: Support for Python 3.14 is under development and may be unstable. Enable `preview` to remove this warning.
tests/test_process.py:532:1: E402 Module level import not at top of file
    |
532 | from typing import Any
    | ^^^^^^^^^^^^^^^^^^^^^^ E402
533 | from unittest.mock import MagicMock
    |

tests/test_process.py:533:1: E402 Module level import not at top of file
    |
532 | from typing import Any
533 | from unittest.mock import MagicMock
    | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ E402
    |

Found 2 errors.

```


**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher && uv run ruff format tests/test_process.py 2>&1**
Status: Completed

Terminal:
```
1 file reformatted




```


## Assistant

<thinking>
The user's tests passed, but ruff is complaining about E402 (module level import not at top of file). I need to move the imports to the top of the file instead of having them in the middle. Let me fix this by moving the imports to the top of test_process.py and removing them from where they are now.

</thinking>

The imports need to be at the top of the file, not in the middle. Let me fix this by adding them to the existing imports section and removing them from the middle of the file.



**Tool Call: Read file `tests/test_process.py` (lines 1-30)**
Status: Completed

```LLamaLauncher/tests/test_process.py
     1	"""Tests for ProcessCommandBuilder - building llama-server command line.
     2	
     3	Phase 3: Process Command Building
     4	
     5	Tests the logic that constructs the llama-server command from configuration
     6	collected by ConfigCollector. Each test verifies one aspect of command building.
     7	
     8	Following the Testing.md Phase 3 plan:
     9	- 3.1 Base Command (llama-server + --model + --api-key)
    10	- 3.2 Sampling Parameters (conditional inclusion based on checkbox state)
    11	"""
    12	
    13	from process_command import ProcessCommandBuilder
    14	
    15	from .test_config import (
    16	    MockCheckBox,
    17	    MockComboBox,
    18	    MockLineEdit,
    19	    MockPathEdit,
    20	    MockSpinBox,
    21	    _make_collector,
    22	)
    23	
    24	# ==================================================================
    25	# 3.1 Base Command
    26	# ==================================================================
    27	
    28	
    29	class TestBaseCommand:
    30	    """3.1: Base command construction with llama-server and required flags."""

```


## Assistant

<thinking>
The user's tests passed, but ruff is complaining about E402 (module level import not at top of file). I need to move the imports to the top of the file instead of having them in the middle. Let me fix this by moving the imports to the top of test_process.py and removing them from where they are now.

I need to:
1. Add `from typing import Any` and `from unittest.mock import MagicMock` to the existing imports at the top
2. Remove the duplicate imports from line 532-533 in the middle of the file

</thinking>

The user's tests passed, but ruff is complaining about E402 (imports not at top of file). I need to move the imports to the top and remove them from the middle.



**Tool Call: tests/test\_process.py**
Status: Completed

Diff: tests/test_process.py
```
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

```


## Assistant

<thinking>
The user's tests passed, but ruff was complaining about E402 (imports not at top of file). I've now fixed this by:
1. Moving the imports to the top of the file
2. Removing the duplicate imports from the middle

Now I need to:
1. Run ruff check again to verify no more linting errors
2. Run the tests again to make sure they still pass
3. Run the full test suite to ensure no regressions
4. Follow the git workflow requirements

Let me run these steps now.

</thinking>

Good, I've moved the imports to the top of the file. Now let me verify the linting passes and the tests still work.



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher && uv run ruff check tests/test_process.py 2>&1**
Status: Completed

Terminal:
```
warning: Support for Python 3.14 is under development and may be unstable. Enable `preview` to remove this warning.
All checks passed!

```


## Assistant

<thinking>
The linting passes now. Let me run the tests again to make sure they still pass after the import changes, then run the full test suite to ensure no regressions.

</thinking>

Linting passes. Now let me verify the tests still pass and then run the full test suite.



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher && uv run pytest tests/test_process.py::TestLaunchModelSideEffects -v 2>&1**
Status: Completed

Terminal:
```
================= test session starts ==================
platform darwin -- Python 3.14.0, pytest-9.1.0, pluggy-1.6.0 -- /Volumes/teaching/Code/LLamaLauncher/.venv/bin/python3
cachedir: .pytest_cache
PySide6 6.11.1 -- Qt runtime 6.11.1 -- Qt compiled 6.11.1
rootdir: /Volumes/teaching/Code/LLamaLauncher
configfile: pyproject.toml
plugins: cov-7.1.0, qt-4.5.0
collected 6 items

tests/test_process.py::TestLaunchModelSideEffects::test_3_6_1_sets_server_url PASSED [ 16%]
tests/test_process.py::TestLaunchModelSideEffects::test_3_6_2_clears_output_display_before_launching PASSED [ 33%]
tests/test_process.py::TestLaunchModelSideEffects::test_3_6_3_appends_launch_command_to_output_display PASSED [ 50%]
tests/test_process.py::TestLaunchModelSideEffects::test_3_6_4_calls_process_start_with_program_and_args PASSED [ 66%]
tests/test_process.py::TestLaunchModelSideEffects::test_3_6_5_updates_launch_button_text_to_stop PASSED [ 83%]
tests/test_process.py::TestLaunchModelSideEffects::test_3_6_6_updates_web_view_url_after_launch PASSED [100%]

================== 6 passed in 0.53s ===================

```


## Assistant

<thinking>
The user's tests still pass after the import changes. Now I need to run the full test suite to ensure no regressions, as required by the project rules. Let me run all tests to verify everything works together.

</thinking>

All 6 tests still pass. Now let me run the full test suite to ensure no regressions.



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher && uv run pytest -v 2>&1**
Status: Completed

Terminal:
```
================= test session starts ==================
platform darwin -- Python 3.14.0, pytest-9.1.0, pluggy-1.6.0 -- /Volumes/teaching/Code/LLamaLauncher/.venv/bin/python3
cachedir: .pytest_cache
PySide6 6.11.1 -- Qt runtime 6.11.1 -- Qt compiled 6.11.1
rootdir: /Volumes/teaching/Code/LLamaLauncher
configfile: pyproject.toml
testpaths: tests
plugins: cov-7.1.0, qt-4.5.0
collected 110 items

tests/test_config.py::TestVersionString::test_collects_version_string_as_1_0 PASSED [  0%]
tests/test_config.py::TestFilePaths::test_collects_model_path_from_fullPath_property PASSED [  1%]
tests/test_config.py::TestFilePaths::test_collects_mmproj_and_draft_and_json_schema_paths PASSED [  2%]
tests/test_config.py::TestFilePaths::test_handles_empty_paths_as_empty_strings_not_none PASSED [  3%]
tests/test_config.py::TestServerSettings::test_collects_server_host_port_api_key PASSED [  4%]
tests/test_config.py::TestServerSettings::test_handles_invalid_port_text_as_default_8080 PASSED [  5%]
tests/test_config.py::TestServerSettings::test_handles_empty_port_text_as_default_8080 PASSED [  6%]
tests/test_config.py::TestSamplingParameters::test_sampling_param_has_enabled_and_value_format PASSED [  7%]
tests/test_config.py::TestSamplingParameters::test_collects_all_sampling_params PASSED [  8%]
tests/test_config.py::TestPerformanceParameters::test_performance_params_have_enabled_value_format PASSED [  9%]
tests/test_config.py::TestPerformanceParameters::test_collects_flash_attn_combobox_text PASSED [ 10%]
tests/test_config.py::TestPerformanceParameters::test_collects_mmap_mlock_cont_batching_booleans PASSED [ 10%]
tests/test_config.py::TestAdvancedParameters::test_collects_advanced_params PASSED [ 11%]
tests/test_config.py::TestAdvancedParameters::test_collects_rope_scaling_combobox_text PASSED [ 12%]
tests/test_config.py::TestOtherSettings::test_collects_context_size_from_user_role PASSED [ 13%]
tests/test_config.py::TestOtherSettings::test_collects_more_options_and_no_mmproj_offload PASSED [ 14%]
tests/test_config.py::TestEndToEnd::test_collect_config_returns_all_expected_keys PASSED [ 15%]
tests/test_config.py::TestEndToEnd::test_config_round_trip_save_and_load PASSED [ 16%]
tests/test_helper_methods.py::TestSetPathField::test_sets_fullpath_property_and_displays_short_filename PASSED [ 17%]
tests/test_helper_methods.py::TestSetPathField::test_handles_empty_path_clears_field PASSED [ 18%]
tests/test_helper_methods.py::TestSetPathField::test_handles_none_path_clears_field PASSED [ 19%]
tests/test_helper_methods.py::TestApplyParam::test_applies_enabled_plus_value_dict_format PASSED [ 20%]
tests/test_helper_methods.py::TestApplyParam::test_applies_disabled_parameter PASSED [ 20%]
tests/test_helper_methods.py::TestApplyParam::test_handles_legacy_format_just_value PASSED [ 21%]
tests/test_helper_methods.py::TestApplyParam::test_ignores_missing_parameter_name PASSED [ 22%]
tests/test_helper_methods.py::TestApplyComboParam::test_applies_enabled_plus_value_dict_format PASSED [ 23%]
tests/test_helper_methods.py::TestApplyComboParam::test_applies_disabled_combobox_parameter PASSED [ 24%]
tests/test_helper_methods.py::TestApplyComboParam::test_handles_legacy_format_just_value PASSED [ 25%]
tests/test_helper_methods.py::TestApplyComboParam::test_handles_missing_combobox_item PASSED [ 26%]
tests/test_helper_methods.py::TestApplyComboParam::test_ignores_missing_parameter_name PASSED [ 27%]
tests/test_main.py::TestWriteConfigFile::test_writes_valid_json_to_file_path PASSED [ 28%]
tests/test_main.py::TestWriteConfigFile::test_appends_success_message_to_output_display PASSED [ 29%]
tests/test_main.py::TestWriteConfigFile::test_shows_qmessagebox_critical_on_write_failure PASSED [ 30%]
tests/test_main.py::TestApplyConfig::test_2_4_1_applies_files_section PASSED [ 30%]
tests/test_main.py::TestApplyConfig::test_2_4_1_empty_files_section PASSED [ 31%]
tests/test_main.py::TestApplyConfig::test_2_4_2_applies_server_section_with_defaults PASSED [ 32%]
tests/test_main.py::TestApplyConfig::test_2_4_2_applies_server_section_with_custom_values PASSED [ 33%]
tests/test_main.py::TestApplyConfig::test_2_4_3_applies_sampling_parameters PASSED [ 34%]
tests/test_main.py::TestApplyConfig::test_2_4_3_sampling_with_legacy_scalar_values PASSED [ 35%]
tests/test_main.py::TestApplyConfig::test_2_4_4_applies_performance_parameters PASSED [ 36%]
tests/test_main.py::TestApplyConfig::test_2_4_5_applies_flash_attn_combobox PASSED [ 37%]
tests/test_main.py::TestApplyConfig::test_2_4_5_flash_attn_not_found PASSED [ 38%]
tests/test_main.py::TestApplyConfig::test_2_4_6_applies_cache_type_combo_params PASSED [ 39%]
tests/test_main.py::TestApplyConfig::test_2_4_7_applies_boolean_performance_params PASSED [ 40%]
tests/test_main.py::TestApplyConfig::test_2_4_8_applies_advanced_section PASSED [ 40%]
tests/test_main.py::TestApplyConfig::test_2_4_9_applies_draft_model_path_based_params PASSED [ 41%]
tests/test_main.py::TestApplyConfig::test_2_4_9_draft_model_disabled PASSED [ 42%]
tests/test_main.py::TestApplyConfig::test_2_4_10_applies_grammar_path_based_params PASSED [ 43%]
tests/test_main.py::TestApplyConfig::test_2_4_11_applies_json_schema_path_based_params PASSED [ 44%]
tests/test_main.py::TestApplyConfig::test_2_4_12_applies_rope_scaling_combo_param PASSED [ 45%]
tests/test_main.py::TestApplyConfig::test_2_4_13_applies_context_size_selection PASSED [ 46%]
tests/test_main.py::TestApplyConfig::test_2_4_13_context_size_not_found PASSED [ 47%]
tests/test_main.py::TestApplyConfig::test_2_4_14_applies_more_options_and_no_mmproj_offload PASSED [ 48%]
tests/test_main.py::TestApplyConfig::test_2_4_14_no_mmproj_offload_false PASSED [ 49%]
tests/test_main.py::TestApplyConfig::test_2_4_15_handles_missing_config_sections_gracefully PASSED [ 50%]
tests/test_main.py::TestApplyConfig::test_2_4_15_handles_empty_sections_gracefully PASSED [ 50%]
tests/test_main.py::TestApplyConfig::test_2_4_applies_all_sections_together PASSED [ 51%]
tests/test_main.py::TestApplyConfig::test_2_4_sampling_with_disabled_params PASSED [ 52%]
tests/test_main.py::TestApplyConfig::test_2_4_advanced_with_rope_params PASSED [ 53%]
tests/test_process.py::TestBaseCommand::test_base_command_includes_llama_server_and_model PASSED [ 54%]
tests/test_process.py::TestBaseCommand::test_base_command_includes_api_key_default_when_empty PASSED [ 55%]
tests/test_process.py::TestBaseCommand::test_base_command_includes_custom_api_key PASSED [ 56%]
tests/test_process.py::TestTemperatureParameter::test_includes_temp_when_temperature_enabled PASSED [ 57%]
tests/test_process.py::TestTemperatureParameter::test_omits_temp_when_temperature_disabled PASSED [ 58%]
tests/test_process.py::TestTopPParameter::test_includes_top_p_when_enabled PASSED [ 59%]
tests/test_process.py::TestTopPParameter::test_omits_top_p_when_disabled PASSED [ 60%]
tests/test_process.py::TestTopKParameter::test_includes_top_k_when_enabled PASSED [ 60%]
tests/test_process.py::TestTopKParameter::test_omits_top_k_when_disabled PASSED [ 61%]
tests/test_process.py::TestMinPParameter::test_includes_min_p_when_enabled PASSED [ 62%]
tests/test_process.py::TestMinPParameter::test_omits_min_p_when_disabled PASSED [ 63%]
tests/test_process.py::TestTypicalPParameter::test_includes_typical_p_when_enabled PASSED [ 64%]
tests/test_process.py::TestTypicalPParameter::test_omits_typical_p_when_disabled PASSED [ 65%]
tests/test_process.py::TestRepeatPenaltyParameter::test_includes_repeat_penalty_when_enabled PASSED [ 66%]
tests/test_process.py::TestRepeatPenaltyParameter::test_omits_repeat_penalty_when_disabled PASSED [ 67%]
tests/test_process.py::TestRepeatLastNParameter::test_includes_repeat_last_n_when_enabled PASSED [ 68%]
tests/test_process.py::TestRepeatLastNParameter::test_omits_repeat_last_n_when_disabled PASSED [ 69%]
tests/test_process.py::TestPresencePenaltyParameter::test_includes_presence_penalty_when_enabled PASSED [ 70%]
tests/test_process.py::TestPresencePenaltyParameter::test_omits_presence_penalty_when_disabled PASSED [ 70%]
tests/test_process.py::TestFrequencyPenaltyParameter::test_includes_frequency_penalty_when_enabled PASSED [ 71%]
tests/test_process.py::TestFrequencyPenaltyParameter::test_omits_frequency_penalty_when_disabled PASSED [ 72%]
tests/test_process.py::TestMirostatParameters::test_includes_all_mirostat_params_when_enabled PASSED [ 73%]
tests/test_process.py::TestMirostatParameters::test_omits_mirostat_when_disabled PASSED [ 74%]
tests/test_process.py::TestMirostatParameters::test_omits_mirostat_lr_when_disabled PASSED [ 75%]
tests/test_process.py::TestMirostatParameters::test_omits_mirostat_ent_when_disabled PASSED [ 76%]
tests/test_process.py::TestServerHostPort::test_uses_host_from_config PASSED [ 77%]
tests/test_process.py::TestServerHostPort::test_uses_port_from_config PASSED [ 78%]
tests/test_process.py::TestServerHostPort::test_handles_invalid_port_falls_back_to_default PASSED [ 79%]
tests/test_process.py::TestMmprojParameters::test_includes_mmproj_when_path_set PASSED [ 80%]
tests/test_process.py::TestMmprojParameters::test_includes_no_mmproj_offload_when_mmproj_and_checkbox_checked PASSED [ 80%]
tests/test_process.py::TestMmprojParameters::test_omits_no_mmproj_offload_when_checkbox_unchecked PASSED [ 81%]
tests/test_process.py::TestExtraFlags::test_parses_extra_flags_from_more_options PASSED [ 82%]
tests/test_process.py::TestExtraFlags::test_omits_extra_flags_when_empty PASSED [ 83%]
tests/test_process.py::TestContextSize::test_includes_ctx_size_when_greater_than_zero PASSED [ 84%]
tests/test_process.py::TestContextSize::test_omits_ctx_size_when_zero PASSED [ 85%]
tests/test_process.py::TestLaunchModelSideEffects::test_3_6_1_sets_server_url PASSED [ 86%]
tests/test_process.py::TestLaunchModelSideEffects::test_3_6_2_clears_output_display_before_launching PASSED [ 87%]
tests/test_process.py::TestLaunchModelSideEffects::test_3_6_3_appends_launch_command_to_output_display PASSED [ 88%]
tests/test_process.py::TestLaunchModelSideEffects::test_3_6_4_calls_process_start_with_program_and_args PASSED [ 89%]
tests/test_process.py::TestLaunchModelSideEffects::test_3_6_5_updates_launch_button_text_to_stop PASSED [ 90%]
tests/test_process.py::TestLaunchModelSideEffects::test_3_6_6_updates_web_view_url_after_launch PASSED [ 90%]
tests/test_ui_loader.py::TestLoadUIFileErrors::test_load_ui_raises_when_file_does_not_exist PASSED [ 91%]
tests/test_ui_loader.py::TestLoadUIFileErrors::test_load_ui_raises_when_file_open_fails PASSED [ 92%]
tests/test_ui_loader.py::TestLoadUIFileErrors::test_load_ui_raises_when_file_is_invalid PASSED [ 93%]
tests/test_ui_loader.py::TestLoadUIWidgetAttributeAssignment::test_load_ui_assigns_widget_attributes_by_object_name PASSED [ 94%]
tests/test_ui_loader.py::TestLoadUIWidgetAttributeAssignment::test_load_ui_assigns_layout_attributes_by_object_name PASSED [ 95%]
tests/test_ui_loader.py::TestLoadUIWidgetAttributeAssignment::test_load_ui_captures_top_level_layout_not_in_find_children PASSED [ 96%]
tests/test_ui_loader.py::TestLoadUISetupByParentType::test_load_ui_sets_up_dialog_correctly PASSED [ 97%]
tests/test_ui_loader.py::TestLoadUISetupByParentType::test_load_ui_sets_up_main_window_correctly PASSED [ 98%]
tests/test_ui_loader.py::TestLoadUISetupByParentType::test_load_ui_embeds_widget_via_zero_margin_layout PASSED [ 99%]
tests/test_ui_loader.py::TestLoadUIPathSupport::test_load_ui_accepts_path_object PASSED [100%]

================= 110 passed in 0.52s ==================

```


## Assistant

<thinking>
The user's tests all passed! All 6 tests for section 3.6 (Process Launch Side Effects) are passing, and the full test suite (110 tests) is also passing with no regressions.

Let me provide a summary of what was accomplished:

1. Created a git worktree `.worktrees/test-process-launch-side-effects` on branch `test/process-launch-side-effects`
2. Implemented 6 tests for section 3.6 (Process Launch Side Effects):
   - test_3_6_1_sets_server_url - Verifies _server_url is set after building command
   - test_3_6_2_clears_output_display_before_launching - Verifies output_display.clear() is called
   - test_3_6_3_appends_launch_command_to_output_display - Verifies launch command is logged
   - test_3_6_4_calls_process_start_with_program_and_args - Verifies _process.start() is called correctly
   - test_3_6_5_updates_launch_button_text_to_stop - Verifies launch_button text is set to "STOP"
   - test_3_6_6_updates_web_view_url_after_launch - Verifies web view URL is updated

3. Created a helper function `_make_launch_app()` that builds a mock LlamaLaunchApp with all necessary widgets configured
4. Fixed linting issues (E402 - imports not at top of file)
5. All 110 tests pass with no regressions

The task is complete! I should summarize this for the user.

</thinking>

All 110 tests pass with no regressions. Here's a summary of what was implemented:

## Summary

### Tests Implemented (Section 3.6 - Process Launch Side Effects)

Added 6 new tests to `tests/test_process.py`:

| # | Test | Verification |
|---|-------|--------------|
| 3.6.1 | `test_3_6_1_sets_server_url` | `_server_url` set to `http://{host}:{port}` |
| 3.6.2 | `test_3_6_2_clears_output_display_before_launching` | `output_display.clear()` called once |
| 3.6.3 | `test_3_6_3_appends_launch_command_to_output_display` | Output starts with "Launching: " and contains command details |
| 3.6.4 | `test_3_6_4_calls_process_start_with_program_and_args` | `_process.start("llama-server", args)` called correctly |
| 3.6.5 | `test_3_6_5_updates_launch_button_text_to_stop` | `launch_button.setText("STOP")` called |
| 3.6.6 | `test_3_6_6_updates_web_view_url_after_launch` | `server_web_view.setUrl()` called with correct URL |

### Helper Function

Created `_make_launch_app(**overrides)` - a mock builder that configures all required widget attributes (23 spinboxes, 33 checkboxes, comboboxes, path widgets, etc.) to simulate a minimal valid app state for testing `_launch_model`.

### Validation

- All 6 new tests pass
- Full test suite: **110/110 passed** (no regressions)
- Ruff linting: clean
