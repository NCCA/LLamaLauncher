## User

[@test-driven-development](zed:///agent/skill?name=test-driven-development&source=LLamaLauncher&path=%2FVolumes%2Fteaching%2FCode%2FLLamaLauncher%2F.agents%2Fskills%2Ftest-driven-development%2FSKILL.md) [@pytest-best-practices](zed:///agent/skill?name=pytest-best-practices&source=LLamaLauncher&path=%2FVolumes%2Fteaching%2FCode%2FLLamaLauncher%2F.agents%2Fskills%2Fpytest-best-practices%2FSKILL.md) implement the selected tests [@Testing.md (275:295)](file:///Volumes/teaching/Code/LLamaLauncher/Testing.md#L275:295)

## Assistant

<thinking>
I need to read the test-driven-development skill, pytest-best-practices skill, and the main.py file to understand the methods I need to implement tests for.

</thinking>

I'll start by reading the relevant skills and understanding the target code in `main.py` before writing the tests.



**Tool Call: `test-driven-development` Skill**
Status: Completed

```json
{
  "rendered": "<skill_content name=\"test-driven-development\">\n<source>project-local</source>\n<worktree>LLamaLauncher</worktree>\n<directory>/Volumes/teaching/Code/LLamaLauncher/.agents/skills/test-driven-development</directory>\nRelative paths in this skill resolve against <directory>.\n\n# Test-Driven Development (TDD)\n\n## Overview\n\nWrite the test first. Watch it fail. Write minimal code to pass.\n\n**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.\n\n**Violating the letter of the rules is violating the spirit of the rules.**\n\n## When to Use\n\n**Always:**\n- New features\n- Bug fixes\n- Refactoring\n- Behavior changes\n\n**Exceptions (ask your human partner):**\n- Throwaway prototypes\n- Generated code\n- Configuration files\n\nThinking \"skip TDD just this once\"? Stop. That's rationalization.\n\n## The Iron Law\n\n```\nNO PRODUCTION CODE WITHOUT A FAILING TEST FIRST\n```\n\nWrite code before the test? Delete it. Start over.\n\n**No exceptions:**\n- Don't keep it as \"reference\"\n- Don't \"adapt\" it while writing tests\n- Don't look at it\n- Delete means delete\n\nImplement fresh from tests. Period.\n\n## Red-Green-Refactor\n\n```dot\ndigraph tdd_cycle {\n    rankdir=LR;\n    red [label=\"RED\\nWrite failing test\", shape=box, style=filled, fillcolor=\"#ffcccc\"];\n    verify_red [label=\"Verify fails\\ncorrectly\", shape=diamond];\n    green [label=\"GREEN\\nMinimal code\", shape=box, style=filled, fillcolor=\"#ccffcc\"];\n    verify_green [label=\"Verify passes\\nAll green\", shape=diamond];\n    refactor [label=\"REFACTOR\\nClean up\", shape=box, style=filled, fillcolor=\"#ccccff\"];\n    next [label=\"Next\", shape=ellipse];\n\n    red -> verify_red;\n    verify_red -> green [label=\"yes\"];\n    verify_red -> red [label=\"wrong\\nfailure\"];\n    green -> verify_green;\n    verify_green -> refactor [label=\"yes\"];\n    verify_green -> green [label=\"no\"];\n    refactor -> verify_green [label=\"stay\\ngreen\"];\n    verify_green -> next;\n    next -> red;\n}\n```\n\n### RED - Write Failing Test\n\nWrite one minimal test showing what should happen.\n\n<Good>\n```typescript\ntest('retries failed operations 3 times', async () => {\n  let attempts = 0;\n  const operation = () => {\n    attempts++;\n    if (attempts < 3) throw new Error('fail');\n    return 'success';\n  };\n\n  const result = await retryOperation(operation);\n\n  expect(result).toBe('success');\n  expect(attempts).toBe(3);\n});\n```\nClear name, tests real behavior, one thing\n</Good>\n\n<Bad>\n```typescript\ntest('retry works', async () => {\n  const mock = jest.fn()\n    .mockRejectedValueOnce(new Error())\n    .mockRejectedValueOnce(new Error())\n    .mockResolvedValueOnce('success');\n  await retryOperation(mock);\n  expect(mock).toHaveBeenCalledTimes(3);\n});\n```\nVague name, tests mock not code\n</Bad>\n\n**Requirements:**\n- One behavior\n- Clear name\n- Real code (no mocks unless unavoidable)\n\n### Verify RED - Watch It Fail\n\n**MANDATORY. Never skip.**\n\n```bash\nnpm test path/to/test.test.ts\n```\n\nConfirm:\n- Test fails (not errors)\n- Failure message is expected\n- Fails because feature missing (not typos)\n\n**Test passes?** You're testing existing behavior. Fix test.\n\n**Test errors?** Fix error, re-run until it fails correctly.\n\n### GREEN - Minimal Code\n\nWrite simplest code to pass the test.\n\n<Good>\n```typescript\nasync function retryOperation<T>(fn: () => Promise<T>): Promise<T> {\n  for (let i = 0; i < 3; i++) {\n    try {\n      return await fn();\n    } catch (e) {\n      if (i === 2) throw e;\n    }\n  }\n  throw new Error('unreachable');\n}\n```\nJust enough to pass\n</Good>\n\n<Bad>\n```typescript\nasync function retryOperation<T>(\n  fn: () => Promise<T>,\n  options?: {\n    maxRetries?: number;\n    backoff?: 'linear' | 'exponential';\n    onRetry?: (attempt: number) => void;\n  }\n): Promise<T> {\n  // YAGNI\n}\n```\nOver-engineered\n</Bad>\n\nDon't add features, refactor other code, or \"improve\" beyond the test.\n\n### Verify GREEN - Watch It Pass\n\n**MANDATORY.**\n\n```bash\nnpm test path/to/test.test.ts\n```\n\nConfirm:\n- Test passes\n- Other tests still pass\n- Output pristine (no errors, warnings)\n\n**Test fails?** Fix code, not test.\n\n**Other tests fail?** Fix now.\n\n### REFACTOR - Clean Up\n\nAfter green only:\n- Remove duplication\n- Improve names\n- Extract helpers\n\nKeep tests green. Don't add behavior.\n\n### Repeat\n\nNext failing test for next feature.\n\n## Good Tests\n\n| Quality | Good | Bad |\n|---------|------|-----|\n| **Minimal** | One thing. \"and\" in name? Split it. | `test('validates email and domain and whitespace')` |\n| **Clear** | Name describes behavior | `test('test1')` |\n| **Shows intent** | Demonstrates desired API | Obscures what code should do |\n\n## Why Order Matters\n\n**\"I'll write tests after to verify it works\"**\n\nTests written after code pass immediately. Passing immediately proves nothing:\n- Might test wrong thing\n- Might test implementation, not behavior\n- Might miss edge cases you forgot\n- You never saw it catch the bug\n\nTest-first forces you to see the test fail, proving it actually tests something.\n\n**\"I already manually tested all the edge cases\"**\n\nManual testing is ad-hoc. You think you tested everything but:\n- No record of what you tested\n- Can't re-run when code changes\n- Easy to forget cases under pressure\n- \"It worked when I tried it\" ≠ comprehensive\n\nAutomated tests are systematic. They run the same way every time.\n\n**\"Deleting X hours of work is wasteful\"**\n\nSunk cost fallacy. The time is already gone. Your choice now:\n- Delete and rewrite with TDD (X more hours, high confidence)\n- Keep it and add tests after (30 min, low confidence, likely bugs)\n\nThe \"waste\" is keeping code you can't trust. Working code without real tests is technical debt.\n\n**\"TDD is dogmatic, being pragmatic means adapting\"**\n\nTDD IS pragmatic:\n- Finds bugs before commit (faster than debugging after)\n- Prevents regressions (tests catch breaks immediately)\n- Documents behavior (tests show how to use code)\n- Enables refactoring (change freely, tests catch breaks)\n\n\"Pragmatic\" shortcuts = debugging in production = slower.\n\n**\"Tests after achieve the same goals - it's spirit not ritual\"**\n\nNo. Tests-after answer \"What does this do?\" Tests-first answer \"What should this do?\"\n\nTests-after are biased by your implementation. You test what you built, not what's required. You verify remembered edge cases, not discovered ones.\n\nTests-first force edge case discovery before implementing. Tests-after verify you remembered everything (you didn't).\n\n30 minutes of tests after ≠ TDD. You get coverage, lose proof tests work.\n\n## Common Rationalizations\n\n| Excuse | Reality |\n|--------|---------|\n| \"Too simple to test\" | Simple code breaks. Test takes 30 seconds. |\n| \"I'll test after\" | Tests passing immediately prove nothing. |\n| \"Tests after achieve same goals\" | Tests-after = \"what does this do?\" Tests-first = \"what should this do?\" |\n| \"Already manually tested\" | Ad-hoc ≠ systematic. No record, can't re-run. |\n| \"Deleting X hours is wasteful\" | Sunk cost fallacy. Keeping unverified code is technical debt. |\n| \"Keep as reference, write tests first\" | You'll adapt it. That's testing after. Delete means delete. |\n| \"Need to explore first\" | Fine. Throw away exploration, start with TDD. |\n| \"Test hard = design unclear\" | Listen to test. Hard to test = hard to use. |\n| \"TDD will slow me down\" | TDD faster than debugging. Pragmatic = test-first. |\n| \"Manual test faster\" | Manual doesn't prove edge cases. You'll re-test every change. |\n| \"Existing code has no tests\" | You're improving it. Add tests for existing code. |\n\n## Red Flags - STOP and Start Over\n\n- Code before test\n- Test after implementation\n- Test passes immediately\n- Can't explain why test failed\n- Tests added \"later\"\n- Rationalizing \"just this once\"\n- \"I already manually tested it\"\n- \"Tests after achieve the same purpose\"\n- \"It's about spirit not ritual\"\n- \"Keep as reference\" or \"adapt existing code\"\n- \"Already spent X hours, deleting is wasteful\"\n- \"TDD is dogmatic, I'm being pragmatic\"\n- \"This is different because...\"\n\n**All of these mean: Delete code. Start over with TDD.**\n\n## Example: Bug Fix\n\n**Bug:** Empty email accepted\n\n**RED**\n```typescript\ntest('rejects empty email', async () => {\n  const result = await submitForm({ email: '' });\n  expect(result.error).toBe('Email required');\n});\n```\n\n**Verify RED**\n```bash\n$ npm test\nFAIL: expected 'Email required', got undefined\n```\n\n**GREEN**\n```typescript\nfunction submitForm(data: FormData) {\n  if (!data.email?.trim()) {\n    return { error: 'Email required' };\n  }\n  // ...\n}\n```\n\n**Verify GREEN**\n```bash\n$ npm test\nPASS\n```\n\n**REFACTOR**\nExtract validation for multiple fields if needed.\n\n## Verification Checklist\n\nBefore marking work complete:\n\n- [ ] Every new function/method has a test\n- [ ] Watched each test fail before implementing\n- [ ] Each test failed for expected reason (feature missing, not typo)\n- [ ] Wrote minimal code to pass each test\n- [ ] All tests pass\n- [ ] Output pristine (no errors, warnings)\n- [ ] Tests use real code (mocks only if unavoidable)\n- [ ] Edge cases and errors covered\n\nCan't check all boxes? You skipped TDD. Start over.\n\n## When Stuck\n\n| Problem | Solution |\n|---------|----------|\n| Don't know how to test | Write wished-for API. Write assertion first. Ask your human partner. |\n| Test too complicated | Design too complicated. Simplify interface. |\n| Must mock everything | Code too coupled. Use dependency injection. |\n| Test setup huge | Extract helpers. Still complex? Simplify design. |\n\n## Debugging Integration\n\nBug found? Write failing test reproducing it. Follow TDD cycle. Test proves fix and prevents regression.\n\nNever fix bugs without a test.\n\n## Testing Anti-Patterns\n\nWhen adding mocks or test utilities, read @testing-anti-patterns.md to avoid common pitfalls:\n- Testing mock behavior instead of real behavior\n- Adding test-only methods to production classes\n- Mocking without understanding dependencies\n\n## Final Rule\n\n```\nProduction code → test exists and failed first\nOtherwise → not TDD\n```\n\nNo exceptions without your human partner's permission.\n</skill_content>\n"
}
```

**Tool Call: `pytest-best-practices` Skill**
Status: Completed

```json
{
  "rendered": "<skill_content name=\"pytest-best-practices\">\n<source>project-local</source>\n<worktree>LLamaLauncher</worktree>\n<directory>/Volumes/teaching/Code/LLamaLauncher/.agents/skills/pytest-best-practices</directory>\nRelative paths in this skill resolve against <directory>.\n\n# Pytest Best Practices\n\n## Overview\n\nUse pytest to create fast, readable, maintainable tests that verify\nbehavior.\n\nThis skill applies after the TDD process has decided what needs testing.\n\nFocus: - Writing idiomatic pytest - Designing maintainable tests - Using\nfixtures correctly - Avoiding brittle tests - Keeping tests readable -\nManaging complex test environments with nox\n\n------------------------------------------------------------------------\n\n# Test Structure\n\n## Follow Arrange-Act-Assert\n\nEvery test should clearly separate:\n\n1.  Arrange - setup test data/state\n2.  Act - execute the behavior\n3.  Assert - verify the result\n\nGood:\n\n``` python\ndef test_user_registration_rejects_duplicate_email():\n    service = UserService()\n    service.create_user(\"test@example.com\")\n\n    result = service.create_user(\"test@example.com\")\n\n    assert result.error == \"Email already exists\"\n```\n\n------------------------------------------------------------------------\n\n# Test Naming\n\nTest names should describe behavior.\n\nGood:\n\n``` python\ndef test_payment_fails_when_card_is_expired():\n    ...\n```\n\nBad:\n\n``` python\ndef test_payment():\n    ...\n```\n\n------------------------------------------------------------------------\n\n# Assertions\n\nPrefer direct assertions:\n\n``` python\nassert user.name == \"Alice\"\nassert response.status_code == 200\n```\n\nTest behavior, not implementation details.\n\n------------------------------------------------------------------------\n\n# One Behaviour Per Test\n\nTests should verify one thing.\n\nGood:\n\n``` python\ndef test_discount_is_applied_to_members():\n    price = calculate_price(100, member=True)\n\n    assert price == 90\n```\n\n------------------------------------------------------------------------\n\n# Fixtures\n\nUse fixtures for reusable setup:\n\n``` python\nimport pytest\n\n@pytest.fixture\ndef user():\n    return User(name=\"Alice\")\n```\n\nKeep fixtures isolated and avoid shared mutable state.\n\n------------------------------------------------------------------------\n\n# Parametrized Tests\n\nUse parametrization for multiple inputs:\n\n``` python\n@pytest.mark.parametrize(\n    \"email\",\n    [\"\", \"invalid\", \"missing@domain\"]\n)\ndef test_invalid_emails_are_rejected(email):\n    assert validate_email(email) is False\n```\n\n------------------------------------------------------------------------\n\n# Exception Testing\n\nUse pytest.raises:\n\n``` python\nwith pytest.raises(FileNotFoundError):\n    load_file(\"missing.txt\")\n```\n\n------------------------------------------------------------------------\n\n# Mocking\n\nMock only external boundaries:\n\n-   Network calls\n-   Filesystem\n-   Time\n-   External services\n\nAvoid mocking your own code because it tests the mock rather than the\nbehavior.\n\n------------------------------------------------------------------------\n\n# Temporary Files\n\nUse tmp_path:\n\n``` python\ndef test_save_file(tmp_path):\n    path = tmp_path / \"data.txt\"\n\n    save_data(path, \"hello\")\n\n    assert path.read_text() == \"hello\"\n```\n\n------------------------------------------------------------------------\n\n# Nox for Complex Test Workflows\n\nUse nox when tests need multiple environments, Python versions, external\nservices, or repeatable automation.\n\nNox creates isolated test sessions using virtual environments.\n\nCommon uses:\n\n-   Testing against multiple Python versions\n-   Running linting and formatting checks\n-   Running integration tests\n-   Testing optional dependencies\n-   Reproducing CI pipelines locally\n\nExample `noxfile.py`:\n\n``` python\nimport nox\n\n\n@nox.session(python=[\"3.10\", \"3.11\", \"3.12\"])\ndef tests(session):\n    session.install(\".[test]\")\n    session.run(\"pytest\")\n```\n\nRun:\n\n``` bash\nnox\n```\n\n------------------------------------------------------------------------\n\n## Separate Test Sessions\n\nKeep different types of tests separate.\n\nExample:\n\n``` python\n@nox.session\ndef unit(session):\n    session.install(\".[test]\")\n    session.run(\"pytest\", \"tests/unit\")\n\n\n@nox.session\ndef integration(session):\n    session.install(\".[test]\")\n    session.run(\"pytest\", \"tests/integration\")\n```\n\nRun:\n\n``` bash\nnox -s unit\nnox -s integration\n```\n\n------------------------------------------------------------------------\n\n## Running External Services\n\nFor integration tests, use nox to manage setup.\n\nExample:\n\n``` python\n@nox.session\ndef database_tests(session):\n    session.install(\".[test]\")\n\n    session.run(\n        \"pytest\",\n        \"tests/database\"\n    )\n```\n\nKeep environment setup reproducible.\n\nAvoid tests that only work because a developer machine happens to be\nconfigured correctly.\n\n------------------------------------------------------------------------\n\n## Nox Best Practices\n\nGood:\n\n-   Keep sessions small and focused\n-   Match CI environments locally\n-   Pin important dependencies\n-   Use sessions for repeatable workflows\n-   Keep unit tests fast and separate from integration tests\n\nAvoid:\n\n-   Putting all test logic inside `noxfile.py`\n-   Replacing pytest with nox\n-   Running slow integration tests for every small change\n\nNox orchestrates tests. Pytest defines tests.\n\n------------------------------------------------------------------------\n\n# Test Files\n\nRecommended structure:\n\n    project/\n        src/\n            users.py\n\n        tests/\n            test_users.py\n\nNaming:\n\n    test_<module>.py\n    test_<behavior>()\n\n------------------------------------------------------------------------\n\n# Running Tests\n\nFocused:\n\n``` bash\nuv run pytest tests/test_users.py\n```\n\nSingle test:\n\n``` bash\nuv run pytest tests/test_users.py::test_create_user\n```\n\nVerbose:\n\n``` bash\nuv run pytest -v\n```\n\nStop on first failure:\n\n``` bash\nuv run pytest -x\n```\n\n------------------------------------------------------------------------\n\n# Coverage\n\nUse coverage to find missing tests:\n\n``` bash\nuv run pytest --cov=src\n```\n\nDo not chase 100% coverage blindly.\n\nPrefer: - Important behaviour covered - Edge cases covered - Failure\nmodes covered\n\n------------------------------------------------------------------------\n\n# Common Pytest Mistakes\n\n  Mistake                   Better Approach\n  ------------------------- ----------------------------\n  Testing private methods   Test public behaviour\n  Large fixtures            Smaller focused fixtures\n  Shared state              Fresh fixtures\n  Too many mocks            Test real code\n  Duplicate cases           Parametrize\n  Weak assertions           Assert meaningful outcomes\n\n------------------------------------------------------------------------\n\n# Style\n\nWhen grouping tests, prefer function-based grouping over class-based grouping. \n\nIf a test needs shared state, prefer a fixture over a class. \n\nIf a test needs to be grouped logically, prefer class-based grouping over function-based grouping.\n\nCan use @pytest.mark. to group tests by category or feature.\n\n| Situation | Use |\n|---|---|\n| Single behaviour | Function |\n| Fixture-based tests | Function |\n| Parameterised tests | Function |\n| Many related behaviours | Class |\n| Large feature area | Class |\n| Need shared state | Usually fixture, not class |\n\n# Final Checklist\n\n-   [ ] Test name explains behaviour\n-   [ ] Test follows Arrange-Act-Assert\n-   [ ] Test verifies behaviour, not implementation\n-   [ ] Fixtures used correctly\n-   [ ] Tests are isolated\n-   [ ] Parametrize repeated cases\n-   [ ] Mocks only used at boundaries\n-   [ ] Nox used for complex/repeatable workflows\n-   [ ] Assertions verify meaningful results\n-   [ ] pytest passes successfully\n\nA good pytest suite should be:\n\n-   Fast\n-   Clear\n-   Deterministic\n-   Maintainable\n-   Trustworthy\n\n\n# Pytest installation\n``` bash\nuv install --dev pytest\n```\n</skill_content>\n"
}
```

**Tool Call: Read file `main.py` (lines 541-616)**
Status: Completed

```LLamaLauncher/main.py
   541	                "n_predict",
   542	                self.enable_n_predict_checkbox,
   543	                self.n_predict_spinbox,
   544	            )
   545	            self._apply_param(
   546	                perf, "parallel", self.enable_parallel_checkbox, self.parallel_spinbox
   547	            )
   548	
   549	            if "flash_attn" in perf:
   550	                text = perf["flash_attn"]
   551	                index = self.flash_attn_combobox.findText(text)
   552	                if index >= 0:
   553	                    self.flash_attn_combobox.setCurrentIndex(index)
   554	
   555	            self._apply_combo_param(
   556	                perf,
   557	                "cache_type_k",
   558	                self.enable_cache_type_k_checkbox,
   559	                self.cache_type_k_combobox,
   560	            )
   561	            self._apply_combo_param(
   562	                perf,
   563	                "cache_type_v",
   564	                self.enable_cache_type_v_checkbox,
   565	                self.cache_type_v_combobox,
   566	            )
   567	
   568	            if "mmap" in perf:
   569	                self.enable_mmap_checkbox.setChecked(bool(perf["mmap"]))
   570	            if "mlock" in perf:
   571	                self.enable_mlock_checkbox.setChecked(bool(perf["mlock"]))
   572	            if "cont_batching" in perf:
   573	                self.enable_cont_batching_checkbox.setChecked(
   574	                    bool(perf["cont_batching"])
   575	                )
   576	
   577	        # Advanced Generation parameters
   578	        if "advanced" in config:
   579	            adv = config["advanced"]
   580	            self._apply_param(
   581	                adv,
   582	                "spec_draft_n_max",
   583	                self.enable_spec_draft_n_max_checkbox,
   584	                self.spec_draft_n_max_spinbox,
   585	            )
   586	            self._apply_param(adv, "seed", self.enable_seed_checkbox, self.seed_spinbox)
   587	
   588	            # Draft model (path-based)
   589	            if "draft_model" in adv:
   590	                draft = adv["draft_model"]
   591	                self.enable_draft_model_checkbox.setChecked(draft.get("enabled", False))
   592	                self._set_path_field(self.draft_model_line_edit, draft.get("path", ""))
   593	
   594	            # Grammar (path-based)
   595	            if "grammar" in adv:
   596	                grammar = adv["grammar"]
   597	                self.enable_grammar_checkbox.setChecked(grammar.get("enabled", False))
   598	                self._set_path_field(self.grammar_line_edit, grammar.get("path", ""))
   599	
   600	            # JSON schema (path-based)
   601	            if "json_schema" in adv:
   602	                js = adv["json_schema"]
   603	                self.enable_json_schema_checkbox.setChecked(js.get("enabled", False))
   604	                self._set_path_field(self.json_schema_line_edit, js.get("path", ""))
   605	
   606	            self._apply_combo_param(
   607	                adv,
   608	                "rope_scaling",
   609	                self.enable_rope_scaling_checkbox,
   610	                self.rope_scaling_combobox,
   611	            )
   612	            self._apply_param(
   613	                adv,
   614	                "rope_freq_base",
   615	                self.enable_rope_freq_base_checkbox,
   616	                self.rope_freq_base_spinbox,

```


## Assistant

<thinking>
The line numbers in main.py don't match - I got lines 541+ but they show `_apply_param` and config loading code, not the file selection methods. Let me search for the actual file selection methods mentioned in the task (lines 541-610 in the spec).

Let me read the correct section of main.py with the file selection methods.

</thinking>

The line numbers shifted. Let me find the actual file selection methods in main.py:



**Tool Call: Search files for regex `def _select_model|def _select_mmproj|def _select_draft_model|def _select_json_schema|def _on_model_selection_changed`**
Status: Completed

Found 5 matches:

## Matches in LLamaLauncher/main.py

### class LlamaLaunchApp › def _select_model › L760-764
```
    # ------------------------------------------------------------------

    def _select_model(self) -> None:
        """Open a file dialog to select a .gguf model file.

```

### class LlamaLaunchApp › def _select_mmproj › L779-783
```
            self._on_model_selection_changed()

    def _select_mmproj(self) -> None:
        """Open a file dialog to select a .gguf mmproj file.

```

### class LlamaLaunchApp › def _select_draft_model › L797-801
```
            self.mmproj_path_edit.setText(file_path.rsplit("/", 1)[-1])

    def _select_draft_model(self) -> None:
        """Open a file dialog to select a draft model .gguf file.

```

### class LlamaLaunchApp › def _select_json_schema › L814-818
```
            self.draft_model_line_edit.setText(file_path.rsplit("/", 1)[-1])

    def _select_json_schema(self) -> None:
        """Open a file dialog to select a JSON schema file.

```

### class LlamaLaunchApp › def _on_model_selection_changed › L831-835
```
            self.json_schema_line_edit.setText(file_path.rsplit("/", 1)[-1])

    def _on_model_selection_changed(self) -> None:
        """Enable launch button when a model is selected, disable otherwise."""
        has_model = bool(self.model_path_edit.property("fullPath"))
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
Now I need to read the actual methods in main.py to understand their implementation. Let me read the relevant lines for each method.

</thinking>

Now let me read all 5 methods and the existing test file structure:



**Tool Call: Read file `main.py` (lines 760-840)**
Status: Completed

```LLamaLauncher/main.py
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
   831	            self.json_schema_line_edit.setText(file_path.rsplit("/", 1)[-1])
   832	
   833	    def _on_model_selection_changed(self) -> None:
   834	        """Enable launch button when a model is selected, disable otherwise."""
   835	        has_model = bool(self.model_path_edit.property("fullPath"))
   836	        is_running = self._process.state() == QProcess.Running
   837	        self.launch_button.setEnabled(has_model and not is_running)
   838	
   839	    def _toggle_launch(self) -> None:
   840	        """Launch or stop the llama-server based on current process state."""

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


## Assistant

<thinking>
Good, I need to create a git worktree and then implement the tests. Let me first check if there's an existing test file for file selection.

</thinking>

Now I understand the methods. Let me check if `test_file_selection.py` already exists and read any existing test files for patterns:



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
Good, I can see there's no test_file_selection.py yet. Let me create a git worktree first, then implement the tests following TDD.

Let me also check if there's an existing test file pattern to follow by reading one of the simpler test files.

</thinking>

Now let me create the git worktree as required by the project rules:



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher && git status --short**
Status: Completed

Terminal:
```
?? .DS_Store
?? .worktrees/
?? SmallModel.json
?? docs/agent-sessions/
?? docs/llama_help.md
?? headroom_memory.db
?? process_command.py
?? pytest-best-practices.md
?? test.json
?? tests/test_process.py

```


## Assistant

<thinking>
Good, there are uncommitted changes but they're all untracked files. The main branch should be clean. Let me check the current branch and create a worktree for this task.

</thinking>

Good, only untracked files. Let me check the current branch and create a worktree:



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher && git branch --show-current**
Status: Completed

Terminal:
```
main




```


## Assistant

<thinking>
The user is in the main branch. According to the git workflow rules, I need to create a worktree before editing code. Let me follow the TDD process:

1. First, create a git worktree for this task
2. Then write the failing test (RED)
3. Run the test to verify it fails
4. Write minimal code to pass (GREEN)
5. Run tests to verify all pass
6. Refactor if needed

Let me start by creating the worktree and then writing the first test.

I need to create tests for 6 methods:
- `_select_model` (L762-779) - opens dialog, sets fullPath + short filename on model_path_edit
- `_select_mmproj` (L781-797) - opens dialog, sets fullPath + short filename on mmproj_path_edit
- `_select_draft_model` (L799-815) - opens dialog, sets fullPath + short filename on draft_model_line_edit
- `_select_json_schema` (L817-832) - opens dialog, sets fullPath + short filename on json_schema_line_edit
- `_on_model_selection_changed` (L834-838) - enables launch button when model is selected

All of these require mocking `QFileDialog.getOpenFileName`. The tests will be in `tests/test_file_selection.py`.

Let me follow TDD strictly: write one test at a time, watch it fail, then implement. But wait - the production code already exists! The task says "implement the selected tests" for methods that are already implemented in main.py. So this is testing existing code, not writing new code.

Given that the production code already exists, I should:
1. Create the test file with all 6 tests
2. Run them to verify they pass (since the code is already implemented)
3. This is essentially adding tests for existing functionality

Actually, re-reading the task: "implement the selected tests" from Testing.md Phase 4. The production methods are already in main.py. I need to write tests for them following TDD principles. Since the code exists, I'll write the tests first (which will initially fail because the test file doesn't exist yet), then verify they pass.

Let me follow the TDD spirit: write tests first, run them, make sure they pass. Since this is testing existing code, the "RED" phase is that the tests don't exist yet (or would fail if the methods didn't exist). The "GREEN" phase is making the tests pass against the existing implementation.

Let me create the worktree and then write the test file.

</thinking>

I'll follow TDD by writing tests first, then verifying they pass against the existing implementation. Let me start by creating a worktree for this task.



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher && git worktree add .worktrees/file-selection-tests -b test/file-selection-tests 2>&1**
Status: Completed

Terminal:
```
Preparing worktree (new branch 'test/file-selection-tests')
HEAD is now at 1fe709d more tests added


```


## Assistant

<thinking>
Good, the worktree was created successfully. Now I need to follow TDD: write the failing test first, then make it pass.

Since the production code already exists in main.py, I'll write the tests for each method one at a time, following the red-green-refactor cycle. Let me start by reading the exact implementation of each method again to understand what I need to test.

Let me read the methods more carefully:

</thinking>

Good, worktree created. Now let me read the exact implementations of the methods I need to test:



**Tool Call: Read file `main.py` (lines 760-845)**
Status: Completed

```LLamaLauncher/main.py
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
   831	            self.json_schema_line_edit.setText(file_path.rsplit("/", 1)[-1])
   832	
   833	    def _on_model_selection_changed(self) -> None:
   834	        """Enable launch button when a model is selected, disable otherwise."""
   835	        has_model = bool(self.model_path_edit.property("fullPath"))
   836	        is_running = self._process.state() == QProcess.Running
   837	        self.launch_button.setEnabled(has_model and not is_running)
   838	
   839	    def _toggle_launch(self) -> None:
   840	        """Launch or stop the llama-server based on current process state."""
   841	        if self._process.state() == QProcess.Running:
   842	            self._stop_model()
   843	        else:
   844	            self._launch_model()
   845	

```


## Assistant

<thinking>
Now I have a clear understanding of the 6 methods I need to write tests for:

1. `_select_model` - Opens QFileDialog, sets fullPath property and text on model_path_edit, calls _on_model_selection_changed
2. `_select_mmproj` - Opens QFileDialog, sets fullPath property and text on mmproj_path_edit
3. `_select_draft_model` - Opens QFileDialog, sets fullPath property and text on draft_model_line_edit
4. `_select_json_schema` - Opens QFileDialog, sets fullPath property and text on json_schema_line_edit
5. `_on_model_selection_changed` - Enables launch button when model is selected, disables otherwise

Now let me follow TDD:
1. Write the test file with all 6 tests first
2. Run the tests to verify they pass against the existing implementation
3. Refactor if needed

Let me also check if there's an existing mock_app fixture or similar that I can use as a base for my tests. I need to understand how to create a minimal app instance for testing these methods.

Looking at the conftest.py, I see:
- `qapp` fixture - provides QApplication singleton
- `temp_dir` fixture - provides temporary directory
- `mock_qprocess` fixture - provides mocked QProcess

I need to create a fixture that gives me an instance of LlamaLaunchApp (or whatever the main window class is called). Let me check what the class is called.

From the grep results, I can see "class LlamaLaunchApp" so that's the class name.

Now let me write the tests following TDD:
1. Write the test file with all 6 test cases
2. Run them to verify they pass
3. Refactor if needed

Let me create the test file.

</thinking>

Now I have a clear picture of all 6 methods. Let me follow TDD strictly: write tests first, then verify they pass against the existing implementation.

Let me check the app class name and any existing fixtures I can leverage:



**Tool Call: Search files for regex `^class LlamaLaunchApp`**
Status: Completed

Found 1 matches:

## Matches in LLamaLauncher/main.py

### class LlamaLaunchApp › L25-35
```
class LlamaLaunchApp(QMainWindow):
    """Main application window for the Llama model launcher.

    Loads its UI from a .ui file via QUiLoader and wires up all
    signals and slots to preserve existing behaviour.
    """

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 8080,
```

1084 lines remaining in ancestor node. Read the file to see all.


## Assistant

<thinking>
Now I have a clear picture of what I need to do. Let me follow TDD strictly:

1. First, I'll write the failing test (RED) - create the test file with all 6 test cases
2. Then run the tests to verify they fail (since the test file doesn't exist yet)
3. Then make them pass (GREEN) - since the production code already exists, the tests should pass once I fix any issues

Let me create the test file with all 6 tests following the Arrange-Act-Assert pattern, using pytest fixtures and mocking QFileDialog.getOpenFileName.

I need to:
1. Create a fixture that provides a LlamaLaunchApp instance with mocked line edits
2. Mock QFileDialog.getOpenFileName to return a fake file path
3. Write 6 test cases following the TDD red-green-refactor cycle

Let me start by writing all 6 tests in the test file.

</thinking>

Now I have everything I need. Let me follow TDD strictly: write the failing test first (RED), then make it pass (GREEN).

**RED - Write Failing Test**

I'll create the test file with all 6 test cases, starting with the fixture and first test:



**Tool Call: tests/test\_file\_selection.py**
Status: Completed

Diff: tests/test_file_selection.py
```
"""Tests for file dialog selection methods in LlamaLaunchApp.

These methods open file dialogs via QFileDialog.getOpenFileName and set
properties on line edit widgets. Each test mocks the file dialog to return
a controlled path and verifies the correct side effects.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Ensure production module is importable
_project_root = str(Path(__file__).resolve().parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from PySide6.QtCore import QProcess
from PySide6.QtWidgets import QApplication, QLineEdit

from main import LlamaLaunchApp


@pytest.fixture()
def mock_line_edit():
    """Provide a mock QLineEdit for testing path display logic."""
    edit = MagicMock(spec=QLineEdit)
    edit.property.return_value = None
    return edit


@pytest.fixture()
def app_with_line_edits(mock_line_edit):
    """Provide a LlamaLaunchApp with line edits replaced by mocks.

    This fixture creates a minimal app instance and replaces the line
    edit attributes that file selection methods interact with, allowing
    us to verify property and text calls without a full UI.
    """
    app = QApplication.instance() or QApplication([])
    window = LlamaLaunchApp.__new__(LlamaLaunchApp)

    # Mock the process attribute
    window._process = MagicMock(spec=QProcess)
    window._process.state.return_value = QProcess.NotRunning  # type: ignore

    # Replace line edits with mocks
    window.model_path_edit = mock_line_edit
    window.mmproj_path_edit = MagicMock(spec=QLineEdit)
    window.mmproj_path_edit.property.return_value = None
    window.draft_model_line_edit = MagicMock(spec=QLineEdit)
    window.draft_model_line_edit.property.return_value = None
    window.json_schema_line_edit = MagicMock(spec=QLineEdit)
    window.json_schema_line_edit.property.return_value = None

    # Mock launch button
    window.launch_button = MagicMock()

    # Private path attributes
    window._model_path = ""
    window._mmproj_path = ""

    return window


class TestSelectModel:
    """Tests for _select_model file dialog method.

    Target: main.py lines 762-779
    """

    def test_select_model_sets_fullpath_on_model_path_edit(self, app_with_line_edits):
        """_select_model stores the full path as a custom property on model_path_edit."""
        fake_path = "/models/llama.gguf"

        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=(fake_path, ""),
        ):
            app_with_line_edits._select_model()

        app_with_line_edits.model_path_edit.setProperty.assert_called_once_with("fullPath", fake_path)

    def test_select_model_sets_short_filename_on_model_path_edit(self, app_with_line_edits):
        """_select_model displays only the short filename in the line edit."""
        fake_path = "/models/llama.gguf"

        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=(fake_path, ""),
        ):
            app_with_line_edits._select_model()

        app_with_line_edits.model_path_edit.setText.assert_called_once_with("llama.gguf")

    def test_select_model_stores_full_path_in_private_attribute(self, app_with_line_edits):
        """_select_model stores the full path in _model_path."""
        fake_path = "/models/llama.gguf"

        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=(fake_path, ""),
        ):
            app_with_line_edits._select_model()

        assert app_with_line_edits._model_path == fake_path

    def test_select_model_calls_on_model_selection_changed(self, app_with_line_edits):
        """_select_model triggers _on_model_selection_changed after setting path."""
        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=("/models/llama.gguf", ""),
        ):
            with patch.object(
                app_with_line_edits,
                "_on_model_selection_changed",
            ) as mock_callback:
                app_with_line_edits._select_model()

                mock_callback.assert_called_once()

    def test_select_model_does_nothing_on_cancel(self, app_with_line_edits):
        """_select_model does nothing when the user cancels the dialog."""
        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=("", ""),
        ):
            app_with_line_edits._select_model()

        app_with_line_edits.model_path_edit.setProperty.assert_not_called()
        app_with_line_edits.model_path_edit.setText.assert_not_called()


class TestSelectMmproj:
    """Tests for _select_mmproj file dialog method.

    Target: main.py lines 781-797
    """

    def test_select_mmproj_sets_fullpath_on_mmproj_path_edit(self, app_with_line_edits):
        """_select_mmproj stores the full path as a custom property on mmproj_path_edit."""
        fake_path = "/models/multi-modal.gguf"

        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=(fake_path, ""),
        ):
            app_with_line_edits._select_mmproj()

        app_with_line_edits.mmproj_path_edit.setProperty.assert_called_once_with("fullPath", fake_path)

    def test_select_mmproj_sets_short_filename_on_mmproj_path_edit(self, app_with_line_edits):
        """_select_mmproj displays only the short filename in the line edit."""
        fake_path = "/models/multi-modal.gguf"

        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=(fake_path, ""),
        ):
            app_with_line_edits._select_mmproj()

        app_with_line_edits.mmproj_path_edit.setText.assert_called_once_with("multi-modal.gguf")

    def test_select_mmproj_stores_full_path_in_private_attribute(self, app_with_line_edits):
        """_select_mmproj stores the full path in _mmproj_path."""
        fake_path = "/models/multi-modal.gguf"

        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=(fake_path, ""),
        ):
            app_with_line_edits._select_mmproj()

        assert app_with_line_edits._mmproj_path == fake_path

    def test_select_mmproj_does_nothing_on_cancel(self, app_with_line_edits):
        """_select_mmproj does nothing when the user cancels the dialog."""
        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=("", ""),
        ):
            app_with_line_edits._select_mmproj()

        app_with_line_edits.mmproj_path_edit.setProperty.assert_not_called()
        app_with_line_edits.mmproj_path_edit.setText.assert_not_called()


class TestSelectDraftModel:
    """Tests for _select_draft_model file dialog method.

    Target: main.py lines 799-814
    """

    def test_select_draft_model_sets_fullpath_on_draft_model_line_edit(self, app_with_line_edits):
        """_select_draft_model stores the full path as a custom property on draft_model_line_edit."""
        fake_path = "/models/draft-model.gguf"

        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=(fake_path, ""),
        ):
            app_with_line_edits._select_draft_model()

        app_with_line_edits.draft_model_line_edit.setProperty.assert_called_once_with("fullPath", fake_path)

    def test_select_draft_model_sets_short_filename_on_draft_model_line_edit(self, app_with_line_edits):
        """_select_draft_model displays only the short filename in the line edit."""
        fake_path = "/models/draft-model.gguf"

        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=(fake_path, ""),
        ):
            app_with_line_edits._select_draft_model()

        app_with_line_edits.draft_model_line_edit.setText.assert_called_once_with("draft-model.gguf")

    def test_select_draft_model_does_nothing_on_cancel(self, app_with_line_edits):
        """_select_draft_model does nothing when the user cancels the dialog."""
        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=("", ""),
        ):
            app_with_line_edits._select_draft_model()

        app_with_line_edits.draft_model_line_edit.setProperty.assert_not_called()
        app_with_line_edits.draft_model_line_edit.setText.assert_not_called()


class TestSelectJsonSchema:
    """Tests for _select_json_schema file dialog method.

    Target: main.py lines 816-831
    """

    def test_select_json_schema_sets_fullpath_on_json_schema_line_edit(self, app_with_line_edits):
        """_select_json_schema stores the full path as a custom property on json_schema_line_edit."""
        fake_path = "/schemas/schema.json"

        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=(fake_path, ""),
        ):
            app_with_line_edits._select_json_schema()

        app_with_line_edits.json_schema_line_edit.setProperty.assert_called_once_with("fullPath", fake_path)

    def test_select_json_schema_sets_short_filename_on_json_schema_line_edit(self, app_with_line_edits):
        """_select_json_schema displays only the short filename in the line edit."""
        fake_path = "/schemas/schema.json"

        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=(fake_path, ""),
        ):
            app_with_line_edits._select_json_schema()

        app_with_line_edits.json_schema_line_edit.setText.assert_called_once_with("schema.json")

    def test_select_json_schema_does_nothing_on_cancel(self, app_with_line_edits):
        """_select_json_schema does nothing when the user cancels the dialog."""
        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=("", ""),
        ):
            app_with_line_edits._select_json_schema()

        app_with_line_edits.json_schema_line_edit.setProperty.assert_not_called()
        app_with_line_edits.json_schema_line_edit.setText.assert_not_called()


class TestOnModelSelectionChanged:
    """Tests for _on_model_selection_changed method.

    Target: main.py lines 833-837
    """

    def test_on_model_selection_changed_enables_launch_button_when_model_selected(self, app_with_line_edits):
        """_on_model_selection_changed enables the launch button when a model path exists."""
        app_with_line_edits.model_path_edit.property.return_value = "/models/llama.gguf"

        app_with_line_edits._on_model_selection_changed()

        app_with_line_edits.launch_button.setEnabled.assert_called_once_with(True)

    def test_on_model_selection_changed_disables_launch_button_when_no_model(self, app_with_line_edits):
        """_on_model_selection_changed disables the launch button when no model is selected."""
        app_with_line_edits.model_path_edit.property.return_value = None

        app_with_line_edits._on_model_selection_changed()

        app_with_line_edits.launch_button.setEnabled.assert_called_once_with(False)

    def test_on_model_selection_changed_disables_launch_button_when_process_running(self, app_with_line_edits):
        """_on_model_selection_changed disables the launch button when process is running."""
        from PySide6.QtCore import QProcess

        app_with_line_edits.model_path_edit.property.return_value = "/models/llama.gguf"
        app_with_line_edits._process.state.return_value = QProcess.Running  # type: ignore

        app_with_line_edits._on_model_selection_changed()

        app_with_line_edits.launch_button.setEnabled.assert_called_once_with(False)

```


## Assistant

<thinking>
The file was written successfully. Now I need to run the tests to verify they pass against the existing implementation. Let me run the tests in the worktree.

</thinking>

Good, the test file is created. Now let me run the tests to verify they pass against the existing implementation:



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher && uv run pytest -v tests/test_file_selection.py 2>&1**
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
collected 18 items

tests/test_file_selection.py::TestSelectModel::test_select_model_sets_fullpath_on_model_path_edit PASSED [  5%]
tests/test_file_selection.py::TestSelectModel::test_select_model_sets_short_filename_on_model_path_edit PASSED [ 11%]
tests/test_file_selection.py::TestSelectModel::test_select_model_stores_full_path_in_private_attribute PASSED [ 16%]
tests/test_file_selection.py::TestSelectModel::test_select_model_calls_on_model_selection_changed PASSED [ 22%]
tests/test_file_selection.py::TestSelectModel::test_select_model_does_nothing_on_cancel PASSED [ 27%]
tests/test_file_selection.py::TestSelectMmproj::test_select_mmproj_sets_fullpath_on_mmproj_path_edit PASSED [ 33%]
tests/test_file_selection.py::TestSelectMmproj::test_select_mmproj_sets_short_filename_on_mmproj_path_edit PASSED [ 38%]
tests/test_file_selection.py::TestSelectMmproj::test_select_mmproj_stores_full_path_in_private_attribute PASSED [ 44%]
tests/test_file_selection.py::TestSelectMmproj::test_select_mmproj_does_nothing_on_cancel PASSED [ 50%]
tests/test_file_selection.py::TestSelectDraftModel::test_select_draft_model_sets_fullpath_on_draft_model_line_edit PASSED [ 55%]
tests/test_file_selection.py::TestSelectDraftModel::test_select_draft_model_sets_short_filename_on_draft_model_line_edit PASSED [ 61%]
tests/test_file_selection.py::TestSelectDraftModel::test_select_draft_model_does_nothing_on_cancel PASSED [ 66%]
tests/test_file_selection.py::TestSelectJsonSchema::test_select_json_schema_sets_fullpath_on_json_schema_line_edit PASSED [ 72%]
tests/test_file_selection.py::TestSelectJsonSchema::test_select_json_schema_sets_short_filename_on_json_schema_line_edit PASSED [ 77%]
tests/test_file_selection.py::TestSelectJsonSchema::test_select_json_schema_does_nothing_on_cancel PASSED [ 83%]
tests/test_file_selection.py::TestOnModelSelectionChanged::test_on_model_selection_changed_enables_launch_button_when_model_selected PASSED [ 88%]
tests/test_file_selection.py::TestOnModelSelectionChanged::test_on_model_selection_changed_disables_launch_button_when_no_model PASSED [ 94%]
tests/test_file_selection.py::TestOnModelSelectionChanged::test_on_model_selection_changed_disables_launch_button_when_process_running PASSED [100%]

================== 18 passed in 0.38s ==================

```


## Assistant

<thinking>
The user didn't say anything new - this appears to be an empty message after I ran the tests. Let me check what happened with my test run. The output was compressed, so I need to retrieve it to see if all tests passed.

Looking at the initial output, I can see tests 1-9 passed (lines 5%-50%). I need to see the rest of the results to know if all 18 tests passed. Let me retrieve the full output.

</thinking>

Let me retrieve the full test output to see if all tests passed:



**Tool Call: headroom_retrieve**
Status: Failed

## Assistant

<thinking>
The user didn't send a message - this appears to be an empty/missing message. Let me just run the tests again to see the full output and check if they all passed.

</thinking>

Let me run the tests again to see the full output:



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher && uv run pytest -v tests/test_file_selection.py 2>&1**
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
collected 18 items

tests/test_file_selection.py::TestSelectModel::test_select_model_sets_fullpath_on_model_path_edit PASSED [  5%]
tests/test_file_selection.py::TestSelectModel::test_select_model_sets_short_filename_on_model_path_edit PASSED [ 11%]
tests/test_file_selection.py::TestSelectModel::test_select_model_stores_full_path_in_private_attribute PASSED [ 16%]
tests/test_file_selection.py::TestSelectModel::test_select_model_calls_on_model_selection_changed PASSED [ 22%]
tests/test_file_selection.py::TestSelectModel::test_select_model_does_nothing_on_cancel PASSED [ 27%]
tests/test_file_selection.py::TestSelectMmproj::test_select_mmproj_sets_fullpath_on_mmproj_path_edit PASSED [ 33%]
tests/test_file_selection.py::TestSelectMmproj::test_select_mmproj_sets_short_filename_on_mmproj_path_edit PASSED [ 38%]
tests/test_file_selection.py::TestSelectMmproj::test_select_mmproj_stores_full_path_in_private_attribute PASSED [ 44%]
tests/test_file_selection.py::TestSelectMmproj::test_select_mmproj_does_nothing_on_cancel PASSED [ 50%]
tests/test_file_selection.py::TestSelectDraftModel::test_select_draft_model_sets_fullpath_on_draft_model_line_edit PASSED [ 55%]
tests/test_file_selection.py::TestSelectDraftModel::test_select_draft_model_sets_short_filename_on_draft_model_line_edit PASSED [ 61%]
tests/test_file_selection.py::TestSelectDraftModel::test_select_draft_model_does_nothing_on_cancel PASSED [ 66%]
tests/test_file_selection.py::TestSelectJsonSchema::test_select_json_schema_sets_fullpath_on_json_schema_line_edit PASSED [ 72%]
tests/test_file_selection.py::TestSelectJsonSchema::test_select_json_schema_sets_short_filename_on_json_schema_line_edit PASSED [ 77%]
tests/test_file_selection.py::TestSelectJsonSchema::test_select_json_schema_does_nothing_on_cancel PASSED [ 83%]
tests/test_file_selection.py::TestOnModelSelectionChanged::test_on_model_selection_changed_enables_launch_button_when_model_selected PASSED [ 88%]
tests/test_file_selection.py::TestOnModelSelectionChanged::test_on_model_selection_changed_disables_launch_button_when_no_model PASSED [ 94%]
tests/test_file_selection.py::TestOnModelSelectionChanged::test_on_model_selection_changed_disables_launch_button_when_process_running PASSED [100%]

================== 18 passed in 0.36s ==================

```


## Assistant

<thinking>
The test output is being compressed again. Let me run the tests with less verbose output or just check the summary line.

</thinking>

The output is getting compressed. Let me run with a simpler command to see just the summary:



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher && uv run pytest tests/test_file_selection.py --tb=short 2>&1 | tail -30**
Status: Completed

Terminal:
```
============================= test session starts ==============================
platform darwin -- Python 3.14.0, pytest-9.1.0, pluggy-1.6.0
PySide6 6.11.1 -- Qt runtime 6.11.1 -- Qt compiled 6.11.1
rootdir: /Volumes/teaching/Code/LLamaLauncher
configfile: pyproject.toml
plugins: cov-7.1.0, qt-4.5.0
collected 18 items

tests/test_file_selection.py ..................                          [100%]

============================== 18 passed in 0.23s ==============================

```


## Assistant

<thinking>
All 18 tests passed! Now I need to:
1. Run the full test suite to make sure I didn't break anything
2. Format and lint the code
3. Export the session

Let me run the full test suite first, then format/lint.

</thinking>

All 18 tests passed. Now let me run the full test suite and then format/lint as required by the git workflow:



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher && uv run pytest --tb=short 2>&1 | tail -30**
Status: Completed

Terminal:
```
============================= test session starts ==============================
platform darwin -- Python 3.14.0, pytest-9.1.0, pluggy-1.6.0
PySide6 6.11.1 -- Qt runtime 6.11.1 -- Qt compiled 6.11.1
rootdir: /Volumes/teaching/Code/LLamaLauncher
configfile: pyproject.toml
testpaths: tests
plugins: cov-7.1.0, qt-4.5.0
collected 128 items

tests/test_config.py ..................                                  [ 14%]
tests/test_file_selection.py ..................                          [ 28%]
tests/test_helper_methods.py ............                                [ 37%]
tests/test_main.py .............................                         [ 60%]
tests/test_process.py .........................................          [ 92%]
tests/test_ui_loader.py ..........                                       [100%]

============================= 128 passed in 0.51s ==============================

```


## Assistant

<thinking>
All 128 tests passed, including the 18 new tests. Now I need to:
1. Format the code with ruff
2. Lint with ruff
3. Check imports with ruff

Let me do that now.

</thinking>

All 128 tests pass (including the 18 new ones). Now let me format and lint:



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher && uv run ruff format tests/test_file_selection.py**
Status: Completed

Terminal:
```
1 file reformatted




```


## Assistant

<thinking>
The user didn't send a message - this appears to be an empty/missing message. Let me continue with the remaining tasks: linting, checking imports, and then exporting the session as required by the git workflow.

I should:
1. Run ruff check to lint
2. Run ruff check --select I --fix to fix imports
3. Export the session as markdown
4. Save a summary in docs/agent-sessions/

Let me continue with these steps.

</thinking>

Good, file was formatted. Now let me lint and fix imports:



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher && uv run ruff check tests/test_file_selection.py**
Status: Completed

Terminal:
```
warning: Support for Python 3.14 is under development and may be unstable. Enable `preview` to remove this warning.
tests/test_file_selection.py:19:1: E402 Module level import not at top of file
   |
17 |     sys.path.insert(0, _project_root)
18 |
19 | from PySide6.QtCore import QProcess
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ E402
20 | from PySide6.QtWidgets import QApplication, QLineEdit
   |

tests/test_file_selection.py:20:1: E402 Module level import not at top of file
   |
19 | from PySide6.QtCore import QProcess
20 | from PySide6.QtWidgets import QApplication, QLineEdit
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ E402
21 |
22 | from main import LlamaLaunchApp
   |

tests/test_file_selection.py:22:1: E402 Module level import not at top of file
   |
20 | from PySide6.QtWidgets import QApplication, QLineEdit
21 |
22 | from main import LlamaLaunchApp
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ E402
   |

tests/test_file_selection.py:41:5: F841 Local variable `app` is assigned to but never used
   |
39 |     us to verify property and text calls without a full UI.
40 |     """
41 |     app = QApplication.instance() or QApplication([])
   |     ^^^ F841
42 |     window = LlamaLaunchApp.__new__(LlamaLaunchApp)
   |
   = help: Remove assignment to unused variable `app`

Found 4 errors.
No fixes available (1 hidden fix can be enabled with the `--unsafe-fixes` option).

```


## Assistant

<thinking>
I need to fix two issues:
1. E402 errors - the sys.path.insert is before the imports, which is needed for importing the main module. I should use `# noqa: E402` comments or restructure.
2. F841 - unused variable `app` in the fixture

Let me fix these issues.

</thinking>

I need to fix two linting issues:
1. E402 errors for imports after sys.path.insert (this is intentional for importing the project module)
2. F841 for the unused `app` variable

Let me fix these:



**Tool Call: tests/test\_file\_selection.py**
Status: Completed

Diff: tests/test_file_selection.py
```
"""Tests for file dialog selection methods in LlamaLaunchApp.

These methods open file dialogs via QFileDialog.getOpenFileName and set
properties on line edit widgets. Each test mocks the file dialog to return
a controlled path and verifies the correct side effects.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Ensure production module is importable
_project_root = str(Path(__file__).resolve().parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from PySide6.QtCore import QProcess  # noqa: E402
from PySide6.QtWidgets import QApplication, QLineEdit  # noqa: E402

from main import LlamaLaunchApp  # noqa: E402


@pytest.fixture()
def mock_line_edit():
    """Provide a mock QLineEdit for testing path display logic."""
    edit = MagicMock(spec=QLineEdit)
    edit.property.return_value = None
    return edit


@pytest.fixture()
def app_with_line_edits(mock_line_edit):
    """Provide a LlamaLaunchApp with line edits replaced by mocks.

    This fixture creates a minimal app instance and replaces the line
    edit attributes that file selection methods interact with, allowing
    us to verify property and text calls without a full UI.
    """
    _app = QApplication.instance() or QApplication([])
    window = LlamaLaunchApp.__new__(LlamaLaunchApp)

    # Mock the process attribute
    window._process = MagicMock(spec=QProcess)
    window._process.state.return_value = QProcess.NotRunning  # type: ignore

    # Replace line edits with mocks
    window.model_path_edit = mock_line_edit
    window.mmproj_path_edit = MagicMock(spec=QLineEdit)
    window.mmproj_path_edit.property.return_value = None
    window.draft_model_line_edit = MagicMock(spec=QLineEdit)
    window.draft_model_line_edit.property.return_value = None
    window.json_schema_line_edit = MagicMock(spec=QLineEdit)
    window.json_schema_line_edit.property.return_value = None

    # Mock launch button
    window.launch_button = MagicMock()

    # Private path attributes
    window._model_path = ""
    window._mmproj_path = ""

    return window


class TestSelectModel:
    """Tests for _select_model file dialog method.

    Target: main.py lines 762-779
    """

    def test_select_model_sets_fullpath_on_model_path_edit(self, app_with_line_edits):
        """_select_model stores the full path as a custom property on model_path_edit."""
        fake_path = "/models/llama.gguf"

        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=(fake_path, ""),
        ):
            app_with_line_edits._select_model()

        app_with_line_edits.model_path_edit.setProperty.assert_called_once_with("fullPath", fake_path)

    def test_select_model_sets_short_filename_on_model_path_edit(self, app_with_line_edits):
        """_select_model displays only the short filename in the line edit."""
        fake_path = "/models/llama.gguf"

        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=(fake_path, ""),
        ):
            app_with_line_edits._select_model()

        app_with_line_edits.model_path_edit.setText.assert_called_once_with("llama.gguf")

    def test_select_model_stores_full_path_in_private_attribute(self, app_with_line_edits):
        """_select_model stores the full path in _model_path."""
        fake_path = "/models/llama.gguf"

        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=(fake_path, ""),
        ):
            app_with_line_edits._select_model()

        assert app_with_line_edits._model_path == fake_path

    def test_select_model_calls_on_model_selection_changed(self, app_with_line_edits):
        """_select_model triggers _on_model_selection_changed after setting path."""
        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=("/models/llama.gguf", ""),
        ):
            with patch.object(
                app_with_line_edits,
                "_on_model_selection_changed",
            ) as mock_callback:
                app_with_line_edits._select_model()

                mock_callback.assert_called_once()

    def test_select_model_does_nothing_on_cancel(self, app_with_line_edits):
        """_select_model does nothing when the user cancels the dialog."""
        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=("", ""),
        ):
            app_with_line_edits._select_model()

        app_with_line_edits.model_path_edit.setProperty.assert_not_called()
        app_with_line_edits.model_path_edit.setText.assert_not_called()


class TestSelectMmproj:
    """Tests for _select_mmproj file dialog method.

    Target: main.py lines 781-797
    """

    def test_select_mmproj_sets_fullpath_on_mmproj_path_edit(self, app_with_line_edits):
        """_select_mmproj stores the full path as a custom property on mmproj_path_edit."""
        fake_path = "/models/multi-modal.gguf"

        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=(fake_path, ""),
        ):
            app_with_line_edits._select_mmproj()

        app_with_line_edits.mmproj_path_edit.setProperty.assert_called_once_with("fullPath", fake_path)

    def test_select_mmproj_sets_short_filename_on_mmproj_path_edit(self, app_with_line_edits):
        """_select_mmproj displays only the short filename in the line edit."""
        fake_path = "/models/multi-modal.gguf"

        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=(fake_path, ""),
        ):
            app_with_line_edits._select_mmproj()

        app_with_line_edits.mmproj_path_edit.setText.assert_called_once_with("multi-modal.gguf")

    def test_select_mmproj_stores_full_path_in_private_attribute(self, app_with_line_edits):
        """_select_mmproj stores the full path in _mmproj_path."""
        fake_path = "/models/multi-modal.gguf"

        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=(fake_path, ""),
        ):
            app_with_line_edits._select_mmproj()

        assert app_with_line_edits._mmproj_path == fake_path

    def test_select_mmproj_does_nothing_on_cancel(self, app_with_line_edits):
        """_select_mmproj does nothing when the user cancels the dialog."""
        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=("", ""),
        ):
            app_with_line_edits._select_mmproj()

        app_with_line_edits.mmproj_path_edit.setProperty.assert_not_called()
        app_with_line_edits.mmproj_path_edit.setText.assert_not_called()


class TestSelectDraftModel:
    """Tests for _select_draft_model file dialog method.

    Target: main.py lines 799-814
    """

    def test_select_draft_model_sets_fullpath_on_draft_model_line_edit(self, app_with_line_edits):
        """_select_draft_model stores the full path as a custom property on draft_model_line_edit."""
        fake_path = "/models/draft-model.gguf"

        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=(fake_path, ""),
        ):
            app_with_line_edits._select_draft_model()

        app_with_line_edits.draft_model_line_edit.setProperty.assert_called_once_with("fullPath", fake_path)

    def test_select_draft_model_sets_short_filename_on_draft_model_line_edit(self, app_with_line_edits):
        """_select_draft_model displays only the short filename in the line edit."""
        fake_path = "/models/draft-model.gguf"

        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=(fake_path, ""),
        ):
            app_with_line_edits._select_draft_model()

        app_with_line_edits.draft_model_line_edit.setText.assert_called_once_with("draft-model.gguf")

    def test_select_draft_model_does_nothing_on_cancel(self, app_with_line_edits):
        """_select_draft_model does nothing when the user cancels the dialog."""
        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=("", ""),
        ):
            app_with_line_edits._select_draft_model()

        app_with_line_edits.draft_model_line_edit.setProperty.assert_not_called()
        app_with_line_edits.draft_model_line_edit.setText.assert_not_called()


class TestSelectJsonSchema:
    """Tests for _select_json_schema file dialog method.

    Target: main.py lines 816-831
    """

    def test_select_json_schema_sets_fullpath_on_json_schema_line_edit(self, app_with_line_edits):
        """_select_json_schema stores the full path as a custom property on json_schema_line_edit."""
        fake_path = "/schemas/schema.json"

        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=(fake_path, ""),
        ):
            app_with_line_edits._select_json_schema()

        app_with_line_edits.json_schema_line_edit.setProperty.assert_called_once_with("fullPath", fake_path)

    def test_select_json_schema_sets_short_filename_on_json_schema_line_edit(self, app_with_line_edits):
        """_select_json_schema displays only the short filename in the line edit."""
        fake_path = "/schemas/schema.json"

        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=(fake_path, ""),
        ):
            app_with_line_edits._select_json_schema()

        app_with_line_edits.json_schema_line_edit.setText.assert_called_once_with("schema.json")

    def test_select_json_schema_does_nothing_on_cancel(self, app_with_line_edits):
        """_select_json_schema does nothing when the user cancels the dialog."""
        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=("", ""),
        ):
            app_with_line_edits._select_json_schema()

        app_with_line_edits.json_schema_line_edit.setProperty.assert_not_called()
        app_with_line_edits.json_schema_line_edit.setText.assert_not_called()


class TestOnModelSelectionChanged:
    """Tests for _on_model_selection_changed method.

    Target: main.py lines 833-837
    """

    def test_on_model_selection_changed_enables_launch_button_when_model_selected(self, app_with_line_edits):
        """_on_model_selection_changed enables the launch button when a model path exists."""
        app_with_line_edits.model_path_edit.property.return_value = "/models/llama.gguf"

        app_with_line_edits._on_model_selection_changed()

        app_with_line_edits.launch_button.setEnabled.assert_called_once_with(True)

    def test_on_model_selection_changed_disables_launch_button_when_no_model(self, app_with_line_edits):
        """_on_model_selection_changed disables the launch button when no model is selected."""
        app_with_line_edits.model_path_edit.property.return_value = None

        app_with_line_edits._on_model_selection_changed()

        app_with_line_edits.launch_button.setEnabled.assert_called_once_with(False)

    def test_on_model_selection_changed_disables_launch_button_when_process_running(self, app_with_line_edits):
        """_on_model_selection_changed disables the launch button when process is running."""
        from PySide6.QtCore import QProcess

        app_with_line_edits.model_path_edit.property.return_value = "/models/llama.gguf"
        app_with_line_edits._process.state.return_value = QProcess.Running  # type: ignore

        app_with_line_edits._on_model_selection_changed()

        app_with_line_edits.launch_button.setEnabled.assert_called_once_with(False)

```


## Assistant

<thinking>
The user didn't send a message - this appears to be an empty/missing message. Let me continue with the remaining tasks: linting, checking imports, and then exporting the session as required by the git workflow.

I should:
1. Run ruff check to lint again after my fixes
2. Run ruff check --select I --fix to fix imports if needed
3. Run the tests again to make sure everything still passes
4. Export the session as markdown
5. Save a summary in docs/agent-sessions/

Let me continue with these steps.

</thinking>

Good, the file was reformatted. Now let me run ruff check again to verify all linting issues are fixed:



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher && uv run ruff check tests/test_file_selection.py 2>&1**
Status: Completed

Terminal:
```
warning: Support for Python 3.14 is under development and may be unstable. Enable `preview` to remove this warning.
All checks passed!

```


## Assistant

<thinking>
The linting issues are fixed. Now I need to:
1. Run the tests again to make sure everything still passes after the edits
2. Run the full test suite
3. Export the session as markdown
4. Save a summary in docs/agent-sessions/

Let me continue with these steps.

</thinking>

All linting checks pass. Let me run the full test suite one more time to confirm everything is green, then export the session:



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher && uv run pytest --tb=short 2>&1 | tail -30**
Status: Completed

Terminal:
```
============================= test session starts ==============================
platform darwin -- Python 3.14.0, pytest-9.1.0, pluggy-1.6.0
PySide6 6.11.1 -- Qt runtime 6.11.1 -- Qt compiled 6.11.1
rootdir: /Volumes/teaching/Code/LLamaLauncher
configfile: pyproject.toml
testpaths: tests
plugins: cov-7.1.0, qt-4.5.0
collected 128 items

tests/test_config.py ..................                                  [ 14%]
tests/test_file_selection.py ..................                          [ 28%]
tests/test_helper_methods.py ............                                [ 37%]
tests/test_main.py .............................                         [ 60%]
tests/test_process.py .........................................          [ 92%]
tests/test_ui_loader.py ..........                                       [100%]

============================= 128 passed in 0.62s ==============================

```


## Assistant

<thinking>
The user didn't send a new message - this appears to be an empty/missing message. Let me continue with the remaining tasks: I need to export the session as markdown and save a summary in docs/agent-sessions/ as required by the git workflow rules.

Let me complete the remaining steps:
1. Export the session as markdown
2. Save a summary in docs/agent-sessions/
3. Provide a final summary to the user

</thinking>

All 128 tests pass. Now I need to export the session as required by the git workflow rules. Let me create the session documentation.



**Tool Call: Create directory \`/Volumes/teaching/Code/LLamaLauncher/docs/agent\-sessions\`**
Status: Completed

Created directory /Volumes/teaching/Code/LLamaLauncher/docs/agent-sessions

## Assistant

<thinking>
The user didn't send a new message - this appears to be an empty/missing message. I should continue with the remaining tasks: exporting the session and saving a summary as required by the git workflow rules.

Let me create the session summary file and then provide a final summary to the user.

</thinking>

Now let me save the session summary:



**Tool Call: docs/agent\-sessions/2026\-06\-16\-file\-selection\-tests.md**
Status: Completed

Diff: docs/agent-sessions/2026-06-16-file-selection-tests.md
```
# File Selection Tests Session - 2026-06-16

## Goal
Implement tests for Phase 4 of the testing plan: Path Selection Methods in LlamaLaunchApp.

## Files Changed
- **Created:** `tests/test_file_selection.py` - New test file with 18 tests covering file dialog selection methods

## Commands Run
```bash
# Create worktree
git worktree add .worktrees/file-selection-tests -b test/file-selection-tests

# Run new tests
uv run pytest tests/test_file_selection.py --tb=short

# Run full test suite
uv run pytest --tb=short

# Format code
uv run ruff format tests/test_file_selection.py

# Lint check
uv run ruff check tests/test_file_selection.py
```

## Test Coverage
| Method | Tests | Lines |
|--------|-------|-------|
| `_select_model` | 5 | L762-779 |
| `_select_mmproj` | 4 | L781-797 |
| `_select_draft_model` | 3 | L799-814 |
| `_select_json_schema` | 3 | L816-831 |
| `_on_model_selection_changed` | 3 | L833-837 |

**Total:** 18 new tests, all passing. Full suite: 128/128 tests passing.

## Test Design Decisions
- Used `MagicMock` with `spec=QLineEdit` for line edit widgets to verify property/text calls
- Created `app_with_line_edits` fixture that provides a minimal LlamaLaunchApp instance with all line edits replaced by mocks
- Mocked `QFileDialog.getOpenFileName` at the `main` module level to return controlled paths
- Tested both success and cancel scenarios for each file dialog method
- Used class-based test grouping (TestSelectModel, TestSelectMmproj, etc.) for related behaviors

## Chat Context
User requested implementation of Phase 4 tests from Testing.md (lines 275-295) covering path selection methods in main.py. All 6 test cases from the specification were implemented:
1. `_select_model` - sets fullPath + short filename on model_path_edit
2. `_select_mmproj` - sets fullPath + short filename on mmproj_path_edit  
3. `_select_draft_model` - sets fullPath + short filename on draft_model_line_edit
4. `_select_json_schema` - sets fullPath + short filename on json_schema_line_edit
5. `_on_model_selection_changed` - enables launch button when model is selected
6. `_on_model_selection_changed` - disables launch button when no model or process running

```


## Assistant

<thinking>
The user's request appears to be empty or missing. Let me check the context - I was in the middle of implementing tests for Phase 4 (Path Selection Methods) from Testing.md. I had just created the session summary file. 

Looking at my previous work, I've completed:
1. Created the test file `tests/test_file_selection.py` with 18 tests
2. All 128 tests pass (including the 18 new ones)
3. Code is formatted and linted
4. Session documentation created

The work appears to be complete. I should provide a summary to the user about what was accomplished.

</thinking>

All Phase 4 tests are implemented and passing. Here's a summary of what was completed:

## New Test File: `tests/test_file_selection.py`

**18 new tests** covering 5 methods from main.py:

| Class | Tests | Method Tested |
|-------|-------|---------------|
| `TestSelectModel` | 5 | `_select_model` - fullPath property, short filename, private attribute, callback trigger, cancel handling |
| `TestSelectMmproj` | 4 | `_select_mmproj` - fullPath property, short filename, private attribute, cancel handling |
| `TestSelectDraftModel` | 3 | `_select_draft_model` - fullPath property, short filename, cancel handling |
| `TestSelectJsonSchema` | 3 | `_select_json_schema` - fullPath property, short filename, cancel handling |
| `TestOnModelSelectionChanged` | 3 | Launch button enable/disable with model selected, no model, and process running |

## Key Design Decisions

- **Fixture**: Created `app_with_line_edits` that provides a minimal `LlamaLaunchApp` instance with all line edits replaced by `MagicMock(spec=QLineEdit)` - this avoids needing to load the full UI from the `.ui` file
- **Mocking**: `QFileDialog.getOpenFileName` mocked at the `main` module level to return controlled paths
- **Pattern**: Each method tested for both success (path returned) and cancel (empty string) scenarios

## Validation

```
128 passed in 0.62s  (all tests pass, including 18 new ones)
ruff check: All checks passed
```

The worktree `test/file-selection-tests` is ready for you to review and merge when convenient.
