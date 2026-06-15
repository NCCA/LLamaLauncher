## User

./main.py
js: [ToolsStore] Failed to fetch built-in tools: Error: File Not Found
Traceback (most recent call last):
  File "/Volumes/teaching/Code/LLamaLauncher/./main.py", line 247, in _toggle_launch
    self._launch_model()
    ~~~~~~~~~~~~~~~~~~^^
  File "/Volumes/teaching/Code/LLamaLauncher/./main.py", line 367, in _launch_model
    flash_attn = self.flash_attn_combobox.currentText()
                 ^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'LlamaLaunchApp' object has no attribute 'flash_attn_combobox'

## Assistant

<thinking>
Let me analyze this error. The issue is that `LlamaLaunchApp` doesn't have a `flash_attn_combobox` attribute when `_launch_model` tries to access it. Let me look at the main.py file to understand the structure and find where this combobox should be defined.

</thinking>

Let me look at the code to understand the issue.



**Tool Call: Read file `main.py`**
Status: Completed

```
SUCCESS: File outline retrieved. This file is too large to read all at once, so the outline below shows the file's structure with line numbers.

IMPORTANT: Do NOT retry this call without line numbers - you will get the same outline.
Instead, use the line numbers below to read specific sections by calling this tool again with start_line and end_line parameters.

# File outline for /Volumes/teaching/Code/LLamaLauncher/main.py

class LlamaLaunchApp [L21-499]
 def __init__ [L28-49]
 def _create_cache_dir [L55-63]
 def _create_persistent_profile [L65-89]
 def _init_web_view [L91-100]
 def _setup_ui [L102-111]
 def _setup_context_size_combo [L113-146]
 def _connect_signals [L152-159]
 def _select_model [L165-182]
 def _select_mmproj [L184-200]
 def _select_draft_model [L202-217]
 def _select_json_schema [L219-234]
 def _on_model_selection_changed [L236-240]
 def _toggle_launch [L242-247]
 def _stop_model [L249-258]
 def _force_kill_if_needed [L260-264]
 def _reset_launch_button [L266-269]
 def _launch_model [L271-437]
 def _on_stdout [L443-452]
 def _on_stderr [L454-463]
 def _check_and_refresh [L465-479]
 def _refresh_web_view [L481-485]
 def _on_error [L487-491]
 def _on_finished [L493-499]

Showing symbols 1-24 (total symbols: 24)


NEXT STEPS: To read a specific symbol's implementation, call read_file with the same path plus start_line and end_line from the outline above.
For example, to read a function shown as [L100-150], use start_line: 100 and end_line: 150.
```


## Assistant

<thinking>
Let me look at key sections of this file to understand the issue with `flash_attn_combobox`.

</thinking>

**Tool Call: Read file `main.py` (lines 102-160)**
Status: Completed

```LLamaLauncher/main.py
   102	    def _setup_ui(self) -> None:
   103	        """Load the main window UI from the .ui file.
   104	
   105	        All child widgets and layouts are auto-assigned as attributes
   106	        on this instance by their ``objectName`` so that the .ui file
   107	        controls which names are available.
   108	        """
   109	        ui_path = Path(__file__).resolve().parent / "ui" / "llama_launch.ui"
   110	        load_ui(ui_path, self)
   111	        self._setup_context_size_combo()
   112	
   113	    def _setup_context_size_combo(self) -> None:
   114	        """Populate the model context size combobox with options and tooltips.
   115	
   116	        Each item stores its numeric value (used as ``--ctx-size``) in the
   117	        user data role so the launch method can retrieve it later.
   118	        """
   119	        self.model_context_size.clear()
   120	
   121	        context_options = [
   122	            ("Auto (model default)", 0, "Recommended default; uses GGUF model context"),
   123	            ("2K", 2048, "Very small models / low memory"),
   124	            ("4K", 4096, "Basic chat, small coding tasks"),
   125	            ("8K", 8192, "General purpose"),
   126	            ("16K", 16384, "Better coding/chat history"),
   127	            ("32K", 32768, "Large files, coding assistants"),
   128	            ("64K", 65536, "Long documents, repo context"),
   129	            ("128K", 131072, "Modern long-context models"),
   130	        ]
   131	
   132	        for display_name, value, tooltip in context_options:
   133	            self.model_context_size.addItem(display_name, value)
   134	            index = self.model_context_size.count() - 1
   135	            self.model_context_size.setItemData(index, tooltip, Qt.ToolTipRole)
   136	
   137	        # Pre-select from CLI if provided, otherwise default to 16K
   138	        if self._ctx_size is not None:
   139	            target = self._ctx_size
   140	        else:
   141	            target = 16384  # 16K default
   142	
   143	        for i in range(self.model_context_size.count()):
   144	            if int(self.model_context_size.itemData(i, Qt.UserRole)) == target:
   145	                self.model_context_size.setCurrentIndex(i)
   146	                break
   147	
   148	    # ------------------------------------------------------------------
   149	    # Signal connections
   150	    # ------------------------------------------------------------------
   151	
   152	    def _connect_signals(self) -> None:
   153	        """Connect widget signals to their slot methods."""
   154	        self.select_model_button.clicked.connect(self._select_model)
   155	        self.select_mmproj_button.clicked.connect(self._select_mmproj)
   156	        self.select_draft_model_button.clicked.connect(self._select_draft_model)
   157	        self.select_json_schema_button.clicked.connect(self._select_json_schema)
   158	        self.model_path_edit.textChanged.connect(self._on_model_selection_changed)
   159	        self.launch_button.clicked.connect(self._toggle_launch)
   160	

```


## Assistant

<thinking>
Now let me look at the _launch_model method where the error occurs, specifically around line 367.

</thinking>

**Tool Call: Read file `main.py` (lines 271-400)**
Status: Completed

```LLamaLauncher/main.py
   271	    def _launch_model(self) -> None:
   272	        """Launch the llama-server binary with current configuration.
   273	
   274	        Builds the command-line arguments from the UI fields and starts
   275	        ``llama-server`` via QProcess.  Live stdout/stderr output is
   276	        streamed into ``output_display``.
   277	        """
   278	        model_path = self.model_path_edit.property("fullPath")
   279	        if not model_path:
   280	            self.output_display.appendPlainText("Error: no model selected.")
   281	            return
   282	
   283	        temperature = self.temperature_spinbox.value()
   284	        top_p = self.top_p_spinbox.value()
   285	        top_k = self.top_k_spinbox.value()
   286	        min_p = self.min_p_spinbox.value()
   287	        typical_p = self.typical_p_spinbox.value()
   288	        repeat_penalty = self.repeat_penalty_spinbox.value()
   289	        repeat_last_n = self.repeat_last_n_spinbox.value()
   290	        presence_penalty = self.presence_penalty_spinbox.value()
   291	        frequency_penalty = self.frequency_penalty_spinbox.value()
   292	
   293	        mirostat = self.mirostat_spinbox.value()
   294	        mirostat_lr = self.mirostat_lr_spinbox.value()
   295	        mirostat_ent = self.mirostat_ent_spinbox.value()
   296	
   297	        # Performance parameters
   298	        gpu_layers = self.gpu_layers_spinbox.value()
   299	        threads = self.threads_spinbox.value()
   300	        threads_batch = self.threads_batch_spinbox.value()
   301	        batch_size = self.batch_size_spinbox.value()
   302	        ubatch_size = self.ubatch_size_spinbox.value()
   303	        n_predict = self.n_predict_spinbox.value()
   304	        parallel = self.parallel_spinbox.value()
   305	        cache_type_k = self.cache_type_k_combobox.currentText()
   306	        cache_type_v = self.cache_type_v_combobox.currentText()
   307	
   308	        # Advanced Generation parameters
   309	        spec_draft_n_max = self.spec_draft_n_max_spinbox.value()
   310	        seed = self.seed_spinbox.value()
   311	        rope_scaling = self.rope_scaling_combobox.currentText()
   312	        rope_freq_base = self.rope_freq_base_spinbox.value()
   313	        rope_freq_scale = self.rope_freq_scale_spinbox.value()
   314	
   315	        mmproj_path = self.mmproj_path_edit.property("fullPath")
   316	        no_mmproj_offload = self.no_mmproj_offload_checkbox.isChecked()
   317	        api_key = self.api_key_line_edit.text() if self.api_key_line_edit.text() else "12345"
   318	
   319	        # Build command: llama-server --model ... (conditional sampling params) ...
   320	        cmd = [
   321	            "llama-server",
   322	            "--model",
   323	            model_path,
   324	            "--api-key",
   325	            api_key,
   326	        ]
   327	
   328	        if self.enable_temperature_checkbox.isChecked():
   329	            cmd.extend(["--temp", str(temperature)])
   330	        if self.enable_top_p_checkbox.isChecked():
   331	            cmd.extend(["--top-p", str(top_p)])
   332	        if self.enable_top_k_checkbox.isChecked():
   333	            cmd.extend(["--top-k", str(top_k)])
   334	        if self.enable_min_p_checkbox.isChecked():
   335	            cmd.extend(["--min-p", str(min_p)])
   336	        if self.enable_typical_p_checkbox.isChecked():
   337	            cmd.extend(["--typical-p", str(typical_p)])
   338	        if self.enable_repeat_penalty_checkbox.isChecked():
   339	            cmd.extend(["--repeat-penalty", str(repeat_penalty)])
   340	        if self.enable_repeat_last_n_checkbox.isChecked():
   341	            cmd.extend(["--repeat-last-n", str(repeat_last_n)])
   342	        if self.enable_presence_penalty_checkbox.isChecked():
   343	            cmd.extend(["--presence-penalty", str(presence_penalty)])
   344	        if self.enable_frequency_penalty_checkbox.isChecked():
   345	            cmd.extend(["--frequency-penalty", str(frequency_penalty)])
   346	        if self.enable_mirostat_checkbox.isChecked():
   347	            cmd.extend(["--mirostat", str(mirostat)])
   348	        if self.enable_mirostat_lr_checkbox.isChecked():
   349	            cmd.extend(["--mirostat-lr", str(mirostat_lr)])
   350	        if self.enable_mirostat_ent_checkbox.isChecked():
   351	            cmd.extend(["--mirostat-ent", str(mirostat_ent)])
   352	
   353	        # Performance parameters
   354	        if self.enable_gpu_layers_checkbox.isChecked():
   355	            cmd.extend(["--n-gpu-layers", str(gpu_layers)])
   356	        if self.enable_threads_checkbox.isChecked():
   357	            cmd.extend(["--threads", str(threads)])
   358	        if self.enable_threads_batch_checkbox.isChecked():
   359	            cmd.extend(["--threads-batch", str(threads_batch)])
   360	        if self.enable_batch_size_checkbox.isChecked():
   361	            cmd.extend(["--batch-size", str(batch_size)])
   362	        if self.enable_ubatch_size_checkbox.isChecked():
   363	            cmd.extend(["--ubatch-size", str(ubatch_size)])
   364	        if self.enable_n_predict_checkbox.isChecked():
   365	            cmd.extend(["--n-predict", str(n_predict)])
   366	        # Flash Attention: always pass the selected value (default auto)
   367	        flash_attn = self.flash_attn_combobox.currentText()
   368	        cmd.extend(["--flash-attn", flash_attn])
   369	        if self.enable_cache_type_k_checkbox.isChecked():
   370	            cmd.extend(["--cache-type-k", cache_type_k])
   371	        if self.enable_cache_type_v_checkbox.isChecked():
   372	            cmd.extend(["--cache-type-v", cache_type_v])
   373	        if self.enable_mmap_checkbox.isChecked():
   374	            cmd.append("--mmap")
   375	        if self.enable_mlock_checkbox.isChecked():
   376	            cmd.append("--mlock")
   377	        if self.enable_cont_batching_checkbox.isChecked():
   378	            cmd.append("--cont-batching")
   379	        if self.enable_parallel_checkbox.isChecked():
   380	            cmd.extend(["--parallel", str(parallel)])
   381	
   382	        # Advanced Generation parameters
   383	        draft_model_path = self.draft_model_line_edit.property("fullPath")
   384	        if self.enable_draft_model_checkbox.isChecked() and draft_model_path:
   385	            cmd.extend(["--draft-model", draft_model_path])
   386	        if self.enable_spec_draft_n_max_checkbox.isChecked():
   387	            cmd.extend(["--spec-draft-n-max", str(spec_draft_n_max)])
   388	        if self.enable_seed_checkbox.isChecked():
   389	            cmd.extend(["--seed", str(seed)])
   390	        grammar_text = self.grammar_line_edit.text().strip()
   391	        if self.enable_grammar_checkbox.isChecked() and grammar_text:
   392	            cmd.extend(["--grammar", grammar_text])
   393	        json_schema_path = self.json_schema_line_edit.property("fullPath")
   394	        if self.enable_json_schema_checkbox.isChecked() and json_schema_path:
   395	            cmd.extend(["--json-schema", json_schema_path])
   396	        if self.enable_rope_scaling_checkbox.isChecked():
   397	            cmd.extend(["--rope-scaling", rope_scaling])
   398	        if self.enable_rope_freq_base_checkbox.isChecked():
   399	            cmd.extend(["--rope-freq-base", str(rope_freq_base)])
   400	        if self.enable_rope_freq_scale_checkbox.isChecked():

```


## Assistant

<thinking>
The error is clear: `self.flash_attn_combobox` doesn't exist as an attribute on the `LlamaLaunchApp` instance. This is a Qt UI widget that should be loaded from the `.ui` file via `load_ui()`, but either:

1. The `.ui` file doesn't have a widget with `objectName="flash_attn_combobox"`
2. The widget was renamed or removed from the UI

Let me check the UI file to see if this widget exists there.

</thinking>

Now I need to check the UI file to see if the `flash_attn_combobox` widget exists there.



**Tool Call: Search files for regex `flash_attn_combobox`**
Status: Completed

No matches found

## Assistant

<thinking>
The `flash_attn_combobox` widget doesn't exist in the UI file. This means either:

1. The widget was removed from the UI but is still referenced in the code
2. The widget needs to be added to the UI file

Let me check what other flash-attn related patterns exist in the UI and codebase to understand the context better.

</thinking>

**Tool Call: Search files for regex `flash.attn|flash_attn`**
Status: Completed

Showing matches 1-20 (there were more matches found; use offset: 20 to see next page):

## Matches in LLamaLauncher/.worktrees/advanced-generation/AgentChats/AgentChat24.md

### ## Assistant › L119-129
```
   100	    | `-c` / `--ctx-size` | Maximum context window size | `8192–131072` depending on model |
   101	
   102	    | `--n-predict` | Maximum tokens generated | `2048–8192` |
   103	
   104	  - [ ] Enable attention optimisations
   105	
   106	    | Parameter | Purpose | Typical Value |
   107	
   108	    |---|---|---|
   109	
   110	    | `--flash-attn` | Enable Flash Attention to reduce memory use and improve speed | `on` |
```

113 lines remaining in ancestor node. Read the file to see all.

### # Files: › ## Assistant › L2210-2212
```
- `--flash-attn`: Enable Flash Attention (checkbox/bool)

**KV Cache:**
```

### # Files: › ## Assistant › L2409-2410
```
5. Attention Optimizations (flash_attn)
6. KV Cache (cache_type_k, cache_type_v)
```

### # Files: › ## Assistant › L3369-3379
```
       </item>
       <item>
        <widget class="QGroupBox" name="flash_attn_group">
         <property name="title">
          <string>Attention Optimizations</string>
         </property>
         <layout class="QVBoxLayout" name="flash_attn_layout">
          <item>
           <widget class="QCheckBox" name="enable_flash_attn_checkbox">
            <property name="toolTip">
             <string
```

### # Files: › ## Assistant › L4508-4513
```
        if self.enable_n_predict_checkbox.isChecked():
            cmd.extend(["--n-predict", str(n_predict)])
        if self.enable_flash_attn_checkbox.isChecked():
            cmd.append("--flash-attn")
        if self.enable_cache_type_k_checkbox.isChecked():
            cmd.extend(["--cache-type-k", cache_type_k])
```

### # Files: › ## Summary › ### UI Changes (`ui/llama_launch.ui`) › L4823-4833
```
| Group | Parameters |
|-------|-----------|
| **GPU Layer Offload** | `--n-gpu-layers` (QSpinBox, default 99) |
| **CPU Threading** | `--threads`, `--threads-batch` (QSpinBoxes, default 0/auto) |
| **Batching** | `--batch-size`, `--ubatch-size` (QSpinBoxes, default 512) |
| **Generation** | `--n-predict` (QSpinBox, default 2048) |
| **Attention Optimizations** | `--flash-attn` (QCheckBox) |
| **KV Cache** | `--cache-type-k`, `--cache-type-v` (QComboBoxes: f16/q8_0/q4_0) |
| **Memory Handling** | `--mmap`, `--mlock` (QCheckBoxes, mmap checked by default) |
| **Server Batching** | `--cont-batching`, `--parallel`, `--defrag-thold` |

```

### # Files: › ## Assistant › L5471-5481
```
   934	       </item>
   935	       <item>
   936	        <widget class="QGroupBox" name="flash_attn_group">
   937	         <property name="title">
   938	          <string>Attention Optimizations</string>
   939	         </property>
   940	         <layout class="QVBoxLayout" name="flash_attn_layout">
   941	          <item>
   942	           <widget class="QCheckBox" name="enable_flash_attn_checkbox">
   943	            <property name="toolTip">
   944	             <string
```

### # Files: › ## Assistant › L6623-6633
```
   934	       </item>
   935	       <item>
   936	        <widget class="QGroupBox" name="flash_attn_group">
   937	         <property name="title">
   938	          <string>Attention Optimizations</string>
   939	         </property>
   940	         <layout class="QVBoxLayout" name="flash_attn_layout">
   941	          <item>
   942	           <widget class="QCheckBox" name="enable_flash_attn_checkbox">
   943	            <property name="toolTip">
   944	             <string
```

### # Files: › ## Assistant › L8865-8875
```
           </item>
           <item>
            <widget class="QGroupBox" name="flash_attn_group">
             <property name="title">
              <string>Attention Optimizations</string>
             </property>
             <layout class="QVBoxLayout" name="flash_attn_layout">
              <item>
               <widget class="QCheckBox" name="enable_flash_attn_checkbox">
                <property name="toolTip">
                 <string
```

## Matches in LLamaLauncher/.worktrees/advanced-generation/AgentChats/AgentChat25.md

### # Files: › ## Assistant › L2532-2542
```
   885	           </item>
   886	           <item>
   887	            <widget class="QGroupBox" name="flash_attn_group">
   888	             <property name="title">
   889	              <string>Attention Optimizations</string>
   890	             </property>
   891	             <layout class="QVBoxLayout" name="flash_attn_layout">
   892	              <item>
   893	               <widget class="QCheckBox" name="enable_flash_attn_checkbox">
   894	                <property name="toolTip">
   895	                 <string
```

### # Files: › ## Assistant › L4249-4259
```
   885	           </item>
   886	           <item>
   887	            <widget class="QGroupBox" name="flash_attn_group">
   888	             <property name="title">
   889	              <string>Attention Optimizations</string>
   890	             </property>
   891	             <layout class="QVBoxLayout" name="flash_attn_layout">
   892	              <item>
   893	               <widget class="QCheckBox" name="enable_flash_attn_checkbox">
   894	                <property name="toolTip">
   895	                 <string
```

### # Files: › ## Assistant › L5930-5940
```
           </item>
           <item>
            <widget class="QGroupBox" name="flash_attn_group">
             <property name="title">
              <string>Attention Optimizations</string>
             </property>
             <layout class="QVBoxLayout" name="flash_attn_layout">
              <item>
               <widget class="QCheckBox" name="enable_flash_attn_checkbox">
                <property name="toolTip">
                 <string
```

### # Files: › ## Assistant › L6646-6656
```
   904	           </item>
   905	           <item>
   906	            <widget class="QGroupBox" name="flash_attn_group">
   907	             <property name="title">
   908	              <string>Attention Optimizations</string>
   909	             </property>
   910	             <layout class="QVBoxLayout" name="flash_attn_layout">
   911	              <item>
   912	               <widget class="QCheckBox" name="enable_flash_attn_checkbox">
   913	                <property name="toolTip">
   914	                 <string
```

### # Files: › ## Assistant › L7837-7847
```
           </item>
           <item>
            <widget class="QGroupBox" name="flash_attn_group">
             <property name="title">
              <string>Attention Optimizations</string>
             </property>
             <layout class="QVBoxLayout" name="flash_attn_layout">
              <item>
               <widget class="QCheckBox" name="enable_flash_attn_checkbox">
                <property name="toolTip">
                 <string
```

### # Files: › ## Assistant › L9208-9218
```
           </item>
           <item>
            <widget class="QGroupBox" name="flash_attn_group">
             <property name="title">
              <string>Attention Optimizations</string>
             </property>
             <layout class="QVBoxLayout" name="flash_attn_layout">
              <item>
               <widget class="QCheckBox" name="enable_flash_attn_checkbox">
                <property name="toolTip">
                 <string
```

### # Files: › ## Assistant › L10473-10483
```
           </item>
           <item>
            <widget class="QGroupBox" name="flash_attn_group">
             <property name="title">
              <string>Attention Optimizations</string>
             </property>
             <layout class="QVBoxLayout" name="flash_attn_layout">
              <item>
               <widget class="QCheckBox" name="enable_flash_attn_checkbox">
                <property name="toolTip">
                 <string
```

### # Files: › ## Assistant › L11071-11081
```
   919	           </item>
   920	           <item>
   921	            <widget class="QGroupBox" name="flash_attn_group">
   922	             <property name="title">
   923	              <string>Attention Optimizations</string>
   924	             </property>
   925	             <layout class="QVBoxLayout" name="flash_attn_layout">
   926	              <item>
   927	               <widget class="QCheckBox" name="enable_flash_attn_checkbox">
   928	                <property name="toolTip">
   929	                 <string
```

### # Files: › ## Assistant › L12525-12535
```
           </item>
           <item>
            <widget class="QGroupBox" name="flash_attn_group">
             <property name="title">
              <string>Attention Optimizations</string>
             </property>
             <layout class="QVBoxLayout" name="flash_attn_layout">
              <item>
               <widget class="QCheckBox" name="enable_flash_attn_checkbox">
                <property name="toolTip">
                 <string
```

## Matches in LLamaLauncher/.worktrees/advanced-generation/AgentChats/WebChatAboutParams.md

### L1-5
```
I have started you with these parameters what do they mean  llama-server --api-key 12345\
    -m ~/teaching/AI_Models/Qwen3.6-35B-A3B-UD-Q4_K_XL.gguf \
    --jinja -ngl 999 -np 1 --flash-attn on  -fit off  --no-mmap  --jinja --ctx-size 32768 \
    --temp 0.7 --min-p 0.0 --top-p 0.80 --top-k 20 --repeat-penalty 1.05 --spec-type draft-mtp \
    --spec-draft-n-max 4
```

### ## Performance & Hardware Optimization › L19-26
```
    --jinja: Enables Jinja templating for chat prompts. This allows you to use Jinja2 syntax in your prompts for more flexible and structured message formatting (e.g., handling system/user/assistant roles dynamically).
    -ngl 999: Sets the number of GPU layers to offload. 999 is a common trick to offload all possible layers to the GPU (the actual limit depends on your VRAM). This maximizes GPU usage for faster inference.
    -np 1: Sets the number of parallel requests (concurrent connections) to 1. This limits the server to handling one request at a time, which can help with stability but reduces throughput.
    --flash-attn on: Enables Flash Attention, an optimized attention mechanism that significantly speeds up inference and reduces memory usage, especially for long contexts.
    -fit off: Disables Fit (a feature in some llama.cpp versions for optimizing context window handling). Turning it off may prevent unexpected behavior or bugs in certain configurations.
    --no-mmap: Disables memory-mapped file I/O. This forces the model to be loaded entirely into RAM/VRAM at startup. It can improve performance and stability but uses more memory upfront.

## Context & Generation Parameters
```


## Assistant

<thinking>
I can see from the grep results that in the worktree branch (`advanced-generation`), `flash-attn` was implemented as a simple **QCheckBox** (`enable_flash_attn_checkbox`), not a QComboBox. The current main.py code is trying to use `self.flash_attn_combobox` which doesn't exist.

Let me look at the UI file to see what flash_attn widgets actually exist there.

</thinking>

I can see the issue now. Let me check what flash-attn related widgets actually exist in the current UI file.



**Tool Call: Search files for regex `flash.attn|flash_attn`**
Status: Completed

Found 1 matches:

## Matches in LLamaLauncher/ui/llama_launch.ui

### ui › widget › layout › item › widget › widget › layout › item › widget › widget › layout › item › widget › widget › layout › item › widget › L923-939
```
           <item>
            <widget class="QGroupBox" name="flash_attn_group">
             <property name="title">
              <string>Attention Optimizations</string>
             </property>
             <layout class="QVBoxLayout" name="flash_attn_layout">
              <item>
               <widget class="QCheckBox" name="enable_flash_attn_checkbox">
                <property name="toolTip">
                 <string
                                                                                    >Enable Flash Attention to reduce memory use and improve speed.
Requires compatible GPU.</string>
                </property>
                <property name="text">
                 <string>Flash Attention</string>
                </property>
               </widget>
```

4 lines remaining in ancestor node. Read the file to see all.


## Assistant

<thinking>
The UI file has `enable_flash_attn_checkbox` (a QCheckBox), but the code at line 367 is trying to use `self.flash_attn_combobox.currentText()` which doesn't exist. 

Looking at the llama-server CLI, `--flash-attn` can take values like "on", "off", "auto", etc. The code wants to pass a specific value from a combobox, but the UI only has a checkbox.

I need to either:
1. Add a combobox widget to the UI file for flash attention options
2. Change the code to work with the existing checkbox

Given that the code comment says "always pass the selected value (default auto)", it seems like the intent was to have a combobox with options like "on", "off", "auto". 

Let me look at what the llama-server actually expects for --flash-attn. Based on the grep results, I see examples like `--flash-attn on`. Let me check the UI file more carefully to see the full structure of the flash_attn_group.

I should add a QComboBox to the UI file for flash attention options. Let me read the relevant section of the UI file first.

</thinking>

Now I understand the issue. The UI file has a `enable_flash_attn_checkbox` (QCheckBox), but the code at line 367 references `self.flash_attn_combobox` which doesn't exist. The intent was to have a combobox with options like "on", "off", "auto" for flash attention.

Let me read the full flash_attn_group section from the UI file to understand where to add the combobox.



**Tool Call: Read file `ui/llama_launch.ui` (lines 920-980)**
Status: Completed

```LLamaLauncher/ui/llama_launch.ui
   920	             </layout>
   921	            </widget>
   922	           </item>
   923	           <item>
   924	            <widget class="QGroupBox" name="flash_attn_group">
   925	             <property name="title">
   926	              <string>Attention Optimizations</string>
   927	             </property>
   928	             <layout class="QVBoxLayout" name="flash_attn_layout">
   929	              <item>
   930	               <widget class="QCheckBox" name="enable_flash_attn_checkbox">
   931	                <property name="toolTip">
   932	                 <string
   933	                                                                                    >Enable Flash Attention to reduce memory use and improve speed.
   934	Requires compatible GPU.</string>
   935	                </property>
   936	                <property name="text">
   937	                 <string>Flash Attention</string>
   938	                </property>
   939	               </widget>
   940	              </item>
   941	             </layout>
   942	            </widget>
   943	           </item>
   944	           <item>
   945	            <widget class="QGroupBox" name="kv_cache_group">
   946	             <property name="title">
   947	              <string>KV Cache</string>
   948	             </property>
   949	             <layout class="QVBoxLayout" name="kv_cache_layout">
   950	              <item>
   951	               <layout class="QHBoxLayout" name="cache_type_k_hbox">
   952	                <item>
   953	                 <widget class="QCheckBox" name="enable_cache_type_k_checkbox">
   954	                  <property name="toolTip">
   955	                   <string>KV cache key precision.
   956	f16 = highest quality, q8_0/q4_0 = lower memory use.</string>
   957	                  </property>
   958	                  <property name="text">
   959	                   <string>Cache Type K</string>
   960	                  </property>
   961	                 </widget>
   962	                </item>
   963	                <item>
   964	                 <widget class="QComboBox" name="cache_type_k_combobox">
   965	                  <property name="toolTip">
   966	                   <string>KV cache key data type precision.
   967	f16 = full precision, q8_0/q4_0 = quantized.</string>
   968	                  </property>
   969	                  <item>
   970	                   <property name="text">
   971	                    <string>f16</string>
   972	                   </property>
   973	                  </item>
   974	                  <item>
   975	                   <property name="text">
   976	                    <string>q8_0</string>
   977	                   </property>
   978	                  </item>
   979	                  <item>
   980	                   <property name="text">

```


## Assistant

<thinking>
The user's code is broken because `self.flash_attn_combobox` doesn't exist. I need to add a QComboBox widget to the UI file for flash attention options. Let me read more of the UI file to understand the structure better and find the right place to add the combobox.

</thinking>

Let me read more of the UI file to see the complete structure of the Attention Optimizations group and KV Cache section.



**Tool Call: Read file `ui/llama_launch.ui` (lines 910-1020)**
Status: Completed

```LLamaLauncher/ui/llama_launch.ui
   910	                  <property name="maximum">
   911	                   <number>65536</number>
   912	                  </property>
   913	                  <property name="value">
   914	                   <number>2048</number>
   915	                  </property>
   916	                 </widget>
   917	                </item>
   918	               </layout>
   919	              </item>
   920	             </layout>
   921	            </widget>
   922	           </item>
   923	           <item>
   924	            <widget class="QGroupBox" name="flash_attn_group">
   925	             <property name="title">
   926	              <string>Attention Optimizations</string>
   927	             </property>
   928	             <layout class="QVBoxLayout" name="flash_attn_layout">
   929	              <item>
   930	               <widget class="QCheckBox" name="enable_flash_attn_checkbox">
   931	                <property name="toolTip">
   932	                 <string
   933	                                                                                    >Enable Flash Attention to reduce memory use and improve speed.
   934	Requires compatible GPU.</string>
   935	                </property>
   936	                <property name="text">
   937	                 <string>Flash Attention</string>
   938	                </property>
   939	               </widget>
   940	              </item>
   941	             </layout>
   942	            </widget>
   943	           </item>
   944	           <item>
   945	            <widget class="QGroupBox" name="kv_cache_group">
   946	             <property name="title">
   947	              <string>KV Cache</string>
   948	             </property>
   949	             <layout class="QVBoxLayout" name="kv_cache_layout">
   950	              <item>
   951	               <layout class="QHBoxLayout" name="cache_type_k_hbox">
   952	                <item>
   953	                 <widget class="QCheckBox" name="enable_cache_type_k_checkbox">
   954	                  <property name="toolTip">
   955	                   <string>KV cache key precision.
   956	f16 = highest quality, q8_0/q4_0 = lower memory use.</string>
   957	                  </property>
   958	                  <property name="text">
   959	                   <string>Cache Type K</string>
   960	                  </property>
   961	                 </widget>
   962	                </item>
   963	                <item>
   964	                 <widget class="QComboBox" name="cache_type_k_combobox">
   965	                  <property name="toolTip">
   966	                   <string>KV cache key data type precision.
   967	f16 = full precision, q8_0/q4_0 = quantized.</string>
   968	                  </property>
   969	                  <item>
   970	                   <property name="text">
   971	                    <string>f16</string>
   972	                   </property>
   973	                  </item>
   974	                  <item>
   975	                   <property name="text">
   976	                    <string>q8_0</string>
   977	                   </property>
   978	                  </item>
   979	                  <item>
   980	                   <property name="text">
   981	                    <string>q4_0</string>
   982	                   </property>
   983	                  </item>
   984	                 </widget>
   985	                </item>
   986	               </layout>
   987	              </item>
   988	              <item>
   989	               <layout class="QHBoxLayout" name="cache_type_v_hbox">
   990	                <item>
   991	                 <widget class="QCheckBox" name="enable_cache_type_v_checkbox">
   992	                  <property name="toolTip">
   993	                   <string>KV cache value precision.
   994	f16 = highest quality, q8_0/q4_0 = lower memory use.</string>
   995	                  </property>
   996	                  <property name="text">
   997	                   <string>Cache Type V</string>
   998	                  </property>
   999	                 </widget>
  1000	                </item>
  1001	                <item>
  1002	                 <widget class="QComboBox" name="cache_type_v_combobox">
  1003	                  <property name="toolTip">
  1004	                   <string>KV cache value data type precision.
  1005	f16 = full precision, q8_0/q4_0 = quantized.</string>
  1006	                  </property>
  1007	                  <item>
  1008	                   <property name="text">
  1009	                    <string>f16</string>
  1010	                   </property>
  1011	                  </item>
  1012	                  <item>
  1013	                   <property name="text">
  1014	                    <string>q8_0</string>
  1015	                   </property>
  1016	                  </item>
  1017	                  <item>
  1018	                   <property name="text">
  1019	                    <string>q4_0</string>
  1020	                   </property>

```


## Assistant

<thinking>
Now I can see the structure. The "Attention Optimizations" group only has a checkbox for flash attention, but the code wants a combobox. I need to add a QComboBox widget to the UI file within the flash_attn_group, and then update the main.py code to use it properly.

Let me look at how the cache_type_k_combobox is structured in the UI to follow the same pattern.

</thinking>

Now let me look at how the cache_type_k_combobox is structured in the UI so I can follow the same pattern for flash_attn_combobox.



**Tool Call: Read file `ui/llama_launch.ui` (lines 946-988)**
Status: Completed

```LLamaLauncher/ui/llama_launch.ui
   946	             <property name="title">
   947	              <string>KV Cache</string>
   948	             </property>
   949	             <layout class="QVBoxLayout" name="kv_cache_layout">
   950	              <item>
   951	               <layout class="QHBoxLayout" name="cache_type_k_hbox">
   952	                <item>
   953	                 <widget class="QCheckBox" name="enable_cache_type_k_checkbox">
   954	                  <property name="toolTip">
   955	                   <string>KV cache key precision.
   956	f16 = highest quality, q8_0/q4_0 = lower memory use.</string>
   957	                  </property>
   958	                  <property name="text">
   959	                   <string>Cache Type K</string>
   960	                  </property>
   961	                 </widget>
   962	                </item>
   963	                <item>
   964	                 <widget class="QComboBox" name="cache_type_k_combobox">
   965	                  <property name="toolTip">
   966	                   <string>KV cache key data type precision.
   967	f16 = full precision, q8_0/q4_0 = quantized.</string>
   968	                  </property>
   969	                  <item>
   970	                   <property name="text">
   971	                    <string>f16</string>
   972	                   </property>
   973	                  </item>
   974	                  <item>
   975	                   <property name="text">
   976	                    <string>q8_0</string>
   977	                   </property>
   978	                  </item>
   979	                  <item>
   980	                   <property name="text">
   981	                    <string>q4_0</string>
   982	                   </property>
   983	                  </item>
   984	                 </widget>
   985	                </item>
   986	               </layout>
   987	              </item>
   988	              <item>

```


## Assistant

<thinking>
The user is experiencing an error where `self.flash_attn_combobox` doesn't exist in the `LlamaLaunchApp` class. The UI file has a checkbox (`enable_flash_attn_checkbox`) but not a combobox for flash attention options.

I need to:
1. Add a QComboBox widget named `flash_attn_combobox` to the UI file within the "Attention Optimizations" group
2. This combobox should have options like "on", "off", "auto" (based on llama-server CLI)

Let me look at more of the UI structure to understand how to properly add this widget. The grep output was truncated and hard to read. Let me fetch more context from the worktree session that discussed this feature.

</thinking>

Let me get more details about the intended flash_attn_combobox design from the worktree session where this feature was discussed.



**Tool Call: Search files for regex `flash.attn.*QComboBox|flash_attn.*QComboBox`**
Status: Completed

No matches found

## Assistant

<thinking>
The user is getting an error because `self.flash_attn_combobox` doesn't exist. The UI file has a checkbox (`enable_flash_attn_checkbox`) but the code references a combobox that doesn't exist.

Looking at the code on line 367:
```python
flash_attn = self.flash_attn_combobox.currentText()
cmd.extend(["--flash-attn", flash_attn])
```

This always passes the selected value. The comment says "always pass the selected value (default auto)".

Looking at llama-server/llama.cpp documentation, `--flash-attn` takes values like "on", "off", "auto". 

I need to add a QComboBox widget named `flash_attn_combobox` to the UI file within the "Attention Optimizations" group. Let me look at the structure of the cache_type_k_combobox in the UI file to understand the pattern.

From the grep results, I can see the cache_type_k_combobox has items like f16, q8_0, q4_0. The flash_attn_combobox should have items like "on", "off", "auto".

Let me read more of the UI file to get the exact XML structure of a combobox, then add the flash_attn_combobox widget.

</thinking>

The user is getting an error because `self.flash_attn_combobox` doesn't exist. The code on line 367 references a combobox that was never added to the UI file. I need to add a QComboBox widget named `flash_attn_combobox` to the "Attention Optimizations" group in the UI file.

Let me first get a clear view of the exact XML structure around the flash attention section and how similar comboboxes are structured.



**Tool Call: Search files for regex `cache_type_k_combobox`**
Status: Completed

Found 1 matches:

## Matches in LLamaLauncher/ui/llama_launch.ui

### ui › widget › layout › item › widget › widget › layout › item › widget › widget › layout › item › widget › widget › layout › item › widget › layout › item › layout › item › widget › L963-973
```
                <item>
                 <widget class="QComboBox" name="cache_type_k_combobox">
                  <property name="toolTip">
                   <string>KV cache key data type precision.
f16 = full precision, q8_0/q4_0 = quantized.</string>
                  </property>
                  <item>
                   <property name="text">
                    <string>f16</string>
                   </property>
                  </item>
```

12 lines remaining in ancestor node. Read the file to see all.


## Assistant

<thinking>
The user is experiencing an AttributeError because `self.flash_attn_combobox` doesn't exist on the `LlamaLaunchApp` instance. The UI file has a checkbox (`enable_flash_attn_checkbox`) but the code at line 367 references a combobox that was never added to the UI file.

I need to:
1. Add a QComboBox widget named `flash_attn_combobox` to the "Attention Optimizations" group in the UI file
2. The combobox should have options like "on", "off", "auto" based on what llama-server expects for --flash-attn

Let me read more of the UI file to understand the exact XML structure I need to add.

</thinking>

I can see the issue now. The code at line 367 references `self.flash_attn_combobox`, but the UI file only has a checkbox (`enable_flash_attn_checkbox`) in the "Attention Optimizations" group - no combobox was ever added.

Let me read more of the cache_type_k_combobox structure to understand the exact XML format, then add the missing flash_attn_combobox widget.



**Tool Call: Read file `ui/llama_launch.ui` (lines 963-1000)**
Status: Completed

```LLamaLauncher/ui/llama_launch.ui
   963	                <item>
   964	                 <widget class="QComboBox" name="cache_type_k_combobox">
   965	                  <property name="toolTip">
   966	                   <string>KV cache key data type precision.
   967	f16 = full precision, q8_0/q4_0 = quantized.</string>
   968	                  </property>
   969	                  <item>
   970	                   <property name="text">
   971	                    <string>f16</string>
   972	                   </property>
   973	                  </item>
   974	                  <item>
   975	                   <property name="text">
   976	                    <string>q8_0</string>
   977	                   </property>
   978	                  </item>
   979	                  <item>
   980	                   <property name="text">
   981	                    <string>q4_0</string>
   982	                   </property>
   983	                  </item>
   984	                 </widget>
   985	                </item>
   986	               </layout>
   987	              </item>
   988	              <item>
   989	               <layout class="QHBoxLayout" name="cache_type_v_hbox">
   990	                <item>
   991	                 <widget class="QCheckBox" name="enable_cache_type_v_checkbox">
   992	                  <property name="toolTip">
   993	                   <string>KV cache value precision.
   994	f16 = highest quality, q8_0/q4_0 = lower memory use.</string>
   995	                  </property>
   996	                  <property name="text">
   997	                   <string>Cache Type V</string>
   998	                  </property>
   999	                 </widget>
  1000	                </item>

```


## Assistant

<thinking>
Now I understand the issue. The code at line 367 references `self.flash_attn_combobox`, but this widget doesn't exist in the UI file. The UI file only has a checkbox (`enable_flash_attn_checkbox`) in the "Attention Optimizations" group.

I need to:
1. Add a QComboBox widget named `flash_attn_combobox` to the "Attention Optimizations" group in the UI file
2. The combobox should have options like "on", "off", "auto" based on what llama-server expects for --flash-attn

Let me read more of the UI file to understand the exact structure of the flash_attn_group so I can add the combobox in the right place.

</thinking>

Now I understand the issue clearly. The code at line 367 references `self.flash_attn_combobox`, but this widget doesn't exist in the UI file. The UI file only has a checkbox (`enable_flash_attn_checkbox`) in the "Attention Optimizations" group.

I need to add a QComboBox widget named `flash_attn_combobox` to the "Attention Optimizations" group in the UI file. Let me first read more of the flash_attn_group structure to understand exactly where to insert it.



**Tool Call: Read file `ui/llama_launch.ui` (lines 920-945)**
Status: Completed

```LLamaLauncher/ui/llama_launch.ui
   920	             </layout>
   921	            </widget>
   922	           </item>
   923	           <item>
   924	            <widget class="QGroupBox" name="flash_attn_group">
   925	             <property name="title">
   926	              <string>Attention Optimizations</string>
   927	             </property>
   928	             <layout class="QVBoxLayout" name="flash_attn_layout">
   929	              <item>
   930	               <widget class="QCheckBox" name="enable_flash_attn_checkbox">
   931	                <property name="toolTip">
   932	                 <string
   933	                                                                                    >Enable Flash Attention to reduce memory use and improve speed.
   934	Requires compatible GPU.</string>
   935	                </property>
   936	                <property name="text">
   937	                 <string>Flash Attention</string>
   938	                </property>
   939	               </widget>
   940	              </item>
   941	             </layout>
   942	            </widget>
   943	           </item>
   944	           <item>
   945	            <widget class="QGroupBox" name="kv_cache_group">

```


## Assistant

<thinking>
Now I understand the issue. The code at line 367 references `self.flash_attn_combobox`, but this widget doesn't exist in the UI file. The UI file only has a checkbox (`enable_flash_attn_checkbox`) in the "Attention Optimizations" group.

I need to:
1. Add a QComboBox widget named `flash_attn_combobox` to the "Attention Optimizations" group in the UI file
2. The combobox should have options like "on", "off", "auto" based on what llama-server expects for --flash-attn

Let me add the flash_attn_combobox widget to the UI file after the checkbox. I'll follow the same pattern as the cache_type_k_combobox.

</thinking>

Now I can see the exact structure. The `flash_attn_group` only contains a checkbox, but the code expects a `flash_attn_combobox`. I need to add the combobox widget inside this group.



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
    <height>713</height>
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
           <layout class="QHBoxLayout" name="context_layout">
            <item>
             <widget class="QLabel" name="context_size_label">
              <property name="text">
               <string>Model Context Size</string>
              </property>
             </widget>
            </item>
            <item>
             <widget class="QComboBox" name="model_context_size" />
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
               <enum>Qt::Orientation::Horizontal</enum>
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
        <widget class="QTabWidget" name="parameter_tab">
         <widget class="QWidget" name="tempGroupPage1_2">
          <attribute name="title">
           <string>Sampling Parameters</string>
          </attribute>
          <layout class="QVBoxLayout" name="sampling_page_layout">
           <item>
            <widget class="QScrollArea" name="sampling_scroll_area">
             <property name="widgetResizable">
              <bool>true</bool>
             </property>
             <widget class="QWidget" name="sampling_scroll_content">
              <property name="geometry">
               <rect>
                <x>0</x>
                <y>0</y>
                <width>700</width>
                <height>400</height>
               </rect>
              </property>
              <layout class="QGridLayout" name="temp_group_layout">
               <property name="horizontalSpacing">
                <number>12</number>
               </property>
               <property name="verticalSpacing">
                <number>8</number>
               </property>
           <item row="0" column="0">
            <layout class="QHBoxLayout" name="temperature_layout">
             <item>
              <widget class="QCheckBox" name="enable_temperature_checkbox">
               <property name="toolTip">
                <string
                                                                                >Controls randomness. Lower values are more deterministic, higher values are more creative.
Typical range: 0.1-0.4</string>
               </property>
               <property name="text">
                <string>Temperature</string>
               </property>
               <property name="checked">
                <bool>true</bool>
               </property>
              </widget>
             </item>
             <item>
              <widget class="QDoubleSpinBox" name="temperature_spinbox">
               <property name="toolTip">
                <string>Temperature value for token selection randomness.
Lower = more focused, Higher = more creative</string>
               </property>
               <property name="decimals">
                <number>2</number>
               </property>
               <property name="minimum">
                <double>0.000000000000000</double>
               </property>
               <property name="maximum">
                <double>5.000000000000000</double>
               </property>
               <property name="singleStep">
                <double>0.050000000000000</double>
               </property>
               <property name="value">
                <double>0.300000000000000</double>
               </property>
              </widget>
             </item>
            </layout>
           </item>
           <item row="0" column="1">
            <layout class="QHBoxLayout" name="top_p_layout">
             <item>
              <widget class="QCheckBox" name="enable_top_p_checkbox">
               <property name="toolTip">
                <string
                                                                                >Nucleus sampling: considers tokens with cumulative probability P.
Typical range: 0.8-0.95</string>
               </property>
               <property name="text">
                <string>Top P</string>
               </property>
               <property name="checked">
                <bool>true</bool>
               </property>
              </widget>
             </item>
             <item>
              <widget class="QDoubleSpinBox" name="top_p_spinbox">
               <property name="toolTip">
                <string>Top P cutoff for nucleus sampling.
0.9 = consider top 90% cumulative probability</string>
               </property>
               <property name="decimals">
                <number>2</number>
               </property>
               <property name="minimum">
                <double>0.000000000000000</double>
               </property>
               <property name="maximum">
                <double>1.000000000000000</double>
               </property>
               <property name="singleStep">
                <double>0.050000000000000</double>
               </property>
               <property name="value">
                <double>0.900000000000000</double>
               </property>
              </widget>
             </item>
            </layout>
           </item>
           <item row="0" column="2">
            <layout class="QHBoxLayout" name="top_k_layout">
             <item>
              <widget class="QCheckBox" name="enable_top_k_checkbox">
               <property name="toolTip">
                <string>Restricts sampling to the K most likely tokens.
Typical range: 20-50</string>
               </property>
               <property name="text">
                <string>Top K</string>
               </property>
               <property name="checked">
                <bool>true</bool>
               </property>
              </widget>
             </item>
             <item>
              <widget class="QSpinBox" name="top_k_spinbox">
               <property name="toolTip">
                <string
                                                                                >Number of highest probability tokens to consider for sampling.</string>
               </property>
               <property name="minimum">
                <number>1</number>
               </property>
               <property name="maximum">
                <number>500</number>
               </property>
               <property name="singleStep">
                <number>5</number>
               </property>
               <property name="value">
                <number>40</number>
               </property>
              </widget>
             </item>
            </layout>
           </item>
           <item row="1" column="0">
            <layout class="QHBoxLayout" name="min_p_layout">
             <item>
              <widget class="QCheckBox" name="enable_min_p_checkbox">
               <property name="toolTip">
                <string
                                                                                >Minimum probability relative to the highest token probability.
Typical range: 0.05-0.1</string>
               </property>
               <property name="text">
                <string>Min P</string>
               </property>
              </widget>
             </item>
             <item>
              <widget class="QDoubleSpinBox" name="min_p_spinbox">
               <property name="toolTip">
                <string
                                                                                >Minimum probability cutoff relative to the most likely token.</string>
               </property>
               <property name="decimals">
                <number>3</number>
               </property>
               <property name="minimum">
                <double>0.000000000000000</double>
               </property>
               <property name="maximum">
                <double>1.000000000000000</double>
               </property>
               <property name="singleStep">
                <double>0.010000000000000</double>
               </property>
               <property name="value">
                <double>0.050000000000000</double>
               </property>
              </widget>
             </item>
            </layout>
           </item>
           <item row="1" column="1">
            <layout class="QHBoxLayout" name="typical_p_layout">
             <item>
              <widget class="QCheckBox" name="enable_typical_p_checkbox">
               <property name="toolTip">
                <string
                                                                                >Selects tokens near the &quot;typical&quot; probability distribution.
Typical range: 0.9-1.0</string>
               </property>
               <property name="text">
                <string>Typical P</string>
               </property>
              </widget>
             </item>
             <item>
              <widget class="QDoubleSpinBox" name="typical_p_spinbox">
               <property name="toolTip">
                <string
                                                                                >Typical sampling parameter for balanced randomness.</string>
               </property>
               <property name="decimals">
                <number>3</number>
               </property>
               <property name="minimum">
                <double>0.000000000000000</double>
               </property>
               <property name="maximum">
                <double>1.000000000000000</double>
               </property>
               <property name="singleStep">
                <double>0.010000000000000</double>
               </property>
               <property name="value">
                <double>1.000000000000000</double>
               </property>
              </widget>
             </item>
            </layout>
           </item>
           <item row="1" column="2">
            <layout class="QHBoxLayout" name="repeat_penalty_layout">
             <item>
              <widget class="QCheckBox" name="enable_repeat_penalty_checkbox">
               <property name="toolTip">
                <string>Penalizes repeated tokens to reduce repetition.
Typical range: 1.05-1.15</string>
               </property>
               <property name="text">
                <string>Repeat Penalty</string>
               </property>
               <property name="checked">
                <bool>true</bool>
               </property>
              </widget>
             </item>
             <item>
              <widget class="QDoubleSpinBox" name="repeat_penalty_spinbox">
               <property name="toolTip">
                <string
                                                                                >Penalty for repeated tokens. Higher = stronger penalty.</string>
               </property>
               <property name="decimals">
                <number>2</number>
               </property>
               <property name="minimum">
                <double>0.500000000000000</double>
               </property>
               <property name="maximum">
                <double>2.000000000000000</double>
               </property>
               <property name="singleStep">
                <double>0.050000000000000</double>
               </property>
               <property name="value">
                <double>1.100000000000000</double>
               </property>
              </widget>
             </item>
            </layout>
           </item>
           <item row="2" column="0">
            <layout class="QHBoxLayout" name="repeat_last_n_layout">
             <item>
              <widget class="QCheckBox" name="enable_repeat_last_n_checkbox">
               <property name="toolTip">
                <string>Number of previous tokens to check for repetition.
Typical range: 64-256</string>
               </property>
               <property name="text">
                <string>Repeat Last N</string>
               </property>
               <property name="checked">
                <bool>true</bool>
               </property>
              </widget>
             </item>
             <item>
              <widget class="QSpinBox" name="repeat_last_n_spinbox">
               <property name="toolTip">
                <string
                                                                                >How many recent tokens to consider when penalizing repetition. 0 = use model default.</string>
               </property>
               <property name="minimum">
                <number>0</number>
               </property>
               <property name="maximum">
                <number>512</number>
               </property>
               <property name="singleStep">
                <number>32</number>
               </property>
               <property name="value">
                <number>64</number>
               </property>
              </widget>
             </item>
            </layout>
           </item>
           <item row="2" column="1">
            <layout class="QHBoxLayout" name="presence_penalty_layout">
             <item>
              <widget class="QCheckBox" name="enable_presence_penalty_checkbox">
               <property name="toolTip">
                <string>Penalizes tokens that have already appeared in the text.
Typical range: 0-0.5</string>
               </property>
               <property name="text">
                <string>Presence Penalty</string>
               </property>
              </widget>
             </item>
             <item>
              <widget class="QDoubleSpinBox" name="presence_penalty_spinbox">
               <property name="toolTip">
                <string
                                                                                >Positive values penalize new tokens based on whether they appear in the text so far.</string>
               </property>
               <property name="decimals">
                <number>2</number>
               </property>
               <property name="minimum">
                <double>-2.000000000000000</double>
               </property>
               <property name="maximum">
                <double>2.000000000000000</double>
               </property>
               <property name="singleStep">
                <double>0.100000000000000</double>
               </property>
               <property name="value">
                <double>0.000000000000000</double>
               </property>
              </widget>
             </item>
            </layout>
           </item>
           <item row="2" column="2">
            <layout class="QHBoxLayout" name="frequency_penalty_layout">
             <item>
              <widget
                                                                            class="QCheckBox"
                                                                            name="enable_frequency_penalty_checkbox"
                                                                        >
               <property name="toolTip">
                <string>Penalizes tokens based on their frequency in the text.
Typical range: 0-0.5</string>
               </property>
               <property name="text">
                <string>Frequency Penalty</string>
               </property>
              </widget>
             </item>
             <item>
              <widget class="QDoubleSpinBox" name="frequency_penalty_spinbox">
               <property name="toolTip">
                <string
                                                                                >Positive values penalize new tokens based on their existing frequency in the text so far.</string>
               </property>
               <property name="decimals">
                <number>2</number>
               </property>
               <property name="minimum">
                <double>-2.000000000000000</double>
               </property>
               <property name="maximum">
                <double>2.000000000000000</double>
               </property>
               <property name="singleStep">
                <double>0.100000000000000</double>
               </property>
               <property name="value">
                <double>0.000000000000000</double>
               </property>
              </widget>
             </item>
            </layout>
           </item>
           <item row="3" column="0">
            <layout class="QHBoxLayout" name="mirostat_layout">
             <item>
              <widget class="QCheckBox" name="enable_mirostat_checkbox">
               <property name="toolTip">
                <string>Enable adaptive sampling algorithm.
0 = off, 1 = Mirostat 1.0, 2 = Mirostat 2.0</string>
               </property>
               <property name="text">
                <string>Mirostat</string>
               </property>
              </widget>
             </item>
             <item>
              <widget class="QSpinBox" name="mirostat_spinbox">
               <property name="toolTip">
                <string
                                                                                >Mirostat mode: 0=off, 1=Mirostat 1.0, 2=Mirostat 2.0</string>
               </property>
               <property name="minimum">
                <number>0</number>
               </property>
               <property name="maximum">
                <number>2</number>
               </property>
               <property name="singleStep">
                <number>1</number>
               </property>
               <property name="value">
                <number>1</number>
               </property>
              </widget>
             </item>
            </layout>
           </item>
           <item row="3" column="1">
            <layout class="QHBoxLayout" name="mirostat_lr_layout">
             <item>
              <widget class="QCheckBox" name="enable_mirostat_lr_checkbox">
               <property name="toolTip">
                <string>Mirostat learning rate (eta).
Typical value: 0.1</string>
               </property>
               <property name="text">
                <string>Mirostat LR</string>
               </property>
              </widget>
             </item>
             <item>
              <widget class="QDoubleSpinBox" name="mirostat_lr_spinbox">
               <property name="toolTip">
                <string>Learning rate for Mirostat adaptive sampling.</string>
               </property>
               <property name="decimals">
                <number>3</number>
               </property>
               <property name="minimum">
                <double>0.001000000000000</double>
               </property>
               <property name="maximum">
                <double>1.000000000000000</double>
               </property>
               <property name="singleStep">
                <double>0.010000000000000</double>
               </property>
               <property name="value">
                <double>0.100000000000000</double>
               </property>
              </widget>
             </item>
            </layout>
           </item>
           <item row="3" column="2">
            <layout class="QHBoxLayout" name="mirostat_ent_layout">
             <item>
              <widget class="QCheckBox" name="enable_mirostat_ent_checkbox">
               <property name="toolTip">
                <string>Target entropy for Mirostat.
Typical range: 5-7</string>
               </property>
               <property name="text">
                <string>Mirostat Ent</string>
               </property>
              </widget>
             </item>
             <item>
              <widget class="QDoubleSpinBox" name="mirostat_ent_spinbox">
               <property name="toolTip">
                <string>Target entropy for Mirostat adaptive sampling.</string>
               </property>
               <property name="decimals">
                <number>1</number>
               </property>
               <property name="minimum">
                <double>1.000000000000000</double>
               </property>
               <property name="maximum">
                <double>10.000000000000000</double>
               </property>
               <property name="singleStep">
                <double>0.500000000000000</double>
               </property>
               <property name="value">
                <double>5.000000000000000</double>
               </property>
              </widget>
             </item>
            </layout>
           </item>
              </layout>
             </widget>
            </widget>
           </item>
          </layout>
         </widget>
         <widget class="QWidget" name="performancePage">
          <attribute name="title">
           <string>Performance</string>
          </attribute>
          <layout class="QVBoxLayout" name="performance_page_layout">
           <item>
            <widget class="QScrollArea" name="performance_scroll_area">
             <property name="widgetResizable">
              <bool>true</bool>
             </property>
             <widget class="QWidget" name="performance_scroll_content">
              <property name="geometry">
               <rect>
                <x>0</x>
                <y>0</y>
                <width>700</width>
                <height>600</height>
               </rect>
              </property>
              <layout class="QVBoxLayout" name="performance_page_layout_inner">
               <item>
                <widget class="QGroupBox" name="gpu_layers_group">
                 <property name="title">
                  <string>GPU Layer Offload</string>
                 </property>
                 <layout class="QVBoxLayout" name="gpu_layers_layout">
                  <item>
                   <layout class="QHBoxLayout" name="gpu_layers_hbox">
                    <item>
                     <widget
                                                                                        class="QCheckBox"
                                                                                        name="enable_gpu_layers_checkbox"
                                                                                    >
                  <property name="toolTip">
                   <string>Number of model layers to offload to GPU.
99 = full offload if memory allows</string>
                  </property>
                  <property name="text">
                   <string>GPU Layers</string>
                  </property>
                 </widget>
                </item>
                <item>
                 <widget class="QSpinBox" name="gpu_layers_spinbox">
                  <property name="toolTip">
                   <string>Number of model layers to offload to GPU.
Higher values use more VRAM but speed up generation.</string>
                  </property>
                  <property name="minimum">
                   <number>0</number>
                  </property>
                  <property name="maximum">
                   <number>999</number>
                  </property>
                  <property name="value">
                   <number>99</number>
                  </property>
                 </widget>
                </item>
               </layout>
              </item>
             </layout>
            </widget>
           </item>
           <item>
            <widget class="QGroupBox" name="cpu_threading_group">
             <property name="title">
              <string>CPU Threading</string>
             </property>
             <layout class="QVBoxLayout" name="cpu_threading_layout">
              <item>
               <layout class="QHBoxLayout" name="threads_hbox">
                <item>
                 <widget class="QCheckBox" name="enable_threads_checkbox">
                  <property name="toolTip">
                   <string>Number of CPU threads used for generation.
Set to number of performance cores or leave at 0 for auto.</string>
                  </property>
                  <property name="text">
                   <string>Threads</string>
                  </property>
                 </widget>
                </item>
                <item>
                 <widget class="QSpinBox" name="threads_spinbox">
                  <property name="toolTip">
                   <string>Number of CPU threads used for token generation.
0 = use system default.</string>
                  </property>
                  <property name="minimum">
                   <number>0</number>
                  </property>
                  <property name="maximum">
                   <number>1024</number>
                  </property>
                  <property name="value">
                   <number>0</number>
                  </property>
                 </widget>
                </item>
               </layout>
              </item>
              <item>
               <layout class="QHBoxLayout" name="threads_batch_hbox">
                <item>
                 <widget class="QCheckBox" name="enable_threads_batch_checkbox">
                  <property name="toolTip">
                   <string>Number of CPU threads used during prompt processing.
Typically higher than generation threads.</string>
                  </property>
                  <property name="text">
                   <string>Threads Batch</string>
                  </property>
                 </widget>
                </item>
                <item>
                 <widget class="QSpinBox" name="threads_batch_spinbox">
                  <property name="toolTip">
                   <string>Number of CPU threads used during prompt processing.
0 = same as threads.</string>
                  </property>
                  <property name="minimum">
                   <number>0</number>
                  </property>
                  <property name="maximum">
                   <number>1024</number>
                  </property>
                  <property name="value">
                   <number>0</number>
                  </property>
                 </widget>
                </item>
               </layout>
              </item>
             </layout>
            </widget>
           </item>
           <item>
            <widget class="QGroupBox" name="batching_group">
             <property name="title">
              <string>Batching</string>
             </property>
             <layout class="QVBoxLayout" name="batching_layout">
              <item>
               <layout class="QHBoxLayout" name="batch_size_hbox">
                <item>
                 <widget class="QCheckBox" name="enable_batch_size_checkbox">
                  <property name="toolTip">
                   <string>Number of tokens processed per batch.
Typical range: 512-2048</string>
                  </property>
                  <property name="text">
                   <string>Batch Size</string>
                  </property>
                 </widget>
                </item>
                <item>
                 <widget class="QSpinBox" name="batch_size_spinbox">
                  <property name="toolTip">
                   <string>Number of tokens processed per batch.
Higher values improve throughput but use more memory.</string>
                  </property>
                  <property name="minimum">
                   <number>1</number>
                  </property>
                  <property name="maximum">
                   <number>4096</number>
                  </property>
                  <property name="value">
                   <number>512</number>
                  </property>
                 </widget>
                </item>
               </layout>
              </item>
              <item>
               <layout class="QHBoxLayout" name="ubatch_size_hbox">
                <item>
                 <widget class="QCheckBox" name="enable_ubatch_size_checkbox">
                  <property name="toolTip">
                   <string>Physical micro-batch size.
Typical range: 128-512</string>
                  </property>
                  <property name="text">
                   <string>Micro-Batch Size</string>
                  </property>
                 </widget>
                </item>
                <item>
                 <widget class="QSpinBox" name="ubatch_size_spinbox">
                  <property name="toolTip">
                   <string>Physical micro-batch size for prompt processing.
Smaller values reduce memory spikes.</string>
                  </property>
                  <property name="minimum">
                   <number>1</number>
                  </property>
                  <property name="maximum">
                   <number>1024</number>
                  </property>
                  <property name="value">
                   <number>512</number>
                  </property>
                 </widget>
                </item>
               </layout>
              </item>
             </layout>
            </widget>
           </item>
           <item>
            <widget class="QGroupBox" name="n_predict_group">
             <property name="title">
              <string>Generation</string>
             </property>
             <layout class="QVBoxLayout" name="n_predict_layout">
              <item>
               <layout class="QHBoxLayout" name="n_predict_hbox">
                <item>
                 <widget class="QCheckBox" name="enable_n_predict_checkbox">
                  <property name="toolTip">
                   <string>Maximum number of tokens to generate per request.
Typical range: 2048-8192</string>
                  </property>
                  <property name="text">
                   <string>N Predict</string>
                  </property>
                 </widget>
                </item>
                <item>
                 <widget class="QSpinBox" name="n_predict_spinbox">
                  <property name="toolTip">
                   <string
                                                                                            >Maximum number of tokens to generate in a single request.
0 = unlimited (until EOS or context limit).</string>
                  </property>
                  <property name="minimum">
                   <number>0</number>
                  </property>
                  <property name="maximum">
                   <number>65536</number>
                  </property>
                  <property name="value">
                   <number>2048</number>
                  </property>
                 </widget>
                </item>
               </layout>
              </item>
             </layout>
            </widget>
           </item>
           <item>
            <widget class="QGroupBox" name="flash_attn_group">
             <property name="title">
              <string>Attention Optimizations</string>
             </property>
             <layout class="QVBoxLayout" name="flash_attn_layout">
              <item>
               <widget class="QCheckBox" name="enable_flash_attn_checkbox">
                <property name="toolTip">
                 <string
                                                                                    >Enable Flash Attention to reduce memory use and improve speed.
Requires compatible GPU.</string>
                </property>
                <property name="text">
                 <string>Flash Attention</string>
                </property>
               </widget>
              </item>
              <item>
               <layout class="QHBoxLayout" name="flash_attn_hbox">
                <item>
                 <widget class="QLabel" name="flash_attn_label">
                  <property name="text">
                   <string>Mode:</string>
                  </property>
                 </widget>
                </item>
                <item>
                 <widget class="QComboBox" name="flash_attn_combobox">
                  <property name="toolTip">
                   <string>Flash Attention mode.
on = enabled, off = disabled, auto = let llama-server decide.</string>
                  </property>
                  <item>
                   <property name="text">
                    <string>auto</string>
                   </property>
                  </item>
                  <item>
                   <property name="text">
                    <string>on</string>
                   </property>
                  </item>
                  <item>
                   <property name="text">
                    <string>off</string>
                   </property>
                  </item>
                 </widget>
                </item>
               </layout>
              </item>
             </layout>
            </widget>
           </item>
           <item>
            <widget class="QGroupBox" name="kv_cache_group">
             <property name="title">
              <string>KV Cache</string>
             </property>
             <layout class="QVBoxLayout" name="kv_cache_layout">
              <item>
               <layout class="QHBoxLayout" name="cache_type_k_hbox">
                <item>
                 <widget class="QCheckBox" name="enable_cache_type_k_checkbox">
                  <property name="toolTip">
                   <string>KV cache key precision.
f16 = highest quality, q8_0/q4_0 = lower memory use.</string>
                  </property>
                  <property name="text">
                   <string>Cache Type K</string>
                  </property>
                 </widget>
                </item>
                <item>
                 <widget class="QComboBox" name="cache_type_k_combobox">
                  <property name="toolTip">
                   <string>KV cache key data type precision.
f16 = full precision, q8_0/q4_0 = quantized.</string>
                  </property>
                  <item>
                   <property name="text">
                    <string>f16</string>
                   </property>
                  </item>
                  <item>
                   <property name="text">
                    <string>q8_0</string>
                   </property>
                  </item>
                  <item>
                   <property name="text">
                    <string>q4_0</string>
                   </property>
                  </item>
                 </widget>
                </item>
               </layout>
              </item>
              <item>
               <layout class="QHBoxLayout" name="cache_type_v_hbox">
                <item>
                 <widget class="QCheckBox" name="enable_cache_type_v_checkbox">
                  <property name="toolTip">
                   <string>KV cache value precision.
f16 = highest quality, q8_0/q4_0 = lower memory use.</string>
                  </property>
                  <property name="text">
                   <string>Cache Type V</string>
                  </property>
                 </widget>
                </item>
                <item>
                 <widget class="QComboBox" name="cache_type_v_combobox">
                  <property name="toolTip">
                   <string>KV cache value data type precision.
f16 = full precision, q8_0/q4_0 = quantized.</string>
                  </property>
                  <item>
                   <property name="text">
                    <string>f16</string>
                   </property>
                  </item>
                  <item>
                   <property name="text">
                    <string>q8_0</string>
                   </property>
                  </item>
                  <item>
                   <property name="text">
                    <string>q4_0</string>
                   </property>
                  </item>
                 </widget>
                </item>
               </layout>
              </item>
             </layout>
            </widget>
           </item>
           <item>
            <widget class="QGroupBox" name="memory_group">
             <property name="title">
              <string>Memory Handling</string>
             </property>
             <layout class="QVBoxLayout" name="memory_layout">
              <item>
               <widget class="QCheckBox" name="enable_mmap_checkbox">
                <property name="toolTip">
                 <string>Memory-map the model file for efficient loading.
Recommended to keep enabled.</string>
                </property>
                <property name="text">
                 <string>MMap</string>
                </property>
                <property name="checked">
                 <bool>true</bool>
                </property>
               </widget>
              </item>
              <item>
               <widget class="QCheckBox" name="enable_mlock_checkbox">
                <property name="toolTip">
                 <string>Lock model into RAM to prevent swapping.
Enable only if you have enough system RAM.</string>
                </property>
                <property name="text">
                 <string>MLock</string>
                </property>
               </widget>
              </item>
             </layout>
            </widget>
           </item>
           <item>
            <widget class="QGroupBox" name="server_batching_group">
             <property name="title">
              <string>Server Batching</string>
             </property>
             <layout class="QVBoxLayout" name="server_batching_layout">
              <item>
               <widget class="QCheckBox" name="enable_cont_batching_checkbox">
                <property name="toolTip">
                 <string
                                                                                    >Enable continuous batching for handling multiple requests.
Improves throughput for concurrent users.</string>
                </property>
                <property name="text">
                 <string>Continuous Batching</string>
                </property>
               </widget>
              </item>
              <item>
               <layout class="QHBoxLayout" name="parallel_hbox">
                <item>
                 <widget class="QCheckBox" name="enable_parallel_checkbox">
                  <property name="toolTip">
                   <string>Number of concurrent sequences the server can handle.
Typical range: 1-8+</string>
                  </property>
                  <property name="text">
                   <string>Parallel Sequences</string>
                  </property>
                 </widget>
                </item>
                <item>
                 <widget class="QSpinBox" name="parallel_spinbox">
                  <property name="toolTip">
                   <string>Number of concurrent sequences to process.
Higher values support more users but use more memory.</string>
                  </property>
                  <property name="minimum">
                   <number>1</number>
                  </property>
                  <property name="maximum">
                   <number>32</number>
                  </property>
                  <property name="value">
                   <number>4</number>
                  </property>
                 </widget>
                </item>
               </layout>
              </item>
             </layout>
            </widget>
           </item>
               <item>
                <spacer name="performance_vertical_spacer">
                 <property name="orientation">
                  <enum>Qt::Orientation::Vertical</enum>
                 </property>
                 <property name="sizeHint" stdset="0">
                  <size>
                   <width>20</width>
                   <height>40</height>
                  </size>
                 </property>
                </spacer>
               </item>
              </layout>
             </widget>
            </widget>
           </item>
          </layout>
         </widget>
         <widget class="QWidget" name="advancedGenPage">
          <attribute name="title">
           <string>Advanced Generation</string>
          </attribute>
          <layout class="QVBoxLayout" name="advanced_gen_page_layout">
           <item>
            <widget class="QScrollArea" name="advanced_gen_scroll_area">
             <property name="widgetResizable">
              <bool>true</bool>
             </property>
             <widget class="QWidget" name="advanced_gen_scroll_content">
              <property name="geometry">
               <rect>
                <x>0</x>
                <y>0</y>
                <width>700</width>
                <height>600</height>
               </rect>
              </property>
              <layout class="QVBoxLayout" name="advanced_gen_page_layout_inner">
               <item>
                <widget class="QGroupBox" name="speculative_decoding_group">
                 <property name="title">
                  <string>Speculative Decoding</string>
                 </property>
                 <layout class="QVBoxLayout" name="speculative_decoding_layout">
                  <item>
                   <layout class="QHBoxLayout" name="draft_model_layout">
                    <item>
                     <widget
                                                                                        class="QCheckBox"
                                                                                        name="enable_draft_model_checkbox"
                                                                                    >
                      <property name="toolTip">
                       <string>Path to a draft model for speculative decoding.
Uses a smaller model to propose tokens for the larger model to verify.</string>
                      </property>
                      <property name="text">
                       <string>Draft Model</string>
                      </property>
                     </widget>
                    </item>
                    <item>
                     <widget class="QLineEdit" name="draft_model_line_edit">
                      <property name="placeholderText">
                       <string>Select draft model path...</string>
                      </property>
                     </widget>
                    </item>
                    <item>
                     <widget
                                                                                        class="QPushButton"
                                                                                        name="select_draft_model_button"
                                                                                    >
                      <property name="text">
                       <string>...</string>
                      </property>
                     </widget>
                    </item>
                   </layout>
                  </item>
                  <item>
                   <layout class="QHBoxLayout" name="spec_draft_n_max_layout">
                    <item>
                     <widget
                                                                                        class="QCheckBox"
                                                                                        name="enable_spec_draft_n_max_checkbox"
                                                                                    >
                      <property name="toolTip">
                       <string
                                                                                            >Maximum number of draft tokens per verification step.
Typical range: 4-8</string>
                      </property>
                      <property name="text">
                       <string>Spec Draft N Max</string>
                      </property>
                     </widget>
                    </item>
                    <item>
                     <widget class="QSpinBox" name="spec_draft_n_max_spinbox">
                      <property name="toolTip">
                       <string
                                                                                            >Maximum number of tokens to draft in speculative decoding.</string>
                      </property>
                      <property name="minimum">
                       <number>1</number>
                      </property>
                      <property name="maximum">
                       <number>16</number>
                      </property>
                      <property name="value">
                       <number>5</number>
                      </property>
                     </widget>
                    </item>
                   </layout>
                  </item>
                 </layout>
                </widget>
               </item>
               <item>
                <widget class="QGroupBox" name="deterministic_group">
                 <property name="title">
                  <string>Deterministic Generation</string>
                 </property>
                 <layout class="QVBoxLayout" name="deterministic_layout">
                  <item>
                   <layout class="QHBoxLayout" name="seed_layout">
                    <item>
                     <widget class="QCheckBox" name="enable_seed_checkbox">
                      <property name="toolTip">
                       <string>Random seed for reproducible output.
Set to a fixed value for consistent results.</string>
                      </property>
                      <property name="text">
                       <string>Seed</string>
                      </property>
                     </widget>
                    </item>
                    <item>
                     <widget class="QSpinBox" name="seed_spinbox">
                      <property name="toolTip">
                       <string>Random seed for reproducible generation.
Use a fixed value for deterministic output.</string>
                      </property>
                      <property name="minimum">
                       <number>0</number>
                      </property>
                      <property name="maximum">
                       <number>2147483647</number>
                      </property>
                      <property name="value">
                       <number>42</number>
                      </property>
                     </widget>
                    </item>
                   </layout>
                  </item>
                 </layout>
                </widget>
               </item>
               <item>
                <widget class="QGroupBox" name="structured_output_group">
                 <property name="title">
                  <string>Structured Output</string>
                 </property>
                 <layout class="QVBoxLayout" name="structured_output_layout">
                  <item>
                   <layout class="QHBoxLayout" name="grammar_layout">
                    <item>
                     <widget class="QCheckBox" name="enable_grammar_checkbox">
                      <property name="toolTip">
                       <string>Apply grammar constraints to generation.
Can be a grammar string or path to a grammar file.</string>
                      </property>
                      <property name="text">
                       <string>Grammar</string>
                      </property>
                     </widget>
                    </item>
                    <item>
                     <widget class="QLineEdit" name="grammar_line_edit">
                      <property name="placeholderText">
                       <string>Grammar string or file path...</string>
                      </property>
                     </widget>
                    </item>
                   </layout>
                  </item>
                  <item>
                   <layout class="QHBoxLayout" name="json_schema_layout">
                    <item>
                     <widget
                                                                                        class="QCheckBox"
                                                                                        name="enable_json_schema_checkbox"
                                                                                    >
                      <property name="toolTip">
                       <string>Force JSON schema compliant output.
Specify path to a JSON schema file.</string>
                      </property>
                      <property name="text">
                       <string>JSON Schema</string>
                      </property>
                     </widget>
                    </item>
                    <item>
                     <widget class="QLineEdit" name="json_schema_line_edit">
                      <property name="placeholderText">
                       <string>Select JSON schema file...</string>
                      </property>
                     </widget>
                    </item>
                    <item>
                     <widget
                                                                                        class="QPushButton"
                                                                                        name="select_json_schema_button"
                                                                                    >
                      <property name="text">
                       <string>...</string>
                      </property>
                     </widget>
                    </item>
                   </layout>
                  </item>
                 </layout>
                </widget>
               </item>
               <item>
                <widget class="QGroupBox" name="model_behaviour_group">
                 <property name="title">
                  <string>Model Behaviour</string>
                 </property>
                 <layout class="QVBoxLayout" name="model_behaviour_layout">
                  <item>
                   <layout class="QHBoxLayout" name="rope_scaling_layout">
                    <item>
                     <widget
                                                                                        class="QCheckBox"
                                                                                        name="enable_rope_scaling_checkbox"
                                                                                    >
                      <property name="toolTip">
                       <string>Extend model context length using RoPE scaling.
Choose based on your model's capabilities.</string>
                      </property>
                      <property name="text">
                       <string>RoPE Scaling</string>
                      </property>
                     </widget>
                    </item>
                    <item>
                     <widget class="QComboBox" name="rope_scaling_combobox">
                      <property name="toolTip">
                       <string
                                                                                            >RoPE (Rotary Positional Embeddings) scaling method.
Model dependent - check model documentation.</string>
                      </property>
                      <item>
                       <property name="text">
                        <string>none</string>
                       </property>
                      </item>
                      <item>
                       <property name="text">
                        <string>linear</string>
                       </property>
                      </item>
                      <item>
                       <property name="text">
                        <string>yarn</string>
                       </property>
                      </item>
                     </widget>
                    </item>
                   </layout>
                  </item>
                  <item>
                   <layout class="QHBoxLayout" name="rope_freq_base_layout">
                    <item>
                     <widget
                                                                                        class="QCheckBox"
                                                                                        name="enable_rope_freq_base_checkbox"
                                                                                    >
                      <property name="toolTip">
                       <string>Modify RoPE frequency base.
Model dependent - typically 1.0 for most models.</string>
                      </property>
                      <property name="text">
                       <string>RoPE Freq Base</string>
                      </property>
                     </widget>
                    </item>
                    <item>
                     <widget
                                                                                        class="QDoubleSpinBox"
                                                                                        name="rope_freq_base_spinbox"
                                                                                    >
                      <property name="toolTip">
                       <string
                                                                                            >Base frequency for RoPE positional embeddings.</string>
                      </property>
                      <property name="decimals">
                       <number>3</number>
                      </property>
                      <property name="minimum">
                       <double>0.001000000000000</double>
                      </property>
                      <property name="maximum">
                       <double>1000000.000000000000000</double>
                      </property>
                      <property name="singleStep">
                       <double>0.100000000000000</double>
                      </property>
                      <property name="value">
                       <double>1.000000000000000</double>
                      </property>
                     </widget>
                    </item>
                   </layout>
                  </item>
                  <item>
                   <layout class="QHBoxLayout" name="rope_freq_scale_layout">
                    <item>
                     <widget
                                                                                        class="QCheckBox"
                                                                                        name="enable_rope_freq_scale_checkbox"
                                                                                    >
                      <property name="toolTip">
                       <string>Adjust positional scaling for RoPE.
Model dependent - typically 1.0 for most models.</string>
                      </property>
                      <property name="text">
                       <string>RoPE Freq Scale</string>
                      </property>
                     </widget>
                    </item>
                    <item>
                     <widget
                                                                                        class="QDoubleSpinBox"
                                                                                        name="rope_freq_scale_spinbox"
                                                                                    >
                      <property name="toolTip">
                       <string
                                                                                            >Scaling factor for RoPE positional embeddings.</string>
                      </property>
                      <property name="decimals">
                       <number>3</number>
                      </property>
                      <property name="minimum">
                       <double>0.001000000000000</double>
                      </property>
                      <property name="maximum">
                       <double>10.000000000000000</double>
                      </property>
                      <property name="singleStep">
                       <double>0.050000000000000</double>
                      </property>
                      <property name="value">
                       <double>1.000000000000000</double>
                      </property>
                     </widget>
                    </item>
                   </layout>
                  </item>
                 </layout>
                </widget>
               </item>
               <item>
                <spacer name="advanced_gen_vertical_spacer">
                 <property name="orientation">
                  <enum>Qt::Orientation::Vertical</enum>
                 </property>
                 <property name="sizeHint" stdset="0">
                  <size>
                   <width>20</width>
                   <height>40</height>
                  </size>
                 </property>
                </spacer>
               </item>
              </layout>
             </widget>
            </widget>
           </item>
          </layout>
         </widget>
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
        <widget class="QWebEngineView" name="server_web_view" native="true" />
       </item>
      </layout>
     </widget>
    </widget>
   </item>
  </layout>
 </widget>
 <customwidgets>
  <customwidget>
   <class>QWebEngineView</class>
   <extends>QWidget</extends>
   <header>qwebengineview.h</header>
  </customwidget>
 </customwidgets>
 <resources />
 <connections />
</ui>

```


## Assistant

<thinking>
The UI file has been updated with the flash_attn_combobox widget. Now I need to verify that this fix resolves the AttributeError. The combobox is now added to the UI file with:
- Name: `flash_attn_combobox`
- Items: "auto", "on", "off"
- Default: "auto" (first item)

Since `load_ui()` auto-assigns widgets as attributes based on their `objectName`, `self.flash_attn_combobox` should now exist when the UI is loaded.

Let me also check if there are any other references to flash_attn in the code that might need updating, and verify the fix by checking if the application can at least start without this error.

I should also check if there's an `enable_flash_attn_checkbox` reference in the launch code that might conflict with the new combobox approach. Looking at line 367:
```python
flash_attn = self.flash_attn_combobox.currentText()
cmd.extend(["--flash-attn", flash_attn])
```

This always passes the selected value, which is fine. The checkbox still exists for enabling/disabling the feature, but now we also have a combobox to select the mode.

Wait, let me re-read the code more carefully. Looking at line 367:
```python
# Flash Attention: always pass the selected value (default auto)
flash_attn = self.flash_attn_combobox.currentText()
cmd.extend(["--flash-attn", flash_attn])
```

This always adds `--flash-attn` with the selected value, regardless of whether the checkbox is checked. This might be intentional - the comment says "always pass the selected value". But it would be good to check if there's supposed to be a conditional check like other parameters.

Actually, looking at the pattern in the code, most parameters are wrapped in `if self.enable_*_checkbox.isChecked():` blocks. The flash_attn implementation here is different - it always passes the value. This might be intentional for llama-server to know the intended mode even when not explicitly enabled.

For now, the fix should resolve the AttributeError. Let me verify by checking if there are any other issues.

</thinking>

The `flash_attn_combobox` widget has been added to the UI file. Now `self.flash_attn_combobox` will be available as an attribute when the UI is loaded via `load_ui()`.

The combobox includes:
- **auto** (default) – let llama-server decide
- **on** – enable Flash Attention  
- **off** – disable Flash Attention

This matches the `--flash-attn` CLI argument that accepts those three values. The widget will be auto-assigned as `self.flash_attn_combobox` by `load_ui()` since its `objectName` is set to `flash_attn_combobox`.

The original error should now be resolved – the app can access the combobox and pass its selected value to `llama-server --flash-attn <value>`.
