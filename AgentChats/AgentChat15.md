## User

Implement Phase 1 from [@TODO.md](file:///Volumes/teaching/Code/LLamaLauncher/TODO.md)

## Assistant

<thinking>
Let me start by understanding the project structure and reading the TODO file, then explore the codebase to understand how to implement these changes.

</thinking>

I'll start by exploring the project structure and understanding the current codebase before implementing Phase 1.



**Tool Call: List the `LLamaLauncher` directory's contents**
Status: Completed

# Folders:
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
LLamaLauncher/TODO.md
LLamaLauncher/err
LLamaLauncher/main.py
LLamaLauncher/pyproject.toml
LLamaLauncher/ui_loader.py
LLamaLauncher/uv.lock


**Tool Call: Read file `TODO.md`**
Status: Completed

```LLamaLauncher/TODO.md
     1	# TODO
     2	
     3	## Phase 1: Web viewer
     4	
     5	[ ] Add ability to set --host HOST  and --port PORT this should be below the api section. Default values should be 127.0.0.1 and 8080 respectively.
     6	[ ] Update the central widget so the current UI is in a tab group called Model
     7	[ ] Add another Tab group for Server
     8	[ ] In the server tab group add a QWebEngineView that displays the server from above

```


## Assistant

<thinking>
<think>


</thinking>

Now let me explore the main files to understand the current structure:



**Tool Call: Read file `main.py`**
Status: Completed

```LLamaLauncher/main.py
     1	#!/usr/bin/env -S uv run --script
     2	"""Llama model launcher application."""
     3	
     4	import sys
     5	from pathlib import Path
     6	
     7	from PySide6.QtCore import QProcess, QTimer
     8	from PySide6.QtWidgets import (
     9	    QApplication,
    10	    QFileDialog,
    11	    QMainWindow,
    12	)
    13	
    14	from ui_loader import load_ui
    15	
    16	
    17	class LlamaLaunchApp(QMainWindow):
    18	    """Main application window for the Llama model launcher.
    19	
    20	    Loads its UI from a .ui file via QUiLoader and wires up all
    21	    signals and slots to preserve existing behaviour.
    22	    """
    23	
    24	    def __init__(self) -> None:
    25	        super().__init__()
    26	        self._process = QProcess(self)
    27	        self._process.readyReadStandardOutput.connect(self._on_stdout)
    28	        self._process.readyReadStandardError.connect(self._on_stderr)
    29	        self._process.finished.connect(self._on_finished)
    30	        self._process.errorOccurred.connect(self._on_error)
    31	        self._setup_ui()
    32	        self._connect_signals()
    33	
    34	    # ------------------------------------------------------------------
    35	    # UI loading
    36	    # ------------------------------------------------------------------
    37	
    38	    def _setup_ui(self) -> None:
    39	        """Load the main window UI from the .ui file.
    40	
    41	        All child widgets and layouts are auto-assigned as attributes
    42	        on this instance by their ``objectName`` so that the .ui file
    43	        controls which names are available.
    44	        """
    45	        ui_path = Path(__file__).resolve().parent / "ui" / "llama_launch.ui"
    46	        load_ui(ui_path, self)
    47	
    48	    # ------------------------------------------------------------------
    49	    # Signal connections
    50	    # ------------------------------------------------------------------
    51	
    52	    def _connect_signals(self) -> None:
    53	        """Connect widget signals to their slot methods."""
    54	        self.select_model_button.clicked.connect(self._select_model)
    55	        self.select_mmproj_button.clicked.connect(self._select_mmproj)
    56	        self.model_path_edit.textChanged.connect(self._on_model_selection_changed)
    57	        self.launch_button.clicked.connect(self._toggle_launch)
    58	
    59	    # ------------------------------------------------------------------
    60	    # Slots
    61	    # ------------------------------------------------------------------
    62	
    63	    def _select_model(self) -> None:
    64	        """Open a file dialog to select a .gguf model file.
    65	
    66	        Stores the full path as a custom property on the line edit
    67	        (accessible via ``getProperty("fullPath")``) while displaying
    68	        only the short filename in the UI.
    69	        """
    70	        file_path, _ = QFileDialog.getOpenFileName(
    71	            self,
    72	            "Select GGUF Model",
    73	            "",
    74	            "GGUF Files (*.gguf)",
    75	        )
    76	        if file_path:
    77	            self._model_path = file_path
    78	            self.model_path_edit.setProperty("fullPath", file_path)
    79	            self.model_path_edit.setText(file_path.rsplit("/", 1)[-1])
    80	            self._on_model_selection_changed()
    81	
    82	    def _select_mmproj(self) -> None:
    83	        """Open a file dialog to select a .gguf mmproj file.
    84	
    85	        Stores the full path as a custom property on the line edit
    86	        (accessible via ``getProperty("fullPath")``) while displaying
    87	        only the short filename in the UI.
    88	        """
    89	        file_path, _ = QFileDialog.getOpenFileName(
    90	            self,
    91	            "Select Multi-Modal Projector",
    92	            "",
    93	            "GGUF Files (*.gguf)",
    94	        )
    95	        if file_path:
    96	            self._mmproj_path = file_path
    97	            self.mmproj_path_edit.setProperty("fullPath", file_path)
    98	            self.mmproj_path_edit.setText(file_path.rsplit("/", 1)[-1])
    99	
   100	    def _on_model_selection_changed(self) -> None:
   101	        """Enable launch button when a model is selected, disable otherwise."""
   102	        has_model = bool(self.model_path_edit.property("fullPath"))
   103	        is_running = self._process.state() == QProcess.Running
   104	        self.launch_button.setEnabled(has_model and not is_running)
   105	
   106	    def _toggle_launch(self) -> None:
   107	        """Launch or stop the llama-server based on current process state."""
   108	        if self._process.state() == QProcess.Running:
   109	            self._stop_model()
   110	        else:
   111	            self._launch_model()
   112	
   113	    def _stop_model(self) -> None:
   114	        """Stop the llama-server gracefully.
   115	
   116	        Sends SIGTERM (like pressing Ctrl+C) so the server can shut down
   117	        cleanly. If it does not stop within 2 seconds, falls back to
   118	        SIGKILL.
   119	        """
   120	        self._process.terminate()
   121	        self.output_display.appendPlainText("Stopping server... (sent SIGTERM)")
   122	        QTimer.singleShot(2000, self._force_kill_if_needed)
   123	
   124	    def _force_kill_if_needed(self) -> None:
   125	        """Force kill the process if graceful termination did not work."""
   126	        if self._process.state() == QProcess.Running:
   127	            self.output_display.appendPlainText("Server didn't stop gracefully. Force killing...")
   128	            self._process.kill()
   129	
   130	    def _reset_launch_button(self) -> None:
   131	        """Reset the launch button to its default state."""
   132	        self.launch_button.setText("LAUNCH")
   133	        self._on_model_selection_changed()
   134	
   135	    def _launch_model(self) -> None:
   136	        """Launch the llama-server binary with current configuration.
   137	
   138	        Builds the command-line arguments from the UI fields and starts
   139	        ``llama-server`` via QProcess.  Live stdout/stderr output is
   140	        streamed into ``output_display``.
   141	        """
   142	        model_path = self.model_path_edit.property("fullPath")
   143	        if not model_path:
   144	            self.output_display.appendPlainText("Error: no model selected.")
   145	            return
   146	
   147	        temperature = self.temperature_spinbox.value()
   148	        top_p = self.top_p_spinbox.value()
   149	        top_k = self.top_k_spinbox.value()
   150	
   151	        mmproj_path = self.mmproj_path_edit.property("fullPath")
   152	        no_mmproj_offload = self.no_mmproj_offload_checkbox.isChecked()
   153	        api_key = self.api_key_line_edit.text() if self.api_key_line_edit.text() else "12345"
   154	
   155	        # Build command: llama-server --model ... --temp ... ...
   156	        cmd = [
   157	            "llama-server",
   158	            "--model",
   159	            model_path,
   160	            "--temp",
   161	            str(temperature),
   162	            "--top-p",
   163	            str(top_p),
   164	            "--top-k",
   165	            str(top_k),
   166	            "--api-key",
   167	            api_key,
   168	        ]
   169	
   170	        if mmproj_path:
   171	            cmd.extend(["--mmproj", mmproj_path])
   172	            if no_mmproj_offload:
   173	                cmd.append("--no-mmproj-offload")
   174	
   175	        self.output_display.clear()
   176	        self.output_display.appendPlainText(f"Launching: {' '.join(cmd)}\n---\n")
   177	
   178	        # Use two-argument form: program + arguments list (args must NOT include the program)
   179	        self._process.start(cmd[0], cmd[1:])
   180	        self.launch_button.setText("STOP")
   181	
   182	    # ------------------------------------------------------------------
   183	    # QProcess output slots
   184	    # ------------------------------------------------------------------
   185	
   186	    def _on_stdout(self) -> None:
   187	        """Append stdout from the child process to the output display."""
   188	        data = self._process.readAllStandardOutput().data().decode("utf-8", errors="replace")
   189	        if data:
   190	            self.output_display.appendPlainText(data)
   191	
   192	    def _on_stderr(self) -> None:
   193	        """Append stderr from the child process to the output display."""
   194	        data = self._process.readAllStandardError().data().decode("utf-8", errors="replace")
   195	        if data:
   196	            self.output_display.appendPlainText(data)
   197	
   198	    def _on_error(self, error: QProcess.ProcessError) -> None:
   199	        """Called when the process encounters an error (e.g. not found)."""
   200	        msg = f"Error launching process: {error}"
   201	        self.output_display.appendPlainText(msg)
   202	        self._reset_launch_button()
   203	
   204	    def _on_finished(self, code: int, status: QProcess.ExitStatus) -> None:
   205	        """Called when the child process exits."""
   206	        if status == QProcess.ExitStatus.NormalExit:
   207	            self.output_display.appendPlainText(f"\n--- Process exited with code {code} ---")
   208	        else:
   209	            self.output_display.appendPlainText(f"\n--- Process terminated abnormally (code {code}) ---")
   210	        self._reset_launch_button()
   211	
   212	
   213	if __name__ == "__main__":
   214	    app = QApplication(sys.argv)
   215	    window = LlamaLaunchApp()
   216	    window.resize(800, 600)
   217	    window.show()
   218	    sys.exit(app.exec())

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


**Tool Call: List the `LLamaLauncher/ui` directory's contents**
Status: Completed


# Files:
LLamaLauncher/ui/llama_launch.ui


## Assistant

<thinking>
<think>


</thinking>

**Tool Call: Read file `ui/llama_launch.ui`**
Status: Completed

```LLamaLauncher/ui/llama_launch.ui
     1	<?xml version="1.0" encoding="UTF-8" ?>
     2	<ui version="4.0">
     3	 <class>LlamaLaunchApp</class>
     4	 <widget class="QWidget" name="LlamaLaunchApp">
     5	  <property name="geometry">
     6	   <rect>
     7	    <x>0</x>
     8	    <y>0</y>
     9	    <width>800</width>
    10	    <height>600</height>
    11	   </rect>
    12	  </property>
    13	  <property name="windowTitle">
    14	   <string>Llama Launch</string>
    15	  </property>
    16	  <layout class="QVBoxLayout" name="verticalLayout">
    17	   <item>
    18	    <widget class="QGroupBox" name="model_group">
    19	     <property name="title">
    20	      <string>MODEL</string>
    21	     </property>
    22	     <layout class="QVBoxLayout" name="model_group_layout">
    23	      <item>
    24	       <layout class="QHBoxLayout" name="model_selector_layout">
    25	        <item>
    26	         <widget class="QLabel" name="choose_label">
    27	          <property name="text">
    28	           <string>Model</string>
    29	          </property>
    30	         </widget>
    31	        </item>
    32	        <item>
    33	         <widget class="QLineEdit" name="model_path_edit">
    34	          <property name="readOnly">
    35	           <bool>true</bool>
    36	          </property>
    37	         </widget>
    38	        </item>
    39	        <item>
    40	         <widget class="QPushButton" name="select_model_button">
    41	          <property name="text">
    42	           <string>Select Model...</string>
    43	          </property>
    44	         </widget>
    45	        </item>
    46	       </layout>
    47	      </item>
    48	      <item>
    49	       <layout class="QHBoxLayout" name="mmproj_selector_layout">
    50	        <item>
    51	         <widget class="QLabel" name="mmproj_label">
    52	          <property name="text">
    53	           <string>Multi Modal Input</string>
    54	          </property>
    55	         </widget>
    56	        </item>
    57	        <item>
    58	         <widget class="QLineEdit" name="mmproj_path_edit">
    59	          <property name="readOnly">
    60	           <bool>true</bool>
    61	          </property>
    62	         </widget>
    63	        </item>
    64	        <item>
    65	         <widget class="QPushButton" name="select_mmproj_button">
    66	          <property name="text">
    67	           <string>Select...</string>
    68	          </property>
    69	         </widget>
    70	        </item>
    71	        <item>
    72	         <widget class="QCheckBox" name="no_mmproj_offload_checkbox">
    73	          <property name="text">
    74	           <string>--no-mmproj-offload</string>
    75	          </property>
    76	         </widget>
    77	        </item>
    78	       </layout>
    79	      </item>
    80	      <item>
    81	       <layout class="QHBoxLayout" name="api_key_layout">
    82	        <item>
    83	         <widget class="QLabel" name="api_key_label">
    84	          <property name="text">
    85	           <string>API key</string>
    86	          </property>
    87	         </widget>
    88	        </item>
    89	        <item>
    90	         <widget class="QLineEdit" name="api_key_line_edit">
    91	          <property name="text">
    92	           <string>12345</string>
    93	          </property>
    94	         </widget>
    95	        </item>
    96	        <item>
    97	         <spacer name="api_key_spacer">
    98	          <property name="orientation">
    99	           <enum>Qt::Horizontal</enum>
   100	          </property>
   101	          <property name="sizeHint" stdset="0">
   102	           <size>
   103	            <width>40</width>
   104	            <height>20</height>
   105	           </size>
   106	          </property>
   107	         </spacer>
   108	        </item>
   109	       </layout>
   110	      </item>
   111	     </layout>
   112	    </widget>
   113	   </item>
   114	   <item>
   115	    <widget class="QGroupBox" name="tempGroup">
   116	     <property name="title">
   117	      <string>TEMP</string>
   118	     </property>
   119	     <layout class="QVBoxLayout" name="temp_group_layout">
   120	      <item>
   121	       <layout class="QFormLayout" name="temp_form_layout">
   122	        <item row="0" column="0">
   123	         <widget class="QLabel" name="temp_label">
   124	          <property name="text">
   125	           <string>Temp:</string>
   126	          </property>
   127	         </widget>
   128	        </item>
   129	        <item row="0" column="1">
   130	         <widget class="QDoubleSpinBox" name="temperature_spinbox">
   131	          <property name="value">
   132	           <double>0.300000000000000</double>
   133	          </property>
   134	         </widget>
   135	        </item>
   136	        <item row="1" column="0">
   137	         <widget class="QLabel" name="top_p_label">
   138	          <property name="text">
   139	           <string>Top P:</string>
   140	          </property>
   141	         </widget>
   142	        </item>
   143	        <item row="1" column="1">
   144	         <widget class="QDoubleSpinBox" name="top_p_spinbox">
   145	          <property name="value">
   146	           <double>0.900000000000000</double>
   147	          </property>
   148	         </widget>
   149	        </item>
   150	        <item row="2" column="0">
   151	         <widget class="QLabel" name="top_k_label">
   152	          <property name="text">
   153	           <string>Top K:</string>
   154	          </property>
   155	         </widget>
   156	        </item>
   157	        <item row="2" column="1">
   158	         <widget class="QDoubleSpinBox" name="top_k_spinbox">
   159	          <property name="value">
   160	           <double>40.000000000000000</double>
   161	          </property>
   162	         </widget>
   163	        </item>
   164	       </layout>
   165	      </item>
   166	     </layout>
   167	    </widget>
   168	   </item>
   169	   <item>
   170	    <widget class="QGroupBox" name="moreOptionsGroup">
   171	     <property name="title">
   172	      <string>More Options</string>
   173	     </property>
   174	     <layout class="QVBoxLayout" name="more_options_layout">
   175	      <item>
   176	       <widget class="QLabel" name="more_options_label">
   177	        <property name="text">
   178	         <string>More Options...</string>
   179	        </property>
   180	       </widget>
   181	      </item>
   182	     </layout>
   183	    </widget>
   184	   </item>
   185	   <item>
   186	    <widget class="QPlainTextEdit" name="output_display">
   187	     <property name="readOnly">
   188	      <bool>true</bool>
   189	     </property>
   190	     <property name="placeholderText">
   191	      <string>Model output will appear here...</string>
   192	     </property>
   193	    </widget>
   194	   </item>
   195	   <item>
   196	    <widget class="QPushButton" name="launch_button">
   197	     <property name="text">
   198	      <string>LAUNCH</string>
   199	     </property>
   200	    </widget>
   201	   </item>
   202	   <item>
   203	    <spacer name="vertical_spacer">
   204	     <property name="orientation">
   205	      <enum>Qt::Orientation::Vertical</enum>
   206	     </property>
   207	     <property name="sizeHint" stdset="0">
   208	      <size>
   209	       <width>0</width>
   210	       <height>0</height>
   211	      </size>
   212	     </property>
   213	    </spacer>
   214	   </item>
   215	  </layout>
   216	 </widget>
   217	 <resources />
   218	 <connections />
   219	</ui>

```


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

```


## Assistant

<thinking>
<think>


</thinking>

Now I have a clear picture of the codebase. Let me check for existing tests before creating the worktree.



**Tool Call: No matches**
Status: Completed

```json
{
  "offset": 0,
  "current_matches_page": [],
  "all_matches_len": 0
}
```

**Tool Call: List the `LLamaLauncher/.worktrees` directory's contents**
Status: Completed

# Folders:
LLamaLauncher/.worktrees/resize-ui


## Assistant

<thinking>
Let me understand the current git status and create a worktree for this task.

Looking at the TODO, I need to:
1. Add `--host HOST` and `--port PORT` CLI arguments (defaults: 127.0.0.1 and 8080), placed below the API section in the UI
2. Wrap the current UI in a QTabWidget with "Model" as one tab
3. Add another tab called "Server"
4. In the Server tab, add a QWebEngineView to display the server web interface

Let me check the git status first and create a worktree.

</thinking>

**Tool Call: cd LLamaLauncher && git status --short**
Status: Completed

Terminal:
```
sh: cd: LLamaLauncher: No such file or directory





```


## Assistant

<thinking>
The user's project is at /Volumes/teaching/Code/LLamaLauncher. I need to use the absolute path for the terminal command.

</thinking>

**Tool Call: git status --short**
Status: Completed

Terminal:
```
?? .worktrees/
?? docs/agent-sessions/
?? docs/llama_help.md



```


## Assistant

<thinking>
Let me check the current branch status before creating a worktree.

</thinking>

Good, there are only untracked files on the current branch. Let me create the worktree and implement Phase 1.



**Tool Call: git worktree add .worktrees/phase1-web-viewer -b agent/phase1-web-viewer**
Status: Completed

Terminal:
```
Preparing worktree (new branch 'agent/phase1-web-viewer')
HEAD is now at 21ec907 added TODO




```


## Assistant

<thinking>
Now I need to implement Phase 1 from the TODO. Let me understand what needs to be done:

1. Add ability to set --host HOST and --port PORT (below the api section, defaults: 127.0.0.1 and 8080)
2. Update the central widget so the current UI is in a tab group called "Model"
3. Add another Tab group for "Server"
4. In the server tab group add a QWebEngineView that displays the server

Let me plan the implementation:

1. **CLI arguments**: Add argparse for --host and --port in main.py, pass these to the app
2. **UI changes**: Modify the .ui file to wrap existing content in a QTabWidget with "Model" tab, add "Server" tab with QWebEngineView
3. **Add host/port fields**: These should be added to the UI below the API key section
4. **main.py updates**: Accept host/port, pass to launch command, initialize QWebEngineView in Server tab

Let me think about the structure:
- The current .ui file loads into the QMainWindow as central widget
- I need to wrap everything in a QTabWidget with two tabs: "Model" and "Server"
- The "Model" tab contains all the current UI (model selection, temp, more options, output display, launch button)
- The "Server" tab contains a QWebEngineView

For the host/port fields, they should be added to the UI below the API section. Since the TODO says "below the api section", I'll add them as new fields in the UI file.

Actually, let me reconsider. The host/port could either be:
1. CLI arguments (--host, --port) that override UI values
2. UI fields for host and port inputs

The TODO says "Add ability to set --host HOST and --port PORT" which suggests CLI arguments. But since this is a GUI app, it makes sense to have both - CLI args for convenience and UI fields for flexibility.

Let me add:
- CLI arguments --host and --port with defaults
- UI fields in the .ui file (after API key section) for host and port
- The launch command should use these values

For the QWebEngineView, I need to add it to the pyproject.toml dependencies and create it in the Server tab.

Let me implement this step by step:

1. Update pyproject.toml to add pyside6-webengine dependency
2. Update the .ui file to add host/port fields and wrap in QTabWidget
3. Update main.py to handle CLI args, pass them through, and initialize the web view

Actually, looking more carefully at the code structure:
- The UI is loaded from a .ui file via QUiLoader
- The main.py uses load_ui() which sets the loaded widget as central widget
- I need to wrap the current content in a QTabWidget

The cleanest approach would be to:
1. Modify the .ui file to include a QTabWidget with two tabs
2. Add host/port input fields to the Model tab (below API key)
3. Add QWebEngineView to the Server tab
4. Update main.py to handle CLI args and initialize the web engine

Let me start implementing:

For the UI file, I'll restructure it to have:
- A central QTabWidget
  - Tab 1: "Model" (contains all current content)
    - model_group
    - tempGroup
    - moreOptionsGroup
    - New host/port group (below API key section)
    - output_display
    - launch_button
  - Tab 2: "Server"
    - QWebEngineView

Actually, I need to be careful here. The TODO says "Update the central widget so the current UI is in a tab group called Model". This means wrapping the entire current UI into a tab. Let me think about whether to put host/port in the Model tab or as a separate section.

The TODO says "Add ability to set --host HOST and --port PORT this should be below the api section." So it should be in the UI, below the API key line edit. I'll add it to the Model tab since that's where the configuration controls are.

Let me structure the .ui file changes:
1. Wrap everything in a QTabWidget
2. First tab: "Model" with all current content plus host/port fields after api_key_layout
3. Second tab: "Server" with QWebEngineView

Now for the main.py changes:
1. Add argparse to parse --host and --port
2. Pass these values to the app constructor or widget
3. Use them in _launch_model() to add --host and --port arguments
4. Initialize QWebEngineView in the Server tab
5. Load the server URL (http://host:port) into the web view

Let me also check if pyside6-webengine is needed or if it's included with pyside6. In Qt6, WebEngine is a separate module that needs to be installed separately as pyside6-webengine.

Let me implement this now.

</thinking>

Now I'll implement Phase 1. Let me start by updating the project dependencies and then modifying the UI and main code.



**Tool Call: pyproject.toml**
Status: Completed

Diff: pyproject.toml
```
[project]
name = "llamalauncher"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.14"
dependencies = [
    "pyside6>=6.11.1",
    "pyside6-webengine>=6.11.1",
    "requests>=2.34.2",
]

```


## Assistant

<thinking>
Now I need to update the UI file and main.py. Let me think about the structure carefully.

The TODO says:
1. Add --host HOST and --port PORT CLI arguments (defaults 127.0.0.1 and 8080)
2. Wrap current UI in a tab group called "Model"
3. Add another tab for "Server"
4. In Server tab, add QWebEngineView to display the server

For the UI file, I need to:
- Add host and port input fields below the API key section
- Wrap everything in a QTabWidget with "Model" and "Server" tabs

Let me create the updated UI file and main.py.

</thinking>

Now let me update the UI file to add host/port fields and wrap the content in a QTabWidget:



**Tool Call: ui/llama\_launch.ui**
Status: Completed

Diff: ui/llama_launch.ui
```
<?xml version="1.0" encoding="UTF-8" ?>
<ui version="4.0">
 <class>LlamaLaunchApp</class>
 <widget class="QWidget" name="LlamaLaunchApp">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>800</width>
    <height>600</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Llama Launch</string>
  </property>
  <layout class="QVBoxLayout" name="verticalLayout">
   <item>
    <widget class="QGroupBox" name="model_group">
     <property name="title">
      <string>MODEL</string>
     </property>
     <layout class="QVBoxLayout" name="model_group_layout">
      <item>
       <layout class="QHBoxLayout" name="model_selector_layout">
        <item>
         <widget class="QLabel" name="choose_label">
          <property name="text">
           <string>Model</string>
          </property>
         </widget>
        </item>
        <item>
         <widget class="QLineEdit" name="model_path_edit">
          <property name="readOnly">
           <bool>true</bool>
          </property>
         </widget>
        </item>
        <item>
         <widget class="QPushButton" name="select_model_button">
          <property name="text">
           <string>Select Model...</string>
          </property>
         </widget>
        </item>
       </layout>
      </item>
      <item>
       <layout class="QHBoxLayout" name="mmproj_selector_layout">
        <item>
         <widget class="QLabel" name="mmproj_label">
          <property name="text">
           <string>Multi Modal Input</string>
          </property>
         </widget>
        </item>
        <item>
         <widget class="QLineEdit" name="mmproj_path_edit">
          <property name="readOnly">
           <bool>true</bool>
          </property>
         </widget>
        </item>
        <item>
         <widget class="QPushButton" name="select_mmproj_button">
          <property name="text">
           <string>Select...</string>
          </property>
         </widget>
        </item>
        <item>
         <widget class="QCheckBox" name="no_mmproj_offload_checkbox">
          <property name="text">
           <string>--no-mmproj-offload</string>
          </property>
         </widget>
        </item>
       </layout>
      </item>
      <item>
       <layout class="QHBoxLayout" name="api_key_layout">
        <item>
         <widget class="QLabel" name="api_key_label">
          <property name="text">
           <string>API key</string>
          </property>
         </widget>
        </item>
        <item>
         <widget class="QLineEdit" name="api_key_line_edit">
          <property name="text">
           <string>12345</string>
          </property>
         </widget>
        </item>
        <item>
         <spacer name="api_key_spacer">
          <property name="orientation">
           <enum>Qt::Horizontal</enum>
          </property>
          <property name="sizeHint" stdset="0">
           <size>
            <width>40</width>
            <height>20</height>
           </size>
          </property>
         </spacer>
        </item>
       </layout>
      </item>
      <item>
       <layout class="QHBoxLayout" name="host_port_layout">
        <item>
         <widget class="QLabel" name="host_label">
          <property name="text">
           <string>Host:</string>
          </property>
         </widget>
        </item>
        <item>
         <widget class="QLineEdit" name="host_line_edit">
          <property name="text">
           <string>127.0.0.1</string>
          </property>
         </widget>
        </item>
        <item>
         <widget class="QLabel" name="port_label">
          <property name="text">
           <string>Port:</string>
          </property>
         </widget>
        </item>
        <item>
         <widget class="QLineEdit" name="port_line_edit">
          <property name="text">
           <string>8080</string>
          </property>
         </widget>
        </item>
       </layout>
      </item>
     </layout>
    </widget>
   </item>
   <item>
    <widget class="QGroupBox" name="tempGroup">
     <property name="title">
      <string>TEMP</string>
     </property>
     <layout class="QVBoxLayout" name="temp_group_layout">
      <item>
       <layout class="QFormLayout" name="temp_form_layout">
        <item row="0" column="0">
         <widget class="QLabel" name="temp_label">
          <property name="text">
           <string>Temp:</string>
          </property>
         </widget>
        </item>
        <item row="0" column="1">
         <widget class="QDoubleSpinBox" name="temperature_spinbox">
          <property name="value">
           <double>0.300000000000000</double>
          </property>
         </widget>
        </item>
        <item row="1" column="0">
         <widget class="QLabel" name="top_p_label">
          <property name="text">
           <string>Top P:</string>
          </property>
         </widget>
        </item>
        <item row="1" column="1">
         <widget class="QDoubleSpinBox" name="top_p_spinbox">
          <property name="value">
           <double>0.900000000000000</double>
          </property>
         </widget>
        </item>
        <item row="2" column="0">
         <widget class="QLabel" name="top_k_label">
          <property name="text">
           <string>Top K:</string>
          </property>
         </widget>
        </item>
        <item row="2" column="1">
         <widget class="QDoubleSpinBox" name="top_k_spinbox">
          <property name="value">
           <double>40.000000000000000</double>
          </property>
         </widget>
        </item>
       </layout>
      </item>
     </layout>
    </widget>
   </item>
   <item>
    <widget class="QGroupBox" name="moreOptionsGroup">
     <property name="title">
      <string>More Options</string>
     </property>
     <layout class="QVBoxLayout" name="more_options_layout">
      <item>
       <widget class="QLabel" name="more_options_label">
        <property name="text">
         <string>More Options...</string>
        </property>
       </widget>
      </item>
     </layout>
    </widget>
   </item>
   <item>
    <widget class="QPlainTextEdit" name="output_display">
     <property name="readOnly">
      <bool>true</bool>
     </property>
     <property name="placeholderText">
      <string>Model output will appear here...</string>
     </property>
    </widget>
   </item>
   <item>
    <widget class="QPushButton" name="launch_button">
     <property name="text">
      <string>LAUNCH</string>
     </property>
    </widget>
   </item>
   <item>
    <spacer name="vertical_spacer">
     <property name="orientation">
      <enum>Qt::Orientation::Vertical</enum>
     </property>
     <property name="sizeHint" stdset="0">
      <size>
       <width>0</width>
       <height>0</height>
      </size>
     </property>
    </spacer>
   </item>
  </layout>
 </widget>
 <resources />
 <connections />
</ui>

```


## Assistant

<thinking>
Good, I've added the host/port fields to the UI file. Now I need to:

1. Wrap the entire content in a QTabWidget with "Model" and "Server" tabs
2. Add QWebEngineView to the Server tab
3. Update main.py to:
   - Add CLI argument parsing for --host and --port
   - Use the UI values for host/port when launching
   - Initialize QWebEngineView in the Server tab

Let me now wrap the current content in a QTabWidget. I need to restructure the UI file significantly. The current structure is:

```xml
<widget class="QWidget" name="LlamaLaunchApp">
  <layout class="QVBoxLayout" name="verticalLayout">
    <item>
      <widget class="QGroupBox" name="model_group">...</widget>
    </item>
    <item>
      <widget class="QGroupBox" name="tempGroup">...</widget>
    </item>
    ...
  </layout>
</widget>
```

I need to change it to:

```xml
<widget class="QWidget" name="LlamaLaunchApp">
  <layout class="QVBoxLayout" name="verticalLayout">
    <item>
      <widget class="QTabWidget" name="tab_widget">
        <widget class="QWidget" name="model_tab">
          <attribute name="title">
            <string>Model</string>
          </attribute>
          <layout class="QVBoxLayout" name="model_tab_layout">
            <!-- All current content goes here -->
          </layout>
        </widget>
        <widget class="QWidget" name="server_tab">
          <attribute name="title">
            <string>Server</string>
          </attribute>
          <layout class="QVBoxLayout" name="server_tab_layout">
            <item>
              <widget class="QWebEngineView" name="server_web_view"/>
            </item>
          </layout>
        </widget>
      </widget>
    </item>
  </layout>
</widget>
```

I need to restructure the entire UI file. Let me do this carefully. The current content inside verticalLayout includes:
1. model_group (with model_selector_layout, mmproj_selector_layout, api_key_layout, and now host_port_layout)
2. tempGroup (with temp_form_layout)
3. moreOptionsGroup
4. output_display
5. launch_button
6. vertical_spacer

I'll wrap all of these in the Model tab, and add the Server tab with QWebEngineView.

Let me write the new UI file content.

Actually, I should use write_file to overwrite the entire UI file since the changes are structural and extensive. But first, let me read the current file again to make sure I have all the content.

Actually, I already have the content from my earlier read. Let me create the new structure.

For main.py, I need to:
1. Add argparse for --host and --port CLI arguments
2. Pass these values to the app (either via constructor or by setting them on the widget after loading)
3. In _launch_model(), use the UI values (or CLI overrides) for host and port
4. Initialize QWebEngineView in the Server tab - this means I need to import WebEngineView and load the URL

Let me think about how to handle CLI vs UI values:
- CLI args should override UI values if provided
- The app should store these values and use them when launching

I'll modify the approach:
1. Parse CLI args in main.py
2. After loading the UI, if CLI args were provided, set the host_line_edit and port_line_edit text to those values
3. In _launch_model(), read from the UI fields (which now have either default or CLI-overridden values)

For the QWebEngineView:
- Import QWebEngineView from PySide6.QtWebEngineWidgets
- After loading the UI, get the server_web_view widget
- Connect to the server URL when it's available or when the server starts

Actually, I should load the URL into the web view. The TODO says "displays the server from above", which means the llama-server web interface at http://host:port.

Let me think about when to load the URL:
- Option 1: Load it immediately when the app starts (but the server isn't running yet)
- Option 2: Load it when the user clicks LAUNCH
- Option 3: Keep reloading or have a refresh button

I think the best approach is to load the URL when the app initializes, and let the web view show a "cannot connect" message until the server starts. Or I could load it when the LAUNCH button is clicked.

Actually, looking at similar launcher apps, the common pattern is:
1. Show the web view in the Server tab
2. When the user clicks LAUNCH, start the server and then load the URL in the web view
3. The web view will show the server's web interface once it's running

Let me implement it so that when _launch_model() succeeds (process starts), we update the web view to point to http://host:port. I'll also need to handle the case where the server stops - maybe clear the URL or show a message.

For simplicity, I'll load the URL in _launch_model() after successfully starting the process, and also connect to the process finished signal to potentially update the view.

Let me now write the complete new UI file and update main.py.

I realize I should write the full UI file since I'm restructuring it significantly. Let me do that.

For the web engine view, I need to use QWebEngineView from PySide6.QtWebEngineWidgets. In Qt6, this is part of the pyside6-webengine package which I just added to dependencies.

Let me write the complete new UI file now.

</thinking>

Now I need to wrap the entire content in a QTabWidget with "Model" and "Server" tabs, and add QWebEngineView to the Server tab. Let me restructure the UI file:



**Tool Call: ui/llama\_launch.ui**
Status: Completed

Diff: ui/llama_launch.ui
```
<?xml version="1.0" encoding="UTF-8" ?>
<ui version="4.0">
 <class>LlamaLaunchApp</class>
 <widget class="QWidget" name="LlamaLaunchApp">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>800</width>
    <height>600</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Llama Launch</string>
  </property>
  <layout class="QVBoxLayout" name="verticalLayout">
   <item>
    <widget class="QTabWidget" name="tab_widget">
     <property name="currentIndex">
      <number>0</number>
     </property>
     <widget class="QWidget" name="model_tab">
      <attribute name="title">
       <string>Model</string>
      </attribute>
      <layout class="QVBoxLayout" name="model_tab_layout">
       <item>
        <widget class="QGroupBox" name="model_group">
         <property name="title">
          <string>MODEL</string>
         </property>
         <layout class="QVBoxLayout" name="model_group_layout">
          <item>
           <layout class="QHBoxLayout" name="model_selector_layout">
            <item>
             <widget class="QLabel" name="choose_label">
              <property name="text">
               <string>Model</string>
              </property>
             </widget>
            </item>
            <item>
             <widget class="QLineEdit" name="model_path_edit">
              <property name="readOnly">
               <bool>true</bool>
              </property>
             </widget>
            </item>
            <item>
             <widget class="QPushButton" name="select_model_button">
              <property name="text">
               <string>Select Model...</string>
              </property>
             </widget>
            </item>
           </layout>
          </item>
          <item>
           <layout class="QHBoxLayout" name="mmproj_selector_layout">
            <item>
             <widget class="QLabel" name="mmproj_label">
              <property name="text">
               <string>Multi Modal Input</string>
              </property>
             </widget>
            </item>
            <item>
             <widget class="QLineEdit" name="mmproj_path_edit">
              <property name="readOnly">
               <bool>true</bool>
              </property>
             </widget>
            </item>
            <item>
             <widget class="QPushButton" name="select_mmproj_button">
              <property name="text">
               <string>Select...</string>
              </property>
             </widget>
            </item>
            <item>
             <widget class="QCheckBox" name="no_mmproj_offload_checkbox">
              <property name="text">
               <string>--no-mmproj-offload</string>
              </property>
             </widget>
            </item>
           </layout>
          </item>
          <item>
           <layout class="QHBoxLayout" name="api_key_layout">
            <item>
             <widget class="QLabel" name="api_key_label">
              <property name="text">
               <string>API key</string>
              </property>
             </widget>
            </item>
            <item>
             <widget class="QLineEdit" name="api_key_line_edit">
              <property name="text">
               <string>12345</string>
              </property>
             </widget>
            </item>
            <item>
             <spacer name="api_key_spacer">
              <property name="orientation">
               <enum>Qt::Horizontal</enum>
              </property>
              <property name="sizeHint" stdset="0">
               <size>
                <width>40</width>
                <height>20</height>
               </size>
              </property>
             </spacer>
            </item>
           </layout>
          </item>
          <item>
           <layout class="QHBoxLayout" name="host_port_layout">
            <item>
             <widget class="QLabel" name="host_label">
              <property name="text">
               <string>Host:</string>
              </property>
             </widget>
            </item>
            <item>
             <widget class="QLineEdit" name="host_line_edit">
              <property name="text">
               <string>127.0.0.1</string>
              </property>
             </widget>
            </item>
            <item>
             <widget class="QLabel" name="port_label">
              <property name="text">
               <string>Port:</string>
              </property>
             </widget>
            </item>
            <item>
             <widget class="QLineEdit" name="port_line_edit">
              <property name="text">
               <string>8080</string>
              </property>
             </widget>
            </item>
           </layout>
          </item>
         </layout>
        </widget>
       </item>
       <item>
        <widget class="QGroupBox" name="tempGroup">
         <property name="title">
          <string>TEMP</string>
         </property>
         <layout class="QVBoxLayout" name="temp_group_layout">
          <item>
           <layout class="QFormLayout" name="temp_form_layout">
            <item row="0" column="0">
             <widget class="QLabel" name="temp_label">
              <property name="text">
               <string>Temp:</string>
              </property>
             </widget>
            </item>
            <item row="0" column="1">
             <widget class="QDoubleSpinBox" name="temperature_spinbox">
              <property name="value">
               <double>0.300000000000000</double>
              </property>
             </widget>
            </item>
            <item row="1" column="0">
             <widget class="QLabel" name="top_p_label">
              <property name="text">
               <string>Top P:</string>
              </property>
             </widget>
            </item>
            <item row="1" column="1">
             <widget class="QDoubleSpinBox" name="top_p_spinbox">
              <property name="value">
               <double>0.900000000000000</double>
              </property>
             </widget>
            </item>
            <item row="2" column="0">
             <widget class="QLabel" name="top_k_label">
              <property name="text">
               <string>Top K:</string>
              </property>
             </widget>
            </item>
            <item row="2" column="1">
             <widget class="QDoubleSpinBox" name="top_k_spinbox">
              <property name="value">
               <double>40.000000000000000</double>
              </property>
             </widget>
            </item>
           </layout>
          </item>
         </layout>
        </widget>
       </item>
       <item>
        <widget class="QGroupBox" name="moreOptionsGroup">
         <property name="title">
          <string>More Options</string>
         </property>
         <layout class="QVBoxLayout" name="more_options_layout">
          <item>
           <widget class="QLabel" name="more_options_label">
            <property name="text">
             <string>More Options...</string>
            </property>
           </widget>
          </item>
         </layout>
        </widget>
       </item>
       <item>
        <widget class="QPlainTextEdit" name="output_display">
         <property name="readOnly">
          <bool>true</bool>
         </property>
         <property name="placeholderText">
          <string>Model output will appear here...</string>
         </property>
        </widget>
       </item>
       <item>
        <widget class="QPushButton" name="launch_button">
         <property name="text">
          <string>LAUNCH</string>
         </property>
        </widget>
       </item>
       <item>
        <spacer name="vertical_spacer">
         <property name="orientation">
          <enum>Qt::Orientation::Vertical</enum>
         </property>
         <property name="sizeHint" stdset="0">
          <size>
           <width>0</width>
           <height>0</height>
          </size>
         </property>
        </spacer>
       </item>
      </layout>
     </widget>
     <widget class="QWidget" name="server_tab">
      <attribute name="title">
       <string>Server</string>
      </attribute>
      <layout class="QVBoxLayout" name="server_tab_layout">
       <item>
        <widget class="QWebEngineView" name="server_web_view" />
       </item>
      </layout>
     </widget>
    </widget>
   </item>
  </layout>
 </widget>
 <resources />
 <connections />
</ui>

```


## Assistant

<thinking>
<think>


</thinking>

Good, the UI file is updated. Now I need to update main.py to:
1. Add argparse for --host and --port CLI arguments
2. Pass these values to the app
3. Use them when launching the server
4. Initialize QWebEngineView in the Server tab



**Tool Call: main.py**
Status: Completed

Diff: main.py
```
#!/usr/bin/env -S uv run --script
"""Llama model launcher application."""

import argparse
import sys
from pathlib import Path

from PySide6.QtCore import QProcess, QTimer
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
)

from ui_loader import load_ui


class LlamaLaunchApp(QMainWindow):
    """Main application window for the Llama model launcher.

    Loads its UI from a .ui file via QUiLoader and wires up all
    signals and slots to preserve existing behaviour.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 8080) -> None:
        super().__init__()
        self._process = QProcess(self)
        self._process.readyReadStandardOutput.connect(self._on_stdout)
        self._process.readyReadStandardError.connect(self._on_stderr)
        self._process.finished.connect(self._on_finished)
        self._process.errorOccurred.connect(self._on_error)
        self._host = host
        self._port = port
        self._setup_ui()
        self._connect_signals()
        self._init_web_view()

    # ------------------------------------------------------------------
    # UI loading and initialization
    # ------------------------------------------------------------------

    def _init_web_view(self) -> None:
        """Initialize the QWebEngineView in the Server tab."""
        url = f"http://{self._host}:{self._port}"
        self.server_web_view.setUrl(url)

    def _setup_ui(self) -> None:
        """Load the main window UI from the .ui file.

        All child widgets and layouts are auto-assigned as attributes
        on this instance by their ``objectName`` so that the .ui file
        controls which names are available.
        """
        ui_path = Path(__file__).resolve().parent / "ui" / "llama_launch.ui"
        load_ui(ui_path, self)

    # ------------------------------------------------------------------
    # Signal connections
    # ------------------------------------------------------------------

    def _connect_signals(self) -> None:
        """Connect widget signals to their slot methods."""
        self.select_model_button.clicked.connect(self._select_model)
        self.select_mmproj_button.clicked.connect(self._select_mmproj)
        self.model_path_edit.textChanged.connect(self._on_model_selection_changed)
        self.launch_button.clicked.connect(self._toggle_launch)

    # ------------------------------------------------------------------
    # Slots
    # ------------------------------------------------------------------

    def _select_model(self) -> None:
        """Open a file dialog to select a .gguf model file.

        Stores the full path as a custom property on the line edit
        (accessible via ``getProperty("fullPath")``) while displaying
        only the short filename in the UI.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select GGUF Model",
            "",
            "GGUF Files (*.gguf)",
        )
        if file_path:
            self._model_path = file_path
            self.model_path_edit.setProperty("fullPath", file_path)
            self.model_path_edit.setText(file_path.rsplit("/", 1)[-1])
            self._on_model_selection_changed()

    def _select_mmproj(self) -> None:
        """Open a file dialog to select a .gguf mmproj file.

        Stores the full path as a custom property on the line edit
        (accessible via ``getProperty("fullPath")``) while displaying
        only the short filename in the UI.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Multi-Modal Projector",
            "",
            "GGUF Files (*.gguf)",
        )
        if file_path:
            self._mmproj_path = file_path
            self.mmproj_path_edit.setProperty("fullPath", file_path)
            self.mmproj_path_edit.setText(file_path.rsplit("/", 1)[-1])

    def _on_model_selection_changed(self) -> None:
        """Enable launch button when a model is selected, disable otherwise."""
        has_model = bool(self.model_path_edit.property("fullPath"))
        is_running = self._process.state() == QProcess.Running
        self.launch_button.setEnabled(has_model and not is_running)

    def _toggle_launch(self) -> None:
        """Launch or stop the llama-server based on current process state."""
        if self._process.state() == QProcess.Running:
            self._stop_model()
        else:
            self._launch_model()

    def _stop_model(self) -> None:
        """Stop the llama-server gracefully.

        Sends SIGTERM (like pressing Ctrl+C) so the server can shut down
        cleanly. If it does not stop within 2 seconds, falls back to
        SIGKILL.
        """
        self._process.terminate()
        self.output_display.appendPlainText("Stopping server... (sent SIGTERM)")
        QTimer.singleShot(2000, self._force_kill_if_needed)

    def _force_kill_if_needed(self) -> None:
        """Force kill the process if graceful termination did not work."""
        if self._process.state() == QProcess.Running:
            self.output_display.appendPlainText("Server didn't stop gracefully. Force killing...")
            self._process.kill()

    def _reset_launch_button(self) -> None:
        """Reset the launch button to its default state."""
        self.launch_button.setText("LAUNCH")
        self._on_model_selection_changed()

    def _launch_model(self) -> None:
        """Launch the llama-server binary with current configuration.

        Builds the command-line arguments from the UI fields and starts
        ``llama-server`` via QProcess.  Live stdout/stderr output is
        streamed into ``output_display``.
        """
        model_path = self.model_path_edit.property("fullPath")
        if not model_path:
            self.output_display.appendPlainText("Error: no model selected.")
            return

        temperature = self.temperature_spinbox.value()
        top_p = self.top_p_spinbox.value()
        top_k = self.top_k_spinbox.value()

        mmproj_path = self.mmproj_path_edit.property("fullPath")
        no_mmproj_offload = self.no_mmproj_offload_checkbox.isChecked()
        api_key = self.api_key_line_edit.text() if self.api_key_line_edit.text() else "12345"

        # Build command: llama-server --model ... --temp ... ...
        cmd = [
            "llama-server",
            "--model",
            model_path,
            "--temp",
            str(temperature),
            "--top-p",
            str(top_p),
            "--top-k",
            str(top_k),
            "--api-key",
            api_key,
        ]

        host = self.host_line_edit.text() or self._host
        port_str = self.port_line_edit.text() or str(self._port)
        try:
            port = int(port_str)
        except ValueError:
            port = self._port

        if mmproj_path:
            cmd.extend(["--mmproj", mmproj_path])
            if no_mmproj_offload:
                cmd.append("--no-mmproj-offload")

        self.output_display.clear()
        self.output_display.appendPlainText(f"Launching: {' '.join(cmd)}\n---\n")

        # Use two-argument form: program + arguments list (args must NOT include the program)
        self._process.start(cmd[0], cmd[1:])
        self.launch_button.setText("STOP")

    # ------------------------------------------------------------------
    # QProcess output slots
    # ------------------------------------------------------------------

    def _on_stdout(self) -> None:
        """Append stdout from the child process to the output display."""
        data = self._process.readAllStandardOutput().data().decode("utf-8", errors="replace")
        if data:
            self.output_display.appendPlainText(data)

    def _on_stderr(self) -> None:
        """Append stderr from the child process to the output display."""
        data = self._process.readAllStandardError().data().decode("utf-8", errors="replace")
        if data:
            self.output_display.appendPlainText(data)

    def _on_error(self, error: QProcess.ProcessError) -> None:
        """Called when the process encounters an error (e.g. not found)."""
        msg = f"Error launching process: {error}"
        self.output_display.appendPlainText(msg)
        self._reset_launch_button()

    def _on_finished(self, code: int, status: QProcess.ExitStatus) -> None:
        """Called when the child process exits."""
        if status == QProcess.ExitStatus.NormalExit:
            self.output_display.appendPlainText(f"\n--- Process exited with code {code} ---")
        else:
            self.output_display.appendPlainText(f"\n--- Process terminated abnormally (code {code}) ---")
        self._reset_launch_button()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LlamaLaunchApp()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())

```


## Assistant

<thinking>
I need to add --host and --port arguments to the llama-server command, and also update the web view URL when the server starts. Let me also add the CLI argument parsing at the bottom of the file.

Looking at my edits, I added host/port reading but didn't add them to the cmd list yet. I need to:
1. Add --host and --port to the cmd list in _launch_model()
2. Update the web view URL after launching
3. Add argparse at the bottom for CLI arguments

Let me continue editing main.py.

</thinking>

Now I need to add `--host` and `--port` to the llama-server command, update the web view URL when the server launches, and add CLI argument parsing at the bottom of the file:



**Tool Call: main.py**
Status: Completed

Diff: main.py
```
#!/usr/bin/env -S uv run --script
"""Llama model launcher application."""

import argparse
import sys
from pathlib import Path

from PySide6.QtCore import QProcess, QTimer
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
)

from ui_loader import load_ui


class LlamaLaunchApp(QMainWindow):
    """Main application window for the Llama model launcher.

    Loads its UI from a .ui file via QUiLoader and wires up all
    signals and slots to preserve existing behaviour.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 8080) -> None:
        super().__init__()
        self._process = QProcess(self)
        self._process.readyReadStandardOutput.connect(self._on_stdout)
        self._process.readyReadStandardError.connect(self._on_stderr)
        self._process.finished.connect(self._on_finished)
        self._process.errorOccurred.connect(self._on_error)
        self._host = host
        self._port = port
        self._setup_ui()
        self._connect_signals()
        self._init_web_view()

    # ------------------------------------------------------------------
    # UI loading and initialization
    # ------------------------------------------------------------------

    def _init_web_view(self) -> None:
        """Initialize the QWebEngineView in the Server tab."""
        url = f"http://{self._host}:{self._port}"
        self.server_web_view.setUrl(url)

    def _setup_ui(self) -> None:
        """Load the main window UI from the .ui file.

        All child widgets and layouts are auto-assigned as attributes
        on this instance by their ``objectName`` so that the .ui file
        controls which names are available.
        """
        ui_path = Path(__file__).resolve().parent / "ui" / "llama_launch.ui"
        load_ui(ui_path, self)

    # ------------------------------------------------------------------
    # Signal connections
    # ------------------------------------------------------------------

    def _connect_signals(self) -> None:
        """Connect widget signals to their slot methods."""
        self.select_model_button.clicked.connect(self._select_model)
        self.select_mmproj_button.clicked.connect(self._select_mmproj)
        self.model_path_edit.textChanged.connect(self._on_model_selection_changed)
        self.launch_button.clicked.connect(self._toggle_launch)

    # ------------------------------------------------------------------
    # Slots
    # ------------------------------------------------------------------

    def _select_model(self) -> None:
        """Open a file dialog to select a .gguf model file.

        Stores the full path as a custom property on the line edit
        (accessible via ``getProperty("fullPath")``) while displaying
        only the short filename in the UI.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select GGUF Model",
            "",
            "GGUF Files (*.gguf)",
        )
        if file_path:
            self._model_path = file_path
            self.model_path_edit.setProperty("fullPath", file_path)
            self.model_path_edit.setText(file_path.rsplit("/", 1)[-1])
            self._on_model_selection_changed()

    def _select_mmproj(self) -> None:
        """Open a file dialog to select a .gguf mmproj file.

        Stores the full path as a custom property on the line edit
        (accessible via ``getProperty("fullPath")``) while displaying
        only the short filename in the UI.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Multi-Modal Projector",
            "",
            "GGUF Files (*.gguf)",
        )
        if file_path:
            self._mmproj_path = file_path
            self.mmproj_path_edit.setProperty("fullPath", file_path)
            self.mmproj_path_edit.setText(file_path.rsplit("/", 1)[-1])

    def _on_model_selection_changed(self) -> None:
        """Enable launch button when a model is selected, disable otherwise."""
        has_model = bool(self.model_path_edit.property("fullPath"))
        is_running = self._process.state() == QProcess.Running
        self.launch_button.setEnabled(has_model and not is_running)

    def _toggle_launch(self) -> None:
        """Launch or stop the llama-server based on current process state."""
        if self._process.state() == QProcess.Running:
            self._stop_model()
        else:
            self._launch_model()

    def _stop_model(self) -> None:
        """Stop the llama-server gracefully.

        Sends SIGTERM (like pressing Ctrl+C) so the server can shut down
        cleanly. If it does not stop within 2 seconds, falls back to
        SIGKILL.
        """
        self._process.terminate()
        self.output_display.appendPlainText("Stopping server... (sent SIGTERM)")
        QTimer.singleShot(2000, self._force_kill_if_needed)

    def _force_kill_if_needed(self) -> None:
        """Force kill the process if graceful termination did not work."""
        if self._process.state() == QProcess.Running:
            self.output_display.appendPlainText("Server didn't stop gracefully. Force killing...")
            self._process.kill()

    def _reset_launch_button(self) -> None:
        """Reset the launch button to its default state."""
        self.launch_button.setText("LAUNCH")
        self._on_model_selection_changed()

    def _launch_model(self) -> None:
        """Launch the llama-server binary with current configuration.

        Builds the command-line arguments from the UI fields and starts
        ``llama-server`` via QProcess.  Live stdout/stderr output is
        streamed into ``output_display``.
        """
        model_path = self.model_path_edit.property("fullPath")
        if not model_path:
            self.output_display.appendPlainText("Error: no model selected.")
            return

        temperature = self.temperature_spinbox.value()
        top_p = self.top_p_spinbox.value()
        top_k = self.top_k_spinbox.value()

        mmproj_path = self.mmproj_path_edit.property("fullPath")
        no_mmproj_offload = self.no_mmproj_offload_checkbox.isChecked()
        api_key = self.api_key_line_edit.text() if self.api_key_line_edit.text() else "12345"

        # Build command: llama-server --model ... --temp ... ...
        cmd = [
            "llama-server",
            "--model",
            model_path,
            "--temp",
            str(temperature),
            "--top-p",
            str(top_p),
            "--top-k",
            str(top_k),
            "--api-key",
            api_key,
        ]

        host = self.host_line_edit.text() or self._host
        port_str = self.port_line_edit.text() or str(self._port)
        try:
            port = int(port_str)
        except ValueError:
            port = self._port

        if mmproj_path:
            cmd.extend(["--mmproj", mmproj_path])
            if no_mmproj_offload:
                cmd.append("--no-mmproj-offload")

        cmd.extend(["--host", host, "--port", str(port)])

        self.output_display.clear()
        self.output_display.appendPlainText(f"Launching: {' '.join(cmd)}\n---\n")

        # Use two-argument form: program + arguments list (args must NOT include the program)
        self._process.start(cmd[0], cmd[1:])
        self.launch_button.setText("STOP")

        # Update web view to point to the server
        server_url = f"http://{host}:{port}"
        self.server_web_view.setUrl(server_url)

    # ------------------------------------------------------------------
    # QProcess output slots
    # ------------------------------------------------------------------

    def _on_stdout(self) -> None:
        """Append stdout from the child process to the output display."""
        data = self._process.readAllStandardOutput().data().decode("utf-8", errors="replace")
        if data:
            self.output_display.appendPlainText(data)

    def _on_stderr(self) -> None:
        """Append stderr from the child process to the output display."""
        data = self._process.readAllStandardError().data().decode("utf-8", errors="replace")
        if data:
            self.output_display.appendPlainText(data)

    def _on_error(self, error: QProcess.ProcessError) -> None:
        """Called when the process encounters an error (e.g. not found)."""
        msg = f"Error launching process: {error}"
        self.output_display.appendPlainText(msg)
        self._reset_launch_button()

    def _on_finished(self, code: int, status: QProcess.ExitStatus) -> None:
        """Called when the child process exits."""
        if status == QProcess.ExitStatus.NormalExit:
            self.output_display.appendPlainText(f"\n--- Process exited with code {code} ---")
        else:
            self.output_display.appendPlainText(f"\n--- Process terminated abnormally (code {code}) ---")
        self._reset_launch_button()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LlamaLaunchApp()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())

```


## Assistant

<thinking>
Now I need to add the CLI argument parsing at the bottom of main.py. Let me edit the `if __name__ == "__main__"` block to parse --host and --port arguments.

</thinking>

Now I need to add the CLI argument parsing at the bottom of main.py:



**Tool Call: main.py**
Status: Completed

Diff: main.py
```
#!/usr/bin/env -S uv run --script
"""Llama model launcher application."""

import argparse
import sys
from pathlib import Path

from PySide6.QtCore import QProcess, QTimer
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
)

from ui_loader import load_ui


class LlamaLaunchApp(QMainWindow):
    """Main application window for the Llama model launcher.

    Loads its UI from a .ui file via QUiLoader and wires up all
    signals and slots to preserve existing behaviour.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 8080) -> None:
        super().__init__()
        self._process = QProcess(self)
        self._process.readyReadStandardOutput.connect(self._on_stdout)
        self._process.readyReadStandardError.connect(self._on_stderr)
        self._process.finished.connect(self._on_finished)
        self._process.errorOccurred.connect(self._on_error)
        self._host = host
        self._port = port
        self._setup_ui()
        self._connect_signals()
        self._init_web_view()

    # ------------------------------------------------------------------
    # UI loading and initialization
    # ------------------------------------------------------------------

    def _init_web_view(self) -> None:
        """Initialize the QWebEngineView in the Server tab."""
        url = f"http://{self._host}:{self._port}"
        self.server_web_view.setUrl(url)

    def _setup_ui(self) -> None:
        """Load the main window UI from the .ui file.

        All child widgets and layouts are auto-assigned as attributes
        on this instance by their ``objectName`` so that the .ui file
        controls which names are available.
        """
        ui_path = Path(__file__).resolve().parent / "ui" / "llama_launch.ui"
        load_ui(ui_path, self)

    # ------------------------------------------------------------------
    # Signal connections
    # ------------------------------------------------------------------

    def _connect_signals(self) -> None:
        """Connect widget signals to their slot methods."""
        self.select_model_button.clicked.connect(self._select_model)
        self.select_mmproj_button.clicked.connect(self._select_mmproj)
        self.model_path_edit.textChanged.connect(self._on_model_selection_changed)
        self.launch_button.clicked.connect(self._toggle_launch)

    # ------------------------------------------------------------------
    # Slots
    # ------------------------------------------------------------------

    def _select_model(self) -> None:
        """Open a file dialog to select a .gguf model file.

        Stores the full path as a custom property on the line edit
        (accessible via ``getProperty("fullPath")``) while displaying
        only the short filename in the UI.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select GGUF Model",
            "",
            "GGUF Files (*.gguf)",
        )
        if file_path:
            self._model_path = file_path
            self.model_path_edit.setProperty("fullPath", file_path)
            self.model_path_edit.setText(file_path.rsplit("/", 1)[-1])
            self._on_model_selection_changed()

    def _select_mmproj(self) -> None:
        """Open a file dialog to select a .gguf mmproj file.

        Stores the full path as a custom property on the line edit
        (accessible via ``getProperty("fullPath")``) while displaying
        only the short filename in the UI.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Multi-Modal Projector",
            "",
            "GGUF Files (*.gguf)",
        )
        if file_path:
            self._mmproj_path = file_path
            self.mmproj_path_edit.setProperty("fullPath", file_path)
            self.mmproj_path_edit.setText(file_path.rsplit("/", 1)[-1])

    def _on_model_selection_changed(self) -> None:
        """Enable launch button when a model is selected, disable otherwise."""
        has_model = bool(self.model_path_edit.property("fullPath"))
        is_running = self._process.state() == QProcess.Running
        self.launch_button.setEnabled(has_model and not is_running)

    def _toggle_launch(self) -> None:
        """Launch or stop the llama-server based on current process state."""
        if self._process.state() == QProcess.Running:
            self._stop_model()
        else:
            self._launch_model()

    def _stop_model(self) -> None:
        """Stop the llama-server gracefully.

        Sends SIGTERM (like pressing Ctrl+C) so the server can shut down
        cleanly. If it does not stop within 2 seconds, falls back to
        SIGKILL.
        """
        self._process.terminate()
        self.output_display.appendPlainText("Stopping server... (sent SIGTERM)")
        QTimer.singleShot(2000, self._force_kill_if_needed)

    def _force_kill_if_needed(self) -> None:
        """Force kill the process if graceful termination did not work."""
        if self._process.state() == QProcess.Running:
            self.output_display.appendPlainText("Server didn't stop gracefully. Force killing...")
            self._process.kill()

    def _reset_launch_button(self) -> None:
        """Reset the launch button to its default state."""
        self.launch_button.setText("LAUNCH")
        self._on_model_selection_changed()

    def _launch_model(self) -> None:
        """Launch the llama-server binary with current configuration.

        Builds the command-line arguments from the UI fields and starts
        ``llama-server`` via QProcess.  Live stdout/stderr output is
        streamed into ``output_display``.
        """
        model_path = self.model_path_edit.property("fullPath")
        if not model_path:
            self.output_display.appendPlainText("Error: no model selected.")
            return

        temperature = self.temperature_spinbox.value()
        top_p = self.top_p_spinbox.value()
        top_k = self.top_k_spinbox.value()

        mmproj_path = self.mmproj_path_edit.property("fullPath")
        no_mmproj_offload = self.no_mmproj_offload_checkbox.isChecked()
        api_key = self.api_key_line_edit.text() if self.api_key_line_edit.text() else "12345"

        # Build command: llama-server --model ... --temp ... ...
        cmd = [
            "llama-server",
            "--model",
            model_path,
            "--temp",
            str(temperature),
            "--top-p",
            str(top_p),
            "--top-k",
            str(top_k),
            "--api-key",
            api_key,
        ]

        host = self.host_line_edit.text() or self._host
        port_str = self.port_line_edit.text() or str(self._port)
        try:
            port = int(port_str)
        except ValueError:
            port = self._port

        if mmproj_path:
            cmd.extend(["--mmproj", mmproj_path])
            if no_mmproj_offload:
                cmd.append("--no-mmproj-offload")

        cmd.extend(["--host", host, "--port", str(port)])

        self.output_display.clear()
        self.output_display.appendPlainText(f"Launching: {' '.join(cmd)}\n---\n")

        # Use two-argument form: program + arguments list (args must NOT include the program)
        self._process.start(cmd[0], cmd[1:])
        self.launch_button.setText("STOP")

        # Update web view to point to the server
        server_url = f"http://{host}:{port}"
        self.server_web_view.setUrl(server_url)

    # ------------------------------------------------------------------
    # QProcess output slots
    # ------------------------------------------------------------------

    def _on_stdout(self) -> None:
        """Append stdout from the child process to the output display."""
        data = self._process.readAllStandardOutput().data().decode("utf-8", errors="replace")
        if data:
            self.output_display.appendPlainText(data)

    def _on_stderr(self) -> None:
        """Append stderr from the child process to the output display."""
        data = self._process.readAllStandardError().data().decode("utf-8", errors="replace")
        if data:
            self.output_display.appendPlainText(data)

    def _on_error(self, error: QProcess.ProcessError) -> None:
        """Called when the process encounters an error (e.g. not found)."""
        msg = f"Error launching process: {error}"
        self.output_display.appendPlainText(msg)
        self._reset_launch_button()

    def _on_finished(self, code: int, status: QProcess.ExitStatus) -> None:
        """Called when the child process exits."""
        if status == QProcess.ExitStatus.NormalExit:
            self.output_display.appendPlainText(f"\n--- Process exited with code {code} ---")
        else:
            self.output_display.appendPlainText(f"\n--- Process terminated abnormally (code {code}) ---")
        self._reset_launch_button()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Llama model launcher application.")
    parser.add_argument("--host", default="127.0.0.1", help="Host address for the server (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8080, help="Port for the server (default: 8080)")
    args = parser.parse_args()

    app = QApplication(sys.argv)
    window = LlamaLaunchApp(host=args.host, port=args.port)
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())

```


## Assistant

<thinking>
Let me verify the changes I've made by reading the updated files to ensure everything is correct before running tests.

</thinking>

Now let me verify the changes look correct and then run the tests:



**Tool Call: Read file `main.py`**
Status: Completed

```LLamaLauncher/main.py
     1	#!/usr/bin/env -S uv run --script
     2	"""Llama model launcher application."""
     3	
     4	import argparse
     5	import sys
     6	from pathlib import Path
     7	
     8	from PySide6.QtCore import QProcess, QTimer
     9	from PySide6.QtWebEngineWidgets import QWebEngineView
    10	from PySide6.QtWidgets import (
    11	    QApplication,
    12	    QFileDialog,
    13	    QMainWindow,
    14	)
    15	
    16	from ui_loader import load_ui
    17	
    18	
    19	class LlamaLaunchApp(QMainWindow):
    20	    """Main application window for the Llama model launcher.
    21	
    22	    Loads its UI from a .ui file via QUiLoader and wires up all
    23	    signals and slots to preserve existing behaviour.
    24	    """
    25	
    26	    def __init__(self, host: str = "127.0.0.1", port: int = 8080) -> None:
    27	        super().__init__()
    28	        self._process = QProcess(self)
    29	        self._process.readyReadStandardOutput.connect(self._on_stdout)
    30	        self._process.readyReadStandardError.connect(self._on_stderr)
    31	        self._process.finished.connect(self._on_finished)
    32	        self._process.errorOccurred.connect(self._on_error)
    33	        self._host = host
    34	        self._port = port
    35	        self._setup_ui()
    36	        self._connect_signals()
    37	        self._init_web_view()
    38	
    39	    # ------------------------------------------------------------------
    40	    # UI loading and initialization
    41	    # ------------------------------------------------------------------
    42	
    43	    def _init_web_view(self) -> None:
    44	        """Initialize the QWebEngineView in the Server tab."""
    45	        url = f"http://{self._host}:{self._port}"
    46	        self.server_web_view.setUrl(url)
    47	
    48	    def _setup_ui(self) -> None:
    49	        """Load the main window UI from the .ui file.
    50	
    51	        All child widgets and layouts are auto-assigned as attributes
    52	        on this instance by their ``objectName`` so that the .ui file
    53	        controls which names are available.
    54	        """
    55	        ui_path = Path(__file__).resolve().parent / "ui" / "llama_launch.ui"
    56	        load_ui(ui_path, self)
    57	
    58	    # ------------------------------------------------------------------
    59	    # Signal connections
    60	    # ------------------------------------------------------------------
    61	
    62	    def _connect_signals(self) -> None:
    63	        """Connect widget signals to their slot methods."""
    64	        self.select_model_button.clicked.connect(self._select_model)
    65	        self.select_mmproj_button.clicked.connect(self._select_mmproj)
    66	        self.model_path_edit.textChanged.connect(self._on_model_selection_changed)
    67	        self.launch_button.clicked.connect(self._toggle_launch)
    68	
    69	    # ------------------------------------------------------------------
    70	    # Slots
    71	    # ------------------------------------------------------------------
    72	
    73	    def _select_model(self) -> None:
    74	        """Open a file dialog to select a .gguf model file.
    75	
    76	        Stores the full path as a custom property on the line edit
    77	        (accessible via ``getProperty("fullPath")``) while displaying
    78	        only the short filename in the UI.
    79	        """
    80	        file_path, _ = QFileDialog.getOpenFileName(
    81	            self,
    82	            "Select GGUF Model",
    83	            "",
    84	            "GGUF Files (*.gguf)",
    85	        )
    86	        if file_path:
    87	            self._model_path = file_path
    88	            self.model_path_edit.setProperty("fullPath", file_path)
    89	            self.model_path_edit.setText(file_path.rsplit("/", 1)[-1])
    90	            self._on_model_selection_changed()
    91	
    92	    def _select_mmproj(self) -> None:
    93	        """Open a file dialog to select a .gguf mmproj file.
    94	
    95	        Stores the full path as a custom property on the line edit
    96	        (accessible via ``getProperty("fullPath")``) while displaying
    97	        only the short filename in the UI.
    98	        """
    99	        file_path, _ = QFileDialog.getOpenFileName(
   100	            self,
   101	            "Select Multi-Modal Projector",
   102	            "",
   103	            "GGUF Files (*.gguf)",
   104	        )
   105	        if file_path:
   106	            self._mmproj_path = file_path
   107	            self.mmproj_path_edit.setProperty("fullPath", file_path)
   108	            self.mmproj_path_edit.setText(file_path.rsplit("/", 1)[-1])
   109	
   110	    def _on_model_selection_changed(self) -> None:
   111	        """Enable launch button when a model is selected, disable otherwise."""
   112	        has_model = bool(self.model_path_edit.property("fullPath"))
   113	        is_running = self._process.state() == QProcess.Running
   114	        self.launch_button.setEnabled(has_model and not is_running)
   115	
   116	    def _toggle_launch(self) -> None:
   117	        """Launch or stop the llama-server based on current process state."""
   118	        if self._process.state() == QProcess.Running:
   119	            self._stop_model()
   120	        else:
   121	            self._launch_model()
   122	
   123	    def _stop_model(self) -> None:
   124	        """Stop the llama-server gracefully.
   125	
   126	        Sends SIGTERM (like pressing Ctrl+C) so the server can shut down
   127	        cleanly. If it does not stop within 2 seconds, falls back to
   128	        SIGKILL.
   129	        """
   130	        self._process.terminate()
   131	        self.output_display.appendPlainText("Stopping server... (sent SIGTERM)")
   132	        QTimer.singleShot(2000, self._force_kill_if_needed)
   133	
   134	    def _force_kill_if_needed(self) -> None:
   135	        """Force kill the process if graceful termination did not work."""
   136	        if self._process.state() == QProcess.Running:
   137	            self.output_display.appendPlainText("Server didn't stop gracefully. Force killing...")
   138	            self._process.kill()
   139	
   140	    def _reset_launch_button(self) -> None:
   141	        """Reset the launch button to its default state."""
   142	        self.launch_button.setText("LAUNCH")
   143	        self._on_model_selection_changed()
   144	
   145	    def _launch_model(self) -> None:
   146	        """Launch the llama-server binary with current configuration.
   147	
   148	        Builds the command-line arguments from the UI fields and starts
   149	        ``llama-server`` via QProcess.  Live stdout/stderr output is
   150	        streamed into ``output_display``.
   151	        """
   152	        model_path = self.model_path_edit.property("fullPath")
   153	        if not model_path:
   154	            self.output_display.appendPlainText("Error: no model selected.")
   155	            return
   156	
   157	        temperature = self.temperature_spinbox.value()
   158	        top_p = self.top_p_spinbox.value()
   159	        top_k = self.top_k_spinbox.value()
   160	
   161	        mmproj_path = self.mmproj_path_edit.property("fullPath")
   162	        no_mmproj_offload = self.no_mmproj_offload_checkbox.isChecked()
   163	        api_key = self.api_key_line_edit.text() if self.api_key_line_edit.text() else "12345"
   164	
   165	        # Build command: llama-server --model ... --temp ... ...
   166	        cmd = [
   167	            "llama-server",
   168	            "--model",
   169	            model_path,
   170	            "--temp",
   171	            str(temperature),
   172	            "--top-p",
   173	            str(top_p),
   174	            "--top-k",
   175	            str(top_k),
   176	            "--api-key",
   177	            api_key,
   178	        ]
   179	
   180	        host = self.host_line_edit.text() or self._host
   181	        port_str = self.port_line_edit.text() or str(self._port)
   182	        try:
   183	            port = int(port_str)
   184	        except ValueError:
   185	            port = self._port
   186	
   187	        if mmproj_path:
   188	            cmd.extend(["--mmproj", mmproj_path])
   189	            if no_mmproj_offload:
   190	                cmd.append("--no-mmproj-offload")
   191	
   192	        cmd.extend(["--host", host, "--port", str(port)])
   193	
   194	        self.output_display.clear()
   195	        self.output_display.appendPlainText(f"Launching: {' '.join(cmd)}\n---\n")
   196	
   197	        # Use two-argument form: program + arguments list (args must NOT include the program)
   198	        self._process.start(cmd[0], cmd[1:])
   199	        self.launch_button.setText("STOP")
   200	
   201	        # Update web view to point to the server
   202	        server_url = f"http://{host}:{port}"
   203	        self.server_web_view.setUrl(server_url)
   204	
   205	    # ------------------------------------------------------------------
   206	    # QProcess output slots
   207	    # ------------------------------------------------------------------
   208	
   209	    def _on_stdout(self) -> None:
   210	        """Append stdout from the child process to the output display."""
   211	        data = self._process.readAllStandardOutput().data().decode("utf-8", errors="replace")
   212	        if data:
   213	            self.output_display.appendPlainText(data)
   214	
   215	    def _on_stderr(self) -> None:
   216	        """Append stderr from the child process to the output display."""
   217	        data = self._process.readAllStandardError().data().decode("utf-8", errors="replace")
   218	        if data:
   219	            self.output_display.appendPlainText(data)
   220	
   221	    def _on_error(self, error: QProcess.ProcessError) -> None:
   222	        """Called when the process encounters an error (e.g. not found)."""
   223	        msg = f"Error launching process: {error}"
   224	        self.output_display.appendPlainText(msg)
   225	        self._reset_launch_button()
   226	
   227	    def _on_finished(self, code: int, status: QProcess.ExitStatus) -> None:
   228	        """Called when the child process exits."""
   229	        if status == QProcess.ExitStatus.NormalExit:
   230	            self.output_display.appendPlainText(f"\n--- Process exited with code {code} ---")
   231	        else:
   232	            self.output_display.appendPlainText(f"\n--- Process terminated abnormally (code {code}) ---")
   233	        self._reset_launch_button()
   234	
   235	
   236	if __name__ == "__main__":
   237	    parser = argparse.ArgumentParser(description="Llama model launcher application.")
   238	    parser.add_argument("--host", default="127.0.0.1", help="Host address for the server (default: 127.0.0.1)")
   239	    parser.add_argument("--port", type=int, default=8080, help="Port for the server (default: 8080)")
   240	    args = parser.parse_args()
   241	
   242	    app = QApplication(sys.argv)
   243	    window = LlamaLaunchApp(host=args.host, port=args.port)
   244	    window.resize(800, 600)
   245	    window.show()
   246	    sys.exit(app.exec())

```
