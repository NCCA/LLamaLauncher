# Project tests improvement ideas and review

**Session ID:** ses_12611cba4ffeCd79EISVfP8hE4
**Created:** 6/18/2026, 9:52:07 AM
**Updated:** 6/18/2026, 10:02:12 AM

---

## User

check this project especially the tests how could it be improved

---

## Assistant (Python-Code-Quality · Claude Sonnet 4.5 · 14.4s)

I'll analyze this project, focusing on the implementation and especially the tests. Let me start by exploring the project structure and examining the codebase.

**Tool: bash**

**Input:**
```json
{
  "command": "find . -type f -name \"*.py\" | grep -E \"(src/|tests/)\" | head -30",
  "description": "Find Python source and test files"
}
```

**Output:**
```
./tests/test_file_selection.py
./tests/test_lifecycle.py
./tests/conftest.py
./tests/config_collector.py
./tests/test_signals.py
./tests/test_helper_methods.py
./tests/__init__.py
./tests/test_process.py
./tests/test_config.py
./tests/test_edge_cases.py
./tests/test_main.py
./tests/test_ui_loader.py
./.worktrees/test-process-launch-side-effects/tests/conftest.py
./.worktrees/test-process-launch-side-effects/tests/config_collector.py
./.worktrees/test-process-launch-side-effects/tests/test_helper_methods.py
./.worktrees/test-process-launch-side-effects/tests/__init__.py
./.worktrees/test-process-launch-side-effects/tests/test_config.py
./.worktrees/test-process-launch-side-effects/tests/test_main.py
./.worktrees/test-process-launch-side-effects/tests/test_ui_loader.py
./.worktrees/process-command-builder/tests/conftest.py
./.worktrees/process-command-builder/tests/config_collector.py
./.worktrees/process-command-builder/tests/test_helper_methods.py
./.worktrees/process-command-builder/tests/__init__.py
./.worktrees/process-command-builder/tests/test_config.py
./.worktrees/process-command-builder/tests/test_main.py
./.worktrees/process-command-builder/tests/test_ui_loader.py
./.worktrees/edge-case-tests/ui_loader.py
./.worktrees/edge-case-tests/tests/test_file_selection.py
./.worktrees/edge-case-tests/tests/conftest.py
./.worktrees/edge-case-tests/tests/config_collector.py

```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Volumes/teaching/Code/LLamaLauncher"
}
```

**Output:**
```
<path>/Volumes/teaching/Code/LLamaLauncher</path>
<type>directory</type>
<entries>
__pycache__/
.agents/
.DS_Store
.git/
.gitignore
.pytest_cache/
.python-version
.ruff_cache/
.venv/
.worktrees/
AgentChats/
AGENTS.md
docs/
headroom_memory.db
main.py
process_command.py
pyproject.toml
pytest-best-practices.md
README.md
SmallModel.json
test.json
Testing.md
tests/
TODO.md
ui_loader.py
ui/
uv.lock

(27 entries)
</entries>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Volumes/teaching/Code/LLamaLauncher/pyproject.toml"
}
```

**Output:**
```
<path>/Volumes/teaching/Code/LLamaLauncher/pyproject.toml</path>
<type>file</type>
<content>
1: [project]
2: name = "llamalauncher"
3: version = "0.1.0"
4: description = "Add your description here"
5: readme = "README.md"
6: requires-python = ">=3.14"
7: dependencies = [
8:     "pyside6>=6.11.1",
9:     "requests>=2.34.2",
10: ]
11: 
12: [dependency-groups]
13: dev = [
14:     "pytest>=9.1.0",
15:     "pytest-cov>=7.1.0",
16:     "pytest-qt>=4.5.0",
17: ]
18: 
19: [tool.pytest.ini_options]
20: testpaths = ["tests"]
21: qt_api = "pyside6"
22: markers = [
23:     "file_errors: Error handling when UI files cannot be loaded",
24:     "widget_assignment: Widget and layout attribute assignment by objectName",
25:     "parent_type_setup: Widget setup for different parent widget types",
26:     "path_support: Path type acceptance",
27: ]
28: 
29: [tool.coverage.run]
30: source = ["src", "."]
31: omit = ["tests/**", "**/conftest.py"]
32: 
33: [tool.coverage.report]
34: exclude_lines = [
35:     "pragma: no cover",
36:     "def __repr__",
37:     "raise NotImplementedError",
38:     "if TYPE_CHECKING:",
39:     "@abstractmethod",
40: ]
41: fail_under = 90

(End of file - total 41 lines)
</content>

[Project README: /Volumes/teaching/Code/LLamaLauncher/README.md]

```

---

## Assistant (Python-Code-Quality · Claude Sonnet 4.5 · 135.1s)

Now let me examine the main source files and test files:

**Tool: read**

**Input:**
```json
{
  "filePath": "/Volumes/teaching/Code/LLamaLauncher/main.py"
}
```

**Output:**
```
<path>/Volumes/teaching/Code/LLamaLauncher/main.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env -S uv run --script
2: """Llama model launcher application."""
3: 
4: import argparse
5: import json
6: import re
7: import sys
8: from pathlib import Path
9: 
10: from PySide6.QtCore import QCoreApplication, QProcess, QSettings, Qt, QTimer, QUrl
11: from PySide6.QtGui import QAction
12: from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile
13: from PySide6.QtWebEngineWidgets import QWebEngineView  # noqa: F401
14: from PySide6.QtWidgets import (
15:     QApplication,
16:     QFileDialog,
17:     QMainWindow,
18:     QMenu,
19:     QMessageBox,
20: )
21: 
22: from ui_loader import load_ui
23: 
24: 
25: class LlamaLaunchApp(QMainWindow):
26:     """Main application window for the Llama model launcher.
27: 
28:     Loads its UI from a .ui file via QUiLoader and wires up all
29:     signals and slots to preserve existing behaviour.
30:     """
31: 
32:     def __init__(
33:         self,
34:         host: str = "127.0.0.1",
35:         port: int = 8080,
36:         ctx_size: int | None = None,
37:     ) -> None:
38:         super().__init__()
39:         self._process = QProcess(self)
40:         self._process.readyReadStandardOutput.connect(self._on_stdout)
41:         self._process.readyReadStandardError.connect(self._on_stderr)
42:         self._process.finished.connect(self._on_finished)
43:         self._process.errorOccurred.connect(self._on_error)
44:         self._host = host
45:         self._port = port
46:         self._server_url: str = f"http://{host}:{port}"
47:         self._auto_refresh_done: bool = False
48:         self._cache_dir: Path = self._create_cache_dir()
49:         self._profile: QWebEngineProfile = self._create_persistent_profile()
50:         self._ctx_size: int | None = ctx_size
51:         self._setup_ui()
52:         self._load_last_session()
53:         self._connect_signals()
54:         self._init_web_view()
55: 
56:     # ------------------------------------------------------------------
57:     # UI loading and initialization
58:     # ------------------------------------------------------------------
59: 
60:     def _create_cache_dir(self) -> Path:
61:         """Create and return a cache directory for persistent web storage.
62: 
63:         Returns:
64:             Path to the cache directory (created if it does not exist).
65:         """
66:         cache_dir = (
67:             Path(QCoreApplication.applicationDirPath()) / ".cache" / "llama-launcher"
68:         )
69:         cache_dir.mkdir(parents=True, exist_ok=True)
70:         return cache_dir
71: 
72:     def _create_persistent_profile(self) -> QWebEngineProfile:
73:         """Create a QWebEngineProfile with disk-backed persistent storage.
74: 
75:         This ensures localStorage, sessionStorage, cookies, and IndexedDB
76:         survive across application restarts so the chat UI remembers
77:         API keys and conversation history.
78: 
79:         Returns:
80:             Configured QWebEngineProfile instance.
81:         """
82:         profile = QWebEngineProfile("llama-launcher-profile", self)
83: 
84:         # Persist localStorage, sessionStorage, and IndexedDB to disk
85:         profile.setPersistentStoragePath(str(self._cache_dir))
86: 
87:         # Persist cookies to disk (not session-only)
88:         profile.setPersistentCookiesPolicy(
89:             QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies
90:         )
91: 
92:         # Enable disk HTTP cache for faster page loads
93:         cache_subdir = self._cache_dir / "cache"
94:         cache_subdir.mkdir(parents=True, exist_ok=True)
95:         profile.setHttpCacheType(QWebEngineProfile.DiskHttpCache)
96:         profile.setHttpCacheMaximumSize(100 * 1024 * 1024)  # 100 MB
97: 
98:         return profile
99: 
100:     def _init_web_view(self) -> None:
101:         """Initialize the QWebEngineView in the Server tab.
102: 
103:         Creates a QWebEnginePage with the persistent profile so that
104:         localStorage, cookies, and IndexedDB are restored from disk.
105:         """
106:         page = QWebEnginePage(self._profile, self.server_web_view)
107:         self.server_web_view.setPage(page)
108:         url = f"http://{self._host}:{self._port}"
109:         self.server_web_view.setUrl(url)
110: 
111:     def _setup_ui(self) -> None:
112:         """Load the main window UI from the .ui file.
113: 
114:         All child widgets and layouts are auto-assigned as attributes
115:         on this instance by their ``objectName`` so that the .ui file
116:         controls which names are available.
117:         """
118:         ui_path = Path(__file__).resolve().parent / "ui" / "llama_launch.ui"
119:         load_ui(ui_path, self)
120:         self._setup_context_size_combo()
121:         self._create_file_menu()
122: 
123:     def _setup_context_size_combo(self) -> None:
124:         """Populate the model context size combobox with options and tooltips.
125: 
126:         Each item stores its numeric value (used as ``--ctx-size``) in the
127:         user data role so the launch method can retrieve it later.
128:         """
129:         self.model_context_size.clear()
130: 
131:         context_options = [
132:             ("Auto (model default)", 0, "Recommended default; uses GGUF model context"),
133:             ("2K", 2048, "Very small models / low memory"),
134:             ("4K", 4096, "Basic chat, small coding tasks"),
135:             ("8K", 8192, "General purpose"),
136:             ("16K", 16384, "Better coding/chat history"),
137:             ("32K", 32768, "Large files, coding assistants"),
138:             ("64K", 65536, "Long documents, repo context"),
139:             ("128K", 131072, "Modern long-context models"),
140:         ]
141: 
142:         for display_name, value, tooltip in context_options:
143:             self.model_context_size.addItem(display_name, value)
144:             index = self.model_context_size.count() - 1
145:             self.model_context_size.setItemData(index, tooltip, Qt.ToolTipRole)
146: 
147:         # Pre-select from CLI if provided, otherwise default to 16K
148:         if self._ctx_size is not None:
149:             target = self._ctx_size
150:         else:
151:             target = 16384  # 16K default
152: 
153:         for i in range(self.model_context_size.count()):
154:             if int(self.model_context_size.itemData(i, Qt.UserRole)) == target:
155:                 self.model_context_size.setCurrentIndex(i)
156:                 break
157: 
158:     # ------------------------------------------------------------------
159:     # File menu
160:     # ------------------------------------------------------------------
161: 
162:     def _create_file_menu(self) -> None:
163:         """Create the File menu with Save, Save As, and Load actions."""
164:         file_menu = QMenu("&File", self)
165: 
166:         save_action = QAction("Save Configuration", self)
167:         save_action.setShortcut("Ctrl+S")
168:         save_action.setStatusTip("Save current configuration to file")
169:         save_action.triggered.connect(self._save_config)
170:         file_menu.addAction(save_action)
171: 
172:         save_as_action = QAction("Save As Configuration...", self)
173:         save_as_action.setStatusTip("Save current configuration to a new file")
174:         save_as_action.triggered.connect(self._save_config_as)
175:         file_menu.addAction(save_as_action)
176: 
177:         load_action = QAction("Load Configuration...", self)
178:         load_action.setShortcut("Ctrl+O")
179:         load_action.setStatusTip("Load configuration from file")
180:         load_action.triggered.connect(self._load_config)
181:         file_menu.addAction(load_action)
182: 
183:         self.menuBar().addMenu(file_menu)
184: 
185:     # ------------------------------------------------------------------
186:     # Configuration save/load
187:     # ------------------------------------------------------------------
188: 
189:     def _save_config(self) -> None:
190:         """Save current configuration to the last saved file or prompt for path."""
191:         if not hasattr(self, "_last_config_path"):
192:             self._save_config_as()
193:             return
194:         self._write_config_file(self._last_config_path)
195: 
196:     def _save_config_as(self) -> None:
197:         """Save current configuration to a user-selected file path."""
198:         file_path, _ = QFileDialog.getSaveFileName(
199:             self,
200:             "Save Configuration",
201:             "",
202:             "JSON Files (*.json);;All Files (*)",
203:         )
204:         if file_path:
205:             self._write_config_file(file_path)
206:             self._last_config_path = file_path
207: 
208:     def _write_config_file(self, file_path: str) -> None:
209:         """Write the current UI configuration to a JSON file.
210: 
211:         Args:
212:             file_path: Path to the JSON file to write.
213:         """
214:         config = self._collect_config()
215:         try:
216:             with open(file_path, "w") as f:
217:                 json.dump(config, f, indent=2)
218:             self.output_display.appendPlainText(f"Configuration saved to {file_path}")
219:         except Exception as e:
220:             QMessageBox.critical(
221:                 self, "Save Error", f"Failed to save configuration:\n{e}"
222:             )
223: 
224:     def _collect_config(self) -> dict:
225:         """Collect all UI widget values into a configuration dictionary.
226: 
227:         Returns:
228:             Dictionary containing all configuration values organized by category.
229:         """
230:         config: dict = {"version": "1.0"}
231: 
232:         # Files/Paths
233:         config["files"] = {
234:             "model_path": self.model_path_edit.property("fullPath") or "",
235:             "mmproj_path": self.mmproj_path_edit.property("fullPath") or "",
236:             "draft_model_path": self.draft_model_line_edit.property("fullPath") or "",
237:             "json_schema_path": self.json_schema_line_edit.property("fullPath") or "",
238:         }
239: 
240:         # Server
241:         config["server"] = {
242:             "host": self.host_line_edit.text(),
243:             "port": int(self.port_line_edit.text())
244:             if self.port_line_edit.text().isdigit()
245:             else 8080,
246:             "api_key": self.api_key_line_edit.text() or "12345",
247:         }
248: 
249:         # Sampling parameters
250:         config["sampling"] = {
251:             "temperature": {
252:                 "enabled": self.enable_temperature_checkbox.isChecked(),
253:                 "value": self.temperature_spinbox.value(),
254:             },
255:             "top_p": {
256:                 "enabled": self.enable_top_p_checkbox.isChecked(),
257:                 "value": self.top_p_spinbox.value(),
258:             },
259:             "top_k": {
260:                 "enabled": self.enable_top_k_checkbox.isChecked(),
261:                 "value": self.top_k_spinbox.value(),
262:             },
263:             "min_p": {
264:                 "enabled": self.enable_min_p_checkbox.isChecked(),
265:                 "value": self.min_p_spinbox.value(),
266:             },
267:             "typical_p": {
268:                 "enabled": self.enable_typical_p_checkbox.isChecked(),
269:                 "value": self.typical_p_spinbox.value(),
270:             },
271:             "repeat_penalty": {
272:                 "enabled": self.enable_repeat_penalty_checkbox.isChecked(),
273:                 "value": self.repeat_penalty_spinbox.value(),
274:             },
275:             "repeat_last_n": {
276:                 "enabled": self.enable_repeat_last_n_checkbox.isChecked(),
277:                 "value": self.repeat_last_n_spinbox.value(),
278:             },
279:             "presence_penalty": {
280:                 "enabled": self.enable_presence_penalty_checkbox.isChecked(),
281:                 "value": self.presence_penalty_spinbox.value(),
282:             },
283:             "frequency_penalty": {
284:                 "enabled": self.enable_frequency_penalty_checkbox.isChecked(),
285:                 "value": self.frequency_penalty_spinbox.value(),
286:             },
287:             "mirostat": {
288:                 "enabled": self.enable_mirostat_checkbox.isChecked(),
289:                 "value": self.mirostat_spinbox.value(),
290:             },
291:             "mirostat_lr": {
292:                 "enabled": self.enable_mirostat_lr_checkbox.isChecked(),
293:                 "value": self.mirostat_lr_spinbox.value(),
294:             },
295:             "mirostat_ent": {
296:                 "enabled": self.enable_mirostat_ent_checkbox.isChecked(),
297:                 "value": self.mirostat_ent_spinbox.value(),
298:             },
299:         }
300: 
301:         # Performance parameters
302:         config["performance"] = {
303:             "gpu_layers": {
304:                 "enabled": self.enable_gpu_layers_checkbox.isChecked(),
305:                 "value": self.gpu_layers_spinbox.value(),
306:             },
307:             "threads": {
308:                 "enabled": self.enable_threads_checkbox.isChecked(),
309:                 "value": self.threads_spinbox.value(),
310:             },
311:             "threads_batch": {
312:                 "enabled": self.enable_threads_batch_checkbox.isChecked(),
313:                 "value": self.threads_batch_spinbox.value(),
314:             },
315:             "batch_size": {
316:                 "enabled": self.enable_batch_size_checkbox.isChecked(),
317:                 "value": self.batch_size_spinbox.value(),
318:             },
319:             "ubatch_size": {
320:                 "enabled": self.enable_ubatch_size_checkbox.isChecked(),
321:                 "value": self.ubatch_size_spinbox.value(),
322:             },
323:             "n_predict": {
324:                 "enabled": self.enable_n_predict_checkbox.isChecked(),
325:                 "value": self.n_predict_spinbox.value(),
326:             },
327:             "parallel": {
328:                 "enabled": self.enable_parallel_checkbox.isChecked(),
329:                 "value": self.parallel_spinbox.value(),
330:             },
331:             "flash_attn": self.flash_attn_combobox.currentText(),
332:             "cache_type_k": {
333:                 "enabled": self.enable_cache_type_k_checkbox.isChecked(),
334:                 "value": self.cache_type_k_combobox.currentText(),
335:             },
336:             "cache_type_v": {
337:                 "enabled": self.enable_cache_type_v_checkbox.isChecked(),
338:                 "value": self.cache_type_v_combobox.currentText(),
339:             },
340:             "mmap": self.enable_mmap_checkbox.isChecked(),
341:             "mlock": self.enable_mlock_checkbox.isChecked(),
342:             "cont_batching": self.enable_cont_batching_checkbox.isChecked(),
343:         }
344: 
345:         # Advanced Generation parameters
346:         config["advanced"] = {
347:             "draft_model": {
348:                 "enabled": self.enable_draft_model_checkbox.isChecked(),
349:                 "path": self.draft_model_line_edit.property("fullPath") or "",
350:             },
351:             "spec_draft_n_max": {
352:                 "enabled": self.enable_spec_draft_n_max_checkbox.isChecked(),
353:                 "value": self.spec_draft_n_max_spinbox.value(),
354:             },
355:             "seed": {
356:                 "enabled": self.enable_seed_checkbox.isChecked(),
357:                 "value": self.seed_spinbox.value(),
358:             },
359:             "grammar": {
360:                 "enabled": self.enable_grammar_checkbox.isChecked(),
361:                 "path": self.grammar_line_edit.property("fullPath") or "",
362:             },
363:             "json_schema": {
364:                 "enabled": self.enable_json_schema_checkbox.isChecked(),
365:                 "path": self.json_schema_line_edit.property("fullPath") or "",
366:             },
367:             "rope_scaling": {
368:                 "enabled": self.enable_rope_scaling_checkbox.isChecked(),
369:                 "value": self.rope_scaling_combobox.currentText(),
370:             },
371:             "rope_freq_base": {
372:                 "enabled": self.enable_rope_freq_base_checkbox.isChecked(),
373:                 "value": self.rope_freq_base_spinbox.value(),
374:             },
375:             "rope_freq_scale": {
376:                 "enabled": self.enable_rope_freq_scale_checkbox.isChecked(),
377:                 "value": self.rope_freq_scale_spinbox.value(),
378:             },
379:         }
380: 
381:         # Other settings
382:         config["context_size"] = self.model_context_size.itemData(
383:             self.model_context_size.currentIndex(), Qt.UserRole
384:         )
385:         config["more_options"] = self.more_options_line_edit.text()
386:         config["no_mmproj_offload"] = self.no_mmproj_offload_checkbox.isChecked()
387: 
388:         return config
389: 
390:     def _load_config(self) -> None:
391:         """Load configuration from a user-selected JSON file."""
392:         file_path, _ = QFileDialog.getOpenFileName(
393:             self,
394:             "Load Configuration",
395:             "",
396:             "JSON Files (*.json);;All Files (*)",
397:         )
398:         if not file_path:
399:             return
400: 
401:         try:
402:             with open(file_path, "r") as f:
403:                 config = json.load(f)
404:             self._apply_config(config)
405:             self._last_config_path = file_path
406:             self.output_display.appendPlainText(
407:                 f"Configuration loaded from {file_path}"
408:             )
409:         except json.JSONDecodeError as e:
410:             QMessageBox.critical(self, "Load Error", f"Invalid JSON format:\n{e}")
411:         except Exception as e:
412:             QMessageBox.critical(
413:                 self, "Load Error", f"Failed to load configuration:\n{e}"
414:             )
415: 
416:     def _apply_config(self, config: dict) -> None:
417:         """Apply configuration values from a dictionary to the UI widgets.
418: 
419:         Args:
420:             config: Configuration dictionary to apply.
421:         """
422:         # Files/Paths
423:         if "files" in config:
424:             files = config["files"]
425:             self._set_path_field(self.model_path_edit, files.get("model_path", ""))
426:             self._set_path_field(self.mmproj_path_edit, files.get("mmproj_path", ""))
427:             self._set_path_field(
428:                 self.draft_model_line_edit, files.get("draft_model_path", "")
429:             )
430:             self._set_path_field(
431:                 self.json_schema_line_edit, files.get("json_schema_path", "")
432:             )
433: 
434:         # Server
435:         if "server" in config:
436:             server = config["server"]
437:             self.host_line_edit.setText(server.get("host", "127.0.0.1"))
438:             port = server.get("port", 8080)
439:             self.port_line_edit.setText(str(port))
440:             self.api_key_line_edit.setText(server.get("api_key", "12345"))
441: 
442:         # Sampling parameters
443:         if "sampling" in config:
444:             sampling = config["sampling"]
445:             self._apply_param(
446:                 sampling,
447:                 "temperature",
448:                 self.enable_temperature_checkbox,
449:                 self.temperature_spinbox,
450:             )
451:             self._apply_param(
452:                 sampling, "top_p", self.enable_top_p_checkbox, self.top_p_spinbox
453:             )
454:             self._apply_param(
455:                 sampling, "top_k", self.enable_top_k_checkbox, self.top_k_spinbox
456:             )
457:             self._apply_param(
458:                 sampling, "min_p", self.enable_min_p_checkbox, self.min_p_spinbox
459:             )
460:             self._apply_param(
461:                 sampling,
462:                 "typical_p",
463:                 self.enable_typical_p_checkbox,
464:                 self.typical_p_spinbox,
465:             )
466:             self._apply_param(
467:                 sampling,
468:                 "repeat_penalty",
469:                 self.enable_repeat_penalty_checkbox,
470:                 self.repeat_penalty_spinbox,
471:             )
472:             self._apply_param(
473:                 sampling,
474:                 "repeat_last_n",
475:                 self.enable_repeat_last_n_checkbox,
476:                 self.repeat_last_n_spinbox,
477:             )
478:             self._apply_param(
479:                 sampling,
480:                 "presence_penalty",
481:                 self.enable_presence_penalty_checkbox,
482:                 self.presence_penalty_spinbox,
483:             )
484:             self._apply_param(
485:                 sampling,
486:                 "frequency_penalty",
487:                 self.enable_frequency_penalty_checkbox,
488:                 self.frequency_penalty_spinbox,
489:             )
490:             self._apply_param(
491:                 sampling,
492:                 "mirostat",
493:                 self.enable_mirostat_checkbox,
494:                 self.mirostat_spinbox,
495:             )
496:             self._apply_param(
497:                 sampling,
498:                 "mirostat_lr",
499:                 self.enable_mirostat_lr_checkbox,
500:                 self.mirostat_lr_spinbox,
501:             )
502:             self._apply_param(
503:                 sampling,
504:                 "mirostat_ent",
505:                 self.enable_mirostat_ent_checkbox,
506:                 self.mirostat_ent_spinbox,
507:             )
508: 
509:         # Performance parameters
510:         if "performance" in config:
511:             perf = config["performance"]
512:             self._apply_param(
513:                 perf,
514:                 "gpu_layers",
515:                 self.enable_gpu_layers_checkbox,
516:                 self.gpu_layers_spinbox,
517:             )
518:             self._apply_param(
519:                 perf, "threads", self.enable_threads_checkbox, self.threads_spinbox
520:             )
521:             self._apply_param(
522:                 perf,
523:                 "threads_batch",
524:                 self.enable_threads_batch_checkbox,
525:                 self.threads_batch_spinbox,
526:             )
527:             self._apply_param(
528:                 perf,
529:                 "batch_size",
530:                 self.enable_batch_size_checkbox,
531:                 self.batch_size_spinbox,
532:             )
533:             self._apply_param(
534:                 perf,
535:                 "ubatch_size",
536:                 self.enable_ubatch_size_checkbox,
537:                 self.ubatch_size_spinbox,
538:             )
539:             self._apply_param(
540:                 perf,
541:                 "n_predict",
542:                 self.enable_n_predict_checkbox,
543:                 self.n_predict_spinbox,
544:             )
545:             self._apply_param(
546:                 perf, "parallel", self.enable_parallel_checkbox, self.parallel_spinbox
547:             )
548: 
549:             if "flash_attn" in perf:
550:                 text = perf["flash_attn"]
551:                 index = self.flash_attn_combobox.findText(text)
552:                 if index >= 0:
553:                     self.flash_attn_combobox.setCurrentIndex(index)
554: 
555:             self._apply_combo_param(
556:                 perf,
557:                 "cache_type_k",
558:                 self.enable_cache_type_k_checkbox,
559:                 self.cache_type_k_combobox,
560:             )
561:             self._apply_combo_param(
562:                 perf,
563:                 "cache_type_v",
564:                 self.enable_cache_type_v_checkbox,
565:                 self.cache_type_v_combobox,
566:             )
567: 
568:             if "mmap" in perf:
569:                 self.enable_mmap_checkbox.setChecked(bool(perf["mmap"]))
570:             if "mlock" in perf:
571:                 self.enable_mlock_checkbox.setChecked(bool(perf["mlock"]))
572:             if "cont_batching" in perf:
573:                 self.enable_cont_batching_checkbox.setChecked(
574:                     bool(perf["cont_batching"])
575:                 )
576: 
577:         # Advanced Generation parameters
578:         if "advanced" in config:
579:             adv = config["advanced"]
580:             self._apply_param(
581:                 adv,
582:                 "spec_draft_n_max",
583:                 self.enable_spec_draft_n_max_checkbox,
584:                 self.spec_draft_n_max_spinbox,
585:             )
586:             self._apply_param(adv, "seed", self.enable_seed_checkbox, self.seed_spinbox)
587: 
588:             # Draft model (path-based)
589:             if "draft_model" in adv:
590:                 draft = adv["draft_model"]
591:                 self.enable_draft_model_checkbox.setChecked(draft.get("enabled", False))
592:                 self._set_path_field(self.draft_model_line_edit, draft.get("path", ""))
593: 
594:             # Grammar (path-based)
595:             if "grammar" in adv:
596:                 grammar = adv["grammar"]
597:                 self.enable_grammar_checkbox.setChecked(grammar.get("enabled", False))
598:                 self._set_path_field(self.grammar_line_edit, grammar.get("path", ""))
599: 
600:             # JSON schema (path-based)
601:             if "json_schema" in adv:
602:                 js = adv["json_schema"]
603:                 self.enable_json_schema_checkbox.setChecked(js.get("enabled", False))
604:                 self._set_path_field(self.json_schema_line_edit, js.get("path", ""))
605: 
606:             self._apply_combo_param(
607:                 adv,
608:                 "rope_scaling",
609:                 self.enable_rope_scaling_checkbox,
610:                 self.rope_scaling_combobox,
611:             )
612:             self._apply_param(
613:                 adv,
614:                 "rope_freq_base",
615:                 self.enable_rope_freq_base_checkbox,
616:                 self.rope_freq_base_spinbox,
617:             )
618:             self._apply_param(
619:                 adv,
620:                 "rope_freq_scale",
621:                 self.enable_rope_freq_scale_checkbox,
622:                 self.rope_freq_scale_spinbox,
623:             )
624: 
625:         # Other settings
626:         if "context_size" in config:
627:             ctx_size = config["context_size"]
628:             for i in range(self.model_context_size.count()):
629:                 if int(self.model_context_size.itemData(i, Qt.UserRole)) == ctx_size:
630:                     self.model_context_size.setCurrentIndex(i)
631:                     break
632: 
633:         if "more_options" in config:
634:             self.more_options_line_edit.setText(config["more_options"])
635: 
636:         if "no_mmproj_offload" in config:
637:             self.no_mmproj_offload_checkbox.setChecked(
638:                 bool(config["no_mmproj_offload"])
639:             )
640: 
641:     def _set_path_field(self, line_edit, path: str) -> None:
642:         """Set a path field with full path stored and short filename displayed.
643: 
644:         Args:
645:             line_edit: The QLineEdit widget to update.
646:             path: The full file path to set.
647:         """
648:         if path:
649:             line_edit.setProperty("fullPath", path)
650:             line_edit.setText(path.rsplit("/", 1)[-1])
651:         else:
652:             line_edit.setProperty("fullPath", "")
653:             line_edit.setText("")
654: 
655:     def _apply_param(self, params: dict, name: str, checkbox, spinbox) -> None:
656:         """Apply an enabled+value parameter pair to a checkbox and spinbox.
657: 
658:         Args:
659:             params: Dictionary containing the parameter data.
660:             name: Parameter name key in the dictionary.
661:             checkbox: The QCheckBox widget.
662:             spinbox: The QSpinBox/QDoubleSpinBox widget.
663:         """
664:         if name in params:
665:             param = params[name]
666:             if isinstance(param, dict):
667:                 checkbox.setChecked(param.get("enabled", False))
668:                 spinbox.setValue(param.get("value", spinbox.value()))
669:             else:
670:                 # Legacy format: just a value
671:                 checkbox.setChecked(True)
672:                 spinbox.setValue(param)
673: 
674:     def _apply_combo_param(self, params: dict, name: str, checkbox, combobox) -> None:
675:         """Apply an enabled+value parameter pair to a checkbox and combobox.
676: 
677:         Args:
678:             params: Dictionary containing the parameter data.
679:             name: Parameter name key in the dictionary.
680:             checkbox: The QCheckBox widget.
681:             combobox: The QComboBox widget.
682:         """
683:         if name in params:
684:             param = params[name]
685:             if isinstance(param, dict):
686:                 checkbox.setChecked(param.get("enabled", False))
687:                 text = param.get("value", "")
688:                 index = combobox.findText(text)
689:                 if index >= 0:
690:                     combobox.setCurrentIndex(index)
691:             else:
692:                 # Legacy format: just a value
693:                 checkbox.setChecked(True)
694:                 index = combobox.findText(str(param))
695:                 if index >= 0:
696:                     combobox.setCurrentIndex(index)
697: 
698:     # ------------------------------------------------------------------
699:     # Window lifecycle
700:     # ------------------------------------------------------------------
701: 
702:     def closeEvent(self, event) -> None:
703:         """Save last session settings when the window is closed.
704: 
705:         Uses QSettings to persist basic connection settings and window
706:         geometry so they are restored on the next launch.
707:         """
708:         self._save_last_session()
709:         super().closeEvent(event)
710: 
711:     def _save_last_session(self) -> None:
712:         """Save last-used settings to QSettings for session restoration."""
713:         settings = QSettings("LLamaLauncher", "LlamaLaunchApp")
714:         settings.setValue(
715:             "lastModelPath", self.model_path_edit.property("fullPath") or ""
716:         )
717:         settings.setValue("host", self.host_line_edit.text())
718:         settings.setValue("port", self.port_line_edit.text())
719:         settings.setValue("windowGeometry", self.saveGeometry())
720: 
721:     def _load_last_session(self) -> None:
722:         """Restore last-used settings from QSettings.
723: 
724:         Pre-populates the UI with the host, port, and model path
725:         from the previous session so the user doesn't have to re-enter them.
726:         """
727:         settings = QSettings("LLamaLauncher", "LlamaLaunchApp")
728: 
729:         # Restore window geometry if saved
730:         geometry = settings.value("windowGeometry")
731:         if geometry:
732:             self.restoreGeometry(geometry)
733: 
734:         # Restore server settings
735:         host = settings.value("host", "127.0.0.1")
736:         port = settings.value("port", "8080")
737:         self.host_line_edit.setText(host)
738:         self.port_line_edit.setText(port)
739: 
740:         # Restore model path if available
741:         last_model_path = settings.value("lastModelPath", "")
742:         if last_model_path:
743:             self._set_path_field(self.model_path_edit, last_model_path)
744: 
745:     # ------------------------------------------------------------------
746:     # Signal connections
747:     # ------------------------------------------------------------------
748: 
749:     def _connect_signals(self) -> None:
750:         """Connect widget signals to their slot methods."""
751:         self.select_model_button.clicked.connect(self._select_model)
752:         self.select_mmproj_button.clicked.connect(self._select_mmproj)
753:         self.select_draft_model_button.clicked.connect(self._select_draft_model)
754:         self.select_json_schema_button.clicked.connect(self._select_json_schema)
755:         self.model_path_edit.textChanged.connect(self._on_model_selection_changed)
756:         self.launch_button.clicked.connect(self._toggle_launch)
757: 
758:     # ------------------------------------------------------------------
759:     # Slots
760:     # ------------------------------------------------------------------
761: 
762:     def _select_model(self) -> None:
763:         """Open a file dialog to select a .gguf model file.
764: 
765:         Stores the full path as a custom property on the line edit
766:         (accessible via ``getProperty("fullPath")``) while displaying
767:         only the short filename in the UI.
768:         """
769:         file_path, _ = QFileDialog.getOpenFileName(
770:             self,
771:             "Select GGUF Model",
772:             "",
773:             "GGUF Files (*.gguf)",
774:         )
775:         if file_path:
776:             self._model_path = file_path
777:             self.model_path_edit.setProperty("fullPath", file_path)
778:             self.model_path_edit.setText(file_path.rsplit("/", 1)[-1])
779:             self._on_model_selection_changed()
780: 
781:     def _select_mmproj(self) -> None:
782:         """Open a file dialog to select a .gguf mmproj file.
783: 
784:         Stores the full path as a custom property on the line edit
785:         (accessible via ``getProperty("fullPath")``) while displaying
786:         only the short filename in the UI.
787:         """
788:         file_path, _ = QFileDialog.getOpenFileName(
789:             self,
790:             "Select Multi-Modal Projector",
791:             "",
792:             "GGUF Files (*.gguf)",
793:         )
794:         if file_path:
795:             self._mmproj_path = file_path
796:             self.mmproj_path_edit.setProperty("fullPath", file_path)
797:             self.mmproj_path_edit.setText(file_path.rsplit("/", 1)[-1])
798: 
799:     def _select_draft_model(self) -> None:
800:         """Open a file dialog to select a draft model .gguf file.
801: 
802:         Stores the full path as a custom property on the line edit
803:         (accessible via ``getProperty("fullPath")``) while displaying
804:         only the short filename in the UI.
805:         """
806:         file_path, _ = QFileDialog.getOpenFileName(
807:             self,
808:             "Select Draft Model",
809:             "",
810:             "GGUF Files (*.gguf)",
811:         )
812:         if file_path:
813:             self.draft_model_line_edit.setProperty("fullPath", file_path)
814:             self.draft_model_line_edit.setText(file_path.rsplit("/", 1)[-1])
815: 
816:     def _select_json_schema(self) -> None:
817:         """Open a file dialog to select a JSON schema file.
818: 
819:         Stores the full path as a custom property on the line edit
820:         (accessible via ``getProperty("fullPath")``) while displaying
821:         only the short filename in the UI.
822:         """
823:         file_path, _ = QFileDialog.getOpenFileName(
824:             self,
825:             "Select JSON Schema",
826:             "",
827:             "JSON Files (*.json)",
828:         )
829:         if file_path:
830:             self.json_schema_line_edit.setProperty("fullPath", file_path)
831:             self.json_schema_line_edit.setText(file_path.rsplit("/", 1)[-1])
832: 
833:     def _on_model_selection_changed(self) -> None:
834:         """Enable launch button when a model is selected, disable otherwise."""
835:         has_model = bool(self.model_path_edit.property("fullPath"))
836:         is_running = self._process.state() == QProcess.Running
837:         self.launch_button.setEnabled(has_model and not is_running)
838: 
839:     def _toggle_launch(self) -> None:
840:         """Launch or stop the llama-server based on current process state."""
841:         if self._process.state() == QProcess.Running:
842:             self._stop_model()
843:         else:
844:             self._launch_model()
845: 
846:     def _stop_model(self) -> None:
847:         """Stop the llama-server gracefully.
848: 
849:         Sends SIGTERM (like pressing Ctrl+C) so the server can shut down
850:         cleanly. If it does not stop within 2 seconds, falls back to
851:         SIGKILL.
852:         """
853:         self._process.terminate()
854:         self.output_display.appendPlainText("Stopping server... (sent SIGTERM)")
855:         QTimer.singleShot(2000, self._force_kill_if_needed)
856: 
857:     def _force_kill_if_needed(self) -> None:
858:         """Force kill the process if graceful termination did not work."""
859:         if self._process.state() == QProcess.Running:
860:             self.output_display.appendPlainText(
861:                 "Server didn't stop gracefully. Force killing..."
862:             )
863:             self._process.kill()
864: 
865:     def _reset_launch_button(self) -> None:
866:         """Reset the launch button to its default state."""
867:         self.launch_button.setText("LAUNCH")
868:         self._on_model_selection_changed()
869: 
870:     def _launch_model(self) -> None:
871:         """Launch the llama-server binary with current configuration.
872: 
873:         Builds the command-line arguments from the UI fields and starts
874:         ``llama-server`` via QProcess.  Live stdout/stderr output is
875:         streamed into ``output_display``.
876:         """
877:         model_path = self.model_path_edit.property("fullPath")
878:         if not model_path:
879:             self.output_display.appendPlainText("Error: no model selected.")
880:             return
881: 
882:         temperature = self.temperature_spinbox.value()
883:         top_p = self.top_p_spinbox.value()
884:         top_k = self.top_k_spinbox.value()
885:         min_p = self.min_p_spinbox.value()
886:         typical_p = self.typical_p_spinbox.value()
887:         repeat_penalty = self.repeat_penalty_spinbox.value()
888:         repeat_last_n = self.repeat_last_n_spinbox.value()
889:         presence_penalty = self.presence_penalty_spinbox.value()
890:         frequency_penalty = self.frequency_penalty_spinbox.value()
891: 
892:         mirostat = self.mirostat_spinbox.value()
893:         mirostat_lr = self.mirostat_lr_spinbox.value()
894:         mirostat_ent = self.mirostat_ent_spinbox.value()
895: 
896:         # Performance parameters
897:         gpu_layers = self.gpu_layers_spinbox.value()
898:         threads = self.threads_spinbox.value()
899:         threads_batch = self.threads_batch_spinbox.value()
900:         batch_size = self.batch_size_spinbox.value()
901:         ubatch_size = self.ubatch_size_spinbox.value()
902:         n_predict = self.n_predict_spinbox.value()
903:         parallel = self.parallel_spinbox.value()
904:         cache_type_k = self.cache_type_k_combobox.currentText()
905:         cache_type_v = self.cache_type_v_combobox.currentText()
906: 
907:         # Advanced Generation parameters
908:         spec_draft_n_max = self.spec_draft_n_max_spinbox.value()
909:         seed = self.seed_spinbox.value()
910:         rope_scaling = self.rope_scaling_combobox.currentText()
911:         rope_freq_base = self.rope_freq_base_spinbox.value()
912:         rope_freq_scale = self.rope_freq_scale_spinbox.value()
913: 
914:         mmproj_path = self.mmproj_path_edit.property("fullPath")
915:         no_mmproj_offload = self.no_mmproj_offload_checkbox.isChecked()
916:         api_key = (
917:             self.api_key_line_edit.text() if self.api_key_line_edit.text() else "12345"
918:         )
919: 
920:         # Build command: llama-server --model ... (conditional sampling params) ...
921:         cmd = [
922:             "llama-server",
923:             "--model",
924:             model_path,
925:             "--api-key",
926:             api_key,
927:         ]
928: 
929:         if self.enable_temperature_checkbox.isChecked():
930:             cmd.extend(["--temp", str(temperature)])
931:         if self.enable_top_p_checkbox.isChecked():
932:             cmd.extend(["--top-p", str(top_p)])
933:         if self.enable_top_k_checkbox.isChecked():
934:             cmd.extend(["--top-k", str(top_k)])
935:         if self.enable_min_p_checkbox.isChecked():
936:             cmd.extend(["--min-p", str(min_p)])
937:         if self.enable_typical_p_checkbox.isChecked():
938:             cmd.extend(["--typical-p", str(typical_p)])
939:         if self.enable_repeat_penalty_checkbox.isChecked():
940:             cmd.extend(["--repeat-penalty", str(repeat_penalty)])
941:         if self.enable_repeat_last_n_checkbox.isChecked():
942:             cmd.extend(["--repeat-last-n", str(repeat_last_n)])
943:         if self.enable_presence_penalty_checkbox.isChecked():
944:             cmd.extend(["--presence-penalty", str(presence_penalty)])
945:         if self.enable_frequency_penalty_checkbox.isChecked():
946:             cmd.extend(["--frequency-penalty", str(frequency_penalty)])
947:         if self.enable_mirostat_checkbox.isChecked():
948:             cmd.extend(["--mirostat", str(mirostat)])
949:         if self.enable_mirostat_lr_checkbox.isChecked():
950:             cmd.extend(["--mirostat-lr", str(mirostat_lr)])
951:         if self.enable_mirostat_ent_checkbox.isChecked():
952:             cmd.extend(["--mirostat-ent", str(mirostat_ent)])
953: 
954:         # Performance parameters
955:         if self.enable_gpu_layers_checkbox.isChecked():
956:             cmd.extend(["--n-gpu-layers", str(gpu_layers)])
957:         if self.enable_threads_checkbox.isChecked():
958:             cmd.extend(["--threads", str(threads)])
959:         if self.enable_threads_batch_checkbox.isChecked():
960:             cmd.extend(["--threads-batch", str(threads_batch)])
961:         if self.enable_batch_size_checkbox.isChecked():
962:             cmd.extend(["--batch-size", str(batch_size)])
963:         if self.enable_ubatch_size_checkbox.isChecked():
964:             cmd.extend(["--ubatch-size", str(ubatch_size)])
965:         if self.enable_n_predict_checkbox.isChecked():
966:             cmd.extend(["--n-predict", str(n_predict)])
967:         # Flash Attention: always pass the selected value (default auto)
968:         flash_attn = self.flash_attn_combobox.currentText()
969:         cmd.extend(["--flash-attn", flash_attn])
970:         if self.enable_cache_type_k_checkbox.isChecked():
971:             cmd.extend(["--cache-type-k", cache_type_k])
972:         if self.enable_cache_type_v_checkbox.isChecked():
973:             cmd.extend(["--cache-type-v", cache_type_v])
974:         if self.enable_mmap_checkbox.isChecked():
975:             cmd.append("--mmap")
976:         if self.enable_mlock_checkbox.isChecked():
977:             cmd.append("--mlock")
978:         if self.enable_cont_batching_checkbox.isChecked():
979:             cmd.append("--cont-batching")
980:         if self.enable_parallel_checkbox.isChecked():
981:             cmd.extend(["--parallel", str(parallel)])
982: 
983:         # Advanced Generation parameters
984:         draft_model_path = self.draft_model_line_edit.property("fullPath")
985:         if self.enable_draft_model_checkbox.isChecked() and draft_model_path:
986:             cmd.extend(["--draft-model", draft_model_path])
987:         if self.enable_spec_draft_n_max_checkbox.isChecked():
988:             cmd.extend(["--spec-draft-n-max", str(spec_draft_n_max)])
989:         if self.enable_seed_checkbox.isChecked():
990:             cmd.extend(["--seed", str(seed)])
991:         grammar_text = self.grammar_line_edit.text().strip()
992:         if self.enable_grammar_checkbox.isChecked() and grammar_text:
993:             cmd.extend(["--grammar", grammar_text])
994:         json_schema_path = self.json_schema_line_edit.property("fullPath")
995:         if self.enable_json_schema_checkbox.isChecked() and json_schema_path:
996:             cmd.extend(["--json-schema", json_schema_path])
997:         if self.enable_rope_scaling_checkbox.isChecked():
998:             cmd.extend(["--rope-scaling", rope_scaling])
999:         if self.enable_rope_freq_base_checkbox.isChecked():
1000:             cmd.extend(["--rope-freq-base", str(rope_freq_base)])
1001:         if self.enable_rope_freq_scale_checkbox.isChecked():
1002:             cmd.extend(["--rope-freq-scale", str(rope_freq_scale)])
1003: 
1004:         host = self.host_line_edit.text() or self._host
1005:         port_str = self.port_line_edit.text() or str(self._port)
1006:         try:
1007:             port = int(port_str)
1008:         except ValueError:
1009:             port = self._port
1010: 
1011:         if mmproj_path:
1012:             cmd.extend(["--mmproj", mmproj_path])
1013:             if no_mmproj_offload:
1014:                 cmd.append("--no-mmproj-offload")
1015: 
1016:         # Extra user-supplied flags from the more options line edit
1017:         extra = self.more_options_line_edit.text().strip()
1018:         if extra:
1019:             cmd.extend(extra.split())
1020: 
1021:         # Context size: only pass --ctx-size when a specific value is selected
1022:         ctx_size = self.model_context_size.itemData(
1023:             self.model_context_size.currentIndex(),
1024:             Qt.UserRole,
1025:         )
1026:         if ctx_size is not None and int(ctx_size) > 0:
1027:             cmd.extend(["--ctx-size", str(ctx_size)])
1028: 
1029:         cmd.extend(["--host", host, "--port", str(port)])
1030: 
1031:         self._server_url = f"http://{host}:{port}"
1032:         self._auto_refresh_done = False
1033: 
1034:         self.output_display.clear()
1035:         self.output_display.appendPlainText(f"Launching: {' '.join(cmd)}\n---\n")
1036: 
1037:         # Use two-argument form: program + arguments list (args must NOT include the program)
1038:         self._process.start(cmd[0], cmd[1:])
1039:         self.launch_button.setText("STOP")
1040: 
1041:         # Update web view to point to the server
1042:         server_url = f"http://{host}:{port}"
1043:         self.server_web_view.setUrl(server_url)
1044: 
1045:     # ------------------------------------------------------------------
1046:     # QProcess output slots
1047:     # ------------------------------------------------------------------
1048: 
1049:     def _on_stdout(self) -> None:
1050:         """Append stdout from the child process to the output display.
1051: 
1052:         Also watches for the server URL pattern (http://HOST:PORT) in the
1053:         output and auto-refreshes the web view once the server is ready.
1054:         """
1055:         data = (
1056:             self._process.readAllStandardOutput()
1057:             .data()
1058:             .decode("utf-8", errors="replace")
1059:         )
1060:         if data:
1061:             self.output_display.appendPlainText(data)
1062:             self._check_and_refresh()
1063: 
1064:     def _on_stderr(self) -> None:
1065:         """Append stderr from the child process to the output display.
1066: 
1067:         Also watches for the server URL pattern (http://HOST:PORT) in the
1068:         output and auto-refreshes the web view once the server is ready.
1069:         """
1070:         data = (
1071:             self._process.readAllStandardError()
1072:             .data()
1073:             .decode("utf-8", errors="replace")
1074:         )
1075:         if data:
1076:             self.output_display.appendPlainText(data)
1077:             self._check_and_refresh()
1078: 
1079:     def _check_and_refresh(self) -> None:
1080:         """Check output for server URL and refresh web view once ready.
1081: 
1082:         Scans the full text of the output display for an HTTP URL pattern.
1083:         When found (and not already refreshed), schedules a one-shot timer
1084:         to reload the web view so the Qt event loop is not blocked.
1085:         """
1086:         if self._auto_refresh_done:
1087:             return
1088: 
1089:         text = self.output_display.toPlainText()
1090:         match = re.search(r"http://[\w.-]+:\d+", text)
1091:         if match:
1092:             self._auto_refresh_done = True
1093:             QTimer.singleShot(0, self._refresh_web_view)
1094: 
1095:     def _refresh_web_view(self) -> None:
1096:         """Reload the server web view to fetch the freshly started server."""
1097:         url = QUrl(self._server_url)
1098:         self.server_web_view.setUrl(url)
1099:         self.output_display.appendPlainText(
1100:             f"\n[Server ready — refreshed web view at {self._server_url}]"
1101:         )
1102: 
1103:     def _on_error(self, error: QProcess.ProcessError) -> None:
1104:         """Called when the process encounters an error (e.g. not found)."""
1105:         msg = f"Error launching process: {error}"
1106:         self.output_display.appendPlainText(msg)
1107:         self._reset_launch_button()
1108: 
1109:     def _on_finished(self, code: int, status: QProcess.ExitStatus) -> None:
1110:         """Called when the child process exits."""
1111:         if status == QProcess.ExitStatus.NormalExit:
1112:             self.output_display.appendPlainText(
1113:                 f"\n--- Process exited with code {code} ---"
1114:             )
1115:         else:
1116:             self.output_display.appendPlainText(
1117:                 f"\n--- Process terminated abnormally (code {code}) ---"
1118:             )
1119:         self._reset_launch_button()
1120: 
1121: 
1122: if __name__ == "__main__":
1123:     parser = argparse.ArgumentParser(description="Llama model launcher application.")
1124:     parser.add_argument(
1125:         "--host",
1126:         default="127.0.0.1",
1127:         help="Host address for the server (default: 127.0.0.1)",
1128:     )
1129:     parser.add_argument(
1130:         "--port", type=int, default=8080, help="Port for the server (default: 8080)"
1131:     )
1132:     parser.add_argument(
1133:         "-c",
1134:         "--ctx-size",
1135:         type=int,
1136:         default=None,
1137:         help="Model context size in tokens (e.g. 4096, 8192, 32768). Overrides the UI combo box.",
1138:     )
1139:     args = parser.parse_args()
1140: 
1141:     app = QApplication(sys.argv)
1142:     window = LlamaLaunchApp(host=args.host, port=args.port, ctx_size=args.ctx_size)
1143:     window.show()
1144:     sys.exit(app.exec())

(End of file - total 1144 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Volumes/teaching/Code/LLamaLauncher/ui_loader.py"
}
```

**Output:**
```
<path>/Volumes/teaching/Code/LLamaLauncher/ui_loader.py</path>
<type>file</type>
<content>
1: from pathlib import Path
2: from typing import TypeVar, Union
3: 
4: from PySide6.QtCore import QFile
5: from PySide6.QtUiTools import QUiLoader
6: from PySide6.QtWidgets import QDialog, QLayout, QMainWindow, QVBoxLayout, QWidget
7: 
8: T = TypeVar("T", bound=QWidget)
9: 
10: 
11: def load_ui(ui_file_path: Union[str, Path], parent: T) -> QWidget:
12:     """Load a .ui file and set up the widget connections.
13: 
14:     Parameters :
15:         ui_file_path : Union[str, Path]
16:             Path to the .ui file to load.
17:         parent : T
18:             The parent widget to load the UI into.
19: 
20:     Returns :
21:         The loaded widget with all children accessible as attributes.
22:     """
23:     loader = QUiLoader()
24:     ui_file = QFile(ui_file_path)
25:     if not ui_file.open(QFile.ReadOnly):
26:         raise RuntimeError(f"Cannot open UI file: {ui_file_path}")
27: 
28:     loaded_ui = loader.load(ui_file, parent)
29:     ui_file.close()
30: 
31:     if loaded_ui is None:
32:         raise RuntimeError(f"Failed to load UI file: {ui_file_path}")
33: 
34:     for widget in loaded_ui.findChildren(QWidget):
35:         name = widget.objectName()
36:         if name:
37:             setattr(parent, name, widget)
38: 
39:     for layout in loaded_ui.findChildren(QLayout):
40:         name = layout.objectName()
41:         if name:
42:             setattr(parent, name, layout)
43: 
44:     # Also capture the top-level layout if it wasn't found by findChildren
45:     main_layout = loaded_ui.layout()
46:     if main_layout:
47:         name = main_layout.objectName()
48:         if name and not hasattr(parent, name):
49:             setattr(parent, name, main_layout)
50: 
51:     if isinstance(parent, QDialog):
52:         if loaded_ui.layout():
53:             parent.setLayout(loaded_ui.layout())
54:         parent.setWindowTitle(loaded_ui.windowTitle())
55:         parent.resize(loaded_ui.size())
56:     elif isinstance(parent, QMainWindow):
57:         parent.setCentralWidget(loaded_ui)
58:         parent.setWindowTitle(loaded_ui.windowTitle())
59:         parent.resize(loaded_ui.size())
60:     else:
61:         # Plain QWidget: embed loaded_ui via a zero-margin layout so its
62:         # contents fill the parent window.
63:         container = QVBoxLayout(parent)
64:         container.setContentsMargins(0, 0, 0, 0)
65:         container.addWidget(loaded_ui)
66:         parent.setWindowTitle(loaded_ui.windowTitle())
67:         parent.resize(loaded_ui.size())
68: 
69:     return loaded_ui

(End of file - total 69 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Volumes/teaching/Code/LLamaLauncher/process_command.py"
}
```

**Output:**
```
<path>/Volumes/teaching/Code/LLamaLauncher/process_command.py</path>
<type>file</type>
<content>
1: """Pure command-building logic for llama-server process.
2: 
3: Extracted from main.py to enable unit testing without Qt dependencies.
4: Accepts a configuration dictionary and returns a list of command arguments
5: suitable for QProcess or subprocess.
6: """
7: 
8: from typing import Any
9: 
10: 
11: class ProcessCommandBuilder:
12:     """Build llama-server command from configuration dictionary.
13: 
14:     Takes a config dict (from ConfigCollector.collect_config()) and returns
15:     a list of command arguments suitable for QProcess or subprocess.
16: 
17:     Attributes:
18:         config: Configuration dictionary containing files, server, sampling,
19:             performance, and advanced parameter settings.
20:     """
21: 
22:     def __init__(self, config: dict[str, Any]) -> None:
23:         """Initialize the builder with configuration.
24: 
25:         Args:
26:             config: Configuration dictionary from ConfigCollector.
27:         """
28:         self._config = config
29: 
30:     def build_command(self) -> list[str]:
31:         """Build the complete llama-server command.
32: 
33:         Returns:
34:             List of command arguments starting with 'llama-server'.
35:         """
36:         cmd: list[str] = []
37: 
38:         # 3.1 Base command
39:         cmd.extend(["llama-server", "--model", self._config["files"]["model_path"]])
40: 
41:         api_key = self._config["server"]["api_key"] or "12345"
42:         cmd.extend(["--api-key", api_key])
43: 
44:         # 3.2 Sampling parameters (conditional)
45:         sampling = self._config["sampling"]
46: 
47:         if sampling["temperature"]["enabled"]:
48:             cmd.extend(["--temp", str(sampling["temperature"]["value"])])
49:         if sampling["top_p"]["enabled"]:
50:             cmd.extend(["--top-p", str(sampling["top_p"]["value"])])
51:         if sampling["top_k"]["enabled"]:
52:             cmd.extend(["--top-k", str(sampling["top_k"]["value"])])
53:         if sampling["min_p"]["enabled"]:
54:             cmd.extend(["--min-p", str(sampling["min_p"]["value"])])
55:         if sampling["typical_p"]["enabled"]:
56:             cmd.extend(["--typical-p", str(sampling["typical_p"]["value"])])
57:         if sampling["repeat_penalty"]["enabled"]:
58:             cmd.extend(["--repeat-penalty", str(sampling["repeat_penalty"]["value"])])
59:         if sampling["repeat_last_n"]["enabled"]:
60:             cmd.extend(["--repeat-last-n", str(sampling["repeat_last_n"]["value"])])
61:         if sampling["presence_penalty"]["enabled"]:
62:             cmd.extend(
63:                 ["--presence-penalty", str(sampling["presence_penalty"]["value"])]
64:             )
65:         if sampling["frequency_penalty"]["enabled"]:
66:             cmd.extend(
67:                 ["--frequency-penalty", str(sampling["frequency_penalty"]["value"])]
68:             )
69:         if sampling["mirostat"]["enabled"]:
70:             cmd.extend(["--mirostat", str(sampling["mirostat"]["value"])])
71:         if sampling["mirostat_lr"]["enabled"]:
72:             cmd.extend(["--mirostat-lr", str(sampling["mirostat_lr"]["value"])])
73:         if sampling["mirostat_ent"]["enabled"]:
74:             cmd.extend(["--mirostat-ent", str(sampling["mirostat_ent"]["value"])])
75: 
76:         # 3.5 Server and Model Parameters
77:         # MMProj parameters
78:         mmproj_path = self._config["files"]["mmproj_path"]
79:         if mmproj_path:
80:             cmd.extend(["--mmproj", mmproj_path])
81:             if self._config.get("no_mmproj_offload", False):
82:                 cmd.append("--no-mmproj-offload")
83: 
84:         # Extra flags from more_options
85:         more_options = self._config.get("more_options", "")
86:         if more_options:
87:             cmd.extend(more_options.split())
88: 
89:         # Context size
90:         context_size = self._config.get("context_size", 0)
91:         if context_size and context_size > 0:
92:             cmd.extend(["--ctx-size", str(context_size)])
93: 
94:         # Server settings
95:         server = self._config["server"]
96:         cmd.extend(["--host", server["host"], "--port", str(server["port"])])
97: 
98:         return cmd

(End of file - total 98 lines)
</content>
```

**Tool: bash**

**Input:**
```json
{
  "command": "ls -la tests/*.py",
  "description": "List test files"
}
```

**Output:**
```
-rw-r--r--@ 1 jmacey  admin      0 15 Jun 20:31 tests/__init__.py
-rw-r--r--@ 1 jmacey  admin  14253 16 Jun 12:37 tests/config_collector.py
-rw-r--r--@ 1 jmacey  admin   1559 16 Jun 20:39 tests/conftest.py
-rw-r--r--@ 1 jmacey  admin  19868 16 Jun 20:39 tests/test_config.py
-rw-r--r--@ 1 jmacey  admin  15628 18 Jun 09:28 tests/test_edge_cases.py
-rw-r--r--@ 1 jmacey  admin  11591 16 Jun 22:21 tests/test_file_selection.py
-rw-r--r--@ 1 jmacey  admin  10129 16 Jun 20:21 tests/test_helper_methods.py
-rw-r--r--@ 1 jmacey  admin  19429 18 Jun 08:23 tests/test_lifecycle.py
-rw-r--r--@ 1 jmacey  admin  25597 16 Jun 19:25 tests/test_main.py
-rw-r--r--@ 1 jmacey  admin  28628 16 Jun 21:57 tests/test_process.py
-rw-r--r--@ 1 jmacey  admin  20715 18 Jun 07:39 tests/test_signals.py
-rw-r--r--@ 1 jmacey  admin   8439 16 Jun 12:00 tests/test_ui_loader.py

```

---

## Assistant (Python-Code-Quality · Claude Sonnet 4.5 · 5.5s)

Let me now examine the test files to understand the testing approach:

**Tool: read**

**Input:**
```json
{
  "filePath": "/Volumes/teaching/Code/LLamaLauncher/tests/conftest.py"
}
```

**Output:**
```
<path>/Volumes/teaching/Code/LLamaLauncher/tests/conftest.py</path>
<type>file</type>
<content>
1: """Shared pytest fixtures LLamaLauncher test suite."""
2: 
3: import sys
4: import tempfile
5: from pathlib import Path
6: from unittest.mock import MagicMock, patch
7: 
8: import pytest
9: 
10: # Allow importing production modules from project root in tests
11: _project_root = str(Path(__file__).resolve().parent.parent)
12: if _project_root not in sys.path:
13:     sys.path.insert(0, _project_root)
14: 
15: 
16: @pytest.fixture(scope="session", autouse=True)
17: def qapp():
18:     """Provide a QApplication singleton for the test session.
19: 
20:     This fixture ensures only one QApplication instance is created
21:     across all Qt tests in the session.
22:     """
23:     from PySide6.QtWidgets import QApplication
24: 
25:     app = QApplication.instance()
26:     if app is None:
27:         app = QApplication([])
28:     yield app
29:     # Cleanup is handled by QApplication at session end
30: 
31: 
32: @pytest.fixture()
33: def temp_dir():
34:     """Provide a temporary directory that is cleaned up after each test.
35: 
36:     Returns the path to the temporary directory and removes it afterward.
37:     """
38:     with tempfile.TemporaryDirectory() as tmpdir:
39:         yield tmpdir
40: 
41: 
42: @pytest.fixture()
43: def mock_qprocess():
44:     """Provide a mocked QProcess for testing process-related code.
45: 
46:     Returns a MagicMock configured to mimic basic QProcess behavior.
47:     """
48:     with patch("PySide6.QtCore.QProcess") as mock:
49:         process = MagicMock()
50:         process.state.return_value = 0  # NotRunning
51:         process.readAllStandardOutput.return_value = b""
52:         process.readAllStandardError.return_value = b""
53:         mock.return_value = process
54:         yield process

(End of file - total 54 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Volumes/teaching/Code/LLamaLauncher/tests/config_collector.py"
}
```

**Output:**
```
<path>/Volumes/teaching/Code/LLamaLauncher/tests/config_collector.py</path>
<type>file</type>
<content>
1: """Pure configuration collection logic.
2: 
3: Extracted from main.py to enable unit testing without Qt dependencies.
4: Accepts widget-like objects through dependency injection and returns
5: a plain dictionary suitable for JSON serialization.
6: """
7: 
8: from dataclasses import dataclass, field
9: from typing import Any
10: 
11: 
12: @dataclass(slots=True)
13: class ConfigCollector:
14:     """Collect configuration values from UI widget-like objects.
15: 
16:     Each widget attribute is a simple object with methods like .text(),
17:     .isChecked(), .value(), .property(), .currentText(), .currentIndex(),
18:     and .itemData() that mirror the Qt widget interface.
19: 
20:     Attributes:
21:         version_edit: Widget providing the version string via .text().
22:         model_path_edit: Path edit with .property("fullPath").
23:         mmproj_path_edit: Path edit for mmproj model path.
24:         draft_model_line_edit: Path edit for draft model path.
25:         json_schema_line_edit: Path edit for JSON schema path.
26:         host_line_edit: Widget providing server host via .text().
27:         port_line_edit: Widget providing server port text (digits or fallback).
28:         api_key_line_edit: Widget providing API key via .text().
29:         enable_temperature_checkbox / temperature_spinbox: Sampling param.
30:         enable_top_p_checkbox / top_p_spinbox: Sampling param.
31:         enable_top_k_checkbox / top_k_spinbox: Sampling param.
32:         enable_min_p_checkbox / min_p_spinbox: Sampling param.
33:         enable_typical_p_checkbox / typical_p_spinbox: Sampling param.
34:         enable_repeat_penalty_checkbox / repeat_penalty_spinbox: Sampling param.
35:         enable_repeat_last_n_checkbox / repeat_last_n_spinbox: Sampling param.
36:         enable_presence_penalty_checkbox / presence_penalty_spinbox: Sampling param.
37:         enable_frequency_penalty_checkbox / frequency_penalty_spinbox: Sampling param.
38:         enable_mirostat_checkbox / mirostat_spinbox: Sampling param.
39:         enable_mirostat_lr_checkbox / mirostat_lr_spinbox: Sampling param.
40:         enable_mirostat_ent_checkbox / mirostat_ent_spinbox: Sampling param.
41:         enable_gpu_layers_checkbox / gpu_layers_spinbox: Performance param.
42:         enable_threads_checkbox / threads_spinbox: Performance param.
43:         enable_threads_batch_checkbox / threads_batch_spinbox: Performance param.
44:         enable_batch_size_checkbox / batch_size_spinbox: Performance param.
45:         enable_ubatch_size_checkbox / ubatch_size_spinbox: Performance param.
46:         enable_n_predict_checkbox / n_predict_spinbox: Performance param.
47:         enable_parallel_checkbox / parallel_spinbox: Performance param.
48:         flash_attn_combobox: Combobox for flash attention setting text.
49:         enable_cache_type_k_checkbox / cache_type_k_combobox: Performance param.
50:         enable_cache_type_v_checkbox / cache_type_v_combobox: Performance param.
51:         enable_mmap_checkbox: Boolean mmap setting.
52:         enable_mlock_checkbox: Boolean mlock setting.
53:         enable_cont_batching_checkbox: Boolean cont_batching setting.
54:         enable_draft_model_checkbox / draft_model_line_edit: Advanced path+enabled.
55:         enable_spec_draft_n_max_checkbox / spec_draft_n_max_spinbox: Advanced param.
56:         enable_seed_checkbox / seed_spinbox: Advanced param.
57:         enable_grammar_checkbox / grammar_line_edit: Advanced path+enabled.
58:         enable_json_schema_checkbox / json_schema_line_edit: Advanced path+enabled.
59:         enable_rope_scaling_checkbox / rope_scaling_combobox: Advanced combobox.
60:         enable_rope_freq_base_checkbox / rope_freq_base_spinbox: Advanced param.
61:         enable_rope_freq_scale_checkbox / rope_freq_scale_spinbox: Advanced param.
62:         model_context_size: Combobox providing context size via .itemData(index, role).
63:         more_options_line_edit: Widget providing extra options text.
64:         no_mmproj_offload_checkbox: Boolean no_mmproj_offload setting.
65:     """
66: 
67:     # Files/Paths
68:     version_edit: Any = field(default=None)
69:     model_path_edit: Any = field(default=None)
70:     mmproj_path_edit: Any = field(default=None)
71:     draft_model_line_edit: Any = field(default=None)
72:     json_schema_line_edit: Any = field(default=None)
73: 
74:     # Server
75:     host_line_edit: Any = field(default=None)
76:     port_line_edit: Any = field(default=None)
77:     api_key_line_edit: Any = field(default=None)
78: 
79:     # Sampling parameters (12 pairs)
80:     enable_temperature_checkbox: Any = field(default=None)
81:     temperature_spinbox: Any = field(default=None)
82:     enable_top_p_checkbox: Any = field(default=None)
83:     top_p_spinbox: Any = field(default=None)
84:     enable_top_k_checkbox: Any = field(default=None)
85:     top_k_spinbox: Any = field(default=None)
86:     enable_min_p_checkbox: Any = field(default=None)
87:     min_p_spinbox: Any = field(default=None)
88:     enable_typical_p_checkbox: Any = field(default=None)
89:     typical_p_spinbox: Any = field(default=None)
90:     enable_repeat_penalty_checkbox: Any = field(default=None)
91:     repeat_penalty_spinbox: Any = field(default=None)
92:     enable_repeat_last_n_checkbox: Any = field(default=None)
93:     repeat_last_n_spinbox: Any = field(default=None)
94:     enable_presence_penalty_checkbox: Any = field(default=None)
95:     presence_penalty_spinbox: Any = field(default=None)
96:     enable_frequency_penalty_checkbox: Any = field(default=None)
97:     frequency_penalty_spinbox: Any = field(default=None)
98:     enable_mirostat_checkbox: Any = field(default=None)
99:     mirostat_spinbox: Any = field(default=None)
100:     enable_mirostat_lr_checkbox: Any = field(default=None)
101:     mirostat_lr_spinbox: Any = field(default=None)
102:     enable_mirostat_ent_checkbox: Any = field(default=None)
103:     mirostat_ent_spinbox: Any = field(default=None)
104: 
105:     # Performance parameters
106:     enable_gpu_layers_checkbox: Any = field(default=None)
107:     gpu_layers_spinbox: Any = field(default=None)
108:     enable_threads_checkbox: Any = field(default=None)
109:     threads_spinbox: Any = field(default=None)
110:     enable_threads_batch_checkbox: Any = field(default=None)
111:     threads_batch_spinbox: Any = field(default=None)
112:     enable_batch_size_checkbox: Any = field(default=None)
113:     batch_size_spinbox: Any = field(default=None)
114:     enable_ubatch_size_checkbox: Any = field(default=None)
115:     ubatch_size_spinbox: Any = field(default=None)
116:     enable_n_predict_checkbox: Any = field(default=None)
117:     n_predict_spinbox: Any = field(default=None)
118:     enable_parallel_checkbox: Any = field(default=None)
119:     parallel_spinbox: Any = field(default=None)
120:     flash_attn_combobox: Any = field(default=None)
121:     enable_cache_type_k_checkbox: Any = field(default=None)
122:     cache_type_k_combobox: Any = field(default=None)
123:     enable_cache_type_v_checkbox: Any = field(default=None)
124:     cache_type_v_combobox: Any = field(default=None)
125:     enable_mmap_checkbox: Any = field(default=None)
126:     enable_mlock_checkbox: Any = field(default=None)
127:     enable_cont_batching_checkbox: Any = field(default=None)
128: 
129:     # Advanced generation parameters
130:     enable_draft_model_checkbox: Any = field(default=None)
131:     enable_spec_draft_n_max_checkbox: Any = field(default=None)
132:     spec_draft_n_max_spinbox: Any = field(default=None)
133:     enable_seed_checkbox: Any = field(default=None)
134:     seed_spinbox: Any = field(default=None)
135:     enable_grammar_checkbox: Any = field(default=None)
136:     grammar_line_edit: Any = field(default=None)
137:     enable_json_schema_checkbox: Any = field(default=None)
138:     json_schema_line_edit: Any = field(default=None)
139:     enable_rope_scaling_checkbox: Any = field(default=None)
140:     rope_scaling_combobox: Any = field(default=None)
141:     enable_rope_freq_base_checkbox: Any = field(default=None)
142:     rope_freq_base_spinbox: Any = field(default=None)
143:     enable_rope_freq_scale_checkbox: Any = field(default=None)
144:     rope_freq_scale_spinbox: Any = field(default=None)
145: 
146:     # Other settings
147:     model_context_size: Any = field(default=None)
148:     more_options_line_edit: Any = field(default=None)
149:     no_mmproj_offload_checkbox: Any = field(default=None)
150: 
151:     def _path(self, widget: Any) -> str:
152:         """Get path string from a path edit widget, returning "" for empty."""
153:         val = widget.property("fullPath")
154:         return val if val else ""
155: 
156:     def _port(self, widget: Any) -> int:
157:         """Get port as int, falling back to 8080 for non-digit text."""
158:         text = widget.text()
159:         return int(text) if text.isdigit() else 8080
160: 
161:     def _param(self, checkbox: Any, spinbox: Any) -> dict[str, Any]:
162:         """Build an enabled+value parameter dict from checkbox and spinbox."""
163:         return {
164:             "enabled": checkbox.isChecked(),
165:             "value": spinbox.value(),
166:         }
167: 
168:     def _combo_param(self, checkbox: Any, combobox: Any) -> dict[str, Any]:
169:         """Build an enabled+text parameter dict from checkbox and combobox."""
170:         return {
171:             "enabled": checkbox.isChecked(),
172:             "value": combobox.currentText(),
173:         }
174: 
175:     def collect_config(self) -> dict[str, Any]:
176:         """Collect all UI widget values into a configuration dictionary.
177: 
178:         Returns:
179:             Dictionary containing all configuration values organized by category.
180:         """
181:         config: dict[str, Any] = {"version": "1.0"}
182: 
183:         # Files/Paths
184:         config["files"] = {
185:             "model_path": self._path(self.model_path_edit),
186:             "mmproj_path": self._path(self.mmproj_path_edit),
187:             "draft_model_path": self._path(self.draft_model_line_edit),
188:             "json_schema_path": self._path(self.json_schema_line_edit),
189:         }
190: 
191:         # Server
192:         config["server"] = {
193:             "host": self.host_line_edit.text(),
194:             "port": self._port(self.port_line_edit),
195:             "api_key": self.api_key_line_edit.text(),
196:         }
197: 
198:         # Sampling parameters
199:         config["sampling"] = {
200:             "temperature": self._param(
201:                 self.enable_temperature_checkbox, self.temperature_spinbox
202:             ),
203:             "top_p": self._param(self.enable_top_p_checkbox, self.top_p_spinbox),
204:             "top_k": self._param(self.enable_top_k_checkbox, self.top_k_spinbox),
205:             "min_p": self._param(self.enable_min_p_checkbox, self.min_p_spinbox),
206:             "typical_p": self._param(
207:                 self.enable_typical_p_checkbox, self.typical_p_spinbox
208:             ),
209:             "repeat_penalty": self._param(
210:                 self.enable_repeat_penalty_checkbox, self.repeat_penalty_spinbox
211:             ),
212:             "repeat_last_n": self._param(
213:                 self.enable_repeat_last_n_checkbox, self.repeat_last_n_spinbox
214:             ),
215:             "presence_penalty": self._param(
216:                 self.enable_presence_penalty_checkbox, self.presence_penalty_spinbox
217:             ),
218:             "frequency_penalty": self._param(
219:                 self.enable_frequency_penalty_checkbox, self.frequency_penalty_spinbox
220:             ),
221:             "mirostat": self._param(
222:                 self.enable_mirostat_checkbox, self.mirostat_spinbox
223:             ),
224:             "mirostat_lr": self._param(
225:                 self.enable_mirostat_lr_checkbox, self.mirostat_lr_spinbox
226:             ),
227:             "mirostat_ent": self._param(
228:                 self.enable_mirostat_ent_checkbox, self.mirostat_ent_spinbox
229:             ),
230:         }
231: 
232:         # Performance parameters
233:         config["performance"] = {
234:             "gpu_layers": self._param(
235:                 self.enable_gpu_layers_checkbox, self.gpu_layers_spinbox
236:             ),
237:             "threads": self._param(self.enable_threads_checkbox, self.threads_spinbox),
238:             "threads_batch": self._param(
239:                 self.enable_threads_batch_checkbox, self.threads_batch_spinbox
240:             ),
241:             "batch_size": self._param(
242:                 self.enable_batch_size_checkbox, self.batch_size_spinbox
243:             ),
244:             "ubatch_size": self._param(
245:                 self.enable_ubatch_size_checkbox, self.ubatch_size_spinbox
246:             ),
247:             "n_predict": self._param(
248:                 self.enable_n_predict_checkbox, self.n_predict_spinbox
249:             ),
250:             "parallel": self._param(
251:                 self.enable_parallel_checkbox, self.parallel_spinbox
252:             ),
253:             "flash_attn": self.flash_attn_combobox.currentText(),
254:             "cache_type_k": self._combo_param(
255:                 self.enable_cache_type_k_checkbox, self.cache_type_k_combobox
256:             ),
257:             "cache_type_v": self._combo_param(
258:                 self.enable_cache_type_v_checkbox, self.cache_type_v_combobox
259:             ),
260:             "mmap": self.enable_mmap_checkbox.isChecked(),
261:             "mlock": self.enable_mlock_checkbox.isChecked(),
262:             "cont_batching": self.enable_cont_batching_checkbox.isChecked(),
263:         }
264: 
265:         # Advanced Generation parameters
266:         config["advanced"] = {
267:             "draft_model": {
268:                 "enabled": self.enable_draft_model_checkbox.isChecked(),
269:                 "path": self._path(self.draft_model_line_edit),
270:             },
271:             "spec_draft_n_max": self._param(
272:                 self.enable_spec_draft_n_max_checkbox, self.spec_draft_n_max_spinbox
273:             ),
274:             "seed": self._param(self.enable_seed_checkbox, self.seed_spinbox),
275:             "grammar": {
276:                 "enabled": self.enable_grammar_checkbox.isChecked(),
277:                 "path": self._path(self.grammar_line_edit),
278:             },
279:             "json_schema": {
280:                 "enabled": self.enable_json_schema_checkbox.isChecked(),
281:                 "path": self._path(self.json_schema_line_edit),
282:             },
283:             "rope_scaling": self._combo_param(
284:                 self.enable_rope_scaling_checkbox, self.rope_scaling_combobox
285:             ),
286:             "rope_freq_base": self._param(
287:                 self.enable_rope_freq_base_checkbox, self.rope_freq_base_spinbox
288:             ),
289:             "rope_freq_scale": self._param(
290:                 self.enable_rope_freq_scale_checkbox, self.rope_freq_scale_spinbox
291:             ),
292:         }
293: 
294:         # Other settings
295:         config["context_size"] = self.model_context_size.itemData(
296:             self.model_context_size.currentIndex(), None
297:         )
298:         config["more_options"] = self.more_options_line_edit.text()
299:         config["no_mmproj_offload"] = self.no_mmproj_offload_checkbox.isChecked()
300: 
301:         return config

(End of file - total 301 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Volumes/teaching/Code/LLamaLauncher/tests/test_process.py"
}
```

**Output:**
```
<path>/Volumes/teaching/Code/LLamaLauncher/tests/test_process.py</path>
<type>file</type>
<content>
1: """Tests for ProcessCommandBuilder - building llama-server command line.
2: 
3: Phase 3: Process Command Building
4: 
5: Tests the logic that constructs the llama-server command from configuration
6: collected by ConfigCollector. Each test verifies one aspect of command building.
7: 
8: Following the Testing.md Phase 3 plan:
9: - 3.1 Base Command (llama-server + --model + --api-key)
10: - 3.2 Sampling Parameters (conditional inclusion based on checkbox state)
11: """
12: 
13: from typing import Any
14: from unittest.mock import MagicMock
15: 
16: from process_command import ProcessCommandBuilder
17: 
18: from .test_config import (
19:     MockCheckBox,
20:     MockComboBox,
21:     MockLineEdit,
22:     MockPathEdit,
23:     MockSpinBox,
24:     _make_collector,
25: )
26: 
27: # ==================================================================
28: # 3.1 Base Command
29: # ==================================================================
30: 
31: 
32: class TestBaseCommand:
33:     """3.1: Base command construction with llama-server and required flags."""
34: 
35:     def test_base_command_includes_llama_server_and_model(self) -> None:
36:         """3.1.1: Base command includes llama-server and --model flags."""
37:         config = _make_collector(
38:             model_path_edit=MockPathEdit(_full_path="/models/llama.gguf"),
39:         ).collect_config()
40:         builder = ProcessCommandBuilder(config)
41:         cmd = builder.build_command()
42: 
43:         assert "llama-server" in cmd
44:         assert "--model" in cmd
45:         model_idx = cmd.index("--model")
46:         assert cmd[model_idx + 1] == "/models/llama.gguf"
47: 
48:     def test_base_command_includes_api_key_default_when_empty(self) -> None:
49:         """3.1.2a: Base command includes --api-key with default when empty."""
50:         config = _make_collector(
51:             api_key_line_edit=MockLineEdit(""),
52:         ).collect_config()
53:         builder = ProcessCommandBuilder(config)
54:         cmd = builder.build_command()
55: 
56:         assert "--api-key" in cmd
57:         api_key_idx = cmd.index("--api-key")
58:         assert cmd[api_key_idx + 1] == "12345"
59: 
60:     def test_base_command_includes_custom_api_key(self) -> None:
61:         """3.1.2b: Base command includes --api-key with custom value when set."""
62:         config = _make_collector(
63:             api_key_line_edit=MockLineEdit("my-secret-key"),
64:         ).collect_config()
65:         builder = ProcessCommandBuilder(config)
66:         cmd = builder.build_command()
67: 
68:         assert "--api-key" in cmd
69:         api_key_idx = cmd.index("--api-key")
70:         assert cmd[api_key_idx + 1] == "my-secret-key"
71: 
72: 
73: # ==================================================================
74: # 3.2 Sampling Parameters (Conditional)
75: # ==================================================================
76: # Each sampling param is gated by its checkbox. Test enabled/disabled pairs.
77: 
78: 
79: class TestTemperatureParameter:
80:     """3.2.1-3.2.2: Temperature parameter toggling."""
81: 
82:     def test_includes_temp_when_temperature_enabled(self) -> None:
83:         """3.2.1: Includes --temp when temperature checkbox is checked."""
84:         config = _make_collector(
85:             enable_temperature_checkbox=MockCheckBox(True),
86:             temperature_spinbox=MockSpinBox(0.7),
87:         ).collect_config()
88:         builder = ProcessCommandBuilder(config)
89:         cmd = builder.build_command()
90: 
91:         assert "--temp" in cmd
92:         temp_idx = cmd.index("--temp")
93:         assert cmd[temp_idx + 1] == "0.7"
94: 
95:     def test_omits_temp_when_temperature_disabled(self) -> None:
96:         """3.2.2: Omits --temp when temperature checkbox is unchecked."""
97:         config = _make_collector(
98:             enable_temperature_checkbox=MockCheckBox(False),
99:             temperature_spinbox=MockSpinBox(0.7),
100:         ).collect_config()
101:         builder = ProcessCommandBuilder(config)
102:         cmd = builder.build_command()
103: 
104:         assert "--temp" not in cmd
105: 
106: 
107: class TestTopPParameter:
108:     """3.2.3: Top-p parameter toggling."""
109: 
110:     def test_includes_top_p_when_enabled(self) -> None:
111:         """3.2.3: Includes --top-p when top_p checkbox is checked."""
112:         config = _make_collector(
113:             enable_top_p_checkbox=MockCheckBox(True),
114:             top_p_spinbox=MockSpinBox(0.9),
115:         ).collect_config()
116:         builder = ProcessCommandBuilder(config)
117:         cmd = builder.build_command()
118: 
119:         assert "--top-p" in cmd
120:         top_p_idx = cmd.index("--top-p")
121:         assert cmd[top_p_idx + 1] == "0.9"
122: 
123:     def test_omits_top_p_when_disabled(self) -> None:
124:         """3.2.3: Omits --top-p when top_p checkbox is unchecked."""
125:         config = _make_collector(
126:             enable_top_p_checkbox=MockCheckBox(False),
127:             top_p_spinbox=MockSpinBox(0.9),
128:         ).collect_config()
129:         builder = ProcessCommandBuilder(config)
130:         cmd = builder.build_command()
131: 
132:         assert "--top-p" not in cmd
133: 
134: 
135: class TestTopKParameter:
136:     """3.2.4: Top-k parameter toggling."""
137: 
138:     def test_includes_top_k_when_enabled(self) -> None:
139:         """3.2.4: Includes --top-k when top_k checkbox is checked."""
140:         config = _make_collector(
141:             enable_top_k_checkbox=MockCheckBox(True),
142:             top_k_spinbox=MockSpinBox(40),
143:         ).collect_config()
144:         builder = ProcessCommandBuilder(config)
145:         cmd = builder.build_command()
146: 
147:         assert "--top-k" in cmd
148:         top_k_idx = cmd.index("--top-k")
149:         assert cmd[top_k_idx + 1] == "40"
150: 
151:     def test_omits_top_k_when_disabled(self) -> None:
152:         """3.2.4: Omits --top-k when top_k checkbox is unchecked."""
153:         config = _make_collector(
154:             enable_top_k_checkbox=MockCheckBox(False),
155:             top_k_spinbox=MockSpinBox(40),
156:         ).collect_config()
157:         builder = ProcessCommandBuilder(config)
158:         cmd = builder.build_command()
159: 
160:         assert "--top-k" not in cmd
161: 
162: 
163: class TestMinPParameter:
164:     """3.2.5: Min-p parameter toggling."""
165: 
166:     def test_includes_min_p_when_enabled(self) -> None:
167:         """3.2.5: Includes --min-p when min_p checkbox is checked."""
168:         config = _make_collector(
169:             enable_min_p_checkbox=MockCheckBox(True),
170:             min_p_spinbox=MockSpinBox(0.05),
171:         ).collect_config()
172:         builder = ProcessCommandBuilder(config)
173:         cmd = builder.build_command()
174: 
175:         assert "--min-p" in cmd
176:         min_p_idx = cmd.index("--min-p")
177:         assert cmd[min_p_idx + 1] == "0.05"
178: 
179:     def test_omits_min_p_when_disabled(self) -> None:
180:         """3.2.5: Omits --min-p when min_p checkbox is unchecked."""
181:         config = _make_collector(
182:             enable_min_p_checkbox=MockCheckBox(False),
183:             min_p_spinbox=MockSpinBox(0.05),
184:         ).collect_config()
185:         builder = ProcessCommandBuilder(config)
186:         cmd = builder.build_command()
187: 
188:         assert "--min-p" not in cmd
189: 
190: 
191: class TestTypicalPParameter:
192:     """3.2.6: Typical-p parameter toggling."""
193: 
194:     def test_includes_typical_p_when_enabled(self) -> None:
195:         """3.2.6: Includes --typical-p when typical_p checkbox is checked."""
196:         config = _make_collector(
197:             enable_typical_p_checkbox=MockCheckBox(True),
198:             typical_p_spinbox=MockSpinBox(1.0),
199:         ).collect_config()
200:         builder = ProcessCommandBuilder(config)
201:         cmd = builder.build_command()
202: 
203:         assert "--typical-p" in cmd
204:         typical_p_idx = cmd.index("--typical-p")
205:         assert cmd[typical_p_idx + 1] == "1.0"
206: 
207:     def test_omits_typical_p_when_disabled(self) -> None:
208:         """3.2.6: Omits --typical-p when typical_p checkbox is unchecked."""
209:         config = _make_collector(
210:             enable_typical_p_checkbox=MockCheckBox(False),
211:             typical_p_spinbox=MockSpinBox(1.0),
212:         ).collect_config()
213:         builder = ProcessCommandBuilder(config)
214:         cmd = builder.build_command()
215: 
216:         assert "--typical-p" not in cmd
217: 
218: 
219: class TestRepeatPenaltyParameter:
220:     """3.2.7: Repeat penalty parameter toggling."""
221: 
222:     def test_includes_repeat_penalty_when_enabled(self) -> None:
223:         """3.2.7: Includes --repeat-penalty when repeat_penalty checkbox is checked."""
224:         config = _make_collector(
225:             enable_repeat_penalty_checkbox=MockCheckBox(True),
226:             repeat_penalty_spinbox=MockSpinBox(1.1),
227:         ).collect_config()
228:         builder = ProcessCommandBuilder(config)
229:         cmd = builder.build_command()
230: 
231:         assert "--repeat-penalty" in cmd
232:         rp_idx = cmd.index("--repeat-penalty")
233:         assert cmd[rp_idx + 1] == "1.1"
234: 
235:     def test_omits_repeat_penalty_when_disabled(self) -> None:
236:         """3.2.7: Omits --repeat-penalty when repeat_penalty checkbox is unchecked."""
237:         config = _make_collector(
238:             enable_repeat_penalty_checkbox=MockCheckBox(False),
239:             repeat_penalty_spinbox=MockSpinBox(1.1),
240:         ).collect_config()
241:         builder = ProcessCommandBuilder(config)
242:         cmd = builder.build_command()
243: 
244:         assert "--repeat-penalty" not in cmd
245: 
246: 
247: class TestRepeatLastNParameter:
248:     """3.2.8: Repeat last N parameter toggling."""
249: 
250:     def test_includes_repeat_last_n_when_enabled(self) -> None:
251:         """3.2.8: Includes --repeat-last-n when repeat_last_n checkbox is checked."""
252:         config = _make_collector(
253:             enable_repeat_last_n_checkbox=MockCheckBox(True),
254:             repeat_last_n_spinbox=MockSpinBox(64),
255:         ).collect_config()
256:         builder = ProcessCommandBuilder(config)
257:         cmd = builder.build_command()
258: 
259:         assert "--repeat-last-n" in cmd
260:         rln_idx = cmd.index("--repeat-last-n")
261:         assert cmd[rln_idx + 1] == "64"
262: 
263:     def test_omits_repeat_last_n_when_disabled(self) -> None:
264:         """3.2.8: Omits --repeat-last-n when repeat_last_n checkbox is unchecked."""
265:         config = _make_collector(
266:             enable_repeat_last_n_checkbox=MockCheckBox(False),
267:             repeat_last_n_spinbox=MockSpinBox(64),
268:         ).collect_config()
269:         builder = ProcessCommandBuilder(config)
270:         cmd = builder.build_command()
271: 
272:         assert "--repeat-last-n" not in cmd
273: 
274: 
275: class TestPresencePenaltyParameter:
276:     """3.2.9: Presence penalty parameter toggling."""
277: 
278:     def test_includes_presence_penalty_when_enabled(self) -> None:
279:         """3.2.9: Includes --presence-penalty when presence_penalty checkbox is checked."""
280:         config = _make_collector(
281:             enable_presence_penalty_checkbox=MockCheckBox(True),
282:             presence_penalty_spinbox=MockSpinBox(0.5),
283:         ).collect_config()
284:         builder = ProcessCommandBuilder(config)
285:         cmd = builder.build_command()
286: 
287:         assert "--presence-penalty" in cmd
288:         pp_idx = cmd.index("--presence-penalty")
289:         assert cmd[pp_idx + 1] == "0.5"
290: 
291:     def test_omits_presence_penalty_when_disabled(self) -> None:
292:         """3.2.9: Omits --presence-penalty when presence_penalty checkbox is unchecked."""
293:         config = _make_collector(
294:             enable_presence_penalty_checkbox=MockCheckBox(False),
295:             presence_penalty_spinbox=MockSpinBox(0.5),
296:         ).collect_config()
297:         builder = ProcessCommandBuilder(config)
298:         cmd = builder.build_command()
299: 
300:         assert "--presence-penalty" not in cmd
301: 
302: 
303: class TestFrequencyPenaltyParameter:
304:     """3.2.10: Frequency penalty parameter toggling."""
305: 
306:     def test_includes_frequency_penalty_when_enabled(self) -> None:
307:         """3.2.10: Includes --frequency-penalty when frequency_penalty checkbox is checked."""
308:         config = _make_collector(
309:             enable_frequency_penalty_checkbox=MockCheckBox(True),
310:             frequency_penalty_spinbox=MockSpinBox(0.3),
311:         ).collect_config()
312:         builder = ProcessCommandBuilder(config)
313:         cmd = builder.build_command()
314: 
315:         assert "--frequency-penalty" in cmd
316:         fp_idx = cmd.index("--frequency-penalty")
317:         assert cmd[fp_idx + 1] == "0.3"
318: 
319:     def test_omits_frequency_penalty_when_disabled(self) -> None:
320:         """3.2.10: Omits --frequency-penalty when frequency_penalty checkbox is unchecked."""
321:         config = _make_collector(
322:             enable_frequency_penalty_checkbox=MockCheckBox(False),
323:             frequency_penalty_spinbox=MockSpinBox(0.3),
324:         ).collect_config()
325:         builder = ProcessCommandBuilder(config)
326:         cmd = builder.build_command()
327: 
328:         assert "--frequency-penalty" not in cmd
329: 
330: 
331: class TestMirostatParameters:
332:     """3.2.11: Mirostat parameters toggling (three related params)."""
333: 
334:     def test_includes_all_mirostat_params_when_enabled(self) -> None:
335:         """3.2.11a: Includes --mirostat, --mirostat-lr, --mirostat-ent when all mirostat checkboxes are checked."""
336:         config = _make_collector(
337:             enable_mirostat_checkbox=MockCheckBox(True),
338:             mirostat_spinbox=MockSpinBox(2),
339:             enable_mirostat_lr_checkbox=MockCheckBox(True),
340:             mirostat_lr_spinbox=MockSpinBox(0.05),
341:             enable_mirostat_ent_checkbox=MockCheckBox(True),
342:             mirostat_ent_spinbox=MockSpinBox(5.0),
343:         ).collect_config()
344:         builder = ProcessCommandBuilder(config)
345:         cmd = builder.build_command()
346: 
347:         assert "--mirostat" in cmd
348:         assert "--mirostat-lr" in cmd
349:         assert "--mirostat-ent" in cmd
350: 
351:     def test_omits_mirostat_when_disabled(self) -> None:
352:         """3.2.11b: Omits --mirostat when mirostat checkbox is unchecked."""
353:         config = _make_collector(
354:             enable_mirostat_checkbox=MockCheckBox(False),
355:             mirostat_spinbox=MockSpinBox(2),
356:         ).collect_config()
357:         builder = ProcessCommandBuilder(config)
358:         cmd = builder.build_command()
359: 
360:         assert "--mirostat" not in cmd
361: 
362:     def test_omits_mirostat_lr_when_disabled(self) -> None:
363:         """3.2.11c: Omits --mirostat-lr when mirostat_lr checkbox is unchecked."""
364:         config = _make_collector(
365:             enable_mirostat_lr_checkbox=MockCheckBox(False),
366:             mirostat_lr_spinbox=MockSpinBox(0.05),
367:         ).collect_config()
368:         builder = ProcessCommandBuilder(config)
369:         cmd = builder.build_command()
370: 
371:         assert "--mirostat-lr" not in cmd
372: 
373:     def test_omits_mirostat_ent_when_disabled(self) -> None:
374:         """3.2.11d: Omits --mirostat-ent when mirostat_ent checkbox is unchecked."""
375:         config = _make_collector(
376:             enable_mirostat_ent_checkbox=MockCheckBox(False),
377:             mirostat_ent_spinbox=MockSpinBox(5.0),
378:         ).collect_config()
379:         builder = ProcessCommandBuilder(config)
380:         cmd = builder.build_command()
381: 
382:         assert "--mirostat-ent" not in cmd
383: 
384: 
385: # ==================================================================
386: # 3.5 Server and Model Parameters
387: # ==================================================================
388: 
389: 
390: class TestServerHostPort:
391:     """3.5.1-3.5.3: Server host and port parameter handling."""
392: 
393:     def test_uses_host_from_config(self) -> None:
394:         """3.5.1: Uses host from config or falls back to default _host."""
395:         config = _make_collector(
396:             host_line_edit=MockLineEdit("0.0.0.0"),
397:         ).collect_config()
398:         builder = ProcessCommandBuilder(config)
399:         cmd = builder.build_command()
400: 
401:         assert "--host" in cmd
402:         host_idx = cmd.index("--host")
403:         assert cmd[host_idx + 1] == "0.0.0.0"
404: 
405:     def test_uses_port_from_config(self) -> None:
406:         """3.5.2: Uses port from config or falls back to default _port."""
407:         config = _make_collector(
408:             port_line_edit=MockLineEdit("3000"),
409:         ).collect_config()
410:         builder = ProcessCommandBuilder(config)
411:         cmd = builder.build_command()
412: 
413:         assert "--port" in cmd
414:         port_idx = cmd.index("--port")
415:         assert cmd[port_idx + 1] == "3000"
416: 
417:     def test_handles_invalid_port_falls_back_to_default(self) -> None:
418:         """3.5.3: Handles invalid port text (ValueError) by falling back to default."""
419:         config = _make_collector(
420:             port_line_edit=MockLineEdit("not_a_number"),
421:         ).collect_config()
422:         builder = ProcessCommandBuilder(config)
423:         cmd = builder.build_command()
424: 
425:         assert "--port" in cmd
426:         port_idx = cmd.index("--port")
427:         # Should fall back to default port 8080
428:         assert cmd[port_idx + 1] == "8080"
429: 
430: 
431: class TestMmprojParameters:
432:     """3.5.4-3.5.5: MMProj model parameters."""
433: 
434:     def test_includes_mmproj_when_path_set(self) -> None:
435:         """3.5.4: Includes --mmproj when mmproj_path is set."""
436:         config = _make_collector(
437:             mmproj_path_edit=MockPathEdit(_full_path="/models/mmproj.bin"),
438:         ).collect_config()
439:         builder = ProcessCommandBuilder(config)
440:         cmd = builder.build_command()
441: 
442:         assert "--mmproj" in cmd
443:         mmproj_idx = cmd.index("--mmproj")
444:         assert cmd[mmproj_idx + 1] == "/models/mmproj.bin"
445: 
446:     def test_includes_no_mmproj_offload_when_mmproj_and_checkbox_checked(self) -> None:
447:         """3.5.5: Includes --no-mmproj-offload when mmproj is set AND checkbox is checked."""
448:         config = _make_collector(
449:             mmproj_path_edit=MockPathEdit(_full_path="/models/mmproj.bin"),
450:             no_mmproj_offload_checkbox=MockCheckBox(True),
451:         ).collect_config()
452:         builder = ProcessCommandBuilder(config)
453:         cmd = builder.build_command()
454: 
455:         assert "--mmproj" in cmd
456:         assert "--no-mmproj-offload" in cmd
457: 
458:     def test_omits_no_mmproj_offload_when_checkbox_unchecked(self) -> None:
459:         """3.5.5b: Omits --no-mmproj-offload when mmproj is set but checkbox is unchecked."""
460:         config = _make_collector(
461:             mmproj_path_edit=MockPathEdit(_full_path="/models/mmproj.bin"),
462:             no_mmproj_offload_checkbox=MockCheckBox(False),
463:         ).collect_config()
464:         builder = ProcessCommandBuilder(config)
465:         cmd = builder.build_command()
466: 
467:         assert "--mmproj" in cmd
468:         assert "--no-mmproj-offload" not in cmd
469: 
470: 
471: class TestExtraFlags:
472:     """3.5.6: Extra flags parsing."""
473: 
474:     def test_parses_extra_flags_from_more_options(self) -> None:
475:         """3.5.6: Parses extra flags from more_options line edit via .split()."""
476:         config = _make_collector(
477:             more_options_line_edit=MockLineEdit("--log-id test --verbose"),
478:         ).collect_config()
479:         builder = ProcessCommandBuilder(config)
480:         cmd = builder.build_command()
481: 
482:         assert "--log-id" in cmd
483:         assert "test" in cmd
484:         assert "--verbose" in cmd
485: 
486:     def test_omits_extra_flags_when_empty(self) -> None:
487:         """3.5.6b: Omits extra flags when more_options is empty."""
488:         config = _make_collector(
489:             more_options_line_edit=MockLineEdit(""),
490:         ).collect_config()
491:         builder = ProcessCommandBuilder(config)
492:         cmd = builder.build_command()
493: 
494:         # No extra flags from empty more_options
495:         assert "--log-id" not in cmd
496: 
497: 
498: class TestContextSize:
499:     """3.5.7-3.5.8: Context size parameter."""
500: 
501:     def test_includes_ctx_size_when_greater_than_zero(self) -> None:
502:         """3.5.7: Includes --ctx-size only when context size > 0."""
503:         config = _make_collector(
504:             model_context_size=MockComboBox(
505:                 _current_text="4096",
506:                 _items=[("512", 512), ("2048", 2048), ("4096", 4096), ("8192", 8192)],
507:             ),
508:         ).collect_config()
509:         builder = ProcessCommandBuilder(config)
510:         cmd = builder.build_command()
511: 
512:         assert "--ctx-size" in cmd
513:         ctx_idx = cmd.index("--ctx-size")
514:         assert cmd[ctx_idx + 1] == "4096"
515: 
516:     def test_omits_ctx_size_when_zero(self) -> None:
517:         """3.5.8: Omits --ctx-size when context size is 0 (Auto)."""
518:         config = _make_collector(
519:             model_context_size=MockComboBox(
520:                 _current_text="Auto",
521:                 _items=[("Auto", 0), ("512", 512), ("2048", 2048), ("4096", 4096)],
522:             ),
523:         ).collect_config()
524:         builder = ProcessCommandBuilder(config)
525:         cmd = builder.build_command()
526: 
527:         assert "--ctx-size" not in cmd
528: 
529: 
530: # ==================================================================
531: # 3.6 Process Launch Side Effects
532: # ==================================================================
533: 
534: 
535: def _make_launch_app(**overrides: Any) -> MagicMock:
536:     """Build a mock LlamaLaunchApp ready for _launch_model testing.
537: 
538:     All widgets are configured with default values that represent
539:     a minimal valid configuration (model selected, defaults for everything else).
540: 
541:     Args:
542:         **overrides: Named widget overrides replace defaults.
543: 
544:     Returns:
545:         MagicMock configured as a LlamaLaunchApp instance.
546:     """
547:     app = MagicMock()
548: 
549:     # Required: model path must be set (otherwise _launch_model returns early)
550:     model_path = overrides.get("model_path", "/models/llama.gguf")
551:     app.model_path_edit = MagicMock()
552:     app.model_path_edit.property.return_value = model_path
553: 
554:     # Server widgets
555:     host = overrides.get("host", "127.0.0.1")
556:     port_str = overrides.get("port", "8080")
557:     app.host_line_edit = MagicMock()
558:     app.host_line_edit.text.return_value = host
559:     app.port_line_edit = MagicMock()
560:     app.port_line_edit.text.return_value = port_str
561:     app._host = overrides.get("_host", host)
562:     app._port = overrides.get("_port", int(port_str))
563: 
564:     # API key
565:     app.api_key_line_edit = MagicMock()
566:     app.api_key_line_edit.text.return_value = overrides.get("api_key", "")
567: 
568:     # All spinboxes - default to 0
569:     spinbox_params = [
570:         "temperature",
571:         "top_p",
572:         "top_k",
573:         "min_p",
574:         "typical_p",
575:         "repeat_penalty",
576:         "repeat_last_n",
577:         "presence_penalty",
578:         "frequency_penalty",
579:         "mirostat",
580:         "mirostat_lr",
581:         "mirostat_ent",
582:         "gpu_layers",
583:         "threads",
584:         "threads_batch",
585:         "batch_size",
586:         "ubatch_size",
587:         "n_predict",
588:         "parallel",
589:         "spec_draft_n_max",
590:         "seed",
591:         "rope_freq_base",
592:         "rope_freq_scale",
593:     ]
594:     for param in spinbox_params:
595:         sb = MagicMock()
596:         sb.value.return_value = overrides.get(f"{param}_value", 0)
597:         setattr(app, f"{param}_spinbox", sb)
598: 
599:     # All checkboxes - default to unchecked
600:     checkbox_params = [
601:         "enable_temperature",
602:         "enable_top_p",
603:         "enable_top_k",
604:         "enable_min_p",
605:         "enable_typical_p",
606:         "enable_repeat_penalty",
607:         "enable_repeat_last_n",
608:         "enable_presence_penalty",
609:         "enable_frequency_penalty",
610:         "enable_mirostat",
611:         "enable_mirostat_lr",
612:         "enable_mirostat_ent",
613:         "enable_gpu_layers",
614:         "enable_threads",
615:         "enable_threads_batch",
616:         "enable_batch_size",
617:         "enable_ubatch_size",
618:         "enable_n_predict",
619:         "enable_parallel",
620:         "enable_mmap",
621:         "enable_mlock",
622:         "enable_cont_batching",
623:         "enable_draft_model",
624:         "enable_spec_draft_n_max",
625:         "enable_seed",
626:         "enable_grammar",
627:         "enable_json_schema",
628:         "enable_rope_scaling",
629:         "enable_rope_freq_base",
630:         "enable_rope_freq_scale",
631:         "enable_cache_type_k",
632:         "enable_cache_type_v",
633:     ]
634:     for cb in checkbox_params:
635:         cb_mock = MagicMock()
636:         cb_mock.isChecked.return_value = overrides.get(f"{cb}_checked", False)
637:         setattr(app, cb, cb_mock)
638: 
639:     # Comboboxes
640:     app.flash_attn_combobox = MagicMock()
641:     app.flash_attn_combobox.currentText.return_value = overrides.get("flash_attn", "auto")
642:     app.cache_type_k_combobox = MagicMock()
643:     app.cache_type_k_combobox.currentText.return_value = overrides.get("cache_type_k", "f32")
644:     app.cache_type_v_combobox = MagicMock()
645:     app.cache_type_v_combobox.currentText.return_value = overrides.get("cache_type_v", "f32")
646:     app.rope_scaling_combobox = MagicMock()
647:     app.rope_scaling_combobox.currentText.return_value = overrides.get("rope_scaling", "linear")
648: 
649:     # Path widgets
650:     mmproj_path = overrides.get("mmproj_path", None)
651:     app.mmproj_path_edit = MagicMock()
652:     app.mmproj_path_edit.property.return_value = mmproj_path
653:     app.draft_model_line_edit = MagicMock()
654:     app.draft_model_line_edit.property.return_value = None
655:     app.json_schema_line_edit = MagicMock()
656:     app.json_schema_line_edit.property.return_value = None
657:     app.grammar_line_edit = MagicMock()
658:     app.grammar_line_edit.text.return_value = ""
659: 
660:     # More options
661:     app.more_options_line_edit = MagicMock()
662:     app.more_options_line_edit.text.return_value = ""
663: 
664:     # Context size - default to Auto (no ctx-size)
665:     app.model_context_size = MagicMock()
666:     app.model_context_size.currentIndex.return_value = 0
667:     app.model_context_size.itemData.return_value = None
668: 
669:     # No mmproj offload checkbox
670:     app.no_mmproj_offload_checkbox = MagicMock()
671:     app.no_mmproj_offload_checkbox.isChecked.return_value = False
672: 
673:     # Side-effect widgets (captured by tests)
674:     app.output_display = MagicMock()
675:     app.launch_button = MagicMock()
676:     app.server_web_view = MagicMock()
677:     app._process = MagicMock()
678: 
679:     return app
680: 
681: 
682: class TestLaunchModelSideEffects:
683:     """3.6: Testing side effects of _launch_model method."""
684: 
685:     def test_3_6_1_sets_server_url(self) -> None:
686:         """3.6.1: Sets _server_url after building command.
687: 
688:         After constructing the command, the method should set
689:         ``_server_url`` to ``http://{host}:{port}``.
690:         """
691:         # Arrange
692:         from main import LlamaLaunchApp
693: 
694:         app = _make_launch_app()
695: 
696:         # Act
697:         LlamaLaunchApp._launch_model(app)
698: 
699:         # Assert
700:         assert app._server_url == "http://127.0.0.1:8080"
701: 
702:     def test_3_6_2_clears_output_display_before_launching(self) -> None:
703:         """3.6.2: Clears output_display before launching.
704: 
705:         The method should call ``output_display.clear()`` to wipe
706:         previous output before writing the new launch message.
707:         """
708:         # Arrange
709:         from main import LlamaLaunchApp
710: 
711:         app = _make_launch_app()
712: 
713:         # Act
714:         LlamaLaunchApp._launch_model(app)
715: 
716:         # Assert
717:         app.output_display.clear.assert_called_once()
718: 
719:     def test_3_6_3_appends_launch_command_to_output_display(self) -> None:
720:         """3.6.3: Appends launch command to output_display.
721: 
722:         After clearing, the method should append a line starting with
723:         ``Launching: `` followed by the full command joined with spaces.
724:         """
725:         # Arrange
726:         from main import LlamaLaunchApp
727: 
728:         app = _make_launch_app()
729: 
730:         # Act
731:         LlamaLaunchApp._launch_model(app)
732: 
733:         # Assert
734:         call_args = app.output_display.appendPlainText.call_args
735:         output_text = call_args[0][0]
736:         assert output_text.startswith("Launching: ")
737:         assert "llama-server" in output_text
738:         assert "/models/llama.gguf" in output_text
739: 
740:     def test_3_6_4_calls_process_start_with_program_and_args(self) -> None:
741:         """3.6.4: Calls _process.start() with correct program and args list.
742: 
743:         The two-argument form of ``QProcess.start`` is used:
744:         first argument is the program, second is a list of arguments
745:         (the program itself must NOT be in the list).
746:         """
747:         # Arrange
748:         from main import LlamaLaunchApp
749: 
750:         app = _make_launch_app()
751: 
752:         # Act
753:         LlamaLaunchApp._launch_model(app)
754: 
755:         # Assert
756:         app._process.start.assert_called_once()
757:         call_args = app._process.start.call_args
758:         program = call_args[0][0]
759:         args = call_args[0][1]
760:         assert program == "llama-server"
761:         assert "llama-server" not in args
762:         assert "--model" in args
763:         assert "/models/llama.gguf" in args
764:         assert "--host" in args
765:         assert "127.0.0.1" in args
766:         assert "--port" in args
767:         assert "8080" in args
768: 
769:     def test_3_6_5_updates_launch_button_text_to_stop(self) -> None:
770:         """3.6.5: Updates launch_button text to STOP.
771: 
772:         After starting the process, the button label should change
773:         from its default to ``STOP`` so the user can stop the server.
774:         """
775:         # Arrange
776:         from main import LlamaLaunchApp
777: 
778:         app = _make_launch_app()
779: 
780:         # Act
781:         LlamaLaunchApp._launch_model(app)
782: 
783:         # Assert
784:         app.launch_button.setText.assert_called_once_with("STOP")
785: 
786:     def test_3_6_6_updates_web_view_url_after_launch(self) -> None:
787:         """3.6.6: Updates web view URL after launch.
788: 
789:         The server web view should be pointed at the new server URL
790:         so that users can immediately interact with the running server.
791:         """
792:         # Arrange
793:         from main import LlamaLaunchApp
794: 
795:         app = _make_launch_app()
796: 
797:         # Act
798:         LlamaLaunchApp._launch_model(app)
799: 
800:         # Assert
801:         app.server_web_view.setUrl.assert_called_once()
802:         called_url = app.server_web_view.setUrl.call_args[0][0]
803:         assert called_url == "http://127.0.0.1:8080"

(End of file - total 803 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Volumes/teaching/Code/LLamaLauncher/tests/test_config.py"
}
```

**Output:**
```
<path>/Volumes/teaching/Code/LLamaLauncher/tests/test_config.py</path>
<type>file</type>
<content>
1: """Tests for configuration collection logic.
2: 
3: Covers the pure data transformation logic for collecting widget values
4: into a configuration dictionary and loading that configuration back.
5: Uses simple dataclass widgets to avoid Qt dependencies in the test layer.
6: """
7: 
8: import json
9: from dataclasses import dataclass, field
10: from pathlib import Path
11: from typing import Any
12: 
13: from .config_collector import ConfigCollector
14: 
15: # ------------------------------------------------------------------
16: # Simple widget data classes (no Qt dependencies)
17: # ------------------------------------------------------------------
18: 
19: 
20: @dataclass(slots=True)
21: class MockLineEdit:
22:     """Minimal QLineEdit replacement for testing."""
23: 
24:     _text: str = ""
25: 
26:     def text(self) -> str:
27:         return self._text
28: 
29: 
30: @dataclass(slots=True)
31: class MockPathEdit:
32:     """Minimal path line edit with fullPath property."""
33: 
34:     _text: str = ""
35:     _full_path: str = ""
36: 
37:     def text(self) -> str:
38:         return self._text
39: 
40:     def property(self, name: str) -> str | None:
41:         if name == "fullPath":
42:             return self._full_path if self._full_path else None
43:         return None
44: 
45:     def setProperty(self, name: str, value: str) -> None:
46:         if name == "fullPath":
47:             self._full_path = value
48: 
49: 
50: @dataclass(slots=True)
51: class MockCheckBox:
52:     """Minimal QCheckBox replacement for testing."""
53: 
54:     _checked: bool = False
55: 
56:     def isChecked(self) -> bool:
57:         return self._checked
58: 
59: 
60: @dataclass(slots=True)
61: class MockSpinBox:
62:     """Minimal QSpinBox/QDoubleSpinBox replacement for testing."""
63: 
64:     _value: float = 0.0
65: 
66:     def value(self) -> float:
67:         return self._value
68: 
69: 
70: @dataclass(slots=True)
71: class MockComboBox:
72:     """Minimal QComboBox replacement for testing."""
73: 
74:     _current_text: str = ""
75:     _items: list[tuple[str, Any]] = field(default_factory=list)
76:     _current_index: int = 0
77: 
78:     def __post_init__(self) -> None:
79:         # Auto-resolve current index from text if items exist and index not set
80:         if self._items and self._current_text:
81:             for i, (text, _) in enumerate(self._items):
82:                 if text == self._current_text:
83:                     self._current_index = i
84:                     break
85: 
86:     def currentText(self) -> str:
87:         return self._current_text
88: 
89:     def currentIndex(self) -> int:
90:         return self._current_index
91: 
92:     def itemData(self, index: int, role: Any) -> Any | None:
93:         if 0 <= index < len(self._items):
94:             return self._items[index][1]
95:         return None
96: 
97: 
98: # ------------------------------------------------------------------
99: # Fixtures
100: # ------------------------------------------------------------------
101: 
102: 
103: def _make_collector(**overrides: Any) -> ConfigCollector:
104:     """Build a ConfigCollector with default mock widgets, then override specific ones.
105: 
106:     Args:
107:         **overrides: Named widget overrides to replace defaults.
108: 
109:     Returns:
110:         ConfigCollector instance ready for testing.
111:     """
112:     defaults = {
113:         "version_edit": MockLineEdit("1.0"),
114:         "model_path_edit": MockPathEdit(_full_path="/models/llama.gguf"),
115:         "mmproj_path_edit": MockPathEdit(_full_path="/models/mmproj.bin"),
116:         "draft_model_line_edit": MockPathEdit(_full_path="/models/draft.gguf"),
117:         "json_schema_line_edit": MockPathEdit(_full_path="/schemas/schema.json"),
118:         "host_line_edit": MockLineEdit("127.0.0.1"),
119:         "port_line_edit": MockLineEdit("8080"),
120:         "api_key_line_edit": MockLineEdit("secret-key"),
121:         "enable_temperature_checkbox": MockCheckBox(True),
122:         "temperature_spinbox": MockSpinBox(0.7),
123:         "enable_top_p_checkbox": MockCheckBox(True),
124:         "top_p_spinbox": MockSpinBox(0.9),
125:         "enable_top_k_checkbox": MockCheckBox(False),
126:         "top_k_spinbox": MockSpinBox(40),
127:         "enable_min_p_checkbox": MockCheckBox(False),
128:         "min_p_spinbox": MockSpinBox(0.05),
129:         "enable_typical_p_checkbox": MockCheckBox(False),
130:         "typical_p_spinbox": MockSpinBox(1.0),
131:         "enable_repeat_penalty_checkbox": MockCheckBox(False),
132:         "repeat_penalty_spinbox": MockSpinBox(1.1),
133:         "enable_repeat_last_n_checkbox": MockCheckBox(False),
134:         "repeat_last_n_spinbox": MockSpinBox(64),
135:         "enable_presence_penalty_checkbox": MockCheckBox(False),
136:         "presence_penalty_spinbox": MockSpinBox(0.0),
137:         "enable_frequency_penalty_checkbox": MockCheckBox(False),
138:         "frequency_penalty_spinbox": MockSpinBox(0.0),
139:         "enable_mirostat_checkbox": MockCheckBox(False),
140:         "mirostat_spinbox": MockSpinBox(0),
141:         "enable_mirostat_lr_checkbox": MockCheckBox(False),
142:         "mirostat_lr_spinbox": MockSpinBox(0.001),
143:         "enable_mirostat_ent_checkbox": MockCheckBox(False),
144:         "mirostat_ent_spinbox": MockSpinBox(5.0),
145:         "enable_gpu_layers_checkbox": MockCheckBox(True),
146:         "gpu_layers_spinbox": MockSpinBox(33),
147:         "enable_threads_checkbox": MockCheckBox(True),
148:         "threads_spinbox": MockSpinBox(8),
149:         "enable_threads_batch_checkbox": MockCheckBox(False),
150:         "threads_batch_spinbox": MockSpinBox(512),
151:         "enable_batch_size_checkbox": MockCheckBox(False),
152:         "batch_size_spinbox": MockSpinBox(512),
153:         "enable_ubatch_size_checkbox": MockCheckBox(False),
154:         "ubatch_size_spinbox": MockSpinBox(512),
155:         "enable_n_predict_checkbox": MockCheckBox(False),
156:         "n_predict_spinbox": MockSpinBox(4096),
157:         "enable_parallel_checkbox": MockCheckBox(False),
158:         "parallel_spinbox": MockSpinBox(4),
159:         "flash_attn_combobox": MockComboBox("false"),
160:         "enable_cache_type_k_checkbox": MockCheckBox(False),
161:         "cache_type_k_combobox": MockComboBox("f32"),
162:         "enable_cache_type_v_checkbox": MockCheckBox(False),
163:         "cache_type_v_combobox": MockComboBox("f32"),
164:         "enable_mmap_checkbox": MockCheckBox(True),
165:         "enable_mlock_checkbox": MockCheckBox(False),
166:         "enable_cont_batching_checkbox": MockCheckBox(True),
167:         "enable_draft_model_checkbox": MockCheckBox(True),
168:         "enable_spec_draft_n_max_checkbox": MockCheckBox(False),
169:         "spec_draft_n_max_spinbox": MockSpinBox(4),
170:         "enable_seed_checkbox": MockCheckBox(False),
171:         "seed_spinbox": MockSpinBox(0),
172:         "enable_grammar_checkbox": MockCheckBox(False),
173:         "grammar_line_edit": MockPathEdit(_full_path="/grammars/json.gbnf"),
174:         "enable_json_schema_checkbox": MockCheckBox(True),
175:         "enable_rope_scaling_checkbox": MockCheckBox(False),
176:         "rope_scaling_combobox": MockComboBox("none"),
177:         "enable_rope_freq_base_checkbox": MockCheckBox(False),
178:         "rope_freq_base_spinbox": MockSpinBox(0.0),
179:         "enable_rope_freq_scale_checkbox": MockCheckBox(False),
180:         "rope_freq_scale_spinbox": MockSpinBox(1.0),
181:         "model_context_size": MockComboBox(
182:             _current_text="4096",
183:             _items=[("512", 512), ("2048", 2048), ("4096", 4096), ("8192", 8192)],
184:         ),
185:         "more_options_line_edit": MockLineEdit(""),
186:         "no_mmproj_offload_checkbox": MockCheckBox(False),
187:     }
188:     defaults.update(overrides)
189:     return ConfigCollector(**defaults)
190: 
191: 
192: # ==================================================================
193: # 2.1 Version string
194: # ==================================================================
195: 
196: 
197: class TestVersionString:
198:     """2.1.1: Collects version string as "1.0"."""
199: 
200:     def test_collects_version_string_as_1_0(self) -> None:
201:         """2.1.1: Version is always collected as the literal "1.0"."""
202:         collector = _make_collector(version_edit=MockLineEdit("1.0"))
203:         config = collector.collect_config()
204: 
205:         assert config["version"] == "1.0"
206: 
207: 
208: # ==================================================================
209: # 2.2 Files/Paths
210: # ==================================================================
211: 
212: 
213: class TestFilePaths:
214:     """2.1.2-2.1.4: Collecting file paths from widget properties."""
215: 
216:     def test_collects_model_path_from_fullPath_property(self) -> None:
217:         """2.1.2: model_path comes from the fullPath property of the path edit."""
218:         collector = _make_collector(
219:             model_path_edit=MockPathEdit(_full_path="/models/llama.gguf")
220:         )
221:         config = collector.collect_config()
222: 
223:         assert config["files"]["model_path"] == "/models/llama.gguf"
224: 
225:     def test_collects_mmproj_and_draft_and_json_schema_paths(self) -> None:
226:         """2.1.3: mmproj_path, draft_model_path, json_schema_path are collected."""
227:         collector = _make_collector(
228:             mmproj_path_edit=MockPathEdit(_full_path="/models/mmproj.bin"),
229:             draft_model_line_edit=MockPathEdit(_full_path="/models/draft.gguf"),
230:             json_schema_line_edit=MockPathEdit(_full_path="/schemas/schema.json"),
231:         )
232:         config = collector.collect_config()
233: 
234:         assert config["files"]["mmproj_path"] == "/models/mmproj.bin"
235:         assert config["files"]["draft_model_path"] == "/models/draft.gguf"
236:         assert config["files"]["json_schema_path"] == "/schemas/schema.json"
237: 
238:     def test_handles_empty_paths_as_empty_strings_not_none(self) -> None:
239:         """2.1.4: Empty paths become empty strings, not None."""
240:         collector = _make_collector(
241:             model_path_edit=MockPathEdit(_full_path=""),
242:             mmproj_path_edit=MockPathEdit(),
243:             draft_model_line_edit=MockPathEdit(),
244:             json_schema_line_edit=MockPathEdit(),
245:         )
246:         config = collector.collect_config()
247: 
248:         for key in (
249:             "model_path",
250:             "mmproj_path",
251:             "draft_model_path",
252:             "json_schema_path",
253:         ):
254:             assert config["files"][key] == ""
255:             assert config["files"][key] is not None
256: 
257: 
258: # ==================================================================
259: # 2.3 Server settings
260: # ==================================================================
261: 
262: 
263: class TestServerSettings:
264:     """2.1.5-2.1.6: Collecting server host, port, and API key."""
265: 
266:     def test_collects_server_host_port_api_key(self) -> None:
267:         """2.1.5: Server host, port (as int), and api_key are collected correctly."""
268:         collector = _make_collector(
269:             host_line_edit=MockLineEdit("0.0.0.0"),
270:             port_line_edit=MockLineEdit("8080"),
271:             api_key_line_edit=MockLineEdit("my-api-key"),
272:         )
273:         config = collector.collect_config()
274: 
275:         assert config["server"]["host"] == "0.0.0.0"
276:         assert config["server"]["port"] == 8080
277:         assert isinstance(config["server"]["port"], int)
278:         assert config["server"]["api_key"] == "my-api-key"
279: 
280:     def test_handles_invalid_port_text_as_default_8080(self) -> None:
281:         """2.1.6: Non-digit port text falls back to default 8080."""
282:         collector = _make_collector(port_line_edit=MockLineEdit("not-a-port"))
283:         config = collector.collect_config()
284: 
285:         assert config["server"]["port"] == 8080
286: 
287:     def test_handles_empty_port_text_as_default_8080(self) -> None:
288:         """2.1.6: Empty port text falls back to default 8080."""
289:         collector = _make_collector(port_line_edit=MockLineEdit(""))
290:         config = collector.collect_config()
291: 
292:         assert config["server"]["port"] == 8080
293: 
294: 
295: # ==================================================================
296: # 2.4 Sampling parameters
297: # ==================================================================
298: 
299: 
300: class TestSamplingParameters:
301:     """2.1.7-2.1.8: Collecting sampling parameters with enabled+value format."""
302: 
303:     def test_sampling_param_has_enabled_and_value_format(self) -> None:
304:         """2.1.7: Each sampling param is a dict with 'enabled' (bool) and 'value' (float)."""
305:         collector = _make_collector(
306:             enable_temperature_checkbox=MockCheckBox(True),
307:             temperature_spinbox=MockSpinBox(0.85),
308:         )
309:         config = collector.collect_config()
310: 
311:         temp = config["sampling"]["temperature"]
312:         assert isinstance(temp, dict)
313:         assert temp["enabled"] is True
314:         assert temp["value"] == 0.85
315: 
316:     def test_collects_all_sampling_params(self) -> None:
317:         """2.1.8: All 11 sampling parameters are present in the config."""
318:         collector = _make_collector()
319:         config = collector.collect_config()
320: 
321:         expected_keys = {
322:             "temperature",
323:             "top_p",
324:             "top_k",
325:             "min_p",
326:             "typical_p",
327:             "repeat_penalty",
328:             "repeat_last_n",
329:             "presence_penalty",
330:             "frequency_penalty",
331:             "mirostat",
332:             "mirostat_lr",
333:             "mirostat_ent",
334:         }
335:         assert set(config["sampling"].keys()) == expected_keys
336: 
337: 
338: # ==================================================================
339: # 2.5 Performance parameters
340: # ==================================================================
341: 
342: 
343: class TestPerformanceParameters:
344:     """2.1.9-2.1.11: Collecting performance parameters."""
345: 
346:     def test_performance_params_have_enabled_value_format(self) -> None:
347:         """2.1.9: Performance params use enabled+value dict format."""
348:         collector = _make_collector(
349:             enable_gpu_layers_checkbox=MockCheckBox(True),
350:             gpu_layers_spinbox=MockSpinBox(33),
351:         )
352:         config = collector.collect_config()
353: 
354:         gpu = config["performance"]["gpu_layers"]
355:         assert isinstance(gpu, dict)
356:         assert gpu["enabled"] is True
357:         assert gpu["value"] == 33
358: 
359:     def test_collects_flash_attn_combobox_text(self) -> None:
360:         """2.1.10: flash_attn collects the combobox current text."""
361:         collector = _make_collector(
362:             flash_attn_combobox=MockComboBox("true"),
363:         )
364:         config = collector.collect_config()
365: 
366:         assert config["performance"]["flash_attn"] == "true"
367: 
368:     def test_collects_mmap_mlock_cont_batching_booleans(self) -> None:
369:         """2.1.11: mmap, mlock, cont_batching are boolean values from checkboxes."""
370:         collector = _make_collector(
371:             enable_mmap_checkbox=MockCheckBox(True),
372:             enable_mlock_checkbox=MockCheckBox(False),
373:             enable_cont_batching_checkbox=MockCheckBox(True),
374:         )
375:         config = collector.collect_config()
376: 
377:         assert config["performance"]["mmap"] is True
378:         assert config["performance"]["mlock"] is False
379:         assert config["performance"]["cont_batching"] is True
380: 
381: 
382: # ==================================================================
383: # 2.6 Advanced parameters
384: # ==================================================================
385: 
386: 
387: class TestAdvancedParameters:
388:     """2.1.12-2.1.13: Collecting advanced generation parameters."""
389: 
390:     def test_collects_advanced_params(self) -> None:
391:         """2.1.12: draft_model, spec_draft_n_max, seed, grammar, json_schema collected."""
392:         collector = _make_collector(
393:             enable_draft_model_checkbox=MockCheckBox(True),
394:             draft_model_line_edit=MockPathEdit(_full_path="/models/draft.gguf"),
395:             enable_spec_draft_n_max_checkbox=MockCheckBox(True),
396:             spec_draft_n_max_spinbox=MockSpinBox(8),
397:             enable_seed_checkbox=MockCheckBox(True),
398:             seed_spinbox=MockSpinBox(42),
399:             enable_grammar_checkbox=MockCheckBox(True),
400:             grammar_line_edit=MockPathEdit(_full_path="/grammars/json.gbnf"),
401:             enable_json_schema_checkbox=MockCheckBox(False),
402:         )
403:         config = collector.collect_config()
404: 
405:         assert config["advanced"]["draft_model"]["enabled"] is True
406:         assert config["advanced"]["draft_model"]["path"] == "/models/draft.gguf"
407:         assert config["advanced"]["spec_draft_n_max"]["enabled"] is True
408:         assert config["advanced"]["spec_draft_n_max"]["value"] == 8
409:         assert config["advanced"]["seed"]["enabled"] is True
410:         assert config["advanced"]["seed"]["value"] == 42
411:         assert config["advanced"]["grammar"]["enabled"] is True
412:         assert config["advanced"]["grammar"]["path"] == "/grammars/json.gbnf"
413:         assert config["advanced"]["json_schema"]["enabled"] is False
414: 
415:     def test_collects_rope_scaling_combobox_text(self) -> None:
416:         """2.1.13: rope_scaling collects the combobox current text."""
417:         collector = _make_collector(
418:             enable_rope_scaling_checkbox=MockCheckBox(True),
419:             rope_scaling_combobox=MockComboBox("linear"),
420:         )
421:         config = collector.collect_config()
422: 
423:         assert config["advanced"]["rope_scaling"]["enabled"] is True
424:         assert config["advanced"]["rope_scaling"]["value"] == "linear"
425: 
426: 
427: # ==================================================================
428: # 2.7 Other settings
429: # ==================================================================
430: 
431: 
432: class TestOtherSettings:
433:     """2.1.14-2.1.15: context_size, more_options, no_mmproj_offload."""
434: 
435:     def test_collects_context_size_from_user_role(self) -> None:
436:         """2.1.14: context_size is read from the combobox UserRole data."""
437:         ctx_size_combo = MockComboBox(
438:             _current_text="8192",
439:             _items=[("512", 512), ("2048", 2048), ("4096", 4096), ("8192", 8192)],
440:         )
441:         collector = _make_collector(model_context_size=ctx_size_combo)
442:         config = collector.collect_config()
443: 
444:         assert config["context_size"] == 8192
445: 
446:     def test_collects_more_options_and_no_mmproj_offload(self) -> None:
447:         """2.1.15: more_options text and no_mmproj_offload boolean collected."""
448:         collector = _make_collector(
449:             more_options_line_edit=MockLineEdit("--log-disable"),
450:             no_mmproj_offload_checkbox=MockCheckBox(True),
451:         )
452:         config = collector.collect_config()
453: 
454:         assert config["more_options"] == "--log-disable"
455:         assert config["no_mmproj_offload"] is True
456: 
457: 
458: # ==================================================================
459: # 2.8 End-to-end: complete config collection
460: # ==================================================================
461: 
462: 
463: class TestEndToEnd:
464:     """Integration: verify a full config round-trip."""
465: 
466:     def test_collect_config_returns_all_expected_keys(self) -> None:
467:         """Full collect_config returns version, files, server, sampling,
468:         performance, advanced, context_size, more_options, no_mmproj_offload.
469:         """
470:         collector = _make_collector()
471:         config = collector.collect_config()
472: 
473:         expected_keys = {
474:             "version",
475:             "files",
476:             "server",
477:             "sampling",
478:             "performance",
479:             "advanced",
480:             "context_size",
481:             "more_options",
482:             "no_mmproj_offload",
483:         }
484:         assert set(config.keys()) == expected_keys
485: 
486:     def test_config_round_trip_save_and_load(self, tmp_path: Path) -> None:
487:         """Config can be serialized to JSON and deserialized back."""
488:         collector = _make_collector(
489:             model_path_edit=MockPathEdit(_full_path="/models/llama.gguf"),
490:             host_line_edit=MockLineEdit("0.0.0.0"),
491:             port_line_edit=MockLineEdit("9999"),
492:             enable_temperature_checkbox=MockCheckBox(True),
493:             temperature_spinbox=MockSpinBox(0.8),
494:             model_context_size=MockComboBox(
495:                 _current_text="4096",
496:                 _items=[("512", 512), ("2048", 2048), ("4096", 4096)],
497:             ),
498:         )
499:         config = collector.collect_config()
500: 
501:         # Save to JSON
502:         json_path = tmp_path / "config.json"
503:         with open(json_path, "w") as f:
504:             json.dump(config, f, indent=2)
505: 
506:         # Load back
507:         with open(json_path, "r") as f:
508:             loaded = json.load(f)
509: 
510:         assert loaded["version"] == "1.0"
511:         assert loaded["files"]["model_path"] == "/models/llama.gguf"
512:         assert loaded["server"]["port"] == 9999
513:         assert loaded["sampling"]["temperature"]["enabled"] is True
514:         assert loaded["sampling"]["temperature"]["value"] == 0.8
515:         assert loaded["context_size"] == 4096

(End of file - total 515 lines)
</content>
```

---

## Assistant (Python-Code-Quality · Claude Sonnet 4.5 · 8.5s)

Now let me check more test files to get a complete picture:

**Tool: read**

**Input:**
```json
{
  "filePath": "/Volumes/teaching/Code/LLamaLauncher/tests/test_edge_cases.py"
}
```

**Output:**
```
<path>/Volumes/teaching/Code/LLamaLauncher/tests/test_edge_cases.py</path>
<type>file</type>
<content>
1: """Phase 7: Edge Cases and Error Handling tests.
2: 
3: Covers error paths, edge cases, and robustness for LlamaLaunchApp:
4: 
5: - _launch_model handles missing model file gracefully
6: - API key defaults when line edit is empty
7: - _apply_param uses spinbox default value
8: - _apply_combo_param does nothing on no text match
9: - _collect_config handles missing optional sections
10: - _on_stdout/_on_stderr handle empty data
11: - _check_and_refresh regex matches various URL formats
12: - __init__ initializes _process with correct signal connections
13: 
14: TDD: tests written before implementation (RED phase).
15: """
16: 
17: import sys
18: from pathlib import Path
19: from unittest.mock import patch
20: 
21: import pytest
22: from PySide6.QtCore import QByteArray, QProcess
23: from PySide6.QtWidgets import (
24:     QApplication,
25:     QCheckBox,
26:     QComboBox,
27:     QDoubleSpinBox,
28:     QSpinBox,
29: )
30: 
31: # Ensure worktree
32: sys.path.insert(0, str(Path(__file__).parent.parent))
33: 
34: 
35: # ---------------------------------------------------------------------------
36: # Fixtures
37: # ---------------------------------------------------------------------------
38: 
39: 
40: @pytest.fixture(scope="module")
41: def app():
42:     """Provide QApplication singleton for test module."""
43:     application = QApplication.instance()
44:     if application is None:
45:         application = QApplication(sys.argv)
46:     yield application
47: 
48: 
49: @pytest.fixture
50: def launch_app(app):
51:     """Provide a LlamaLaunchApp instance for testing.
52: 
53:     Since full UI initialization is expensive, we create the app and
54:     patch widgets that tests don't interact with.
55:     """
56:     from main import LlamaLaunchApp
57: 
58:     instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
59:     yield instance
60:     instance.close()
61: 
62: 
63: @pytest.fixture
64: def minimal_app(app):
65:     """Minimal LlamaLaunchApp-like class for testing helper methods.
66: 
67:     Since _apply_param and _apply_combo_param are instance methods on
68:     LlamaLaunchApp, we create a minimal subclass that only initializes
69:     the widgets we care about.
70:     """
71: 
72:     class TestApp(QApplication):  # type: ignore[misc]
73:         """Minimal app for testing helper method behavior."""
74: 
75:         pass
76: 
77:     return app
78: 
79: 
80: # ---------------------------------------------------------------------------
81: # 7.1: _launch_model handles missing model file gracefully
82: # ---------------------------------------------------------------------------
83: 
84: 
85: class TestLaunchModelMissingFile:
86:     """7.1: _launch_model handles missing model file (command still built)."""
87: 
88:     def test_7_1_appends_error_when_no_model_selected(self, launch_app):
89:         """7.1: _launch_model appends error message when no model is selected."""
90:         # Clear any existing output
91:         launch_app.output_display.clear()
92:         # Ensure model path is empty
93:         launch_app.model_path_edit.setProperty("fullPath", "")
94:         launch_app.model_path_edit.setText("")
95: 
96:         launch_app._launch_model()
97: 
98:         # Should show error message, not crash
99:         output = launch_app.output_display.toPlainText()
100:         assert "Error" in output or "no model" in output.lower()
101: 
102: 
103: # ---------------------------------------------------------------------------
104: # 7.2: API key defaults to "12345" when line edit is empty
105: # ---------------------------------------------------------------------------
106: 
107: 
108: class TestApiKeyDefault:
109:     """7.2: API key defaults to '12345' when line edit is empty."""
110: 
111:     def test_7_2_api_key_defaults_to_12345_when_empty(self, launch_app):
112:         """7.2: _collect_config returns '12345' when api_key_line_edit is empty."""
113:         # Ensure the line edit is empty
114:         launch_app.api_key_line_edit.setText("")
115: 
116:         config = launch_app._collect_config()
117: 
118:         assert config["server"]["api_key"] == "12345"
119: 
120:     def test_7_2_api_key_uses_line_edit_value_when_not_empty(self, launch_app):
121:         """7.2: _collect_config uses line edit value when not empty."""
122:         launch_app.api_key_line_edit.setText("my-secret-key")
123: 
124:         config = launch_app._collect_config()
125: 
126:         assert config["server"]["api_key"] == "my-secret-key"
127: 
128: 
129: # ---------------------------------------------------------------------------
130: # 7.3: _apply_param uses spinbox default when config lacks "value" key
131: # ---------------------------------------------------------------------------
132: 
133: 
134: class TestApplyParamEdgeCases:
135:     """7.3: _apply_param edge cases with main.py implementation."""
136: 
137:     def test_7_3_uses_spinbox_default_when_value_key_missing(self, launch_app):
138:         """7.3: _apply_param falls back to spinbox.value() when 'value' key absent."""
139:         checkbox = QCheckBox()
140:         spinbox = QSpinBox()
141:         spinbox.setValue(42)  # Initial value as "default"
142: 
143:         # Dict with "enabled" but no "value" key
144:         params = {"temperature": {"enabled": True}}
145: 
146:         launch_app._apply_param(params, "temperature", checkbox, spinbox)
147: 
148:         assert checkbox.isChecked() is True
149:         assert spinbox.value() == 42  # Kept the initial value
150: 
151:     def test_7_3_applies_value_when_present(self, launch_app):
152:         """7.3: _apply_param applies 'value' when present in dict."""
153:         checkbox = QCheckBox()
154:         spinbox = QDoubleSpinBox()
155:         spinbox.setValue(0)
156: 
157:         params = {"temperature": {"enabled": True, "value": 0.7}}
158: 
159:         launch_app._apply_param(params, "temperature", checkbox, spinbox)
160: 
161:         assert checkbox.isChecked() is True
162:         assert spinbox.value() == 0.7
163: 
164:     def test_7_3_defaults_enabled_to_false(self, launch_app):
165:         """7.3: _apply_param defaults enabled to False when key missing."""
166:         checkbox = QCheckBox()
167:         checkbox.setChecked(True)  # Start checked
168:         spinbox = QDoubleSpinBox()
169: 
170:         params = {"temperature": {"value": 0.5}}
171: 
172:         launch_app._apply_param(params, "temperature", checkbox, spinbox)
173: 
174:         assert checkbox.isChecked() is False
175:         assert spinbox.value() == 0.5
176: 
177: 
178: # ---------------------------------------------------------------------------
179: # 7.4: _apply_combo_param does nothing when combobox doesn't find text match
180: # ---------------------------------------------------------------------------
181: 
182: 
183: class TestApplyComboParamEdgeCases:
184:     """7.4: _apply_combo_param edge cases with main.py implementation."""
185: 
186:     def test_7_4_no_change_when_text_not_in_combobox(self, launch_app):
187:         """7.4: _apply_combo_param leaves combobox unchanged when text not found."""
188:         checkbox = QCheckBox()
189:         combobox = QComboBox()
190:         combobox.addItems(["auto", "fp16", "bf16"])
191:         combobox.setCurrentText("auto")
192:         initial_index = combobox.currentIndex()
193: 
194:         params = {"cache_type_k": {"enabled": True, "value": "nonexistent"}}
195: 
196:         launch_app._apply_combo_param(params, "cache_type_k", checkbox, combobox)
197: 
198:         # Checkbox should be checked but combobox index unchanged
199:         assert checkbox.isChecked() is True
200:         assert combobox.currentIndex() == initial_index
201: 
202:     def test_7_4_applies_when_text_found(self, launch_app):
203:         """7.4: _apply_combo_param sets combobox when text matches."""
204:         checkbox = QCheckBox()
205:         combobox = QComboBox()
206:         combobox.addItems(["auto", "fp16", "bf16"])
207: 
208:         params = {"cache_type_k": {"enabled": True, "value": "bf16"}}
209: 
210:         launch_app._apply_combo_param(params, "cache_type_k", checkbox, combobox)
211: 
212:         assert checkbox.isChecked() is True
213:         assert combobox.currentText() == "bf16"
214: 
215: 
216: # ---------------------------------------------------------------------------
217: # 7.5: _collect_config handles missing optional sections without error
218: # ---------------------------------------------------------------------------
219: 
220: 
221: class TestCollectConfigMissingSections:
222:     """7.5: _apply_config handles incomplete/missing config sections."""
223: 
224:     def test_7_5_applies_minimal_config(self, launch_app):
225:         """7.5: _apply_config handles file with only required sections."""
226:         minimal_config = {
227:             "version": "1.0",
228:             "server": {"host": "127.0.0.1", "port": 8080},
229:         }
230: 
231:         # Should not raise, should use defaults for missing sections
232:         launch_app._apply_config(minimal_config)
233: 
234:         # Server values should be applied
235:         assert launch_app.host_line_edit.text() == "127.0.0.1"
236:         assert launch_app.port_line_edit.text() == "8080"
237: 
238:     def test_7_5_applies_empty_config(self, launch_app):
239:         """7.5: _apply_config handles empty JSON object without error."""
240: 
241:         # Should not raise
242:         launch_app._apply_config({})
243: 
244: 
245: # ---------------------------------------------------------------------------
246: # 7.6: _on_stdout handles empty data (no append)
247: # ---------------------------------------------------------------------------
248: 
249: 
250: class TestOnStdoutEmptyData:
251:     """7.6: _on_stdout handles empty data gracefully."""
252: 
253:     def test_7_6_does_not_append_when_stdout_empty(self, launch_app):
254:         """7.6: _on_stdout does nothing when process has no stdout data."""
255:         launch_app.output_display.clear()
256: 
257:         # Patch readAllStandardOutput to return a QByteArray that decodes to empty string
258:         with patch.object(
259:             launch_app._process,
260:             "readAllStandardOutput",
261:             return_value=QByteArray(b""),
262:         ):
263:             launch_app._on_stdout()
264: 
265:         output = launch_app.output_display.toPlainText()
266:         assert output == ""
267: 
268: 
269: # ---------------------------------------------------------------------------
270: # 7.7: _on_stderr handles empty data (no append)
271: # ---------------------------------------------------------------------------
272: 
273: 
274: class TestOnStderrEmptyData:
275:     """7.7: _on_stderr handles empty data gracefully."""
276: 
277:     def test_7_7_does_not_append_when_stderr_empty(self, launch_app):
278:         """7.7: _on_stderr does nothing when process has no stderr data."""
279:         launch_app.output_display.clear()
280: 
281:         # Patch readAllStandardError to return a QByteArray that decodes to empty string
282:         with patch.object(
283:             launch_app._process,
284:             "readAllStandardError",
285:             return_value=QByteArray(b""),
286:         ):
287:             launch_app._on_stderr()
288: 
289:         output = launch_app.output_display.toPlainText()
290:         assert output == ""
291: 
292: 
293: # ---------------------------------------------------------------------------
294: # 7.8: _check_and_refresh regex matches various URL formats
295: # ---------------------------------------------------------------------------
296: 
297: 
298: class TestCheckAndRefreshRegex:
299:     """7.8: _check_and_refresh regex handles various URL formats."""
300: 
301:     def test_7_8_matches_standard_url(self, launch_app):
302:         """7.8: Regex matches http://host:port format."""
303:         launch_app.output_display.clear()
304:         launch_app._auto_refresh_done = False
305:         launch_app.output_display.appendPlainText(
306:             "Loading models...\nhttp://127.0.0.1:8080"
307:         )
308: 
309:         launch_app._check_and_refresh()
310: 
311:         assert launch_app._auto_refresh_done is True
312: 
313:     def test_7_8_matches_domain_url(self, launch_app):
314:         """7.8: Regex matches http://domain.com:port format."""
315:         launch_app.output_display.clear()
316:         launch_app._auto_refresh_done = False
317:         launch_app.output_display.appendPlainText("Server at http://localhost:3000")
318: 
319:         launch_app._check_and_refresh()
320: 
321:         assert launch_app._auto_refresh_done is True
322: 
323:     def test_7_8_no_match_for_non_url_text(self, launch_app):
324:         """7.8: Regex does not match text without URL pattern."""
325:         launch_app.output_display.clear()
326:         launch_app._auto_refresh_done = False
327:         launch_app.output_display.appendPlainText("No server URL here")
328: 
329:         launch_app._check_and_refresh()
330: 
331:         assert launch_app._auto_refresh_done is False
332: 
333:     def test_7_8_no_refresh_when_already_done(self, launch_app):
334:         """7.8: _check_and_refresh returns early when already refreshed."""
335:         launch_app._auto_refresh_done = True
336:         # Should return immediately without scanning
337:         launch_app._check_and_refresh()
338:         assert launch_app._auto_refresh_done is True
339: 
340: 
341: # ---------------------------------------------------------------------------
342: # 7.9: __init__ initializes _process with correct signal connections
343: # ---------------------------------------------------------------------------
344: 
345: 
346: class TestInitProcessSetup:
347:     """7.9: __init__ initializes _process with correct signal connections."""
348: 
349:     def test_7_9_process_is_qprocess_instance(self, app):
350:         """7.9: __init__ creates _process as QProcess instance."""
351:         from main import LlamaLaunchApp
352: 
353:         instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
354:         try:
355:             assert isinstance(instance._process, QProcess)
356:         finally:
357:             instance.close()
358: 
359:     def test_7_9_process_parent_is_app(self, app):
360:         """7.9: _process has the app instance as parent (auto-cleanup)."""
361:         from main import LlamaLaunchApp
362: 
363:         instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
364:         try:
365:             assert instance._process.parent() is instance
366:         finally:
367:             instance.close()
368: 
369:     def test_7_9_stdout_signal_connected(self, app):
370:         """7.9: _process.readyReadStandardOutput connected to _on_stdout."""
371:         from main import LlamaLaunchApp
372: 
373:         instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
374:         try:
375:             # Verify slot exists and is callable (indirect connection verification)
376:             assert hasattr(instance, "_on_stdout")
377:             assert callable(instance._on_stdout)
378:             # Emit the signal and verify the slot was called
379:             with patch.object(
380:                 instance, "_on_stdout", wraps=instance._on_stdout
381:             ) as mock:
382:                 instance._process.readyReadStandardOutput.emit()
383:                 mock.assert_called_once()
384:         finally:
385:             instance.close()
386: 
387:     def test_7_9_stderr_signal_connected(self, app):
388:         """7.9: _process.readyReadStandardError connected to _on_stderr."""
389:         from main import LlamaLaunchApp
390: 
391:         instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
392:         try:
393:             assert hasattr(instance, "_on_stderr")
394:             assert callable(instance._on_stderr)
395:             with patch.object(
396:                 instance, "_on_stderr", wraps=instance._on_stderr
397:             ) as mock:
398:                 instance._process.readyReadStandardError.emit()
399:                 mock.assert_called_once()
400:         finally:
401:             instance.close()
402: 
403:     def test_7_9_finished_signal_connected(self, app):
404:         """7.9: _process.finished connected to _on_finished."""
405:         from main import LlamaLaunchApp
406: 
407:         instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
408:         try:
409:             assert hasattr(instance, "_on_finished")
410:             assert callable(instance._on_finished)
411:             with patch.object(
412:                 instance, "_on_finished", wraps=instance._on_finished
413:             ) as mock:
414:                 instance._process.finished.emit(0, QProcess.ExitStatus.NormalExit)
415:                 mock.assert_called_once()
416:         finally:
417:             instance.close()
418: 
419:     def test_7_9_error_signal_connected(self, app):
420:         """7.9: _process.errorOccurred connected to _on_error."""
421:         from main import LlamaLaunchApp
422: 
423:         instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
424:         try:
425:             assert hasattr(instance, "_on_error")
426:             assert callable(instance._on_error)
427:             with patch.object(instance, "_on_error", wraps=instance._on_error) as mock:
428:                 instance._process.errorOccurred.emit(QProcess.ProcessError.UnknownError)
429:                 mock.assert_called_once()
430:         finally:
431:             instance.close()

(End of file - total 431 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Volumes/teaching/Code/LLamaLauncher/tests/test_lifecycle.py",
  "limit": 300
}
```

**Output:**
```
<path>/Volumes/teaching/Code/LLamaLauncher/tests/test_lifecycle.py</path>
<type>file</type>
<content>
1: """Phase 6: Tests for initialization and lifecycle methods."""
2: 
3: import sys
4: import tempfile
5: from pathlib import Path
6: from unittest.mock import MagicMock, patch
7: 
8: import pytest
9: 
10: # Import production modules from project root in tests
11: _project_root = str(Path(__file__).resolve().parent.parent)
12: if _project_root not in sys.path:
13:     sys.path.insert(0, _project_root)
14: 
15: 
16: class _QtSignal:
17:     """Minimal simulation of a Qt signal for testing.
18: 
19:     Supports both connection verification (via recorded calls) and
20:     signal emission to verify that connected slots are invoked.
21:     """
22: 
23:     def __init__(self):
24:         self._callbacks = []
25:         self.connect = MagicMock()
26:         self.connect.side_effect = self._record_connect
27: 
28:     def _record_connect(self, callback):
29:         self._callbacks.append(callback)
30:         return callback
31: 
32:     def emit(self, *args, **kwargs):
33:         """Emit the signal, invoking all connected slots."""
34:         for callback in self._callbacks:
35:             callback(*args, **kwargs)
36: 
37: 
38: class _MockWidget:
39:     """Minimal mock widget with QtSignal-based signals."""
40: 
41:     def __init__(self):
42:         self.clicked = _QtSignal()
43:         self.textChanged = _QtSignal()
44: 
45: 
46: @pytest.fixture()
47: def temp_dir():
48:     """Provide temporary cleaned up directory.
49: 
50:     Returns a Path to a temporary directory that removes itself afterward.
51:     """
52:     with tempfile.TemporaryDirectory() as tmpdir:
53:         yield Path(tmpdir)
54: 
55: 
56: class TestCreateCacheDir:
57:     """Test _create_cache_dir creates cache directory and returns Path."""
58: 
59:     def test_6_1_creates_cache_directory_and_returns_path(self, qapp):
60:         """_create_cache_dir creates the cache directory on disk and returns it as a Path.
61: 
62:         The returned path should exist and be a valid directory.
63:         """
64:         from main import LlamaLaunchApp
65: 
66:         app = LlamaLaunchApp(host="127.0.0.1", port=8080)
67: 
68:         assert isinstance(app._cache_dir, Path)
69:         assert app._cache_dir.exists()
70:         assert app._cache_dir.is_dir()
71:         assert "llama-launcher" in str(app._cache_dir)
72: 
73: 
74: class TestSaveConfig:
75:     """Test _save_config behavior."""
76: 
77:     def test_6_8_calls_save_config_as_when_no_last_config_path(self, qapp):
78:         """_save_config calls _save_config_as when _last_config_path does not exist.
79: 
80:         When there is no previously saved config path, save should prompt
81:         the user for a location via _save_config_as.
82:         """
83:         from main import LlamaLaunchApp
84: 
85:         app = LlamaLaunchApp(host="127.0.0.1", port=8080)
86:         app._save_config_as = MagicMock()
87:         app._write_config_file = MagicMock()
88: 
89:         assert not hasattr(app, "_last_config_path")
90:         app._save_config()
91: 
92:         app._save_config_as.assert_called_once()
93:         app._write_config_file.assert_not_called()
94: 
95:     def test_6_9_writes_to_last_saved_path_when_exists(self, qapp):
96:         """_save_config writes to _last_config_path when it exists.
97: 
98:         When a previous config path is available, save should write directly
99:         to that path without prompting.
100:         """
101:         from main import LlamaLaunchApp
102: 
103:         app = LlamaLaunchApp(host="127.0.0.1", port=8080)
104:         app._last_config_path = Path("/tmp/test-config.json")
105:         app._save_config_as = MagicMock()
106:         app._write_config_file = MagicMock()
107: 
108:         app._save_config()
109: 
110:         app._write_config_file.assert_called_once_with(app._last_config_path)
111:         app._save_config_as.assert_not_called()
112: 
113: 
114: class TestSaveLastSession:
115:     """Test _save_last_session saves settings to QSettings."""
116: 
117:     def test_6_11_saves_model_path_host_port_and_geometry(self, qapp):
118:         """_save_last_session saves model path, host, port, and window geometry.
119: 
120:         All four values should be written to QSettings with the correct keys.
121:         """
122:         from main import LlamaLaunchApp
123: 
124:         # Mock QSettings: configure value() for _load_last_session (called in __init__)
125:         # and capture setValue() calls from _save_last_session
126:         mock_settings_instance = MagicMock()
127:         mock_settings_instance.value.return_value = None  # no saved geometry
128: 
129:         with patch("main.QSettings", return_value=mock_settings_instance):
130:             app = LlamaLaunchApp(host="127.0.0.1", port=8080)
131: 
132:             # Configure widget mocks with expected values
133:             app.model_path_edit = MagicMock()
134:             app.model_path_edit.property.return_value = "/models/test.gguf"
135:             app.host_line_edit = MagicMock()
136:             app.host_line_edit.text.return_value = "192.168.1.100"
137:             app.port_line_edit = MagicMock()
138:             app.port_line_edit.text.return_value = "9000"
139:             app.saveGeometry = MagicMock(return_value=b"geometry-data")
140: 
141:             app._save_last_session()
142: 
143:             # Verify all four values were saved
144:             calls = mock_settings_instance.setValue.call_args_list
145:             assert len(calls) == 4
146: 
147:             call_keys = {call[0][0] for call in calls}
148:             assert "lastModelPath" in call_keys
149:             assert "host" in call_keys
150:             assert "port" in call_keys
151:             assert "windowGeometry" in call_keys
152: 
153:             # Verify specific values
154:             mock_settings_instance.setValue.assert_any_call("lastModelPath", "/models/test.gguf")
155:             mock_settings_instance.setValue.assert_any_call("host", "192.168.1.100")
156:             mock_settings_instance.setValue.assert_any_call("port", "9000")
157:             mock_settings_instance.setValue.assert_any_call("windowGeometry", b"geometry-data")
158: 
159:     def test_6_11_saves_empty_model_path_when_none(self, qapp):
160:         """_save_last_session saves empty string when model path is None.
161: 
162:         If the model path property returns None, an empty string should be saved.
163:         """
164:         from main import LlamaLaunchApp
165: 
166:         mock_settings_instance = MagicMock()
167:         mock_settings_instance.value.return_value = None  # no saved geometry
168:         with patch("main.QSettings", return_value=mock_settings_instance):
169:             app = LlamaLaunchApp(host="127.0.0.1", port=8080)
170: 
171:             app.model_path_edit = MagicMock()
172:             app.model_path_edit.property.return_value = None
173:             app.host_line_edit = MagicMock()
174:             app.host_line_edit.text.return_value = "127.0.0.1"
175:             app.port_line_edit = MagicMock()
176:             app.port_line_edit.text.return_value = "8080"
177:             app.saveGeometry = MagicMock(return_value=b"")
178: 
179:             app._save_last_session()
180: 
181:             mock_settings_instance.setValue.assert_any_call("lastModelPath", "")
182: 
183: 
184: class TestCloseEvent:
185:     """Test closeEvent lifecycle behavior."""
186: 
187:     def test_6_14_calls_save_last_session_before_closing(self, qapp):
188:         """closeEvent calls _save_last_session before delegating to parent.
189: 
190:         The session must be saved before the window closes so settings
191:         are persisted on disk.
192:         """
193:         from PySide6.QtGui import QCloseEvent
194: 
195:         from main import LlamaLaunchApp
196: 
197:         app = LlamaLaunchApp(host="127.0.0.1", port=8080)
198:         app._save_last_session = MagicMock()
199: 
200:         close_event = QCloseEvent()
201:         app.closeEvent(close_event)
202: 
203:         app._save_last_session.assert_called_once()
204:         # super().closeEvent() accepts the event by default
205:         assert close_event.isAccepted()
206: 
207: 
208: class TestCreateFileMenu:
209:     """Test _create_file_menu creates File menu with correct actions."""
210: 
211:     def test_6_7_creates_file_menu_with_save_save_as_load_actions(self, qapp):
212:         """_create_file_menu creates a File menu with Save, Save As, and Load actions.
213: 
214:         The File menu should be added to the menu bar and contain three actions
215:         that are connected to their respective slot methods.
216:         """
217:         from main import LlamaLaunchApp
218: 
219:         app = LlamaLaunchApp(host="127.0.0.1", port=8080)
220: 
221:         # Verify the File menu exists in the menu bar
222:         # QMenuBar.actions() returns QActions that represent menus
223:         file_menu = None
224:         for action in app.menuBar().actions():
225:             menu = action.menu()
226:             if menu is not None and "File" in menu.title():
227:                 file_menu = menu
228:                 break
229: 
230:         assert file_menu is not None, "File menu should exist in menu bar"
231: 
232:         # Verify the menu has three actions
233:         actions = file_menu.actions()
234:         assert len(actions) == 3
235: 
236:         action_texts = [action.text() for action in actions]
237:         assert any("Save Configuration" in text for text in action_texts)
238:         assert any("Save As" in text for text in action_texts)
239:         assert any("Load Configuration" in text for text in action_texts)
240: 
241:     def test_6_7_save_action_connected_to_save_config(self, qapp):
242:         """The Save action is connected to _save_config method."""
243:         from main import LlamaLaunchApp
244: 
245:         app = LlamaLaunchApp(host="127.0.0.1", port=8080)
246:         app._save_config = MagicMock()
247: 
248:         # Find and trigger the Save action in File menu
249:         for action in app.menuBar().actions():
250:             menu = action.menu()
251:             if menu is not None and "File" in menu.title():
252:                 for submenu_action in menu.actions():
253:                     if "Save Configuration" in submenu_action.text():
254:                         submenu_action.trigger()
255:                         break
256:                 break
257: 
258:         app._save_config.assert_called_once()
259: 
260:     def test_6_7_load_action_connected_to_load_config(self, qapp):
261:         """The Load action is connected to _load_config method."""
262:         from main import LlamaLaunchApp
263: 
264:         app = LlamaLaunchApp(host="127.0.0.1", port=8080)
265:         app._load_config = MagicMock()
266: 
267:         # Find and trigger the Load action in File menu
268:         for action in app.menuBar().actions():
269:             menu = action.menu()
270:             if menu is not None and "File" in menu.title():
271:                 for submenu_action in menu.actions():
272:                     if "Load Configuration" in submenu_action.text():
273:                         submenu_action.trigger()
274:                         break
275:                 break
276: 
277:         app._load_config.assert_called_once()
278: 
279: 
280: class TestLoadLastSession:
281:     """Test _load_last_session restores settings from QSettings."""
282: 
283:     def test_6_12_restores_host_port_and_model_path(self, qapp):
284:         """_load_last_session restores host, port, and model path from QSettings.
285: 
286:         When values are saved in QSettings, they should be restored to the
287:         corresponding UI widgets on application startup.
288:         """
289:         from main import LlamaLaunchApp
290: 
291:         # Mock QSettings to return saved values
292:         mock_settings_instance = MagicMock()
293:         mock_settings_instance.value.side_effect = lambda key, default="": {
294:             "windowGeometry": None,
295:             "host": "192.168.1.50",
296:             "port": "9999",
297:             "lastModelPath": "/models/previously-used.gguf",
298:         }.get(key, default)
299: 
300:         with patch("main.QSettings", return_value=mock_settings_instance):

(Showing lines 1-300 of 515. Use offset=301 to continue.)
</content>
```

**Tool: bash**

**Input:**
```json
{
  "command": "uv run pytest --collect-only 2>&1 | head -50",
  "description": "Check pytest collection"
}
```

**Output:**
```
============================= test session starts ==============================
platform darwin -- Python 3.14.0, pytest-9.1.0, pluggy-1.6.0
PySide6 6.11.1 -- Qt runtime 6.11.1 -- Qt compiled 6.11.1
rootdir: /Volumes/teaching/Code/LLamaLauncher
configfile: pyproject.toml
testpaths: tests
plugins: cov-7.1.0, qt-4.5.0
collected 187 items

<Dir LLamaLauncher>
  <Package tests>
    <Module test_config.py>
      <Class TestVersionString>
        <Function test_collects_version_string_as_1_0>
      <Class TestFilePaths>
        <Function test_collects_model_path_from_fullPath_property>
        <Function test_collects_mmproj_and_draft_and_json_schema_paths>
        <Function test_handles_empty_paths_as_empty_strings_not_none>
      <Class TestServerSettings>
        <Function test_collects_server_host_port_api_key>
        <Function test_handles_invalid_port_text_as_default_8080>
        <Function test_handles_empty_port_text_as_default_8080>
      <Class TestSamplingParameters>
        <Function test_sampling_param_has_enabled_and_value_format>
        <Function test_collects_all_sampling_params>
      <Class TestPerformanceParameters>
        <Function test_performance_params_have_enabled_value_format>
        <Function test_collects_flash_attn_combobox_text>
        <Function test_collects_mmap_mlock_cont_batching_booleans>
      <Class TestAdvancedParameters>
        <Function test_collects_advanced_params>
        <Function test_collects_rope_scaling_combobox_text>
      <Class TestOtherSettings>
        <Function test_collects_context_size_from_user_role>
        <Function test_collects_more_options_and_no_mmproj_offload>
      <Class TestEndToEnd>
        <Function test_collect_config_returns_all_expected_keys>
        <Function test_config_round_trip_save_and_load>
    <Module test_edge_cases.py>
      <Class TestLaunchModelMissingFile>
        <Function test_7_1_appends_error_when_no_model_selected>
      <Class TestApiKeyDefault>
        <Function test_7_2_api_key_defaults_to_12345_when_empty>
        <Function test_7_2_api_key_uses_line_edit_value_when_not_empty>
      <Class TestApplyParamEdgeCases>
        <Function test_7_3_uses_spinbox_default_when_value_key_missing>
        <Function test_7_3_applies_value_when_present>
        <Function test_7_3_defaults_enabled_to_false>
      <Class TestApplyComboParamEdgeCases>
        <Function test_7_4_no_change_when_text_not_in_combobox>

```

---

## Assistant (Python-Code-Quality · Claude Sonnet 4.5 · 296.0s)

Now let me run the tests to see current coverage and results:

**Tool: bash**

**Input:**
```json
{
  "command": "uv run pytest --cov=. --cov-report=term-missing --tb=short -q 2>&1 | tail -100",
  "description": "Run tests with coverage",
  "timeout": 60000
}
```

**Output:**
```
...................Release of profile requested but WebEnginePage still not deleted. Expect troubles !
.Release of profile requested but WebEnginePage still not deleted. Expect troubles !
.Release of profile requested but WebEnginePage still not deleted. Expect troubles !
.Release of profile requested but WebEnginePage still not deleted. Expect troubles !
.Release of profile requested but WebEnginePage still not deleted. Expect troubles !
.Release of profile requested but WebEnginePage still not deleted. Expect troubles !
.Release of profile requested but WebEnginePage still not deleted. Expect troubles !
.Release of profile requested but WebEnginePage still not deleted. Expect troubles !
.Release of profile requested but WebEnginePage still not deleted. Expect troubles !
.Release of profile requested but WebEnginePage still not deleted. Expect troubles !
.Release of profile requested but WebEnginePage still not deleted. Expect troubles !
.Release of profile requested but WebEnginePage still not deleted. Expect troubles !
.Release of profile requested but WebEnginePage still not deleted. Expect troubles !
.Release of profile requested but WebEnginePage still not deleted. Expect troubles !
.Release of profile requested but WebEnginePage still not deleted. Expect troubles !
.Release of profile requested but WebEnginePage still not deleted. Expect troubles !
...................................... [ 38%]
........................................................................ [ 77%]
.........................................../Volumes/teaching/Code/LLamaLauncher/.venv/lib/python3.14/site-packages/coverage/report_core.py:113: CoverageWarning: Couldn't parse '/Volumes/teaching/Code/LLamaLauncher/pyscript': No source for code: '/Volumes/teaching/Code/LLamaLauncher/pyscript'. (couldnt-parse); see https://coverage.readthedocs.io/en/7.14.1/messages.html#warning-couldnt-parse
  coverage._warn(msg, slug="couldnt-parse")
/Volumes/teaching/Code/LLamaLauncher/.venv/lib/python3.14/site-packages/coverage/report_core.py:113: CoverageWarning: Couldn't parse '/Volumes/teaching/Code/LLamaLauncher/shibokensupport/__init__.py': No source for code: '/Volumes/teaching/Code/LLamaLauncher/shibokensupport/__init__.py'. (couldnt-parse); see https://coverage.readthedocs.io/en/7.14.1/messages.html#warning-couldnt-parse
  coverage._warn(msg, slug="couldnt-parse")
/Volumes/teaching/Code/LLamaLauncher/.venv/lib/python3.14/site-packages/coverage/report_core.py:113: CoverageWarning: Couldn't parse '/Volumes/teaching/Code/LLamaLauncher/shibokensupport/feature.py': No source for code: '/Volumes/teaching/Code/LLamaLauncher/shibokensupport/feature.py'. (couldnt-parse); see https://coverage.readthedocs.io/en/7.14.1/messages.html#warning-couldnt-parse
  coverage._warn(msg, slug="couldnt-parse")
/Volumes/teaching/Code/LLamaLauncher/.venv/lib/python3.14/site-packages/coverage/report_core.py:113: CoverageWarning: Couldn't parse '/Volumes/teaching/Code/LLamaLauncher/shibokensupport/signature/__init__.py': No source for code: '/Volumes/teaching/Code/LLamaLauncher/shibokensupport/signature/__init__.py'. (couldnt-parse); see https://coverage.readthedocs.io/en/7.14.1/messages.html#warning-couldnt-parse
  coverage._warn(msg, slug="couldnt-parse")
/Volumes/teaching/Code/LLamaLauncher/.venv/lib/python3.14/site-packages/coverage/report_core.py:113: CoverageWarning: Couldn't parse '/Volumes/teaching/Code/LLamaLauncher/shibokensupport/signature/errorhandler.py': No source for code: '/Volumes/teaching/Code/LLamaLauncher/shibokensupport/signature/errorhandler.py'. (couldnt-parse); see https://coverage.readthedocs.io/en/7.14.1/messages.html#warning-couldnt-parse
  coverage._warn(msg, slug="couldnt-parse")
/Volumes/teaching/Code/LLamaLauncher/.venv/lib/python3.14/site-packages/coverage/report_core.py:113: CoverageWarning: Couldn't parse '/Volumes/teaching/Code/LLamaLauncher/shibokensupport/signature/importhandler.py': No source for code: '/Volumes/teaching/Code/LLamaLauncher/shibokensupport/signature/importhandler.py'. (couldnt-parse); see https://coverage.readthedocs.io/en/7.14.1/messages.html#warning-couldnt-parse
  coverage._warn(msg, slug="couldnt-parse")
/Volumes/teaching/Code/LLamaLauncher/.venv/lib/python3.14/site-packages/coverage/report_core.py:113: CoverageWarning: Couldn't parse '/Volumes/teaching/Code/LLamaLauncher/shibokensupport/signature/layout.py': No source for code: '/Volumes/teaching/Code/LLamaLauncher/shibokensupport/signature/layout.py'. (couldnt-parse); see https://coverage.readthedocs.io/en/7.14.1/messages.html#warning-couldnt-parse
  coverage._warn(msg, slug="couldnt-parse")
/Volumes/teaching/Code/LLamaLauncher/.venv/lib/python3.14/site-packages/coverage/report_core.py:113: CoverageWarning: Couldn't parse '/Volumes/teaching/Code/LLamaLauncher/shibokensupport/signature/lib/__init__.py': No source for code: '/Volumes/teaching/Code/LLamaLauncher/shibokensupport/signature/lib/__init__.py'. (couldnt-parse); see https://coverage.readthedocs.io/en/7.14.1/messages.html#warning-couldnt-parse
  coverage._warn(msg, slug="couldnt-parse")
/Volumes/teaching/Code/LLamaLauncher/.venv/lib/python3.14/site-packages/coverage/report_core.py:113: CoverageWarning: Couldn't parse '/Volumes/teaching/Code/LLamaLauncher/shibokensupport/signature/lib/enum_sig.py': No source for code: '/Volumes/teaching/Code/LLamaLauncher/shibokensupport/signature/lib/enum_sig.py'. (couldnt-parse); see https://coverage.readthedocs.io/en/7.14.1/messages.html#warning-couldnt-parse
  coverage._warn(msg, slug="couldnt-parse")
/Volumes/teaching/Code/LLamaLauncher/.venv/lib/python3.14/site-packages/coverage/report_core.py:113: CoverageWarning: Couldn't parse '/Volumes/teaching/Code/LLamaLauncher/shibokensupport/signature/lib/pyi_generator.py': No source for code: '/Volumes/teaching/Code/LLamaLauncher/shibokensupport/signature/lib/pyi_generator.py'. (couldnt-parse); see https://coverage.readthedocs.io/en/7.14.1/messages.html#warning-couldnt-parse
  coverage._warn(msg, slug="couldnt-parse")
/Volumes/teaching/Code/LLamaLauncher/.venv/lib/python3.14/site-packages/coverage/report_core.py:113: CoverageWarning: Couldn't parse '/Volumes/teaching/Code/LLamaLauncher/shibokensupport/signature/lib/tool.py': No source for code: '/Volumes/teaching/Code/LLamaLauncher/shibokensupport/signature/lib/tool.py'. (couldnt-parse); see https://coverage.readthedocs.io/en/7.14.1/messages.html#warning-couldnt-parse
  coverage._warn(msg, slug="couldnt-parse")
/Volumes/teaching/Code/LLamaLauncher/.venv/lib/python3.14/site-packages/coverage/report_core.py:113: CoverageWarning: Couldn't parse '/Volumes/teaching/Code/LLamaLauncher/shibokensupport/signature/loader.py': No source for code: '/Volumes/teaching/Code/LLamaLauncher/shibokensupport/signature/loader.py'. (couldnt-parse); see https://coverage.readthedocs.io/en/7.14.1/messages.html#warning-couldnt-parse
  coverage._warn(msg, slug="couldnt-parse")
/Volumes/teaching/Code/LLamaLauncher/.venv/lib/python3.14/site-packages/coverage/report_core.py:113: CoverageWarning: Couldn't parse '/Volumes/teaching/Code/LLamaLauncher/shibokensupport/signature/mapping.py': No source for code: '/Volumes/teaching/Code/LLamaLauncher/shibokensupport/signature/mapping.py'. (couldnt-parse); see https://coverage.readthedocs.io/en/7.14.1/messages.html#warning-couldnt-parse
  coverage._warn(msg, slug="couldnt-parse")
/Volumes/teaching/Code/LLamaLauncher/.venv/lib/python3.14/site-packages/coverage/report_core.py:113: CoverageWarning: Couldn't parse '/Volumes/teaching/Code/LLamaLauncher/shibokensupport/signature/parser.py': No source for code: '/Volumes/teaching/Code/LLamaLauncher/shibokensupport/signature/parser.py'. (couldnt-parse); see https://coverage.readthedocs.io/en/7.14.1/messages.html#warning-couldnt-parse
  coverage._warn(msg, slug="couldnt-parse")
/Volumes/teaching/Code/LLamaLauncher/.venv/lib/python3.14/site-packages/coverage/report_core.py:113: CoverageWarning: Couldn't parse '/Volumes/teaching/Code/LLamaLauncher/signature_bootstrap.py': No source for code: '/Volumes/teaching/Code/LLamaLauncher/signature_bootstrap.py'. (couldnt-parse); see https://coverage.readthedocs.io/en/7.14.1/messages.html#warning-couldnt-parse
  coverage._warn(msg, slug="couldnt-parse")
                              [100%]
================================ tests coverage ================================
_______________ coverage: platform darwin, python 3.14.0-final-0 _______________

Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
main.py                472     44    91%   198-206, 392-412, 652-653, 671-672, 693-696, 986, 993, 996, 1008-1009, 1012-1014, 1019, 1027, 1123-1144
process_command.py      48      0   100%
ui_loader.py            43      0   100%
--------------------------------------------------
TOTAL                  563     44    92%
Required test coverage of 90.0% reached. Total coverage: 92.18%
187 passed in 2.43s

```

---

## Assistant (Python-Code-Quality · Claude Sonnet 4.5 · 47.1s)

Excellent! Now let me read a few more test files to complete my understanding:

**Tool: read**

**Input:**
```json
{
  "filePath": "/Volumes/teaching/Code/LLamaLauncher/tests/test_ui_loader.py"
}
```

**Output:**
```
<path>/Volumes/teaching/Code/LLamaLauncher/tests/test_ui_loader.py</path>
<type>file</type>
<content>
1: """Tests for ui_loader.load_ui().
2: 
3: Covers error handling, widget attribute assignment, parent type setup,
4: and path type support.
5: """
6: 
7: from pathlib import Path
8: from unittest.mock import MagicMock, patch
9: 
10: import pytest
11: from PySide6.QtCore import QSize
12: from PySide6.QtWidgets import QDialog, QLayout, QMainWindow, QWidget
13: 
14: from ui_loader import load_ui
15: 
16: 
17: @pytest.fixture
18: def mock_file_open_failure():
19:     """1.2.1/1.2.2: Patch QFile to simulate open() failure.
20: 
21:     Returns the patched QFile class mock for tests that expect
22:     RuntimeError when the UI file cannot be opened.
23:     """
24:     with patch("ui_loader.QFile") as mock_qfile_cls:
25:         mock_qfile = MagicMock()
26:         mock_qfile_cls.return_value = mock_qfile
27:         mock_qfile.open.return_value = False
28:         yield mock_qfile_cls
29: 
30: 
31: @pytest.fixture
32: def mock_qt():
33:     """Module-level fixture for successful UI loading scenarios.
34: 
35:     Patches QFile, QUiLoader, and QVBoxLayout, then yields a factory
36:     function that creates fresh mock instances per test. This ensures
37:     each test gets isolated mocks with no shared mutable state.
38: 
39:     Yields:
40:         make_mocks: callable that returns a namespace with:
41:             - mock_qfile_cls: the patched QFile class mock
42:             - mock_loader_cls: the patched QUiLoader class mock
43:             - mock_vbox_cls: the patched QVBoxLayout class mock
44:             - mock_ui: a fresh MagicMock for the loaded UI
45:             - mock_loader: a fresh QUiLoader instance mock
46:             - mock_container: a fresh QVBoxLayout instance mock
47:     """
48:     with (
49:         patch("ui_loader.QFile") as mock_qfile_cls,
50:         patch("ui_loader.QUiLoader") as mock_loader_cls,
51:         patch("ui_loader.QVBoxLayout") as mock_vbox_cls,
52:     ):
53: 
54:         def make_mocks():
55:             """Create a fresh set of mock instances for one test."""
56:             mock_qfile = MagicMock()
57:             mock_qfile_cls.return_value = mock_qfile
58:             mock_qfile.open.return_value = True
59: 
60:             mock_ui = MagicMock()
61:             mock_ui.layout.return_value = None
62:             mock_ui.windowTitle.return_value = ""
63:             mock_ui.size.return_value = QSize(0, 0)
64: 
65:             mock_loader = mock_loader_cls.return_value
66:             mock_loader.load.return_value = mock_ui
67: 
68:             mock_container = mock_vbox_cls.return_value
69: 
70:             return MagicMock(
71:                 mock_qfile_cls=mock_qfile_cls,
72:                 mock_loader_cls=mock_loader_cls,
73:                 mock_vbox_cls=mock_vbox_cls,
74:                 mock_ui=mock_ui,
75:                 mock_loader=mock_loader,
76:                 mock_container=mock_container,
77:             )
78: 
79:         yield make_mocks
80: 
81: 
82: class TestLoadUIFileErrors:
83:     """1.2.1-1.2.3: Error handling when UI files cannot be loaded."""
84: 
85:     def test_load_ui_raises_when_file_does_not_exist(self, mock_file_open_failure):
86:         """1.2.1: load_ui() raises RuntimeError when UI file does not exist."""
87:         parent = QWidget()
88:         with pytest.raises(RuntimeError, match="Cannot open UI file"):
89:             load_ui("/nonexistent/path.ui", parent)
90: 
91:     def test_load_ui_raises_when_file_open_fails(self, mock_file_open_failure):
92:         """1.2.2: load_ui() raises RuntimeError when UI file fails to open."""
93:         parent = QWidget()
94:         with pytest.raises(RuntimeError, match="Cannot open UI file"):
95:             load_ui(Path("/restricted/path.ui"), parent)
96: 
97:     def test_load_ui_raises_when_file_is_invalid(self, mock_qt):
98:         """1.2.3: load_ui() raises RuntimeError when UI file is invalid/empty."""
99:         mocks = mock_qt()
100:         mocks.mock_loader.load.return_value = None
101: 
102:         parent = QWidget()
103:         with pytest.raises(RuntimeError, match="Failed to load UI file"):
104:             load_ui("/invalid/ui.ui", parent)
105: 
106: 
107: class TestLoadUIWidgetAttributeAssignment:
108:     """1.2.4-1.2.6: Widget and layout attribute assignment by objectName."""
109: 
110:     def test_load_ui_assigns_widget_attributes_by_object_name(self, mock_qt):
111:         """1.2.4: load_ui() assigns widget attributes by objectName (QWidget)."""
112:         mocks = mock_qt()
113: 
114:         mock_button = MagicMock(spec=QWidget)
115:         mock_button.objectName.return_value = "myButton"
116: 
117:         mock_label = MagicMock(spec=QWidget)
118:         mock_label.objectName.return_value = "myLabel"
119: 
120:         mocks.mock_ui.findChildren.return_value = [mock_button, mock_label]
121: 
122:         parent = QWidget()
123:         load_ui("/test/ui.ui", parent)
124: 
125:         assert parent.myButton is mock_button
126:         assert parent.myLabel is mock_label
127: 
128:     def test_load_ui_assigns_layout_attributes_by_object_name(self, mock_qt):
129:         """1.2.5: load_ui() assigns layout attributes by objectName."""
130:         mocks = mock_qt()
131: 
132:         mock_layout = MagicMock(spec=QLayout)
133:         mock_layout.objectName.return_value = "mainLayout"
134: 
135:         def find_children(cls):
136:             if cls == QLayout:
137:                 return [mock_layout]
138:             return []
139: 
140:         mocks.mock_ui.findChildren.side_effect = find_children
141: 
142:         parent = QWidget()
143:         load_ui("/test/ui.ui", parent)
144: 
145:         assert parent.mainLayout is mock_layout
146: 
147:     def test_load_ui_captures_top_level_layout_not_in_find_children(self, mock_qt):
148:         """1.2.6: load_ui() captures top-level layout when not found by findChildren."""
149:         mocks = mock_qt()
150: 
151:         mock_main_layout = MagicMock(spec=QLayout)
152:         mock_main_layout.objectName.return_value = "topLevelLayout"
153: 
154:         mocks.mock_ui.findChildren.return_value = []
155:         mocks.mock_ui.layout.return_value = mock_main_layout
156: 
157:         parent = QWidget()
158:         load_ui("/test/ui.ui", parent)
159: 
160:         assert parent.topLevelLayout is mock_main_layout
161: 
162: 
163: class TestLoadUISetupByParentType:
164:     """1.2.7-1.2.9: Widget setup for different parent widget types."""
165: 
166:     def test_load_ui_sets_up_dialog_correctly(self, mock_qt):
167:         """1.2.7: load_ui() sets up QDialog correctly (layout, title, size)."""
168:         mocks = mock_qt()
169: 
170:         mock_layout = MagicMock()
171:         mock_layout.objectName.return_value = ""
172: 
173:         mocks.mock_ui.layout.return_value = mock_layout
174:         mocks.mock_ui.windowTitle.return_value = "My Dialog"
175:         mocks.mock_ui.size.return_value = QSize(400, 300)
176: 
177:         parent = QDialog()
178:         parent.setLayout = MagicMock()
179:         parent.setWindowTitle = MagicMock()
180:         parent.resize = MagicMock()
181:         load_ui("/test/dialog.ui", parent)
182: 
183:         parent.setLayout.assert_called_with(mock_layout)
184:         parent.setWindowTitle.assert_called_with("My Dialog")
185:         parent.resize.assert_called_with(QSize(400, 300))
186: 
187:     def test_load_ui_sets_up_main_window_correctly(self, mock_qt):
188:         """1.2.8: load_ui() sets up QMainWindow correctly (central widget, title, size)."""
189:         mocks = mock_qt()
190: 
191:         mocks.mock_ui.windowTitle.return_value = "My Window"
192:         mocks.mock_ui.size.return_value = QSize(800, 600)
193: 
194:         parent = QMainWindow()
195:         parent.setCentralWidget = MagicMock()
196:         parent.setWindowTitle = MagicMock()
197:         parent.resize = MagicMock()
198:         load_ui("/test/window.ui", parent)
199: 
200:         parent.setCentralWidget.assert_called_with(mocks.mock_ui)
201:         parent.setWindowTitle.assert_called_with("My Window")
202:         parent.resize.assert_called_with(QSize(800, 600))
203: 
204:     def test_load_ui_embeds_widget_via_zero_margin_layout(self, mock_qt):
205:         """1.2.9: load_ui() embeds QWidget via zero-margin layout."""
206:         mocks = mock_qt()
207: 
208:         mocks.mock_ui.windowTitle.return_value = "Embedded UI"
209:         mocks.mock_ui.size.return_value = QSize(300, 200)
210: 
211:         parent = QWidget()
212:         parent.setWindowTitle = MagicMock()
213:         parent.resize = MagicMock()
214:         load_ui("/test/embed.ui", parent)
215: 
216:         mocks.mock_vbox_cls.assert_called_with(parent)
217:         mocks.mock_container.setContentsMargins.assert_called_with(0, 0, 0, 0)
218:         mocks.mock_container.addWidget.assert_called_with(mocks.mock_ui)
219:         parent.setWindowTitle.assert_called_with("Embedded UI")
220:         parent.resize.assert_called_with(QSize(300, 200))
221: 
222: 
223: class TestLoadUIPathSupport:
224:     """1.2.10: Path type acceptance."""
225: 
226:     def test_load_ui_accepts_path_object(self, mock_qt):
227:         """1.2.10: load_ui() accepts both str and Path for ui_file_path."""
228:         mocks = mock_qt()
229: 
230:         parent = QWidget()
231:         result = load_ui(Path("/test/path.ui"), parent)
232: 
233:         mocks.mock_qfile_cls.assert_called_with(Path("/test/path.ui"))
234:         assert result is mocks.mock_ui

(End of file - total 234 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Volumes/teaching/Code/LLamaLauncher/Testing.md",
  "limit": 150
}
```

**Output:**
```
<path>/Volumes/teaching/Code/LLamaLauncher/Testing.md</path>
<type>file</type>
<content>
1: # Testing Plan for LLamaLauncher
2: 
3: ## Overview
4: 
5: This document outlines the phased approach to achieving >90% test coverage on the LLamaLauncher project. Tests should be written **before** implementation code following TDD principles (Red-Green-Refactor).
6: 
7: ### Current State
8: 
9: | Metric | Value |
10: |--------|-------|
11: | Total source files | 2 (`main.py`, `ui_loader.py`) |
12: | Lines of code | ~950 (main.py: 880, ui_loader.py: 69) |
13: | Existing tests | None |
14: | Test framework | pytest (in dev dependencies) |
15: | Target coverage | >90% |
16: 
17: ### Prerequisites
18: 
19: Before writing any tests, install the required testing dependencies:
20: 
21: ```bash
22: uv add --dev pytest-qt pytest-cov
23: ```
24: 
25: - **pytest-qt**: Provides fixtures and utilities for Qt application testing
26: - **pytest-cov**: Generates coverage reports
27: 
28: ---
29: 
30: ## Phase 1: Foundation (Week 1)
31: 
32: ### Goal: Establish test infrastructure and test the smallest, most isolated module first.
33: 
34: ### 1.1 Project Setup
35: 
36: - [ x] Create `tests/` directory with `__init__.py`
37: - [ x] Create `tests/conftest.py` with shared fixtures:
38:   - `qapp`: QApplication singleton (pytest-qt)
39:   - `temp_dir`: Temporary directory for test files
40:   - `mock_qprocess`: Patched QProcess for process tests
41: - [ x] Configure `pyproject.toml` for pytest and coverage:
42:   ```toml
43:   [tool.pytest.ini_options]
44:   testpaths = ["tests"]
45:   qt_api = "pyside6"
46: 
47:   [tool.coverage.run]
48:   source = ["src", "."]
49:   omit = ["tests/**", "**/conftest.py"]
50: 
51:   [tool.coverage.report]
52:   exclude_lines = [
53:       "pragma: no cover",
54:       "def __repr__",
55:       "raise NotImplementedError",
56:       "if TYPE_CHECKING:",
57:       "@abstractmethod",
58:   ]
59:   fail_under = 90
60:   ```
61: - [ x] Create `tests/files/` directory for test fixtures (sample JSON configs, etc.)
62: 
63: ### 1.2 Test `ui_loader.py` (Priority: Highest)
64: 
65: **Why first?** Small module (69 lines), pure utility function, minimal Qt coupling, easy to mock.
66: 
67: **File:** `tests/test_ui_loader.py`
68: 
69: | # | Test Case | Target Lines | Difficulty |
70: |---|-----------|-------------|------------|
71: | 1.2.1 | `load_ui()` raises `RuntimeError` when UI file does not exist | L24-26 | Easy |
72: | 1.2.2 | `load_ui()` raises `RuntimeError` when UI file fails to open | L24-26 | Medium |
73: | 1.2.3 | `load_ui()` raises `RuntimeError` when UI file is invalid/empty | L31-32 | Medium |
74: | 1.2.4 | `load_ui()` assigns widget attributes by `objectName` (QWidget) | L34-37 | Medium |
75: | 1.2.5 | `load_ui()` assigns layout attributes by `objectName` | L39-42 | Medium |
76: | 1.2.6 | `load_ui()` captures top-level layout when not found by `findChildren` | L44-49 | Medium |
77: | 1.2.7 | `load_ui()` sets up QDialog correctly (layout, title, size) | L51-55 | Medium |
78: | 1.2.8 | `load_ui()` sets up QMainWindow correctly (central widget, title, size) | L56-59 | Medium |
79: | 1.2.9 | `load_ui()` embeds QWidget via zero-margin layout for non-dialog/mainwindow parents | L60-67 | Medium |
80: | 1.2.10 | `load_ui()` accepts both `str` and `Path` for `ui_file_path` | L11 | Easy |
81: 
82: **Estimated coverage from this module:** ~7% of total LOC
83: 
84: ---
85: 
86: ## Phase 2: Configuration Logic (Week 2)
87: 
88: ### Goal: Test the pure data transformation logic for configuration save/load.
89: 
90: **Strategy:** Extract configuration methods into a separate testable class or test them by creating a minimal mock widget that mimics the Qt widget interface. This is the highest-value testing work because configuration handling is pure logic with no external side effects.
91: 
92: **File:** `tests/test_config.py`
93: 
94: ### 2.1 Configuration Collection (`_collect_config`)
95: 
96: **Target:** Lines 218-291 in main.py
97: 
98: This method collects UI widget values into a dictionary. Test by creating mock widgets.
99: 
100: | # | Test Case | Target Lines | Difficulty |
101: |---|-----------|-------------|------------|
102: | 2.1.1 | Collects version string as `"1.0"` | L224 | Easy |
103: | 2.1.2 | Collects model_path from `fullPath` property | L227-232 | Medium |
104: | 2.1.3 | Collects mmproj_path, draft_model_path, json_schema_path | L228-232 | Medium |
105: | 2.1.4 | Handles empty paths as empty strings (not `None`) | L228-232 | Easy |
106: | 2.1.5 | Collects server host, port (as int), api_key | L235-239 | Medium |
107: | 2.1.6 | Handles invalid port text (non-digit) as default 8080 | L237 | Medium |
108: | 2.1.7 | Collects sampling parameters with enabled+value dict format | L242-255 | Hard |
109: | 2.1.8 | Collects all 11 sampling params (temperature, top_p, top_k, min_p, typical_p, repeat_penalty, repeat_last_n, presence_penalty, frequency_penalty, mirostat, mirostat_lr, mirostat_ent) | L242-255 | Hard |
110: | 2.1.9 | Collects performance parameters with enabled+value format | L258-272 | Hard |
111: | 2.1.10 | Collects flash_attn combobox text | L266 | Easy |
112: | 2.1.11 | Collects mmap, mlock, cont_batching booleans | L269-272 | Easy |
113: | 2.1.12 | Collects advanced params (draft_model, spec_draft_n_max, seed, grammar, json_schema) | L275-284 | Hard |
114: | 2.1.13 | Collects rope_scaling combobox text | L281 | Easy |
115: | 2.1.14 | Collects context_size from UserRole | L287 | Medium |
116: | 2.1.15 | Collects more_options and no_mmproj_offload | L288-289 | Easy |
117: 
118: ### 2.2 Configuration Writing (`_write_config_file`)
119: 
120: **Target:** Lines 204-216
121: 
122: | # | Test Case | Target Lines | Difficulty |
123: |---|-----------|-------------|------------|
124: | 2.2.1 | Writes valid JSON to file path | L204-216 | Medium |
125: | 2.2.2 | Appends success message to output_display | L214 | Easy |
126: | 2.2.3 | Shows QMessageBox.critical on write failure (permission denied) | L215-216 | Hard (requires mocking filesystem) |
127: 
128: ### 2.3 Configuration Loading (`_load_config`)
129: 
130: **Target:** Lines 293-313
131: 
132: | # | Test Case | Target Lines | Difficulty |
133: |---|-----------|-------------|------------|
134: | 2.3.1 | Loads valid JSON config and calls `_apply_config` | L293-313 | Hard |
135: | 2.3.2 | Handles json.JSONDecodeError with error dialog | L310-311 | Medium |
136: | 2.3.3 | Handles general file read errors with error dialog | L312-313 | Easy |
137: 
138: ### 2.4 Configuration Application (`_apply_config`)
139: 
140: **Target:** Lines 315-420
141: 
142: This is a large method (~105 lines). Break into focused tests:
143: 
144: | # | Test Case | Target Lines | Difficulty |
145: |---|-----------|-------------|------------|
146: | 2.4.1 | Applies files section (model_path, mmproj_path, draft_model_path, json_schema_path) | L322-327 | Medium |
147: | 2.4.2 | Applies server section (host, port, api_key) with defaults | L330-335 | Medium |
148: | 2.4.3 | Applies all sampling parameters via `_apply_param` | L338-351 | Hard |
149: | 2.4.4 | Applies performance parameters (gpu_layers, threads, etc.) | L354-362 | Hard |
150: | 2.4.5 | Applies flash_attn combobox selection | L364-368 | Easy |

(Showing lines 1-150 of 526. Use offset=151 to continue.)
</content>
```

**Tool: bash**

**Input:**
```json
{
  "command": "wc -l tests/*.py main.py ui_loader.py process_command.py | tail -5",
  "description": "Count lines of code"
}
```

**Output:**
```
     234 tests/test_ui_loader.py
    1144 main.py
      69 ui_loader.py
      98 process_command.py
    6093 total

```

---

## Assistant (Python-Code-Quality · Claude Sonnet 4.5 · 97.9s)

Now I have a comprehensive understanding of the project. Let me provide my detailed code review:

# Code Quality Review: LLamaLauncher

## Summary

This is a **well-structured Qt-based Python application** with impressive test coverage (92%). The code demonstrates good separation of concerns, comprehensive testing, and thoughtful architecture. However, there are several opportunities to improve maintainability, reduce complexity, and strengthen test quality.

**Overall Assessment:** Good quality with room for improvement in certain areas.

---

## Critical Issues

### 1. **God Class Anti-Pattern in `main.py`**

**Issue:** The `LlamaLaunchApp` class is **1144 lines** and handles too many responsibilities:
- UI initialization and setup
- Configuration collection and persistence
- Process lifecycle management
- File dialogs
- QSettings persistence
- Web view management
- Command building (though partially extracted)

**Impact:** Hard to test, hard to understand, hard to modify. Adding features requires touching this monolithic class.

**Recommendation:**
```python
# Split into focused classes:
class ConfigManager:
    """Handle config save/load/apply operations."""
    
class ProcessManager:
    """Handle llama-server process lifecycle."""
    
class UISetup:
    """Handle UI widget initialization."""
    
class LlamaLaunchApp(QMainWindow):
    """Coordinate between components."""
    def __init__(self):
        self.config_mgr = ConfigManager(self)
        self.process_mgr = ProcessManager(self)
        # Much thinner orchestration layer
```

### 2. **`_launch_model()` Method is 175 Lines**

**Issue:** Lines 870-1044 collect widget values inline, duplicating logic from `ConfigCollector`.

**Recommendation:** Use the existing `ConfigCollector` + `ProcessCommandBuilder`:
```python
def _launch_model(self) -> None:
    model_path = self.model_path_edit.property("fullPath")
    if not model_path:
        self.output_display.appendPlainText("Error: no model selected.")
        return
    
    # Use the tested, extracted logic
    collector = ConfigCollector(
        model_path_edit=self.model_path_edit,
        # ... all widgets
    )
    config = collector.collect_config()
    builder = ProcessCommandBuilder(config)
    cmd = builder.build_command()
    
    # Launch process
    self._server_url = f"http://{config['server']['host']}:{config['server']['port']}"
    self._auto_refresh_done = False
    self.output_display.clear()
    self.output_display.appendPlainText(f"Launching: {' '.join(cmd)}\n---\n")
    self._process.start(cmd[0], cmd[1:])
    # ... rest of side effects
```

**Why Critical:** The duplication means bugs must be fixed in two places, and tests don't verify the actual launch path.

### 3. **Missing Type Hints in Key Areas**

**Issue:** Many methods lack return type hints:
```python
def closeEvent(self, event) -> None:  # Missing QCloseEvent type
def _on_stdout(self) -> None:  # Good
def _on_error(self, error: QProcess.ProcessError) -> None:  # Good
```

**Recommendation:** Add full type annotations:
```python
from PySide6.QtGui import QCloseEvent

def closeEvent(self, event: QCloseEvent) -> None:
    self._save_last_session()
    super().closeEvent(event)
```

### 4. **`ConfigCollector` Uses `Any` for All Widgets**

**Issue:** The dataclass uses `Any` for 60+ fields, losing all type safety:
```python
@dataclass(slots=True)
class ConfigCollector:
    model_path_edit: Any = field(default=None)  # No type checking!
```

**Recommendation:** Use protocols or abstract base classes:
```python
from typing import Protocol

class LineEditLike(Protocol):
    def text(self) -> str: ...

class CheckBoxLike(Protocol):
    def isChecked(self) -> bool: ...

class SpinBoxLike(Protocol):
    def value(self) -> float: ...

@dataclass(slots=True)
class ConfigCollector:
    model_path_edit: LineEditLike
    enable_temperature_checkbox: CheckBoxLike
    temperature_spinbox: SpinBoxLike
```

This preserves duck typing while enabling type checking.

---

## Software Design Issues

### 5. **Tight Coupling Between UI and Logic**

**Issue:** `_collect_config()` in `main.py` directly accesses `self.model_path_edit`, making it impossible to test without Qt.

**Good:** You've extracted `ConfigCollector` in the test suite, but it's not used in production code.

**Recommendation:** Use `ConfigCollector` in `main.py`:
```python
def _collect_config(self) -> dict:
    """Collect UI values using ConfigCollector."""
    collector = ConfigCollector(
        model_path_edit=self.model_path_edit,
        # ... all widgets
    )
    return collector.collect_config()
```

### 6. **No Separation Between Data and Presentation**

**Issue:** Configuration logic is embedded in the UI class. The `config` dictionary is the only domain model.

**Recommendation:** Introduce a proper domain model:
```python
@dataclass
class ServerConfig:
    host: str
    port: int
    api_key: str

@dataclass
class ModelConfig:
    model_path: Path
    mmproj_path: Optional[Path]
    # ...

@dataclass
class LlamaConfig:
    server: ServerConfig
    model: ModelConfig
    sampling: SamplingConfig
    # ...
```

This provides:
- Type safety
- Validation at construction
- Clear domain language
- Easier testing

### 7. **Magic Strings and Magic Numbers**

**Issue:**
```python
api_key = self.api_key_line_edit.text() if self.api_key_line_edit.text() else "12345"
```

**Recommendation:**
```python
DEFAULT_API_KEY = "12345"
DEFAULT_PORT = 8080
DEFAULT_HOST = "127.0.0.1"

api_key = self.api_key_line_edit.text() or DEFAULT_API_KEY
```

---

## Test Quality Issues

### 8. **Tests Verify Implementation, Not Behavior**

**Major Problem:** Many tests check internal method calls rather than observable outcomes.

**Example from `test_process.py`:**
```python
def test_base_command_includes_llama_server_and_model(self) -> None:
    """3.1.1: Base command includes llama-server and --model flags."""
    config = _make_collector(...).collect_config()
    builder = ProcessCommandBuilder(config)
    cmd = builder.build_command()
    
    assert "llama-server" in cmd  # ✓ Good - verifies output
    assert "--model" in cmd
    model_idx = cmd.index("--model")
    assert cmd[model_idx + 1] == "/models/llama.gguf"
```

This is **good** - it verifies the command structure.

**Bad example from `test_lifecycle.py`:**
```python
def test_6_8_calls_save_config_as_when_no_last_config_path(self, qapp):
    app = LlamaLaunchApp(...)
    app._save_config_as = MagicMock()  # ✗ Mocking implementation
    app._write_config_file = MagicMock()
    
    app._save_config()
    
    app._save_config_as.assert_called_once()  # ✗ Testing implementation detail
```

**Why bad:** If you refactor `_save_config` to inline `_save_config_as`, this test breaks even though behavior is identical.

**Better test:**
```python
def test_save_config_prompts_for_path_when_not_saved_before(self, qapp, tmp_path):
    """Saving without a previous path should prompt user for location."""
    app = LlamaLaunchApp(...)
    
    with patch('main.QFileDialog.getSaveFileName', return_value=(str(tmp_path / "config.json"), "")):
        app._save_config()
    
    # Verify the file was created (behavior, not implementation)
    assert (tmp_path / "config.json").exists()
    with open(tmp_path / "config.json") as f:
        config = json.load(f)
    assert config["version"] == "1.0"
```

### 9. **Overuse of Mocks**

**Issue:** `test_lifecycle.py` patches Qt core classes extensively:
```python
with patch("main.QSettings", return_value=mock_settings_instance):
    app = LlamaLaunchApp(...)
    app.model_path_edit = MagicMock()
    app.host_line_edit = MagicMock()
```

**Problem:** These tests don't verify the real Qt behavior. If Qt changes, tests still pass.

**Recommendation:** Use real Qt widgets where possible:
```python
def test_save_last_session_saves_settings(qapp, tmp_path):
    # Use real QSettings with a test-specific organization/app name
    QCoreApplication.setOrganizationName("LLamaLauncherTest")
    QCoreApplication.setApplicationName("TestApp")
    
    app = LlamaLaunchApp(...)
    app.model_path_edit.setProperty("fullPath", "/test/model.gguf")
    app._save_last_session()
    
    # Verify settings were written
    settings = QSettings("LLamaLauncherTest", "TestApp")
    assert settings.value("lastModelPath") == "/test/model.gguf"
```

### 10. **Tests Don't Cover Integration Paths**

**Missing:** No tests that exercise the full flow:
1. User selects a model file
2. Configures parameters
3. Clicks Launch
4. Process starts
5. stdout/stderr appear in UI
6. Server URL is detected
7. Web view refreshes

**Recommendation:** Add integration tests:
```python
@pytest.mark.integration
def test_full_launch_workflow(qapp, tmp_path):
    """End-to-end test: select model, configure, launch, verify UI updates."""
    app = LlamaLaunchApp()
    
    # Simulate user actions
    test_model = tmp_path / "test.gguf"
    test_model.touch()
    app.model_path_edit.setProperty("fullPath", str(test_model))
    app.model_path_edit.setText("test.gguf")
    
    # Mock QProcess to simulate llama-server output
    with patch.object(app._process, 'start') as mock_start:
        with patch.object(app._process, 'state', return_value=QProcess.Running):
            app._launch_model()
    
    # Verify command was built correctly
    call_args = mock_start.call_args
    assert call_args[0][0] == "llama-server"
    assert "--model" in call_args[0][1]
    
    # Verify UI updates
    assert app.launch_button.text() == "STOP"
    assert "Launching:" in app.output_display.toPlainText()
```

### 11. **Weak Assertions in Edge Case Tests**

**Example from `test_edge_cases.py`:**
```python
def test_7_1_appends_error_when_no_model_selected(self, launch_app):
    launch_app.model_path_edit.setProperty("fullPath", "")
    launch_app._launch_model()
    
    output = launch_app.output_display.toPlainText()
    assert "Error" in output or "no model" in output.lower()  # ✗ Too weak
```

**Problem:** This passes if the output is "Some unrelated error occurred" or "Know your model".

**Better:**
```python
def test_launch_model_shows_specific_error_when_no_model_selected(self, launch_app):
    launch_app.model_path_edit.setProperty("fullPath", "")
    launch_app._launch_model()
    
    output = launch_app.output_display.toPlainText()
    assert output == "Error: no model selected."  # ✓ Exact match
```

### 12. **Test Naming Could Be More Descriptive**

**Current:**
```python
def test_3_6_1_sets_server_url(self) -> None:
    """3.6.1: Sets _server_url after building command."""
```

**Better:**
```python
def test_launch_model_updates_server_url_from_host_and_port(self):
    """_launch_model should set _server_url to http://{host}:{port}."""
```

The test name should describe the **expected behavior**, not just the test number.

### 13. **Missing Failure Case Tests**

**Examples of missing tests:**
- What happens if `llama-server` is not in PATH?
- What if the process crashes immediately after launch?
- What if the model file is corrupted?
- What if the port is already in use?
- What if QSettings fails to write?

**Recommendation:** Add failure scenario tests:
```python
def test_launch_model_shows_error_when_llama_server_not_found(qapp):
    app = LlamaLaunchApp()
    app.model_path_edit.setProperty("fullPath", "/test.gguf")
    
    # Simulate QProcess.FailedToStart
    with patch.object(app._process, 'start', side_effect=QProcess.errorOccurred.emit(QProcess.ProcessError.FailedToStart)):
        app._launch_model()
    
    output = app.output_display.toPlainText()
    assert "llama-server not found" in output.lower()
```

---

## Python Quality Issues

### 14. **Inconsistent Error Handling**

**Issue:** Some methods show QMessageBox, others append to `output_display`, others do nothing:
```python
# _write_config_file: Uses QMessageBox
except Exception as e:
    QMessageBox.critical(self, "Save Error", f"Failed to save configuration:\n{e}")

# _launch_model: Uses output_display
if not model_path:
    self.output_display.appendPlainText("Error: no model selected.")
    return

# _on_error: Uses output_display
def _on_error(self, error: QProcess.ProcessError) -> None:
    msg = f"Error launching process: {error}"
    self.output_display.appendPlainText(msg)
```

**Recommendation:** Use consistent error handling:
```python
class ErrorHandler:
    """Centralized error reporting."""
    
    def show_user_error(self, title: str, message: str) -> None:
        """Show blocking error dialog."""
        QMessageBox.critical(self.parent, title, message)
    
    def log_error(self, message: str) -> None:
        """Append error to output log."""
        self.output_display.appendPlainText(f"ERROR: {message}")
```

### 15. **Missing Docstrings for Complex Logic**

**Issue:** `_setup_context_size_combo()` is 34 lines but lacks a comprehensive docstring explaining the data structure:
```python
def _setup_context_size_combo(self) -> None:
    """Populate the model context size combobox with options and tooltips.
    
    Each item stores its numeric value (used as ``--ctx-size``) in the
    user data role so the launch method can retrieve it later.
    """
```

**Better:**
```python
def _setup_context_size_combo(self) -> None:
    """Populate context size combobox with predefined options.
    
    Each item has three components:
    - Display text (e.g., "16K")
    - Numeric value (e.g., 16384) stored in Qt.UserRole
    - Tooltip describing use case
    
    The value 0 ("Auto") means let the model use its default context size.
    Values are passed to llama-server as --ctx-size unless 0.
    """
```

### 16. **Repetitive Parameter Collection Code**

**Issue:** Lines 882-912 in `_launch_model()` read ~12 spinbox values:
```python
temperature = self.temperature_spinbox.value()
top_p = self.top_p_spinbox.value()
top_k = self.top_k_spinbox.value()
min_p = self.min_p_spinbox.value()
# ... 8 more identical lines
```

**Recommendation:** Use a data-driven approach:
```python
SAMPLING_PARAMS = [
    ("temperature", "temperature_spinbox", "enable_temperature_checkbox", "--temp"),
    ("top_p", "top_p_spinbox", "enable_top_p_checkbox", "--top-p"),
    # ...
]

for name, spinbox_attr, checkbox_attr, flag in SAMPLING_PARAMS:
    if getattr(self, checkbox_attr).isChecked():
        value = getattr(self, spinbox_attr).value()
        cmd.extend([flag, str(value)])
```

---

## Improvements

### 17. **Add Logging**

**Issue:** No logging framework. Debugging requires inserting print statements.

**Recommendation:**
```python
import logging

logger = logging.getLogger(__name__)

class LlamaLaunchApp(QMainWindow):
    def _launch_model(self) -> None:
        logger.info("Launching model: %s", model_path)
        logger.debug("Command: %s", ' '.join(cmd))
        try:
            self._process.start(cmd[0], cmd[1:])
        except Exception as e:
            logger.exception("Failed to start process")
            raise
```

### 18. **Extract Magic Values to Constants**

**Issue:** Scattered throughout:
```python
if int(ctx_size) > 0:  # What does 0 mean?
QTimer.singleShot(2000, self._force_kill_if_needed)  # Why 2000ms?
```

**Recommendation:**
```python
CONTEXT_SIZE_AUTO = 0  # Use model default
PROCESS_TERMINATION_GRACE_PERIOD_MS = 2000
HTTP_CACHE_SIZE_MB = 100

if int(ctx_size) > CONTEXT_SIZE_AUTO:
    cmd.extend(["--ctx-size", str(ctx_size)])
    
QTimer.singleShot(PROCESS_TERMINATION_GRACE_PERIOD_MS, self._force_kill_if_needed)
```

### 19. **Add Validation Layer**

**Issue:** No validation that collected config is valid before building command.

**Recommendation:**
```python
class ConfigValidator:
    def validate(self, config: dict) -> list[str]:
        """Return list of validation errors."""
        errors = []
        
        if not config["files"]["model_path"]:
            errors.append("Model path is required")
        
        if not Path(config["files"]["model_path"]).exists():
            errors.append(f"Model file not found: {config['files']['model_path']}")
        
        if not (1024 <= config["server"]["port"] <= 65535):
            errors.append(f"Invalid port: {config['server']['port']}")
        
        return errors
```

### 20. **Use Pathlib Consistently**

**Issue:** Mix of string paths and Path objects:
```python
ui_path = Path(__file__).resolve().parent / "ui" / "llama_launch.ui"  # ✓
cache_dir = Path(...) / ".cache" / "llama-launcher"  # ✓

file_path.rsplit("/", 1)[-1]  # ✗ String manipulation
```

**Recommendation:**
```python
Path(file_path).name  # Instead of rsplit
```

---

## Good Practices Found

### ✓ Excellent Test Organization
The test suite is well-structured with clear phases (config, process, lifecycle, edge cases) and numbered test cases matching a testing plan.

### ✓ Good Use of Dataclasses
`ConfigCollector` uses `@dataclass(slots=True)` for memory efficiency.

### ✓ Process Command Builder Extraction
Separating command building into `ProcessCommandBuilder` is great for testability.

### ✓ Comprehensive Edge Case Testing
`test_edge_cases.py` covers many failure scenarios.

### ✓ Use of Qt Best Practices
- Proper QProcess parent management
- Signal/slot connections
- QSettings for persistence
- QWebEngineProfile for persistent storage

### ✓ Clear Method Naming
Most methods use descriptive names like `_create_cache_dir`, `_save_last_session`, `_on_stdout`.

### ✓ Good Documentation
Docstrings follow Google style and explain parameters, returns, and purpose.

---

## Priority Recommendations

**High Priority:**
1. Refactor `LlamaLaunchApp` into smaller focused classes
2. Use `ConfigCollector` and `ProcessCommandBuilder` in production code (not just tests)
3. Add Protocol types to `ConfigCollector` instead of `Any`
4. Write integration tests covering full workflows
5. Fix tests that verify implementation details instead of behavior

**Medium Priority:**
6. Add consistent error handling strategy
7. Add logging framework
8. Extract magic values to named constants
9. Add config validation layer
10. Add failure scenario tests (process not found, port in use, etc.)

**Low Priority:**
11. Use pathlib consistently
12. Improve test naming (drop numeric prefixes in production)
13. Add type hints to all method signatures
14. Reduce repetitive parameter collection code

---

**Overall:** This is a solid project with good test coverage. The main issues are architectural (God class, tight coupling) and test quality (mocking implementation, missing integration tests). Addressing the high-priority recommendations would significantly improve maintainability.

---

