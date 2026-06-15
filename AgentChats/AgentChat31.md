## User

[@test-driven-development](zed:///agent/skill?name=test-driven-development&source=LLamaLauncher&path=%2FVolumes%2Fteaching%2FCode%2FLLamaLauncher%2F.agents%2Fskills%2Ftest-driven-development%2FSKILL.md) At present there are no tests in this project, make a plan in a file called Testing.md to outline the order tests should be added to the project. This should be in the form of a todo list and eventually we need > 90% test coverage on the project.

## Assistant

<thinking>
The user wants me to create a Testing.md file that outlines the order tests should be added to their project, in the form of a todo list, with the goal of achieving >90% test coverage. I need to first understand the project structure and codebase before creating this plan.

Let me start by exploring the project structure and understanding what modules/components exist.

</thinking>

I'll start by understanding the project structure and codebase to create an informed testing plan.



**Tool Call: List the `Volumes/teaching/Code/LLamaLauncher` directory's contents**
Status: Failed

Path Volumes/teaching/Code/LLamaLauncher is not in the project

**Tool Call: Read file**
Status: Failed

```json
{
  "Text": "Path Volumes/teaching/Code/LLamaLauncher/pyproject.toml is not in the project"
}
```

## Assistant

<thinking>
The user's project root directory must be `LLamaLauncher` based on the project roots listed earlier. Let me use the correct path.

</thinking>

Let me use the correct project-relative paths.



**Tool Call: List the `LLamaLauncher` directory's contents**
Status: Completed

# Folders:
LLamaLauncher/.agents
LLamaLauncher/.ruff_cache
LLamaLauncher/.venv
LLamaLauncher/.worktrees
LLamaLauncher/AgentChats
LLamaLauncher/__pycache__
LLamaLauncher/docs
LLamaLauncher/ui

# Files:
LLamaLauncher/.gitignore
LLamaLauncher/.python-version
LLamaLauncher/AGENTS.md
LLamaLauncher/README.md
LLamaLauncher/SmallModel.json
LLamaLauncher/TODO.md
LLamaLauncher/headroom_memory.db
LLamaLauncher/main.py
LLamaLauncher/pyproject.toml
LLamaLauncher/test.json
LLamaLauncher/ui_loader.py
LLamaLauncher/uv.lock


**Tool Call: Read file `pyproject.toml`**
Status: Completed

```LLamaLauncher/pyproject.toml
     1	[project]
     2	name = "llamalauncher"
     3	version = "0.1.0"
     4	description = "Add your description here"
     5	readme = "README.md"
     6	requires-python = ">=3.14"
     7	dependencies = [
     8	    "pyside6>=6.11.1",
     9	    "requests>=2.34.2",
    10	]
    11	
    12	[dependency-groups]
    13	dev = [
    14	    "pytest>=9.1.0",
    15	]

```


## Assistant

The project uses PySide6 for GUI, requests for HTTP, and has pytest already in dev dependencies. Let me now read all the source files to understand the codebase.



**Tool Call: Read file `main.py`**
Status: Completed

```
SUCCESS: File outline retrieved. This file is too large to read all at once, so the outline below shows the file's structure with line numbers.

IMPORTANT: Do NOT retry this call without line numbers - you will get the same outline.
Instead, use the line numbers below to read specific sections by calling this tool again with start_line and end_line parameters.

# File outline for /Volumes/teaching/Code/LLamaLauncher/main.py

class LlamaLaunchApp [L25-880]
 def __init__ [L32-54]
 def _create_cache_dir [L60-68]
 def _create_persistent_profile [L70-94]
 def _init_web_view [L96-105]
 def _setup_ui [L107-117]
 def _setup_context_size_combo [L119-152]
 def _create_file_menu [L158-179]
 def _save_config [L185-190]
 def _save_config_as [L192-202]
 def _write_config_file [L204-216]
 def _collect_config [L218-291]
 def _load_config [L293-313]
 def _apply_config [L315-420]
 def _set_path_field [L422-434]
 def _apply_param [L436-453]
 def _apply_combo_param [L455-477]
 def closeEvent [L483-490]
 def _save_last_session [L492-498]
 def _load_last_session [L500-522]
 def _connect_signals [L528-535]
 def _select_model [L541-558]
 def _select_mmproj [L560-576]
 def _select_draft_model [L578-593]
 def _select_json_schema [L595-610]
 def _on_model_selection_changed [L612-616]
 def _toggle_launch [L618-623]
 def _stop_model [L625-634]
 def _force_kill_if_needed [L636-640]
 def _reset_launch_button [L642-645]
 def _launch_model [L647-818]
 def _on_stdout [L824-833]
 def _on_stderr [L835-844]
 def _check_and_refresh [L846-860]
 def _refresh_web_view [L862-866]
 def _on_error [L868-872]
 def _on_finished [L874-880]

Showing symbols 1-37 (total symbols: 37)


NEXT STEPS: To read a specific symbol's implementation, call read_file with the same path plus start_line and end_line from the outline above.
For example, to read a function shown as [L100-150], use start_line: 100 and end_line: 150.
```


**Tool Call: Read file `ui_loader.py`**
Status: Completed

```LLamaLauncher/ui_loader.py
     1	from pathlib import Path
     2	from typing import TypeVar, Union
     3	
     4	from PySide6.QtCore import QFile
     5	from PySide6.QtUiTools import QUiLoader
     6	from PySide6.QtWidgets import QDialog, QLayout, QMainWindow, QVBoxLayout, QWidget
     7	
     8	T = TypeVar("T", bound=QWidget)
     9	
    10	
    11	def load_ui(ui_file_path: Union[str, Path], parent: T) -> QWidget:
    12	    """Load a .ui file and set up the widget connections.
    13	
    14	    Parameters :
    15	        ui_file_path : Union[str, Path]
    16	            Path to the .ui file to load.
    17	        parent : T
    18	            The parent widget to load the UI into.
    19	
    20	    Returns :
    21	        The loaded widget with all children accessible as attributes.
    22	    """
    23	    loader = QUiLoader()
    24	    ui_file = QFile(ui_file_path)
    25	    if not ui_file.open(QFile.ReadOnly):
    26	        raise RuntimeError(f"Cannot open UI file: {ui_file_path}")
    27	
    28	    loaded_ui = loader.load(ui_file, parent)
    29	    ui_file.close()
    30	
    31	    if loaded_ui is None:
    32	        raise RuntimeError(f"Failed to load UI file: {ui_file_path}")
    33	
    34	    for widget in loaded_ui.findChildren(QWidget):
    35	        name = widget.objectName()
    36	        if name:
    37	            setattr(parent, name, widget)
    38	
    39	    for layout in loaded_ui.findChildren(QLayout):
    40	        name = layout.objectName()
    41	        if name:
    42	            setattr(parent, name, layout)
    43	
    44	    # Also capture the top-level layout if it wasn't found by findChildren
    45	    main_layout = loaded_ui.layout()
    46	    if main_layout:
    47	        name = main_layout.objectName()
    48	        if name and not hasattr(parent, name):
    49	            setattr(parent, name, main_layout)
    50	
    51	    if isinstance(parent, QDialog):
    52	        if loaded_ui.layout():
    53	            parent.setLayout(loaded_ui.layout())
    54	        parent.setWindowTitle(loaded_ui.windowTitle())
    55	        parent.resize(loaded_ui.size())
    56	    elif isinstance(parent, QMainWindow):
    57	        parent.setCentralWidget(loaded_ui)
    58	        parent.setWindowTitle(loaded_ui.windowTitle())
    59	        parent.resize(loaded_ui.size())
    60	    else:
    61	        # Plain QWidget: embed loaded_ui via a zero-margin layout so its
    62	        # contents fill the parent window.
    63	        container = QVBoxLayout(parent)
    64	        container.setContentsMargins(0, 0, 0, 0)
    65	        container.addWidget(loaded_ui)
    66	        parent.setWindowTitle(loaded_ui.windowTitle())
    67	        parent.resize(loaded_ui.size())
    68	
    69	    return loaded_ui

```


**Tool Call: List the `LLamaLauncher/AgentChats` directory's contents**
Status: Completed


# Files:
LLamaLauncher/AgentChats/AgentChat1.md
LLamaLauncher/AgentChats/AgentChat10.md
LLamaLauncher/AgentChats/AgentChat11.md
LLamaLauncher/AgentChats/AgentChat12.md
LLamaLauncher/AgentChats/AgentChat13.md
LLamaLauncher/AgentChats/AgentChat14.md
LLamaLauncher/AgentChats/AgentChat15.md
LLamaLauncher/AgentChats/AgentChat16.md
LLamaLauncher/AgentChats/AgentChat17.md
LLamaLauncher/AgentChats/AgentChat18.md
LLamaLauncher/AgentChats/AgentChat19.md
LLamaLauncher/AgentChats/AgentChat2.md
LLamaLauncher/AgentChats/AgentChat20.md
LLamaLauncher/AgentChats/AgentChat21.md
LLamaLauncher/AgentChats/AgentChat22.md
LLamaLauncher/AgentChats/AgentChat23.md
LLamaLauncher/AgentChats/AgentChat24.md
LLamaLauncher/AgentChats/AgentChat25.md
LLamaLauncher/AgentChats/AgentChat26.md
LLamaLauncher/AgentChats/AgentChat27.md
LLamaLauncher/AgentChats/AgentChat28.md
LLamaLauncher/AgentChats/AgentChat29.md
LLamaLauncher/AgentChats/AgentChat3.md
LLamaLauncher/AgentChats/AgentChat30.md
LLamaLauncher/AgentChats/AgentChat4.md
LLamaLauncher/AgentChats/AgentChat5.md
LLamaLauncher/AgentChats/AgentChat6.md
LLamaLauncher/AgentChats/AgentChat7.md
LLamaLauncher/AgentChats/AgentChat8.md
LLamaLauncher/AgentChats/AgentChat9.md
LLamaLauncher/AgentChats/LLamaLauncher Scrollable Parameters Fix Launch Button
LLamaLauncher/AgentChats/WebChatAboutParams.md


**Tool Call: List the `LLamaLauncher/ui` directory's contents**
Status: Completed


# Files:
LLamaLauncher/ui/llama_launch.ui


## Assistant

<thinking>
Now I need to understand the main.py file in detail to plan tests properly. Let me read the key sections.

</thinking>

Let me read the main application class in sections to understand its logic for planning tests.



**Tool Call: Read file `main.py` (lines 25-120)**
Status: Completed

```LLamaLauncher/main.py
    25	class LlamaLaunchApp(QMainWindow):
    26	    """Main application window for the Llama model launcher.
    27	
    28	    Loads its UI from a .ui file via QUiLoader and wires up all
    29	    signals and slots to preserve existing behaviour.
    30	    """
    31	
    32	    def __init__(
    33	        self,
    34	        host: str = "127.0.0.1",
    35	        port: int = 8080,
    36	        ctx_size: int | None = None,
    37	    ) -> None:
    38	        super().__init__()
    39	        self._process = QProcess(self)
    40	        self._process.readyReadStandardOutput.connect(self._on_stdout)
    41	        self._process.readyReadStandardError.connect(self._on_stderr)
    42	        self._process.finished.connect(self._on_finished)
    43	        self._process.errorOccurred.connect(self._on_error)
    44	        self._host = host
    45	        self._port = port
    46	        self._server_url: str = f"http://{host}:{port}"
    47	        self._auto_refresh_done: bool = False
    48	        self._cache_dir: Path = self._create_cache_dir()
    49	        self._profile: QWebEngineProfile = self._create_persistent_profile()
    50	        self._ctx_size: int | None = ctx_size
    51	        self._setup_ui()
    52	        self._load_last_session()
    53	        self._connect_signals()
    54	        self._init_web_view()
    55	
    56	    # ------------------------------------------------------------------
    57	    # UI loading and initialization
    58	    # ------------------------------------------------------------------
    59	
    60	    def _create_cache_dir(self) -> Path:
    61	        """Create and return a cache directory for persistent web storage.
    62	
    63	        Returns:
    64	            Path to the cache directory (created if it does not exist).
    65	        """
    66	        cache_dir = Path(QCoreApplication.applicationDirPath()) / ".cache" / "llama-launcher"
    67	        cache_dir.mkdir(parents=True, exist_ok=True)
    68	        return cache_dir
    69	
    70	    def _create_persistent_profile(self) -> QWebEngineProfile:
    71	        """Create a QWebEngineProfile with disk-backed persistent storage.
    72	
    73	        This ensures localStorage, sessionStorage, cookies, and IndexedDB
    74	        survive across application restarts so the chat UI remembers
    75	        API keys and conversation history.
    76	
    77	        Returns:
    78	            Configured QWebEngineProfile instance.
    79	        """
    80	        profile = QWebEngineProfile("llama-launcher-profile", self)
    81	
    82	        # Persist localStorage, sessionStorage, and IndexedDB to disk
    83	        profile.setPersistentStoragePath(str(self._cache_dir))
    84	
    85	        # Persist cookies to disk (not session-only)
    86	        profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies)
    87	
    88	        # Enable disk HTTP cache for faster page loads
    89	        cache_subdir = self._cache_dir / "cache"
    90	        cache_subdir.mkdir(parents=True, exist_ok=True)
    91	        profile.setHttpCacheType(QWebEngineProfile.DiskHttpCache)
    92	        profile.setHttpCacheMaximumSize(100 * 1024 * 1024)  # 100 MB
    93	
    94	        return profile
    95	
    96	    def _init_web_view(self) -> None:
    97	        """Initialize the QWebEngineView in the Server tab.
    98	
    99	        Creates a QWebEnginePage with the persistent profile so that
   100	        localStorage, cookies, and IndexedDB are restored from disk.
   101	        """
   102	        page = QWebEnginePage(self._profile, self.server_web_view)
   103	        self.server_web_view.setPage(page)
   104	        url = f"http://{self._host}:{self._port}"
   105	        self.server_web_view.setUrl(url)
   106	
   107	    def _setup_ui(self) -> None:
   108	        """Load the main window UI from the .ui file.
   109	
   110	        All child widgets and layouts are auto-assigned as attributes
   111	        on this instance by their ``objectName`` so that the .ui file
   112	        controls which names are available.
   113	        """
   114	        ui_path = Path(__file__).resolve().parent / "ui" / "llama_launch.ui"
   115	        load_ui(ui_path, self)
   116	        self._setup_context_size_combo()
   117	        self._create_file_menu()
   118	
   119	    def _setup_context_size_combo(self) -> None:
   120	        """Populate the model context size combobox with options and tooltips.

```


**Tool Call: Read file `main.py` (lines 120-300)**
Status: Completed

```LLamaLauncher/main.py
   120	        """Populate the model context size combobox with options and tooltips.
   121	
   122	        Each item stores its numeric value (used as ``--ctx-size``) in the
   123	        user data role so the launch method can retrieve it later.
   124	        """
   125	        self.model_context_size.clear()
   126	
   127	        context_options = [
   128	            ("Auto (model default)", 0, "Recommended default; uses GGUF model context"),
   129	            ("2K", 2048, "Very small models / low memory"),
   130	            ("4K", 4096, "Basic chat, small coding tasks"),
   131	            ("8K", 8192, "General purpose"),
   132	            ("16K", 16384, "Better coding/chat history"),
   133	            ("32K", 32768, "Large files, coding assistants"),
   134	            ("64K", 65536, "Long documents, repo context"),
   135	            ("128K", 131072, "Modern long-context models"),
   136	        ]
   137	
   138	        for display_name, value, tooltip in context_options:
   139	            self.model_context_size.addItem(display_name, value)
   140	            index = self.model_context_size.count() - 1
   141	            self.model_context_size.setItemData(index, tooltip, Qt.ToolTipRole)
   142	
   143	        # Pre-select from CLI if provided, otherwise default to 16K
   144	        if self._ctx_size is not None:
   145	            target = self._ctx_size
   146	        else:
   147	            target = 16384  # 16K default
   148	
   149	        for i in range(self.model_context_size.count()):
   150	            if int(self.model_context_size.itemData(i, Qt.UserRole)) == target:
   151	                self.model_context_size.setCurrentIndex(i)
   152	                break
   153	
   154	    # ------------------------------------------------------------------
   155	    # File menu
   156	    # ------------------------------------------------------------------
   157	
   158	    def _create_file_menu(self) -> None:
   159	        """Create the File menu with Save, Save As, and Load actions."""
   160	        file_menu = QMenu("&File", self)
   161	
   162	        save_action = QAction("Save Configuration", self)
   163	        save_action.setShortcut("Ctrl+S")
   164	        save_action.setStatusTip("Save current configuration to file")
   165	        save_action.triggered.connect(self._save_config)
   166	        file_menu.addAction(save_action)
   167	
   168	        save_as_action = QAction("Save As Configuration...", self)
   169	        save_as_action.setStatusTip("Save current configuration to a new file")
   170	        save_as_action.triggered.connect(self._save_config_as)
   171	        file_menu.addAction(save_as_action)
   172	
   173	        load_action = QAction("Load Configuration...", self)
   174	        load_action.setShortcut("Ctrl+O")
   175	        load_action.setStatusTip("Load configuration from file")
   176	        load_action.triggered.connect(self._load_config)
   177	        file_menu.addAction(load_action)
   178	
   179	        self.menuBar().addMenu(file_menu)
   180	
   181	    # ------------------------------------------------------------------
   182	    # Configuration save/load
   183	    # ------------------------------------------------------------------
   184	
   185	    def _save_config(self) -> None:
   186	        """Save current configuration to the last saved file or prompt for path."""
   187	        if not hasattr(self, "_last_config_path"):
   188	            self._save_config_as()
   189	            return
   190	        self._write_config_file(self._last_config_path)
   191	
   192	    def _save_config_as(self) -> None:
   193	        """Save current configuration to a user-selected file path."""
   194	        file_path, _ = QFileDialog.getSaveFileName(
   195	            self,
   196	            "Save Configuration",
   197	            "",
   198	            "JSON Files (*.json);;All Files (*)",
   199	        )
   200	        if file_path:
   201	            self._write_config_file(file_path)
   202	            self._last_config_path = file_path
   203	
   204	    def _write_config_file(self, file_path: str) -> None:
   205	        """Write the current UI configuration to a JSON file.
   206	
   207	        Args:
   208	            file_path: Path to the JSON file to write.
   209	        """
   210	        config = self._collect_config()
   211	        try:
   212	            with open(file_path, "w") as f:
   213	                json.dump(config, f, indent=2)
   214	            self.output_display.appendPlainText(f"Configuration saved to {file_path}")
   215	        except Exception as e:
   216	            QMessageBox.critical(self, "Save Error", f"Failed to save configuration:\n{e}")
   217	
   218	    def _collect_config(self) -> dict:
   219	        """Collect all UI widget values into a configuration dictionary.
   220	
   221	        Returns:
   222	            Dictionary containing all configuration values organized by category.
   223	        """
   224	        config: dict = {"version": "1.0"}
   225	
   226	        # Files/Paths
   227	        config["files"] = {
   228	            "model_path": self.model_path_edit.property("fullPath") or "",
   229	            "mmproj_path": self.mmproj_path_edit.property("fullPath") or "",
   230	            "draft_model_path": self.draft_model_line_edit.property("fullPath") or "",
   231	            "json_schema_path": self.json_schema_line_edit.property("fullPath") or "",
   232	        }
   233	
   234	        # Server
   235	        config["server"] = {
   236	            "host": self.host_line_edit.text(),
   237	            "port": int(self.port_line_edit.text()) if self.port_line_edit.text().isdigit() else 8080,
   238	            "api_key": self.api_key_line_edit.text(),
   239	        }
   240	
   241	        # Sampling parameters
   242	        config["sampling"] = {
   243	            "temperature": {"enabled": self.enable_temperature_checkbox.isChecked(), "value": self.temperature_spinbox.value()},
   244	            "top_p": {"enabled": self.enable_top_p_checkbox.isChecked(), "value": self.top_p_spinbox.value()},
   245	            "top_k": {"enabled": self.enable_top_k_checkbox.isChecked(), "value": self.top_k_spinbox.value()},
   246	            "min_p": {"enabled": self.enable_min_p_checkbox.isChecked(), "value": self.min_p_spinbox.value()},
   247	            "typical_p": {"enabled": self.enable_typical_p_checkbox.isChecked(), "value": self.typical_p_spinbox.value()},
   248	            "repeat_penalty": {"enabled": self.enable_repeat_penalty_checkbox.isChecked(), "value": self.repeat_penalty_spinbox.value()},
   249	            "repeat_last_n": {"enabled": self.enable_repeat_last_n_checkbox.isChecked(), "value": self.repeat_last_n_spinbox.value()},
   250	            "presence_penalty": {"enabled": self.enable_presence_penalty_checkbox.isChecked(), "value": self.presence_penalty_spinbox.value()},
   251	            "frequency_penalty": {"enabled": self.enable_frequency_penalty_checkbox.isChecked(), "value": self.frequency_penalty_spinbox.value()},
   252	            "mirostat": {"enabled": self.enable_mirostat_checkbox.isChecked(), "value": self.mirostat_spinbox.value()},
   253	            "mirostat_lr": {"enabled": self.enable_mirostat_lr_checkbox.isChecked(), "value": self.mirostat_lr_spinbox.value()},
   254	            "mirostat_ent": {"enabled": self.enable_mirostat_ent_checkbox.isChecked(), "value": self.mirostat_ent_spinbox.value()},
   255	        }
   256	
   257	        # Performance parameters
   258	        config["performance"] = {
   259	            "gpu_layers": {"enabled": self.enable_gpu_layers_checkbox.isChecked(), "value": self.gpu_layers_spinbox.value()},
   260	            "threads": {"enabled": self.enable_threads_checkbox.isChecked(), "value": self.threads_spinbox.value()},
   261	            "threads_batch": {"enabled": self.enable_threads_batch_checkbox.isChecked(), "value": self.threads_batch_spinbox.value()},
   262	            "batch_size": {"enabled": self.enable_batch_size_checkbox.isChecked(), "value": self.batch_size_spinbox.value()},
   263	            "ubatch_size": {"enabled": self.enable_ubatch_size_checkbox.isChecked(), "value": self.ubatch_size_spinbox.value()},
   264	            "n_predict": {"enabled": self.enable_n_predict_checkbox.isChecked(), "value": self.n_predict_spinbox.value()},
   265	            "parallel": {"enabled": self.enable_parallel_checkbox.isChecked(), "value": self.parallel_spinbox.value()},
   266	            "flash_attn": self.flash_attn_combobox.currentText(),
   267	            "cache_type_k": {"enabled": self.enable_cache_type_k_checkbox.isChecked(), "value": self.cache_type_k_combobox.currentText()},
   268	            "cache_type_v": {"enabled": self.enable_cache_type_v_checkbox.isChecked(), "value": self.cache_type_v_combobox.currentText()},
   269	            "mmap": self.enable_mmap_checkbox.isChecked(),
   270	            "mlock": self.enable_mlock_checkbox.isChecked(),
   271	            "cont_batching": self.enable_cont_batching_checkbox.isChecked(),
   272	        }
   273	
   274	        # Advanced Generation parameters
   275	        config["advanced"] = {
   276	            "draft_model": {"enabled": self.enable_draft_model_checkbox.isChecked(), "path": self.draft_model_line_edit.property("fullPath") or ""},
   277	            "spec_draft_n_max": {"enabled": self.enable_spec_draft_n_max_checkbox.isChecked(), "value": self.spec_draft_n_max_spinbox.value()},
   278	            "seed": {"enabled": self.enable_seed_checkbox.isChecked(), "value": self.seed_spinbox.value()},
   279	            "grammar": {"enabled": self.enable_grammar_checkbox.isChecked(), "path": self.grammar_line_edit.property("fullPath") or ""},
   280	            "json_schema": {"enabled": self.enable_json_schema_checkbox.isChecked(), "path": self.json_schema_line_edit.property("fullPath") or ""},
   281	            "rope_scaling": {"enabled": self.enable_rope_scaling_checkbox.isChecked(), "value": self.rope_scaling_combobox.currentText()},
   282	            "rope_freq_base": {"enabled": self.enable_rope_freq_base_checkbox.isChecked(), "value": self.rope_freq_base_spinbox.value()},
   283	            "rope_freq_scale": {"enabled": self.enable_rope_freq_scale_checkbox.isChecked(), "value": self.rope_freq_scale_spinbox.value()},
   284	        }
   285	
   286	        # Other settings
   287	        config["context_size"] = self.model_context_size.itemData(self.model_context_size.currentIndex(), Qt.UserRole)
   288	        config["more_options"] = self.more_options_line_edit.text()
   289	        config["no_mmproj_offload"] = self.no_mmproj_offload_checkbox.isChecked()
   290	
   291	        return config
   292	
   293	    def _load_config(self) -> None:
   294	        """Load configuration from a user-selected JSON file."""
   295	        file_path, _ = QFileDialog.getOpenFileName(
   296	            self,
   297	            "Load Configuration",
   298	            "",
   299	            "JSON Files (*.json);;All Files (*)",
   300	        )

```


**Tool Call: Read file `main.py` (lines 300-500)**
Status: Completed

```LLamaLauncher/main.py
   300	        )
   301	        if not file_path:
   302	            return
   303	
   304	        try:
   305	            with open(file_path, "r") as f:
   306	                config = json.load(f)
   307	            self._apply_config(config)
   308	            self._last_config_path = file_path
   309	            self.output_display.appendPlainText(f"Configuration loaded from {file_path}")
   310	        except json.JSONDecodeError as e:
   311	            QMessageBox.critical(self, "Load Error", f"Invalid JSON format:\n{e}")
   312	        except Exception as e:
   313	            QMessageBox.critical(self, "Load Error", f"Failed to load configuration:\n{e}")
   314	
   315	    def _apply_config(self, config: dict) -> None:
   316	        """Apply configuration values from a dictionary to the UI widgets.
   317	
   318	        Args:
   319	            config: Configuration dictionary to apply.
   320	        """
   321	        # Files/Paths
   322	        if "files" in config:
   323	            files = config["files"]
   324	            self._set_path_field(self.model_path_edit, files.get("model_path", ""))
   325	            self._set_path_field(self.mmproj_path_edit, files.get("mmproj_path", ""))
   326	            self._set_path_field(self.draft_model_line_edit, files.get("draft_model_path", ""))
   327	            self._set_path_field(self.json_schema_line_edit, files.get("json_schema_path", ""))
   328	
   329	        # Server
   330	        if "server" in config:
   331	            server = config["server"]
   332	            self.host_line_edit.setText(server.get("host", "127.0.0.1"))
   333	            port = server.get("port", 8080)
   334	            self.port_line_edit.setText(str(port))
   335	            self.api_key_line_edit.setText(server.get("api_key", "12345"))
   336	
   337	        # Sampling parameters
   338	        if "sampling" in config:
   339	            sampling = config["sampling"]
   340	            self._apply_param(sampling, "temperature", self.enable_temperature_checkbox, self.temperature_spinbox)
   341	            self._apply_param(sampling, "top_p", self.enable_top_p_checkbox, self.top_p_spinbox)
   342	            self._apply_param(sampling, "top_k", self.enable_top_k_checkbox, self.top_k_spinbox)
   343	            self._apply_param(sampling, "min_p", self.enable_min_p_checkbox, self.min_p_spinbox)
   344	            self._apply_param(sampling, "typical_p", self.enable_typical_p_checkbox, self.typical_p_spinbox)
   345	            self._apply_param(sampling, "repeat_penalty", self.enable_repeat_penalty_checkbox, self.repeat_penalty_spinbox)
   346	            self._apply_param(sampling, "repeat_last_n", self.enable_repeat_last_n_checkbox, self.repeat_last_n_spinbox)
   347	            self._apply_param(sampling, "presence_penalty", self.enable_presence_penalty_checkbox, self.presence_penalty_spinbox)
   348	            self._apply_param(sampling, "frequency_penalty", self.enable_frequency_penalty_checkbox, self.frequency_penalty_spinbox)
   349	            self._apply_param(sampling, "mirostat", self.enable_mirostat_checkbox, self.mirostat_spinbox)
   350	            self._apply_param(sampling, "mirostat_lr", self.enable_mirostat_lr_checkbox, self.mirostat_lr_spinbox)
   351	            self._apply_param(sampling, "mirostat_ent", self.enable_mirostat_ent_checkbox, self.mirostat_ent_spinbox)
   352	
   353	        # Performance parameters
   354	        if "performance" in config:
   355	            perf = config["performance"]
   356	            self._apply_param(perf, "gpu_layers", self.enable_gpu_layers_checkbox, self.gpu_layers_spinbox)
   357	            self._apply_param(perf, "threads", self.enable_threads_checkbox, self.threads_spinbox)
   358	            self._apply_param(perf, "threads_batch", self.enable_threads_batch_checkbox, self.threads_batch_spinbox)
   359	            self._apply_param(perf, "batch_size", self.enable_batch_size_checkbox, self.batch_size_spinbox)
   360	            self._apply_param(perf, "ubatch_size", self.enable_ubatch_size_checkbox, self.ubatch_size_spinbox)
   361	            self._apply_param(perf, "n_predict", self.enable_n_predict_checkbox, self.n_predict_spinbox)
   362	            self._apply_param(perf, "parallel", self.enable_parallel_checkbox, self.parallel_spinbox)
   363	
   364	            if "flash_attn" in perf:
   365	                text = perf["flash_attn"]
   366	                index = self.flash_attn_combobox.findText(text)
   367	                if index >= 0:
   368	                    self.flash_attn_combobox.setCurrentIndex(index)
   369	
   370	            self._apply_combo_param(perf, "cache_type_k", self.enable_cache_type_k_checkbox, self.cache_type_k_combobox)
   371	            self._apply_combo_param(perf, "cache_type_v", self.enable_cache_type_v_checkbox, self.cache_type_v_combobox)
   372	
   373	            if "mmap" in perf:
   374	                self.enable_mmap_checkbox.setChecked(bool(perf["mmap"]))
   375	            if "mlock" in perf:
   376	                self.enable_mlock_checkbox.setChecked(bool(perf["mlock"]))
   377	            if "cont_batching" in perf:
   378	                self.enable_cont_batching_checkbox.setChecked(bool(perf["cont_batching"]))
   379	
   380	        # Advanced Generation parameters
   381	        if "advanced" in config:
   382	            adv = config["advanced"]
   383	            self._apply_param(adv, "spec_draft_n_max", self.enable_spec_draft_n_max_checkbox, self.spec_draft_n_max_spinbox)
   384	            self._apply_param(adv, "seed", self.enable_seed_checkbox, self.seed_spinbox)
   385	
   386	            # Draft model (path-based)
   387	            if "draft_model" in adv:
   388	                draft = adv["draft_model"]
   389	                self.enable_draft_model_checkbox.setChecked(draft.get("enabled", False))
   390	                self._set_path_field(self.draft_model_line_edit, draft.get("path", ""))
   391	
   392	            # Grammar (path-based)
   393	            if "grammar" in adv:
   394	                grammar = adv["grammar"]
   395	                self.enable_grammar_checkbox.setChecked(grammar.get("enabled", False))
   396	                self._set_path_field(self.grammar_line_edit, grammar.get("path", ""))
   397	
   398	            # JSON schema (path-based)
   399	            if "json_schema" in adv:
   400	                js = adv["json_schema"]
   401	                self.enable_json_schema_checkbox.setChecked(js.get("enabled", False))
   402	                self._set_path_field(self.json_schema_line_edit, js.get("path", ""))
   403	
   404	            self._apply_combo_param(adv, "rope_scaling", self.enable_rope_scaling_checkbox, self.rope_scaling_combobox)
   405	            self._apply_param(adv, "rope_freq_base", self.enable_rope_freq_base_checkbox, self.rope_freq_base_spinbox)
   406	            self._apply_param(adv, "rope_freq_scale", self.enable_rope_freq_scale_checkbox, self.rope_freq_scale_spinbox)
   407	
   408	        # Other settings
   409	        if "context_size" in config:
   410	            ctx_size = config["context_size"]
   411	            for i in range(self.model_context_size.count()):
   412	                if int(self.model_context_size.itemData(i, Qt.UserRole)) == ctx_size:
   413	                    self.model_context_size.setCurrentIndex(i)
   414	                    break
   415	
   416	        if "more_options" in config:
   417	            self.more_options_line_edit.setText(config["more_options"])
   418	
   419	        if "no_mmproj_offload" in config:
   420	            self.no_mmproj_offload_checkbox.setChecked(bool(config["no_mmproj_offload"]))
   421	
   422	    def _set_path_field(self, line_edit, path: str) -> None:
   423	        """Set a path field with full path stored and short filename displayed.
   424	
   425	        Args:
   426	            line_edit: The QLineEdit widget to update.
   427	            path: The full file path to set.
   428	        """
   429	        if path:
   430	            line_edit.setProperty("fullPath", path)
   431	            line_edit.setText(path.rsplit("/", 1)[-1])
   432	        else:
   433	            line_edit.setProperty("fullPath", "")
   434	            line_edit.setText("")
   435	
   436	    def _apply_param(self, params: dict, name: str, checkbox, spinbox) -> None:
   437	        """Apply an enabled+value parameter pair to a checkbox and spinbox.
   438	
   439	        Args:
   440	            params: Dictionary containing the parameter data.
   441	            name: Parameter name key in the dictionary.
   442	            checkbox: The QCheckBox widget.
   443	            spinbox: The QSpinBox/QDoubleSpinBox widget.
   444	        """
   445	        if name in params:
   446	            param = params[name]
   447	            if isinstance(param, dict):
   448	                checkbox.setChecked(param.get("enabled", False))
   449	                spinbox.setValue(param.get("value", spinbox.value()))
   450	            else:
   451	                # Legacy format: just a value
   452	                checkbox.setChecked(True)
   453	                spinbox.setValue(param)
   454	
   455	    def _apply_combo_param(self, params: dict, name: str, checkbox, combobox) -> None:
   456	        """Apply an enabled+value parameter pair to a checkbox and combobox.
   457	
   458	        Args:
   459	            params: Dictionary containing the parameter data.
   460	            name: Parameter name key in the dictionary.
   461	            checkbox: The QCheckBox widget.
   462	            combobox: The QComboBox widget.
   463	        """
   464	        if name in params:
   465	            param = params[name]
   466	            if isinstance(param, dict):
   467	                checkbox.setChecked(param.get("enabled", False))
   468	                text = param.get("value", "")
   469	                index = combobox.findText(text)
   470	                if index >= 0:
   471	                    combobox.setCurrentIndex(index)
   472	            else:
   473	                # Legacy format: just a value
   474	                checkbox.setChecked(True)
   475	                index = combobox.findText(str(param))
   476	                if index >= 0:
   477	                    combobox.setCurrentIndex(index)
   478	
   479	    # ------------------------------------------------------------------
   480	    # Window lifecycle
   481	    # ------------------------------------------------------------------
   482	
   483	    def closeEvent(self, event) -> None:
   484	        """Save last session settings when the window is closed.
   485	
   486	        Uses QSettings to persist basic connection settings and window
   487	        geometry so they are restored on the next launch.
   488	        """
   489	        self._save_last_session()
   490	        super().closeEvent(event)
   491	
   492	    def _save_last_session(self) -> None:
   493	        """Save last-used settings to QSettings for session restoration."""
   494	        settings = QSettings("LLamaLauncher", "LlamaLaunchApp")
   495	        settings.setValue("lastModelPath", self.model_path_edit.property("fullPath") or "")
   496	        settings.setValue("host", self.host_line_edit.text())
   497	        settings.setValue("port", self.port_line_edit.text())
   498	        settings.setValue("windowGeometry", self.saveGeometry())
   499	
   500	    def _load_last_session(self) -> None:

```


**Tool Call: Read file `main.py` (lines 500-700)**
Status: Completed

```LLamaLauncher/main.py
   500	    def _load_last_session(self) -> None:
   501	        """Restore last-used settings from QSettings.
   502	
   503	        Pre-populates the UI with the host, port, and model path
   504	        from the previous session so the user doesn't have to re-enter them.
   505	        """
   506	        settings = QSettings("LLamaLauncher", "LlamaLaunchApp")
   507	
   508	        # Restore window geometry if saved
   509	        geometry = settings.value("windowGeometry")
   510	        if geometry:
   511	            self.restoreGeometry(geometry)
   512	
   513	        # Restore server settings
   514	        host = settings.value("host", "127.0.0.1")
   515	        port = settings.value("port", "8080")
   516	        self.host_line_edit.setText(host)
   517	        self.port_line_edit.setText(port)
   518	
   519	        # Restore model path if available
   520	        last_model_path = settings.value("lastModelPath", "")
   521	        if last_model_path:
   522	            self._set_path_field(self.model_path_edit, last_model_path)
   523	
   524	    # ------------------------------------------------------------------
   525	    # Signal connections
   526	    # ------------------------------------------------------------------
   527	
   528	    def _connect_signals(self) -> None:
   529	        """Connect widget signals to their slot methods."""
   530	        self.select_model_button.clicked.connect(self._select_model)
   531	        self.select_mmproj_button.clicked.connect(self._select_mmproj)
   532	        self.select_draft_model_button.clicked.connect(self._select_draft_model)
   533	        self.select_json_schema_button.clicked.connect(self._select_json_schema)
   534	        self.model_path_edit.textChanged.connect(self._on_model_selection_changed)
   535	        self.launch_button.clicked.connect(self._toggle_launch)
   536	
   537	    # ------------------------------------------------------------------
   538	    # Slots
   539	    # ------------------------------------------------------------------
   540	
   541	    def _select_model(self) -> None:
   542	        """Open a file dialog to select a .gguf model file.
   543	
   544	        Stores the full path as a custom property on the line edit
   545	        (accessible via ``getProperty("fullPath")``) while displaying
   546	        only the short filename in the UI.
   547	        """
   548	        file_path, _ = QFileDialog.getOpenFileName(
   549	            self,
   550	            "Select GGUF Model",
   551	            "",
   552	            "GGUF Files (*.gguf)",
   553	        )
   554	        if file_path:
   555	            self._model_path = file_path
   556	            self.model_path_edit.setProperty("fullPath", file_path)
   557	            self.model_path_edit.setText(file_path.rsplit("/", 1)[-1])
   558	            self._on_model_selection_changed()
   559	
   560	    def _select_mmproj(self) -> None:
   561	        """Open a file dialog to select a .gguf mmproj file.
   562	
   563	        Stores the full path as a custom property on the line edit
   564	        (accessible via ``getProperty("fullPath")``) while displaying
   565	        only the short filename in the UI.
   566	        """
   567	        file_path, _ = QFileDialog.getOpenFileName(
   568	            self,
   569	            "Select Multi-Modal Projector",
   570	            "",
   571	            "GGUF Files (*.gguf)",
   572	        )
   573	        if file_path:
   574	            self._mmproj_path = file_path
   575	            self.mmproj_path_edit.setProperty("fullPath", file_path)
   576	            self.mmproj_path_edit.setText(file_path.rsplit("/", 1)[-1])
   577	
   578	    def _select_draft_model(self) -> None:
   579	        """Open a file dialog to select a draft model .gguf file.
   580	
   581	        Stores the full path as a custom property on the line edit
   582	        (accessible via ``getProperty("fullPath")``) while displaying
   583	        only the short filename in the UI.
   584	        """
   585	        file_path, _ = QFileDialog.getOpenFileName(
   586	            self,
   587	            "Select Draft Model",
   588	            "",
   589	            "GGUF Files (*.gguf)",
   590	        )
   591	        if file_path:
   592	            self.draft_model_line_edit.setProperty("fullPath", file_path)
   593	            self.draft_model_line_edit.setText(file_path.rsplit("/", 1)[-1])
   594	
   595	    def _select_json_schema(self) -> None:
   596	        """Open a file dialog to select a JSON schema file.
   597	
   598	        Stores the full path as a custom property on the line edit
   599	        (accessible via ``getProperty("fullPath")``) while displaying
   600	        only the short filename in the UI.
   601	        """
   602	        file_path, _ = QFileDialog.getOpenFileName(
   603	            self,
   604	            "Select JSON Schema",
   605	            "",
   606	            "JSON Files (*.json)",
   607	        )
   608	        if file_path:
   609	            self.json_schema_line_edit.setProperty("fullPath", file_path)
   610	            self.json_schema_line_edit.setText(file_path.rsplit("/", 1)[-1])
   611	
   612	    def _on_model_selection_changed(self) -> None:
   613	        """Enable launch button when a model is selected, disable otherwise."""
   614	        has_model = bool(self.model_path_edit.property("fullPath"))
   615	        is_running = self._process.state() == QProcess.Running
   616	        self.launch_button.setEnabled(has_model and not is_running)
   617	
   618	    def _toggle_launch(self) -> None:
   619	        """Launch or stop the llama-server based on current process state."""
   620	        if self._process.state() == QProcess.Running:
   621	            self._stop_model()
   622	        else:
   623	            self._launch_model()
   624	
   625	    def _stop_model(self) -> None:
   626	        """Stop the llama-server gracefully.
   627	
   628	        Sends SIGTERM (like pressing Ctrl+C) so the server can shut down
   629	        cleanly. If it does not stop within 2 seconds, falls back to
   630	        SIGKILL.
   631	        """
   632	        self._process.terminate()
   633	        self.output_display.appendPlainText("Stopping server... (sent SIGTERM)")
   634	        QTimer.singleShot(2000, self._force_kill_if_needed)
   635	
   636	    def _force_kill_if_needed(self) -> None:
   637	        """Force kill the process if graceful termination did not work."""
   638	        if self._process.state() == QProcess.Running:
   639	            self.output_display.appendPlainText("Server didn't stop gracefully. Force killing...")
   640	            self._process.kill()
   641	
   642	    def _reset_launch_button(self) -> None:
   643	        """Reset the launch button to its default state."""
   644	        self.launch_button.setText("LAUNCH")
   645	        self._on_model_selection_changed()
   646	
   647	    def _launch_model(self) -> None:
   648	        """Launch the llama-server binary with current configuration.
   649	
   650	        Builds the command-line arguments from the UI fields and starts
   651	        ``llama-server`` via QProcess.  Live stdout/stderr output is
   652	        streamed into ``output_display``.
   653	        """
   654	        model_path = self.model_path_edit.property("fullPath")
   655	        if not model_path:
   656	            self.output_display.appendPlainText("Error: no model selected.")
   657	            return
   658	
   659	        temperature = self.temperature_spinbox.value()
   660	        top_p = self.top_p_spinbox.value()
   661	        top_k = self.top_k_spinbox.value()
   662	        min_p = self.min_p_spinbox.value()
   663	        typical_p = self.typical_p_spinbox.value()
   664	        repeat_penalty = self.repeat_penalty_spinbox.value()
   665	        repeat_last_n = self.repeat_last_n_spinbox.value()
   666	        presence_penalty = self.presence_penalty_spinbox.value()
   667	        frequency_penalty = self.frequency_penalty_spinbox.value()
   668	
   669	        mirostat = self.mirostat_spinbox.value()
   670	        mirostat_lr = self.mirostat_lr_spinbox.value()
   671	        mirostat_ent = self.mirostat_ent_spinbox.value()
   672	
   673	        # Performance parameters
   674	        gpu_layers = self.gpu_layers_spinbox.value()
   675	        threads = self.threads_spinbox.value()
   676	        threads_batch = self.threads_batch_spinbox.value()
   677	        batch_size = self.batch_size_spinbox.value()
   678	        ubatch_size = self.ubatch_size_spinbox.value()
   679	        n_predict = self.n_predict_spinbox.value()
   680	        parallel = self.parallel_spinbox.value()
   681	        cache_type_k = self.cache_type_k_combobox.currentText()
   682	        cache_type_v = self.cache_type_v_combobox.currentText()
   683	
   684	        # Advanced Generation parameters
   685	        spec_draft_n_max = self.spec_draft_n_max_spinbox.value()
   686	        seed = self.seed_spinbox.value()
   687	        rope_scaling = self.rope_scaling_combobox.currentText()
   688	        rope_freq_base = self.rope_freq_base_spinbox.value()
   689	        rope_freq_scale = self.rope_freq_scale_spinbox.value()
   690	
   691	        mmproj_path = self.mmproj_path_edit.property("fullPath")
   692	        no_mmproj_offload = self.no_mmproj_offload_checkbox.isChecked()
   693	        api_key = self.api_key_line_edit.text() if self.api_key_line_edit.text() else "12345"
   694	
   695	        # Build command: llama-server --model ... (conditional sampling params) ...
   696	        cmd = [
   697	            "llama-server",
   698	            "--model",
   699	            model_path,
   700	            "--api-key",

```


**Tool Call: Read file `main.py` (lines 700-880)**
Status: Completed

```LLamaLauncher/main.py
   700	            "--api-key",
   701	            api_key,
   702	        ]
   703	
   704	        if self.enable_temperature_checkbox.isChecked():
   705	            cmd.extend(["--temp", str(temperature)])
   706	        if self.enable_top_p_checkbox.isChecked():
   707	            cmd.extend(["--top-p", str(top_p)])
   708	        if self.enable_top_k_checkbox.isChecked():
   709	            cmd.extend(["--top-k", str(top_k)])
   710	        if self.enable_min_p_checkbox.isChecked():
   711	            cmd.extend(["--min-p", str(min_p)])
   712	        if self.enable_typical_p_checkbox.isChecked():
   713	            cmd.extend(["--typical-p", str(typical_p)])
   714	        if self.enable_repeat_penalty_checkbox.isChecked():
   715	            cmd.extend(["--repeat-penalty", str(repeat_penalty)])
   716	        if self.enable_repeat_last_n_checkbox.isChecked():
   717	            cmd.extend(["--repeat-last-n", str(repeat_last_n)])
   718	        if self.enable_presence_penalty_checkbox.isChecked():
   719	            cmd.extend(["--presence-penalty", str(presence_penalty)])
   720	        if self.enable_frequency_penalty_checkbox.isChecked():
   721	            cmd.extend(["--frequency-penalty", str(frequency_penalty)])
   722	        if self.enable_mirostat_checkbox.isChecked():
   723	            cmd.extend(["--mirostat", str(mirostat)])
   724	        if self.enable_mirostat_lr_checkbox.isChecked():
   725	            cmd.extend(["--mirostat-lr", str(mirostat_lr)])
   726	        if self.enable_mirostat_ent_checkbox.isChecked():
   727	            cmd.extend(["--mirostat-ent", str(mirostat_ent)])
   728	
   729	        # Performance parameters
   730	        if self.enable_gpu_layers_checkbox.isChecked():
   731	            cmd.extend(["--n-gpu-layers", str(gpu_layers)])
   732	        if self.enable_threads_checkbox.isChecked():
   733	            cmd.extend(["--threads", str(threads)])
   734	        if self.enable_threads_batch_checkbox.isChecked():
   735	            cmd.extend(["--threads-batch", str(threads_batch)])
   736	        if self.enable_batch_size_checkbox.isChecked():
   737	            cmd.extend(["--batch-size", str(batch_size)])
   738	        if self.enable_ubatch_size_checkbox.isChecked():
   739	            cmd.extend(["--ubatch-size", str(ubatch_size)])
   740	        if self.enable_n_predict_checkbox.isChecked():
   741	            cmd.extend(["--n-predict", str(n_predict)])
   742	        # Flash Attention: always pass the selected value (default auto)
   743	        flash_attn = self.flash_attn_combobox.currentText()
   744	        cmd.extend(["--flash-attn", flash_attn])
   745	        if self.enable_cache_type_k_checkbox.isChecked():
   746	            cmd.extend(["--cache-type-k", cache_type_k])
   747	        if self.enable_cache_type_v_checkbox.isChecked():
   748	            cmd.extend(["--cache-type-v", cache_type_v])
   749	        if self.enable_mmap_checkbox.isChecked():
   750	            cmd.append("--mmap")
   751	        if self.enable_mlock_checkbox.isChecked():
   752	            cmd.append("--mlock")
   753	        if self.enable_cont_batching_checkbox.isChecked():
   754	            cmd.append("--cont-batching")
   755	        if self.enable_parallel_checkbox.isChecked():
   756	            cmd.extend(["--parallel", str(parallel)])
   757	
   758	        # Advanced Generation parameters
   759	        draft_model_path = self.draft_model_line_edit.property("fullPath")
   760	        if self.enable_draft_model_checkbox.isChecked() and draft_model_path:
   761	            cmd.extend(["--draft-model", draft_model_path])
   762	        if self.enable_spec_draft_n_max_checkbox.isChecked():
   763	            cmd.extend(["--spec-draft-n-max", str(spec_draft_n_max)])
   764	        if self.enable_seed_checkbox.isChecked():
   765	            cmd.extend(["--seed", str(seed)])
   766	        grammar_text = self.grammar_line_edit.text().strip()
   767	        if self.enable_grammar_checkbox.isChecked() and grammar_text:
   768	            cmd.extend(["--grammar", grammar_text])
   769	        json_schema_path = self.json_schema_line_edit.property("fullPath")
   770	        if self.enable_json_schema_checkbox.isChecked() and json_schema_path:
   771	            cmd.extend(["--json-schema", json_schema_path])
   772	        if self.enable_rope_scaling_checkbox.isChecked():
   773	            cmd.extend(["--rope-scaling", rope_scaling])
   774	        if self.enable_rope_freq_base_checkbox.isChecked():
   775	            cmd.extend(["--rope-freq-base", str(rope_freq_base)])
   776	        if self.enable_rope_freq_scale_checkbox.isChecked():
   777	            cmd.extend(["--rope-freq-scale", str(rope_freq_scale)])
   778	
   779	        host = self.host_line_edit.text() or self._host
   780	        port_str = self.port_line_edit.text() or str(self._port)
   781	        try:
   782	            port = int(port_str)
   783	        except ValueError:
   784	            port = self._port
   785	
   786	        if mmproj_path:
   787	            cmd.extend(["--mmproj", mmproj_path])
   788	            if no_mmproj_offload:
   789	                cmd.append("--no-mmproj-offload")
   790	
   791	        # Extra user-supplied flags from the more options line edit
   792	        extra = self.more_options_line_edit.text().strip()
   793	        if extra:
   794	            cmd.extend(extra.split())
   795	
   796	        # Context size: only pass --ctx-size when a specific value is selected
   797	        ctx_size = self.model_context_size.itemData(
   798	            self.model_context_size.currentIndex(),
   799	            Qt.UserRole,
   800	        )
   801	        if ctx_size is not None and int(ctx_size) > 0:
   802	            cmd.extend(["--ctx-size", str(ctx_size)])
   803	
   804	        cmd.extend(["--host", host, "--port", str(port)])
   805	
   806	        self._server_url = f"http://{host}:{port}"
   807	        self._auto_refresh_done = False
   808	
   809	        self.output_display.clear()
   810	        self.output_display.appendPlainText(f"Launching: {' '.join(cmd)}\n---\n")
   811	
   812	        # Use two-argument form: program + arguments list (args must NOT include the program)
   813	        self._process.start(cmd[0], cmd[1:])
   814	        self.launch_button.setText("STOP")
   815	
   816	        # Update web view to point to the server
   817	        server_url = f"http://{host}:{port}"
   818	        self.server_web_view.setUrl(server_url)
   819	
   820	    # ------------------------------------------------------------------
   821	    # QProcess output slots
   822	    # ------------------------------------------------------------------
   823	
   824	    def _on_stdout(self) -> None:
   825	        """Append stdout from the child process to the output display.
   826	
   827	        Also watches for the server URL pattern (http://HOST:PORT) in the
   828	        output and auto-refreshes the web view once the server is ready.
   829	        """
   830	        data = self._process.readAllStandardOutput().data().decode("utf-8", errors="replace")
   831	        if data:
   832	            self.output_display.appendPlainText(data)
   833	            self._check_and_refresh()
   834	
   835	    def _on_stderr(self) -> None:
   836	        """Append stderr from the child process to the output display.
   837	
   838	        Also watches for the server URL pattern (http://HOST:PORT) in the
   839	        output and auto-refreshes the web view once the server is ready.
   840	        """
   841	        data = self._process.readAllStandardError().data().decode("utf-8", errors="replace")
   842	        if data:
   843	            self.output_display.appendPlainText(data)
   844	            self._check_and_refresh()
   845	
   846	    def _check_and_refresh(self) -> None:
   847	        """Check output for server URL and refresh web view once ready.
   848	
   849	        Scans the full text of the output display for an HTTP URL pattern.
   850	        When found (and not already refreshed), schedules a one-shot timer
   851	        to reload the web view so the Qt event loop is not blocked.
   852	        """
   853	        if self._auto_refresh_done:
   854	            return
   855	
   856	        text = self.output_display.toPlainText()
   857	        match = re.search(r"http://[\w.-]+:\d+", text)
   858	        if match:
   859	            self._auto_refresh_done = True
   860	            QTimer.singleShot(0, self._refresh_web_view)
   861	
   862	    def _refresh_web_view(self) -> None:
   863	        """Reload the server web view to fetch the freshly started server."""
   864	        url = QUrl(self._server_url)
   865	        self.server_web_view.setUrl(url)
   866	        self.output_display.appendPlainText(f"\n[Server ready — refreshed web view at {self._server_url}]")
   867	
   868	    def _on_error(self, error: QProcess.ProcessError) -> None:
   869	        """Called when the process encounters an error (e.g. not found)."""
   870	        msg = f"Error launching process: {error}"
   871	        self.output_display.appendPlainText(msg)
   872	        self._reset_launch_button()
   873	
   874	    def _on_finished(self, code: int, status: QProcess.ExitStatus) -> None:
   875	        """Called when the child process exits."""
   876	        if status == QProcess.ExitStatus.NormalExit:
   877	            self.output_display.appendPlainText(f"\n--- Process exited with code {code} ---")
   878	        else:
   879	            self.output_display.appendPlainText(f"\n--- Process terminated abnormally (code {code}) ---")
   880	        self._reset_launch_button()

```


## Assistant

<thinking>
Now I have a good understanding of the codebase. Let me also check the .ui file and any other relevant files to complete my understanding.

</thinking>

Now let me read the UI file to understand what widgets exist, and check the README for more context.



**Tool Call: Read file `ui/llama_launch.ui`**
Status: Completed

```
SUCCESS: File outline retrieved. This file is too large to read all at once, so the outline below shows the file's structure with line numbers.

IMPORTANT: Do NOT retry this call without line numbers - you will get the same outline.
Instead, use the line numbers below to read specific sections by calling this tool again with start_line and end_line parameters.

# First 1KB of /Volumes/teaching/Code/LLamaLauncher/ui/llama_launch.ui (file too large to show full content, and no outline available)

<?xml version="1.0" encoding="UTF-8" ?>
<ui version="4.0">
 <class>LlamaLaunchApp</class>
 <widget class="QWidget" name="LlamaLaunchApp">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>919</width>
    <height>755</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Llama Launch</string>
  </property>
  <layout class="QVBoxLayout" name="verticalLayout" stretch="0">
   <item>
    <widget class="QTabWidget" name="tab_widget">
     <property name="currentIndex">
      <number>0</number>
     </property>
     <widget class="QWidget" name="model_tab">
      <attribute name="title">
       <string>Model</string>
      </attribute>
      <layout class="QVBoxLayout" name="model_tab_layout" stretch="1,5,1,1,1">
       <item>
        <widget class="QGroupBox" name="model_group">
         <property name="title">
          <string>MODEL</string>
         </property>
         <layout class="QVBoxLayout" name="model_group_layout">
          <item>
           <layout class

NEXT STEPS: To read a specific symbol's implementation, call read_file with the same path plus start_line and end_line from the outline above.
For example, to read a function shown as [L100-150], use start_line: 100 and end_line: 150.
```


**Tool Call: Read file `README.md`**
Status: Completed

```LLamaLauncher/README.md

```


## Assistant

<thinking>
The user wants me to create a Testing.md file with a test plan for the project. I've now read the entire main.py (880 lines) and ui_loader.py (69 lines), and understand the codebase well.

Let me analyze what needs testing:

1. **ui_loader.py** - This is a separate, testable module with `load_ui()` function. It's a pure utility function that could be tested independently.

2. **main.py** - Contains the `LlamaLaunchApp` class which is a large PySide6 QMainWindow (~850 lines). It has:
   - Configuration save/load (JSON)
   - Process management (QProcess for llama-server)
   - UI setup and signal connections
   - Session management (QSettings)
   - Web view initialization

For a GUI application like this, testing strategy should prioritize:
1. **Pure functions/logic** that can be tested without Qt event loop
2. **Configuration handling** (collect/apply config)
3. **Process command building** (the logic of constructing the llama-server command)
4. **ui_loader.py** as a standalone module

The main challenges:
- Heavy coupling to Qt widgets
- QProcess, QSettings, QWebEngineView are hard to test
- File dialogs can't be easily tested
- The entire app is one monolithic class

Key approach for this project:
1. Start with the smallest, most testable module (ui_loader.py)
2. Test configuration logic (save/load/collect/apply) - these are pure data transformations
3. Test process command building logic
4. Eventually refactor to extract business logic from Qt widgets for better testability

Let me create a comprehensive Testing.md plan.

Looking at the project structure, I see it's a PySide6 GUI application with no existing tests. The main source files are `main.py` (the `LlamaLaunchApp` QMainWindow) and `ui_loader.py` (a utility function).

For a GUI-heavy Python project like this, the testing strategy should follow these principles:
1. **Start with pure logic** - configuration handling, data transformation
2. **Test ui_loader.py first** - it's a small, self-contained module
3. **Extract testable logic** from the monolithic QMainWindow where possible
4. **Use pytest-qt** for Qt-specific testing patterns
5. **Mock external dependencies** (QProcess, file dialogs, network)

Let me create a comprehensive, prioritized Testing.md plan.

I'm planning a Testing.md file organized by priority, starting with pure logic tests and progressing to more complex GUI integration tests, with the goal of reaching >90% coverage.

</thinking>

The README is empty and I have a thorough understanding of the codebase now. Let me create a comprehensive testing plan.

Based on my analysis of the project:

**Codebase Summary:**
- **main.py** (880 lines) - `LlamaLaunchApp` QMainWindow with config handling, process management, UI wiring, session persistence
- **ui_loader.py** (69 lines) - `load_ui()` utility for loading Qt `.ui` files
- **ui/llama_launch.ui** - The Qt Designer file defining all widgets
- No existing tests; pytest is in dev dependencies

**Key testing challenges:**
- Heavy Qt coupling (QProcess, QSettings, QWebEngineView, file dialogs)
- Monolithic `LlamaLaunchApp` class (~850 lines of methods)
- Many methods are thin wrappers around Qt widgets
- Pure logic is embedded inside UI event handlers

Here's the testing strategy:

1. **ui_loader.py** first (smallest, most testable module)
2. **Configuration handling** (pure data transformation - collect/apply/save/load)
3. **Process command building** (the logic of constructing `llama-server` arguments)
4. **UI integration tests** using pytest-qt for signal/slot behavior
5. **Extract business logic** from QMainWindow to testable classes where feasible

Now let me create the Testing.md file:



**Tool Call: `test-driven-development` Skill**
Status: Completed

```json
{
  "rendered": "<skill_content name=\"test-driven-development\">\n<source>project-local</source>\n<worktree>LLamaLauncher</worktree>\n<directory>/Volumes/teaching/Code/LLamaLauncher/.agents/skills/test-driven-development</directory>\nRelative paths in this skill resolve against <directory>.\n\n# Test-Driven Development (TDD)\n\n## Overview\n\nWrite the test first. Watch it fail. Write minimal code to pass.\n\n**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.\n\n**Violating the letter of the rules is violating the spirit of the rules.**\n\n## When to Use\n\n**Always:**\n- New features\n- Bug fixes\n- Refactoring\n- Behavior changes\n\n**Exceptions (ask your human partner):**\n- Throwaway prototypes\n- Generated code\n- Configuration files\n\nThinking \"skip TDD just this once\"? Stop. That's rationalization.\n\n## The Iron Law\n\n```\nNO PRODUCTION CODE WITHOUT A FAILING TEST FIRST\n```\n\nWrite code before the test? Delete it. Start over.\n\n**No exceptions:**\n- Don't keep it as \"reference\"\n- Don't \"adapt\" it while writing tests\n- Don't look at it\n- Delete means delete\n\nImplement fresh from tests. Period.\n\n## Red-Green-Refactor\n\n```dot\ndigraph tdd_cycle {\n    rankdir=LR;\n    red [label=\"RED\\nWrite failing test\", shape=box, style=filled, fillcolor=\"#ffcccc\"];\n    verify_red [label=\"Verify fails\\ncorrectly\", shape=diamond];\n    green [label=\"GREEN\\nMinimal code\", shape=box, style=filled, fillcolor=\"#ccffcc\"];\n    verify_green [label=\"Verify passes\\nAll green\", shape=diamond];\n    refactor [label=\"REFACTOR\\nClean up\", shape=box, style=filled, fillcolor=\"#ccccff\"];\n    next [label=\"Next\", shape=ellipse];\n\n    red -> verify_red;\n    verify_red -> green [label=\"yes\"];\n    verify_red -> red [label=\"wrong\\nfailure\"];\n    green -> verify_green;\n    verify_green -> refactor [label=\"yes\"];\n    verify_green -> green [label=\"no\"];\n    refactor -> verify_green [label=\"stay\\ngreen\"];\n    verify_green -> next;\n    next -> red;\n}\n```\n\n### RED - Write Failing Test\n\nWrite one minimal test showing what should happen.\n\n<Good>\n```typescript\ntest('retries failed operations 3 times', async () => {\n  let attempts = 0;\n  const operation = () => {\n    attempts++;\n    if (attempts < 3) throw new Error('fail');\n    return 'success';\n  };\n\n  const result = await retryOperation(operation);\n\n  expect(result).toBe('success');\n  expect(attempts).toBe(3);\n});\n```\nClear name, tests real behavior, one thing\n</Good>\n\n<Bad>\n```typescript\ntest('retry works', async () => {\n  const mock = jest.fn()\n    .mockRejectedValueOnce(new Error())\n    .mockRejectedValueOnce(new Error())\n    .mockResolvedValueOnce('success');\n  await retryOperation(mock);\n  expect(mock).toHaveBeenCalledTimes(3);\n});\n```\nVague name, tests mock not code\n</Bad>\n\n**Requirements:**\n- One behavior\n- Clear name\n- Real code (no mocks unless unavoidable)\n\n### Verify RED - Watch It Fail\n\n**MANDATORY. Never skip.**\n\n```bash\nnpm test path/to/test.test.ts\n```\n\nConfirm:\n- Test fails (not errors)\n- Failure message is expected\n- Fails because feature missing (not typos)\n\n**Test passes?** You're testing existing behavior. Fix test.\n\n**Test errors?** Fix error, re-run until it fails correctly.\n\n### GREEN - Minimal Code\n\nWrite simplest code to pass the test.\n\n<Good>\n```typescript\nasync function retryOperation<T>(fn: () => Promise<T>): Promise<T> {\n  for (let i = 0; i < 3; i++) {\n    try {\n      return await fn();\n    } catch (e) {\n      if (i === 2) throw e;\n    }\n  }\n  throw new Error('unreachable');\n}\n```\nJust enough to pass\n</Good>\n\n<Bad>\n```typescript\nasync function retryOperation<T>(\n  fn: () => Promise<T>,\n  options?: {\n    maxRetries?: number;\n    backoff?: 'linear' | 'exponential';\n    onRetry?: (attempt: number) => void;\n  }\n): Promise<T> {\n  // YAGNI\n}\n```\nOver-engineered\n</Bad>\n\nDon't add features, refactor other code, or \"improve\" beyond the test.\n\n### Verify GREEN - Watch It Pass\n\n**MANDATORY.**\n\n```bash\nnpm test path/to/test.test.ts\n```\n\nConfirm:\n- Test passes\n- Other tests still pass\n- Output pristine (no errors, warnings)\n\n**Test fails?** Fix code, not test.\n\n**Other tests fail?** Fix now.\n\n### REFACTOR - Clean Up\n\nAfter green only:\n- Remove duplication\n- Improve names\n- Extract helpers\n\nKeep tests green. Don't add behavior.\n\n### Repeat\n\nNext failing test for next feature.\n\n## Good Tests\n\n| Quality | Good | Bad |\n|---------|------|-----|\n| **Minimal** | One thing. \"and\" in name? Split it. | `test('validates email and domain and whitespace')` |\n| **Clear** | Name describes behavior | `test('test1')` |\n| **Shows intent** | Demonstrates desired API | Obscures what code should do |\n\n## Why Order Matters\n\n**\"I'll write tests after to verify it works\"**\n\nTests written after code pass immediately. Passing immediately proves nothing:\n- Might test wrong thing\n- Might test implementation, not behavior\n- Might miss edge cases you forgot\n- You never saw it catch the bug\n\nTest-first forces you to see the test fail, proving it actually tests something.\n\n**\"I already manually tested all the edge cases\"**\n\nManual testing is ad-hoc. You think you tested everything but:\n- No record of what you tested\n- Can't re-run when code changes\n- Easy to forget cases under pressure\n- \"It worked when I tried it\" ≠ comprehensive\n\nAutomated tests are systematic. They run the same way every time.\n\n**\"Deleting X hours of work is wasteful\"**\n\nSunk cost fallacy. The time is already gone. Your choice now:\n- Delete and rewrite with TDD (X more hours, high confidence)\n- Keep it and add tests after (30 min, low confidence, likely bugs)\n\nThe \"waste\" is keeping code you can't trust. Working code without real tests is technical debt.\n\n**\"TDD is dogmatic, being pragmatic means adapting\"**\n\nTDD IS pragmatic:\n- Finds bugs before commit (faster than debugging after)\n- Prevents regressions (tests catch breaks immediately)\n- Documents behavior (tests show how to use code)\n- Enables refactoring (change freely, tests catch breaks)\n\n\"Pragmatic\" shortcuts = debugging in production = slower.\n\n**\"Tests after achieve the same goals - it's spirit not ritual\"**\n\nNo. Tests-after answer \"What does this do?\" Tests-first answer \"What should this do?\"\n\nTests-after are biased by your implementation. You test what you built, not what's required. You verify remembered edge cases, not discovered ones.\n\nTests-first force edge case discovery before implementing. Tests-after verify you remembered everything (you didn't).\n\n30 minutes of tests after ≠ TDD. You get coverage, lose proof tests work.\n\n## Common Rationalizations\n\n| Excuse | Reality |\n|--------|---------|\n| \"Too simple to test\" | Simple code breaks. Test takes 30 seconds. |\n| \"I'll test after\" | Tests passing immediately prove nothing. |\n| \"Tests after achieve same goals\" | Tests-after = \"what does this do?\" Tests-first = \"what should this do?\" |\n| \"Already manually tested\" | Ad-hoc ≠ systematic. No record, can't re-run. |\n| \"Deleting X hours is wasteful\" | Sunk cost fallacy. Keeping unverified code is technical debt. |\n| \"Keep as reference, write tests first\" | You'll adapt it. That's testing after. Delete means delete. |\n| \"Need to explore first\" | Fine. Throw away exploration, start with TDD. |\n| \"Test hard = design unclear\" | Listen to test. Hard to test = hard to use. |\n| \"TDD will slow me down\" | TDD faster than debugging. Pragmatic = test-first. |\n| \"Manual test faster\" | Manual doesn't prove edge cases. You'll re-test every change. |\n| \"Existing code has no tests\" | You're improving it. Add tests for existing code. |\n\n## Red Flags - STOP and Start Over\n\n- Code before test\n- Test after implementation\n- Test passes immediately\n- Can't explain why test failed\n- Tests added \"later\"\n- Rationalizing \"just this once\"\n- \"I already manually tested it\"\n- \"Tests after achieve the same purpose\"\n- \"It's about spirit not ritual\"\n- \"Keep as reference\" or \"adapt existing code\"\n- \"Already spent X hours, deleting is wasteful\"\n- \"TDD is dogmatic, I'm being pragmatic\"\n- \"This is different because...\"\n\n**All of these mean: Delete code. Start over with TDD.**\n\n## Example: Bug Fix\n\n**Bug:** Empty email accepted\n\n**RED**\n```typescript\ntest('rejects empty email', async () => {\n  const result = await submitForm({ email: '' });\n  expect(result.error).toBe('Email required');\n});\n```\n\n**Verify RED**\n```bash\n$ npm test\nFAIL: expected 'Email required', got undefined\n```\n\n**GREEN**\n```typescript\nfunction submitForm(data: FormData) {\n  if (!data.email?.trim()) {\n    return { error: 'Email required' };\n  }\n  // ...\n}\n```\n\n**Verify GREEN**\n```bash\n$ npm test\nPASS\n```\n\n**REFACTOR**\nExtract validation for multiple fields if needed.\n\n## Verification Checklist\n\nBefore marking work complete:\n\n- [ ] Every new function/method has a test\n- [ ] Watched each test fail before implementing\n- [ ] Each test failed for expected reason (feature missing, not typo)\n- [ ] Wrote minimal code to pass each test\n- [ ] All tests pass\n- [ ] Output pristine (no errors, warnings)\n- [ ] Tests use real code (mocks only if unavoidable)\n- [ ] Edge cases and errors covered\n\nCan't check all boxes? You skipped TDD. Start over.\n\n## When Stuck\n\n| Problem | Solution |\n|---------|----------|\n| Don't know how to test | Write wished-for API. Write assertion first. Ask your human partner. |\n| Test too complicated | Design too complicated. Simplify interface. |\n| Must mock everything | Code too coupled. Use dependency injection. |\n| Test setup huge | Extract helpers. Still complex? Simplify design. |\n\n## Debugging Integration\n\nBug found? Write failing test reproducing it. Follow TDD cycle. Test proves fix and prevents regression.\n\nNever fix bugs without a test.\n\n## Testing Anti-Patterns\n\nWhen adding mocks or test utilities, read @testing-anti-patterns.md to avoid common pitfalls:\n- Testing mock behavior instead of real behavior\n- Adding test-only methods to production classes\n- Mocking without understanding dependencies\n\n## Final Rule\n\n```\nProduction code → test exists and failed first\nOtherwise → not TDD\n```\n\nNo exceptions without your human partner's permission.\n</skill_content>\n"
}
```

## Assistant

<thinking>
The user wants me to create a Testing.md file with a test plan for the project. I've already analyzed the codebase thoroughly. Let me now check if there are any existing tests directories or pytest configuration to understand the testing setup better, then create a comprehensive testing plan.

Key observations from the codebase:
1. main.py has 880 lines - a large QMainWindow class with many methods
2. ui_loader.py has 69 lines - a small utility function
3. No existing tests directory
4. pytest is in dev dependencies but no pytest-qt
5. The app uses PySide6 for GUI, QProcess for spawning llama-server
6. Configuration is saved/loaded as JSON
7. Session persistence uses QSettings

For a GUI-heavy application like this, the testing strategy should be:
1. Start with pure logic that can be tested without Qt (config handling)
2. Test ui_loader.py as it's a small standalone module


3. Move to pytest-qt for Qt-specific tests once we have the foundation
4. Consider refactoring to extract business logic from QMainWindow for better testability

I should check if there's an existing tests directory and look at the pytest configuration to understand how tests are structured in this project.

</thinking>

Let me check for any existing test setup or pytest configuration before creating the plan.



**Tool Call: No matches**
Status: Completed

```json
{
  "offset": 0,
  "current_matches_page": [],
  "all_matches_len": 0
}
```

**Tool Call: Search files for regex `pytest`**
Status: Completed

Found 1 matches:

## Matches in LLamaLauncher/pyproject.toml

### dependency-groups › dev › L13-15
```
dev = [
    "pytest>=9.1.0",
]
```


**Tool Call: Read file `SmallModel.json`**
Status: Completed

```LLamaLauncher/SmallModel.json
     1	{
     2	  "version": "1.0",
     3	  "files": {
     4	    "model_path": "/Volumes/teaching/AI_Models/Llama-3.2-1B-Instruct-Q4_K_M.gguf",
     5	    "mmproj_path": "",
     6	    "draft_model_path": "",
     7	    "json_schema_path": ""
     8	  },
     9	  "server": {
    10	    "host": "127.0.0.1",
    11	    "port": 8080,
    12	    "api_key": "12345"
    13	  },
    14	  "sampling": {
    15	    "temperature": {
    16	      "enabled": true,
    17	      "value": 0.6
    18	    },
    19	    "top_p": {
    20	      "enabled": true,
    21	      "value": 0.9
    22	    },
    23	    "top_k": {
    24	      "enabled": true,
    25	      "value": 20
    26	    },
    27	    "min_p": {
    28	      "enabled": false,
    29	      "value": 0.05
    30	    },
    31	    "typical_p": {
    32	      "enabled": false,
    33	      "value": 1.0
    34	    },
    35	    "repeat_penalty": {
    36	      "enabled": true,
    37	      "value": 1.1
    38	    },
    39	    "repeat_last_n": {
    40	      "enabled": true,
    41	      "value": 64
    42	    },
    43	    "presence_penalty": {
    44	      "enabled": false,
    45	      "value": 0.0
    46	    },
    47	    "frequency_penalty": {
    48	      "enabled": false,
    49	      "value": 0.0
    50	    },
    51	    "mirostat": {
    52	      "enabled": false,
    53	      "value": 1
    54	    },
    55	    "mirostat_lr": {
    56	      "enabled": false,
    57	      "value": 0.1
    58	    },
    59	    "mirostat_ent": {
    60	      "enabled": false,
    61	      "value": 5.0
    62	    }
    63	  },
    64	  "performance": {
    65	    "gpu_layers": {
    66	      "enabled": true,
    67	      "value": 99
    68	    },
    69	    "threads": {
    70	      "enabled": true,
    71	      "value": 4
    72	    },
    73	    "threads_batch": {
    74	      "enabled": false,
    75	      "value": 0
    76	    },
    77	    "batch_size": {
    78	      "enabled": false,
    79	      "value": 512
    80	    },
    81	    "ubatch_size": {
    82	      "enabled": false,
    83	      "value": 512
    84	    },
    85	    "n_predict": {
    86	      "enabled": false,
    87	      "value": 2048
    88	    },
    89	    "parallel": {
    90	      "enabled": false,
    91	      "value": 4
    92	    },
    93	    "flash_attn": "auto",
    94	    "cache_type_k": {
    95	      "enabled": false,
    96	      "value": "f16"
    97	    },
    98	    "cache_type_v": {
    99	      "enabled": false,
   100	      "value": "f16"
   101	    },
   102	    "mmap": true,
   103	    "mlock": false,
   104	    "cont_batching": false
   105	  },
   106	  "advanced": {
   107	    "draft_model": {
   108	      "enabled": false,
   109	      "path": ""
   110	    },
   111	    "spec_draft_n_max": {
   112	      "enabled": false,
   113	      "value": 5
   114	    },
   115	    "seed": {
   116	      "enabled": false,
   117	      "value": 42
   118	    },
   119	    "grammar": {
   120	      "enabled": false,
   121	      "path": ""
   122	    },
   123	    "json_schema": {
   124	      "enabled": false,
   125	      "path": ""
   126	    },
   127	    "rope_scaling": {
   128	      "enabled": false,
   129	      "value": "none"
   130	    },
   131	    "rope_freq_base": {
   132	      "enabled": false,
   133	      "value": 1.0
   134	    },
   135	    "rope_freq_scale": {
   136	      "enabled": false,
   137	      "value": 1.0
   138	    }
   139	  },
   140	  "context_size": 8192,
   141	  "more_options": "",
   142	  "no_mmproj_offload": false
   143	}
```


## Assistant

<thinking>
The user wants me to create a Testing.md file that outlines the order tests should be added to the project as a todo list, with the goal of achieving >90% test coverage. I've analyzed the codebase thoroughly and now have enough context to create a comprehensive testing plan.

Let me review what I know:

1. **Project structure:**
   - `main.py` (880 lines) - Main application class `LlamaLaunchApp` (QMainWindow)
   - `ui_loader.py` (69 lines) - Utility function `load_ui()` for loading Qt .ui files
   - `ui/llama_launch.ui` - Qt Designer UI file
   - `SmallModel.json` - Example configuration file
   - `AgentChats/` - Contains chat markdown files (not code to test)

2. **Dependencies:**
   - PySide6 (Qt for Python)
   - requests
   - pytest (dev dependency, already installed via uv)

3. **Code analysis:**
   - The main application is a large QMainWindow with many methods
   - Configuration handling (save/load JSON)
   - Process management (QProcess for llama-server)
   - Signal/slot connections
   - Session persistence (QSettings)
   - Web view initialization (QWebEngineView)

4. **Testing challenges:**
   - Heavy Qt coupling
   - GUI testing requires QApplication instance
   - QProcess, QSettings are hard to mock
   - File dialogs can't be easily tested
   - Large monolithic class (~850 lines of methods)

Now I need to create a comprehensive testing plan that prioritizes what's actually testable and provides a clear roadmap for achieving coverage. I'll structure it by phases, starting with the most straightforward utilities and working up to more complex Qt integration tests.

</thinking>

Let me check the project's existing pytest configuration and any additional setup files before creating the plan.



**Tool Call: Search files for regex `\[pytest\]|testpaths|python_classes|python_files`**
Status: Completed

No matches found

**Tool Call: List the `LLamaLauncher/tests` directory's contents**
Status: Failed

Path not found: LLamaLauncher/tests

**Tool Call: Read file `test.json`**
Status: Completed

```LLamaLauncher/test.json
     1	{
     2	  "version": "1.0",
     3	  "files": {
     4	    "model_path": "",
     5	    "mmproj_path": "",
     6	    "draft_model_path": "",
     7	    "json_schema_path": ""
     8	  },
     9	  "server": {
    10	    "host": "127.0.0.1",
    11	    "port": 8080,
    12	    "api_key": "12345"
    13	  },
    14	  "sampling": {
    15	    "temperature": {
    16	      "enabled": true,
    17	      "value": 0.3
    18	    },
    19	    "top_p": {
    20	      "enabled": true,
    21	      "value": 0.9
    22	    },
    23	    "top_k": {
    24	      "enabled": true,
    25	      "value": 40
    26	    },
    27	    "min_p": {
    28	      "enabled": false,
    29	      "value": 0.05
    30	    },
    31	    "typical_p": {
    32	      "enabled": false,
    33	      "value": 1.0
    34	    },
    35	    "repeat_penalty": {
    36	      "enabled": true,
    37	      "value": 1.1
    38	    },
    39	    "repeat_last_n": {
    40	      "enabled": true,
    41	      "value": 64
    42	    },
    43	    "presence_penalty": {
    44	      "enabled": false,
    45	      "value": 0.0
    46	    },
    47	    "frequency_penalty": {
    48	      "enabled": false,
    49	      "value": 0.0
    50	    },
    51	    "mirostat": {
    52	      "enabled": false,
    53	      "value": 1
    54	    },
    55	    "mirostat_lr": {
    56	      "enabled": false,
    57	      "value": 0.1
    58	    },
    59	    "mirostat_ent": {
    60	      "enabled": false,
    61	      "value": 5.0
    62	    }
    63	  },
    64	  "performance": {
    65	    "gpu_layers": {
    66	      "enabled": false,
    67	      "value": 99
    68	    },
    69	    "threads": {
    70	      "enabled": false,
    71	      "value": 0
    72	    },
    73	    "threads_batch": {
    74	      "enabled": false,
    75	      "value": 0
    76	    },
    77	    "batch_size": {
    78	      "enabled": false,
    79	      "value": 512
    80	    },
    81	    "ubatch_size": {
    82	      "enabled": false,
    83	      "value": 512
    84	    },
    85	    "n_predict": {
    86	      "enabled": false,
    87	      "value": 2048
    88	    },
    89	    "parallel": {
    90	      "enabled": false,
    91	      "value": 4
    92	    },
    93	    "flash_attn": "auto",
    94	    "cache_type_k": {
    95	      "enabled": false,
    96	      "value": "f16"
    97	    },
    98	    "cache_type_v": {
    99	      "enabled": false,
   100	      "value": "f16"
   101	    },
   102	    "mmap": true,
   103	    "mlock": false,
   104	    "cont_batching": false
   105	  },
   106	  "advanced": {
   107	    "draft_model": {
   108	      "enabled": false,
   109	      "path": ""
   110	    },
   111	    "spec_draft_n_max": {
   112	      "enabled": false,
   113	      "value": 5
   114	    },
   115	    "seed": {
   116	      "enabled": false,
   117	      "value": 42
   118	    },
   119	    "grammar": {
   120	      "enabled": false,
   121	      "path": ""
   122	    },
   123	    "json_schema": {
   124	      "enabled": false,
   125	      "path": ""
   126	    },
   127	    "rope_scaling": {
   128	      "enabled": false,
   129	      "value": "none"
   130	    },
   131	    "rope_freq_base": {
   132	      "enabled": false,
   133	      "value": 1.0
   134	    },
   135	    "rope_freq_scale": {
   136	      "enabled": false,
   137	      "value": 1.0
   138	    }
   139	  },
   140	  "context_size": 16384,
   141	  "more_options": "",
   142	  "no_mmproj_offload": false
   143	}
```


## Assistant

<thinking>
The user wants me to create a Testing.md file that outlines the order tests should be added to the project, in the form of a todo list, with the goal of achieving >90% test coverage. I need to analyze the codebase thoroughly and create a comprehensive testing plan.

From my analysis:

**Project Structure:**
- `main.py` - LlamaLaunchApp class (880 lines) - QMainWindow with ~40 methods
- `ui_loader.py` - load_ui function (69 lines) - utility for loading Qt UI files
- `ui/llama_launch.ui` - Qt Designer UI file
- No existing tests directory

**Key Dependencies:**
- PySide6 (Qt for Python) - GUI framework
- requests - HTTP library
- pytest (dev dependency) - Testing framework

**Testing Challenges:**
1. Heavy Qt coupling throughout main.py
2. QProcess, QSettings, QWebEngineView are hard to test
3. File dialogs can't be easily tested
4. Large monolithic class with many methods
5. No pytest-qt for Qt testing patterns
6. Most logic is embedded in Qt event handlers

**Testing Strategy:**
1. Start with pure logic that can be tested without Qt
2. Test ui_loader.py first (small, standalone module)
3. Add pytest-qt for Qt-specific tests
4. Extract business logic from QMainWindow where feasible
5. Mock external dependencies (QProcess, file dialogs, network)

Now I need to create a comprehensive Testing.md plan that:
- Is organized as a todo list
- Prioritizes testable components
- Provides clear phases for achieving coverage
- Accounts for the GUI-heavy nature of the project
- Includes specific test targets for each module/method

Let me create this file now.

</thinking>

Based on my analysis of the codebase, I can see:

**Project Structure:**
- `main.py` (880 lines) - `LlamaLaunchApp` QMainWindow with ~40 methods
- `ui_loader.py` (69 lines) - `load_ui()` utility for loading Qt UI files  
- No existing tests directory or pytest configuration
- pytest is in dev dependencies but no pytest-qt

**Testing Challenges:**
- Heavy Qt coupling throughout main.py
- QProcess, QSettings, QWebEngineView are hard to test directly
- File dialogs can't be easily tested
- Large monolithic class with most logic embedded in Qt event handlers
- Pure logic is scattered across many small methods

**Testing Strategy:**
1. Start with pure logic that can be tested without Qt
2. Test ui_loader.py first (small, standalone module)
3. Add pytest-qt for Qt-specific tests
4. Extract business logic from QMainWindow where feasible
5. Mock external dependencies (QProcess, file dialogs, network)

Now let me create the comprehensive Testing.md plan:



**Tool Call: `test-driven-development` Skill**
Status: Completed

```json
{
  "rendered": "<skill_content name=\"test-driven-development\">\n<source>project-local</source>\n<worktree>LLamaLauncher</worktree>\n<directory>/Volumes/teaching/Code/LLamaLauncher/.agents/skills/test-driven-development</directory>\nRelative paths in this skill resolve against <directory>.\n\n# Test-Driven Development (TDD)\n\n## Overview\n\nWrite the test first. Watch it fail. Write minimal code to pass.\n\n**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.\n\n**Violating the letter of the rules is violating the spirit of the rules.**\n\n## When to Use\n\n**Always:**\n- New features\n- Bug fixes\n- Refactoring\n- Behavior changes\n\n**Exceptions (ask your human partner):**\n- Throwaway prototypes\n- Generated code\n- Configuration files\n\nThinking \"skip TDD just this once\"? Stop. That's rationalization.\n\n## The Iron Law\n\n```\nNO PRODUCTION CODE WITHOUT A FAILING TEST FIRST\n```\n\nWrite code before the test? Delete it. Start over.\n\n**No exceptions:**\n- Don't keep it as \"reference\"\n- Don't \"adapt\" it while writing tests\n- Don't look at it\n- Delete means delete\n\nImplement fresh from tests. Period.\n\n## Red-Green-Refactor\n\n```dot\ndigraph tdd_cycle {\n    rankdir=LR;\n    red [label=\"RED\\nWrite failing test\", shape=box, style=filled, fillcolor=\"#ffcccc\"];\n    verify_red [label=\"Verify fails\\ncorrectly\", shape=diamond];\n    green [label=\"GREEN\\nMinimal code\", shape=box, style=filled, fillcolor=\"#ccffcc\"];\n    verify_green [label=\"Verify passes\\nAll green\", shape=diamond];\n    refactor [label=\"REFACTOR\\nClean up\", shape=box, style=filled, fillcolor=\"#ccccff\"];\n    next [label=\"Next\", shape=ellipse];\n\n    red -> verify_red;\n    verify_red -> green [label=\"yes\"];\n    verify_red -> red [label=\"wrong\\nfailure\"];\n    green -> verify_green;\n    verify_green -> refactor [label=\"yes\"];\n    verify_green -> green [label=\"no\"];\n    refactor -> verify_green [label=\"stay\\ngreen\"];\n    verify_green -> next;\n    next -> red;\n}\n```\n\n### RED - Write Failing Test\n\nWrite one minimal test showing what should happen.\n\n<Good>\n```typescript\ntest('retries failed operations 3 times', async () => {\n  let attempts = 0;\n  const operation = () => {\n    attempts++;\n    if (attempts < 3) throw new Error('fail');\n    return 'success';\n  };\n\n  const result = await retryOperation(operation);\n\n  expect(result).toBe('success');\n  expect(attempts).toBe(3);\n});\n```\nClear name, tests real behavior, one thing\n</Good>\n\n<Bad>\n```typescript\ntest('retry works', async () => {\n  const mock = jest.fn()\n    .mockRejectedValueOnce(new Error())\n    .mockRejectedValueOnce(new Error())\n    .mockResolvedValueOnce('success');\n  await retryOperation(mock);\n  expect(mock).toHaveBeenCalledTimes(3);\n});\n```\nVague name, tests mock not code\n</Bad>\n\n**Requirements:**\n- One behavior\n- Clear name\n- Real code (no mocks unless unavoidable)\n\n### Verify RED - Watch It Fail\n\n**MANDATORY. Never skip.**\n\n```bash\nnpm test path/to/test.test.ts\n```\n\nConfirm:\n- Test fails (not errors)\n- Failure message is expected\n- Fails because feature missing (not typos)\n\n**Test passes?** You're testing existing behavior. Fix test.\n\n**Test errors?** Fix error, re-run until it fails correctly.\n\n### GREEN - Minimal Code\n\nWrite simplest code to pass the test.\n\n<Good>\n```typescript\nasync function retryOperation<T>(fn: () => Promise<T>): Promise<T> {\n  for (let i = 0; i < 3; i++) {\n    try {\n      return await fn();\n    } catch (e) {\n      if (i === 2) throw e;\n    }\n  }\n  throw new Error('unreachable');\n}\n```\nJust enough to pass\n</Good>\n\n<Bad>\n```typescript\nasync function retryOperation<T>(\n  fn: () => Promise<T>,\n  options?: {\n    maxRetries?: number;\n    backoff?: 'linear' | 'exponential';\n    onRetry?: (attempt: number) => void;\n  }\n): Promise<T> {\n  // YAGNI\n}\n```\nOver-engineered\n</Bad>\n\nDon't add features, refactor other code, or \"improve\" beyond the test.\n\n### Verify GREEN - Watch It Pass\n\n**MANDATORY.**\n\n```bash\nnpm test path/to/test.test.ts\n```\n\nConfirm:\n- Test passes\n- Other tests still pass\n- Output pristine (no errors, warnings)\n\n**Test fails?** Fix code, not test.\n\n**Other tests fail?** Fix now.\n\n### REFACTOR - Clean Up\n\nAfter green only:\n- Remove duplication\n- Improve names\n- Extract helpers\n\nKeep tests green. Don't add behavior.\n\n### Repeat\n\nNext failing test for next feature.\n\n## Good Tests\n\n| Quality | Good | Bad |\n|---------|------|-----|\n| **Minimal** | One thing. \"and\" in name? Split it. | `test('validates email and domain and whitespace')` |\n| **Clear** | Name describes behavior | `test('test1')` |\n| **Shows intent** | Demonstrates desired API | Obscures what code should do |\n\n## Why Order Matters\n\n**\"I'll write tests after to verify it works\"**\n\nTests written after code pass immediately. Passing immediately proves nothing:\n- Might test wrong thing\n- Might test implementation, not behavior\n- Might miss edge cases you forgot\n- You never saw it catch the bug\n\nTest-first forces you to see the test fail, proving it actually tests something.\n\n**\"I already manually tested all the edge cases\"**\n\nManual testing is ad-hoc. You think you tested everything but:\n- No record of what you tested\n- Can't re-run when code changes\n- Easy to forget cases under pressure\n- \"It worked when I tried it\" ≠ comprehensive\n\nAutomated tests are systematic. They run the same way every time.\n\n**\"Deleting X hours of work is wasteful\"**\n\nSunk cost fallacy. The time is already gone. Your choice now:\n- Delete and rewrite with TDD (X more hours, high confidence)\n- Keep it and add tests after (30 min, low confidence, likely bugs)\n\nThe \"waste\" is keeping code you can't trust. Working code without real tests is technical debt.\n\n**\"TDD is dogmatic, being pragmatic means adapting\"**\n\nTDD IS pragmatic:\n- Finds bugs before commit (faster than debugging after)\n- Prevents regressions (tests catch breaks immediately)\n- Documents behavior (tests show how to use code)\n- Enables refactoring (change freely, tests catch breaks)\n\n\"Pragmatic\" shortcuts = debugging in production = slower.\n\n**\"Tests after achieve the same goals - it's spirit not ritual\"**\n\nNo. Tests-after answer \"What does this do?\" Tests-first answer \"What should this do?\"\n\nTests-after are biased by your implementation. You test what you built, not what's required. You verify remembered edge cases, not discovered ones.\n\nTests-first force edge case discovery before implementing. Tests-after verify you remembered everything (you didn't).\n\n30 minutes of tests after ≠ TDD. You get coverage, lose proof tests work.\n\n## Common Rationalizations\n\n| Excuse | Reality |\n|--------|---------|\n| \"Too simple to test\" | Simple code breaks. Test takes 30 seconds. |\n| \"I'll test after\" | Tests passing immediately prove nothing. |\n| \"Tests after achieve same goals\" | Tests-after = \"what does this do?\" Tests-first = \"what should this do?\" |\n| \"Already manually tested\" | Ad-hoc ≠ systematic. No record, can't re-run. |\n| \"Deleting X hours is wasteful\" | Sunk cost fallacy. Keeping unverified code is technical debt. |\n| \"Keep as reference, write tests first\" | You'll adapt it. That's testing after. Delete means delete. |\n| \"Need to explore first\" | Fine. Throw away exploration, start with TDD. |\n| \"Test hard = design unclear\" | Listen to test. Hard to test = hard to use. |\n| \"TDD will slow me down\" | TDD faster than debugging. Pragmatic = test-first. |\n| \"Manual test faster\" | Manual doesn't prove edge cases. You'll re-test every change. |\n| \"Existing code has no tests\" | You're improving it. Add tests for existing code. |\n\n## Red Flags - STOP and Start Over\n\n- Code before test\n- Test after implementation\n- Test passes immediately\n- Can't explain why test failed\n- Tests added \"later\"\n- Rationalizing \"just this once\"\n- \"I already manually tested it\"\n- \"Tests after achieve the same purpose\"\n- \"It's about spirit not ritual\"\n- \"Keep as reference\" or \"adapt existing code\"\n- \"Already spent X hours, deleting is wasteful\"\n- \"TDD is dogmatic, I'm being pragmatic\"\n- \"This is different because...\"\n\n**All of these mean: Delete code. Start over with TDD.**\n\n## Example: Bug Fix\n\n**Bug:** Empty email accepted\n\n**RED**\n```typescript\ntest('rejects empty email', async () => {\n  const result = await submitForm({ email: '' });\n  expect(result.error).toBe('Email required');\n});\n```\n\n**Verify RED**\n```bash\n$ npm test\nFAIL: expected 'Email required', got undefined\n```\n\n**GREEN**\n```typescript\nfunction submitForm(data: FormData) {\n  if (!data.email?.trim()) {\n    return { error: 'Email required' };\n  }\n  // ...\n}\n```\n\n**Verify GREEN**\n```bash\n$ npm test\nPASS\n```\n\n**REFACTOR**\nExtract validation for multiple fields if needed.\n\n## Verification Checklist\n\nBefore marking work complete:\n\n- [ ] Every new function/method has a test\n- [ ] Watched each test fail before implementing\n- [ ] Each test failed for expected reason (feature missing, not typo)\n- [ ] Wrote minimal code to pass each test\n- [ ] All tests pass\n- [ ] Output pristine (no errors, warnings)\n- [ ] Tests use real code (mocks only if unavoidable)\n- [ ] Edge cases and errors covered\n\nCan't check all boxes? You skipped TDD. Start over.\n\n## When Stuck\n\n| Problem | Solution |\n|---------|----------|\n| Don't know how to test | Write wished-for API. Write assertion first. Ask your human partner. |\n| Test too complicated | Design too complicated. Simplify interface. |\n| Must mock everything | Code too coupled. Use dependency injection. |\n| Test setup huge | Extract helpers. Still complex? Simplify design. |\n\n## Debugging Integration\n\nBug found? Write failing test reproducing it. Follow TDD cycle. Test proves fix and prevents regression.\n\nNever fix bugs without a test.\n\n## Testing Anti-Patterns\n\nWhen adding mocks or test utilities, read @testing-anti-patterns.md to avoid common pitfalls:\n- Testing mock behavior instead of real behavior\n- Adding test-only methods to production classes\n- Mocking without understanding dependencies\n\n## Final Rule\n\n```\nProduction code → test exists and failed first\nOtherwise → not TDD\n```\n\nNo exceptions without your human partner's permission.\n</skill_content>\n"
}
```

## Assistant

<thinking>
The user wants me to create a Testing.md file that outlines the order tests should be added to the project, in the form of a todo list, with the goal of achieving >90% test coverage. I've analyzed the codebase thoroughly and now have enough context to create a comprehensive testing plan.

Let me analyze what I know:

**Project Structure:**
- `main.py` (880 lines) - Main application class `LlamaLaunchApp` (QMainWindow)
- `ui_loader.py` (69 lines) - Utility function `load_ui()` for loading Qt .ui files
- `ui/llama_launch.ui` - Qt Designer UI file
- No existing tests directory
- pytest is in dev dependencies but no pytest-qt

**Key Dependencies:**
- PySide6 (Qt for Python)
- requests
- pytest (dev dependency)

**Code Analysis of main.py:**
- `LlamaLaunchApp` class with many methods
- Configuration save/load (JSON)
- Process management (QProcess for llama-server)
- UI setup and signal connections
- Session management (QSettings)
- Web view initialization (QWebEngineView)

**Testing Challenges:**
- Heavy Qt coupling
- QProcess, QSettings, QWebEngineView are hard to test
- File dialogs can't be easily tested
- Large monolithic class
- Pure logic is embedded inside UI event handlers

**Testing Strategy:**
1. Start with pure logic that can be tested without Qt (config handling)
2. Test ui_loader.py first (small, standalone module)
3. Test process command building logic
4. Use pytest-qt for Qt-specific testing patterns
5. Eventually refactor to extract business logic from Qt widgets

Now I need to create a comprehensive Testing.md plan that:
- Is organized as a todo list
- Prioritizes testable components
- Provides clear phases for achieving coverage
- Accounts for the GUI-heavy nature of the project
- Includes specific test targets for each module/method

Let me structure this properly with phases and clear priorities.

</thinking>

Based on my analysis of the codebase, here's the Testing.md plan:



**Tool Call: `test-driven-development` Skill**
Status: Completed

```json
{
  "rendered": "<skill_content name=\"test-driven-development\">\n<source>project-local</source>\n<worktree>LLamaLauncher</worktree>\n<directory>/Volumes/teaching/Code/LLamaLauncher/.agents/skills/test-driven-development</directory>\nRelative paths in this skill resolve against <directory>.\n\n# Test-Driven Development (TDD)\n\n## Overview\n\nWrite the test first. Watch it fail. Write minimal code to pass.\n\n**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.\n\n**Violating the letter of the rules is violating the spirit of the rules.**\n\n## When to Use\n\n**Always:**\n- New features\n- Bug fixes\n- Refactoring\n- Behavior changes\n\n**Exceptions (ask your human partner):**\n- Throwaway prototypes\n- Generated code\n- Configuration files\n\nThinking \"skip TDD just this once\"? Stop. That's rationalization.\n\n## The Iron Law\n\n```\nNO PRODUCTION CODE WITHOUT A FAILING TEST FIRST\n```\n\nWrite code before the test? Delete it. Start over.\n\n**No exceptions:**\n- Don't keep it as \"reference\"\n- Don't \"adapt\" it while writing tests\n- Don't look at it\n- Delete means delete\n\nImplement fresh from tests. Period.\n\n## Red-Green-Refactor\n\n```dot\ndigraph tdd_cycle {\n    rankdir=LR;\n    red [label=\"RED\\nWrite failing test\", shape=box, style=filled, fillcolor=\"#ffcccc\"];\n    verify_red [label=\"Verify fails\\ncorrectly\", shape=diamond];\n    green [label=\"GREEN\\nMinimal code\", shape=box, style=filled, fillcolor=\"#ccffcc\"];\n    verify_green [label=\"Verify passes\\nAll green\", shape=diamond];\n    refactor [label=\"REFACTOR\\nClean up\", shape=box, style=filled, fillcolor=\"#ccccff\"];\n    next [label=\"Next\", shape=ellipse];\n\n    red -> verify_red;\n    verify_red -> green [label=\"yes\"];\n    verify_red -> red [label=\"wrong\\nfailure\"];\n    green -> verify_green;\n    verify_green -> refactor [label=\"yes\"];\n    verify_green -> green [label=\"no\"];\n    refactor -> verify_green [label=\"stay\\ngreen\"];\n    verify_green -> next;\n    next -> red;\n}\n```\n\n### RED - Write Failing Test\n\nWrite one minimal test showing what should happen.\n\n<Good>\n```typescript\ntest('retries failed operations 3 times', async () => {\n  let attempts = 0;\n  const operation = () => {\n    attempts++;\n    if (attempts < 3) throw new Error('fail');\n    return 'success';\n  };\n\n  const result = await retryOperation(operation);\n\n  expect(result).toBe('success');\n  expect(attempts).toBe(3);\n});\n```\nClear name, tests real behavior, one thing\n</Good>\n\n<Bad>\n```typescript\ntest('retry works', async () => {\n  const mock = jest.fn()\n    .mockRejectedValueOnce(new Error())\n    .mockRejectedValueOnce(new Error())\n    .mockResolvedValueOnce('success');\n  await retryOperation(mock);\n  expect(mock).toHaveBeenCalledTimes(3);\n});\n```\nVague name, tests mock not code\n</Bad>\n\n**Requirements:**\n- One behavior\n- Clear name\n- Real code (no mocks unless unavoidable)\n\n### Verify RED - Watch It Fail\n\n**MANDATORY. Never skip.**\n\n```bash\nnpm test path/to/test.test.ts\n```\n\nConfirm:\n- Test fails (not errors)\n- Failure message is expected\n- Fails because feature missing (not typos)\n\n**Test passes?** You're testing existing behavior. Fix test.\n\n**Test errors?** Fix error, re-run until it fails correctly.\n\n### GREEN - Minimal Code\n\nWrite simplest code to pass the test.\n\n<Good>\n```typescript\nasync function retryOperation<T>(fn: () => Promise<T>): Promise<T> {\n  for (let i = 0; i < 3; i++) {\n    try {\n      return await fn();\n    } catch (e) {\n      if (i === 2) throw e;\n    }\n  }\n  throw new Error('unreachable');\n}\n```\nJust enough to pass\n</Good>\n\n<Bad>\n```typescript\nasync function retryOperation<T>(\n  fn: () => Promise<T>,\n  options?: {\n    maxRetries?: number;\n    backoff?: 'linear' | 'exponential';\n    onRetry?: (attempt: number) => void;\n  }\n): Promise<T> {\n  // YAGNI\n}\n```\nOver-engineered\n</Bad>\n\nDon't add features, refactor other code, or \"improve\" beyond the test.\n\n### Verify GREEN - Watch It Pass\n\n**MANDATORY.**\n\n```bash\nnpm test path/to/test.test.ts\n```\n\nConfirm:\n- Test passes\n- Other tests still pass\n- Output pristine (no errors, warnings)\n\n**Test fails?** Fix code, not test.\n\n**Other tests fail?** Fix now.\n\n### REFACTOR - Clean Up\n\nAfter green only:\n- Remove duplication\n- Improve names\n- Extract helpers\n\nKeep tests green. Don't add behavior.\n\n### Repeat\n\nNext failing test for next feature.\n\n## Good Tests\n\n| Quality | Good | Bad |\n|---------|------|-----|\n| **Minimal** | One thing. \"and\" in name? Split it. | `test('validates email and domain and whitespace')` |\n| **Clear** | Name describes behavior | `test('test1')` |\n| **Shows intent** | Demonstrates desired API | Obscures what code should do |\n\n## Why Order Matters\n\n**\"I'll write tests after to verify it works\"**\n\nTests written after code pass immediately. Passing immediately proves nothing:\n- Might test wrong thing\n- Might test implementation, not behavior\n- Might miss edge cases you forgot\n- You never saw it catch the bug\n\nTest-first forces you to see the test fail, proving it actually tests something.\n\n**\"I already manually tested all the edge cases\"**\n\nManual testing is ad-hoc. You think you tested everything but:\n- No record of what you tested\n- Can't re-run when code changes\n- Easy to forget cases under pressure\n- \"It worked when I tried it\" ≠ comprehensive\n\nAutomated tests are systematic. They run the same way every time.\n\n**\"Deleting X hours of work is wasteful\"**\n\nSunk cost fallacy. The time is already gone. Your choice now:\n- Delete and rewrite with TDD (X more hours, high confidence)\n- Keep it and add tests after (30 min, low confidence, likely bugs)\n\nThe \"waste\" is keeping code you can't trust. Working code without real tests is technical debt.\n\n**\"TDD is dogmatic, being pragmatic means adapting\"**\n\nTDD IS pragmatic:\n- Finds bugs before commit (faster than debugging after)\n- Prevents regressions (tests catch breaks immediately)\n- Documents behavior (tests show how to use code)\n- Enables refactoring (change freely, tests catch breaks)\n\n\"Pragmatic\" shortcuts = debugging in production = slower.\n\n**\"Tests after achieve the same goals - it's spirit not ritual\"**\n\nNo. Tests-after answer \"What does this do?\" Tests-first answer \"What should this do?\"\n\nTests-after are biased by your implementation. You test what you built, not what's required. You verify remembered edge cases, not discovered ones.\n\nTests-first force edge case discovery before implementing. Tests-after verify you remembered everything (you didn't).\n\n30 minutes of tests after ≠ TDD. You get coverage, lose proof tests work.\n\n## Common Rationalizations\n\n| Excuse | Reality |\n|--------|---------|\n| \"Too simple to test\" | Simple code breaks. Test takes 30 seconds. |\n| \"I'll test after\" | Tests passing immediately prove nothing. |\n| \"Tests after achieve same goals\" | Tests-after = \"what does this do?\" Tests-first = \"what should this do?\" |\n| \"Already manually tested\" | Ad-hoc ≠ systematic. No record, can't re-run. |\n| \"Deleting X hours is wasteful\" | Sunk cost fallacy. Keeping unverified code is technical debt. |\n| \"Keep as reference, write tests first\" | You'll adapt it. That's testing after. Delete means delete. |\n| \"Need to explore first\" | Fine. Throw away exploration, start with TDD. |\n| \"Test hard = design unclear\" | Listen to test. Hard to test = hard to use. |\n| \"TDD will slow me down\" | TDD faster than debugging. Pragmatic = test-first. |\n| \"Manual test faster\" | Manual doesn't prove edge cases. You'll re-test every change. |\n| \"Existing code has no tests\" | You're improving it. Add tests for existing code. |\n\n## Red Flags - STOP and Start Over\n\n- Code before test\n- Test after implementation\n- Test passes immediately\n- Can't explain why test failed\n- Tests added \"later\"\n- Rationalizing \"just this once\"\n- \"I already manually tested it\"\n- \"Tests after achieve the same purpose\"\n- \"It's about spirit not ritual\"\n- \"Keep as reference\" or \"adapt existing code\"\n- \"Already spent X hours, deleting is wasteful\"\n- \"TDD is dogmatic, I'm being pragmatic\"\n- \"This is different because...\"\n\n**All of these mean: Delete code. Start over with TDD.**\n\n## Example: Bug Fix\n\n**Bug:** Empty email accepted\n\n**RED**\n```typescript\ntest('rejects empty email', async () => {\n  const result = await submitForm({ email: '' });\n  expect(result.error).toBe('Email required');\n});\n```\n\n**Verify RED**\n```bash\n$ npm test\nFAIL: expected 'Email required', got undefined\n```\n\n**GREEN**\n```typescript\nfunction submitForm(data: FormData) {\n  if (!data.email?.trim()) {\n    return { error: 'Email required' };\n  }\n  // ...\n}\n```\n\n**Verify GREEN**\n```bash\n$ npm test\nPASS\n```\n\n**REFACTOR**\nExtract validation for multiple fields if needed.\n\n## Verification Checklist\n\nBefore marking work complete:\n\n- [ ] Every new function/method has a test\n- [ ] Watched each test fail before implementing\n- [ ] Each test failed for expected reason (feature missing, not typo)\n- [ ] Wrote minimal code to pass each test\n- [ ] All tests pass\n- [ ] Output pristine (no errors, warnings)\n- [ ] Tests use real code (mocks only if unavoidable)\n- [ ] Edge cases and errors covered\n\nCan't check all boxes? You skipped TDD. Start over.\n\n## When Stuck\n\n| Problem | Solution |\n|---------|----------|\n| Don't know how to test | Write wished-for API. Write assertion first. Ask your human partner. |\n| Test too complicated | Design too complicated. Simplify interface. |\n| Must mock everything | Code too coupled. Use dependency injection. |\n| Test setup huge | Extract helpers. Still complex? Simplify design. |\n\n## Debugging Integration\n\nBug found? Write failing test reproducing it. Follow TDD cycle. Test proves fix and prevents regression.\n\nNever fix bugs without a test.\n\n## Testing Anti-Patterns\n\nWhen adding mocks or test utilities, read @testing-anti-patterns.md to avoid common pitfalls:\n- Testing mock behavior instead of real behavior\n- Adding test-only methods to production classes\n- Mocking without understanding dependencies\n\n## Final Rule\n\n```\nProduction code → test exists and failed first\nOtherwise → not TDD\n```\n\nNo exceptions without your human partner's permission.\n</skill_content>\n"
}
```

## Assistant

<thinking>
The user wants me to create a Testing.md file that outlines the order tests should be added to the project, in the form of a todo list, with the goal of achieving >90% test coverage. I've already analyzed the codebase thoroughly and have enough context to create a comprehensive testing plan.

Let me review what I know:

**Project Structure:**
- `main.py` (880 lines) - Main application class `LlamaLaunchApp` (QMainWindow)
- `ui_loader.py` (69 lines) - Utility function `load_ui()` for loading Qt .ui files
- `ui/llama_launch.ui` - Qt Designer UI file
- No existing tests directory
- pytest is in dev dependencies but no pytest-qt

**Key Dependencies:**
- PySide6 (Qt for Python)
- requests
- pytest (dev dependency)

**Code Analysis of main.py:**
- `LlamaLaunchApp` class with many methods
- Configuration save/load (JSON)
- Process management (QProcess for llama-server)
- UI setup and signal connections
- Session management (QSettings)
- Web view initialization (QWebEngineView)

**Testing Challenges:**
- Heavy Qt coupling
- QProcess, QSettings, QWebEngineView are hard to test
- File dialogs can't be easily tested
- Large monolithic class
- Pure logic is embedded inside UI event handlers

**Testing Strategy:**
1. Start with pure logic that can be tested without Qt (config handling)
2. Test ui_loader.py first (small, standalone module)
3. Test process command building logic
4. Use pytest-qt for Qt-specific testing patterns
5. Eventually refactor to extract business logic from Qt widgets

Now I need to create a comprehensive Testing.md plan that:
- Is organized as a todo list
- Prioritizes testable components
- Provides clear phases for achieving coverage
- Accounts for the GUI-heavy nature of the project
- Includes specific test targets for each module/method

Let me structure this properly with phases and clear priorities.

</thinking>

The user wants me to create a Testing.md file that outlines the order tests should be added to the project, in the form of a todo list, with the goal of achieving >90% test coverage. I've already analyzed the codebase thoroughly and have enough context to create a comprehensive testing plan.

Let me review what I know:

**Project Structure:**
- `main.py` (880 lines) - Main application class `LlamaLaunchApp` (QMainWindow)
- `ui_loader.py` (69 lines) - Utility function `load_ui()` for loading Qt .ui files
- `ui/llama_launch.ui` - Qt Designer UI file
- No existing tests directory
- pytest is in dev dependencies but no pytest-qt

**Key Dependencies:**
- PySide6 (Qt for Python)
- requests
- pytest (dev dependency)

**Code Analysis of main.py:**
- `LlamaLaunchApp` class with many methods
- Configuration save/load (JSON)
- Process management (QProcess for llama-server)
- UI setup and signal connections
- Session management (QSettings)
- Web view initialization (QWebEngineView)

**Testing Challenges:**
- Heavy Qt coupling
- QProcess, QSettings, QWebEngineView are hard to test
- File dialogs can't be easily tested
- Large monolithic class
- Pure logic is embedded inside UI event handlers

**Testing Strategy:**
1. Start with pure logic that can be tested without Qt (config handling)
2. Test ui_loader.py first (small, standalone module)
3. Test process command building logic
4. Use pytest-qt for Qt-specific testing patterns
5. Eventually refactor to extract business logic from Qt widgets

Now I need to create a comprehensive Testing.md plan that:
- Is organized as a todo list
- Prioritizes testable components
- Provides clear phases for achieving coverage
- Accounts for the GUI-heavy nature of the project
- Includes specific test targets for each module/method

Let me structure this properly with phases and clear priorities.

## User

Write a detailed plan to Testing.md

## Assistant

<thinking>
The user wants me to create a Testing.md file with a detailed test plan for the project. I've already analyzed the codebase thoroughly, so let me create a comprehensive testing plan based on what I know:

1. **main.py** - 880 lines, LlamaLaunchApp QMainWindow with ~40 methods
2. **ui_loader.py** - 69 lines, load_ui() utility function
3. No existing tests directory
4. pytest is in dev dependencies but no pytest-qt

Key testing priorities:
1. Start with pure logic (configuration handling)
2. Test ui_loader.py first (small, standalone)
3. Test process command building logic
4. Use pytest-qt for Qt-specific tests
5. Extract business logic from QMainWindow where feasible

Let me create a comprehensive Testing.md file.

</thinking>

Based on my analysis of the codebase (main.py at 880 lines with ~40 methods, ui_loader.py at 69 lines, no existing tests), here's a comprehensive testing plan:



**Tool Call: Testing.md**
Status: Completed

Diff: Testing.md
```
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

- [ ] Create `tests/` directory with `__init__.py`
- [ ] Create `tests/conftest.py` with shared fixtures:
  - `qapp`: QApplication singleton (pytest-qt)
  - `temp_dir`: Temporary directory for test files
  - `mock_qprocess`: Patched QProcess for process tests
- [ ] Configure `pyproject.toml` for pytest and coverage:
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
- [ ] Create `tests/files/` directory for test fixtures (sample JSON configs, etc.)

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

```


## Assistant

<thinking>
The user wants me to create a Testing.md file with a detailed test plan. I've already analyzed the codebase thoroughly and have all the information I need. Let me review what I know:

**Project Structure:**
- `main.py` (880 lines) - Main application class `LlamaLaunchApp` (QMainWindow)
- `ui_loader.py` (69 lines) - Utility function `load_ui()` for loading Qt .ui files
- No existing tests directory
- pytest is in dev dependencies but no pytest-qt

**Key Dependencies:**
- PySide6 (Qt for Python)
- requests
- pytest (dev dependency)

**Code Analysis of main.py:**
- `LlamaLaunchApp` class with many methods
- Configuration save/load (JSON)
- Process management (QProcess for llama-server)
- UI setup and signal connections
- Session management (QSettings)
- Web view initialization (QWebEngineView)

**Testing Challenges:**
- Heavy Qt coupling
- QProcess, QSettings, QWebEngineView are hard to test
- File dialogs can't be easily tested
- Large monolithic class
- Pure logic is embedded inside UI event handlers

**Testing Strategy:**
1. Start with pure logic that can be tested without Qt (config handling)
2. Test ui_loader.py first (small, standalone module)
3. Test process command building logic
4. Use pytest-qt for Qt-specific testing patterns
5. Eventually refactor to extract business logic from Qt widgets

Now I need to create a comprehensive Testing.md plan that:
- Is organized as a todo list
- Prioritizes testable components
- Provides clear phases for achieving coverage
- Accounts for the GUI-heavy nature of the project
- Includes specific test targets for each module/method

Let me structure this properly with phases and clear priorities. I've already analyzed the codebase thoroughly, so I can create a comprehensive testing plan based on what I know. Let me review my notes:

**Project Structure:**
- `main.py` (880 lines) - Main application class `LlamaLaunchApp` (QMainWindow)
- `ui_loader.py` (69 lines) - Utility function `load_ui()` for loading Qt .ui files
- No existing tests directory
- pytest is in dev dependencies but no pytest-qt

**Key Dependencies:**
- PySide6 (Qt for Python)
- requests
- pytest (dev dependency)

**Code Analysis of main.py:**
- `LlamaLaunchApp` class with many methods
- Configuration save/load (JSON)
- Process management (QProcess for llama-server)
- UI setup and signal connections
- Session management (QSettings)
- Web view initialization (QWebEngineView)

**Testing Challenges:**
- Heavy Qt coupling
- QProcess, QSettings, QWebEngineView are hard to test
- File dialogs can't be easily tested
- Large monolithic class
- Pure logic is embedded inside UI event handlers

**Testing Strategy:**
1. Start with pure logic that can be tested without Qt (config handling)
2. Test ui_loader.py first (small, standalone module)
3. Test process command building logic
4. Use pytest-qt for Qt-specific testing patterns
5. Eventually refactor to extract business logic from Qt widgets

Now I need to create a comprehensive Testing.md plan that:
- Is organized as a todo list
- Prioritizes testable components
- Provides clear phases for achieving coverage
- Accounts for the GUI-heavy nature of the project
- Includes specific test targets for each module/method

Let me structure this properly with phases and clear priorities. I've already created a comprehensive Testing.md file. The user is now asking me to "Write a detailed plan to Testing.md". Looking at my previous response, I already wrote a very detailed testing plan with 8 phases covering:

1. Foundation (test infrastructure + ui_loader.py)
2. Configuration Logic (pure data transformation)
3. Process Command Building (llama-server command construction)
4. Path Selection Methods (file dialogs)
5. Signal Handling and UI Logic
6. Initialization and Lifecycle
7. Edge Cases and Error Handling
8. Integration Tests

The file I created has:
- 100+ individual test cases with specific line references
- Coverage estimates per phase
- Strategy notes for testing Qt code
- Refactoring recommendations
- Test file structure
- Running commands
- TDD implementation notes

This is already a very comprehensive plan. The user's request "Write a detailed plan to Testing.md" seems to be asking me to create this file, which I've already done. Let me verify the file was created successfully and summarize what was written.

Actually, looking at the tool response, it shows the file was created successfully with 526 lines of content. The plan is comprehensive and covers all the key areas. Let me provide a summary to the user.

</thinking>

I've created `Testing.md` — a comprehensive, phased testing plan with **100+ specific test cases** targeting >90% coverage. Here's what it includes:

## Structure

**8 phases**, ordered by priority (easiest/highest-ROI first):

| Phase | Focus | Est. Coverage | Test Cases |
|-------|-------|--------------|------------|
| 1 | Foundation + `ui_loader.py` | ~7% | 10 |
| 2 | Configuration logic (collect/apply/save/load) | ~30% | 41 |
| 3 | Process command building (~80 conditional params) | ~25% | 48 |
| 4 | Path selection methods | ~5% | 6 |
| 5 | Signal handling & UI logic | ~20% | 17 |
| 6 | Initialization & lifecycle | ~8% | 15 |
| 7 | Edge cases & error handling | ~3% | 9 |
| 8 | Integration tests | N/A | 5 |

**Total estimated coverage: ~95%**

## Key Design Decisions

- **Pure logic first** — config handling and command building are testable without Qt event loop, giving highest ROI per hour
- **pytest-qt required** — plan specifies adding `pytest-qt` and `pytest-cov` as dev dependencies
- **Mocking strategy documented** — QFileDialog, QProcess, QSettings all have explicit mocking approaches
- **Refactoring recommendations** — suggests extracting `ConfigurationManager`, `CommandBuilder`, and `SessionManager` classes to dramatically improve testability for future TDD work

## What's Next

To start implementing, the first step would be:

```bash
uv add --dev pytest-qt pytest-cov
mkdir -p tests/files
```

Then begin with **Phase 1.2** — testing `ui_loader.py` (the smallest, most isolated module). Want me to create the test infrastructure and write the first tests?
