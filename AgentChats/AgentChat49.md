## User

[@tdd](zed:///agent/skill?name=tdd&source=global&path=%2FUsers%2Fjmacey%2F.agents%2Fskills%2Ftdd%2FSKILL.md) [@pytest-best-practices](zed:///agent/skill?name=pytest-best-practices&source=LLamaLauncher&path=%2FVolumes%2Fteaching%2FCode%2FLLamaLauncher%2F.agents%2Fskills%2Fpytest-best-practices%2FSKILL.md) uv run pytest
============================== test session starts ===============================
platform darwin -- Python 3.14.0, pytest-9.1.0, pluggy-1.6.0
PySide6 6.11.1 -- Qt runtime 6.11.1 -- Qt compiled 6.11.1
rootdir: /Volumes/teaching/Code/LLamaLauncher
configfile: pyproject.toml
testpaths: tests
plugins: cov-7.1.0, qt-4.5.0
collected 165 items

tests/test_config.py ..................                                    [ 10%]
tests/test_file_selection.py ..................                            [ 21%]
tests/test_helper_methods.py ............                                  [ 29%]
tests/test_lifecycle.py ...............F                                   [ 38%]
tests/test_main.py .............................                           [ 56%]
tests/test_process.py .........................................            [ 81%]
tests/test_signals.py .....................                                [ 93%]
tests/test_ui_loader.py ..........                                         [100%]

==================================== FAILURES ====================================
___________ TestConnectSignals.test_6_15_signals_trigger_correct_slots ___________

self = <tests.test_lifecycle.TestConnectSignals object at 0x10be811d0>
qapp = <PySide6.QtWidgets.QApplication(0x600001302ad0) at 0x10cbdfb40>

    def test_6_15_signals_trigger_correct_slots(self, qapp):
        """Triggered signals call the correct slot methods.

        When a widget signal is emitted (e.g., button clicked), the connected
        slot method should be invoked.
        """
        from main import LlamaLaunchApp

        # Create a mock app with mock widgets and mock slots
        app = MagicMock(spec=LlamaLaunchApp)

        # Set up ALL mock widgets (required by _connect_signals)
        app.select_model_button = MagicMock()
        app.select_mmproj_button = MagicMock()
        app.select_draft_model_button = MagicMock()
        app.select_json_schema_button = MagicMock()
        app.model_path_edit = MagicMock()
        app.launch_button = MagicMock()

        # Set up mock slot methods
        app._select_model = MagicMock()
        app._select_mmproj = MagicMock()
        app._select_draft_model = MagicMock()
        app._select_json_schema = MagicMock()
        app._on_model_selection_changed = MagicMock()
        app._toggle_launch = MagicMock()

        # Connect signals to slots
        LlamaLaunchApp._connect_signals(app)

        # Emit specific signals
        app.select_model_button.clicked.emit()
        app.launch_button.clicked.emit()

        # Verify only the triggered slots were called
>       app._select_model.assert_called_once()

tests/test_lifecycle.py:479:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <MagicMock name='mock._select_model' id='5038367344'>

    def assert_called_once(self):
        """assert that the mock was called only once.
        """
        if not self.call_count == 1:
            msg = ("Expected '%s' to have been called once. Called %s times.%s"
                   % (self._mock_name or 'mock',
                      self.call_count,
                      self._calls_repr()))
>           raise AssertionError(msg)
E           AssertionError: Expected '_select_model' to have been called once. Called 0 times.

/Users/jmacey/.local/share/uv/python/cpython-3.14.0-macos-aarch64-none/lib/python3.14/unittest/mock.py:964: AssertionError
============================ short test summary info =============================
FAILED tests/test_lifecycle.py::TestConnectSignals::test_6_15_signals_trigger_correct_slots - AssertionError: Expected '_select_model' to have been called once. Called 0 t...
========================= 1 failed, 164 passed in 2.00s ==========================
llamalauncher➜  LLamaLauncher git:(main) ✗

## Assistant

<thinking>
The user has a failing test in `tests/test_lifecycle.py::TestConnectSignals::test_6_15_signals_trigger_correct_slots`. Let me analyze the failure:

The test is trying to verify that when signals are emitted (like `app.select_model_button.clicked.emit()`), the connected slot methods (like `app._select_model`) are called. But the mock's `_select_model` was never called.

This suggests that the `_connect_signals` method in `main.py` isn't connecting the signals the way the test expects, OR the way signals are emitted on the mocks doesn't actually trigger the connections.

The issue is likely that when you use `MagicMock()` for widgets, the `clicked` signal is a MagicMock itself, and connecting it to a slot and then emitting it should work. But the test might be failing because:


- The connection setup in `_connect_signals` isn't properly wiring up the mock signals to the slots, or
- The signal emission on the mocks isn't actually triggering the connected callbacks

I need to examine the actual implementation of `_connect_signals` and how the test is structured to see where the disconnect is happening.

</thinking>

Let me understand the failing test and the code it's testing.



**Tool Call: Read file `tests/test_lifecycle.py` (lines 450-520)**
Status: Completed

```LLamaLauncher/tests/test_lifecycle.py
   450	        from main import LlamaLaunchApp
   451	
   452	        # Create a mock app with mock widgets and mock slots
   453	        app = MagicMock(spec=LlamaLaunchApp)
   454	
   455	        # Set up ALL mock widgets (required by _connect_signals)
   456	        app.select_model_button = MagicMock()
   457	        app.select_mmproj_button = MagicMock()
   458	        app.select_draft_model_button = MagicMock()
   459	        app.select_json_schema_button = MagicMock()
   460	        app.model_path_edit = MagicMock()
   461	        app.launch_button = MagicMock()
   462	
   463	        # Set up mock slot methods
   464	        app._select_model = MagicMock()
   465	        app._select_mmproj = MagicMock()
   466	        app._select_draft_model = MagicMock()
   467	        app._select_json_schema = MagicMock()
   468	        app._on_model_selection_changed = MagicMock()
   469	        app._toggle_launch = MagicMock()
   470	
   471	        # Connect signals to slots
   472	        LlamaLaunchApp._connect_signals(app)
   473	
   474	        # Emit specific signals
   475	        app.select_model_button.clicked.emit()
   476	        app.launch_button.clicked.emit()
   477	
   478	        # Verify only the triggered slots were called
   479	        app._select_model.assert_called_once()
   480	        app._toggle_launch.assert_called_once()
   481	        # Other slots should not have been called
   482	        app._select_mmproj.assert_not_called()
   483	        app._select_draft_model.assert_not_called()
   484	        app._select_json_schema.assert_not_called()
   485	        app._on_model_selection_changed.assert_not_called()

```


**Tool Call: Search files for regex `def _connect_signals`**
Status: Completed

Found 8 matches:

## Matches in LLamaLauncher/.worktrees/file-selection-tests/main.py

### class LlamaLaunchApp › def _connect_signals › L747-751
```
    # ------------------------------------------------------------------

    def _connect_signals(self) -> None:
        """Connect widget signals to their slot methods."""
        self.select_model_button.clicked.connect(self._select_model)
```

## Matches in LLamaLauncher/.worktrees/phase6-lifecycle/main.py

### class LlamaLaunchApp › def _connect_signals › L747-751
```
    # ------------------------------------------------------------------

    def _connect_signals(self) -> None:
        """Connect widget signals to their slot methods."""
        self.select_model_button.clicked.connect(self._select_model)
```

## Matches in LLamaLauncher/.worktrees/process-command-builder/main.py

### class LlamaLaunchApp › def _connect_signals › L747-751
```
    # ------------------------------------------------------------------

    def _connect_signals(self) -> None:
        """Connect widget signals to their slot methods."""
        self.select_model_button.clicked.connect(self._select_model)
```

## Matches in LLamaLauncher/.worktrees/test-launch-model-cmd/main.py

### class LlamaLaunchApp › def _connect_signals › L526-530
```
    # ------------------------------------------------------------------

    def _connect_signals(self) -> None:
        """Connect widget signals to their slot methods."""
        self.select_model_button.clicked.connect(self._select_model)
```

## Matches in LLamaLauncher/.worktrees/test-launch-model-params/main.py

### class LlamaLaunchApp › def _connect_signals › L747-751
```
    # ------------------------------------------------------------------

    def _connect_signals(self) -> None:
        """Connect widget signals to their slot methods."""
        self.select_model_button.clicked.connect(self._select_model)
```

## Matches in LLamaLauncher/.worktrees/test-process-launch-side-effects/main.py

### class LlamaLaunchApp › def _connect_signals › L747-751
```
    # ------------------------------------------------------------------

    def _connect_signals(self) -> None:
        """Connect widget signals to their slot methods."""
        self.select_model_button.clicked.connect(self._select_model)
```

## Matches in LLamaLauncher/.worktrees/test-signals-ui-logic/main.py

### class LlamaLaunchApp › def _connect_signals › L747-751
```
    # ------------------------------------------------------------------

    def _connect_signals(self) -> None:
        """Connect widget signals to their slot methods."""
        self.select_model_button.clicked.connect(self._select_model)
```

## Matches in LLamaLauncher/main.py

### class LlamaLaunchApp › def _connect_signals › L747-751
```
    # ------------------------------------------------------------------

    def _connect_signals(self) -> None:
        """Connect widget signals to their slot methods."""
        self.select_model_button.clicked.connect(self._select_model)
```


## Assistant

<thinking>
The test is failing because the `_connect_signals` method in `main.py` connects signals to slots using `self`, but the test passes a `MagicMock` as `app`. The issue is that when `_connect_signals` calls `self.select_model_button.clicked.connect(self._select_model)`, it's calling `connect` on the mock's `clicked` attribute with `self._select_model` (the mock slot).

But the problem is that `_connect_signals` is an instance method that uses `self`, and the test passes a `MagicMock(spec=LlamaLaunchApp)` as the `app`. When you call `LlamaLaunchApp._connect_signals(app)`, it's calling the unbound method with `app` as `self`.

The real issue: when you do `MagicMock()`, the `.clicked` attribute is also a MagicMock. When you call `.clicked.connect(slot)`, it records the call but doesn't actually store or invoke the slot later. The `emit()` call on the same MagicMock also just returns another MagicMock - it doesn't trigger the connected slot.

This is a known problem with mocking Qt signals. The test approach of using plain MagicMock for widgets won't work because:
1. `clicked.connect(slot)` on a MagicMock doesn't actually connect anything
2. `clicked.emit()` on a MagicMock doesn't trigger connected callbacks

The proper way to test this would be either:
1. Use real Qt widgets (which the `qapp` fixture provides)
2. Use a mock that properly simulates signal/slot behavior

Let me read more of the `_connect_signals` method to understand all the connections being made.

Actually, looking at this more carefully - the test is using `MagicMock(spec=LlamaLaunchApp)` and then setting attributes on it. The problem is that when you call `app.select_model_button.clicked.connect(app._select_model)`, the MagicMock for `clicked` doesn't actually store the callback. And when you call `app.select_model_button.clicked.emit()`, it just emits on the mock signal which has no knowledge of connected slots.

The TDD and pytest best practices skills say:
- "Mock only external boundaries" - Qt widgets are internal to the UI, not external boundaries
- "Avoid mocking your own code because it tests the mock rather than the behavior"

So the test approach itself is flawed. The proper way would be to either:
1. Use real Qt widgets and verify behavior through side effects
2. Test at a higher level - verify that clicking a button triggers the expected end-to-end behavior

Let me look at the full `_connect_signals` method to understand what needs to be tested.

Actually, let me re-read the test failure more carefully. The user wants me to fix this failing test. Let me understand what the correct approach is.

The test is testing signal-slot connections using mocks. This is a legitimate concern - we want to verify that signals are connected to the right slots. But the implementation using MagicMock doesn't work because MagicMock doesn't simulate Qt's signal/slot mechanism.

Options:
1. Use a simple helper class that simulates signal/slot behavior
2. Use real Qt widgets (which the qapp fixture provides) and test through actual widget interactions
3. Refactor `_connect_signals` to be more testable (e.g., extract connection logic into a separate method that can be tested)

Given the TDD philosophy ("tests should verify behavior through public interfaces, not implementation details"), testing exact signal-slot connections is somewhat implementation-focused. A better approach would be to:
- Use real widgets in the test
- Click the actual button
- Verify the slot was called (by checking side effects or using a real signal)

Let me look at how other tests in this file handle similar situations, and look at the full `_connect_signals` method.

</thinking>

Let me read the full `_connect_signals` method and understand the test context better.



**Tool Call: Read file `main.py` (lines 745-800)**
Status: Completed

```LLamaLauncher/main.py
   745	    # ------------------------------------------------------------------
   746	    # Signal connections
   747	    # ------------------------------------------------------------------
   748	
   749	    def _connect_signals(self) -> None:
   750	        """Connect widget signals to their slot methods."""
   751	        self.select_model_button.clicked.connect(self._select_model)
   752	        self.select_mmproj_button.clicked.connect(self._select_mmproj)
   753	        self.select_draft_model_button.clicked.connect(self._select_draft_model)
   754	        self.select_json_schema_button.clicked.connect(self._select_json_schema)
   755	        self.model_path_edit.textChanged.connect(self._on_model_selection_changed)
   756	        self.launch_button.clicked.connect(self._toggle_launch)
   757	
   758	    # ------------------------------------------------------------------
   759	    # Slots
   760	    # ------------------------------------------------------------------
   761	
   762	    def _select_model(self) -> None:
   763	        """Open a file dialog to select a .gguf model file.
   764	
   765	        Stores the full path as a custom property on the line edit
   766	        (accessible via ``getProperty("fullPath")``) while displaying
   767	        only the short filename in the UI.
   768	        """
   769	        file_path, _ = QFileDialog.getOpenFileName(
   770	            self,
   771	            "Select GGUF Model",
   772	            "",
   773	            "GGUF Files (*.gguf)",
   774	        )
   775	        if file_path:
   776	            self._model_path = file_path
   777	            self.model_path_edit.setProperty("fullPath", file_path)
   778	            self.model_path_edit.setText(file_path.rsplit("/", 1)[-1])
   779	            self._on_model_selection_changed()
   780	
   781	    def _select_mmproj(self) -> None:
   782	        """Open a file dialog to select a .gguf mmproj file.
   783	
   784	        Stores the full path as a custom property on the line edit
   785	        (accessible via ``getProperty("fullPath")``) while displaying
   786	        only the short filename in the UI.
   787	        """
   788	        file_path, _ = QFileDialog.getOpenFileName(
   789	            self,
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

```


**Tool Call: Read file `tests/test_lifecycle.py` (lines 440-500)**
Status: Completed

```LLamaLauncher/tests/test_lifecycle.py
   440	        app.select_json_schema_button.clicked.connect.assert_called_once_with(app._select_json_schema)
   441	        app.model_path_edit.textChanged.connect.assert_called_once_with(app._on_model_selection_changed)
   442	        app.launch_button.clicked.connect.assert_called_once_with(app._toggle_launch)
   443	
   444	    def test_6_15_signals_trigger_correct_slots(self, qapp):
   445	        """Triggered signals call the correct slot methods.
   446	
   447	        When a widget signal is emitted (e.g., button clicked), the connected
   448	        slot method should be invoked.
   449	        """
   450	        from main import LlamaLaunchApp
   451	
   452	        # Create a mock app with mock widgets and mock slots
   453	        app = MagicMock(spec=LlamaLaunchApp)
   454	
   455	        # Set up ALL mock widgets (required by _connect_signals)
   456	        app.select_model_button = MagicMock()
   457	        app.select_mmproj_button = MagicMock()
   458	        app.select_draft_model_button = MagicMock()
   459	        app.select_json_schema_button = MagicMock()
   460	        app.model_path_edit = MagicMock()
   461	        app.launch_button = MagicMock()
   462	
   463	        # Set up mock slot methods
   464	        app._select_model = MagicMock()
   465	        app._select_mmproj = MagicMock()
   466	        app._select_draft_model = MagicMock()
   467	        app._select_json_schema = MagicMock()
   468	        app._on_model_selection_changed = MagicMock()
   469	        app._toggle_launch = MagicMock()
   470	
   471	        # Connect signals to slots
   472	        LlamaLaunchApp._connect_signals(app)
   473	
   474	        # Emit specific signals
   475	        app.select_model_button.clicked.emit()
   476	        app.launch_button.clicked.emit()
   477	
   478	        # Verify only the triggered slots were called
   479	        app._select_model.assert_called_once()
   480	        app._toggle_launch.assert_called_once()
   481	        # Other slots should not have been called
   482	        app._select_mmproj.assert_not_called()
   483	        app._select_draft_model.assert_not_called()
   484	        app._select_json_schema.assert_not_called()
   485	        app._on_model_selection_changed.assert_not_called()

```


## Assistant

<thinking>
Now I understand the issue clearly. The test `test_6_15_signals_trigger_correct_slots` is using `MagicMock` for widgets, but MagicMock doesn't implement Qt's signal/slot mechanism. When you call `clicked.connect(slot)` on a MagicMock, it doesn't actually store the callback. And when you call `clicked.emit()`, it doesn't invoke connected callbacks.

The previous test (which passes - `test_6_14_all_signals_connected_to_correct_slots`) verifies the connections by checking that `.connect.assert_called_once_with(...)` was called with the right arguments. That works because MagicMock records calls to its methods.


The real problem is that emitting signals on a mock doesn't actually trigger the connected callbacks, so the slots never get invoked. The user's guidelines emphasize testing behavior through public interfaces rather than implementation details, and these pytest best practices say to avoid mocking internal code since you end up testing the mock itself instead of actual behavior.

The right approach here is to either refactor `_connect_signals` to extract the connection logic into something testable, or use real Qt widgets with the `qapp` fixture so the signal-slot mechanism actually works as intended. I'm leaning toward a minimal refactoring that makes the connections verifiable without overcomplicating the design.

The core issue is that mocking Qt signals doesn't work—MagicMock can't simulate how signals and slots actually connect. The cleanest fix would be to test at a higher level by creating a real `LlamaLaunchApp` instance with actual widgets, clicking the button, and verifying the slot gets called through the real signal mechanism rather than trying to mock it away. I need to understand what the test fixture is setting up so I can work within its constraints. Let me examine the fixture structure and see how other tests in this file handle similar scenarios.

The core issue is that MagicMock doesn't properly implement Qt's signal/slot mechanism, so the signal connections never actually fire. I could fix this by either making the mock simulate Qt signals correctly or by using real Qt widgets instead. The cleanest approach might be to create a simple helper class that mimics how Qt signals work, then use that in place of the MagicMock for testing the connection behavior. I'm considering three approaches: replacing the mock with real Qt widgets, creating a custom signal simulator class, or refactoring the code to separate connection logic from the signal definitions themselves. Option C feels like it might be overcomplicating things, so I'm leaning toward either the real widget approach or building a lightweight signal simulation that tracks connections and emits callbacks when signals fire. The simplest fix is to create a helper class that mimics Qt's signal/slot mechanism by storing connected callbacks and invoking them when emit() is called. This way the test can verify that clicking a button actually triggers the correct slot without needing the full Qt framework, though it does sacrifice some of the behavioral testing benefits the user mentioned earlier.

Now I need to decide between using real Qt widgets versus this simpler simulation approach. Real widgets would be more thorough but require significantly more setup, while the signal simulator is minimal and focused on just testing the connection logic.

I'll go with the signal simulator since it keeps the test focused and lightweight. The implementation is straightforward—I'm creating a simple class that stores callbacks when connected and fires them all when emitted. I should also check if there are other tests using the same pattern that might need the same fix.

</thinking>

Now I understand the issue. The test uses `MagicMock` for Qt widgets, but `MagicMock` doesn't implement Qt's signal/slot mechanism. When you call `clicked.connect(slot)` on a MagicMock, it records the call (which is why the previous test checking `.connect.assert_called_once_with()` passes). But when you call `clicked.emit()`, MagicMock just returns another MagicMock — it doesn't invoke the connected callbacks.

Let me check how other tests in this file are structured to understand the patterns used.



**Tool Call: Read file `tests/test_lifecycle.py` (lines 1-50)**
Status: Completed

```LLamaLauncher/tests/test_lifecycle.py
     1	"""Phase 6: Tests for initialization and lifecycle methods."""
     2	
     3	import sys
     4	import tempfile
     5	from pathlib import Path
     6	from unittest.mock import MagicMock, patch
     7	
     8	import pytest
     9	
    10	# Import production modules from project root in tests
    11	_project_root = str(Path(__file__).resolve().parent.parent)
    12	if _project_root not in sys.path:
    13	    sys.path.insert(0, _project_root)
    14	
    15	
    16	@pytest.fixture()
    17	def temp_dir():
    18	    """Provide temporary cleaned up directory.
    19	
    20	    Returns a Path to a temporary directory that removes itself afterward.
    21	    """
    22	    with tempfile.TemporaryDirectory() as tmpdir:
    23	        yield Path(tmpdir)
    24	
    25	
    26	class TestCreateCacheDir:
    27	    """Test _create_cache_dir creates cache directory and returns Path."""
    28	
    29	    def test_6_1_creates_cache_directory_and_returns_path(self, qapp):
    30	        """_create_cache_dir creates the cache directory on disk and returns it as a Path.
    31	
    32	        The returned path should exist and be a valid directory.
    33	        """
    34	        from main import LlamaLaunchApp
    35	
    36	        app = LlamaLaunchApp(host="127.0.0.1", port=8080)
    37	
    38	        assert isinstance(app._cache_dir, Path)
    39	        assert app._cache_dir.exists()
    40	        assert app._cache_dir.is_dir()
    41	        assert "llama-launcher" in str(app._cache_dir)
    42	
    43	
    44	class TestSaveConfig:
    45	    """Test _save_config behavior."""
    46	
    47	    def test_6_8_calls_save_config_as_when_no_last_config_path(self, qapp):
    48	        """_save_config calls _save_config_as when _last_config_path does not exist.
    49	
    50	        When there is no previously saved config path, save should prompt

```


**Tool Call: Search files for regex `class.*Fixture|def.*fixture`**
Status: Completed

No matches found

## Assistant

<thinking>
Now I see the `qapp` fixture is used across tests. Let me look at the conftest.py to understand the qapp fixture, and also look at the full test class to understand the pattern better.

</thinking>

**Tool Call: Search files for regex `def qapp|@pytest\.fixture.*qapp`**
Status: Completed

Found 1 matches:

## Matches in LLamaLauncher/tests/conftest.py

### def qapp › L17-27
```
def qapp():
    """Provide a QApplication singleton for the test session.

    This fixture ensures only one QApplication instance is created
    across all Qt tests in the session.
    """
    from PySide6.QtWidgets import QApplication

    app = QApplication.instance()
    if app is None:
        app = QApplication([])
```

2 lines remaining in ancestor node. Read the file to see all.


**Tool Call: Read file `tests/test_lifecycle.py` (lines 420-490)**
Status: Completed

```LLamaLauncher/tests/test_lifecycle.py
   420	        app.select_draft_model_button = MagicMock()
   421	        app.select_json_schema_button = MagicMock()
   422	        app.model_path_edit = MagicMock()
   423	        app.launch_button = MagicMock()
   424	
   425	        # Set up mock slot methods
   426	        app._select_model = MagicMock()
   427	        app._select_mmproj = MagicMock()
   428	        app._select_draft_model = MagicMock()
   429	        app._select_json_schema = MagicMock()
   430	        app._on_model_selection_changed = MagicMock()
   431	        app._toggle_launch = MagicMock()
   432	
   433	        # Call _connect_signals (bound to the mock instance)
   434	        LlamaLaunchApp._connect_signals(app)
   435	
   436	        # Verify each signal was connected to its slot
   437	        app.select_model_button.clicked.connect.assert_called_once_with(app._select_model)
   438	        app.select_mmproj_button.clicked.connect.assert_called_once_with(app._select_mmproj)
   439	        app.select_draft_model_button.clicked.connect.assert_called_once_with(app._select_draft_model)
   440	        app.select_json_schema_button.clicked.connect.assert_called_once_with(app._select_json_schema)
   441	        app.model_path_edit.textChanged.connect.assert_called_once_with(app._on_model_selection_changed)
   442	        app.launch_button.clicked.connect.assert_called_once_with(app._toggle_launch)
   443	
   444	    def test_6_15_signals_trigger_correct_slots(self, qapp):
   445	        """Triggered signals call the correct slot methods.
   446	
   447	        When a widget signal is emitted (e.g., button clicked), the connected
   448	        slot method should be invoked.
   449	        """
   450	        from main import LlamaLaunchApp
   451	
   452	        # Create a mock app with mock widgets and mock slots
   453	        app = MagicMock(spec=LlamaLaunchApp)
   454	
   455	        # Set up ALL mock widgets (required by _connect_signals)
   456	        app.select_model_button = MagicMock()
   457	        app.select_mmproj_button = MagicMock()
   458	        app.select_draft_model_button = MagicMock()
   459	        app.select_json_schema_button = MagicMock()
   460	        app.model_path_edit = MagicMock()
   461	        app.launch_button = MagicMock()
   462	
   463	        # Set up mock slot methods
   464	        app._select_model = MagicMock()
   465	        app._select_mmproj = MagicMock()
   466	        app._select_draft_model = MagicMock()
   467	        app._select_json_schema = MagicMock()
   468	        app._on_model_selection_changed = MagicMock()
   469	        app._toggle_launch = MagicMock()
   470	
   471	        # Connect signals to slots
   472	        LlamaLaunchApp._connect_signals(app)
   473	
   474	        # Emit specific signals
   475	        app.select_model_button.clicked.emit()
   476	        app.launch_button.clicked.emit()
   477	
   478	        # Verify only the triggered slots were called
   479	        app._select_model.assert_called_once()
   480	        app._toggle_launch.assert_called_once()
   481	        # Other slots should not have been called
   482	        app._select_mmproj.assert_not_called()
   483	        app._select_draft_model.assert_not_called()
   484	        app._select_json_schema.assert_not_called()
   485	        app._on_model_selection_changed.assert_not_called()

```


## Assistant

<thinking>
Now I have a clear picture. The issue is that `MagicMock` doesn't implement Qt's signal/slot mechanism. When you call `clicked.connect(slot)` on a MagicMock, it records the call (which is why `test_6_14` passes - it checks `.connect.assert_called_once_with()`). But when you call `clicked.emit()`, MagicMock just returns another MagicMock - it doesn't invoke connected callbacks.

The fix is to replace the plain `MagicMock()` for widget signals with a simple class that simulates Qt's signal/slot mechanism. This way:


- `.connect(slot)` stores the callback
- `.emit()` invokes all stored callbacks

This is minimal and focused on fixing just this test.

</thinking>

Now I understand the problem clearly. The test uses `MagicMock` for widget signals, but `MagicMock` doesn't implement Qt's signal/slot mechanism:

- `clicked.connect(slot)` on a MagicMock records the call (so `test_6_14` passes by checking `.connect.assert_called_once_with()`)
- `clicked.emit()` on a MagicMock just returns another MagicMock — it **doesn't invoke** connected callbacks

The fix is to replace plain `MagicMock` widgets with a lightweight class that simulates Qt's signal/slot behavior: `.connect()` stores callbacks, and `.emit()` invokes them.



**Tool Call: Read file `tests/test_lifecycle.py` (lines 400-443)**
Status: Completed

```LLamaLauncher/tests/test_lifecycle.py
   400	        assert int(combo.itemData(combo.currentIndex(), Qt.UserRole)) == 16384
   401	
   402	
   403	class TestConnectSignals:
   404	    """Test _connect_signals wires up widget signals to slot methods."""
   405	
   406	    def test_6_15_wires_up_all_button_clicks_and_signals(self, qapp):
   407	        """_connect_signals connects all widget signals to their slot methods.
   408	
   409	        Each button's clicked signal and the model path edit's textChanged signal
   410	        should be connected to their respective handler methods.
   411	        """
   412	        from main import LlamaLaunchApp
   413	
   414	        # Create a mock app with mock widgets and mock slots
   415	        app = MagicMock(spec=LlamaLaunchApp)
   416	
   417	        # Set up mock widgets with MagicMock signals
   418	        app.select_model_button = MagicMock()
   419	        app.select_mmproj_button = MagicMock()
   420	        app.select_draft_model_button = MagicMock()
   421	        app.select_json_schema_button = MagicMock()
   422	        app.model_path_edit = MagicMock()
   423	        app.launch_button = MagicMock()
   424	
   425	        # Set up mock slot methods
   426	        app._select_model = MagicMock()
   427	        app._select_mmproj = MagicMock()
   428	        app._select_draft_model = MagicMock()
   429	        app._select_json_schema = MagicMock()
   430	        app._on_model_selection_changed = MagicMock()
   431	        app._toggle_launch = MagicMock()
   432	
   433	        # Call _connect_signals (bound to the mock instance)
   434	        LlamaLaunchApp._connect_signals(app)
   435	
   436	        # Verify each signal was connected to its slot
   437	        app.select_model_button.clicked.connect.assert_called_once_with(app._select_model)
   438	        app.select_mmproj_button.clicked.connect.assert_called_once_with(app._select_mmproj)
   439	        app.select_draft_model_button.clicked.connect.assert_called_once_with(app._select_draft_model)
   440	        app.select_json_schema_button.clicked.connect.assert_called_once_with(app._select_json_schema)
   441	        app.model_path_edit.textChanged.connect.assert_called_once_with(app._on_model_selection_changed)
   442	        app.launch_button.clicked.connect.assert_called_once_with(app._toggle_launch)
   443	

```


## Assistant

<thinking>
Now I have the full picture. The test `test_6_15_signals_trigger_correct_slots` uses `MagicMock` for widget signals, but `MagicMock` doesn't implement Qt's signal/slot mechanism. When you call `.emit()` on a MagicMock, it doesn't invoke connected callbacks.

The fix is to replace the plain `MagicMock` widgets with a lightweight class that simulates Qt's signal/slot behavior:
- `.connect(slot)` stores the callback in a list
- `.emit()` invokes all stored callbacks
- Still supports `.connect.assert_called_once_with(...)` for backward compatibility with test_6_14

Wait, actually I need to be more careful. The `test_6_14` (actually `test_6_15_wires_up_all_button_clicks_and_signals`) checks `app.select_model_button.clicked.connect.assert_called_once_with(...)`. This works because `clicked` is a MagicMock, and `clicked.connect` is also a MagicMock that records calls.

For `test_6_15_signals_trigger_correct_slots`, the issue is that `clicked.emit()` doesn't actually call the connected slot. With real Qt, when you do:
```python
self.select_model_button.clicked.connect(self._select_model)
```
The signal stores a reference to the slot. When you emit the signal, it calls all connected slots.

With MagicMock:
```python
app.select_model_button = MagicMock()  # clicked is also MagicMock
app.select_model_button.clicked.connect(app._select_model)  # records the call, but doesn't store for later
app.select_model_button.clicked.emit()  # just returns another MagicMock, doesn't call app._select_model
```

The fix: Create a simple `QtSignal` class that simulates this behavior. The `.connect()` method should both record the call (so test_6_14 still works) AND store the callback for later emission.

But there's a subtlety: test_6_14 checks `app.select_model_button.clicked.connect.assert_called_once_with(app._select_model)`. This means `clicked.connect` must be a MagicMock (or at least have the `assert_called_once_with` method).

So I need a class where:
- The instance has a `.connect` attribute that is a MagicMock (for test_6_14 compatibility)
- The instance also has an `.emit()` method that calls all stored callbacks

One approach: Create a class that wraps both a MagicMock (for `.connect`) and a callback list (for `.emit`).

```python
class QtSignal:
    """Simulates Qt signal behavior for testing."""
    
    def __init__(self):
        self._connect_mock = MagicMock()
        self._callbacks = []
    
    def connect(self, callback):
        self._connect_mock.connect.assert_called_once_with  # No wait...
```

Hmm, let me think about this differently. The test_6_14 checks:
```python
app.select_model_button.clicked.connect.assert_called_once_with(app._select_model)
```

So `clicked.connect` needs to be a mock that records calls. But we also need `clicked.emit()` to invoke the connected callbacks.

I can create a class where:
- `.connect` is itself a MagicMock
- `.emit()` calls all stored callbacks

```python
class QtSignal:
    """Simulates Qt signal behavior for testing."""
    
    def __init__(self):
        self.connect = MagicMock()
        self._callbacks = []
    
    def emit(self, *args, **kwargs):
        for callback in self._callbacks:
            callback(*args, **kwargs)
```

Wait, but the `_connect_signals` method does:
```python
self.select_model_button.clicked.connect(self._select_model)
```

So `clicked.connect(slot)` is called. With my QtSignal class, this would call `MagicMock.__call__` (since `self.connect` is a MagicMock). The MagicMock would record this call, so `clicked.connect.assert_called_once_with(app._select_model)` would work.

But I also need to store the callback for later emission. I can do this by making `connect` a real method that also calls the mock:

```python
class QtSignal:
    """Simulates Qt signal behavior for testing."""
    
    def __init__(self):
        self._callbacks = []
    
    def connect(self, callback):
        self._callbacks.append(callback)
    
    def emit(self, *args, **kwargs):
        for callback in self._callbacks:
            callback(*args, **kwargs)
```

But then `clicked.connect` is a regular method, not a MagicMock. The test_6_14 check `app.select_model_button.clicked.connect.assert_called_once_with(...)` would fail because regular methods don't have `assert_called_once_with`.

So I need both: a MagicMock for `.connect` AND callback storage for `.emit()`.

One approach is to make `connect` a property that returns a MagicMock, but also stores the callback. But that's tricky because the `connect` method call happens at connection time, not at assertion time.

Let me think about this differently. I can use a wrapper:

```python
class QtSignal:
    """Simulates Qt signal behavior for testing."""
    
    def __init__(self):
        self._callbacks = []
        self._connect_calls = []  # Store connect calls for verification
    
    def connect(self, callback):
        """Connect a slot to this signal."""
        self._callbacks.append(callback)
        self._connect_calls.append(callback)
    
    def emit(self, *args, **kwargs):
        """Emit the signal, calling all connected slots."""
        for callback in self._callbacks:
            callback(*args, **kwargs)
    
    @property
    def connect_mock(self):
        """Return a mock that records connect calls (for test compatibility)."""
        mock = MagicMock()
        for cb in self._connect_calls:
            mock.assert_called_once_with  # No, this doesn't work...
```

Hmm, this is getting complicated. Let me think of another approach.

Actually, the simplest approach is to just fix test_6_15 to use real Qt widgets instead of mocks. The `qapp` fixture provides a QApplication. I can create real QPushButton and QLineEdit instances, connect them, and emit signals. This would be more aligned with the TDD philosophy of testing behavior through public interfaces.

But that would require changing the test significantly and might be more fragile. Let me think about what's minimal and correct.

Actually, looking at this from a different angle: the test_6_14 and test_6_15 are both in `TestConnectSignals` class. They're testing the same method `_connect_signals` from different angles:
- test_6_14: "verify that connect was called with the right arguments" (implementation detail check)
- test_6_15: "verify that emitting signals actually calls the slots" (behavioral check)

The problem is that test_6_15's approach (using MagicMock) can't work because MagicMock doesn't simulate Qt signals.

Options:
1. Replace MagicMock with a QtSignal class that simulates signal/slot behavior AND supports assertion on connect calls
2. Use real Qt widgets for test_6_15
3. Remove test_6_15 since test_6_14 already verifies the connections (and real Qt will handle the rest at runtime)

Given the TDD philosophy ("tests should verify behavior through public interfaces, not implementation details"), option 3 might be valid. But test_6_15 is testing a different concern - that the signals actually trigger the slots, which is a behavioral test.

Let me go with option 1: Create a QtSignal class that properly simulates Qt signals while still supporting the assertion pattern used in test_6_14.

Here's my approach:

```python
class _QtSignal:
    """Minimal simulation of a Qt signal for testing.
    
    Supports both connection verification (via recorded calls) and
    signal emission to verify that connected slots are invoked.
    """
    
    def __init__(self):
        self._callbacks = []
        self._connect_args: list = []
    
    def connect(self, callback):
        """Connect a slot callback."""
        self._callbacks.append(callback)
        self._connect_args.append(callback)
    
    def emit(self, *args, **kwargs):
        """Emit the signal, invoking all connected slots."""
        for callback in self._callbacks:
            callback(*args, **kwargs)
    
    def assert_called_once_with(self, expected_callback):
        """Assert that connect was called exactly once with the given callback."""
        assert len(self._connect_args) == 1, f"Expected 1 connect call, got {len(self._connect_args)}"
        assert self._connect_args[0] == expected_callback, \
            f"Expected connect to {expected_callback}, got {self._connect_args[0]}"
```

Wait, but test_6_14 uses `app.select_model_button.clicked.connect.assert_called_once_with(app._select_model)`. The `clicked` attribute needs to have a `.connect` that supports this pattern.

If I make `clicked` be a `_QtSignal` instance, then `clicked.connect` is the `_QtSignal.connect` method. Calling `clicked.connect(callback)` would store the callback and append to `_connect_args`. Then calling `clicked.connect.assert_called_once_with(callback)` wouldn't work because `.connect` is a method, not a mock with `assert_called_once_with`.

I need to restructure. Let me make it so that:
- `signal.connect(...)` stores the callback AND records it for assertion
- `signal.connect` (the attribute itself) has an `assert_called_once_with` method

This is tricky because `.connect` needs to be both callable (to receive callbacks) and have assertion methods.

One way: make `.connect` a mock that also has side effects:

```python
class _QtSignal:
    """Minimal simulation of a Qt signal for testing."""
    
    def __init__(self):
        self._callbacks = []
        self.connect = MagicMock()
        self.connect.side_effect = self._record_connect
    
    def _record_connect(self, callback):
        self._callbacks.append(callback)
        return callback
    
    def emit(self, *args, **kwargs):
        for callback in self._callbacks:
            callback(*args, **kwargs)
```

Now:
- `signal.connect(callback)` calls `MagicMock.__call__` which records the call AND triggers `side_effect`, calling `_record_connect` which stores the callback
- `signal.connect.assert_called_once_with(callback)` works because `self.connect` is a MagicMock
- `signal.emit()` invokes all stored callbacks

This should work for both test_6_14 and test_6_15!

Let me verify:
- test_6_14 does: `app.select_model_button.clicked.connect.assert_called_once_with(app._select_model)`
  - `clicked` is `_QtSignal`, so `clicked.connect` is a MagicMock
  - When `_connect_signals` calls `clicked.connect(slot)`, the MagicMock records the call and triggers side_effect
  - The assertion checks that connect was called once with the right argument ✓

- test_6_15 does: `app.select_model_button.clicked.emit()` then `app._select_model.assert_called_once()`
  - `clicked` is `_QtSignal`, so `clicked.emit()` calls all stored callbacks
  - The stored callback is `app._select_model` (which is a MagicMock)
  - So `app._select_model` gets called ✓

This approach works. Let me implement it.

I'll add the `_QtSignal` class at the top of the test file (near the imports) and replace `MagicMock()` widget signal attributes with `_QtSignal()`.

Wait, I need to be careful about what exactly needs to be replaced. Looking at the code:

For test_6_14:
```python
app.select_model_button = MagicMock()  # This creates a MagicMock where .clicked is also MagicMock
```

The `MagicMock()` creates a mock where any attribute access returns another MagicMock. So `app.select_model_button.clicked` is a MagicMock, and `app.select_model_button.clicked.connect` is also a MagicMock.

For test_6_15:
Same setup, but we need `.clicked.emit()` to actually call connected callbacks.

So I need to replace the widget mocks so that their `.clicked`, `.textChanged` etc. attributes are `_QtSignal` instances instead of plain MagicMock.

Let me update both tests to use a helper that creates widgets with QtSignal-based signals.

Actually, for minimal change, I should:
1. Add the `_QtSignal` class to the test file
2. In test_6_15, replace `MagicMock()` widgets with a custom class that has `_QtSignal` for signal attributes

Let me write this out:

```python
class _QtSignal:
    """Minimal simulation of a Qt signal for testing.
    
    Supports both connection verification (via recorded calls) and
    signal emission to verify that connected slots are invoked.
    """
    
    def __init__(self):
        self._callbacks = []
        self.connect = MagicMock()
        self.connect.side_effect = self._record_connect
    
    def _record_connect(self, callback):
        self._callbacks.append(callback)
        return callback
    
    def emit(self, *args, **kwargs):
        """Emit the signal, invoking all connected slots."""
        for callback in self._callbacks:
            callback(*args, **kwargs)


class _MockWidget:
    """Minimal mock widget with QtSignal-based signals."""
    
    def __init__(self):
        self.clicked = _QtSignal()
        self.textChanged = _QtSignal()
```

Then in test_6_15, replace:
```python
app.select_model_button = MagicMock()
```
with:
```python
app.select_model_button = _MockWidget()
```

And similarly for other widgets. For `model_path_edit`, it uses `textChanged` signal, so the `_MockWidget` handles that too.

Wait, let me check if any widget uses `textChanged`:
- `self.model_path_edit.textChanged.connect(self._on_model_selection_changed)` - yes!

So I need to make sure `_MockWidget` has both `clicked` and `textChanged` as `_QtSignal` instances.

Let me finalize the implementation:

```python
class _QtSignal:
    """Minimal simulation of a Qt signal for testing.
    
    Supports both connection verification (via recorded calls) and
    signal emission to verify that connected slots are invoked.
    """
    
    def __init__(self):
        self._callbacks = []
        self.connect = MagicMock()
        self.connect.side_effect = self._record_connect
    
    def _record_connect(self, callback):
        self._callbacks.append(callback)
        return callback
    
    def emit(self, *args, **kwargs):
        """Emit the signal, invoking all connected slots."""
        for callback in self._callbacks:
            callback(*args, **kwargs)


class _MockWidget:
    """Minimal mock widget with QtSignal-based signals."""
    
    def __init__(self):
        self.clicked = _QtSignal()
        self.textChanged = _QtSignal()
```

And in test_6_15, replace all `MagicMock()` for widgets with `_MockWidget()`.

This is a clean, minimal fix that:
1. Fixes the failing test
2. Maintains compatibility with test_6_14 (which checks `.connect.assert_called_once_with()`)
3. Properly simulates Qt signal/slot behavior

Let me implement this now.

</thinking>

Now I have full context. The problem is clear: `MagicMock` doesn't implement Qt's signal/slot mechanism. When you call `.emit()` on a MagicMock, it just returns another MagicMock — it never invokes connected callbacks.

The fix is to create a minimal class that simulates Qt signals: `.connect()` stores the callback (and records it for assertion), and `.emit()` invokes all stored callbacks.



**Tool Call: tests/test\_lifecycle.py**
Status: Completed

Diff: tests/test_lifecycle.py
```
"""Phase 6: Tests for initialization and lifecycle methods."""

import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Import production modules from project root in tests
_project_root = str(Path(__file__).resolve().parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)


class _QtSignal:
    """Minimal simulation of a Qt signal for testing.

    Supports both connection verification (via recorded calls) and
    signal emission to verify that connected slots are invoked.
    """

    def __init__(self):
        self._callbacks = []
        self.connect = MagicMock()
        self.connect.side_effect = self._record_connect

    def _record_connect(self, callback):
        self._callbacks.append(callback)
        return callback

    def emit(self, *args, **kwargs):
        """Emit the signal, invoking all connected slots."""
        for callback in self._callbacks:
            callback(*args, **kwargs)


class _MockWidget:
    """Minimal mock widget with QtSignal-based signals."""

    def __init__(self):
        self.clicked = _QtSignal()
        self.textChanged = _QtSignal()


@pytest.fixture()
def temp_dir():
    """Provide temporary cleaned up directory.

    Returns a Path to a temporary directory that removes itself afterward.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


class TestCreateCacheDir:
    """Test _create_cache_dir creates cache directory and returns Path."""

    def test_6_1_creates_cache_directory_and_returns_path(self, qapp):
        """_create_cache_dir creates the cache directory on disk and returns it as a Path.

        The returned path should exist and be a valid directory.
        """
        from main import LlamaLaunchApp

        app = LlamaLaunchApp(host="127.0.0.1", port=8080)

        assert isinstance(app._cache_dir, Path)
        assert app._cache_dir.exists()
        assert app._cache_dir.is_dir()
        assert "llama-launcher" in str(app._cache_dir)


class TestSaveConfig:
    """Test _save_config behavior."""

    def test_6_8_calls_save_config_as_when_no_last_config_path(self, qapp):
        """_save_config calls _save_config_as when _last_config_path does not exist.

        When there is no previously saved config path, save should prompt
        the user for a location via _save_config_as.
        """
        from main import LlamaLaunchApp

        app = LlamaLaunchApp(host="127.0.0.1", port=8080)
        app._save_config_as = MagicMock()
        app._write_config_file = MagicMock()

        assert not hasattr(app, "_last_config_path")
        app._save_config()

        app._save_config_as.assert_called_once()
        app._write_config_file.assert_not_called()

    def test_6_9_writes_to_last_saved_path_when_exists(self, qapp):
        """_save_config writes to _last_config_path when it exists.

        When a previous config path is available, save should write directly
        to that path without prompting.
        """
        from main import LlamaLaunchApp

        app = LlamaLaunchApp(host="127.0.0.1", port=8080)
        app._last_config_path = Path("/tmp/test-config.json")
        app._save_config_as = MagicMock()
        app._write_config_file = MagicMock()

        app._save_config()

        app._write_config_file.assert_called_once_with(app._last_config_path)
        app._save_config_as.assert_not_called()


class TestSaveLastSession:
    """Test _save_last_session saves settings to QSettings."""

    def test_6_11_saves_model_path_host_port_and_geometry(self, qapp):
        """_save_last_session saves model path, host, port, and window geometry.

        All four values should be written to QSettings with the correct keys.
        """
        from main import LlamaLaunchApp

        # Mock QSettings: configure value() for _load_last_session (called in __init__)
        # and capture setValue() calls from _save_last_session
        mock_settings_instance = MagicMock()
        mock_settings_instance.value.return_value = None  # no saved geometry

        with patch("main.QSettings", return_value=mock_settings_instance):
            app = LlamaLaunchApp(host="127.0.0.1", port=8080)

            # Configure widget mocks with expected values
            app.model_path_edit = MagicMock()
            app.model_path_edit.property.return_value = "/models/test.gguf"
            app.host_line_edit = MagicMock()
            app.host_line_edit.text.return_value = "192.168.1.100"
            app.port_line_edit = MagicMock()
            app.port_line_edit.text.return_value = "9000"
            app.saveGeometry = MagicMock(return_value=b"geometry-data")

            app._save_last_session()

            # Verify all four values were saved
            calls = mock_settings_instance.setValue.call_args_list
            assert len(calls) == 4

            call_keys = {call[0][0] for call in calls}
            assert "lastModelPath" in call_keys
            assert "host" in call_keys
            assert "port" in call_keys
            assert "windowGeometry" in call_keys

            # Verify specific values
            mock_settings_instance.setValue.assert_any_call("lastModelPath", "/models/test.gguf")
            mock_settings_instance.setValue.assert_any_call("host", "192.168.1.100")
            mock_settings_instance.setValue.assert_any_call("port", "9000")
            mock_settings_instance.setValue.assert_any_call("windowGeometry", b"geometry-data")

    def test_6_11_saves_empty_model_path_when_none(self, qapp):
        """_save_last_session saves empty string when model path is None.

        If the model path property returns None, an empty string should be saved.
        """
        from main import LlamaLaunchApp

        mock_settings_instance = MagicMock()
        mock_settings_instance.value.return_value = None  # no saved geometry
        with patch("main.QSettings", return_value=mock_settings_instance):
            app = LlamaLaunchApp(host="127.0.0.1", port=8080)

            app.model_path_edit = MagicMock()
            app.model_path_edit.property.return_value = None
            app.host_line_edit = MagicMock()
            app.host_line_edit.text.return_value = "127.0.0.1"
            app.port_line_edit = MagicMock()
            app.port_line_edit.text.return_value = "8080"
            app.saveGeometry = MagicMock(return_value=b"")

            app._save_last_session()

            mock_settings_instance.setValue.assert_any_call("lastModelPath", "")


class TestCloseEvent:
    """Test closeEvent lifecycle behavior."""

    def test_6_14_calls_save_last_session_before_closing(self, qapp):
        """closeEvent calls _save_last_session before delegating to parent.

        The session must be saved before the window closes so settings
        are persisted on disk.
        """
        from PySide6.QtGui import QCloseEvent

        from main import LlamaLaunchApp

        app = LlamaLaunchApp(host="127.0.0.1", port=8080)
        app._save_last_session = MagicMock()

        close_event = QCloseEvent()
        app.closeEvent(close_event)

        app._save_last_session.assert_called_once()
        # super().closeEvent() accepts the event by default
        assert close_event.isAccepted()


class TestCreateFileMenu:
    """Test _create_file_menu creates File menu with correct actions."""

    def test_6_7_creates_file_menu_with_save_save_as_load_actions(self, qapp):
        """_create_file_menu creates a File menu with Save, Save As, and Load actions.

        The File menu should be added to the menu bar and contain three actions
        that are connected to their respective slot methods.
        """
        from main import LlamaLaunchApp

        app = LlamaLaunchApp(host="127.0.0.1", port=8080)

        # Verify the File menu exists in the menu bar
        # QMenuBar.actions() returns QActions that represent menus
        file_menu = None
        for action in app.menuBar().actions():
            menu = action.menu()
            if menu is not None and "File" in menu.title():
                file_menu = menu
                break

        assert file_menu is not None, "File menu should exist in menu bar"

        # Verify the menu has three actions
        actions = file_menu.actions()
        assert len(actions) == 3

        action_texts = [action.text() for action in actions]
        assert any("Save Configuration" in text for text in action_texts)
        assert any("Save As" in text for text in action_texts)
        assert any("Load Configuration" in text for text in action_texts)

    def test_6_7_save_action_connected_to_save_config(self, qapp):
        """The Save action is connected to _save_config method."""
        from main import LlamaLaunchApp

        app = LlamaLaunchApp(host="127.0.0.1", port=8080)
        app._save_config = MagicMock()

        # Find and trigger the Save action in File menu
        for action in app.menuBar().actions():
            menu = action.menu()
            if menu is not None and "File" in menu.title():
                for submenu_action in menu.actions():
                    if "Save Configuration" in submenu_action.text():
                        submenu_action.trigger()
                        break
                break

        app._save_config.assert_called_once()

    def test_6_7_load_action_connected_to_load_config(self, qapp):
        """The Load action is connected to _load_config method."""
        from main import LlamaLaunchApp

        app = LlamaLaunchApp(host="127.0.0.1", port=8080)
        app._load_config = MagicMock()

        # Find and trigger the Load action in File menu
        for action in app.menuBar().actions():
            menu = action.menu()
            if menu is not None and "File" in menu.title():
                for submenu_action in menu.actions():
                    if "Load Configuration" in submenu_action.text():
                        submenu_action.trigger()
                        break
                break

        app._load_config.assert_called_once()


class TestLoadLastSession:
    """Test _load_last_session restores settings from QSettings."""

    def test_6_12_restores_host_port_and_model_path(self, qapp):
        """_load_last_session restores host, port, and model path from QSettings.

        When values are saved in QSettings, they should be restored to the
        corresponding UI widgets on application startup.
        """
        from main import LlamaLaunchApp

        # Mock QSettings to return saved values
        mock_settings_instance = MagicMock()
        mock_settings_instance.value.side_effect = lambda key, default="": {
            "windowGeometry": None,
            "host": "192.168.1.50",
            "port": "9999",
            "lastModelPath": "/models/previously-used.gguf",
        }.get(key, default)

        with patch("main.QSettings", return_value=mock_settings_instance):
            app = LlamaLaunchApp(host="127.0.0.1", port=8080)

            # Replace widgets with mocks to verify setText calls
            app.host_line_edit = MagicMock()
            app.port_line_edit = MagicMock()
            app.model_path_edit = MagicMock()
            app._set_path_field = MagicMock()

            # Re-run _load_last_session with the mocked widgets
            app._load_last_session()

            # Verify host and port were set
            app.host_line_edit.setText.assert_called_with("192.168.1.50")
            app.port_line_edit.setText.assert_called_with("9999")

            # Verify model path was restored via _set_path_field
            app._set_path_field.assert_called_once_with(app.model_path_edit, "/models/previously-used.gguf")

    def test_6_12_uses_defaults_when_no_saved_values(self, qapp):
        """_load_last_session uses default values when nothing is saved.

        When QSettings has no saved values, the method should use the
        hardcoded defaults (host=127.0.0.1, port=8080).
        """
        from main import LlamaLaunchApp

        # Mock QSettings to return None for keys with no saved data,
        # but respect default parameters for host/port lookups
        mock_settings_instance = MagicMock()

        def mock_value(key, default=""):
            # No saved data, so always return the default
            return default

        mock_settings_instance.value.side_effect = mock_value

        with patch("main.QSettings", return_value=mock_settings_instance):
            app = LlamaLaunchApp(host="127.0.0.1", port=8080)

            # Replace widgets with mocks to verify setText calls
            app.host_line_edit = MagicMock()
            app.port_line_edit = MagicMock()
            app.model_path_edit = MagicMock()
            app._set_path_field = MagicMock()

            app._load_last_session()

            # Verify defaults were used
            app.host_line_edit.setText.assert_called_with("127.0.0.1")
            app.port_line_edit.setText.assert_called_with("8080")

            # Model path should not be set when empty
            app._set_path_field.assert_not_called()


class TestSetupContextSizeCombo:
    """Test _setup_context_size_combo populates combobox with options."""

    def test_6_4_populates_all_8_context_size_options(self, qapp):
        """_setup_context_size_combo populates the combobox with 8 context size options.

        Each option should have a display name, numeric value in user data role,
        and a tooltip.
        """
        from PySide6.QtCore import Qt

        from main import LlamaLaunchApp

        app = LlamaLaunchApp(host="127.0.0.1", port=8080)

        # Verify 8 options were added
        combo = app.model_context_size
        assert combo.count() == 8

        # Verify expected display names and values
        expected_options = [
            ("Auto (model default)", 0),
            ("2K", 2048),
            ("4K", 4096),
            ("8K", 8192),
            ("16K", 16384),
            ("32K", 32768),
            ("64K", 65536),
            ("128K", 131072),
        ]

        for i, (display_name, value) in enumerate(expected_options):
            assert combo.itemText(i) == display_name
            assert int(combo.itemData(i, Qt.UserRole)) == value

        # Verify tooltips are set
        for i in range(combo.count()):
            tooltip = combo.itemData(i, Qt.ToolTipRole)
            assert tooltip is not None
            assert len(str(tooltip)) > 0

    def test_6_5_pre_selects_from_cli_ctx_size(self, qapp):
        """_setup_context_size_combo pre-selects the option matching CLI ctx_size.

        When _ctx_size is provided during initialization, the combobox should
        select the matching option.
        """
        from PySide6.QtCore import Qt

        from main import LlamaLaunchApp

        # Create app with ctx_size=8192 (8K option)
        app = LlamaLaunchApp(host="127.0.0.1", port=8080, ctx_size=8192)

        combo = app.model_context_size
        # 8K is the 4th option (index 3)
        assert combo.currentIndex() == 3
        assert int(combo.itemData(combo.currentIndex(), Qt.UserRole)) == 8192

    def test_6_6_defaults_to_16k_when_no_ctx_size(self, qapp):
        """_setup_context_size_combo defaults to 16K when no CLI ctx_size provided.

        When _ctx_size is None, the combobox should default to 16K (16384).
        """
        from PySide6.QtCore import Qt

        from main import LlamaLaunchApp

        # Create app without ctx_size (defaults to None)
        app = LlamaLaunchApp(host="127.0.0.1", port=8080)

        combo = app.model_context_size
        # 16K is the 5th option (index 4)
        assert combo.currentIndex() == 4
        assert int(combo.itemData(combo.currentIndex(), Qt.UserRole)) == 16384


class TestConnectSignals:
    """Test _connect_signals wires up widget signals to slot methods."""

    def test_6_15_wires_up_all_button_clicks_and_signals(self, qapp):
        """_connect_signals connects all widget signals to their slot methods.

        Each button's clicked signal and the model path edit's textChanged signal
        should be connected to their respective handler methods.
        """
        from main import LlamaLaunchApp

        # Create a mock app with mock widgets and mock slots
        app = MagicMock(spec=LlamaLaunchApp)

        # Set up mock widgets with MagicMock signals
        app.select_model_button = MagicMock()
        app.select_mmproj_button = MagicMock()
        app.select_draft_model_button = MagicMock()
        app.select_json_schema_button = MagicMock()
        app.model_path_edit = MagicMock()
        app.launch_button = MagicMock()

        # Set up mock slot methods
        app._select_model = MagicMock()
        app._select_mmproj = MagicMock()
        app._select_draft_model = MagicMock()
        app._select_json_schema = MagicMock()
        app._on_model_selection_changed = MagicMock()
        app._toggle_launch = MagicMock()

        # Call _connect_signals (bound to the mock instance)
        LlamaLaunchApp._connect_signals(app)

        # Verify each signal was connected to its slot
        app.select_model_button.clicked.connect.assert_called_once_with(app._select_model)
        app.select_mmproj_button.clicked.connect.assert_called_once_with(app._select_mmproj)
        app.select_draft_model_button.clicked.connect.assert_called_once_with(app._select_draft_model)
        app.select_json_schema_button.clicked.connect.assert_called_once_with(app._select_json_schema)
        app.model_path_edit.textChanged.connect.assert_called_once_with(app._on_model_selection_changed)
        app.launch_button.clicked.connect.assert_called_once_with(app._toggle_launch)

    def test_6_15_signals_trigger_correct_slots(self, qapp):
        """Triggered signals call the correct slot methods.

        When a widget signal is emitted (e.g., button clicked), the connected
        slot method should be invoked.
        """
        from main import LlamaLaunchApp

        # Create a mock app with mock widgets and mock slots
        app = MagicMock(spec=LlamaLaunchApp)

        # Set up ALL mock widgets (required by _connect_signals)
        app.select_model_button = MagicMock()
        app.select_mmproj_button = MagicMock()
        app.select_draft_model_button = MagicMock()
        app.select_json_schema_button = MagicMock()
        app.model_path_edit = MagicMock()
        app.launch_button = MagicMock()

        # Set up mock slot methods
        app._select_model = MagicMock()
        app._select_mmproj = MagicMock()
        app._select_draft_model = MagicMock()
        app._select_json_schema = MagicMock()
        app._on_model_selection_changed = MagicMock()
        app._toggle_launch = MagicMock()

        # Connect signals to slots
        LlamaLaunchApp._connect_signals(app)

        # Emit specific signals
        app.select_model_button.clicked.emit()
        app.launch_button.clicked.emit()

        # Verify only the triggered slots were called
        app._select_model.assert_called_once()
        app._toggle_launch.assert_called_once()
        # Other slots should not have been called
        app._select_mmproj.assert_not_called()
        app._select_draft_model.assert_not_called()
        app._select_json_schema.assert_not_called()
        app._on_model_selection_changed.assert_not_called()

```


## Assistant

<thinking>
Now I need to update the test_6_15_signals_trigger_correct_slots test to use _MockWidget instead of MagicMock for the widget attributes. Let me read the current state of that test to see what needs to be changed.

</thinking>

Now I need to update the failing test to use `_MockWidget` instead of `MagicMock()` for the widget instances:



**Tool Call: Read file `tests/test_lifecycle.py` (lines 474-520)**
Status: Completed

```LLamaLauncher/tests/test_lifecycle.py
   474	    def test_6_15_signals_trigger_correct_slots(self, qapp):
   475	        """Triggered signals call the correct slot methods.
   476	
   477	        When a widget signal is emitted (e.g., button clicked), the connected
   478	        slot method should be invoked.
   479	        """
   480	        from main import LlamaLaunchApp
   481	
   482	        # Create a mock app with mock widgets and mock slots
   483	        app = MagicMock(spec=LlamaLaunchApp)
   484	
   485	        # Set up ALL mock widgets (required by _connect_signals)
   486	        app.select_model_button = MagicMock()
   487	        app.select_mmproj_button = MagicMock()
   488	        app.select_draft_model_button = MagicMock()
   489	        app.select_json_schema_button = MagicMock()
   490	        app.model_path_edit = MagicMock()
   491	        app.launch_button = MagicMock()
   492	
   493	        # Set up mock slot methods
   494	        app._select_model = MagicMock()
   495	        app._select_mmproj = MagicMock()
   496	        app._select_draft_model = MagicMock()
   497	        app._select_json_schema = MagicMock()
   498	        app._on_model_selection_changed = MagicMock()
   499	        app._toggle_launch = MagicMock()
   500	
   501	        # Connect signals to slots
   502	        LlamaLaunchApp._connect_signals(app)
   503	
   504	        # Emit specific signals
   505	        app.select_model_button.clicked.emit()
   506	        app.launch_button.clicked.emit()
   507	
   508	        # Verify only the triggered slots were called
   509	        app._select_model.assert_called_once()
   510	        app._toggle_launch.assert_called_once()
   511	        # Other slots should not have been called
   512	        app._select_mmproj.assert_not_called()
   513	        app._select_draft_model.assert_not_called()
   514	        app._select_json_schema.assert_not_called()
   515	        app._on_model_selection_changed.assert_not_called()

```


## Assistant

<thinking>
Now I need to update the test to use `_MockWidget` instead of `MagicMock()` for the widget instances. Let me make that change.

</thinking>

**Tool Call: tests/test\_lifecycle.py**
Status: Completed

Diff: tests/test_lifecycle.py
```
"""Phase 6: Tests for initialization and lifecycle methods."""

import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Import production modules from project root in tests
_project_root = str(Path(__file__).resolve().parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)


class _QtSignal:
    """Minimal simulation of a Qt signal for testing.

    Supports both connection verification (via recorded calls) and
    signal emission to verify that connected slots are invoked.
    """

    def __init__(self):
        self._callbacks = []
        self.connect = MagicMock()
        self.connect.side_effect = self._record_connect

    def _record_connect(self, callback):
        self._callbacks.append(callback)
        return callback

    def emit(self, *args, **kwargs):
        """Emit the signal, invoking all connected slots."""
        for callback in self._callbacks:
            callback(*args, **kwargs)


class _MockWidget:
    """Minimal mock widget with QtSignal-based signals."""

    def __init__(self):
        self.clicked = _QtSignal()
        self.textChanged = _QtSignal()


@pytest.fixture()
def temp_dir():
    """Provide temporary cleaned up directory.

    Returns a Path to a temporary directory that removes itself afterward.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


class TestCreateCacheDir:
    """Test _create_cache_dir creates cache directory and returns Path."""

    def test_6_1_creates_cache_directory_and_returns_path(self, qapp):
        """_create_cache_dir creates the cache directory on disk and returns it as a Path.

        The returned path should exist and be a valid directory.
        """
        from main import LlamaLaunchApp

        app = LlamaLaunchApp(host="127.0.0.1", port=8080)

        assert isinstance(app._cache_dir, Path)
        assert app._cache_dir.exists()
        assert app._cache_dir.is_dir()
        assert "llama-launcher" in str(app._cache_dir)


class TestSaveConfig:
    """Test _save_config behavior."""

    def test_6_8_calls_save_config_as_when_no_last_config_path(self, qapp):
        """_save_config calls _save_config_as when _last_config_path does not exist.

        When there is no previously saved config path, save should prompt
        the user for a location via _save_config_as.
        """
        from main import LlamaLaunchApp

        app = LlamaLaunchApp(host="127.0.0.1", port=8080)
        app._save_config_as = MagicMock()
        app._write_config_file = MagicMock()

        assert not hasattr(app, "_last_config_path")
        app._save_config()

        app._save_config_as.assert_called_once()
        app._write_config_file.assert_not_called()

    def test_6_9_writes_to_last_saved_path_when_exists(self, qapp):
        """_save_config writes to _last_config_path when it exists.

        When a previous config path is available, save should write directly
        to that path without prompting.
        """
        from main import LlamaLaunchApp

        app = LlamaLaunchApp(host="127.0.0.1", port=8080)
        app._last_config_path = Path("/tmp/test-config.json")
        app._save_config_as = MagicMock()
        app._write_config_file = MagicMock()

        app._save_config()

        app._write_config_file.assert_called_once_with(app._last_config_path)
        app._save_config_as.assert_not_called()


class TestSaveLastSession:
    """Test _save_last_session saves settings to QSettings."""

    def test_6_11_saves_model_path_host_port_and_geometry(self, qapp):
        """_save_last_session saves model path, host, port, and window geometry.

        All four values should be written to QSettings with the correct keys.
        """
        from main import LlamaLaunchApp

        # Mock QSettings: configure value() for _load_last_session (called in __init__)
        # and capture setValue() calls from _save_last_session
        mock_settings_instance = MagicMock()
        mock_settings_instance.value.return_value = None  # no saved geometry

        with patch("main.QSettings", return_value=mock_settings_instance):
            app = LlamaLaunchApp(host="127.0.0.1", port=8080)

            # Configure widget mocks with expected values
            app.model_path_edit = MagicMock()
            app.model_path_edit.property.return_value = "/models/test.gguf"
            app.host_line_edit = MagicMock()
            app.host_line_edit.text.return_value = "192.168.1.100"
            app.port_line_edit = MagicMock()
            app.port_line_edit.text.return_value = "9000"
            app.saveGeometry = MagicMock(return_value=b"geometry-data")

            app._save_last_session()

            # Verify all four values were saved
            calls = mock_settings_instance.setValue.call_args_list
            assert len(calls) == 4

            call_keys = {call[0][0] for call in calls}
            assert "lastModelPath" in call_keys
            assert "host" in call_keys
            assert "port" in call_keys
            assert "windowGeometry" in call_keys

            # Verify specific values
            mock_settings_instance.setValue.assert_any_call("lastModelPath", "/models/test.gguf")
            mock_settings_instance.setValue.assert_any_call("host", "192.168.1.100")
            mock_settings_instance.setValue.assert_any_call("port", "9000")
            mock_settings_instance.setValue.assert_any_call("windowGeometry", b"geometry-data")

    def test_6_11_saves_empty_model_path_when_none(self, qapp):
        """_save_last_session saves empty string when model path is None.

        If the model path property returns None, an empty string should be saved.
        """
        from main import LlamaLaunchApp

        mock_settings_instance = MagicMock()
        mock_settings_instance.value.return_value = None  # no saved geometry
        with patch("main.QSettings", return_value=mock_settings_instance):
            app = LlamaLaunchApp(host="127.0.0.1", port=8080)

            app.model_path_edit = MagicMock()
            app.model_path_edit.property.return_value = None
            app.host_line_edit = MagicMock()
            app.host_line_edit.text.return_value = "127.0.0.1"
            app.port_line_edit = MagicMock()
            app.port_line_edit.text.return_value = "8080"
            app.saveGeometry = MagicMock(return_value=b"")

            app._save_last_session()

            mock_settings_instance.setValue.assert_any_call("lastModelPath", "")


class TestCloseEvent:
    """Test closeEvent lifecycle behavior."""

    def test_6_14_calls_save_last_session_before_closing(self, qapp):
        """closeEvent calls _save_last_session before delegating to parent.

        The session must be saved before the window closes so settings
        are persisted on disk.
        """
        from PySide6.QtGui import QCloseEvent

        from main import LlamaLaunchApp

        app = LlamaLaunchApp(host="127.0.0.1", port=8080)
        app._save_last_session = MagicMock()

        close_event = QCloseEvent()
        app.closeEvent(close_event)

        app._save_last_session.assert_called_once()
        # super().closeEvent() accepts the event by default
        assert close_event.isAccepted()


class TestCreateFileMenu:
    """Test _create_file_menu creates File menu with correct actions."""

    def test_6_7_creates_file_menu_with_save_save_as_load_actions(self, qapp):
        """_create_file_menu creates a File menu with Save, Save As, and Load actions.

        The File menu should be added to the menu bar and contain three actions
        that are connected to their respective slot methods.
        """
        from main import LlamaLaunchApp

        app = LlamaLaunchApp(host="127.0.0.1", port=8080)

        # Verify the File menu exists in the menu bar
        # QMenuBar.actions() returns QActions that represent menus
        file_menu = None
        for action in app.menuBar().actions():
            menu = action.menu()
            if menu is not None and "File" in menu.title():
                file_menu = menu
                break

        assert file_menu is not None, "File menu should exist in menu bar"

        # Verify the menu has three actions
        actions = file_menu.actions()
        assert len(actions) == 3

        action_texts = [action.text() for action in actions]
        assert any("Save Configuration" in text for text in action_texts)
        assert any("Save As" in text for text in action_texts)
        assert any("Load Configuration" in text for text in action_texts)

    def test_6_7_save_action_connected_to_save_config(self, qapp):
        """The Save action is connected to _save_config method."""
        from main import LlamaLaunchApp

        app = LlamaLaunchApp(host="127.0.0.1", port=8080)
        app._save_config = MagicMock()

        # Find and trigger the Save action in File menu
        for action in app.menuBar().actions():
            menu = action.menu()
            if menu is not None and "File" in menu.title():
                for submenu_action in menu.actions():
                    if "Save Configuration" in submenu_action.text():
                        submenu_action.trigger()
                        break
                break

        app._save_config.assert_called_once()

    def test_6_7_load_action_connected_to_load_config(self, qapp):
        """The Load action is connected to _load_config method."""
        from main import LlamaLaunchApp

        app = LlamaLaunchApp(host="127.0.0.1", port=8080)
        app._load_config = MagicMock()

        # Find and trigger the Load action in File menu
        for action in app.menuBar().actions():
            menu = action.menu()
            if menu is not None and "File" in menu.title():
                for submenu_action in menu.actions():
                    if "Load Configuration" in submenu_action.text():
                        submenu_action.trigger()
                        break
                break

        app._load_config.assert_called_once()


class TestLoadLastSession:
    """Test _load_last_session restores settings from QSettings."""

    def test_6_12_restores_host_port_and_model_path(self, qapp):
        """_load_last_session restores host, port, and model path from QSettings.

        When values are saved in QSettings, they should be restored to the
        corresponding UI widgets on application startup.
        """
        from main import LlamaLaunchApp

        # Mock QSettings to return saved values
        mock_settings_instance = MagicMock()
        mock_settings_instance.value.side_effect = lambda key, default="": {
            "windowGeometry": None,
            "host": "192.168.1.50",
            "port": "9999",
            "lastModelPath": "/models/previously-used.gguf",
        }.get(key, default)

        with patch("main.QSettings", return_value=mock_settings_instance):
            app = LlamaLaunchApp(host="127.0.0.1", port=8080)

            # Replace widgets with mocks to verify setText calls
            app.host_line_edit = MagicMock()
            app.port_line_edit = MagicMock()
            app.model_path_edit = MagicMock()
            app._set_path_field = MagicMock()

            # Re-run _load_last_session with the mocked widgets
            app._load_last_session()

            # Verify host and port were set
            app.host_line_edit.setText.assert_called_with("192.168.1.50")
            app.port_line_edit.setText.assert_called_with("9999")

            # Verify model path was restored via _set_path_field
            app._set_path_field.assert_called_once_with(app.model_path_edit, "/models/previously-used.gguf")

    def test_6_12_uses_defaults_when_no_saved_values(self, qapp):
        """_load_last_session uses default values when nothing is saved.

        When QSettings has no saved values, the method should use the
        hardcoded defaults (host=127.0.0.1, port=8080).
        """
        from main import LlamaLaunchApp

        # Mock QSettings to return None for keys with no saved data,
        # but respect default parameters for host/port lookups
        mock_settings_instance = MagicMock()

        def mock_value(key, default=""):
            # No saved data, so always return the default
            return default

        mock_settings_instance.value.side_effect = mock_value

        with patch("main.QSettings", return_value=mock_settings_instance):
            app = LlamaLaunchApp(host="127.0.0.1", port=8080)

            # Replace widgets with mocks to verify setText calls
            app.host_line_edit = MagicMock()
            app.port_line_edit = MagicMock()
            app.model_path_edit = MagicMock()
            app._set_path_field = MagicMock()

            app._load_last_session()

            # Verify defaults were used
            app.host_line_edit.setText.assert_called_with("127.0.0.1")
            app.port_line_edit.setText.assert_called_with("8080")

            # Model path should not be set when empty
            app._set_path_field.assert_not_called()


class TestSetupContextSizeCombo:
    """Test _setup_context_size_combo populates combobox with options."""

    def test_6_4_populates_all_8_context_size_options(self, qapp):
        """_setup_context_size_combo populates the combobox with 8 context size options.

        Each option should have a display name, numeric value in user data role,
        and a tooltip.
        """
        from PySide6.QtCore import Qt

        from main import LlamaLaunchApp

        app = LlamaLaunchApp(host="127.0.0.1", port=8080)

        # Verify 8 options were added
        combo = app.model_context_size
        assert combo.count() == 8

        # Verify expected display names and values
        expected_options = [
            ("Auto (model default)", 0),
            ("2K", 2048),
            ("4K", 4096),
            ("8K", 8192),
            ("16K", 16384),
            ("32K", 32768),
            ("64K", 65536),
            ("128K", 131072),
        ]

        for i, (display_name, value) in enumerate(expected_options):
            assert combo.itemText(i) == display_name
            assert int(combo.itemData(i, Qt.UserRole)) == value

        # Verify tooltips are set
        for i in range(combo.count()):
            tooltip = combo.itemData(i, Qt.ToolTipRole)
            assert tooltip is not None
            assert len(str(tooltip)) > 0

    def test_6_5_pre_selects_from_cli_ctx_size(self, qapp):
        """_setup_context_size_combo pre-selects the option matching CLI ctx_size.

        When _ctx_size is provided during initialization, the combobox should
        select the matching option.
        """
        from PySide6.QtCore import Qt

        from main import LlamaLaunchApp

        # Create app with ctx_size=8192 (8K option)
        app = LlamaLaunchApp(host="127.0.0.1", port=8080, ctx_size=8192)

        combo = app.model_context_size
        # 8K is the 4th option (index 3)
        assert combo.currentIndex() == 3
        assert int(combo.itemData(combo.currentIndex(), Qt.UserRole)) == 8192

    def test_6_6_defaults_to_16k_when_no_ctx_size(self, qapp):
        """_setup_context_size_combo defaults to 16K when no CLI ctx_size provided.

        When _ctx_size is None, the combobox should default to 16K (16384).
        """
        from PySide6.QtCore import Qt

        from main import LlamaLaunchApp

        # Create app without ctx_size (defaults to None)
        app = LlamaLaunchApp(host="127.0.0.1", port=8080)

        combo = app.model_context_size
        # 16K is the 5th option (index 4)
        assert combo.currentIndex() == 4
        assert int(combo.itemData(combo.currentIndex(), Qt.UserRole)) == 16384


class TestConnectSignals:
    """Test _connect_signals wires up widget signals to slot methods."""

    def test_6_15_wires_up_all_button_clicks_and_signals(self, qapp):
        """_connect_signals connects all widget signals to their slot methods.

        Each button's clicked signal and the model path edit's textChanged signal
        should be connected to their respective handler methods.
        """
        from main import LlamaLaunchApp

        # Create a mock app with mock widgets and mock slots
        app = MagicMock(spec=LlamaLaunchApp)

        # Set up mock widgets with MagicMock signals
        app.select_model_button = MagicMock()
        app.select_mmproj_button = MagicMock()
        app.select_draft_model_button = MagicMock()
        app.select_json_schema_button = MagicMock()
        app.model_path_edit = MagicMock()
        app.launch_button = MagicMock()

        # Set up mock slot methods
        app._select_model = MagicMock()
        app._select_mmproj = MagicMock()
        app._select_draft_model = MagicMock()
        app._select_json_schema = MagicMock()
        app._on_model_selection_changed = MagicMock()
        app._toggle_launch = MagicMock()

        # Call _connect_signals (bound to the mock instance)
        LlamaLaunchApp._connect_signals(app)

        # Verify each signal was connected to its slot
        app.select_model_button.clicked.connect.assert_called_once_with(app._select_model)
        app.select_mmproj_button.clicked.connect.assert_called_once_with(app._select_mmproj)
        app.select_draft_model_button.clicked.connect.assert_called_once_with(app._select_draft_model)
        app.select_json_schema_button.clicked.connect.assert_called_once_with(app._select_json_schema)
        app.model_path_edit.textChanged.connect.assert_called_once_with(app._on_model_selection_changed)
        app.launch_button.clicked.connect.assert_called_once_with(app._toggle_launch)

    def test_6_15_signals_trigger_correct_slots(self, qapp):
        """Triggered signals call the correct slot methods.

        When a widget signal is emitted (e.g., button clicked), the connected
        slot method should be invoked.
        """
        from main import LlamaLaunchApp

        # Create a mock app with mock widgets and mock slots
        app = MagicMock(spec=LlamaLaunchApp)

        # Set up ALL mock widgets (required by _connect_signals)
        app.select_model_button = _MockWidget()
        app.select_mmproj_button = _MockWidget()
        app.select_draft_model_button = _MockWidget()
        app.select_json_schema_button = _MockWidget()
        app.model_path_edit = _MockWidget()
        app.launch_button = _MockWidget()

        # Set up mock slot methods
        app._select_model = MagicMock()
        app._select_mmproj = MagicMock()
        app._select_draft_model = MagicMock()
        app._select_json_schema = MagicMock()
        app._on_model_selection_changed = MagicMock()
        app._toggle_launch = MagicMock()

        # Connect signals to slots
        LlamaLaunchApp._connect_signals(app)

        # Emit specific signals
        app.select_model_button.clicked.emit()
        app.launch_button.clicked.emit()

        # Verify only the triggered slots were called
        app._select_model.assert_called_once()
        app._toggle_launch.assert_called_once()
        # Other slots should not have been called
        app._select_mmproj.assert_not_called()
        app._select_draft_model.assert_not_called()
        app._select_json_schema.assert_not_called()
        app._on_model_selection_changed.assert_not_called()

```


## Assistant

<thinking>
Now let me run the tests to verify the fix works. I need to run pytest to see if the failing test now passes, and also make sure the other test (test_6_14) still passes since it also uses the same signal connection pattern.

</thinking>

Now let me run the tests to verify the fix:



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher && uv run pytest tests/test_lifecycle.py -v**
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
collected 16 items

tests/test_lifecycle.py::TestCreateCacheDir::test_6_1_creates_cache_directory_and_returns_path PASSED [  6%]
tests/test_lifecycle.py::TestSaveConfig::test_6_8_calls_save_config_as_when_no_last_config_path PASSED [ 12%]
tests/test_lifecycle.py::TestSaveConfig::test_6_9_writes_to_last_saved_path_when_exists PASSED [ 18%]
tests/test_lifecycle.py::TestSaveLastSession::test_6_11_saves_model_path_host_port_and_geometry PASSED [ 25%]
tests/test_lifecycle.py::TestSaveLastSession::test_6_11_saves_empty_model_path_when_none PASSED [ 31%]
tests/test_lifecycle.py::TestCloseEvent::test_6_14_calls_save_last_session_before_closing PASSED [ 37%]
tests/test_lifecycle.py::TestCreateFileMenu::test_6_7_creates_file_menu_with_save_save_as_load_actions PASSED [ 43%]
tests/test_lifecycle.py::TestCreateFileMenu::test_6_7_save_action_connected_to_save_config PASSED [ 50%]
tests/test_lifecycle.py::TestCreateFileMenu::test_6_7_load_action_connected_to_load_config PASSED [ 56%]
tests/test_lifecycle.py::TestLoadLastSession::test_6_12_restores_host_port_and_model_path PASSED [ 62%]
tests/test_lifecycle.py::TestLoadLastSession::test_6_12_uses_defaults_when_no_saved_values PASSED [ 68%]
tests/test_lifecycle.py::TestSetupContextSizeCombo::test_6_4_populates_all_8_context_size_options PASSED [ 75%]
tests/test_lifecycle.py::TestSetupContextSizeCombo::test_6_5_pre_selects_from_cli_ctx_size PASSED [ 81%]
tests/test_lifecycle.py::TestSetupContextSizeCombo::test_6_6_defaults_to_16k_when_no_ctx_size PASSED [ 87%]
tests/test_lifecycle.py::TestConnectSignals::test_6_15_wires_up_all_button_clicks_and_signals PASSED [ 93%]
tests/test_lifecycle.py::TestConnectSignals::test_6_15_signals_trigger_correct_slots PASSED [100%]

================== 16 passed in 1.89s ==================

```


## Assistant

<thinking>
The output is truncated. Let me see the full results, especially for the TestConnectSignals tests.

</thinking>

Output was truncated — let me see the rest:



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher && uv run pytest tests/test_lifecycle.py -v 2>&1 | tail -40**
Status: Completed

Terminal:
```
============================= test session starts ==============================
platform darwin -- Python 3.14.0, pytest-9.1.0, pluggy-1.6.0 -- /Volumes/teaching/Code/LLamaLauncher/.venv/bin/python3
cachedir: .pytest_cache
PySide6 6.11.1 -- Qt runtime 6.11.1 -- Qt compiled 6.11.1
rootdir: /Volumes/teaching/Code/LLamaLauncher
configfile: pyproject.toml
plugins: cov-7.1.0, qt-4.5.0
collecting ... collected 16 items

tests/test_lifecycle.py::TestCreateCacheDir::test_6_1_creates_cache_directory_and_returns_path PASSED [  6%]
tests/test_lifecycle.py::TestSaveConfig::test_6_8_calls_save_config_as_when_no_last_config_path PASSED [ 12%]
tests/test_lifecycle.py::TestSaveConfig::test_6_9_writes_to_last_saved_path_when_exists PASSED [ 18%]
tests/test_lifecycle.py::TestSaveLastSession::test_6_11_saves_model_path_host_port_and_geometry PASSED [ 25%]
tests/test_lifecycle.py::TestSaveLastSession::test_6_11_saves_empty_model_path_when_none PASSED [ 31%]
tests/test_lifecycle.py::TestCloseEvent::test_6_14_calls_save_last_session_before_closing PASSED [ 37%]
tests/test_lifecycle.py::TestCreateFileMenu::test_6_7_creates_file_menu_with_save_save_as_load_actions PASSED [ 43%]
tests/test_lifecycle.py::TestCreateFileMenu::test_6_7_save_action_connected_to_save_config PASSED [ 50%]
tests/test_lifecycle.py::TestCreateFileMenu::test_6_7_load_action_connected_to_load_config PASSED [ 56%]
tests/test_lifecycle.py::TestLoadLastSession::test_6_12_restores_host_port_and_model_path PASSED [ 62%]
tests/test_lifecycle.py::TestLoadLastSession::test_6_12_uses_defaults_when_no_saved_values PASSED [ 68%]
tests/test_lifecycle.py::TestSetupContextSizeCombo::test_6_4_populates_all_8_context_size_options PASSED [ 75%]
tests/test_lifecycle.py::TestSetupContextSizeCombo::test_6_5_pre_selects_from_cli_ctx_size PASSED [ 81%]
tests/test_lifecycle.py::TestSetupContextSizeCombo::test_6_6_defaults_to_16k_when_no_ctx_size PASSED [ 87%]
tests/test_lifecycle.py::TestConnectSignals::test_6_15_wires_up_all_button_clicks_and_signals PASSED [ 93%]
tests/test_lifecycle.py::TestConnectSignals::test_6_15_signals_trigger_correct_slots PASSED [100%]

============================== 16 passed in 0.65s ==============================

```


## Assistant

<thinking>
The output is still being truncated. Let me try a different approach to see the full test results.

</thinking>

Output truncated again. Let me redirect to a file and read it:



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher && uv run pytest tests/test_lifecycle.py -v 2>&1 | tee /tmp/test_results.txt && echo "---SEPARATOR---" && cat /tmp/test_results.txt**
Status: Completed

Terminal:
```
============================= test session starts ==============================
platform darwin -- Python 3.14.0, pytest-9.1.0, pluggy-1.6.0 -- /Volumes/teaching/Code/LLamaLauncher/.venv/bin/python3
cachedir: .pytest_cache
PySide6 6.11.1 -- Qt runtime 6.11.1 -- Qt compiled 6.11.1
rootdir: /Volumes/teaching/Code/LLamaLauncher
configfile: pyproject.toml
plugins: cov-7.1.0, qt-4.5.0
collecting ... collected 16 items

tests/test_lifecycle.py::TestCreateCacheDir::test_6_1_creates_cache_directory_and_returns_path PASSED [  6%]
tests/test_lifecycle.py::TestSaveConfig::test_6_8_calls_save_config_as_when_no_last_config_path PASSED [ 12%]
tests/test_lifecycle.py::TestSaveConfig::test_6_9_writes_to_last_saved_path_when_exists PASSED [ 18%]
tests/test_lifecycle.py::TestSaveLastSession::test_6_11_saves_model_path_host_port_and_geometry PASSED [ 25%]
tests/test_lifecycle.py::TestSaveLastSession::test_6_11_saves_empty_model_path_when_none PASSED [ 31%]
tests/test_lifecycle.py::TestCloseEvent::test_6_14_calls_save_last_session_before_closing PASSED [ 37%]
tests/test_lifecycle.py::TestCreateFileMenu::test_6_7_creates_file_menu_with_save_save_as_load_actions PASSED [ 43%]
tests/test_lifecycle.py::TestCreateFileMenu::test_6_7_save_action_connected_to_save_config PASSED [ 50%]
tests/test_lifecycle.py::TestCreateFileMenu::test_6_7_load_action_connected_to_load_config PASSED [ 56%]
tests/test_lifecycle.py::TestLoadLastSession::test_6_12_restores_host_port_and_model_path PASSED [ 62%]
tests/test_lifecycle.py::TestLoadLastSession::test_6_12_uses_defaults_when_no_saved_values PASSED [ 68%]
tests/test_lifecycle.py::TestSetupContextSizeCombo::test_6_4_populates_all_8_context_size_options PASSED [ 75%]
tests/test_lifecycle.py::TestSetupContextSizeCombo::test_6_5_pre_selects_from_cli_ctx_size PASSED [ 81%]
tests/test_lifecycle.py::TestSetupContextSizeCombo::test_6_6_defaults_to_16k_when_no_ctx_size PASSED [ 87%]
tests/test_lifecycle.py::TestConnectSignals::test_6_15_wires_up_all_button_clicks_and_signals PASSED [ 93%]
tests/test_lifecycle.py::TestConnectSignals::test_6_15_signals_trigger_correct_slots PASSED [100%]

============================== 16 passed in 0.66s ==============================
---SEPARATOR---
============================= test session starts ==============================
platform darwin -- Python 3.14.0, pytest-9.1.0, pluggy-1.6.0 -- /Volumes/teaching/Code/LLamaLauncher/.venv/bin/python3
cachedir: .pytest_cache
PySide6 6.11.1 -- Qt runtime 6.11.1 -- Qt compiled 6.11.1
rootdir: /Volumes/teaching/Code/LLamaLauncher
configfile: pyproject.toml
plugins: cov-7.1.0, qt-4.5.0
collecting ... collected 16 items

tests/test_lifecycle.py::TestCreateCacheDir::test_6_1_creates_cache_directory_and_returns_path PASSED [  6%]
tests/test_lifecycle.py::TestSaveConfig::test_6_8_calls_save_config_as_when_no_last_config_path PASSED [ 12%]
tests/test_lifecycle.py::TestSaveConfig::test_6_9_writes_to_last_saved_path_when_exists PASSED [ 18%]
tests/test_lifecycle.py::TestSaveLastSession::test_6_11_saves_model_path_host_port_and_geometry PASSED [ 25%]
tests/test_lifecycle.py::TestSaveLastSession::test_6_11_saves_empty_model_path_when_none PASSED [ 31%]
tests/test_lifecycle.py::TestCloseEvent::test_6_14_calls_save_last_session_before_closing PASSED [ 37%]
tests/test_lifecycle.py::TestCreateFileMenu::test_6_7_creates_file_menu_with_save_save_as_load_actions PASSED [ 43%]
tests/test_lifecycle.py::TestCreateFileMenu::test_6_7_save_action_connected_to_save_config PASSED [ 50%]
tests/test_lifecycle.py::TestCreateFileMenu::test_6_7_load_action_connected_to_load_config PASSED [ 56%]
tests/test_lifecycle.py::TestLoadLastSession::test_6_12_restores_host_port_and_model_path PASSED [ 62%]
tests/test_lifecycle.py::TestLoadLastSession::test_6_12_uses_defaults_when_no_saved_values PASSED [ 68%]
tests/test_lifecycle.py::TestSetupContextSizeCombo::test_6_4_populates_all_8_context_size_options PASSED [ 75%]
tests/test_lifecycle.py::TestSetupContextSizeCombo::test_6_5_pre_selects_from_cli_ctx_size PASSED [ 81%]
tests/test_lifecycle.py::TestSetupContextSizeCombo::test_6_6_defaults_to_16k_when_no_ctx_size PASSED [ 87%]
tests/test_lifecycle.py::TestConnectSignals::test_6_15_wires_up_all_button_clicks_and_signals PASSED [ 93%]
tests/test_lifecycle.py::TestConnectSignals::test_6_15_signals_trigger_correct_slots PASSED [100%]

============================== 16 passed in 0.66s ==============================

```


## Assistant

<thinking>
The terminal output is still being truncated. Let me try a different approach - just run the specific test that was failing to see if it passes now.

</thinking>

Let me just run the specific test class that contains the failing test:



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher && uv run pytest tests/test_lifecycle.py::TestConnectSignals -v 2>&1**
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
collected 2 items

tests/test_lifecycle.py::TestConnectSignals::test_6_15_wires_up_all_button_clicks_and_signals PASSED [ 50%]
tests/test_lifecycle.py::TestConnectSignals::test_6_15_signals_trigger_correct_slots PASSED [100%]

================== 2 passed in 0.17s ===================

```


## Assistant

<thinking>
Both tests pass now. Let me also run the full test suite to make sure nothing else broke.

</thinking>

Both `TestConnectSignals` tests pass now. Let me run the full suite to confirm nothing else broke:



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher && uv run pytest 2>&1**
Status: Completed

Terminal:
```
================= test session starts ==================
platform darwin -- Python 3.14.0, pytest-9.1.0, pluggy-1.6.0
PySide6 6.11.1 -- Qt runtime 6.11.1 -- Qt compiled 6.11.1
rootdir: /Volumes/teaching/Code/LLamaLauncher
configfile: pyproject.toml
testpaths: tests
plugins: cov-7.1.0, qt-4.5.0
collected 165 items

tests/test_config.py ..................          [ 10%]
tests/test_file_selection.py ..................  [ 21%]
tests/test_helper_methods.py ............        [ 29%]
tests/test_lifecycle.py ................         [ 38%]
tests/test_main.py ............................. [ 56%]
                                                 [ 56%]
tests/test_process.py .......................... [ 72%]
...............                                  [ 81%]
tests/test_signals.py .....................      [ 93%]
tests/test_ui_loader.py ..........               [100%]

================= 165 passed in 0.97s ==================

```


## Assistant

<thinking>
The user is running the full test suite and all 165 tests pass. The fix worked. Now I should summarize what was done.

</thinking>

All **165 tests pass**. Here's a summary of the fix:

**Root cause**: `MagicMock` doesn't implement Qt's signal/slot mechanism. When you call `.emit()` on a MagicMock, it just returns another MagicMock — it never invokes connected callbacks. So `app.select_model_button.clicked.emit()` didn't actually call `app._select_model`.

**Fix** (in `LLamaLauncher/tests/test_lifecycle.py`):

Added two helper classes:
- **`_QtSignal`** — simulates a Qt signal: `.connect(callback)` stores the callback AND records it for assertion (via an embedded `MagicMock`), and `.emit()` invokes all stored callbacks.
- **`_MockWidget`** — creates widgets with `_QtSignal` instances for `clicked` and `textChanged`.

Updated `test_6_15_signals_trigger_correct_slots` to use `_MockWidget()` instead of `MagicMock()` for widget attributes. This preserves compatibility with `test_6_14` (which verifies `.connect.assert_called_once_with(...)`) while making signal emission actually trigger the slots.
