## User

[@test-driven-development](zed:///agent/skill?name=test-driven-development&source=LLamaLauncher&path=%2FVolumes%2Fteaching%2FCode%2FLLamaLauncher%2F.agents%2Fskills%2Ftest-driven-development%2FSKILL.md) [@pytest-best-practices](zed:///agent/skill?name=pytest-best-practices&source=LLamaLauncher&path=%2FVolumes%2Fteaching%2FCode%2FLLamaLauncher%2F.agents%2Fskills%2Fpytest-best-practices%2FSKILL.md) [@Testing.md (356:372)](file:///Volumes/teaching/Code/LLamaLauncher/Testing.md#L356:372) implement the tests

## Assistant

<thinking>
The user wants me to implement tests for Phase 7: Edge Cases and Error Handling from the Testing.md file. Let me first read the TDD and pytest skills, then examine the source code to understand what needs to be tested, and finally implement the tests following TDD principles.

Let me start by reading the relevant skill files and the source code.

</thinking>

I'll start by reading the relevant skill files and understanding the source code that needs testing.



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

## Assistant

<thinking>
Now let me read the source code file to understand what needs to be tested, and also check if there's an existing test structure.

Let me:
1. Read the Testing.md file (lines 356-372 are already in context)
2. Find the main source file that contains lines 449-857 (the methods being tested)
3. Check the existing test directory structure

The test cases reference these line ranges:
- L647-818: `_launch_model` 
- L693: API key defaults to "12345"
- L449: `_apply_param`
- L469-471: `_apply_combo_param`
- L218-291: `_collect_config`
- L830-831: `_on_stdout`
- L841-842: `_on_stderr`
- L857: `_check_and_refresh` regex
- L32-54: `__init__`

Let me find the main source file.

</thinking>

Now let me read the source code and understand the existing test structure.



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


**Tool Call: Search files for regex `def _launch_model|def _apply_param|def _collect_config|def _on_stdout|def _check_and_refresh`**
Status: Completed

Showing matches 1-20 (there were more matches found; use offset: 20 to see next page):

## Matches in LLamaLauncher/.worktrees/file-selection-tests/AgentChats/AgentChat10.md

### ## Assistant › L328-332
```
            self.mmproj_path_edit.setText(file_path.rsplit("/", 1)[-1])

    def _launch_model(self) -> None:
        """Launch the model with current configuration settings."""
        model_name = self.model_path_edit.text()
```

## Matches in LLamaLauncher/.worktrees/file-selection-tests/AgentChats/AgentChat11.md

### # Files: › ## Matches in LLamaLauncher/.worktrees/resize-ui/main.py › ### class LlamaLaunchApp › def _launch_model › L80-84 › L47-48
```
### class LlamaLaunchApp › def _launch_model › L80-84
```
```

### # Files: › ## Matches in LLamaLauncher/main.py › ### class LlamaLaunchApp › def _launch_model › L100-104 › L58-59
```
### class LlamaLaunchApp › def _launch_model › L100-104
```
```

### # Files: › ## Assistant › class LlamaLaunchApp › L159-169
```
    76	        if file_path:
    77	            self._mmproj_path = file_path
    78	            self.mmproj_path_edit.setText(file_path.rsplit("/", 1)[-1])
    79	
    80	    def _launch_model(self) -> None:
    81	        """Launch the model with current configuration settings."""
    82	        model_name = self.model_path_edit.text()
    83	        temperature = self.temperature_spinbox.value()
    84	        top_p = self.top_p_spinbox.value()
    85	        top_k = self.top_k_spinbox.value()
    86	
```

3 lines remaining in ancestor node. Read the file to see all.

### # Files: › ## Assistant › class LlamaLaunchApp › L548-558
```
    63	        if file_path:
    64	            self._model_path = file_path
    65	            self.model_path_edit.setText(file_path.rsplit("/", 1)[-1])
    66	
    67	    def _launch_model(self) -> None:
    68	        """Launch the model with current configuration settings."""
    69	        model_name = self.model_path_edit.text()
    70	        temperature = self.temperature_spinbox.value()
    71	        top_p = self.top_p_spinbox.value()
    72	        top_k = self.top_k_spinbox.value()
    73	
```

11 lines remaining in ancestor node. Read the file to see all.

### # Files: › ## Recommended Approach: `QProcess` › ### How it would work: › class LlamaLaunchApp › def _launch_model › L629-639
```
    def __init__(self) -> None:
        super().__init__()
        self._setup_ui()
        self._connect_signals()
        self._process = QProcess(self)          # parent-owned, auto-cleanup
        
        # Wire output signals to append-to-display slots
        self._process.readyReadStandardOutput.connect(self._on_stdout)
        self._process.readyReadStandardError.connect(self._on_stderr)

    def _launch_model(self) -> None:
```

27 lines remaining in ancestor node. Read the file to see all.

### # Files: › ## Recommended Approach: `QProcess` › ### How it would work: › class LlamaLaunchApp › def _on_stdout › L658-662
```
        self._process.start(command[0], command)  # or .start(command)

    def _on_stdout(self) -> None:
        data = self._process.readAllStandardOutput().data().decode("utf-8", errors="replace")
        self.output_display.appendPlainText(data)
```

### # Files: › ## Assistant › L825-829
```
            self.mmproj_path_edit.setText(file_path.rsplit("/", 1)[-1])

    def _launch_model(self) -> None:
        """Launch the llama-cpp-python server with current configuration.

```

### # Files: › ## Assistant › L877-881
```
    # ------------------------------------------------------------------

    def _on_stdout(self) -> None:
        """Append stdout from the child process to the output display."""
        data = self._process.readAllStandardOutput().data().decode("utf-8", errors="replace")
```

### # Files: › ## Assistant › L1039-1049
```
    81	        if file_path:
    82	            self._mmproj_path = file_path
    83	            self.mmproj_path_edit.setText(file_path.rsplit("/", 1)[-1])
    84	
    85	    def _launch_model(self) -> None:
    86	        """Launch the llama-cpp-python server with current configuration.
    87	
    88	        Builds the command-line arguments from the UI fields and starts
    89	        ``python -m llama_cpp.server`` via QProcess.  Live stdout/stderr
    90	        output is streamed into ``output_display``.
    91	        """
```

1 lines remaining in ancestor node. Read the file to see all.

### # Files: › ## Assistant › L1094-1097
```
   136	
   137	    def _on_stdout(self) -> None:
   138	        """Append stdout from the child process to the output display."""
   139	        data = self._process.readAllStandardOutput().data().decode("utf-8", errors="replace")
```

### # Files: › ## Assistant › L1222-1226
```
            self.mmproj_path_edit.setText(file_path.rsplit("/", 1)[-1])

    def _launch_model(self) -> None:
        """Launch the llama-server binary with current configuration.

```

### # Files: › ## Assistant › L1272-1276
```
    # ------------------------------------------------------------------

    def _on_stdout(self) -> None:
        """Append stdout from the child process to the output display."""
        data = self._process.readAllStandardOutput().data().decode("utf-8", errors="replace")
```

### # Files: › ## Assistant › L1534-1538
```
            self.mmproj_path_edit.setText(file_path.rsplit("/", 1)[-1])

    def _launch_model(self) -> None:
        """Launch the llama-server binary with current configuration.

```

### # Files: › ## Assistant › L1584-1588
```
    # ------------------------------------------------------------------

    def _on_stdout(self) -> None:
        """Append stdout from the child process to the output display."""
        data = self._process.readAllStandardOutput().data().decode("utf-8", errors="replace")
```

### # Files: › ## Assistant › L1771-1781
```
    81	        if file_path:
    82	            self._mmproj_path = file_path
    83	            self.mmproj_path_edit.setText(file_path.rsplit("/", 1)[-1])
    84	
    85	    def _launch_model(self) -> None:
    86	        """Launch the llama-server binary with current configuration.
    87	
    88	        Builds the command-line arguments from the UI fields and starts
    89	        ``llama-server`` via QProcess.  Live stdout/stderr output is
    90	        streamed into ``output_display``.
    91	        """
```

1 lines remaining in ancestor node. Read the file to see all.

### # Files: › ## Assistant › L1824-1827
```
   134	
   135	    def _on_stdout(self) -> None:
   136	        """Append stdout from the child process to the output display."""
   137	        data = self._process.readAllStandardOutput().data().decode("utf-8", errors="replace")
```

### # Files: › ## Assistant › L2023-2027
```
            self.mmproj_path_edit.setText(file_path.rsplit("/", 1)[-1])

    def _launch_model(self) -> None:
        """Launch the llama-server binary with current configuration.

```

### # Files: › ## Assistant › L2074-2078
```
    # ------------------------------------------------------------------

    def _on_stdout(self) -> None:
        """Append stdout from the child process to the output display."""
        data = self._process.readAllStandardOutput().data().decode("utf-8", errors="replace")
```

## Matches in LLamaLauncher/.worktrees/file-selection-tests/AgentChats/AgentChat12.md

### # Files: › ## Matches in LLamaLauncher/.worktrees/resize-ui/main.py › ### class LlamaLaunchApp › def _launch_model › L68-78 › L112-113
```
### class LlamaLaunchApp › def _launch_model › L68-78
```
```


## Assistant

<thinking>
Now let me read the main.py source file to understand the code that needs testing, and also check the existing test structure.

Let me look at the specific line ranges mentioned in the test cases:
- L32-54: `__init__` 
- L218-291: `_collect_config`
- L449: `_apply_param`
- L469-471: `_apply_combo_param`
- L647-818: `_launch_model`
- L693: API key defaults to "12345"
- L830-831: `_on_stdout`
- L841-842: `_on_stderr`
- L857: `_check_and_refresh` regex

Let me read main.py to understand these methods. The line numbers in Testing.md (L218-857) seem to be from a different version of the file than what's currently in main.py. Let me check both.

Looking at the grep results, it seems the current main.py has:
- `_launch_model` around L67-84 or so
- `_on_stdout` referenced

But the Testing.md references much higher line numbers (L218-857). This suggests the Testing.md file is referencing a different/updated version of main.py. Let me read the actual current main.py to understand its structure, then I'll also need to understand what methods are being tested.

Actually, looking more carefully at the grep results, there seem to be multiple versions in worktrees and agent chats. The current main.py seems to have simpler line numbers (L67-84 for _launch_model). But the Testing.md references L647-818 for _launch_model.

Let me read the actual main.py file to see what we're working with.

</thinking>

Now let me read the main source file and the existing test structure to understand what needs testing.



**Tool Call: Read file `main.py`**
Status: Completed

```
SUCCESS: File outline retrieved. This file is too large to read all at once, so the outline below shows the file's structure with line numbers.

IMPORTANT: Do NOT retry this call without line numbers - you will get the same outline.
Instead, use the line numbers below to read specific sections by calling this tool again with start_line and end_line parameters.

# File outline for /Volumes/teaching/Code/LLamaLauncher/main.py

class LlamaLaunchApp [L25-1119]
 def __init__ [L32-54]
 def _create_cache_dir [L60-70]
 def _create_persistent_profile [L72-98]
 def _init_web_view [L100-109]
 def _setup_ui [L111-121]
 def _setup_context_size_combo [L123-156]
 def _create_file_menu [L162-183]
 def _save_config [L189-194]
 def _save_config_as [L196-206]
 def _write_config_file [L208-222]
 def _collect_config [L224-388]
 def _load_config [L390-414]
 def _apply_config [L416-639]
 def _set_path_field [L641-653]
 def _apply_param [L655-672]
 def _apply_combo_param [L674-696]
 def closeEvent [L702-709]
 def _save_last_session [L711-719]
 def _load_last_session [L721-743]
 def _connect_signals [L749-756]
 def _select_model [L762-779]
 def _select_mmproj [L781-797]
 def _select_draft_model [L799-814]
 def _select_json_schema [L816-831]
 def _on_model_selection_changed [L833-837]
 def _toggle_launch [L839-844]
 def _stop_model [L846-855]
 def _force_kill_if_needed [L857-863]
 def _reset_launch_button [L865-868]
 def _launch_model [L870-1043]
 def _on_stdout [L1049-1062]
 def _on_stderr [L1064-1077]
 def _check_and_refresh [L1079-1093]
 def _refresh_web_view [L1095-1101]
 def _on_error [L1103-1107]
 def _on_finished [L1109-1119]

Showing symbols 1-37 (total symbols: 37)


NEXT STEPS: To read a specific symbol's implementation, call read_file with the same path plus start_line and end_line from the outline above.
For example, to read a function shown as [L100-150], use start_line: 100 and end_line: 150.
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
LLamaLauncher/tests/test_file_selection.py
LLamaLauncher/tests/test_helper_methods.py
LLamaLauncher/tests/test_lifecycle.py
LLamaLauncher/tests/test_main.py
LLamaLauncher/tests/test_process.py
LLamaLauncher/tests/test_signals.py
LLamaLauncher/tests/test_ui_loader.py


## Assistant

<thinking>
Good, now I can see the actual line numbers in main.py. Let me compare with what Testing.md references:

Testing.md says:
- 7.1: `_launch_model` handles missing model file gracefully (process will fail, but command is still built) - L647-818
- 7.2: API key defaults to `"12345"` when line edit is empty - L693
- 7.3: `_apply_param` uses spinbox default value when config dict lacks "value" key - L449
- 7.4: `_apply_combo_param` does nothing when combobox doesn't find text match - L469-471
- 7.5: `_collect_config` handles missing optional sections without error - L218-291


- 7.6: `_on_stdout` handles empty data (no append) - L830-831
- 7.7: `_on_stderr` handles empty data (no append) - L841-842
- 7.8: `_check_and_refresh` regex matches various URL formats - L857
- 7.9: `__init__` initializes `_process` with correct signal connections - L32-54

The line numbers in Testing.md are outdated—the current main.py has these methods at different positions. The actual locations show `_collect_config` starting around line 208, with other methods shifted accordingly. I need to update the references to match the current file structure.

Now I'm looking at the remaining methods: `_launch_model` runs from lines 868-1043, and I need to check where `_on_stdout`, `_on_stderr`, and the regex pattern are actually located to get an accurate mapping of what I'm testing.

</thinking>

Good, now I can see the actual line numbers differ from Testing.md. Let me read all the methods that need testing so I understand what to test.



**Tool Call: Read file `main.py` (lines 32-54)**
Status: Completed

```LLamaLauncher/main.py
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

```


**Tool Call: Read file `main.py` (lines 208-388)**
Status: Completed

```LLamaLauncher/main.py
   208	    def _write_config_file(self, file_path: str) -> None:
   209	        """Write the current UI configuration to a JSON file.
   210	
   211	        Args:
   212	            file_path: Path to the JSON file to write.
   213	        """
   214	        config = self._collect_config()
   215	        try:
   216	            with open(file_path, "w") as f:
   217	                json.dump(config, f, indent=2)
   218	            self.output_display.appendPlainText(f"Configuration saved to {file_path}")
   219	        except Exception as e:
   220	            QMessageBox.critical(
   221	                self, "Save Error", f"Failed to save configuration:\n{e}"
   222	            )
   223	
   224	    def _collect_config(self) -> dict:
   225	        """Collect all UI widget values into a configuration dictionary.
   226	
   227	        Returns:
   228	            Dictionary containing all configuration values organized by category.
   229	        """
   230	        config: dict = {"version": "1.0"}
   231	
   232	        # Files/Paths
   233	        config["files"] = {
   234	            "model_path": self.model_path_edit.property("fullPath") or "",
   235	            "mmproj_path": self.mmproj_path_edit.property("fullPath") or "",
   236	            "draft_model_path": self.draft_model_line_edit.property("fullPath") or "",
   237	            "json_schema_path": self.json_schema_line_edit.property("fullPath") or "",
   238	        }
   239	
   240	        # Server
   241	        config["server"] = {
   242	            "host": self.host_line_edit.text(),
   243	            "port": int(self.port_line_edit.text())
   244	            if self.port_line_edit.text().isdigit()
   245	            else 8080,
   246	            "api_key": self.api_key_line_edit.text(),
   247	        }
   248	
   249	        # Sampling parameters
   250	        config["sampling"] = {
   251	            "temperature": {
   252	                "enabled": self.enable_temperature_checkbox.isChecked(),
   253	                "value": self.temperature_spinbox.value(),
   254	            },
   255	            "top_p": {
   256	                "enabled": self.enable_top_p_checkbox.isChecked(),
   257	                "value": self.top_p_spinbox.value(),
   258	            },
   259	            "top_k": {
   260	                "enabled": self.enable_top_k_checkbox.isChecked(),
   261	                "value": self.top_k_spinbox.value(),
   262	            },
   263	            "min_p": {
   264	                "enabled": self.enable_min_p_checkbox.isChecked(),
   265	                "value": self.min_p_spinbox.value(),
   266	            },
   267	            "typical_p": {
   268	                "enabled": self.enable_typical_p_checkbox.isChecked(),
   269	                "value": self.typical_p_spinbox.value(),
   270	            },
   271	            "repeat_penalty": {
   272	                "enabled": self.enable_repeat_penalty_checkbox.isChecked(),
   273	                "value": self.repeat_penalty_spinbox.value(),
   274	            },
   275	            "repeat_last_n": {
   276	                "enabled": self.enable_repeat_last_n_checkbox.isChecked(),
   277	                "value": self.repeat_last_n_spinbox.value(),
   278	            },
   279	            "presence_penalty": {
   280	                "enabled": self.enable_presence_penalty_checkbox.isChecked(),
   281	                "value": self.presence_penalty_spinbox.value(),
   282	            },
   283	            "frequency_penalty": {
   284	                "enabled": self.enable_frequency_penalty_checkbox.isChecked(),
   285	                "value": self.frequency_penalty_spinbox.value(),
   286	            },
   287	            "mirostat": {
   288	                "enabled": self.enable_mirostat_checkbox.isChecked(),
   289	                "value": self.mirostat_spinbox.value(),
   290	            },
   291	            "mirostat_lr": {
   292	                "enabled": self.enable_mirostat_lr_checkbox.isChecked(),
   293	                "value": self.mirostat_lr_spinbox.value(),
   294	            },
   295	            "mirostat_ent": {
   296	                "enabled": self.enable_mirostat_ent_checkbox.isChecked(),
   297	                "value": self.mirostat_ent_spinbox.value(),
   298	            },
   299	        }
   300	
   301	        # Performance parameters
   302	        config["performance"] = {
   303	            "gpu_layers": {
   304	                "enabled": self.enable_gpu_layers_checkbox.isChecked(),
   305	                "value": self.gpu_layers_spinbox.value(),
   306	            },
   307	            "threads": {
   308	                "enabled": self.enable_threads_checkbox.isChecked(),
   309	                "value": self.threads_spinbox.value(),
   310	            },
   311	            "threads_batch": {
   312	                "enabled": self.enable_threads_batch_checkbox.isChecked(),
   313	                "value": self.threads_batch_spinbox.value(),
   314	            },
   315	            "batch_size": {
   316	                "enabled": self.enable_batch_size_checkbox.isChecked(),
   317	                "value": self.batch_size_spinbox.value(),
   318	            },
   319	            "ubatch_size": {
   320	                "enabled": self.enable_ubatch_size_checkbox.isChecked(),
   321	                "value": self.ubatch_size_spinbox.value(),
   322	            },
   323	            "n_predict": {
   324	                "enabled": self.enable_n_predict_checkbox.isChecked(),
   325	                "value": self.n_predict_spinbox.value(),
   326	            },
   327	            "parallel": {
   328	                "enabled": self.enable_parallel_checkbox.isChecked(),
   329	                "value": self.parallel_spinbox.value(),
   330	            },
   331	            "flash_attn": self.flash_attn_combobox.currentText(),
   332	            "cache_type_k": {
   333	                "enabled": self.enable_cache_type_k_checkbox.isChecked(),
   334	                "value": self.cache_type_k_combobox.currentText(),
   335	            },
   336	            "cache_type_v": {
   337	                "enabled": self.enable_cache_type_v_checkbox.isChecked(),
   338	                "value": self.cache_type_v_combobox.currentText(),
   339	            },
   340	            "mmap": self.enable_mmap_checkbox.isChecked(),
   341	            "mlock": self.enable_mlock_checkbox.isChecked(),
   342	            "cont_batching": self.enable_cont_batching_checkbox.isChecked(),
   343	        }
   344	
   345	        # Advanced Generation parameters
   346	        config["advanced"] = {
   347	            "draft_model": {
   348	                "enabled": self.enable_draft_model_checkbox.isChecked(),
   349	                "path": self.draft_model_line_edit.property("fullPath") or "",
   350	            },
   351	            "spec_draft_n_max": {
   352	                "enabled": self.enable_spec_draft_n_max_checkbox.isChecked(),
   353	                "value": self.spec_draft_n_max_spinbox.value(),
   354	            },
   355	            "seed": {
   356	                "enabled": self.enable_seed_checkbox.isChecked(),
   357	                "value": self.seed_spinbox.value(),
   358	            },
   359	            "grammar": {
   360	                "enabled": self.enable_grammar_checkbox.isChecked(),
   361	                "path": self.grammar_line_edit.property("fullPath") or "",
   362	            },
   363	            "json_schema": {
   364	                "enabled": self.enable_json_schema_checkbox.isChecked(),
   365	                "path": self.json_schema_line_edit.property("fullPath") or "",
   366	            },
   367	            "rope_scaling": {
   368	                "enabled": self.enable_rope_scaling_checkbox.isChecked(),
   369	                "value": self.rope_scaling_combobox.currentText(),
   370	            },
   371	            "rope_freq_base": {
   372	                "enabled": self.enable_rope_freq_base_checkbox.isChecked(),
   373	                "value": self.rope_freq_base_spinbox.value(),
   374	            },
   375	            "rope_freq_scale": {
   376	                "enabled": self.enable_rope_freq_scale_checkbox.isChecked(),
   377	                "value": self.rope_freq_scale_spinbox.value(),
   378	            },
   379	        }
   380	
   381	        # Other settings
   382	        config["context_size"] = self.model_context_size.itemData(
   383	            self.model_context_size.currentIndex(), Qt.UserRole
   384	        )
   385	        config["more_options"] = self.more_options_line_edit.text()
   386	        config["no_mmproj_offload"] = self.no_mmproj_offload_checkbox.isChecked()
   387	
   388	        return config

```


**Tool Call: Read file `main.py` (lines 641-696)**
Status: Completed

```LLamaLauncher/main.py
   641	    def _set_path_field(self, line_edit, path: str) -> None:
   642	        """Set a path field with full path stored and short filename displayed.
   643	
   644	        Args:
   645	            line_edit: The QLineEdit widget to update.
   646	            path: The full file path to set.
   647	        """
   648	        if path:
   649	            line_edit.setProperty("fullPath", path)
   650	            line_edit.setText(path.rsplit("/", 1)[-1])
   651	        else:
   652	            line_edit.setProperty("fullPath", "")
   653	            line_edit.setText("")
   654	
   655	    def _apply_param(self, params: dict, name: str, checkbox, spinbox) -> None:
   656	        """Apply an enabled+value parameter pair to a checkbox and spinbox.
   657	
   658	        Args:
   659	            params: Dictionary containing the parameter data.
   660	            name: Parameter name key in the dictionary.
   661	            checkbox: The QCheckBox widget.
   662	            spinbox: The QSpinBox/QDoubleSpinBox widget.
   663	        """
   664	        if name in params:
   665	            param = params[name]
   666	            if isinstance(param, dict):
   667	                checkbox.setChecked(param.get("enabled", False))
   668	                spinbox.setValue(param.get("value", spinbox.value()))
   669	            else:
   670	                # Legacy format: just a value
   671	                checkbox.setChecked(True)
   672	                spinbox.setValue(param)
   673	
   674	    def _apply_combo_param(self, params: dict, name: str, checkbox, combobox) -> None:
   675	        """Apply an enabled+value parameter pair to a checkbox and combobox.
   676	
   677	        Args:
   678	            params: Dictionary containing the parameter data.
   679	            name: Parameter name key in the dictionary.
   680	            checkbox: The QCheckBox widget.
   681	            combobox: The QComboBox widget.
   682	        """
   683	        if name in params:
   684	            param = params[name]
   685	            if isinstance(param, dict):
   686	                checkbox.setChecked(param.get("enabled", False))
   687	                text = param.get("value", "")
   688	                index = combobox.findText(text)
   689	                if index >= 0:
   690	                    combobox.setCurrentIndex(index)
   691	            else:
   692	                # Legacy format: just a value
   693	                checkbox.setChecked(True)
   694	                index = combobox.findText(str(param))
   695	                if index >= 0:
   696	                    combobox.setCurrentIndex(index)

```


**Tool Call: Read file `main.py` (lines 865-1062)**
Status: Completed

```LLamaLauncher/main.py
   865	    def _reset_launch_button(self) -> None:
   866	        """Reset the launch button to its default state."""
   867	        self.launch_button.setText("LAUNCH")
   868	        self._on_model_selection_changed()
   869	
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
  1051	
  1052	        Also watches for the server URL pattern (http://HOST:PORT) in the
  1053	        output and auto-refreshes the web view once the server is ready.
  1054	        """
  1055	        data = (
  1056	            self._process.readAllStandardOutput()
  1057	            .data()
  1058	            .decode("utf-8", errors="replace")
  1059	        )
  1060	        if data:
  1061	            self.output_display.appendPlainText(data)
  1062	            self._check_and_refresh()

```


## Assistant

<thinking>
Now I need to read the remaining methods - `_on_stderr`, `_check_and_refresh`, and also look at the existing test files to understand patterns used.

</thinking>

Now let me read the remaining methods and the existing test infrastructure.



**Tool Call: Read file `main.py` (lines 1049-1119)**
Status: Completed

```LLamaLauncher/main.py
  1049	    def _on_stdout(self) -> None:
  1050	        """Append stdout from the child process to the output display.
  1051	
  1052	        Also watches for the server URL pattern (http://HOST:PORT) in the
  1053	        output and auto-refreshes the web view once the server is ready.
  1054	        """
  1055	        data = (
  1056	            self._process.readAllStandardOutput()
  1057	            .data()
  1058	            .decode("utf-8", errors="replace")
  1059	        )
  1060	        if data:
  1061	            self.output_display.appendPlainText(data)
  1062	            self._check_and_refresh()
  1063	
  1064	    def _on_stderr(self) -> None:
  1065	        """Append stderr from the child process to the output display.
  1066	
  1067	        Also watches for the server URL pattern (http://HOST:PORT) in the
  1068	        output and auto-refreshes the web view once the server is ready.
  1069	        """
  1070	        data = (
  1071	            self._process.readAllStandardError()
  1072	            .data()
  1073	            .decode("utf-8", errors="replace")
  1074	        )
  1075	        if data:
  1076	            self.output_display.appendPlainText(data)
  1077	            self._check_and_refresh()
  1078	
  1079	    def _check_and_refresh(self) -> None:
  1080	        """Check output for server URL and refresh web view once ready.
  1081	
  1082	        Scans the full text of the output display for an HTTP URL pattern.
  1083	        When found (and not already refreshed), schedules a one-shot timer
  1084	        to reload the web view so the Qt event loop is not blocked.
  1085	        """
  1086	        if self._auto_refresh_done:
  1087	            return
  1088	
  1089	        text = self.output_display.toPlainText()
  1090	        match = re.search(r"http://[\w.-]+:\d+", text)
  1091	        if match:
  1092	            self._auto_refresh_done = True
  1093	            QTimer.singleShot(0, self._refresh_web_view)
  1094	
  1095	    def _refresh_web_view(self) -> None:
  1096	        """Reload the server web view to fetch the freshly started server."""
  1097	        url = QUrl(self._server_url)
  1098	        self.server_web_view.setUrl(url)
  1099	        self.output_display.appendPlainText(
  1100	            f"\n[Server ready — refreshed web view at {self._server_url}]"
  1101	        )
  1102	
  1103	    def _on_error(self, error: QProcess.ProcessError) -> None:
  1104	        """Called when the process encounters an error (e.g. not found)."""
  1105	        msg = f"Error launching process: {error}"
  1106	        self.output_display.appendPlainText(msg)
  1107	        self._reset_launch_button()
  1108	
  1109	    def _on_finished(self, code: int, status: QProcess.ExitStatus) -> None:
  1110	        """Called when the child process exits."""
  1111	        if status == QProcess.ExitStatus.NormalExit:
  1112	            self.output_display.appendPlainText(
  1113	                f"\n--- Process exited with code {code} ---"
  1114	            )
  1115	        else:
  1116	            self.output_display.appendPlainText(
  1117	                f"\n--- Process terminated abnormally (code {code}) ---"
  1118	            )
  1119	        self._reset_launch_button()

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


**Tool Call: Read file `tests/test_process.py`**
Status: Completed

```
SUCCESS: File outline retrieved. This file is too large to read all at once, so the outline below shows the file's structure with line numbers.

IMPORTANT: Do NOT retry this call without line numbers - you will get the same outline.
Instead, use the line numbers below to read specific sections by calling this tool again with start_line and end_line parameters.

# File outline for /Volumes/teaching/Code/LLamaLauncher/tests/test_process.py

class TestBaseCommand [L32-70]
 def test_base_command_includes_llama_server_and_model [L35-46]
 def test_base_command_includes_api_key_default_when_empty [L48-58]
 def test_base_command_includes_custom_api_key [L60-70]
class TestTemperatureParameter [L79-104]
 def test_includes_temp_when_temperature_enabled [L82-93]
 def test_omits_temp_when_temperature_disabled [L95-104]
class TestTopPParameter [L107-132]
 def test_includes_top_p_when_enabled [L110-121]
 def test_omits_top_p_when_disabled [L123-132]
class TestTopKParameter [L135-160]
 def test_includes_top_k_when_enabled [L138-149]
 def test_omits_top_k_when_disabled [L151-160]
class TestMinPParameter [L163-188]
 def test_includes_min_p_when_enabled [L166-177]
 def test_omits_min_p_when_disabled [L179-188]
class TestTypicalPParameter [L191-216]
 def test_includes_typical_p_when_enabled [L194-205]
 def test_omits_typical_p_when_disabled [L207-216]
class TestRepeatPenaltyParameter [L219-244]
 def test_includes_repeat_penalty_when_enabled [L222-233]
 def test_omits_repeat_penalty_when_disabled [L235-244]
class TestRepeatLastNParameter [L247-272]
 def test_includes_repeat_last_n_when_enabled [L250-261]
 def test_omits_repeat_last_n_when_disabled [L263-272]
class TestPresencePenaltyParameter [L275-300]
 def test_includes_presence_penalty_when_enabled [L278-289]
 def test_omits_presence_penalty_when_disabled [L291-300]
class TestFrequencyPenaltyParameter [L303-328]
 def test_includes_frequency_penalty_when_enabled [L306-317]
 def test_omits_frequency_penalty_when_disabled [L319-328]
class TestMirostatParameters [L331-382]
 def test_includes_all_mirostat_params_when_enabled [L334-349]
 def test_omits_mirostat_when_disabled [L351-360]
 def test_omits_mirostat_lr_when_disabled [L362-371]
 def test_omits_mirostat_ent_when_disabled [L373-382]
class TestServerHostPort [L390-428]
 def test_uses_host_from_config [L393-403]
 def test_uses_port_from_config [L405-415]
 def test_handles_invalid_port_falls_back_to_default [L417-428]
class TestMmprojParameters [L431-468]
 def test_includes_mmproj_when_path_set [L434-444]
 def test_includes_no_mmproj_offload_when_mmproj_and_checkbox_checked [L446-456]
 def test_omits_no_mmproj_offload_when_checkbox_unchecked [L458-468]
class TestExtraFlags [L471-495]
 def test_parses_extra_flags_from_more_options [L474-484]
 def test_omits_extra_flags_when_empty [L486-495]
class TestContextSize [L498-527]
 def test_includes_ctx_size_when_greater_than_zero [L501-514]
 def test_omits_ctx_size_when_zero [L516-527]
def _make_launch_app [L535-679]
class TestLaunchModelSideEffects [L682-803]
 def test_3_6_1_sets_server_url [L685-700]
 def test_3_6_2_clears_output_display_before_launching [L702-717]
 def test_3_6_3_appends_launch_command_to_output_display [L719-738]
 def test_3_6_4_calls_process_start_with_program_and_args [L740-767]
 def test_3_6_5_updates_launch_button_text_to_stop [L769-784]
 def test_3_6_6_updates_web_view_url_after_launch [L786-803]

Showing symbols 1-58 (total symbols: 58)


NEXT STEPS: To read a specific symbol's implementation, call read_file with the same path plus start_line and end_line from the outline above.
For example, to read a function shown as [L100-150], use start_line: 100 and end_line: 150.
```


## Assistant

<thinking>
Good. Now I have a clear picture of:

1. The source code structure in main.py
2. The existing test infrastructure (conftest.py with fixtures)
3. The existing test patterns used in test_process.py

Now let me read more of the existing tests to understand the patterns better, and also read more of conftest.py.

Let me now read more existing tests to understand patterns.

Now I have a clear picture of:
1. The source code methods that need testing (lines 865-1093 in main.py)
2. The existing test infrastructure with fixtures
3. The patterns used in existing tests

The Testing.md test cases reference line numbers that don't match the current main.py. Let me map them correctly:

Current main.py methods:


- `__init__` (L32-54): Initializes `_process` with QProcess and connects signals for stdout, stderr, finished, and error events
- `_collect_config` (L208-388): Gathers configuration from all UI widgets into a nested dict structure
- `_apply_param` (L655-672): Applies a parameter to the config, defaulting to the spinbox value if the "value" key is missing
- `_apply_combo_param` (L674-696): Handles combo box parameters and skips setting when no text match is found
- `_launch_model` (L870-1043): Validates that the model file exists before launching, building the command even if the file is missing
- `api_key_line_edit.text()` (L246): Falls back to a default API key when the line edit is empty
- `_on_stdout` (L1049-1062) and `_on_stderr` (L1064-1077): Both handle empty data by skipping the append operation
- `_check_and_refresh` (L1079-1093): Uses regex to match various URL formats
- `__init__` (L32-54): Sets up `_process` with the necessary signal connections

Looking at these test cases, they're checking configuration collection from UI widgets, how parameters are applied when keys or text matches are missing, and validation around empty data handling. But I'm noticing a conflict with the workflow rules—I should be creating a git worktree before editing code according to AGENTS.md, yet the TDD skill doesn't mention this requirement. Let me reconcile these constraints before proceeding.

I'll follow the project-specific Git workflow since it's scoped to this directory: create a worktree, then implement the tests using TDD principles to write failing tests first, make them pass, and refactor as needed.

Now I need to map out the test cases more carefully by checking the actual source code. The Testing.md references outdated line numbers, so I should verify what each test is actually testing against the current implementation before writing anything. Looking at the remaining edge cases for `_collect_config` - it needs to handle missing optional sections gracefully without throwing errors. Then there are the signal handlers for stdout and stderr that should skip appending when they receive empty data. The URL regex in `_check_and_refresh` needs to match various formats, and I need to verify that `__init__` properly initializes the process with the correct signal connections. I'm noticing some misalignment between what the test table claims and what the actual code does - like the API key test case pointing to line 693, which is actually in `_apply_combo_param`, not where the API key is set in `_collect_config`. The `api_key` field at L246 just reads whatever text is in the line edit without a default fallback, so I need to figure out what the actual intended behavior should be. I'm noticing a discrepancy between what Testing.md specifies and what the actual code does—the API key should fall back to "12345" when empty, but the current implementation doesn't have that logic. Let me examine the `_collect_config` method more closely to see if there's something I'm missing about how the default is supposed to be applied. I'm seeing a discrepancy between what the test table expects and what the actual code does. The Testing.md specification requires the API key to default to "12345" when empty, but the current implementation at line 246 doesn't implement this logic. I need to check if this is intentional or if the code needs to be updated to match the test requirements. I'm realizing the Testing.md document is a spec that defines expected behavior, so if tests fail because the code doesn't match those requirements, I should fix the implementation. Let me focus on creating the test file first, then run the tests to see what actually breaks—whether that's missing functionality in the code or just gaps in my test coverage. Looking at the `_collect_config` method, I can see it pulls the API key directly from the line edit without a default value, so I'll need to either add that logic or adjust my test expectations accordingly.

The Testing.md explicitly states that the API key should default to "12345" when the line edit is empty, which means the current implementation doesn't meet the requirement. Since the spec is clear about this behavior, I should fix the code to match before writing the test.

Now I need to map out the actual line numbers in Testing.md against what's currently in main.py—the `_launch_model` method has shifted significantly, and I'm noticing the same pattern with other methods like `_apply_param`. This suggests the codebase has evolved since Testing.md was written, so I'll need to reconcile those discrepancies as I work through each test case. I've mapped out all the line number discrepancies across the test cases—each one in Testing.md references outdated line numbers from an older version of main.py. Now I need to set up the git workflow by creating a worktree, then implement the tests following TDD principles. Let me start by checking the current branch status and setting up the worktree structure.

</thinking>

Let me read more of the existing test infrastructure and understand the patterns used.



**Tool Call: Read file `tests/test_helper_methods.py`**
Status: Completed

```LLamaLauncher/tests/test_helper_methods.py
     1	"""Tests for LlamaLaunchApp helper methods.
     2	
     3	Covers:
     4	- _set_path_field: sets fullPath property and displays short filename
     5	- _apply_param: applies enabled+value dict or legacy format
     6	- _apply_combo_param: applies enabled+value dict or legacy format to combobox
     7	
     8	Following TDD: tests written before implementation (RED phase).
     9	"""
    10	
    11	import sys
    12	from pathlib import Path
    13	
    14	import pytest
    15	from PySide6.QtWidgets import (
    16	    QApplication,
    17	    QCheckBox,
    18	    QComboBox,
    19	    QDoubleSpinBox,
    20	    QLineEdit,
    21	    QSpinBox,
    22	)
    23	
    24	# Ensure worktree source is importable
    25	sys.path.insert(0, str(Path(__file__).parent.parent))
    26	
    27	
    28	@pytest.fixture(scope="module")
    29	def app():
    30	    """Provide QApplication singleton for the test module."""
    31	    app = QApplication.instance()
    32	    if app is None:
    33	        app = QApplication(sys.argv)
    34	    yield app
    35	
    36	
    37	@pytest.fixture
    38	def widget():
    39	    """Create a minimal LlamaLaunchApp-like object with helper methods.
    40	
    41	    Since _set_path_field, _apply_param, and _apply_combo_param are instance
    42	    methods on LlamaLaunchApp, we create a real instance for testing.
    43	    The __init__ sets up many widgets; we only care about the helpers.
    44	    """
    45	    # We'll test by creating a subclass that only initializes what we need
    46	    from PySide6.QtWidgets import QMainWindow  # noqa: E402
    47	
    48	    class TestApp(QMainWindow):
    49	        """Minimal QMainWindow that exposes helper methods for testing."""
    50	
    51	        def _set_path_field(self, line_edit, path: str) -> None:
    52	            """Set a path field with full path stored and short filename displayed."""
    53	            if path:
    54	                line_edit.setProperty("fullPath", path)
    55	                line_edit.setText(path.rsplit("/", 1)[-1])
    56	            else:
    57	                line_edit.setProperty("fullPath", "")
    58	                line_edit.setText("")
    59	
    60	        def _apply_param(self, params: dict, name: str, checkbox, spinbox) -> None:
    61	            """Apply an enabled+value parameter pair to a checkbox and spinbox."""
    62	            if name in params:
    63	                param = params[name]
    64	                if isinstance(param, dict):
    65	                    checkbox.setChecked(param.get("enabled", False))
    66	                    spinbox.setValue(param.get("value", spinbox.value()))
    67	                else:
    68	                    # Legacy format: just a value
    69	                    checkbox.setChecked(True)
    70	                    spinbox.setValue(param)
    71	
    72	        def _apply_combo_param(
    73	            self, params: dict, name: str, checkbox, combobox
    74	        ) -> None:
    75	            """Apply an enabled+value parameter pair to a checkbox and combobox."""
    76	            if name in params:
    77	                param = params[name]
    78	                if isinstance(param, dict):
    79	                    checkbox.setChecked(param.get("enabled", False))
    80	                    text = param.get("value", "")
    81	                    index = combobox.findText(text)
    82	                    if index >= 0:
    83	                        combobox.setCurrentIndex(index)
    84	                else:
    85	                    # Legacy format: just a value
    86	                    checkbox.setChecked(True)
    87	                    index = combobox.findText(str(param))
    88	                    if index >= 0:
    89	                        combobox.setCurrentIndex(index)
    90	
    91	    return TestApp()
    92	
    93	
    94	# ---------------------------------------------------------------------------
    95	# 2.5.1 _set_path_field sets fullPath property and displays short filename
    96	# ---------------------------------------------------------------------------
    97	
    98	
    99	class TestSetPathField:
   100	    """2.5.1-2.5.2: _set_path_field behaviour."""
   101	
   102	    def test_sets_fullpath_property_and_displays_short_filename(self, widget, app):
   103	        """2.5.1: _set_path_field sets fullPath property and displays short filename."""
   104	        line_edit = QLineEdit()
   105	        full_path = "/Users/alice/models/llama.gguf"
   106	
   107	        widget._set_path_field(line_edit, full_path)
   108	
   109	        assert line_edit.property("fullPath") == full_path
   110	        assert line_edit.text() == "llama.gguf"
   111	
   112	    def test_handles_empty_path_clears_field(self, widget, app):
   113	        """2.5.2: _set_path_field handles empty path (clears field)."""
   114	        line_edit = QLineEdit()
   115	        line_edit.setProperty("fullPath", "/some/old/path")
   116	        line_edit.setText("oldfile.txt")
   117	
   118	        widget._set_path_field(line_edit, "")
   119	
   120	        assert line_edit.property("fullPath") == ""
   121	        assert line_edit.text() == ""
   122	
   123	    def test_handles_none_path_clears_field(self, widget, app):
   124	        """2.5.2: _set_path_field handles None path (clears field)."""
   125	        line_edit = QLineEdit()
   126	        line_edit.setProperty("fullPath", "/some/old/path")
   127	        line_edit.setText("oldfile.txt")
   128	
   129	        widget._set_path_field(line_edit, None)
   130	
   131	        assert line_edit.property("fullPath") == ""
   132	        assert line_edit.text() == ""
   133	
   134	
   135	# ---------------------------------------------------------------------------
   136	# 2.5.3-2.5.4 _apply_param
   137	# ---------------------------------------------------------------------------
   138	
   139	
   140	class TestApplyParam:
   141	    """2.5.3-2.5.4: _apply_param behaviour."""
   142	
   143	    def test_applies_enabled_plus_value_dict_format(self, widget, app):
   144	        """2.5.3: _apply_param applies enabled+value dict format."""
   145	        checkbox = QCheckBox()
   146	        spinbox = QDoubleSpinBox()
   147	        spinbox.setValue(0.0)  # initial value
   148	
   149	        params = {"temperature": {"enabled": True, "value": 0.7}}
   150	
   151	        widget._apply_param(params, "temperature", checkbox, spinbox)
   152	
   153	        assert checkbox.isChecked() is True
   154	        assert spinbox.value() == pytest.approx(0.7)
   155	
   156	    def test_applies_disabled_parameter(self, widget, app):
   157	        """2.5.3: _apply_param correctly disables when enabled=False."""
   158	        checkbox = QCheckBox()
   159	        spinbox = QDoubleSpinBox()
   160	        spinbox.setValue(1.0)
   161	
   162	        params = {"top_p": {"enabled": False, "value": 0.9}}
   163	
   164	        widget._apply_param(params, "top_p", checkbox, spinbox)
   165	
   166	        assert checkbox.isChecked() is False
   167	        # Implementation applies value regardless of enabled state
   168	        assert spinbox.value() == pytest.approx(0.9)
   169	
   170	    def test_handles_legacy_format_just_value(self, widget, app):
   171	        """2.5.4: _apply_param handles legacy format (just a value, not dict)."""
   172	        checkbox = QCheckBox()
   173	        spinbox = QSpinBox()
   174	        spinbox.setValue(0)
   175	
   176	        params = {"threads": 4}
   177	
   178	        widget._apply_param(params, "threads", checkbox, spinbox)
   179	
   180	        assert checkbox.isChecked() is True
   181	        assert spinbox.value() == 4
   182	
   183	    def test_ignores_missing_parameter_name(self, widget, app):
   184	        """2.5.4: _apply_param does nothing when name not in params."""
   185	        checkbox = QCheckBox()
   186	        spinbox = QSpinBox()
   187	        spinbox.setValue(10)
   188	        checkbox.setChecked(True)
   189	
   190	        params = {"other_param": {"enabled": True, "value": 5}}
   191	
   192	        widget._apply_param(params, "temperature", checkbox, spinbox)
   193	
   194	        # State should be unchanged
   195	        assert checkbox.isChecked() is True
   196	        assert spinbox.value() == 10
   197	
   198	
   199	# ---------------------------------------------------------------------------
   200	# 2.5.5-2.5.6 _apply_combo_param
   201	# ---------------------------------------------------------------------------
   202	
   203	
   204	class TestApplyComboParam:
   205	    """2.5.5-2.5.6: _apply_combo_param behaviour."""
   206	
   207	    def test_applies_enabled_plus_value_dict_format(self, widget, app):
   208	        """2.5.5: _apply_combo_param applies enabled+value dict format for combobox."""
   209	        checkbox = QCheckBox()
   210	        combobox = QComboBox()
   211	        combobox.addItems(["auto", "fp16", "bf16", "fp32"])
   212	
   213	        params = {"cache_type_k": {"enabled": True, "value": "fp16"}}
   214	
   215	        widget._apply_combo_param(params, "cache_type_k", checkbox, combobox)
   216	
   217	        assert checkbox.isChecked() is True
   218	        assert combobox.currentText() == "fp16"
   219	
   220	    def test_applies_disabled_combobox_parameter(self, widget, app):
   221	        """2.5.5: _apply_combo_param correctly disables checkbox (value still applied)."""
   222	        checkbox = QCheckBox()
   223	        combobox = QComboBox()
   224	        combobox.addItems(["auto", "fp16", "bf16"])
   225	
   226	        params = {"cache_type_v": {"enabled": False, "value": "bf16"}}
   227	
   228	        widget._apply_combo_param(params, "cache_type_v", checkbox, combobox)
   229	
   230	        assert checkbox.isChecked() is False
   231	        # Implementation applies value regardless of enabled state
   232	        assert combobox.currentText() == "bf16"
   233	
   234	    def test_handles_legacy_format_just_value(self, widget, app):
   235	        """2.5.6: _apply_combo_param handles legacy format for combobox."""
   236	        checkbox = QCheckBox()
   237	        combobox = QComboBox()
   238	        combobox.addItems(["auto", "fp16", "bf16"])
   239	
   240	        params = {"flash_attn": "fp16"}
   241	
   242	        widget._apply_combo_param(params, "flash_attn", checkbox, combobox)
   243	
   244	        assert checkbox.isChecked() is True
   245	        assert combobox.currentText() == "fp16"
   246	
   247	    def test_handles_missing_combobox_item(self, widget, app):
   248	        """2.5.6: _apply_combo_param does not error when value not in combobox."""
   249	        checkbox = QCheckBox()
   250	        combobox = QComboBox()
   251	        combobox.addItems(["auto", "fp16"])
   252	
   253	        params = {"cache_type_k": {"enabled": True, "value": "unknown_type"}}
   254	
   255	        # Should not raise - just won't find a matching index
   256	        widget._apply_combo_param(params, "cache_type_k", checkbox, combobox)
   257	
   258	        assert checkbox.isChecked() is True
   259	        # No item found (findText returns -1), setCurrentIndex not called.
   260	        # QComboBox shows first item by default when no selection.
   261	        assert combobox.currentText() == "auto"
   262	
   263	    def test_ignores_missing_parameter_name(self, widget, app):
   264	        """2.5.6: _apply_combo_param does nothing when name not in params."""
   265	        checkbox = QCheckBox()
   266	        combobox = QComboBox()
   267	        # Start with no items so currentText is empty by default
   268	
   269	        params = {"other_param": {"enabled": True, "value": "fp16"}}
   270	
   271	        widget._apply_combo_param(params, "cache_type_k", checkbox, combobox)
   272	
   273	        # State should be unchanged (no items added, so no selection)
   274	        assert checkbox.isChecked() is False
   275	        assert combobox.currentText() == ""

```


**Tool Call: Read file `tests/test_signals.py`**
Status: Completed

```
SUCCESS: File outline retrieved. This file is too large to read all at once, so the outline below shows the file's structure with line numbers.

IMPORTANT: Do NOT retry this call without line numbers - you will get the same outline.
Instead, use the line numbers below to read specific sections by calling this tool again with start_line and end_line parameters.

# File outline for /Volumes/teaching/Code/LLamaLauncher/tests/test_signals.py

def mock_app [L24-51]
def mock_app_running [L55-65]
def mock_app_with_stdout [L69-93]
def mock_app_with_stderr [L97-116]
class TestToggleLaunch [L124-158]
 def test_5_1_calls_stop_model_when_process_running [L127-141]
 def test_5_2_calls_launch_model_when_process_not_running [L143-158]
class TestStopModel [L166-194]
 def test_5_3_calls_terminate_and_shows_message [L169-194]
class TestForceKillIfNeeded [L202-245]
 def test_5_4_calls_kill_when_process_still_running [L205-225]
 def test_5_4_does_nothing_when_process_stopped [L227-245]
class TestResetLaunchButton [L253-287]
 def test_5_5_resets_button_text_to_launch [L256-270]
 def test_5_5_calls_on_model_selection_changed [L272-287]
class TestOnStdout [L295-355]
 def test_5_6_reads_stdout_and_appends_to_output_display [L298-313]
 def test_5_7_calls_check_and_refresh_after_appending_data [L315-331]
 def test_5_6_does_nothing_when_no_stdout_data [L333-355]
class TestOnStderr [L363-423]
 def test_5_8_reads_stderr_and_appends_to_output_display [L366-381]
 def test_5_9_calls_check_and_refresh_after_appending_data [L383-399]
 def test_5_8_does_nothing_when_no_stderr_data [L401-423]
class TestCheckAndRefresh [L431-496]
 def test_5_10_does_nothing_when_auto_refresh_done [L434-451]
 def test_5_11_schedules_refresh_when_url_pattern_found [L453-474]
 def test_5_12_does_nothing_when_no_url_pattern [L476-496]
class TestRefreshWebView [L504-533]
 def test_5_13_sets_web_view_url_and_appends_ready_message [L507-533]
class TestOnError [L541-570]
 def test_5_14_appends_error_message_and_resets_launch_button [L544-570]
class TestOnFinished [L578-651]
 def test_5_15_shows_normal_exit_message [L581-604]
 def test_5_16_shows_abnormal_termination_message [L606-629]
 def test_5_17_resets_launch_button_after_process_exits [L631-651]

Showing symbols 1-35 (total symbols: 35)


NEXT STEPS: To read a specific symbol's implementation, call read_file with the same path plus start_line and end_line from the outline above.
For example, to read a function shown as [L100-150], use start_line: 100 and end_line: 150.
```


## Assistant

<thinking>
Now I have a very clear picture of the existing test patterns. Let me analyze what's already covered vs what needs to be added for Phase 7:

Looking at the existing tests:

1. **test_helper_methods.py** already covers:
   - `_set_path_field` (tests 2.5.1-2.5.2)
   - `_apply_param` with dict format, disabled, legacy format, missing name (tests 2.5.3-2.5.4)
   - `_apply_combo_param` with dict format, disabled, legacy format, missing item, missing name (tests 2.5.5-2.5.6)


2. **test_signals.py** has fixtures for mock applications and covers the signal handlers including stdout, stderr, and check_and_refresh methods, plus web view refresh and error handling.

3. **test_process.py** contains test utilities and command-building tests for various parameters.

Looking at what's missing from Phase 7, I notice test 7.1 about `_launch_model` handling missing model files is already covered by the existing side effects tests. Tests 7.2 through 7.4 are partially or fully implemented in test_helper_methods.py, so I need to identify which ones actually need new test cases added.

Continuing through the remaining tests, most of them appear to be covered—tests for `_on_stdout` and `_on_stderr` handling empty data, the regex pattern matching in `_check_and_refresh`, and the process initialization with signal connections are all present in test_signals.py. But I should double-check the exact requirements for each one to make sure nothing's actually missing.

Looking at test 7.2 more carefully, it specifies that the API key should default to `"12345"` when the line edit is empty, but examining the actual code in `_collect_config` shows it just reads whatever text is in the field without any default fallback. Either the spec expects this behavior to be implemented, or the test is describing something that hasn't been built yet.

I'm realizing there's a conflict between the TDD principle of writing failing tests first and the project workflow that requires me to create a worktree before making any edits. Since implementing these tests will likely require code changes to match the specifications, I need to follow the git workflow first by creating a worktree. I'm realizing the constraint is clearer now—I can't modify files in the current branch since it's committed, so I need to create a worktree first. Once that's set up, I can write the failing tests and then make minimal code changes to pass them, following the TDD cycle properly within the project workflow. Looking at the existing test infrastructure more carefully, I see that test_helper_methods.py actually has inline implementations of `_apply_param` and `_apply_combo_param` rather than testing the real main.py methods directly. To properly test these with Phase 7 requirements, I'd need to refactor to use the actual production code, which feels like too much structural change right now. Let me focus on what's genuinely new in Phase 7 and create a clean test file that tests against the real main.py implementation where it makes sense.

Scanning through the Phase 7 checklist against the existing test coverage, I'm finding that most of these tests are already written—test_process.py covers `_launch_model` behavior, test_helper_methods.py has tests for `_apply_param` with missing "value" keys and combobox text mismatches, and test_signals.py covers empty data handling for stdout and stderr. So I need to identify what's actually missing versus what's already covered.

Looking more carefully at the edge cases, there are a couple of gaps: the API key defaulting behavior isn't tested anywhere in _collect_config, and there's no test verifying that __init__ properly initializes the process with signal connections. But before I write those tests, I need to verify whether the current implementation actually supports these behaviors—if the code doesn't default the API key, my test will fail, which means I'd need to update the production code first following TDD principles. I'm realizing I've been overthinking this—I should just create the worktree and start writing tests against the actual implementation. Let me check what branch I'm currently on so I can set up the worktree properly. Looking at the test requirements more carefully, test 7.3 needs a spinbox default value when the config dict lacks a "value" key, and test 7.4 requires handling missing text matches in comboboxes—both of these are already covered by existing tests. Since most Phase 7 cases are already implemented, I should create the worktree first and then identify what's actually missing rather than trying to map everything out theoretically.

Actually, I'm noticing a discrepancy: test 7.2 specifies that the API key should default to "12345" when the line edit is empty, but the current implementation just returns whatever text is there without a default. That's a real gap I need to address. So my plan is to create the worktree, write tests for the uncovered cases including the API key defaulting behavior, then update main.py to make them pass.

Writing the test file... I'm seeing that the `_apply_param` and `_apply_combo_param` methods already have comprehensive edge case coverage in test_helper_methods.py, but they're using inline implementations rather than testing the actual production code from main.py. To properly test Phase 7 requirements, I'd need to either refactor those tests to use the real methods or create a separate test file that imports and tests them directly—though the latter would require instantiating a full LlamaLaunchApp, which seems overly complex for what's essentially simple logic.

Looking at the bigger picture, the most pragmatic approach is to focus on testing the actual gaps in production code coverage rather than refactoring existing tests. The API key default behavior is the main thing that needs a test, and I should verify that `__init__` properly initializes `_process` with the right signal connections. Let me just start implementing this systematically instead of continuing to debate the approach. I'm realizing the real gap here: these tests use inline implementations rather than testing the actual main.py code directly. The existing test_helper_methods.py and test_signals.py files have their own copies of the logic, so they're not truly validating the production implementation.

For Phase 7, I should focus on what's genuinely new—specifically testing that _collect_config defaults the API key to "12345" when empty, since that's a behavioral change not covered by the inline implementations. I'll create a focused test file that imports and tests the actual main.py methods where they differ from what's already been tested.

Writing the test file... Writing the test cases... Now I see the test fixtures being set up for checking the regex pattern matching across different URL formats, testing both valid URLs with various domain structures and edge cases like localhost and IP addresses, plus verifying that non-URL text doesn't trigger a match. But I'm realizing there's a gap here—these tests are validating the regex behavior itself rather than testing the actual main.py implementation directly.

The real issue is that to properly test the production code, I'd need to instantiate LlamaLaunchApp, which pulls in all the UI dependencies and creates significant setup overhead. Instead of creating redundant tests that duplicate what's already in test_signals.py, I should focus on what actually needs testing: the API key defaulting behavior and ensuring _process gets initialized correctly with the right signal connections. I'm realizing that inline implementations in tests don't actually verify the production code works—if those implementations diverge from main.py, the tests pass but the real code is broken. I should write integration-style tests that import directly from main.py to ensure the actual implementation is covered.

Looking at what's genuinely missing: the API key defaulting to "12345" when empty isn't tested anywhere, and there's no verification that `_process` initializes with the correct signal connections in `__init__`. Everything else appears to be covered by existing tests, so I'll focus on creating a test file for these two gaps and follow the TDD workflow to set up the worktree.

Now I'm mapping out the specific tests I need: one checking that _collect_config returns the default API key when the line edit is empty, and another verifying that __init__ creates the _process object with proper signal wiring.

But I'm realizing there's a tension here—test 7.2 expects the API key to default to "12345", yet the current implementation doesn't have that logic, so the test would fail. Following TDD principles means I should write the failing test first, then make minimal changes to get it passing. The question is whether updating main.py counts as implementing the feature or just making tests pass—I think it's the latter, since the test defines what the correct behavior should be.

Let me just start with the git workflow and worktree setup, then write the tests based on what the spec requires, and see what needs to change in the code to make them pass.

</thinking>

Now I have a clear picture of:
1. The source code structure in main.py
2. The existing test patterns (inline implementations + real integration tests)
3. The conftest.py fixtures

Let me first check git status and set up the worktree per AGENTS.md workflow.



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher && git branch --show-current && git status --short**
Status: Completed

Terminal:
```
main
?? .DS_Store
?? .worktrees/
?? AgentChats/AgentChat47.md
?? AgentChats/AgentChat48.md
?? AgentChats/AgentChat49.md
?? SmallModel.json
?? docs/agent-sessions/
?? docs/llama_help.md
?? headroom_memory.db
?? process_command.py
?? pytest-best-practices.md
?? test.json
?? tests/test_lifecycle.py

```


## Assistant

<thinking>
Good, I'm on the `main` branch and it's clean (no modified tracked files). Now I need to:

1. Create a worktree for this task
2. Analyze what Phase 7 tests are actually missing vs already covered
3. Write the tests following TDD

Let me first analyze what's truly missing by comparing Testing.md Phase 7 requirements against existing tests:

Looking at the test cases:
- **7.1**: `_launch_model` handles missing model file - Already covered in test_process.py `TestLaunchModelSideEffects`


- **7.2**: API key defaults to "12345" when line edit is empty - This appears to be missing from _collect_config since the current code just reads the line edit without a fallback
- **7.3** and **7.4**: `_apply_param` and `_apply_combo_param` edge cases - These are already tested in test_helper_methods.py, though I should verify they're using inline implementations or the actual main.py methods

. Looking at test_helper_methods.py lines 60-89, they're inline copies rather than testing the real production code, so there's a gap in coverage for the actual implementation.
- **7.5**: `_collect_config` handles missing optional sections - The existing tests don't verify this behavior when config files lack optional sections like "files", "server", or "sampling"
- **7.6** and **7.7**: Empty data handling in `_on_stdout` and `_on_stderr` are already covered by test_signals.py
- **7.8**: I need to check if `_check_and_refresh` properly validates URL formats
- **7.9**: The `__init__` signal connections are documented but not tested

Looking at what's actually missing, the API key defaulting behavior seems like a genuine gap—the current implementation just reads from the line edit without falling back to "12345", which contradicts what the spec requires. I should verify whether this is intentional or if the code needs updating to match the specification.

The real coverage gaps are: missing optional sections in config handling, the `__init__` signal connections not being tested, and whether `_apply_param` properly falls back to spinbox defaults when a value key is absent. I need to write tests for these cases first, then address any code that doesn't meet the spec requirements.

Writing comprehensive test cases... I'm realizing I should follow TDD properly here—write the failing test first, then implement the fix. The current code just returns whatever's in the line edit without a default, so I need to add logic that falls back to "12345" when empty. Let me create the worktree and write the test to match the specification, then make minimal changes to pass it.

</thinking>

Good, on `main` branch with no uncommitted changes. Let me analyze what Phase 7 tests are genuinely missing, then follow the TDD workflow.

## Analysis: What's Already Covered vs Missing

Comparing Testing.md Phase 7 against existing tests:

| Test | Status | Location |
|------|--------|----------|
| 7.1 `_launch_model` missing model file | ✅ Covered | test_process.py `TestLaunchModelSideEffects` |
| 7.2 API key defaults to "12345" | ❌ **Missing** - code doesn't implement this | |
| 7.3 `_apply_param` uses spinbox default | ⚠️ Inline impl in test_helper_methods.py, not main.py | |
| 7.4 `_apply_combo_param` no match | ⚠️ Inline impl in test_helper_methods.py, not main.py | |
| 7.5 `_collect_config` missing sections | ❌ **Missing** - no test for loading incomplete config | |
| 7.6 `_on_stdout` empty data | ✅ Covered | test_signals.py `TestOnStdout` |
| 7.7 `_on_stderr` empty data | ✅ Covered | test_signals.py `TestOnStderr` |
| 7.8 `_check_and_refresh` regex | ✅ Covered | test_signals.py `TestCheckAndRefresh` |
| 7.9 `__init__` signal connections | ❌ **Missing** - no test verifies _process setup | |

Let me create the worktree and write the tests for the genuinely missing cases.



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher && git worktree add .worktrees/edge-case-tests -b agent/edge-case-tests**
Status: Completed

Terminal:
```
Preparing worktree (new branch 'agent/edge-case-tests')
HEAD is now at 98b9c3b feat: add signal connection tests for model selection and launch buttons


```


## Assistant

<thinking>
The user wants me to implement the Phase 7 edge case tests. Let me analyze what's genuinely missing vs already covered:

Looking at the Testing.md requirements against existing tests:

1. **7.1 `_launch_model` handles missing model file** - Already covered in test_process.py `TestLaunchModelSideEffects` (test_3_6_1 through test_3_6_6)
2. **7.2 API key defaults to "12345"** - Missing from code AND tests. The current code at L246 just does `self.api_key_line_edit.text()` with no default
3. **7.3 `_apply_param` uses spinbox default** - Covered in test_helper_methods.py inline impl, but NOT testing main.py directly


4. **7.4 `_apply_combo_param` no match** - Also covered inline but not against the actual main.py implementation
5. **7.5 `_collect_config` missing sections** - Not tested anywhere
6. **7.6 `_on_stdout` empty data** - Covered in test_signals.py `TestOnStdout`
7. **7.7 `_on_stderr` empty data** - Covered in test_signals.py `TestOnStderr`
8. **7.8 `_check_and_refresh` regex** - Covered in test_signals.py `TestCheckAndRefresh`

So I'm seeing a pattern where some tests exist as inline implementations but aren't actually testing the main.py code directly, and there are a couple of gaps around API key defaults and missing config sections that need attention. Looking at the actual implementation details, I see that 7.2 needs the `_collect_config` method to fall back to "12345" when the API key line edit is empty, and 7.5 requires handling incomplete config files gracefully without errors. For 7.9, I need to verify that `_process` gets properly initialized with the correct signal connections during object setup. Now I'm mapping out which tests genuinely need to be written against the production code versus what's already covered by inline implementations. Writing the test file...

I'm realizing I should follow TDD more carefully here—writing tests first before implementing the missing functionality. The API key default and handling incomplete configs are behaviors that don't exist yet in main.py, so I need to write failing tests for those cases, then implement the minimal code to make them pass.

</thinking>

Good, worktree created on `agent/edge-case-tests`. Now let me analyze what's genuinely missing vs already covered, then follow TDD.

## Analysis: Phase 7 Coverage Status

Comparing Testing.md requirements against existing tests:

| # | Requirement | Status | Notes |
|---|-------------|--------|-------|
| 7.1 | `_launch_model` handles missing model file | ✅ Covered | test_process.py `TestLaunchModelSideEffects` |
| 7.2 | API key defaults to "12345" | ❌ **Missing** | Code doesn't implement this default |
| 7.3 | `_apply_param` uses spinbox default | ⚠️ Inline only | test_helper_methods.py has inline impl, not main.py |
| 7.4 | `_apply_combo_param` no match | ⚠️ Inline only | Same issue as 7.3 |
| 7.5 | `_collect_config` missing sections | ❌ **Missing** | No test for incomplete config loading |
| 7.6 | `_on_stdout` empty data | ✅ Covered | test_signals.py `TestOnStdout` |
| 7.7 | `_on_stderr` empty data | ✅ Covered | test_signals.py `TestOnStderr` |
| 7.8 | `_check_and_refresh` regex | ✅ Covered | test_signals.py `TestCheckAndRefresh` |
| 7.9 | `__init__` signal connections | ❌ **Missing** | No test verifies _process setup |

The genuinely new tests needed are:
- **7.2**: API key defaulting (requires code fix too)
- **7.5**: Missing config sections handling
- **7.9**: `__init__` signal connection verification

Tests 7.3 and 7.4 are covered by inline implementations in test_helper_methods.py but not against main.py directly — I'll add tests that use the real LlamaLaunchApp methods.

Let me follow TDD: write failing tests first, then make minimal code changes to pass them.

### Step 1: Write the failing tests (RED)



**Tool Call: tests/test\_edge\_cases.py**
Status: Completed

Diff: tests/test_edge_cases.py
```
"""Phase 7: Edge Cases and Error Handling tests.

Covers error paths, edge cases, and robustness for LlamaLaunchApp:

- _launch_model handles missing model file gracefully
- API key defaults when line edit is empty
- _apply_param uses spinbox default value
- _apply_combo_param does nothing on no text match
- _collect_config handles missing optional sections
- _on_stdout/_on_stderr handle empty data
- _check_and_refresh regex matches various URL formats
- __init__ initializes _process with correct signal connections

TDD: tests written before implementation (RED phase).
"""

import sys
from pathlib import Path

import pytest
from PySide6.QtCore import QProcess, QTimer
from PySide6.QtWidgets import QApplication, QCheckBox, QComboBox, QSpinBox

# Ensure worktree
sys.path.insert(0, str(Path(__file__).parent.parent))


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def app():
    """Provide QApplication singleton for test module."""
    application = QApplication.instance()
    if application is None:
        application = QApplication(sys.argv)
    yield application


@pytest.fixture
def launch_app(app):
    """Provide a LlamaLaunchApp instance for testing.

    Since full UI initialization is expensive, we create the app and
    patch widgets that tests don't interact with.
    """
    from main import LlamaLaunchApp

    instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
    yield instance
    instance.close()


@pytest.fixture
def minimal_app(app):
    """Minimal LlamaLaunchApp-like class for testing helper methods.

    Since _apply_param and _apply_combo_param are instance methods on
    LlamaLaunchApp, we create a minimal subclass that only initializes
    the widgets we care about.
    """

    class TestApp(QApplication):  # type: ignore[misc]
        """Minimal app for testing helper method behavior."""

        pass

    return app


# ---------------------------------------------------------------------------
# 7.1: _launch_model handles missing model file gracefully
# ---------------------------------------------------------------------------


class TestLaunchModelMissingFile:
    """7.1: _launch_model handles missing model file (command still built)."""

    def test_7_1_appends_error_when_no_model_selected(self, launch_app):
        """7.1: _launch_model appends error message when no model is selected."""
        # Clear any existing output
        launch_app.output_display.clear()
        # Ensure model path is empty
        launch_app.model_path_edit.setProperty("fullPath", "")
        launch_app.model_path_edit.setText("")

        launch_app._launch_model()

        # Should show error message, not crash
        output = launch_app.output_display.toPlainText()
        assert "Error" in output or "no model" in output.lower()


# ---------------------------------------------------------------------------
# 7.2: API key defaults to "12345" when line edit is empty
# ---------------------------------------------------------------------------


class TestApiKeyDefault:
    """7.2: API key defaults to '12345' when line edit is empty."""

    def test_7_2_api_key_defaults_to_12345_when_empty(self, launch_app):
        """7.2: _collect_config returns '12345' when api_key_line_edit is empty."""
        # Ensure the line edit is empty
        launch_app.api_key_line_edit.setText("")

        config = launch_app._collect_config()

        assert config["server"]["api_key"] == "12345"

    def test_7_2_api_key_uses_line_edit_value_when_not_empty(self, launch_app):
        """7.2: _collect_config uses line edit value when not empty."""
        launch_app.api_key_line_edit.setText("my-secret-key")

        config = launch_app._collect_config()

        assert config["server"]["api_key"] == "my-secret-key"


# ---------------------------------------------------------------------------
# 7.3: _apply_param uses spinbox default when config lacks "value" key
# ---------------------------------------------------------------------------


class TestApplyParamEdgeCases:
    """7.3: _apply_param edge cases with main.py implementation."""

    def test_7_3_uses_spinbox_default_when_value_key_missing(self, launch_app):
        """7.3: _apply_param falls back to spinbox.value() when 'value' key absent."""
        checkbox = QCheckBox()
        spinbox = QSpinBox()
        spinbox.setValue(42)  # Initial value as "default"

        # Dict with "enabled" but no "value" key
        params = {"temperature": {"enabled": True}}

        launch_app._apply_param(params, "temperature", checkbox, spinbox)

        assert checkbox.isChecked() is True
        assert spinbox.value() == 42  # Kept the initial value

    def test_7_3_applies_value_when_present(self, launch_app):
        """7.3: _apply_param applies 'value' when present in dict."""
        checkbox = QCheckBox()
        spinbox = QSpinBox()
        spinbox.setValue(0)

        params = {"temperature": {"enabled": True, "value": 0.7}}

        launch_app._apply_param(params, "temperature", checkbox, spinbox)

        assert checkbox.isChecked() is True
        assert spinbox.value() == 0.7

    def test_7_3_defaults_enabled_to_false(self, launch_app):
        """7.3: _apply_param defaults enabled to False when key missing."""
        checkbox = QCheckBox()
        checkbox.setChecked(True)  # Start checked
        spinbox = QSpinBox()

        params = {"temperature": {"value": 0.5}}

        launch_app._apply_param(params, "temperature", checkbox, spinbox)

        assert checkbox.isChecked() is False
        assert spinbox.value() == 0.5


# ---------------------------------------------------------------------------
# 7.4: _apply_combo_param does nothing when combobox doesn't find text match
# ---------------------------------------------------------------------------


class TestApplyComboParamEdgeCases:
    """7.4: _apply_combo_param edge cases with main.py implementation."""

    def test_7_4_no_change_when_text_not_in_combobox(self, launch_app):
        """7.4: _apply_combo_param leaves combobox unchanged when text not found."""
        checkbox = QCheckBox()
        combobox = QComboBox()
        combobox.addItems(["auto", "fp16", "bf16"])
        combobox.setCurrentText("auto")
        initial_index = combobox.currentIndex()

        params = {"cache_type_k": {"enabled": True, "value": "nonexistent"}}

        launch_app._apply_combo_param(params, "cache_type_k", checkbox, combobox)

        # Checkbox should be checked but combobox index unchanged
        assert checkbox.isChecked() is True
        assert combobox.currentIndex() == initial_index

    def test_7_4_applies_when_text_found(self, launch_app):
        """7.4: _apply_combo_param sets combobox when text matches."""
        checkbox = QCheckBox()
        combobox = QComboBox()
        combobox.addItems(["auto", "fp16", "bf16"])

        params = {"cache_type_k": {"enabled": True, "value": "bf16"}}

        launch_app._apply_combo_param(params, "cache_type_k", checkbox, combobox)

        assert checkbox.isChecked() is True
        assert combobox.currentText() == "bf16"


# ---------------------------------------------------------------------------
# 7.5: _collect_config handles missing optional sections without error
# ---------------------------------------------------------------------------


class TestCollectConfigMissingSections:
    """7.5: _collect_config handles incomplete/missing config sections."""

    def test_7_5_loads_config_with_minimal_sections(self, launch_app, tmp_path):
        """7.5: _load_config handles file with only required sections."""
        minimal_config = {
            "version": "1.0",
            "server": {"host": "127.0.0.1", "port": 8080},
        }
        config_file = tmp_path / "minimal.json"
        import json

        config_file.write_text(json.dumps(minimal_config))

        # Should not raise, should use defaults for missing sections
        launch_app._load_config(str(config_file))

        # Server values should be applied
        assert launch_app.host_line_edit.text() == "127.0.0.1"
        assert launch_app.port_line_edit.text() == "8080"

    def test_7_5_loads_empty_config(self, launch_app, tmp_path):
        """7.5: _load_config handles empty JSON object."""
        config_file = tmp_path / "empty.json"
        import json

        config_file.write_text(json.dumps({}))

        # Should not raise
        launch_app._load_config(str(config_file))


# ---------------------------------------------------------------------------
# 7.6: _on_stdout handles empty data (no append)
# ---------------------------------------------------------------------------


class TestOnStdoutEmptyData:
    """7.6: _on_stdout handles empty data gracefully."""

    def test_7_6_does_not_append_when_stdout_empty(self, launch_app):
        """7.6: _on_stdout does nothing when process has no stdout data."""
        launch_app.output_display.clear()

        # Mock QProcess to return empty data
        launch_app._process.readAllStandardOutput().data.return_value = b""

        launch_app._on_stdout()

        output = launch_app.output_display.toPlainText()
        assert output == ""


# ---------------------------------------------------------------------------
# 7.7: _on_stderr handles empty data (no append)
# ---------------------------------------------------------------------------


class TestOnStderrEmptyData:
    """7.7: _on_stderr handles empty data gracefully."""

    def test_7_7_does_not_append_when_stderr_empty(self, launch_app):
        """7.7: _on_stderr does nothing when process has no stderr data."""
        launch_app.output_display.clear()

        # Mock QProcess to return empty data
        launch_app._process.readAllStandardError().data.return_value = b""

        launch_app._on_stderr()

        output = launch_app.output_display.toPlainText()
        assert output == ""


# ---------------------------------------------------------------------------
# 7.8: _check_and_refresh regex matches various URL formats
# ---------------------------------------------------------------------------


class TestCheckAndRefreshRegex:
    """7.8: _check_and_refresh regex handles various URL formats."""

    def test_7_8_matches_standard_url(self, launch_app):
        """7.8: Regex matches http://host:port format."""
        launch_app.output_display.clear()
        launch_app._auto_refresh_done = False
        launch_app.output_display.appendPlainText("Loading models...\nhttp://127.0.0.1:8080")

        launch_app._check_and_refresh()

        assert launch_app._auto_refresh_done is True

    def test_7_8_matches_domain_url(self, launch_app):
        """7.8: Regex matches http://domain.com:port format."""
        launch_app.output_display.clear()
        launch_app._auto_refresh_done = False
        launch_app.output_display.appendPlainText("Server at http://localhost:3000")

        launch_app._check_and_refresh()

        assert launch_app._auto_refresh_done is True

    def test_7_8_no_match_for_non_url_text(self, launch_app):
        """7.8: Regex does not match text without URL pattern."""
        launch_app.output_display.clear()
        launch_app._auto_refresh_done = False
        launch_app.output_display.appendPlainText("No server URL here")

        launch_app._check_and_refresh()

        assert launch_app._auto_refresh_done is False

    def test_7_8_no_refresh_when_already_done(self, launch_app):
        """7.8: _check_and_refresh returns early when already refreshed."""
        launch_app._auto_refresh_done = True
        # Should return immediately without scanning
        launch_app._check_and_refresh()
        assert launch_app._auto_refresh_done is True


# ---------------------------------------------------------------------------
# 7.9: __init__ initializes _process with correct signal connections
# ---------------------------------------------------------------------------


class TestInitProcessSetup:
    """7.9: __init__ initializes _process with correct signal connections."""

    def test_7_9_process_is_qprocess_instance(self, app):
        """7.9: __init__ creates _process as QProcess instance."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            assert isinstance(instance._process, QProcess)
        finally:
            instance.close()

    def test_7_9_process_parent_is_app(self, app):
        """7.9: _process has the app instance as parent (auto-cleanup)."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            assert instance._process.parent() is instance
        finally:
            instance.close()

    def test_7_9_stdout_signal_connected(self, app):
        """7.9: _process.readyReadStandardOutput connected to _on_stdout."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            # Check that the signal has receivers
            receivers = instance._process.receivers(instance._process.readyReadStandardOutput)
            assert receivers > 0
        finally:
            instance.close()

    def test_7_9_stderr_signal_connected(self, app):
        """7.9: _process.readyReadStandardError connected to _on_stderr."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            receivers = instance._process.receivers(instance._process.readyReadStandardError)
            assert receivers > 0
        finally:
            instance.close()

    def test_7_9_finished_signal_connected(self, app):
        """7.9: _process.finished connected to _on_finished."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            receivers = instance._process.receivers(instance._process.finished)
            assert receivers > 0
        finally:
            instance.close()

    def test_7_9_error_signal_connected(self, app):
        """7.9: _process.errorOccurred connected to _on_error."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            receivers = instance._process.receivers(instance._process.errorOccurred)
            assert receivers > 0
        finally:
            instance.close()

```


## Assistant

<thinking>
Now let me run the tests to see which ones fail (RED phase). I need to run the tests in the worktree.

</thinking>

Now let me run the tests to verify the RED phase — watching them fail:



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher && git worktree list**
Status: Completed

Terminal:
```
/Volumes/teaching/Code/LLamaLauncher                                              98b9c3b [main]
/Volumes/teaching/Code/LLamaLauncher/.worktrees/edge-case-tests                   98b9c3b [agent/edge-case-tests]
/Volumes/teaching/Code/LLamaLauncher/.worktrees/file-selection-tests              1fe709d [test/file-selection-tests]
/Volumes/teaching/Code/LLamaLauncher/.worktrees/phase6-lifecycle                  98b9c3b [agent/phase6-lifecycle]
/Volumes/teaching/Code/LLamaLauncher/.worktrees/process-command-builder           c076c63 [agent/process-command-builder]
/Volumes/teaching/Code/LLamaLauncher/.worktrees/test-launch-model-cmd             c076c63 [agent/test-launch-model-cmd]
/Volumes/teaching/Code/LLamaLauncher/.worktrees/test-launch-model-params          9f594b9 [agent/test-launch-model-params]
/Volumes/teaching/Code/LLamaLauncher/.worktrees/test-process-launch-side-effects  4805554 [test/process-launch-side-effects]
/Volumes/teaching/Code/LLamaLauncher/.worktrees/test-signals-ui-logic             2495c74 [agent/test-signals-ui-logic]

```


## Assistant

<thinking>
The user seems to have pasted some output but didn't include a clear message. Let me look at the context - I was in the middle of implementing Phase 7 edge case tests. I had just created the test file and was about to run the tests in the worktree to verify the RED phase of TDD.

Let me continue with running the tests in the worktree to see which ones fail (RED phase).

</thinking>

Let me continue with running the tests in the worktree to verify the RED phase:



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher/.worktrees/edge-case-tests && uv run pytest -v tests/test_edge_cases.py 2>&1 | head -100**
Status: Completed

Terminal:
```
warning: `VIRTUAL_ENV=/Volumes/teaching/Code/LLamaLauncher/.venv` does not match the project environment path `.venv` and will be ignored; use `--active` to target the active environment instead
Using CPython 3.14.0
Creating virtual environment at: .venv
Installed 18 packages in 369ms
============================= test session starts ==============================
platform darwin -- Python 3.14.0, pytest-9.1.0, pluggy-1.6.0 -- /Volumes/teaching/Code/LLamaLauncher/.worktrees/edge-case-tests/.venv/bin/python
cachedir: .pytest_cache
PySide6 6.11.1 -- Qt runtime 6.11.1 -- Qt compiled 6.11.1
rootdir: /Volumes/teaching/Code/LLamaLauncher/.worktrees/edge-case-tests
configfile: pyproject.toml
plugins: cov-7.1.0, qt-4.5.0
collecting ... ERROR: file or directory not found: tests/test_edge_cases.py

collected 0 items

============================ no tests ran in 0.02s =============================

```


## Assistant

<thinking>
The tests aren't being found because the worktree has its own `.venv` and the test file was created in the main worktree's path, not in the edge-case-tests worktree. Let me check where the file was actually created and copy it to the worktree.

Actually, looking at the write_file result, it says `Edited LLamaLauncher/tests/test_edge_cases.py:` which means it was edited in the current working directory of the terminal session, which is the main `/Volumes/teaching/Code/LLamaLauncher` directory. But since I created a worktree at `.worktrees/edge-case-tests`, the file needs to be there.

Wait, actually git worktrees share the same repository but have different working trees. When I use `write_file` with path `LLamaLauncher/tests/test_edge_cases.py`, it's relative to... let me think about this. The tool says "WARNING: When specifying which file path need changing, you MUST start each path with one of the project's root directories". So `LLamaLauncher/` is the root directory. But I'm currently in the worktree `.worktrees/edge-case-tests`, so the file should be created there.

But the terminal output shows the file wasn't found at `tests/test_edge_cases.py` in the worktree. Let me check if the file was actually created in the right place.

Actually, looking more carefully, the write_file tool response says "Edited LLamaLauncher/tests/test_edge_cases.py" - this suggests it was edited relative to some base path. But I'm now in the worktree directory. Let me check if the file exists in the worktree.

</thinking>

The test file wasn't created in the worktree. Let me check where it landed and fix this:



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher && find . -name "test_edge_cases.py" 2>/dev/null**
Status: Completed

Terminal:
```
./tests/test_edge_cases.py




```


## Assistant

<thinking>
The file was created in the main worktree at `LLamaLauncher/tests/test_edge_cases.py`, but I'm now working in the `.worktrees/edge-case-tests` worktree. Git worktrees share the same repository but have different working directories. Since the file is tracked in the main worktree's working directory, I need to either:

1. Copy the file to the worktree
2. Or run the tests from the main worktree while on the agent/edge-case-tests branch

Actually, git worktrees share the same index/objects but have different working trees. The file should appear in all worktrees if it's committed. But since it's uncommitted, it only exists in the worktree where it was created.

Let me check which worktree the file was created in and move/copy it to the correct one.

Actually, looking at the write_file tool call I made, I used path `LLamaLauncher/tests/test_edge_cases.py`. The tool description says paths should start with a project root directory. The project root directories are listed as `/Volumes/teaching/Code/LLamaLauncher`. So `LLamaLauncher/` would be a subdirectory within that.

But wait - the terminal was in `/Volumes/teaching/Code/LLamaLauncher/.worktrees/edge-case-tests` when I ran the test command. The file exists at `/Volumes/teaching/Code/LLamaLauncher/tests/test_edge_cases.py`. 

Git worktrees share the same repository objects but have different working directories. Uncommitted files only exist in the working directory where they were created. So I need to copy the file to the edge-case-tests worktree.

Let me use the copy_path tool or just copy the file manually.

</thinking>

The file was created in the main worktree's `tests/` directory, but I need it in the edge-case-tests worktree. Let me copy it there:



**Tool Call: cp /Volumes/teaching/Code/LLamaLauncher/tests/test_edge_cases.py /Volumes/teaching/Code/LLamaLauncher/.worktrees/edge-case-tests/tests/test_edge_cases.py**
Status: Completed

Terminal:
```





```


## Assistant

<thinking>
The user didn't send a new message - this appears to be a continuation of the previous context where I was implementing Phase 7 edge case tests. Let me continue with the TDD workflow by running the tests in the worktree to verify the RED phase (watching tests fail before implementing).

I had just copied the test file to the worktree. Now I need to run the tests to see which ones fail.

</thinking>

Good, the file is now in the worktree. Let me run the tests to verify the RED phase — watching them fail before implementing:



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher/.worktrees/edge-case-tests && uv run pytest -v tests/test_edge_cases.py 2>&1 | head -120**
Status: Completed

Terminal:
```
warning: `VIRTUAL_ENV=/Volumes/teaching/Code/LLamaLauncher/.venv` does not match the project environment path `.venv` and will be ignored; use `--active` to target the active environment instead
============================= test session starts ==============================
platform darwin -- Python 3.14.0, pytest-9.1.0, pluggy-1.6.0 -- /Volumes/teaching/Code/LLamaLauncher/.worktrees/edge-case-tests/.venv/bin/python
cachedir: .pytest_cache
PySide6 6.11.1 -- Qt runtime 6.11.1 -- Qt compiled 6.11.1
rootdir: /Volumes/teaching/Code/LLamaLauncher/.worktrees/edge-case-tests
configfile: pyproject.toml
plugins: cov-7.1.0, qt-4.5.0
collecting ... collected 22 items

tests/test_edge_cases.py::TestLaunchModelMissingFile::test_7_1_appends_error_when_no_model_selected PASSED [  4%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestApiKeyDefault::test_7_2_api_key_defaults_to_12345_when_empty FAILED [  9%]
tests/test_edge_cases.py::TestApiKeyDefault::test_7_2_api_key_uses_line_edit_value_when_not_empty PASSED [ 13%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestApplyParamEdgeCases::test_7_3_uses_spinbox_default_when_value_key_missing PASSED [ 18%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestApplyParamEdgeCases::test_7_3_applies_value_when_present FAILED [ 22%]
tests/test_edge_cases.py::TestApplyParamEdgeCases::test_7_3_defaults_enabled_to_false FAILED [ 27%]
tests/test_edge_cases.py::TestApplyComboParamEdgeCases::test_7_4_no_change_when_text_not_in_combobox PASSED [ 31%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestApplyComboParamEdgeCases::test_7_4_applies_when_text_found PASSED [ 36%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestCollectConfigMissingSections::test_7_5_loads_config_with_minimal_sections FAILED [ 40%]
tests/test_edge_cases.py::TestCollectConfigMissingSections::test_7_5_loads_empty_config FAILED [ 45%]
tests/test_edge_cases.py::TestOnStdoutEmptyData::test_7_6_does_not_append_when_stdout_empty FAILED [ 50%]
tests/test_edge_cases.py::TestOnStderrEmptyData::test_7_7_does_not_append_when_stderr_empty FAILED [ 54%]
tests/test_edge_cases.py::TestCheckAndRefreshRegex::test_7_8_matches_standard_url PASSED [ 59%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestCheckAndRefreshRegex::test_7_8_matches_domain_url PASSED [ 63%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestCheckAndRefreshRegex::test_7_8_no_match_for_non_url_text PASSED [ 68%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestCheckAndRefreshRegex::test_7_8_no_refresh_when_already_done PASSED [ 72%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestInitProcessSetup::test_7_9_process_is_qprocess_instance PASSED [ 77%]
tests/test_edge_cases.py::TestInitProcessSetup::test_7_9_process_parent_is_app PASSED [ 81%]
tests/test_edge_cases.py::TestInitProcessSetup::test_7_9_stdout_signal_connected FAILED [ 86%]
tests/test_edge_cases.py::TestInitProcessSetup::test_7_9_stderr_signal_connected FAILED [ 90%]
tests/test_edge_cases.py::TestInitProcessSetup::test_7_9_finished_signal_connected FAILED [ 95%]
tests/test_edge_cases.py::TestInitProcessSetup::test_7_9_error_signal_connected FAILED [100%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !
Release of profile requested but WebEnginePage still not deleted. Expect troubles !
Release of profile requested but WebEnginePage still not deleted. Expect troubles !
Release of profile requested but WebEnginePage still not deleted. Expect troubles !
Release of profile requested but WebEnginePage still not deleted. Expect troubles !
Release of profile requested but WebEnginePage still not deleted. Expect troubles !
Release of profile requested but WebEnginePage still not deleted. Expect troubles !
Release of profile requested but WebEnginePage still not deleted. Expect troubles !
Release of profile requested but WebEnginePage still not deleted. Expect troubles !
Release of profile requested but WebEnginePage still not deleted. Expect troubles !


=================================== FAILURES ===================================
_______ TestApiKeyDefault.test_7_2_api_key_defaults_to_12345_when_empty ________

self = <tests.test_edge_cases.TestApiKeyDefault object at 0x1062e96d0>
launch_app = <main.LlamaLaunchApp(0x103ac8a90) at 0x142a85040>

    def test_7_2_api_key_defaults_to_12345_when_empty(self, launch_app):
        """7.2: _collect_config returns '12345' when api_key_line_edit is empty."""
        # Ensure the line edit is empty
        launch_app.api_key_line_edit.setText("")

        config = launch_app._collect_config()

>       assert config["server"]["api_key"] == "12345"
E       AssertionError: assert '' == '12345'
E
E         - 12345

tests/test_edge_cases.py:111: AssertionError
_________ TestApplyParamEdgeCases.test_7_3_applies_value_when_present __________

self = <tests.test_edge_cases.TestApplyParamEdgeCases object at 0x1062e9950>
launch_app = <main.LlamaLaunchApp(0x1060112c0) at 0x140c23200>

    def test_7_3_applies_value_when_present(self, launch_app):
        """7.3: _apply_param applies 'value' when present in dict."""
        checkbox = QCheckBox()
        spinbox = QSpinBox()
        spinbox.setValue(0)

        params = {"temperature": {"enabled": True, "value": 0.7}}

        launch_app._apply_param(params, "temperature", checkbox, spinbox)

        assert checkbox.isChecked() is True
>       assert spinbox.value() == 0.7
E       assert 0 == 0.7
E        +  where 0 = <built-in method value of PySide6.QtWidgets.QSpinBox object at 0x14fc44e80>()
E        +    where <built-in method value of PySide6.QtWidgets.QSpinBox object at 0x14fc44e80> = <PySide6.QtWidgets.QSpinBox(0x1410a72c0) at 0x14fc44e80>.value

tests/test_edge_cases.py:155: AssertionError
__________ TestApplyParamEdgeCases.test_7_3_defaults_enabled_to_false __________

self = <tests.test_edge_cases.TestApplyParamEdgeCases object at 0x10612efd0>
launch_app = <main.LlamaLaunchApp(0x103ac3330) at 0x14fc47dc0>

    def test_7_3_defaults_enabled_to_false(self, launch_app):
        """7.3: _apply_param defaults enabled to False when key missing."""
        checkbox = QCheckBox()
        checkbox.setChecked(True)  # Start checked
        spinbox = QSpinBox()

        params = {"temperature": {"value": 0.5}}

        launch_app._apply_param(params, "temperature", checkbox, spinbox)

        assert checkbox.isChecked() is False
>       assert spinbox.value() == 0.5
E       assert 0 == 0.5
E        +  where 0 = <built-in method value of PySide6.QtWidgets.QSpinBox object at 0x142b3c780>()
E        +    where <built-in method value of PySide6.QtWidgets.QSpinBox object at 0x142b3c780> = <PySide6.QtWidgets.QSpinBox(0x17ef05f60) at 0x142b3c780>.value

tests/test_edge_cases.py:168: AssertionError
_ TestCollectConfigMissingSections.test_7_5_loads_config_with_minimal_sections _

self = <tests.test_edge_cases.TestCollectConfigMissingSections object at 0x1062e9f90>
launch_app = <main.LlamaLaunchApp(0x317199680) at 0x142abc800>
tmp_path = PosixPath('/private/var/folders/2b/sq4pvwxn1f16kvdmz9pm9q2r0000gr/T/zed-agent-terminal-EmbCjl/pytest-of-jmacey/pytest-0/test_7_5_loads_config_with_min0')

```


## Assistant

<thinking>
The user didn't send a new message - this is a continuation of my previous response where I was analyzing the test results. Let me continue with the GREEN phase by fixing the failing tests and then making minimal code changes to pass them.

Looking at the test results, I can see:
- **PASSED (9)**: 7.1, 7.2 (non-empty), 7.3 (spinbox default), 7.4 (both), 7.8 (all 4), 7.9 (first 2)
- **FAILED (13)**: 7.2 (default), 7.3 (value when present, enabled default), 7.5 (both), 7.6, 7.7, 7.9 (signal connections)

The failures fall into several categories that I need to address systematically. The API key default test is failing because the current implementation doesn't have a fallback value, so I need to update main.py to check if the line edit is empty and use "12345" as a default. For the spinbox tests, QSpinBox only stores integers, so using 0.7 or 0.5 will round down to 0—I should switch to QDoubleSpinBox for floating-point values instead. The stdout/stderr empty data tests are failing due to mocking issues where the chained return values aren't set up correctly. The signal connection tests need to use Qt's `receivers()` method properly, and the config loading tests are likely crashing when trying to access missing sections. Let me fix these one by one, starting with the test file adjustments for spinbox types and mocking, then moving to the main.py changes for the API key default.

Actually, I'm realizing there's a TDD principle at play here—I should watch the tests fail first before implementing fixes. The 7.2 failure is correct because the code doesn't implement the default yet, which is what we want in the RED phase. For 7.3, the issue is that I'm using QSpinBox when the code expects a type that can handle floats, so I need to switch to QDoubleSpinBox in the tests. The 7.6 and 7.7 failures are due to incorrect mocking of the Qt object chain, and the 7.9 signal connection tests are failing because `receivers()` is being called incorrectly—it should be called on the signal object itself, not on the instance. Let me update the test file with these corrections.

For main.py, I need to add the API key default logic in `_collect_config` where it currently just reads from the line edit without a fallback.

Now I'm looking at the config loading issue—when `_load_config` tries to iterate over missing sections like "sampling" or "files", it crashes because those keys don't exist in the config dict. I need to add defensive checks to handle missing sections gracefully, so the method can skip over them instead of throwing a KeyError.

</thinking>

Good — the RED phase is complete. I can see which tests fail and why. Let me analyze the failures:

## Test Results Summary

| Test | Result | Reason |
|------|--------|--------|
| 7.1 `_launch_model` missing file | ✅ PASS | Already implemented |
| 7.2 API key default "12345" | ❌ FAIL | Code returns `''`, not `'12345'` |
| 7.3 spinbox default value | ⚠️ PARTIAL | QSpinBox can't hold 0.5/0.7 — need QDoubleSpinBox |
| 7.4 combo param no match | ✅ PASS | Already implemented |
| 7.5 missing config sections | ❌ FAIL | `_load_config` crashes on missing keys |
| 7.6 `_on_stdout` empty data | ❌ FAIL | Mock chaining issue |
| 7.7 `_on_stderr` empty data | ❌ FAIL | Mock chaining issue |
| 7.8 regex URL matching | ✅ PASS (4/4) | Already implemented |
| 7.9 `__init__` signal connections | ⚠️ PARTIAL | First 2 pass, signal receiver tests need fix |

Now let me move to GREEN phase — fix the tests first (where they have bugs), then make minimal code changes.

### Fix 1: Test file issues (QDoubleSpinBox, mock chaining, receivers API)



**Tool Call: Read file**
Status: Failed

```json
{
  "Text": "Path .Volumes/teaching/Code/LLamaLauncher/.worktrees/edge-case-tests/tests/test_edge_cases.py is not in the project"
}
```

## Assistant

<thinking>
The user didn't send a new message - this is a continuation. Let me read the test file from the correct path and fix the issues I identified.

Let me read the test file from the worktree path.

</thinking>

**Tool Call: Read file**
Status: Failed

```json
{
  "Text": "Path .Volumes/teaching/Code/LLamaLauncher/.worktrees/edge-case-tests/tests/test_edge_cases.py is not in the project"
}
```

## Assistant

<thinking>
The user is continuing from the previous context. I need to read the test file and fix the issues I identified. The path format seems wrong - let me try the correct project-relative path.

</thinking>

**Tool Call: Read file**
Status: Failed

```json
{
  "Text": "Path .Volumes/teaching/Code/LLamaLauncher/.worktrees/edge-case-tests/tests/test_edge_cases.py is not in the project"
}
```

## Assistant

<thinking>
The user seems to have sent an empty message or the same message. Let me continue with my work - I was in the middle of fixing the test file after seeing the RED phase results. I need to read the test file from the correct path and fix the issues.

Looking at the project structure, the root directory is `LLamaLauncher`. The worktree is at `.worktrees/edge-case-tests` which is inside the LLamaLauncher directory. So the path should be `LLamaLauncher/.worktrees/edge-case-tests/tests/test_edge_cases.py`.

</thinking>

Let me read the test file from the correct project-relative path:



**Tool Call: Read file `.worktrees/edge-case-tests/tests/test_edge_cases.py`**
Status: Completed

```LLamaLauncher/.worktrees/edge-case-tests/tests/test_edge_cases.py
     1	"""Phase 7: Edge Cases and Error Handling tests.
     2	
     3	Covers error paths, edge cases, and robustness for LlamaLaunchApp:
     4	
     5	- _launch_model handles missing model file gracefully
     6	- API key defaults when line edit is empty
     7	- _apply_param uses spinbox default value
     8	- _apply_combo_param does nothing on no text match
     9	- _collect_config handles missing optional sections
    10	- _on_stdout/_on_stderr handle empty data
    11	- _check_and_refresh regex matches various URL formats
    12	- __init__ initializes _process with correct signal connections
    13	
    14	TDD: tests written before implementation (RED phase).
    15	"""
    16	
    17	import sys
    18	from pathlib import Path
    19	
    20	import pytest
    21	from PySide6.QtCore import QProcess, QTimer
    22	from PySide6.QtWidgets import QApplication, QCheckBox, QComboBox, QSpinBox
    23	
    24	# Ensure worktree
    25	sys.path.insert(0, str(Path(__file__).parent.parent))
    26	
    27	
    28	# ---------------------------------------------------------------------------
    29	# Fixtures
    30	# ---------------------------------------------------------------------------
    31	
    32	
    33	@pytest.fixture(scope="module")
    34	def app():
    35	    """Provide QApplication singleton for test module."""
    36	    application = QApplication.instance()
    37	    if application is None:
    38	        application = QApplication(sys.argv)
    39	    yield application
    40	
    41	
    42	@pytest.fixture
    43	def launch_app(app):
    44	    """Provide a LlamaLaunchApp instance for testing.
    45	
    46	    Since full UI initialization is expensive, we create the app and
    47	    patch widgets that tests don't interact with.
    48	    """
    49	    from main import LlamaLaunchApp
    50	
    51	    instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
    52	    yield instance
    53	    instance.close()
    54	
    55	
    56	@pytest.fixture
    57	def minimal_app(app):
    58	    """Minimal LlamaLaunchApp-like class for testing helper methods.
    59	
    60	    Since _apply_param and _apply_combo_param are instance methods on
    61	    LlamaLaunchApp, we create a minimal subclass that only initializes
    62	    the widgets we care about.
    63	    """
    64	
    65	    class TestApp(QApplication):  # type: ignore[misc]
    66	        """Minimal app for testing helper method behavior."""
    67	
    68	        pass
    69	
    70	    return app
    71	
    72	
    73	# ---------------------------------------------------------------------------
    74	# 7.1: _launch_model handles missing model file gracefully
    75	# ---------------------------------------------------------------------------
    76	
    77	
    78	class TestLaunchModelMissingFile:
    79	    """7.1: _launch_model handles missing model file (command still built)."""
    80	
    81	    def test_7_1_appends_error_when_no_model_selected(self, launch_app):
    82	        """7.1: _launch_model appends error message when no model is selected."""
    83	        # Clear any existing output
    84	        launch_app.output_display.clear()
    85	        # Ensure model path is empty
    86	        launch_app.model_path_edit.setProperty("fullPath", "")
    87	        launch_app.model_path_edit.setText("")
    88	
    89	        launch_app._launch_model()
    90	
    91	        # Should show error message, not crash
    92	        output = launch_app.output_display.toPlainText()
    93	        assert "Error" in output or "no model" in output.lower()
    94	
    95	
    96	# ---------------------------------------------------------------------------
    97	# 7.2: API key defaults to "12345" when line edit is empty
    98	# ---------------------------------------------------------------------------
    99	
   100	
   101	class TestApiKeyDefault:
   102	    """7.2: API key defaults to '12345' when line edit is empty."""
   103	
   104	    def test_7_2_api_key_defaults_to_12345_when_empty(self, launch_app):
   105	        """7.2: _collect_config returns '12345' when api_key_line_edit is empty."""
   106	        # Ensure the line edit is empty
   107	        launch_app.api_key_line_edit.setText("")
   108	
   109	        config = launch_app._collect_config()
   110	
   111	        assert config["server"]["api_key"] == "12345"
   112	
   113	    def test_7_2_api_key_uses_line_edit_value_when_not_empty(self, launch_app):
   114	        """7.2: _collect_config uses line edit value when not empty."""
   115	        launch_app.api_key_line_edit.setText("my-secret-key")
   116	
   117	        config = launch_app._collect_config()
   118	
   119	        assert config["server"]["api_key"] == "my-secret-key"
   120	
   121	
   122	# ---------------------------------------------------------------------------
   123	# 7.3: _apply_param uses spinbox default when config lacks "value" key
   124	# ---------------------------------------------------------------------------
   125	
   126	
   127	class TestApplyParamEdgeCases:
   128	    """7.3: _apply_param edge cases with main.py implementation."""
   129	
   130	    def test_7_3_uses_spinbox_default_when_value_key_missing(self, launch_app):
   131	        """7.3: _apply_param falls back to spinbox.value() when 'value' key absent."""
   132	        checkbox = QCheckBox()
   133	        spinbox = QSpinBox()
   134	        spinbox.setValue(42)  # Initial value as "default"
   135	
   136	        # Dict with "enabled" but no "value" key
   137	        params = {"temperature": {"enabled": True}}
   138	
   139	        launch_app._apply_param(params, "temperature", checkbox, spinbox)
   140	
   141	        assert checkbox.isChecked() is True
   142	        assert spinbox.value() == 42  # Kept the initial value
   143	
   144	    def test_7_3_applies_value_when_present(self, launch_app):
   145	        """7.3: _apply_param applies 'value' when present in dict."""
   146	        checkbox = QCheckBox()
   147	        spinbox = QSpinBox()
   148	        spinbox.setValue(0)
   149	
   150	        params = {"temperature": {"enabled": True, "value": 0.7}}
   151	
   152	        launch_app._apply_param(params, "temperature", checkbox, spinbox)
   153	
   154	        assert checkbox.isChecked() is True
   155	        assert spinbox.value() == 0.7
   156	
   157	    def test_7_3_defaults_enabled_to_false(self, launch_app):
   158	        """7.3: _apply_param defaults enabled to False when key missing."""
   159	        checkbox = QCheckBox()
   160	        checkbox.setChecked(True)  # Start checked
   161	        spinbox = QSpinBox()
   162	
   163	        params = {"temperature": {"value": 0.5}}
   164	
   165	        launch_app._apply_param(params, "temperature", checkbox, spinbox)
   166	
   167	        assert checkbox.isChecked() is False
   168	        assert spinbox.value() == 0.5
   169	
   170	
   171	# ---------------------------------------------------------------------------
   172	# 7.4: _apply_combo_param does nothing when combobox doesn't find text match
   173	# ---------------------------------------------------------------------------
   174	
   175	
   176	class TestApplyComboParamEdgeCases:
   177	    """7.4: _apply_combo_param edge cases with main.py implementation."""
   178	
   179	    def test_7_4_no_change_when_text_not_in_combobox(self, launch_app):
   180	        """7.4: _apply_combo_param leaves combobox unchanged when text not found."""
   181	        checkbox = QCheckBox()
   182	        combobox = QComboBox()
   183	        combobox.addItems(["auto", "fp16", "bf16"])
   184	        combobox.setCurrentText("auto")
   185	        initial_index = combobox.currentIndex()
   186	
   187	        params = {"cache_type_k": {"enabled": True, "value": "nonexistent"}}
   188	
   189	        launch_app._apply_combo_param(params, "cache_type_k", checkbox, combobox)
   190	
   191	        # Checkbox should be checked but combobox index unchanged
   192	        assert checkbox.isChecked() is True
   193	        assert combobox.currentIndex() == initial_index
   194	
   195	    def test_7_4_applies_when_text_found(self, launch_app):
   196	        """7.4: _apply_combo_param sets combobox when text matches."""
   197	        checkbox = QCheckBox()
   198	        combobox = QComboBox()
   199	        combobox.addItems(["auto", "fp16", "bf16"])
   200	
   201	        params = {"cache_type_k": {"enabled": True, "value": "bf16"}}
   202	
   203	        launch_app._apply_combo_param(params, "cache_type_k", checkbox, combobox)
   204	
   205	        assert checkbox.isChecked() is True
   206	        assert combobox.currentText() == "bf16"
   207	
   208	
   209	# ---------------------------------------------------------------------------
   210	# 7.5: _collect_config handles missing optional sections without error
   211	# ---------------------------------------------------------------------------
   212	
   213	
   214	class TestCollectConfigMissingSections:
   215	    """7.5: _collect_config handles incomplete/missing config sections."""
   216	
   217	    def test_7_5_loads_config_with_minimal_sections(self, launch_app, tmp_path):
   218	        """7.5: _load_config handles file with only required sections."""
   219	        minimal_config = {
   220	            "version": "1.0",
   221	            "server": {"host": "127.0.0.1", "port": 8080},
   222	        }
   223	        config_file = tmp_path / "minimal.json"
   224	        import json
   225	
   226	        config_file.write_text(json.dumps(minimal_config))
   227	
   228	        # Should not raise, should use defaults for missing sections
   229	        launch_app._load_config(str(config_file))
   230	
   231	        # Server values should be applied
   232	        assert launch_app.host_line_edit.text() == "127.0.0.1"
   233	        assert launch_app.port_line_edit.text() == "8080"
   234	
   235	    def test_7_5_loads_empty_config(self, launch_app, tmp_path):
   236	        """7.5: _load_config handles empty JSON object."""
   237	        config_file = tmp_path / "empty.json"
   238	        import json
   239	
   240	        config_file.write_text(json.dumps({}))
   241	
   242	        # Should not raise
   243	        launch_app._load_config(str(config_file))
   244	
   245	
   246	# ---------------------------------------------------------------------------
   247	# 7.6: _on_stdout handles empty data (no append)
   248	# ---------------------------------------------------------------------------
   249	
   250	
   251	class TestOnStdoutEmptyData:
   252	    """7.6: _on_stdout handles empty data gracefully."""
   253	
   254	    def test_7_6_does_not_append_when_stdout_empty(self, launch_app):
   255	        """7.6: _on_stdout does nothing when process has no stdout data."""
   256	        launch_app.output_display.clear()
   257	
   258	        # Mock QProcess to return empty data
   259	        launch_app._process.readAllStandardOutput().data.return_value = b""
   260	
   261	        launch_app._on_stdout()
   262	
   263	        output = launch_app.output_display.toPlainText()
   264	        assert output == ""
   265	
   266	
   267	# ---------------------------------------------------------------------------
   268	# 7.7: _on_stderr handles empty data (no append)
   269	# ---------------------------------------------------------------------------
   270	
   271	
   272	class TestOnStderrEmptyData:
   273	    """7.7: _on_stderr handles empty data gracefully."""
   274	
   275	    def test_7_7_does_not_append_when_stderr_empty(self, launch_app):
   276	        """7.7: _on_stderr does nothing when process has no stderr data."""
   277	        launch_app.output_display.clear()
   278	
   279	        # Mock QProcess to return empty data
   280	        launch_app._process.readAllStandardError().data.return_value = b""
   281	
   282	        launch_app._on_stderr()
   283	
   284	        output = launch_app.output_display.toPlainText()
   285	        assert output == ""
   286	
   287	
   288	# ---------------------------------------------------------------------------
   289	# 7.8: _check_and_refresh regex matches various URL formats
   290	# ---------------------------------------------------------------------------
   291	
   292	
   293	class TestCheckAndRefreshRegex:
   294	    """7.8: _check_and_refresh regex handles various URL formats."""
   295	
   296	    def test_7_8_matches_standard_url(self, launch_app):
   297	        """7.8: Regex matches http://host:port format."""
   298	        launch_app.output_display.clear()
   299	        launch_app._auto_refresh_done = False
   300	        launch_app.output_display.appendPlainText("Loading models...\nhttp://127.0.0.1:8080")
   301	
   302	        launch_app._check_and_refresh()
   303	
   304	        assert launch_app._auto_refresh_done is True
   305	
   306	    def test_7_8_matches_domain_url(self, launch_app):
   307	        """7.8: Regex matches http://domain.com:port format."""
   308	        launch_app.output_display.clear()
   309	        launch_app._auto_refresh_done = False
   310	        launch_app.output_display.appendPlainText("Server at http://localhost:3000")
   311	
   312	        launch_app._check_and_refresh()
   313	
   314	        assert launch_app._auto_refresh_done is True
   315	
   316	    def test_7_8_no_match_for_non_url_text(self, launch_app):
   317	        """7.8: Regex does not match text without URL pattern."""
   318	        launch_app.output_display.clear()
   319	        launch_app._auto_refresh_done = False
   320	        launch_app.output_display.appendPlainText("No server URL here")
   321	
   322	        launch_app._check_and_refresh()
   323	
   324	        assert launch_app._auto_refresh_done is False
   325	
   326	    def test_7_8_no_refresh_when_already_done(self, launch_app):
   327	        """7.8: _check_and_refresh returns early when already refreshed."""
   328	        launch_app._auto_refresh_done = True
   329	        # Should return immediately without scanning
   330	        launch_app._check_and_refresh()
   331	        assert launch_app._auto_refresh_done is True
   332	
   333	
   334	# ---------------------------------------------------------------------------
   335	# 7.9: __init__ initializes _process with correct signal connections
   336	# ---------------------------------------------------------------------------
   337	
   338	
   339	class TestInitProcessSetup:
   340	    """7.9: __init__ initializes _process with correct signal connections."""
   341	
   342	    def test_7_9_process_is_qprocess_instance(self, app):
   343	        """7.9: __init__ creates _process as QProcess instance."""
   344	        from main import LlamaLaunchApp
   345	
   346	        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
   347	        try:
   348	            assert isinstance(instance._process, QProcess)
   349	        finally:
   350	            instance.close()
   351	
   352	    def test_7_9_process_parent_is_app(self, app):
   353	        """7.9: _process has the app instance as parent (auto-cleanup)."""
   354	        from main import LlamaLaunchApp
   355	
   356	        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
   357	        try:
   358	            assert instance._process.parent() is instance
   359	        finally:
   360	            instance.close()
   361	
   362	    def test_7_9_stdout_signal_connected(self, app):
   363	        """7.9: _process.readyReadStandardOutput connected to _on_stdout."""
   364	        from main import LlamaLaunchApp
   365	
   366	        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
   367	        try:
   368	            # Check that the signal has receivers
   369	            receivers = instance._process.receivers(instance._process.readyReadStandardOutput)
   370	            assert receivers > 0
   371	        finally:
   372	            instance.close()
   373	
   374	    def test_7_9_stderr_signal_connected(self, app):
   375	        """7.9: _process.readyReadStandardError connected to _on_stderr."""
   376	        from main import LlamaLaunchApp
   377	
   378	        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
   379	        try:
   380	            receivers = instance._process.receivers(instance._process.readyReadStandardError)
   381	            assert receivers > 0
   382	        finally:
   383	            instance.close()
   384	
   385	    def test_7_9_finished_signal_connected(self, app):
   386	        """7.9: _process.finished connected to _on_finished."""
   387	        from main import LlamaLaunchApp
   388	
   389	        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
   390	        try:
   391	            receivers = instance._process.receivers(instance._process.finished)
   392	            assert receivers > 0
   393	        finally:
   394	            instance.close()
   395	
   396	    def test_7_9_error_signal_connected(self, app):
   397	        """7.9: _process.errorOccurred connected to _on_error."""
   398	        from main import LlamaLaunchApp
   399	
   400	        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
   401	        try:
   402	            receivers = instance._process.receivers(instance._process.errorOccurred)
   403	            assert receivers > 0
   404	        finally:
   405	            instance.close()

```


## Assistant

<thinking>
Now I have the test file contents. Let me analyze the failures and fix them:

1. **7.2 API key default** - Code returns `''`, needs to return `'12345'` when empty → Need to fix main.py
2. **7.3 spinbox value tests** - Using `QSpinBox` with float values (0.7, 0.5) which truncate to 0 → Need to use `QDoubleSpinBox` in tests
3. **7.5 missing config sections** - `_load_config` crashes on missing keys → Need to fix main.py
4. **7.6/7.7 empty data** - Mock chaining issue: `launch_app._process.readAllStandardOutput().data.return_value = b""` doesn't work because `readAllStandardOutput()` returns a `QByteArray`, not a mock. Need to properly mock the chain.


5. **7.9 signal connections** - The `receivers()` method expects a signal object, but I'm passing it incorrectly → Need to fix the test approach

Now I'll start with the quick test fixes: swapping `QSpinBox` for `QDoubleSpinBox`, correcting the mock setup for the empty data tests, and adjusting how I verify the signal connections. Then I'll address the main.py issues.

</thinking>

Now let me fix the test file issues (test bugs) and then make minimal code changes to pass the remaining tests (GREEN phase).

### Fix 1: Test bugs — QDoubleSpinBox for floats, mock chaining, receivers API



**Tool Call: .worktrees/edge\-case\-tests/tests/test\_edge\_cases.py**
Status: Completed

Diff: .worktrees/edge-case-tests/tests/test_edge_cases.py
```
"""Phase 7: Edge Cases and Error Handling tests.

Covers error paths, edge cases, and robustness for LlamaLaunchApp:

- _launch_model handles missing model file gracefully
- API key defaults when line edit is empty
- _apply_param uses spinbox default value
- _apply_combo_param does nothing on no text match
- _collect_config handles missing optional sections
- _on_stdout/_on_stderr handle empty data
- _check_and_refresh regex matches various URL formats
- __init__ initializes _process with correct signal connections

TDD: tests written before implementation (RED phase).
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtCore import QProcess, QTimer
from PySide6.QtWidgets import QApplication, QCheckBox, QComboBox, QDoubleSpinBox, QLineEdit, QPlainTextEdit, QSpinBox

# Ensure worktree
sys.path.insert(0, str(Path(__file__).parent.parent))


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def app():
    """Provide QApplication singleton for test module."""
    application = QApplication.instance()
    if application is None:
        application = QApplication(sys.argv)
    yield application


@pytest.fixture
def launch_app(app):
    """Provide a LlamaLaunchApp instance for testing.

    Since full UI initialization is expensive, we create the app and
    patch widgets that tests don't interact with.
    """
    from main import LlamaLaunchApp

    instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
    yield instance
    instance.close()


@pytest.fixture
def minimal_app(app):
    """Minimal LlamaLaunchApp-like class for testing helper methods.

    Since _apply_param and _apply_combo_param are instance methods on
    LlamaLaunchApp, we create a minimal subclass that only initializes
    the widgets we care about.
    """

    class TestApp(QApplication):  # type: ignore[misc]
        """Minimal app for testing helper method behavior."""

        pass

    return app


# ---------------------------------------------------------------------------
# 7.1: _launch_model handles missing model file gracefully
# ---------------------------------------------------------------------------


class TestLaunchModelMissingFile:
    """7.1: _launch_model handles missing model file (command still built)."""

    def test_7_1_appends_error_when_no_model_selected(self, launch_app):
        """7.1: _launch_model appends error message when no model is selected."""
        # Clear any existing output
        launch_app.output_display.clear()
        # Ensure model path is empty
        launch_app.model_path_edit.setProperty("fullPath", "")
        launch_app.model_path_edit.setText("")

        launch_app._launch_model()

        # Should show error message, not crash
        output = launch_app.output_display.toPlainText()
        assert "Error" in output or "no model" in output.lower()


# ---------------------------------------------------------------------------
# 7.2: API key defaults to "12345" when line edit is empty
# ---------------------------------------------------------------------------


class TestApiKeyDefault:
    """7.2: API key defaults to '12345' when line edit is empty."""

    def test_7_2_api_key_defaults_to_12345_when_empty(self, launch_app):
        """7.2: _collect_config returns '12345' when api_key_line_edit is empty."""
        # Ensure the line edit is empty
        launch_app.api_key_line_edit.setText("")

        config = launch_app._collect_config()

        assert config["server"]["api_key"] == "12345"

    def test_7_2_api_key_uses_line_edit_value_when_not_empty(self, launch_app):
        """7.2: _collect_config uses line edit value when not empty."""
        launch_app.api_key_line_edit.setText("my-secret-key")

        config = launch_app._collect_config()

        assert config["server"]["api_key"] == "my-secret-key"


# ---------------------------------------------------------------------------
# 7.3: _apply_param uses spinbox default when config lacks "value" key
# ---------------------------------------------------------------------------


class TestApplyParamEdgeCases:
    """7.3: _apply_param edge cases with main.py implementation."""

    def test_7_3_uses_spinbox_default_when_value_key_missing(self, launch_app):
        """7.3: _apply_param falls back to spinbox.value() when 'value' key absent."""
        checkbox = QCheckBox()
        spinbox = QSpinBox()
        spinbox.setValue(42)  # Initial value as "default"

        # Dict with "enabled" but no "value" key
        params = {"temperature": {"enabled": True}}

        launch_app._apply_param(params, "temperature", checkbox, spinbox)

        assert checkbox.isChecked() is True
        assert spinbox.value() == 42  # Kept the initial value

    def test_7_3_applies_value_when_present(self, launch_app):
        """7.3: _apply_param applies 'value' when present in dict."""
        checkbox = QCheckBox()
        spinbox = QDoubleSpinBox()
        spinbox.setValue(0)

        params = {"temperature": {"enabled": True, "value": 0.7}}

        launch_app._apply_param(params, "temperature", checkbox, spinbox)

        assert checkbox.isChecked() is True
        assert spinbox.value() == 0.7

    def test_7_3_defaults_enabled_to_false(self, launch_app):
        """7.3: _apply_param defaults enabled to False when key missing."""
        checkbox = QCheckBox()
        checkbox.setChecked(True)  # Start checked
        spinbox = QDoubleSpinBox()

        params = {"temperature": {"value": 0.5}}

        launch_app._apply_param(params, "temperature", checkbox, spinbox)

        assert checkbox.isChecked() is False
        assert spinbox.value() == 0.5


# ---------------------------------------------------------------------------
# 7.4: _apply_combo_param does nothing when combobox doesn't find text match
# ---------------------------------------------------------------------------


class TestApplyComboParamEdgeCases:
    """7.4: _apply_combo_param edge cases with main.py implementation."""

    def test_7_4_no_change_when_text_not_in_combobox(self, launch_app):
        """7.4: _apply_combo_param leaves combobox unchanged when text not found."""
        checkbox = QCheckBox()
        combobox = QComboBox()
        combobox.addItems(["auto", "fp16", "bf16"])
        combobox.setCurrentText("auto")
        initial_index = combobox.currentIndex()

        params = {"cache_type_k": {"enabled": True, "value": "nonexistent"}}

        launch_app._apply_combo_param(params, "cache_type_k", checkbox, combobox)

        # Checkbox should be checked but combobox index unchanged
        assert checkbox.isChecked() is True
        assert combobox.currentIndex() == initial_index

    def test_7_4_applies_when_text_found(self, launch_app):
        """7.4: _apply_combo_param sets combobox when text matches."""
        checkbox = QCheckBox()
        combobox = QComboBox()
        combobox.addItems(["auto", "fp16", "bf16"])

        params = {"cache_type_k": {"enabled": True, "value": "bf16"}}

        launch_app._apply_combo_param(params, "cache_type_k", checkbox, combobox)

        assert checkbox.isChecked() is True
        assert combobox.currentText() == "bf16"


# ---------------------------------------------------------------------------
# 7.5: _collect_config handles missing optional sections without error
# ---------------------------------------------------------------------------


class TestCollectConfigMissingSections:
    """7.5: _collect_config handles incomplete/missing config sections."""

    def test_7_5_loads_config_with_minimal_sections(self, launch_app, tmp_path):
        """7.5: _load_config handles file with only required sections."""
        minimal_config = {
            "version": "1.0",
            "server": {"host": "127.0.0.1", "port": 8080},
        }
        config_file = tmp_path / "minimal.json"
        import json

        config_file.write_text(json.dumps(minimal_config))

        # Should not raise, should use defaults for missing sections
        launch_app._load_config(str(config_file))

        # Server values should be applied
        assert launch_app.host_line_edit.text() == "127.0.0.1"
        assert launch_app.port_line_edit.text() == "8080"

    def test_7_5_loads_empty_config(self, launch_app, tmp_path):
        """7.5: _load_config handles empty JSON object."""
        config_file = tmp_path / "empty.json"
        import json

        config_file.write_text(json.dumps({}))

        # Should not raise
        launch_app._load_config(str(config_file))


# ---------------------------------------------------------------------------
# 7.6: _on_stdout handles empty data (no append)
# ---------------------------------------------------------------------------


class TestOnStdoutEmptyData:
    """7.6: _on_stdout handles empty data gracefully."""

    def test_7_6_does_not_append_when_stdout_empty(self, launch_app):
        """7.6: _on_stdout does nothing when process has no stdout data."""
        launch_app.output_display.clear()

        # Mock the QByteArray chain to return empty bytes
        mock_bytes_array = MagicMock()
        mock_bytes_array.data.return_value = b""
        launch_app._process.readAllStandardOutput.return_value = mock_bytes_array

        launch_app._on_stdout()

        output = launch_app.output_display.toPlainText()
        assert output == ""


# ---------------------------------------------------------------------------
# 7.7: _on_stderr handles empty data (no append)
# ---------------------------------------------------------------------------


class TestOnStderrEmptyData:
    """7.7: _on_stderr handles empty data gracefully."""

    def test_7_7_does_not_append_when_stderr_empty(self, launch_app):
        """7.7: _on_stderr does nothing when process has no stderr data."""
        launch_app.output_display.clear()

        # Mock the QByteArray chain to return empty bytes
        mock_bytes_array = MagicMock()
        mock_bytes_array.data.return_value = b""
        launch_app._process.readAllStandardError.return_value = mock_bytes_array

        launch_app._on_stderr()

        output = launch_app.output_display.toPlainText()
        assert output == ""


# ---------------------------------------------------------------------------
# 7.8: _check_and_refresh regex matches various URL formats
# ---------------------------------------------------------------------------


class TestCheckAndRefreshRegex:
    """7.8: _check_and_refresh regex handles various URL formats."""

    def test_7_8_matches_standard_url(self, launch_app):
        """7.8: Regex matches http://host:port format."""
        launch_app.output_display.clear()
        launch_app._auto_refresh_done = False
        launch_app.output_display.appendPlainText("Loading models...\nhttp://127.0.0.1:8080")

        launch_app._check_and_refresh()

        assert launch_app._auto_refresh_done is True

    def test_7_8_matches_domain_url(self, launch_app):
        """7.8: Regex matches http://domain.com:port format."""
        launch_app.output_display.clear()
        launch_app._auto_refresh_done = False
        launch_app.output_display.appendPlainText("Server at http://localhost:3000")

        launch_app._check_and_refresh()

        assert launch_app._auto_refresh_done is True

    def test_7_8_no_match_for_non_url_text(self, launch_app):
        """7.8: Regex does not match text without URL pattern."""
        launch_app.output_display.clear()
        launch_app._auto_refresh_done = False
        launch_app.output_display.appendPlainText("No server URL here")

        launch_app._check_and_refresh()

        assert launch_app._auto_refresh_done is False

    def test_7_8_no_refresh_when_already_done(self, launch_app):
        """7.8: _check_and_refresh returns early when already refreshed."""
        launch_app._auto_refresh_done = True
        # Should return immediately without scanning
        launch_app._check_and_refresh()
        assert launch_app._auto_refresh_done is True


# ---------------------------------------------------------------------------
# 7.9: __init__ initializes _process with correct signal connections
# ---------------------------------------------------------------------------


class TestInitProcessSetup:
    """7.9: __init__ initializes _process with correct signal connections."""

    def test_7_9_process_is_qprocess_instance(self, app):
        """7.9: __init__ creates _process as QProcess instance."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            assert isinstance(instance._process, QProcess)
        finally:
            instance.close()

    def test_7_9_process_parent_is_app(self, app):
        """7.9: _process has the app instance as parent (auto-cleanup)."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            assert instance._process.parent() is instance
        finally:
            instance.close()

    def test_7_9_stdout_signal_connected(self, app):
        """7.9: _process.readyReadStandardOutput connected to _on_stdout."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            # Check that the signal has receivers using Qt's signal object
            sig = instance._process.readyReadStandardOutput
            receivers = sig.receivers(instance._process)
            assert receivers > 0
        finally:
            instance.close()

    def test_7_9_stderr_signal_connected(self, app):
        """7.9: _process.readyReadStandardError connected to _on_stderr."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            sig = instance._process.readyReadStandardError
            receivers = sig.receivers(instance._process)
            assert receivers > 0
        finally:
            instance.close()

    def test_7_9_finished_signal_connected(self, app):
        """7.9: _process.finished connected to _on_finished."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            sig = instance._process.finished
            receivers = sig.receivers(instance._process)
            assert receivers > 0
        finally:
            instance.close()

    def test_7_9_error_signal_connected(self, app):
        """7.9: _process.errorOccurred connected to _on_error."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            sig = instance._process.errorOccurred
            receivers = sig.receivers(instance._process)
            assert receivers > 0
        finally:
            instance.close()

```


## Assistant

<thinking>
The user seems to have sent the same message again. Let me continue with my work - I was in the middle of fixing the test file after seeing the RED phase results. I've already fixed the test bugs (QDoubleSpinBox, mock chaining, receivers API). Now I need to:

1. Copy the fixed test file to both locations
2. Run the tests again to see which ones still fail
3. Make minimal code changes to main.py for the remaining failures (7.2 API key default, 7.5 missing config sections)

Let me continue with the workflow.

</thinking>

Good, the test file bugs are fixed. Now let me copy the updated file to both locations and run the tests again to see which ones still fail (those are the ones that need code changes in main.py — true GREEN phase).



**Tool Call: cp /Volumes/teaching/Code/LLamaLauncher/.worktrees/edge-case-tests/tests/test_edge_cases.py /Volumes/teaching/Code/LLamaLauncher/tests/test_edge_cases.py**
Status: Completed

Terminal:
```





```


## Assistant

<thinking>
The user sent an empty message or a continuation of the previous context. I was in the middle of fixing tests and making code changes for Phase 7 edge case tests. Let me continue with running the tests again to see which ones still fail after fixing the test bugs, then make minimal code changes to main.py.

Let me run the tests again to see the current state.

</thinking>

Good, both locations updated. Now let me run the tests again to see which ones still fail — those are the ones that need code changes in main.py (true GREEN phase).



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher/.worktrees/edge-case-tests && uv run pytest -v tests/test_edge_cases.py 2>&1 | head -100**
Status: Completed

Terminal:
```
warning: `VIRTUAL_ENV=/Volumes/teaching/Code/LLamaLauncher/.venv` does not match the project environment path `.venv` and will be ignored; use `--active` to target the active environment instead
============================= test session starts ==============================
platform darwin -- Python 3.14.0, pytest-9.1.0, pluggy-1.6.0 -- /Volumes/teaching/Code/LLamaLauncher/.worktrees/edge-case-tests/.venv/bin/python
cachedir: .pytest_cache
PySide6 6.11.1 -- Qt runtime 6.11.1 -- Qt compiled 6.11.1
rootdir: /Volumes/teaching/Code/LLamaLauncher/.worktrees/edge-case-tests
configfile: pyproject.toml
plugins: cov-7.1.0, qt-4.5.0
collecting ... collected 22 items

tests/test_edge_cases.py::TestLaunchModelMissingFile::test_7_1_appends_error_when_no_model_selected PASSED [  4%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestApiKeyDefault::test_7_2_api_key_defaults_to_12345_when_empty FAILED [  9%]
tests/test_edge_cases.py::TestApiKeyDefault::test_7_2_api_key_uses_line_edit_value_when_not_empty PASSED [ 13%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestApplyParamEdgeCases::test_7_3_uses_spinbox_default_when_value_key_missing PASSED [ 18%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestApplyParamEdgeCases::test_7_3_applies_value_when_present PASSED [ 22%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestApplyParamEdgeCases::test_7_3_defaults_enabled_to_false PASSED [ 27%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestApplyComboParamEdgeCases::test_7_4_no_change_when_text_not_in_combobox PASSED [ 31%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestApplyComboParamEdgeCases::test_7_4_applies_when_text_found PASSED [ 36%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestCollectConfigMissingSections::test_7_5_loads_config_with_minimal_sections FAILED [ 40%]
tests/test_edge_cases.py::TestCollectConfigMissingSections::test_7_5_loads_empty_config FAILED [ 45%]
tests/test_edge_cases.py::TestOnStdoutEmptyData::test_7_6_does_not_append_when_stdout_empty FAILED [ 50%]
tests/test_edge_cases.py::TestOnStderrEmptyData::test_7_7_does_not_append_when_stderr_empty FAILED [ 54%]
tests/test_edge_cases.py::TestCheckAndRefreshRegex::test_7_8_matches_standard_url PASSED [ 59%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestCheckAndRefreshRegex::test_7_8_matches_domain_url PASSED [ 63%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestCheckAndRefreshRegex::test_7_8_no_match_for_non_url_text PASSED [ 68%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestCheckAndRefreshRegex::test_7_8_no_refresh_when_already_done PASSED [ 72%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestInitProcessSetup::test_7_9_process_is_qprocess_instance PASSED [ 77%]
tests/test_edge_cases.py::TestInitProcessSetup::test_7_9_process_parent_is_app PASSED [ 81%]
tests/test_edge_cases.py::TestInitProcessSetup::test_7_9_stdout_signal_connected FAILED [ 86%]
tests/test_edge_cases.py::TestInitProcessSetup::test_7_9_stderr_signal_connected FAILED [ 90%]
tests/test_edge_cases.py::TestInitProcessSetup::test_7_9_finished_signal_connected FAILED [ 95%]
tests/test_edge_cases.py::TestInitProcessSetup::test_7_9_error_signal_connected FAILED [100%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !
Release of profile requested but WebEnginePage still not deleted. Expect troubles !
Release of profile requested but WebEnginePage still not deleted. Expect troubles !
Release of profile requested but WebEnginePage still not deleted. Expect troubles !
Release of profile requested but WebEnginePage still not deleted. Expect troubles !
Release of profile requested but WebEnginePage still not deleted. Expect troubles !
Release of profile requested but WebEnginePage still not deleted. Expect troubles !
Release of profile requested but WebEnginePage still not deleted. Expect troubles !


=================================== FAILURES ===================================
_______ TestApiKeyDefault.test_7_2_api_key_defaults_to_12345_when_empty ________

self = <tests.test_edge_cases.TestApiKeyDefault object at 0x103abdf90>
launch_app = <main.LlamaLaunchApp(0x11581baa0) at 0x113d343c0>

    def test_7_2_api_key_defaults_to_12345_when_empty(self, launch_app):
        """7.2: _collect_config returns '12345' when api_key_line_edit is empty."""
        # Ensure the line edit is empty
        launch_app.api_key_line_edit.setText("")

        config = launch_app._collect_config()

>       assert config["server"]["api_key"] == "12345"
E       AssertionError: assert '' == '12345'
E
E         - 12345

tests/test_edge_cases.py:112: AssertionError
_ TestCollectConfigMissingSections.test_7_5_loads_config_with_minimal_sections _

self = <tests.test_edge_cases.TestCollectConfigMissingSections object at 0x103abead0>
launch_app = <main.LlamaLaunchApp(0x1158fbd60) at 0x122b24c40>
tmp_path = PosixPath('/private/var/folders/2b/sq4pvwxn1f16kvdmz9pm9q2r0000gr/T/zed-agent-terminal-EmbCjl/pytest-of-jmacey/pytest-1/test_7_5_loads_config_with_min0')

    def test_7_5_loads_config_with_minimal_sections(self, launch_app, tmp_path):
        """7.5: _load_config handles file with only required sections."""
        minimal_config = {
            "version": "1.0",
            "server": {"host": "127.0.0.1", "port": 8080},
        }
        config_file = tmp_path / "minimal.json"
        import json

        config_file.write_text(json.dumps(minimal_config))

        # Should not raise, should use defaults for missing sections
>       launch_app._load_config(str(config_file))
E       TypeError: LlamaLaunchApp._load_config() takes 1 positional argument but 2 were given

tests/test_edge_cases.py:230: TypeError
_________ TestCollectConfigMissingSections.test_7_5_loads_empty_config _________

self = <tests.test_edge_cases.TestCollectConfigMissingSections object at 0x103abec10>
launch_app = <main.LlamaLaunchApp(0x115cdf6f0) at 0x127c01d80>
tmp_path = PosixPath('/private/var/folders/2b/sq4pvwxn1f16kvdmz9pm9q2r0000gr/T/zed-agent-terminal-EmbCjl/pytest-of-jmacey/pytest-1/test_7_5_loads_empty_config0')

    def test_7_5_loads_empty_config(self, launch_app, tmp_path):

```


## Assistant

<thinking>
Good progress! The test results show:

**Fixed by test changes (9 more passing now):**
- 7.3 `test_7_3_applies_value_when_present` - Now PASS (QDoubleSpinBox fix)
- 7.3 `test_7_3_defaults_enabled_to_false` - Now PASS (QDoubleSpinBox fix)
- 7.8 All 4 tests still PASS

**Still failing (6 tests):**
1. **7.2 API key default** - Code returns `''`, needs to return `'12345'` → Fix main.py `_collect_config`
2. **7.5 loads_config_with_minimal_sections** - `TypeError: _load_config() takes 1 positional argument but 2 were given` → The method signature is wrong, need to check main.py


3. **7.5 loads_empty_config** - Same TypeError issue
4. **7.6 stdout empty data** - Mock still failing
5. **7.7 stderr empty data** - Mock still failing
6. **7.9 All 4 signal connection tests** - `receivers()` method not working as expected

I need to dig into the main.py implementation for `_load_config` to understand why it's rejecting arguments, then trace through the mock setup for the stdout/stderr tests and figure out the correct way to verify signal connections on the QProcess object.

</thinking>

Good progress! Fixed 3 more tests with the QDoubleSpinBox change. Still failing:

| Test | Error | Fix needed |
|------|-------|------------|
| 7.2 API key default | Returns `''` not `'12345'` | Fix main.py `_collect_config` |
| 7.5 minimal config | `TypeError: _load_config() takes 1 positional argument but 2 were given` | Check method signature in main.py |
| 7.6 stdout empty | Mock still failing | Need to check how `_on_stdout` calls the process |
| 7.7 stderr empty | Mock still failing | Same mock issue |
| 7.9 All 4 signal tests | `receivers()` API not working | Need different approach |

Let me check the actual method signatures and fix the remaining issues.



**Tool Call: Read file `.worktrees/edge-case-tests/main.py` (lines 390-415)**
Status: Completed

```LLamaLauncher/.worktrees/edge-case-tests/main.py
   390	    def _load_config(self) -> None:
   391	        """Load configuration from a user-selected JSON file."""
   392	        file_path, _ = QFileDialog.getOpenFileName(
   393	            self,
   394	            "Load Configuration",
   395	            "",
   396	            "JSON Files (*.json);;All Files (*)",
   397	        )
   398	        if not file_path:
   399	            return
   400	
   401	        try:
   402	            with open(file_path, "r") as f:
   403	                config = json.load(f)
   404	            self._apply_config(config)
   405	            self._last_config_path = file_path
   406	            self.output_display.appendPlainText(
   407	                f"Configuration loaded from {file_path}"
   408	            )
   409	        except json.JSONDecodeError as e:
   410	            QMessageBox.critical(self, "Load Error", f"Invalid JSON format:\n{e}")
   411	        except Exception as e:
   412	            QMessageBox.critical(
   413	                self, "Load Error", f"Failed to load configuration:\n{e}"
   414	            )
   415	

```


**Tool Call: Read file `.worktrees/edge-case-tests/main.py` (lines 240-250)**
Status: Completed

```LLamaLauncher/.worktrees/edge-case-tests/main.py
   240	        # Server
   241	        config["server"] = {
   242	            "host": self.host_line_edit.text(),
   243	            "port": int(self.port_line_edit.text())
   244	            if self.port_line_edit.text().isdigit()
   245	            else 8080,
   246	            "api_key": self.api_key_line_edit.text(),
   247	        }
   248	
   249	        # Sampling parameters
   250	        config["sampling"] = {

```


## Assistant

<thinking>
Good, now I can see the issues:

1. **7.2 API key default**: Line 246 shows `"api_key": self.api_key_line_edit.text()` - no default. Need to change to use `.text() or "12345"`.

2. **7.5 _load_config signature**: The method is `def _load_config(self) -> None:` with no path parameter - it opens a file dialog. My tests are calling it with a path argument. I need to either:
   a. Create a helper method that accepts a path parameter, or
   b. Call `_apply_config` directly since that's what does the actual config application

Looking at the code flow:
- `_load_config()` → opens file dialog → reads JSON → calls `_apply_config(config)`
- For testing, I should test `_apply_config` directly with minimal configs, since that's where the missing sections handling would matter.

Let me check what `_apply_config` does and how it handles missing sections.

3. **7.6/7.7 stdout/stderr empty**: The mock approach isn't working. Let me look at how `_on_stdout` actually calls the process:
```python
def _on_stdout(self) -> None:
    data = (
        self._process.readAllStandardOutput()
        .data()
        .decode("utf-8", errors="replace")
    )
    if data:
        self.output_display.appendPlainText(data)
        self._check_and_refresh()
```

The issue is that `readAllStandardOutput()` returns a `QByteArray` object, and we're chaining `.data().decode()`. When I mock `_process.readAllStandardOutput.return_value = mock_bytes_array`, the mock should work. But wait - the real `QByteArray.data()` returns bytes, and then we call `.decode()` on it. 

Let me think about this more carefully. The mock chain is:
- `launch_app._process.readAllStandardOutput()` → returns `mock_bytes_array`
- `mock_bytes_array.data()` → returns `b""`
- `b"".decode("utf-8", errors="replace")` → returns `""`

This should work... unless the issue is that `QByteArray` has a `.data()` method that returns a pointer, not bytes. Let me check the Qt documentation.

Actually, in PySide6, `QByteArray.data()` returns `Optional[bytes]` when called with specific encoding, or it might return a pointer. The actual method to get bytes from QByteArray is `.toUtf8().data()` or using `bytes(qbytearray)`.

Wait, looking at the actual code again:
```python
data = (
    self._process.readAllStandardOutput()
    .data()
    .decode("utf-8", errors="replace")
)
```

`readAllStandardOutput()` returns a `QByteArray`. Then `.data()` is called on it. In Qt, `QByteArray::data()` returns `char*`, but in Python bindings, it might return bytes or None. 

Actually, I think the issue might be that `QByteArray.data()` in PySide6 returns a pointer to the internal data, and calling `.decode()` on it would fail because a pointer doesn't have a `.decode()` method. But the code works in production...

Let me look at this differently. The real issue is that my mock setup might not be correct. Let me try a different approach - patch the methods directly on the instance.

4. **7.9 signal connections**: The `receivers()` method in Qt is called on the signal object, but the API might be different in PySide6. Let me try a different approach - check if the connections exist by looking at the object's connect method or using a different verification method.

Let me fix all these issues:

1. Fix main.py for 7.2 (API key default)
2. Fix tests for 7.5 (use _apply_config directly instead of _load_config)
3. Fix tests for 7.6/7.7 (better mock approach)
4. Fix tests for 7.9 (different signal verification approach)

Let me start with the main.py fix and then the test fixes.

</thinking>

Now I can see the issues clearly:

1. **7.2**: Line 246 has `"api_key": self.api_key_line_edit.text()` — no default fallback
2. **7.5**: `_load_config(self)` takes no path argument — it opens a file dialog. I should test `_apply_config` directly instead
3. **7.6/7.7**: The mock chaining approach isn't matching how `QByteArray.data()` works in PySide6
4. **7.9**: The `receivers()` API needs adjustment for PySide6

Let me fix main.py first (GREEN phase), then fix the test issues.

### GREEN: Fix main.py — API key default (test 7.2)



**Tool Call: .worktrees/edge\-case\-tests/main.py**
Status: Completed

Diff: .worktrees/edge-case-tests/main.py
```
#!/usr/bin/env -S uv run --script
"""Llama model launcher application."""

import argparse
import json
import re
import sys
from pathlib import Path

from PySide6.QtCore import QCoreApplication, QProcess, QSettings, Qt, QTimer, QUrl
from PySide6.QtGui import QAction
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile
from PySide6.QtWebEngineWidgets import QWebEngineView  # noqa: F401
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QMenu,
    QMessageBox,
)

from ui_loader import load_ui


class LlamaLaunchApp(QMainWindow):
    """Main application window for the Llama model launcher.

    Loads its UI from a .ui file via QUiLoader and wires up all
    signals and slots to preserve existing behaviour.
    """

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 8080,
        ctx_size: int | None = None,
    ) -> None:
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
        self._profile: QWebEngineProfile = self._create_persistent_profile()
        self._ctx_size: int | None = ctx_size
        self._setup_ui()
        self._load_last_session()
        self._connect_signals()
        self._init_web_view()

    # ------------------------------------------------------------------
    # UI loading and initialization
    # ------------------------------------------------------------------

    def _create_cache_dir(self) -> Path:
        """Create and return a cache directory for persistent web storage.

        Returns:
            Path to the cache directory (created if it does not exist).
        """
        cache_dir = Path(QCoreApplication.applicationDirPath()) / ".cache" / "llama-launcher"
        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir

    def _create_persistent_profile(self) -> QWebEngineProfile:
        """Create a QWebEngineProfile with disk-backed persistent storage.

        This ensures localStorage, sessionStorage, cookies, and IndexedDB
        survive across application restarts so the chat UI remembers
        API keys and conversation history.

        Returns:
            Configured QWebEngineProfile instance.
        """
        profile = QWebEngineProfile("llama-launcher-profile", self)

        # Persist localStorage, sessionStorage, and IndexedDB to disk
        profile.setPersistentStoragePath(str(self._cache_dir))

        # Persist cookies to disk (not session-only)
        profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies)

        # Enable disk HTTP cache for faster page loads
        cache_subdir = self._cache_dir / "cache"
        cache_subdir.mkdir(parents=True, exist_ok=True)
        profile.setHttpCacheType(QWebEngineProfile.DiskHttpCache)
        profile.setHttpCacheMaximumSize(100 * 1024 * 1024)  # 100 MB

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

    def _setup_ui(self) -> None:
        """Load the main window UI from the .ui file.

        All child widgets and layouts are auto-assigned as attributes
        on this instance by their ``objectName`` so that the .ui file
        controls which names are available.
        """
        ui_path = Path(__file__).resolve().parent / "ui" / "llama_launch.ui"
        load_ui(ui_path, self)
        self._setup_context_size_combo()
        self._create_file_menu()

    def _setup_context_size_combo(self) -> None:
        """Populate the model context size combobox with options and tooltips.

        Each item stores its numeric value (used as ``--ctx-size``) in the
        user data role so the launch method can retrieve it later.
        """
        self.model_context_size.clear()

        context_options = [
            ("Auto (model default)", 0, "Recommended default; uses GGUF model context"),
            ("2K", 2048, "Very small models / low memory"),
            ("4K", 4096, "Basic chat, small coding tasks"),
            ("8K", 8192, "General purpose"),
            ("16K", 16384, "Better coding/chat history"),
            ("32K", 32768, "Large files, coding assistants"),
            ("64K", 65536, "Long documents, repo context"),
            ("128K", 131072, "Modern long-context models"),
        ]

        for display_name, value, tooltip in context_options:
            self.model_context_size.addItem(display_name, value)
            index = self.model_context_size.count() - 1
            self.model_context_size.setItemData(index, tooltip, Qt.ToolTipRole)

        # Pre-select from CLI if provided, otherwise default to 16K
        if self._ctx_size is not None:
            target = self._ctx_size
        else:
            target = 16384  # 16K default

        for i in range(self.model_context_size.count()):
            if int(self.model_context_size.itemData(i, Qt.UserRole)) == target:
                self.model_context_size.setCurrentIndex(i)
                break

    # ------------------------------------------------------------------
    # File menu
    # ------------------------------------------------------------------

    def _create_file_menu(self) -> None:
        """Create the File menu with Save, Save As, and Load actions."""
        file_menu = QMenu("&File", self)

        save_action = QAction("Save Configuration", self)
        save_action.setShortcut("Ctrl+S")
        save_action.setStatusTip("Save current configuration to file")
        save_action.triggered.connect(self._save_config)
        file_menu.addAction(save_action)

        save_as_action = QAction("Save As Configuration...", self)
        save_as_action.setStatusTip("Save current configuration to a new file")
        save_as_action.triggered.connect(self._save_config_as)
        file_menu.addAction(save_as_action)

        load_action = QAction("Load Configuration...", self)
        load_action.setShortcut("Ctrl+O")
        load_action.setStatusTip("Load configuration from file")
        load_action.triggered.connect(self._load_config)
        file_menu.addAction(load_action)

        self.menuBar().addMenu(file_menu)

    # ------------------------------------------------------------------
    # Configuration save/load
    # ------------------------------------------------------------------

    def _save_config(self) -> None:
        """Save current configuration to the last saved file or prompt for path."""
        if not hasattr(self, "_last_config_path"):
            self._save_config_as()
            return
        self._write_config_file(self._last_config_path)

    def _save_config_as(self) -> None:
        """Save current configuration to a user-selected file path."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Configuration",
            "",
            "JSON Files (*.json);;All Files (*)",
        )
        if file_path:
            self._write_config_file(file_path)
            self._last_config_path = file_path

    def _write_config_file(self, file_path: str) -> None:
        """Write the current UI configuration to a JSON file.

        Args:
            file_path: Path to the JSON file to write.
        """
        config = self._collect_config()
        try:
            with open(file_path, "w") as f:
                json.dump(config, f, indent=2)
            self.output_display.appendPlainText(f"Configuration saved to {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Failed to save configuration:\n{e}")

    def _collect_config(self) -> dict:
        """Collect all UI widget values into a configuration dictionary.

        Returns:
            Dictionary containing all configuration values organized by category.
        """
        config: dict = {"version": "1.0"}

        # Files/Paths
        config["files"] = {
            "model_path": self.model_path_edit.property("fullPath") or "",
            "mmproj_path": self.mmproj_path_edit.property("fullPath") or "",
            "draft_model_path": self.draft_model_line_edit.property("fullPath") or "",
            "json_schema_path": self.json_schema_line_edit.property("fullPath") or "",
        }

        # Server
        config["server"] = {
            "host": self.host_line_edit.text(),
            "port": int(self.port_line_edit.text()) if self.port_line_edit.text().isdigit() else 8080,
            "api_key": self.api_key_line_edit.text() or "12345",
        }

        # Sampling parameters
        config["sampling"] = {
            "temperature": {
                "enabled": self.enable_temperature_checkbox.isChecked(),
                "value": self.temperature_spinbox.value(),
            },
            "top_p": {
                "enabled": self.enable_top_p_checkbox.isChecked(),
                "value": self.top_p_spinbox.value(),
            },
            "top_k": {
                "enabled": self.enable_top_k_checkbox.isChecked(),
                "value": self.top_k_spinbox.value(),
            },
            "min_p": {
                "enabled": self.enable_min_p_checkbox.isChecked(),
                "value": self.min_p_spinbox.value(),
            },
            "typical_p": {
                "enabled": self.enable_typical_p_checkbox.isChecked(),
                "value": self.typical_p_spinbox.value(),
            },
            "repeat_penalty": {
                "enabled": self.enable_repeat_penalty_checkbox.isChecked(),
                "value": self.repeat_penalty_spinbox.value(),
            },
            "repeat_last_n": {
                "enabled": self.enable_repeat_last_n_checkbox.isChecked(),
                "value": self.repeat_last_n_spinbox.value(),
            },
            "presence_penalty": {
                "enabled": self.enable_presence_penalty_checkbox.isChecked(),
                "value": self.presence_penalty_spinbox.value(),
            },
            "frequency_penalty": {
                "enabled": self.enable_frequency_penalty_checkbox.isChecked(),
                "value": self.frequency_penalty_spinbox.value(),
            },
            "mirostat": {
                "enabled": self.enable_mirostat_checkbox.isChecked(),
                "value": self.mirostat_spinbox.value(),
            },
            "mirostat_lr": {
                "enabled": self.enable_mirostat_lr_checkbox.isChecked(),
                "value": self.mirostat_lr_spinbox.value(),
            },
            "mirostat_ent": {
                "enabled": self.enable_mirostat_ent_checkbox.isChecked(),
                "value": self.mirostat_ent_spinbox.value(),
            },
        }

        # Performance parameters
        config["performance"] = {
            "gpu_layers": {
                "enabled": self.enable_gpu_layers_checkbox.isChecked(),
                "value": self.gpu_layers_spinbox.value(),
            },
            "threads": {
                "enabled": self.enable_threads_checkbox.isChecked(),
                "value": self.threads_spinbox.value(),
            },
            "threads_batch": {
                "enabled": self.enable_threads_batch_checkbox.isChecked(),
                "value": self.threads_batch_spinbox.value(),
            },
            "batch_size": {
                "enabled": self.enable_batch_size_checkbox.isChecked(),
                "value": self.batch_size_spinbox.value(),
            },
            "ubatch_size": {
                "enabled": self.enable_ubatch_size_checkbox.isChecked(),
                "value": self.ubatch_size_spinbox.value(),
            },
            "n_predict": {
                "enabled": self.enable_n_predict_checkbox.isChecked(),
                "value": self.n_predict_spinbox.value(),
            },
            "parallel": {
                "enabled": self.enable_parallel_checkbox.isChecked(),
                "value": self.parallel_spinbox.value(),
            },
            "flash_attn": self.flash_attn_combobox.currentText(),
            "cache_type_k": {
                "enabled": self.enable_cache_type_k_checkbox.isChecked(),
                "value": self.cache_type_k_combobox.currentText(),
            },
            "cache_type_v": {
                "enabled": self.enable_cache_type_v_checkbox.isChecked(),
                "value": self.cache_type_v_combobox.currentText(),
            },
            "mmap": self.enable_mmap_checkbox.isChecked(),
            "mlock": self.enable_mlock_checkbox.isChecked(),
            "cont_batching": self.enable_cont_batching_checkbox.isChecked(),
        }

        # Advanced Generation parameters
        config["advanced"] = {
            "draft_model": {
                "enabled": self.enable_draft_model_checkbox.isChecked(),
                "path": self.draft_model_line_edit.property("fullPath") or "",
            },
            "spec_draft_n_max": {
                "enabled": self.enable_spec_draft_n_max_checkbox.isChecked(),
                "value": self.spec_draft_n_max_spinbox.value(),
            },
            "seed": {
                "enabled": self.enable_seed_checkbox.isChecked(),
                "value": self.seed_spinbox.value(),
            },
            "grammar": {
                "enabled": self.enable_grammar_checkbox.isChecked(),
                "path": self.grammar_line_edit.property("fullPath") or "",
            },
            "json_schema": {
                "enabled": self.enable_json_schema_checkbox.isChecked(),
                "path": self.json_schema_line_edit.property("fullPath") or "",
            },
            "rope_scaling": {
                "enabled": self.enable_rope_scaling_checkbox.isChecked(),
                "value": self.rope_scaling_combobox.currentText(),
            },
            "rope_freq_base": {
                "enabled": self.enable_rope_freq_base_checkbox.isChecked(),
                "value": self.rope_freq_base_spinbox.value(),
            },
            "rope_freq_scale": {
                "enabled": self.enable_rope_freq_scale_checkbox.isChecked(),
                "value": self.rope_freq_scale_spinbox.value(),
            },
        }

        # Other settings
        config["context_size"] = self.model_context_size.itemData(self.model_context_size.currentIndex(), Qt.UserRole)
        config["more_options"] = self.more_options_line_edit.text()
        config["no_mmproj_offload"] = self.no_mmproj_offload_checkbox.isChecked()

        return config

    def _load_config(self) -> None:
        """Load configuration from a user-selected JSON file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Configuration",
            "",
            "JSON Files (*.json);;All Files (*)",
        )
        if not file_path:
            return

        try:
            with open(file_path, "r") as f:
                config = json.load(f)
            self._apply_config(config)
            self._last_config_path = file_path
            self.output_display.appendPlainText(f"Configuration loaded from {file_path}")
        except json.JSONDecodeError as e:
            QMessageBox.critical(self, "Load Error", f"Invalid JSON format:\n{e}")
        except Exception as e:
            QMessageBox.critical(self, "Load Error", f"Failed to load configuration:\n{e}")

    def _apply_config(self, config: dict) -> None:
        """Apply configuration values from a dictionary to the UI widgets.

        Args:
            config: Configuration dictionary to apply.
        """
        # Files/Paths
        if "files" in config:
            files = config["files"]
            self._set_path_field(self.model_path_edit, files.get("model_path", ""))
            self._set_path_field(self.mmproj_path_edit, files.get("mmproj_path", ""))
            self._set_path_field(self.draft_model_line_edit, files.get("draft_model_path", ""))
            self._set_path_field(self.json_schema_line_edit, files.get("json_schema_path", ""))

        # Server
        if "server" in config:
            server = config["server"]
            self.host_line_edit.setText(server.get("host", "127.0.0.1"))
            port = server.get("port", 8080)
            self.port_line_edit.setText(str(port))
            self.api_key_line_edit.setText(server.get("api_key", "12345"))

        # Sampling parameters
        if "sampling" in config:
            sampling = config["sampling"]
            self._apply_param(
                sampling,
                "temperature",
                self.enable_temperature_checkbox,
                self.temperature_spinbox,
            )
            self._apply_param(sampling, "top_p", self.enable_top_p_checkbox, self.top_p_spinbox)
            self._apply_param(sampling, "top_k", self.enable_top_k_checkbox, self.top_k_spinbox)
            self._apply_param(sampling, "min_p", self.enable_min_p_checkbox, self.min_p_spinbox)
            self._apply_param(
                sampling,
                "typical_p",
                self.enable_typical_p_checkbox,
                self.typical_p_spinbox,
            )
            self._apply_param(
                sampling,
                "repeat_penalty",
                self.enable_repeat_penalty_checkbox,
                self.repeat_penalty_spinbox,
            )
            self._apply_param(
                sampling,
                "repeat_last_n",
                self.enable_repeat_last_n_checkbox,
                self.repeat_last_n_spinbox,
            )
            self._apply_param(
                sampling,
                "presence_penalty",
                self.enable_presence_penalty_checkbox,
                self.presence_penalty_spinbox,
            )
            self._apply_param(
                sampling,
                "frequency_penalty",
                self.enable_frequency_penalty_checkbox,
                self.frequency_penalty_spinbox,
            )
            self._apply_param(
                sampling,
                "mirostat",
                self.enable_mirostat_checkbox,
                self.mirostat_spinbox,
            )
            self._apply_param(
                sampling,
                "mirostat_lr",
                self.enable_mirostat_lr_checkbox,
                self.mirostat_lr_spinbox,
            )
            self._apply_param(
                sampling,
                "mirostat_ent",
                self.enable_mirostat_ent_checkbox,
                self.mirostat_ent_spinbox,
            )

        # Performance parameters
        if "performance" in config:
            perf = config["performance"]
            self._apply_param(
                perf,
                "gpu_layers",
                self.enable_gpu_layers_checkbox,
                self.gpu_layers_spinbox,
            )
            self._apply_param(perf, "threads", self.enable_threads_checkbox, self.threads_spinbox)
            self._apply_param(
                perf,
                "threads_batch",
                self.enable_threads_batch_checkbox,
                self.threads_batch_spinbox,
            )
            self._apply_param(
                perf,
                "batch_size",
                self.enable_batch_size_checkbox,
                self.batch_size_spinbox,
            )
            self._apply_param(
                perf,
                "ubatch_size",
                self.enable_ubatch_size_checkbox,
                self.ubatch_size_spinbox,
            )
            self._apply_param(
                perf,
                "n_predict",
                self.enable_n_predict_checkbox,
                self.n_predict_spinbox,
            )
            self._apply_param(perf, "parallel", self.enable_parallel_checkbox, self.parallel_spinbox)

            if "flash_attn" in perf:
                text = perf["flash_attn"]
                index = self.flash_attn_combobox.findText(text)
                if index >= 0:
                    self.flash_attn_combobox.setCurrentIndex(index)

            self._apply_combo_param(
                perf,
                "cache_type_k",
                self.enable_cache_type_k_checkbox,
                self.cache_type_k_combobox,
            )
            self._apply_combo_param(
                perf,
                "cache_type_v",
                self.enable_cache_type_v_checkbox,
                self.cache_type_v_combobox,
            )

            if "mmap" in perf:
                self.enable_mmap_checkbox.setChecked(bool(perf["mmap"]))
            if "mlock" in perf:
                self.enable_mlock_checkbox.setChecked(bool(perf["mlock"]))
            if "cont_batching" in perf:
                self.enable_cont_batching_checkbox.setChecked(bool(perf["cont_batching"]))

        # Advanced Generation parameters
        if "advanced" in config:
            adv = config["advanced"]
            self._apply_param(
                adv,
                "spec_draft_n_max",
                self.enable_spec_draft_n_max_checkbox,
                self.spec_draft_n_max_spinbox,
            )
            self._apply_param(adv, "seed", self.enable_seed_checkbox, self.seed_spinbox)

            # Draft model (path-based)
            if "draft_model" in adv:
                draft = adv["draft_model"]
                self.enable_draft_model_checkbox.setChecked(draft.get("enabled", False))
                self._set_path_field(self.draft_model_line_edit, draft.get("path", ""))

            # Grammar (path-based)
            if "grammar" in adv:
                grammar = adv["grammar"]
                self.enable_grammar_checkbox.setChecked(grammar.get("enabled", False))
                self._set_path_field(self.grammar_line_edit, grammar.get("path", ""))

            # JSON schema (path-based)
            if "json_schema" in adv:
                js = adv["json_schema"]
                self.enable_json_schema_checkbox.setChecked(js.get("enabled", False))
                self._set_path_field(self.json_schema_line_edit, js.get("path", ""))

            self._apply_combo_param(
                adv,
                "rope_scaling",
                self.enable_rope_scaling_checkbox,
                self.rope_scaling_combobox,
            )
            self._apply_param(
                adv,
                "rope_freq_base",
                self.enable_rope_freq_base_checkbox,
                self.rope_freq_base_spinbox,
            )
            self._apply_param(
                adv,
                "rope_freq_scale",
                self.enable_rope_freq_scale_checkbox,
                self.rope_freq_scale_spinbox,
            )

        # Other settings
        if "context_size" in config:
            ctx_size = config["context_size"]
            for i in range(self.model_context_size.count()):
                if int(self.model_context_size.itemData(i, Qt.UserRole)) == ctx_size:
                    self.model_context_size.setCurrentIndex(i)
                    break

        if "more_options" in config:
            self.more_options_line_edit.setText(config["more_options"])

        if "no_mmproj_offload" in config:
            self.no_mmproj_offload_checkbox.setChecked(bool(config["no_mmproj_offload"]))

    def _set_path_field(self, line_edit, path: str) -> None:
        """Set a path field with full path stored and short filename displayed.

        Args:
            line_edit: The QLineEdit widget to update.
            path: The full file path to set.
        """
        if path:
            line_edit.setProperty("fullPath", path)
            line_edit.setText(path.rsplit("/", 1)[-1])
        else:
            line_edit.setProperty("fullPath", "")
            line_edit.setText("")

    def _apply_param(self, params: dict, name: str, checkbox, spinbox) -> None:
        """Apply an enabled+value parameter pair to a checkbox and spinbox.

        Args:
            params: Dictionary containing the parameter data.
            name: Parameter name key in the dictionary.
            checkbox: The QCheckBox widget.
            spinbox: The QSpinBox/QDoubleSpinBox widget.
        """
        if name in params:
            param = params[name]
            if isinstance(param, dict):
                checkbox.setChecked(param.get("enabled", False))
                spinbox.setValue(param.get("value", spinbox.value()))
            else:
                # Legacy format: just a value
                checkbox.setChecked(True)
                spinbox.setValue(param)

    def _apply_combo_param(self, params: dict, name: str, checkbox, combobox) -> None:
        """Apply an enabled+value parameter pair to a checkbox and combobox.

        Args:
            params: Dictionary containing the parameter data.
            name: Parameter name key in the dictionary.
            checkbox: The QCheckBox widget.
            combobox: The QComboBox widget.
        """
        if name in params:
            param = params[name]
            if isinstance(param, dict):
                checkbox.setChecked(param.get("enabled", False))
                text = param.get("value", "")
                index = combobox.findText(text)
                if index >= 0:
                    combobox.setCurrentIndex(index)
            else:
                # Legacy format: just a value
                checkbox.setChecked(True)
                index = combobox.findText(str(param))
                if index >= 0:
                    combobox.setCurrentIndex(index)

    # ------------------------------------------------------------------
    # Window lifecycle
    # ------------------------------------------------------------------

    def closeEvent(self, event) -> None:
        """Save last session settings when the window is closed.

        Uses QSettings to persist basic connection settings and window
        geometry so they are restored on the next launch.
        """
        self._save_last_session()
        super().closeEvent(event)

    def _save_last_session(self) -> None:
        """Save last-used settings to QSettings for session restoration."""
        settings = QSettings("LLamaLauncher", "LlamaLaunchApp")
        settings.setValue("lastModelPath", self.model_path_edit.property("fullPath") or "")
        settings.setValue("host", self.host_line_edit.text())
        settings.setValue("port", self.port_line_edit.text())
        settings.setValue("windowGeometry", self.saveGeometry())

    def _load_last_session(self) -> None:
        """Restore last-used settings from QSettings.

        Pre-populates the UI with the host, port, and model path
        from the previous session so the user doesn't have to re-enter them.
        """
        settings = QSettings("LLamaLauncher", "LlamaLaunchApp")

        # Restore window geometry if saved
        geometry = settings.value("windowGeometry")
        if geometry:
            self.restoreGeometry(geometry)

        # Restore server settings
        host = settings.value("host", "127.0.0.1")
        port = settings.value("port", "8080")
        self.host_line_edit.setText(host)
        self.port_line_edit.setText(port)

        # Restore model path if available
        last_model_path = settings.value("lastModelPath", "")
        if last_model_path:
            self._set_path_field(self.model_path_edit, last_model_path)

    # ------------------------------------------------------------------
    # Signal connections
    # ------------------------------------------------------------------

    def _connect_signals(self) -> None:
        """Connect widget signals to their slot methods."""
        self.select_model_button.clicked.connect(self._select_model)
        self.select_mmproj_button.clicked.connect(self._select_mmproj)
        self.select_draft_model_button.clicked.connect(self._select_draft_model)
        self.select_json_schema_button.clicked.connect(self._select_json_schema)
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

    def _select_draft_model(self) -> None:
        """Open a file dialog to select a draft model .gguf file.

        Stores the full path as a custom property on the line edit
        (accessible via ``getProperty("fullPath")``) while displaying
        only the short filename in the UI.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Draft Model",
            "",
            "GGUF Files (*.gguf)",
        )
        if file_path:
            self.draft_model_line_edit.setProperty("fullPath", file_path)
            self.draft_model_line_edit.setText(file_path.rsplit("/", 1)[-1])

    def _select_json_schema(self) -> None:
        """Open a file dialog to select a JSON schema file.

        Stores the full path as a custom property on the line edit
        (accessible via ``getProperty("fullPath")``) while displaying
        only the short filename in the UI.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select JSON Schema",
            "",
            "JSON Files (*.json)",
        )
        if file_path:
            self.json_schema_line_edit.setProperty("fullPath", file_path)
            self.json_schema_line_edit.setText(file_path.rsplit("/", 1)[-1])

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
        min_p = self.min_p_spinbox.value()
        typical_p = self.typical_p_spinbox.value()
        repeat_penalty = self.repeat_penalty_spinbox.value()
        repeat_last_n = self.repeat_last_n_spinbox.value()
        presence_penalty = self.presence_penalty_spinbox.value()
        frequency_penalty = self.frequency_penalty_spinbox.value()

        mirostat = self.mirostat_spinbox.value()
        mirostat_lr = self.mirostat_lr_spinbox.value()
        mirostat_ent = self.mirostat_ent_spinbox.value()

        # Performance parameters
        gpu_layers = self.gpu_layers_spinbox.value()
        threads = self.threads_spinbox.value()
        threads_batch = self.threads_batch_spinbox.value()
        batch_size = self.batch_size_spinbox.value()
        ubatch_size = self.ubatch_size_spinbox.value()
        n_predict = self.n_predict_spinbox.value()
        parallel = self.parallel_spinbox.value()
        cache_type_k = self.cache_type_k_combobox.currentText()
        cache_type_v = self.cache_type_v_combobox.currentText()

        # Advanced Generation parameters
        spec_draft_n_max = self.spec_draft_n_max_spinbox.value()
        seed = self.seed_spinbox.value()
        rope_scaling = self.rope_scaling_combobox.currentText()
        rope_freq_base = self.rope_freq_base_spinbox.value()
        rope_freq_scale = self.rope_freq_scale_spinbox.value()

        mmproj_path = self.mmproj_path_edit.property("fullPath")
        no_mmproj_offload = self.no_mmproj_offload_checkbox.isChecked()
        api_key = self.api_key_line_edit.text() if self.api_key_line_edit.text() else "12345"

        # Build command: llama-server --model ... (conditional sampling params) ...
        cmd = [
            "llama-server",
            "--model",
            model_path,
            "--api-key",
            api_key,
        ]

        if self.enable_temperature_checkbox.isChecked():
            cmd.extend(["--temp", str(temperature)])
        if self.enable_top_p_checkbox.isChecked():
            cmd.extend(["--top-p", str(top_p)])
        if self.enable_top_k_checkbox.isChecked():
            cmd.extend(["--top-k", str(top_k)])
        if self.enable_min_p_checkbox.isChecked():
            cmd.extend(["--min-p", str(min_p)])
        if self.enable_typical_p_checkbox.isChecked():
            cmd.extend(["--typical-p", str(typical_p)])
        if self.enable_repeat_penalty_checkbox.isChecked():
            cmd.extend(["--repeat-penalty", str(repeat_penalty)])
        if self.enable_repeat_last_n_checkbox.isChecked():
            cmd.extend(["--repeat-last-n", str(repeat_last_n)])
        if self.enable_presence_penalty_checkbox.isChecked():
            cmd.extend(["--presence-penalty", str(presence_penalty)])
        if self.enable_frequency_penalty_checkbox.isChecked():
            cmd.extend(["--frequency-penalty", str(frequency_penalty)])
        if self.enable_mirostat_checkbox.isChecked():
            cmd.extend(["--mirostat", str(mirostat)])
        if self.enable_mirostat_lr_checkbox.isChecked():
            cmd.extend(["--mirostat-lr", str(mirostat_lr)])
        if self.enable_mirostat_ent_checkbox.isChecked():
            cmd.extend(["--mirostat-ent", str(mirostat_ent)])

        # Performance parameters
        if self.enable_gpu_layers_checkbox.isChecked():
            cmd.extend(["--n-gpu-layers", str(gpu_layers)])
        if self.enable_threads_checkbox.isChecked():
            cmd.extend(["--threads", str(threads)])
        if self.enable_threads_batch_checkbox.isChecked():
            cmd.extend(["--threads-batch", str(threads_batch)])
        if self.enable_batch_size_checkbox.isChecked():
            cmd.extend(["--batch-size", str(batch_size)])
        if self.enable_ubatch_size_checkbox.isChecked():
            cmd.extend(["--ubatch-size", str(ubatch_size)])
        if self.enable_n_predict_checkbox.isChecked():
            cmd.extend(["--n-predict", str(n_predict)])
        # Flash Attention: always pass the selected value (default auto)
        flash_attn = self.flash_attn_combobox.currentText()
        cmd.extend(["--flash-attn", flash_attn])
        if self.enable_cache_type_k_checkbox.isChecked():
            cmd.extend(["--cache-type-k", cache_type_k])
        if self.enable_cache_type_v_checkbox.isChecked():
            cmd.extend(["--cache-type-v", cache_type_v])
        if self.enable_mmap_checkbox.isChecked():
            cmd.append("--mmap")
        if self.enable_mlock_checkbox.isChecked():
            cmd.append("--mlock")
        if self.enable_cont_batching_checkbox.isChecked():
            cmd.append("--cont-batching")
        if self.enable_parallel_checkbox.isChecked():
            cmd.extend(["--parallel", str(parallel)])

        # Advanced Generation parameters
        draft_model_path = self.draft_model_line_edit.property("fullPath")
        if self.enable_draft_model_checkbox.isChecked() and draft_model_path:
            cmd.extend(["--draft-model", draft_model_path])
        if self.enable_spec_draft_n_max_checkbox.isChecked():
            cmd.extend(["--spec-draft-n-max", str(spec_draft_n_max)])
        if self.enable_seed_checkbox.isChecked():
            cmd.extend(["--seed", str(seed)])
        grammar_text = self.grammar_line_edit.text().strip()
        if self.enable_grammar_checkbox.isChecked() and grammar_text:
            cmd.extend(["--grammar", grammar_text])
        json_schema_path = self.json_schema_line_edit.property("fullPath")
        if self.enable_json_schema_checkbox.isChecked() and json_schema_path:
            cmd.extend(["--json-schema", json_schema_path])
        if self.enable_rope_scaling_checkbox.isChecked():
            cmd.extend(["--rope-scaling", rope_scaling])
        if self.enable_rope_freq_base_checkbox.isChecked():
            cmd.extend(["--rope-freq-base", str(rope_freq_base)])
        if self.enable_rope_freq_scale_checkbox.isChecked():
            cmd.extend(["--rope-freq-scale", str(rope_freq_scale)])

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

        # Extra user-supplied flags from the more options line edit
        extra = self.more_options_line_edit.text().strip()
        if extra:
            cmd.extend(extra.split())

        # Context size: only pass --ctx-size when a specific value is selected
        ctx_size = self.model_context_size.itemData(
            self.model_context_size.currentIndex(),
            Qt.UserRole,
        )
        if ctx_size is not None and int(ctx_size) > 0:
            cmd.extend(["--ctx-size", str(ctx_size)])

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
    # QProcess output slots
    # ------------------------------------------------------------------

    def _on_stdout(self) -> None:
        """Append stdout from the child process to the output display.

        Also watches for the server URL pattern (http://HOST:PORT) in the
        output and auto-refreshes the web view once the server is ready.
        """
        data = self._process.readAllStandardOutput().data().decode("utf-8", errors="replace")
        if data:
            self.output_display.appendPlainText(data)
            self._check_and_refresh()

    def _on_stderr(self) -> None:
        """Append stderr from the child process to the output display.

        Also watches for the server URL pattern (http://HOST:PORT) in the
        output and auto-refreshes the web view once the server is ready.
        """
        data = self._process.readAllStandardError().data().decode("utf-8", errors="replace")
        if data:
            self.output_display.appendPlainText(data)
            self._check_and_refresh()

    def _check_and_refresh(self) -> None:
        """Check output for server URL and refresh web view once ready.

        Scans the full text of the output display for an HTTP URL pattern.
        When found (and not already refreshed), schedules a one-shot timer
        to reload the web view so the Qt event loop is not blocked.
        """
        if self._auto_refresh_done:
            return

        text = self.output_display.toPlainText()
        match = re.search(r"http://[\w.-]+:\d+", text)
        if match:
            self._auto_refresh_done = True
            QTimer.singleShot(0, self._refresh_web_view)

    def _refresh_web_view(self) -> None:
        """Reload the server web view to fetch the freshly started server."""
        url = QUrl(self._server_url)
        self.server_web_view.setUrl(url)
        self.output_display.appendPlainText(f"\n[Server ready — refreshed web view at {self._server_url}]")

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
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host address for the server (default: 127.0.0.1)",
    )
    parser.add_argument("--port", type=int, default=8080, help="Port for the server (default: 8080)")
    parser.add_argument(
        "-c",
        "--ctx-size",
        type=int,
        default=None,
        help="Model context size in tokens (e.g. 4096, 8192, 32768). Overrides the UI combo box.",
    )
    args = parser.parse_args()

    app = QApplication(sys.argv)
    window = LlamaLaunchApp(host=args.host, port=args.port, ctx_size=args.ctx_size)
    window.show()
    sys.exit(app.exec())

```


## Assistant

<thinking>
The user didn't send a new message - this is a continuation of my previous response where I was fixing test issues and making code changes to main.py. I had just edited main.py in the worktree to fix the API key default (7.2), but the edit also applied some formatting changes that weren't necessary.

Now I need to:
1. Fix the remaining test issues (7.5, 7.6, 7.7, 7.9)
2. Run the tests again to verify GREEN phase
3. Copy changes back to main worktree

Let me continue with fixing the test file for the remaining failures:
- 7.5: Need to test `_apply_config` directly instead of `_load_config` (which opens a file dialog)
- 7.6/7.7: The mock approach needs adjustment - I need to understand how `QByteArray.data()` works in PySide6


- 7.9: The signal connection verification needs a different approach

I'm realizing the main.py edit also made some formatting changes that weren't strictly necessary. Let me focus on fixing the test issues first, then run the tests to see if the API key default change alone is sufficient. For 7.5, I'll update the tests to call `_apply_config` directly since that's what handles the actual config application. For 7.6 and 7.7, I need to reconsider how `QByteArray.data()` works in PySide6 - it might return bytes directly rather than requiring a `.decode()` call.

The `receivers()` method in PySide6 likely needs to be called on the signal object itself, not on the instance. Let me tackle these test fixes one at a time and see what passes.

</thinking>

The user didn't send a new message - this is a continuation of my previous work where I was fixing test issues and making code changes. I had just applied the main.py fix for the API key default (7.2), but the edit also made some formatting changes. Let me now fix the remaining test issues and verify all tests pass.

Let me fix the remaining test issues:
- **7.5**: Test `_apply_config` directly (not `_load_config` which opens a file dialog)
- **7.6/7.7**: Fix mock approach for QByteArray chain
- **7.9**: Fix signal connection verification

### Fix 7.5: Use `_apply_config` directly instead of `_load_config`



**Tool Call: .worktrees/edge\-case\-tests/tests/test\_edge\_cases.py**
Status: Completed

Diff: .worktrees/edge-case-tests/tests/test_edge_cases.py
```
"""Phase 7: Edge Cases and Error Handling tests.

Covers error paths, edge cases, and robustness for LlamaLaunchApp:

- _launch_model handles missing model file gracefully
- API key defaults when line edit is empty
- _apply_param uses spinbox default value
- _apply_combo_param does nothing on no text match
- _collect_config handles missing optional sections
- _on_stdout/_on_stderr handle empty data
- _check_and_refresh regex matches various URL formats
- __init__ initializes _process with correct signal connections

TDD: tests written before implementation (RED phase).
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtCore import QProcess, QTimer
from PySide6.QtWidgets import QApplication, QCheckBox, QComboBox, QDoubleSpinBox, QLineEdit, QPlainTextEdit, QSpinBox

# Ensure worktree
sys.path.insert(0, str(Path(__file__).parent.parent))


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def app():
    """Provide QApplication singleton for test module."""
    application = QApplication.instance()
    if application is None:
        application = QApplication(sys.argv)
    yield application


@pytest.fixture
def launch_app(app):
    """Provide a LlamaLaunchApp instance for testing.

    Since full UI initialization is expensive, we create the app and
    patch widgets that tests don't interact with.
    """
    from main import LlamaLaunchApp

    instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
    yield instance
    instance.close()


@pytest.fixture
def minimal_app(app):
    """Minimal LlamaLaunchApp-like class for testing helper methods.

    Since _apply_param and _apply_combo_param are instance methods on
    LlamaLaunchApp, we create a minimal subclass that only initializes
    the widgets we care about.
    """

    class TestApp(QApplication):  # type: ignore[misc]
        """Minimal app for testing helper method behavior."""

        pass

    return app


# ---------------------------------------------------------------------------
# 7.1: _launch_model handles missing model file gracefully
# ---------------------------------------------------------------------------


class TestLaunchModelMissingFile:
    """7.1: _launch_model handles missing model file (command still built)."""

    def test_7_1_appends_error_when_no_model_selected(self, launch_app):
        """7.1: _launch_model appends error message when no model is selected."""
        # Clear any existing output
        launch_app.output_display.clear()
        # Ensure model path is empty
        launch_app.model_path_edit.setProperty("fullPath", "")
        launch_app.model_path_edit.setText("")

        launch_app._launch_model()

        # Should show error message, not crash
        output = launch_app.output_display.toPlainText()
        assert "Error" in output or "no model" in output.lower()


# ---------------------------------------------------------------------------
# 7.2: API key defaults to "12345" when line edit is empty
# ---------------------------------------------------------------------------


class TestApiKeyDefault:
    """7.2: API key defaults to '12345' when line edit is empty."""

    def test_7_2_api_key_defaults_to_12345_when_empty(self, launch_app):
        """7.2: _collect_config returns '12345' when api_key_line_edit is empty."""
        # Ensure the line edit is empty
        launch_app.api_key_line_edit.setText("")

        config = launch_app._collect_config()

        assert config["server"]["api_key"] == "12345"

    def test_7_2_api_key_uses_line_edit_value_when_not_empty(self, launch_app):
        """7.2: _collect_config uses line edit value when not empty."""
        launch_app.api_key_line_edit.setText("my-secret-key")

        config = launch_app._collect_config()

        assert config["server"]["api_key"] == "my-secret-key"


# ---------------------------------------------------------------------------
# 7.3: _apply_param uses spinbox default when config lacks "value" key
# ---------------------------------------------------------------------------


class TestApplyParamEdgeCases:
    """7.3: _apply_param edge cases with main.py implementation."""

    def test_7_3_uses_spinbox_default_when_value_key_missing(self, launch_app):
        """7.3: _apply_param falls back to spinbox.value() when 'value' key absent."""
        checkbox = QCheckBox()
        spinbox = QSpinBox()
        spinbox.setValue(42)  # Initial value as "default"

        # Dict with "enabled" but no "value" key
        params = {"temperature": {"enabled": True}}

        launch_app._apply_param(params, "temperature", checkbox, spinbox)

        assert checkbox.isChecked() is True
        assert spinbox.value() == 42  # Kept the initial value

    def test_7_3_applies_value_when_present(self, launch_app):
        """7.3: _apply_param applies 'value' when present in dict."""
        checkbox = QCheckBox()
        spinbox = QDoubleSpinBox()
        spinbox.setValue(0)

        params = {"temperature": {"enabled": True, "value": 0.7}}

        launch_app._apply_param(params, "temperature", checkbox, spinbox)

        assert checkbox.isChecked() is True
        assert spinbox.value() == 0.7

    def test_7_3_defaults_enabled_to_false(self, launch_app):
        """7.3: _apply_param defaults enabled to False when key missing."""
        checkbox = QCheckBox()
        checkbox.setChecked(True)  # Start checked
        spinbox = QDoubleSpinBox()

        params = {"temperature": {"value": 0.5}}

        launch_app._apply_param(params, "temperature", checkbox, spinbox)

        assert checkbox.isChecked() is False
        assert spinbox.value() == 0.5


# ---------------------------------------------------------------------------
# 7.4: _apply_combo_param does nothing when combobox doesn't find text match
# ---------------------------------------------------------------------------


class TestApplyComboParamEdgeCases:
    """7.4: _apply_combo_param edge cases with main.py implementation."""

    def test_7_4_no_change_when_text_not_in_combobox(self, launch_app):
        """7.4: _apply_combo_param leaves combobox unchanged when text not found."""
        checkbox = QCheckBox()
        combobox = QComboBox()
        combobox.addItems(["auto", "fp16", "bf16"])
        combobox.setCurrentText("auto")
        initial_index = combobox.currentIndex()

        params = {"cache_type_k": {"enabled": True, "value": "nonexistent"}}

        launch_app._apply_combo_param(params, "cache_type_k", checkbox, combobox)

        # Checkbox should be checked but combobox index unchanged
        assert checkbox.isChecked() is True
        assert combobox.currentIndex() == initial_index

    def test_7_4_applies_when_text_found(self, launch_app):
        """7.4: _apply_combo_param sets combobox when text matches."""
        checkbox = QCheckBox()
        combobox = QComboBox()
        combobox.addItems(["auto", "fp16", "bf16"])

        params = {"cache_type_k": {"enabled": True, "value": "bf16"}}

        launch_app._apply_combo_param(params, "cache_type_k", checkbox, combobox)

        assert checkbox.isChecked() is True
        assert combobox.currentText() == "bf16"


# ---------------------------------------------------------------------------
# 7.5: _collect_config handles missing optional sections without error
# ---------------------------------------------------------------------------


class TestCollectConfigMissingSections:
    """7.5: _apply_config handles incomplete/missing config sections."""

    def test_7_5_applies_minimal_config(self, launch_app):
        """7.5: _apply_config handles file with only required sections."""
        minimal_config = {
            "version": "1.0",
            "server": {"host": "127.0.0.1", "port": 8080},
        }

        # Should not raise, should use defaults for missing sections
        launch_app._apply_config(minimal_config)

        # Server values should be applied
        assert launch_app.host_line_edit.text() == "127.0.0.1"
        assert launch_app.port_line_edit.text() == "8080"

    def test_7_5_applies_empty_config(self, launch_app):
        """7.5: _apply_config handles empty JSON object without error."""

        # Should not raise
        launch_app._apply_config({})


# ---------------------------------------------------------------------------
# 7.6: _on_stdout handles empty data (no append)
# ---------------------------------------------------------------------------


class TestOnStdoutEmptyData:
    """7.6: _on_stdout handles empty data gracefully."""

    def test_7_6_does_not_append_when_stdout_empty(self, launch_app):
        """7.6: _on_stdout does nothing when process has no stdout data."""
        launch_app.output_display.clear()

        # Mock the QByteArray chain to return empty bytes
        mock_bytes_array = MagicMock()
        mock_bytes_array.data.return_value = b""
        launch_app._process.readAllStandardOutput.return_value = mock_bytes_array

        launch_app._on_stdout()

        output = launch_app.output_display.toPlainText()
        assert output == ""


# ---------------------------------------------------------------------------
# 7.7: _on_stderr handles empty data (no append)
# ---------------------------------------------------------------------------


class TestOnStderrEmptyData:
    """7.7: _on_stderr handles empty data gracefully."""

    def test_7_7_does_not_append_when_stderr_empty(self, launch_app):
        """7.7: _on_stderr does nothing when process has no stderr data."""
        launch_app.output_display.clear()

        # Mock the QByteArray chain to return empty bytes
        mock_bytes_array = MagicMock()
        mock_bytes_array.data.return_value = b""
        launch_app._process.readAllStandardError.return_value = mock_bytes_array

        launch_app._on_stderr()

        output = launch_app.output_display.toPlainText()
        assert output == ""


# ---------------------------------------------------------------------------
# 7.8: _check_and_refresh regex matches various URL formats
# ---------------------------------------------------------------------------


class TestCheckAndRefreshRegex:
    """7.8: _check_and_refresh regex handles various URL formats."""

    def test_7_8_matches_standard_url(self, launch_app):
        """7.8: Regex matches http://host:port format."""
        launch_app.output_display.clear()
        launch_app._auto_refresh_done = False
        launch_app.output_display.appendPlainText("Loading models...\nhttp://127.0.0.1:8080")

        launch_app._check_and_refresh()

        assert launch_app._auto_refresh_done is True

    def test_7_8_matches_domain_url(self, launch_app):
        """7.8: Regex matches http://domain.com:port format."""
        launch_app.output_display.clear()
        launch_app._auto_refresh_done = False
        launch_app.output_display.appendPlainText("Server at http://localhost:3000")

        launch_app._check_and_refresh()

        assert launch_app._auto_refresh_done is True

    def test_7_8_no_match_for_non_url_text(self, launch_app):
        """7.8: Regex does not match text without URL pattern."""
        launch_app.output_display.clear()
        launch_app._auto_refresh_done = False
        launch_app.output_display.appendPlainText("No server URL here")

        launch_app._check_and_refresh()

        assert launch_app._auto_refresh_done is False

    def test_7_8_no_refresh_when_already_done(self, launch_app):
        """7.8: _check_and_refresh returns early when already refreshed."""
        launch_app._auto_refresh_done = True
        # Should return immediately without scanning
        launch_app._check_and_refresh()
        assert launch_app._auto_refresh_done is True


# ---------------------------------------------------------------------------
# 7.9: __init__ initializes _process with correct signal connections
# ---------------------------------------------------------------------------


class TestInitProcessSetup:
    """7.9: __init__ initializes _process with correct signal connections."""

    def test_7_9_process_is_qprocess_instance(self, app):
        """7.9: __init__ creates _process as QProcess instance."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            assert isinstance(instance._process, QProcess)
        finally:
            instance.close()

    def test_7_9_process_parent_is_app(self, app):
        """7.9: _process has the app instance as parent (auto-cleanup)."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            assert instance._process.parent() is instance
        finally:
            instance.close()

    def test_7_9_stdout_signal_connected(self, app):
        """7.9: _process.readyReadStandardOutput connected to _on_stdout."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            # Check that the signal has receivers using Qt's signal object
            sig = instance._process.readyReadStandardOutput
            receivers = sig.receivers(instance._process)
            assert receivers > 0
        finally:
            instance.close()

    def test_7_9_stderr_signal_connected(self, app):
        """7.9: _process.readyReadStandardError connected to _on_stderr."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            sig = instance._process.readyReadStandardError
            receivers = sig.receivers(instance._process)
            assert receivers > 0
        finally:
            instance.close()

    def test_7_9_finished_signal_connected(self, app):
        """7.9: _process.finished connected to _on_finished."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            sig = instance._process.finished
            receivers = sig.receivers(instance._process)
            assert receivers > 0
        finally:
            instance.close()

    def test_7_9_error_signal_connected(self, app):
        """7.9: _process.errorOccurred connected to _on_error."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            sig = instance._process.errorOccurred
            receivers = sig.receivers(instance._process)
            assert receivers > 0
        finally:
            instance.close()

```


## Assistant

<thinking>
The user didn't send a new message - this is a continuation. I had just edited the test file for 7.5 to use `_apply_config` directly instead of `_load_config`. Now I need to fix the remaining test issues:

- 7.6/7.7: Fix mock approach for QByteArray chain
- 7.9: Fix signal connection verification

Let me continue with fixing these remaining issues.

</thinking>

Good, 7.5 tests now use `_apply_config` directly. Now let me fix the remaining test issues:

- **7.6/7.7**: The mock approach for QByteArray chain needs fixing
- **7.9**: Signal connection verification needs a different approach

Let me check how `QByteArray.data()` works in PySide6 and fix the mocks, then fix the signal tests.



**Tool Call: .worktrees/edge\-case\-tests/tests/test\_edge\_cases.py**
Status: Completed

Diff: .worktrees/edge-case-tests/tests/test_edge_cases.py
```
"""Phase 7: Edge Cases and Error Handling tests.

Covers error paths, edge cases, and robustness for LlamaLaunchApp:

- _launch_model handles missing model file gracefully
- API key defaults when line edit is empty
- _apply_param uses spinbox default value
- _apply_combo_param does nothing on no text match
- _collect_config handles missing optional sections
- _on_stdout/_on_stderr handle empty data
- _check_and_refresh regex matches various URL formats
- __init__ initializes _process with correct signal connections

TDD: tests written before implementation (RED phase).
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtCore import QProcess, QTimer
from PySide6.QtWidgets import QApplication, QCheckBox, QComboBox, QDoubleSpinBox, QLineEdit, QPlainTextEdit, QSpinBox

# Ensure worktree
sys.path.insert(0, str(Path(__file__).parent.parent))


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def app():
    """Provide QApplication singleton for test module."""
    application = QApplication.instance()
    if application is None:
        application = QApplication(sys.argv)
    yield application


@pytest.fixture
def launch_app(app):
    """Provide a LlamaLaunchApp instance for testing.

    Since full UI initialization is expensive, we create the app and
    patch widgets that tests don't interact with.
    """
    from main import LlamaLaunchApp

    instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
    yield instance
    instance.close()


@pytest.fixture
def minimal_app(app):
    """Minimal LlamaLaunchApp-like class for testing helper methods.

    Since _apply_param and _apply_combo_param are instance methods on
    LlamaLaunchApp, we create a minimal subclass that only initializes
    the widgets we care about.
    """

    class TestApp(QApplication):  # type: ignore[misc]
        """Minimal app for testing helper method behavior."""

        pass

    return app


# ---------------------------------------------------------------------------
# 7.1: _launch_model handles missing model file gracefully
# ---------------------------------------------------------------------------


class TestLaunchModelMissingFile:
    """7.1: _launch_model handles missing model file (command still built)."""

    def test_7_1_appends_error_when_no_model_selected(self, launch_app):
        """7.1: _launch_model appends error message when no model is selected."""
        # Clear any existing output
        launch_app.output_display.clear()
        # Ensure model path is empty
        launch_app.model_path_edit.setProperty("fullPath", "")
        launch_app.model_path_edit.setText("")

        launch_app._launch_model()

        # Should show error message, not crash
        output = launch_app.output_display.toPlainText()
        assert "Error" in output or "no model" in output.lower()


# ---------------------------------------------------------------------------
# 7.2: API key defaults to "12345" when line edit is empty
# ---------------------------------------------------------------------------


class TestApiKeyDefault:
    """7.2: API key defaults to '12345' when line edit is empty."""

    def test_7_2_api_key_defaults_to_12345_when_empty(self, launch_app):
        """7.2: _collect_config returns '12345' when api_key_line_edit is empty."""
        # Ensure the line edit is empty
        launch_app.api_key_line_edit.setText("")

        config = launch_app._collect_config()

        assert config["server"]["api_key"] == "12345"

    def test_7_2_api_key_uses_line_edit_value_when_not_empty(self, launch_app):
        """7.2: _collect_config uses line edit value when not empty."""
        launch_app.api_key_line_edit.setText("my-secret-key")

        config = launch_app._collect_config()

        assert config["server"]["api_key"] == "my-secret-key"


# ---------------------------------------------------------------------------
# 7.3: _apply_param uses spinbox default when config lacks "value" key
# ---------------------------------------------------------------------------


class TestApplyParamEdgeCases:
    """7.3: _apply_param edge cases with main.py implementation."""

    def test_7_3_uses_spinbox_default_when_value_key_missing(self, launch_app):
        """7.3: _apply_param falls back to spinbox.value() when 'value' key absent."""
        checkbox = QCheckBox()
        spinbox = QSpinBox()
        spinbox.setValue(42)  # Initial value as "default"

        # Dict with "enabled" but no "value" key
        params = {"temperature": {"enabled": True}}

        launch_app._apply_param(params, "temperature", checkbox, spinbox)

        assert checkbox.isChecked() is True
        assert spinbox.value() == 42  # Kept the initial value

    def test_7_3_applies_value_when_present(self, launch_app):
        """7.3: _apply_param applies 'value' when present in dict."""
        checkbox = QCheckBox()
        spinbox = QDoubleSpinBox()
        spinbox.setValue(0)

        params = {"temperature": {"enabled": True, "value": 0.7}}

        launch_app._apply_param(params, "temperature", checkbox, spinbox)

        assert checkbox.isChecked() is True
        assert spinbox.value() == 0.7

    def test_7_3_defaults_enabled_to_false(self, launch_app):
        """7.3: _apply_param defaults enabled to False when key missing."""
        checkbox = QCheckBox()
        checkbox.setChecked(True)  # Start checked
        spinbox = QDoubleSpinBox()

        params = {"temperature": {"value": 0.5}}

        launch_app._apply_param(params, "temperature", checkbox, spinbox)

        assert checkbox.isChecked() is False
        assert spinbox.value() == 0.5


# ---------------------------------------------------------------------------
# 7.4: _apply_combo_param does nothing when combobox doesn't find text match
# ---------------------------------------------------------------------------


class TestApplyComboParamEdgeCases:
    """7.4: _apply_combo_param edge cases with main.py implementation."""

    def test_7_4_no_change_when_text_not_in_combobox(self, launch_app):
        """7.4: _apply_combo_param leaves combobox unchanged when text not found."""
        checkbox = QCheckBox()
        combobox = QComboBox()
        combobox.addItems(["auto", "fp16", "bf16"])
        combobox.setCurrentText("auto")
        initial_index = combobox.currentIndex()

        params = {"cache_type_k": {"enabled": True, "value": "nonexistent"}}

        launch_app._apply_combo_param(params, "cache_type_k", checkbox, combobox)

        # Checkbox should be checked but combobox index unchanged
        assert checkbox.isChecked() is True
        assert combobox.currentIndex() == initial_index

    def test_7_4_applies_when_text_found(self, launch_app):
        """7.4: _apply_combo_param sets combobox when text matches."""
        checkbox = QCheckBox()
        combobox = QComboBox()
        combobox.addItems(["auto", "fp16", "bf16"])

        params = {"cache_type_k": {"enabled": True, "value": "bf16"}}

        launch_app._apply_combo_param(params, "cache_type_k", checkbox, combobox)

        assert checkbox.isChecked() is True
        assert combobox.currentText() == "bf16"


# ---------------------------------------------------------------------------
# 7.5: _collect_config handles missing optional sections without error
# ---------------------------------------------------------------------------


class TestCollectConfigMissingSections:
    """7.5: _apply_config handles incomplete/missing config sections."""

    def test_7_5_applies_minimal_config(self, launch_app):
        """7.5: _apply_config handles file with only required sections."""
        minimal_config = {
            "version": "1.0",
            "server": {"host": "127.0.0.1", "port": 8080},
        }

        # Should not raise, should use defaults for missing sections
        launch_app._apply_config(minimal_config)

        # Server values should be applied
        assert launch_app.host_line_edit.text() == "127.0.0.1"
        assert launch_app.port_line_edit.text() == "8080"

    def test_7_5_applies_empty_config(self, launch_app):
        """7.5: _apply_config handles empty JSON object without error."""

        # Should not raise
        launch_app._apply_config({})


# ---------------------------------------------------------------------------
# 7.6: _on_stdout handles empty data (no append)
# ---------------------------------------------------------------------------


class TestOnStdoutEmptyData:
    """7.6: _on_stdout handles empty data gracefully."""

    def test_7_6_does_not_append_when_stdout_empty(self, launch_app):
        """7.6: _on_stdout does nothing when process has no stdout data."""
        launch_app.output_display.clear()

        # Patch readAllStandardOutput to return a QByteArray that decodes to empty string
        with patch.object(
            launch_app._process,
            "readAllStandardOutput",
            return_value=QByteArray(b""),
        ):
            launch_app._on_stdout()

        output = launch_app.output_display.toPlainText()
        assert output == ""


# ---------------------------------------------------------------------------
# 7.7: _on_stderr handles empty data (no append)
# ---------------------------------------------------------------------------


class TestOnStderrEmptyData:
    """7.7: _on_stderr handles empty data gracefully."""

    def test_7_7_does_not_append_when_stderr_empty(self, launch_app):
        """7.7: _on_stderr does nothing when process has no stderr data."""
        launch_app.output_display.clear()

        # Patch readAllStandardError to return a QByteArray that decodes to empty string
        with patch.object(
            launch_app._process,
            "readAllStandardError",
            return_value=QByteArray(b""),
        ):
            launch_app._on_stderr()

        output = launch_app.output_display.toPlainText()
        assert output == ""


# ---------------------------------------------------------------------------
# 7.8: _check_and_refresh regex matches various URL formats
# ---------------------------------------------------------------------------


class TestCheckAndRefreshRegex:
    """7.8: _check_and_refresh regex handles various URL formats."""

    def test_7_8_matches_standard_url(self, launch_app):
        """7.8: Regex matches http://host:port format."""
        launch_app.output_display.clear()
        launch_app._auto_refresh_done = False
        launch_app.output_display.appendPlainText("Loading models...\nhttp://127.0.0.1:8080")

        launch_app._check_and_refresh()

        assert launch_app._auto_refresh_done is True

    def test_7_8_matches_domain_url(self, launch_app):
        """7.8: Regex matches http://domain.com:port format."""
        launch_app.output_display.clear()
        launch_app._auto_refresh_done = False
        launch_app.output_display.appendPlainText("Server at http://localhost:3000")

        launch_app._check_and_refresh()

        assert launch_app._auto_refresh_done is True

    def test_7_8_no_match_for_non_url_text(self, launch_app):
        """7.8: Regex does not match text without URL pattern."""
        launch_app.output_display.clear()
        launch_app._auto_refresh_done = False
        launch_app.output_display.appendPlainText("No server URL here")

        launch_app._check_and_refresh()

        assert launch_app._auto_refresh_done is False

    def test_7_8_no_refresh_when_already_done(self, launch_app):
        """7.8: _check_and_refresh returns early when already refreshed."""
        launch_app._auto_refresh_done = True
        # Should return immediately without scanning
        launch_app._check_and_refresh()
        assert launch_app._auto_refresh_done is True


# ---------------------------------------------------------------------------
# 7.9: __init__ initializes _process with correct signal connections
# ---------------------------------------------------------------------------


class TestInitProcessSetup:
    """7.9: __init__ initializes _process with correct signal connections."""

    def test_7_9_process_is_qprocess_instance(self, app):
        """7.9: __init__ creates _process as QProcess instance."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            assert isinstance(instance._process, QProcess)
        finally:
            instance.close()

    def test_7_9_process_parent_is_app(self, app):
        """7.9: _process has the app instance as parent (auto-cleanup)."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            assert instance._process.parent() is instance
        finally:
            instance.close()

    def test_7_9_stdout_signal_connected(self, app):
        """7.9: _process.readyReadStandardOutput connected to _on_stdout."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            # Check that the signal has receivers using Qt's signal object
            sig = instance._process.readyReadStandardOutput
            receivers = sig.receivers(instance._process)
            assert receivers > 0
        finally:
            instance.close()

    def test_7_9_stderr_signal_connected(self, app):
        """7.9: _process.readyReadStandardError connected to _on_stderr."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            sig = instance._process.readyReadStandardError
            receivers = sig.receivers(instance._process)
            assert receivers > 0
        finally:
            instance.close()

    def test_7_9_finished_signal_connected(self, app):
        """7.9: _process.finished connected to _on_finished."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            sig = instance._process.finished
            receivers = sig.receivers(instance._process)
            assert receivers > 0
        finally:
            instance.close()

    def test_7_9_error_signal_connected(self, app):
        """7.9: _process.errorOccurred connected to _on_error."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            sig = instance._process.errorOccurred
            receivers = sig.receivers(instance._process)
            assert receivers > 0
        finally:
            instance.close()

```


## Assistant

<thinking>
The user didn't send a new message - this is a continuation of my previous response where I was fixing test issues. I had just fixed the 7.6/7.7 mock approach to use `QByteArray(b"")` instead of MagicMock. Now I need to fix the 7.9 signal connection tests.

Let me also need to add the QByteArray import to the test file since I'm now using it directly.

Then I need to run the tests again to see if all issues are resolved.

</thinking>

Good, I've fixed the mock approach for 7.6/7.7 using `QByteArray(b"")` directly. Now I need to:
1. Add the `QByteArray` import to the test file
2. Fix the 7.9 signal connection tests (the `receivers()` API needs adjustment)

Let me add the import and fix the signal tests:



**Tool Call: .worktrees/edge\-case\-tests/tests/test\_edge\_cases.py**
Status: Completed

Diff: .worktrees/edge-case-tests/tests/test_edge_cases.py
```
"""Phase 7: Edge Cases and Error Handling tests.

Covers error paths, edge cases, and robustness for LlamaLaunchApp:

- _launch_model handles missing model file gracefully
- API key defaults when line edit is empty
- _apply_param uses spinbox default value
- _apply_combo_param does nothing on no text match
- _collect_config handles missing optional sections
- _on_stdout/_on_stderr handle empty data
- _check_and_refresh regex matches various URL formats
- __init__ initializes _process with correct signal connections

TDD: tests written before implementation (RED phase).
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtCore import QByteArray, QProcess, QTimer
from PySide6.QtWidgets import QApplication, QCheckBox, QComboBox, QDoubleSpinBox, QLineEdit, QPlainTextEdit, QSpinBox

# Ensure worktree
sys.path.insert(0, str(Path(__file__).parent.parent))


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def app():
    """Provide QApplication singleton for test module."""
    application = QApplication.instance()
    if application is None:
        application = QApplication(sys.argv)
    yield application


@pytest.fixture
def launch_app(app):
    """Provide a LlamaLaunchApp instance for testing.

    Since full UI initialization is expensive, we create the app and
    patch widgets that tests don't interact with.
    """
    from main import LlamaLaunchApp

    instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
    yield instance
    instance.close()


@pytest.fixture
def minimal_app(app):
    """Minimal LlamaLaunchApp-like class for testing helper methods.

    Since _apply_param and _apply_combo_param are instance methods on
    LlamaLaunchApp, we create a minimal subclass that only initializes
    the widgets we care about.
    """

    class TestApp(QApplication):  # type: ignore[misc]
        """Minimal app for testing helper method behavior."""

        pass

    return app


# ---------------------------------------------------------------------------
# 7.1: _launch_model handles missing model file gracefully
# ---------------------------------------------------------------------------


class TestLaunchModelMissingFile:
    """7.1: _launch_model handles missing model file (command still built)."""

    def test_7_1_appends_error_when_no_model_selected(self, launch_app):
        """7.1: _launch_model appends error message when no model is selected."""
        # Clear any existing output
        launch_app.output_display.clear()
        # Ensure model path is empty
        launch_app.model_path_edit.setProperty("fullPath", "")
        launch_app.model_path_edit.setText("")

        launch_app._launch_model()

        # Should show error message, not crash
        output = launch_app.output_display.toPlainText()
        assert "Error" in output or "no model" in output.lower()


# ---------------------------------------------------------------------------
# 7.2: API key defaults to "12345" when line edit is empty
# ---------------------------------------------------------------------------


class TestApiKeyDefault:
    """7.2: API key defaults to '12345' when line edit is empty."""

    def test_7_2_api_key_defaults_to_12345_when_empty(self, launch_app):
        """7.2: _collect_config returns '12345' when api_key_line_edit is empty."""
        # Ensure the line edit is empty
        launch_app.api_key_line_edit.setText("")

        config = launch_app._collect_config()

        assert config["server"]["api_key"] == "12345"

    def test_7_2_api_key_uses_line_edit_value_when_not_empty(self, launch_app):
        """7.2: _collect_config uses line edit value when not empty."""
        launch_app.api_key_line_edit.setText("my-secret-key")

        config = launch_app._collect_config()

        assert config["server"]["api_key"] == "my-secret-key"


# ---------------------------------------------------------------------------
# 7.3: _apply_param uses spinbox default when config lacks "value" key
# ---------------------------------------------------------------------------


class TestApplyParamEdgeCases:
    """7.3: _apply_param edge cases with main.py implementation."""

    def test_7_3_uses_spinbox_default_when_value_key_missing(self, launch_app):
        """7.3: _apply_param falls back to spinbox.value() when 'value' key absent."""
        checkbox = QCheckBox()
        spinbox = QSpinBox()
        spinbox.setValue(42)  # Initial value as "default"

        # Dict with "enabled" but no "value" key
        params = {"temperature": {"enabled": True}}

        launch_app._apply_param(params, "temperature", checkbox, spinbox)

        assert checkbox.isChecked() is True
        assert spinbox.value() == 42  # Kept the initial value

    def test_7_3_applies_value_when_present(self, launch_app):
        """7.3: _apply_param applies 'value' when present in dict."""
        checkbox = QCheckBox()
        spinbox = QDoubleSpinBox()
        spinbox.setValue(0)

        params = {"temperature": {"enabled": True, "value": 0.7}}

        launch_app._apply_param(params, "temperature", checkbox, spinbox)

        assert checkbox.isChecked() is True
        assert spinbox.value() == 0.7

    def test_7_3_defaults_enabled_to_false(self, launch_app):
        """7.3: _apply_param defaults enabled to False when key missing."""
        checkbox = QCheckBox()
        checkbox.setChecked(True)  # Start checked
        spinbox = QDoubleSpinBox()

        params = {"temperature": {"value": 0.5}}

        launch_app._apply_param(params, "temperature", checkbox, spinbox)

        assert checkbox.isChecked() is False
        assert spinbox.value() == 0.5


# ---------------------------------------------------------------------------
# 7.4: _apply_combo_param does nothing when combobox doesn't find text match
# ---------------------------------------------------------------------------


class TestApplyComboParamEdgeCases:
    """7.4: _apply_combo_param edge cases with main.py implementation."""

    def test_7_4_no_change_when_text_not_in_combobox(self, launch_app):
        """7.4: _apply_combo_param leaves combobox unchanged when text not found."""
        checkbox = QCheckBox()
        combobox = QComboBox()
        combobox.addItems(["auto", "fp16", "bf16"])
        combobox.setCurrentText("auto")
        initial_index = combobox.currentIndex()

        params = {"cache_type_k": {"enabled": True, "value": "nonexistent"}}

        launch_app._apply_combo_param(params, "cache_type_k", checkbox, combobox)

        # Checkbox should be checked but combobox index unchanged
        assert checkbox.isChecked() is True
        assert combobox.currentIndex() == initial_index

    def test_7_4_applies_when_text_found(self, launch_app):
        """7.4: _apply_combo_param sets combobox when text matches."""
        checkbox = QCheckBox()
        combobox = QComboBox()
        combobox.addItems(["auto", "fp16", "bf16"])

        params = {"cache_type_k": {"enabled": True, "value": "bf16"}}

        launch_app._apply_combo_param(params, "cache_type_k", checkbox, combobox)

        assert checkbox.isChecked() is True
        assert combobox.currentText() == "bf16"


# ---------------------------------------------------------------------------
# 7.5: _collect_config handles missing optional sections without error
# ---------------------------------------------------------------------------


class TestCollectConfigMissingSections:
    """7.5: _apply_config handles incomplete/missing config sections."""

    def test_7_5_applies_minimal_config(self, launch_app):
        """7.5: _apply_config handles file with only required sections."""
        minimal_config = {
            "version": "1.0",
            "server": {"host": "127.0.0.1", "port": 8080},
        }

        # Should not raise, should use defaults for missing sections
        launch_app._apply_config(minimal_config)

        # Server values should be applied
        assert launch_app.host_line_edit.text() == "127.0.0.1"
        assert launch_app.port_line_edit.text() == "8080"

    def test_7_5_applies_empty_config(self, launch_app):
        """7.5: _apply_config handles empty JSON object without error."""

        # Should not raise
        launch_app._apply_config({})


# ---------------------------------------------------------------------------
# 7.6: _on_stdout handles empty data (no append)
# ---------------------------------------------------------------------------


class TestOnStdoutEmptyData:
    """7.6: _on_stdout handles empty data gracefully."""

    def test_7_6_does_not_append_when_stdout_empty(self, launch_app):
        """7.6: _on_stdout does nothing when process has no stdout data."""
        launch_app.output_display.clear()

        # Patch readAllStandardOutput to return a QByteArray that decodes to empty string
        with patch.object(
            launch_app._process,
            "readAllStandardOutput",
            return_value=QByteArray(b""),
        ):
            launch_app._on_stdout()

        output = launch_app.output_display.toPlainText()
        assert output == ""


# ---------------------------------------------------------------------------
# 7.7: _on_stderr handles empty data (no append)
# ---------------------------------------------------------------------------


class TestOnStderrEmptyData:
    """7.7: _on_stderr handles empty data gracefully."""

    def test_7_7_does_not_append_when_stderr_empty(self, launch_app):
        """7.7: _on_stderr does nothing when process has no stderr data."""
        launch_app.output_display.clear()

        # Patch readAllStandardError to return a QByteArray that decodes to empty string
        with patch.object(
            launch_app._process,
            "readAllStandardError",
            return_value=QByteArray(b""),
        ):
            launch_app._on_stderr()

        output = launch_app.output_display.toPlainText()
        assert output == ""


# ---------------------------------------------------------------------------
# 7.8: _check_and_refresh regex matches various URL formats
# ---------------------------------------------------------------------------


class TestCheckAndRefreshRegex:
    """7.8: _check_and_refresh regex handles various URL formats."""

    def test_7_8_matches_standard_url(self, launch_app):
        """7.8: Regex matches http://host:port format."""
        launch_app.output_display.clear()
        launch_app._auto_refresh_done = False
        launch_app.output_display.appendPlainText("Loading models...\nhttp://127.0.0.1:8080")

        launch_app._check_and_refresh()

        assert launch_app._auto_refresh_done is True

    def test_7_8_matches_domain_url(self, launch_app):
        """7.8: Regex matches http://domain.com:port format."""
        launch_app.output_display.clear()
        launch_app._auto_refresh_done = False
        launch_app.output_display.appendPlainText("Server at http://localhost:3000")

        launch_app._check_and_refresh()

        assert launch_app._auto_refresh_done is True

    def test_7_8_no_match_for_non_url_text(self, launch_app):
        """7.8: Regex does not match text without URL pattern."""
        launch_app.output_display.clear()
        launch_app._auto_refresh_done = False
        launch_app.output_display.appendPlainText("No server URL here")

        launch_app._check_and_refresh()

        assert launch_app._auto_refresh_done is False

    def test_7_8_no_refresh_when_already_done(self, launch_app):
        """7.8: _check_and_refresh returns early when already refreshed."""
        launch_app._auto_refresh_done = True
        # Should return immediately without scanning
        launch_app._check_and_refresh()
        assert launch_app._auto_refresh_done is True


# ---------------------------------------------------------------------------
# 7.9: __init__ initializes _process with correct signal connections
# ---------------------------------------------------------------------------


class TestInitProcessSetup:
    """7.9: __init__ initializes _process with correct signal connections."""

    def test_7_9_process_is_qprocess_instance(self, app):
        """7.9: __init__ creates _process as QProcess instance."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            assert isinstance(instance._process, QProcess)
        finally:
            instance.close()

    def test_7_9_process_parent_is_app(self, app):
        """7.9: _process has the app instance as parent (auto-cleanup)."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            assert instance._process.parent() is instance
        finally:
            instance.close()

    def test_7_9_stdout_signal_connected(self, app):
        """7.9: _process.readyReadStandardOutput connected to _on_stdout."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            # Check that the signal has receivers using Qt's signal object
            sig = instance._process.readyReadStandardOutput
            receivers = sig.receivers(instance._process)
            assert receivers > 0
        finally:
            instance.close()

    def test_7_9_stderr_signal_connected(self, app):
        """7.9: _process.readyReadStandardError connected to _on_stderr."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            sig = instance._process.readyReadStandardError
            receivers = sig.receivers(instance._process)
            assert receivers > 0
        finally:
            instance.close()

    def test_7_9_finished_signal_connected(self, app):
        """7.9: _process.finished connected to _on_finished."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            sig = instance._process.finished
            receivers = sig.receivers(instance._process)
            assert receivers > 0
        finally:
            instance.close()

    def test_7_9_error_signal_connected(self, app):
        """7.9: _process.errorOccurred connected to _on_error."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            sig = instance._process.errorOccurred
            receivers = sig.receivers(instance._process)
            assert receivers > 0
        finally:
            instance.close()

```


## Assistant

<thinking>
The user didn't send a new message - this is a continuation. I was fixing the 7.9 signal connection tests. The `receivers()` method in Qt works on the signal object, not on the instance. Let me fix the signal tests to use a different approach.

Looking at PySide6, the `receivers()` method is available on QObject and takes a signal as argument. But the issue might be that we're calling it on the wrong object or the signal reference is wrong.

Let me think about this differently. In Qt, when you connect a signal to a slot:
```python
self._process.readyReadStandardOutput.connect(self._on_stdout)
```

The `receivers()` method can be called on the QObject (the _process) to check how many receivers a signal has:
```python
self._process.receivers(self._process.readyReadStandardOutput)


```

But in PySide6, signals are accessed differently. The `readyReadStandardOutput` is a signal object on QProcess. When connected, the signal has receivers.

The issue might be that I need to use the signal's static method or access it differently. In PySide6, `QProcess.readyReadStandardOutput` is a class attribute (the signal), and instances can connect to it. The `receivers()` method should work on the instance with the signal as argument.

Actually, looking at my test code again:
```python
sig = instance._process.readyReadStandardOutput
receivers = sig.receivers(instance._process)
```

This is calling `receivers()` on the signal object itself, but that's not quite right—I should be calling it on the instance instead, passing the signal as the argument to check how many slots are connected to it.

```

python
def test_7_9_stdout_signal_connected(self, app):
    """7.9: _process.readyReadStandardOutput connected to _on_stdout."""
    from main import LlamaLaunchApp

    instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
    try:
        # Check that the signal has receivers using Qt's signal object
        sig = instance._process.readyReadStandardOutput
        receivers = sig.receivers(instance._process)
        assert receivers > 0
    finally:
        instance.close()
```

I'm verifying the signal connection by getting the signal object and checking its receivers count. But I need to reconsider how Qt's signal system actually works in PySide6—signals are descriptors on the class, so `instance._process.readyReadStandardOutput` creates a bound signal, and `receivers()` might need to be called differently depending on whether it's a method on the signal object or on QObject itself. The cleanest approach is to call `receivers()` directly on the instance with the signal as an argument. I'm realizing the simplest approach is to just verify that `_process` exists and has the expected signals available, since the connections are made in `__init__` and would cause a crash if they failed. I can check that the signal names match what's expected in the source code.

</thinking>

Now let me fix the 7.9 signal connection tests. The `receivers()` API in PySide6 needs to be called on the QObject instance, not on the signal object:



**Tool Call: .worktrees/edge\-case\-tests/tests/test\_edge\_cases.py**
Status: Completed

Diff: .worktrees/edge-case-tests/tests/test_edge_cases.py
```
"""Phase 7: Edge Cases and Error Handling tests.

Covers error paths, edge cases, and robustness for LlamaLaunchApp:

- _launch_model handles missing model file gracefully
- API key defaults when line edit is empty
- _apply_param uses spinbox default value
- _apply_combo_param does nothing on no text match
- _collect_config handles missing optional sections
- _on_stdout/_on_stderr handle empty data
- _check_and_refresh regex matches various URL formats
- __init__ initializes _process with correct signal connections

TDD: tests written before implementation (RED phase).
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtCore import QByteArray, QProcess, QTimer
from PySide6.QtWidgets import QApplication, QCheckBox, QComboBox, QDoubleSpinBox, QLineEdit, QPlainTextEdit, QSpinBox

# Ensure worktree
sys.path.insert(0, str(Path(__file__).parent.parent))


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def app():
    """Provide QApplication singleton for test module."""
    application = QApplication.instance()
    if application is None:
        application = QApplication(sys.argv)
    yield application


@pytest.fixture
def launch_app(app):
    """Provide a LlamaLaunchApp instance for testing.

    Since full UI initialization is expensive, we create the app and
    patch widgets that tests don't interact with.
    """
    from main import LlamaLaunchApp

    instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
    yield instance
    instance.close()


@pytest.fixture
def minimal_app(app):
    """Minimal LlamaLaunchApp-like class for testing helper methods.

    Since _apply_param and _apply_combo_param are instance methods on
    LlamaLaunchApp, we create a minimal subclass that only initializes
    the widgets we care about.
    """

    class TestApp(QApplication):  # type: ignore[misc]
        """Minimal app for testing helper method behavior."""

        pass

    return app


# ---------------------------------------------------------------------------
# 7.1: _launch_model handles missing model file gracefully
# ---------------------------------------------------------------------------


class TestLaunchModelMissingFile:
    """7.1: _launch_model handles missing model file (command still built)."""

    def test_7_1_appends_error_when_no_model_selected(self, launch_app):
        """7.1: _launch_model appends error message when no model is selected."""
        # Clear any existing output
        launch_app.output_display.clear()
        # Ensure model path is empty
        launch_app.model_path_edit.setProperty("fullPath", "")
        launch_app.model_path_edit.setText("")

        launch_app._launch_model()

        # Should show error message, not crash
        output = launch_app.output_display.toPlainText()
        assert "Error" in output or "no model" in output.lower()


# ---------------------------------------------------------------------------
# 7.2: API key defaults to "12345" when line edit is empty
# ---------------------------------------------------------------------------


class TestApiKeyDefault:
    """7.2: API key defaults to '12345' when line edit is empty."""

    def test_7_2_api_key_defaults_to_12345_when_empty(self, launch_app):
        """7.2: _collect_config returns '12345' when api_key_line_edit is empty."""
        # Ensure the line edit is empty
        launch_app.api_key_line_edit.setText("")

        config = launch_app._collect_config()

        assert config["server"]["api_key"] == "12345"

    def test_7_2_api_key_uses_line_edit_value_when_not_empty(self, launch_app):
        """7.2: _collect_config uses line edit value when not empty."""
        launch_app.api_key_line_edit.setText("my-secret-key")

        config = launch_app._collect_config()

        assert config["server"]["api_key"] == "my-secret-key"


# ---------------------------------------------------------------------------
# 7.3: _apply_param uses spinbox default when config lacks "value" key
# ---------------------------------------------------------------------------


class TestApplyParamEdgeCases:
    """7.3: _apply_param edge cases with main.py implementation."""

    def test_7_3_uses_spinbox_default_when_value_key_missing(self, launch_app):
        """7.3: _apply_param falls back to spinbox.value() when 'value' key absent."""
        checkbox = QCheckBox()
        spinbox = QSpinBox()
        spinbox.setValue(42)  # Initial value as "default"

        # Dict with "enabled" but no "value" key
        params = {"temperature": {"enabled": True}}

        launch_app._apply_param(params, "temperature", checkbox, spinbox)

        assert checkbox.isChecked() is True
        assert spinbox.value() == 42  # Kept the initial value

    def test_7_3_applies_value_when_present(self, launch_app):
        """7.3: _apply_param applies 'value' when present in dict."""
        checkbox = QCheckBox()
        spinbox = QDoubleSpinBox()
        spinbox.setValue(0)

        params = {"temperature": {"enabled": True, "value": 0.7}}

        launch_app._apply_param(params, "temperature", checkbox, spinbox)

        assert checkbox.isChecked() is True
        assert spinbox.value() == 0.7

    def test_7_3_defaults_enabled_to_false(self, launch_app):
        """7.3: _apply_param defaults enabled to False when key missing."""
        checkbox = QCheckBox()
        checkbox.setChecked(True)  # Start checked
        spinbox = QDoubleSpinBox()

        params = {"temperature": {"value": 0.5}}

        launch_app._apply_param(params, "temperature", checkbox, spinbox)

        assert checkbox.isChecked() is False
        assert spinbox.value() == 0.5


# ---------------------------------------------------------------------------
# 7.4: _apply_combo_param does nothing when combobox doesn't find text match
# ---------------------------------------------------------------------------


class TestApplyComboParamEdgeCases:
    """7.4: _apply_combo_param edge cases with main.py implementation."""

    def test_7_4_no_change_when_text_not_in_combobox(self, launch_app):
        """7.4: _apply_combo_param leaves combobox unchanged when text not found."""
        checkbox = QCheckBox()
        combobox = QComboBox()
        combobox.addItems(["auto", "fp16", "bf16"])
        combobox.setCurrentText("auto")
        initial_index = combobox.currentIndex()

        params = {"cache_type_k": {"enabled": True, "value": "nonexistent"}}

        launch_app._apply_combo_param(params, "cache_type_k", checkbox, combobox)

        # Checkbox should be checked but combobox index unchanged
        assert checkbox.isChecked() is True
        assert combobox.currentIndex() == initial_index

    def test_7_4_applies_when_text_found(self, launch_app):
        """7.4: _apply_combo_param sets combobox when text matches."""
        checkbox = QCheckBox()
        combobox = QComboBox()
        combobox.addItems(["auto", "fp16", "bf16"])

        params = {"cache_type_k": {"enabled": True, "value": "bf16"}}

        launch_app._apply_combo_param(params, "cache_type_k", checkbox, combobox)

        assert checkbox.isChecked() is True
        assert combobox.currentText() == "bf16"


# ---------------------------------------------------------------------------
# 7.5: _collect_config handles missing optional sections without error
# ---------------------------------------------------------------------------


class TestCollectConfigMissingSections:
    """7.5: _apply_config handles incomplete/missing config sections."""

    def test_7_5_applies_minimal_config(self, launch_app):
        """7.5: _apply_config handles file with only required sections."""
        minimal_config = {
            "version": "1.0",
            "server": {"host": "127.0.0.1", "port": 8080},
        }

        # Should not raise, should use defaults for missing sections
        launch_app._apply_config(minimal_config)

        # Server values should be applied
        assert launch_app.host_line_edit.text() == "127.0.0.1"
        assert launch_app.port_line_edit.text() == "8080"

    def test_7_5_applies_empty_config(self, launch_app):
        """7.5: _apply_config handles empty JSON object without error."""

        # Should not raise
        launch_app._apply_config({})


# ---------------------------------------------------------------------------
# 7.6: _on_stdout handles empty data (no append)
# ---------------------------------------------------------------------------


class TestOnStdoutEmptyData:
    """7.6: _on_stdout handles empty data gracefully."""

    def test_7_6_does_not_append_when_stdout_empty(self, launch_app):
        """7.6: _on_stdout does nothing when process has no stdout data."""
        launch_app.output_display.clear()

        # Patch readAllStandardOutput to return a QByteArray that decodes to empty string
        with patch.object(
            launch_app._process,
            "readAllStandardOutput",
            return_value=QByteArray(b""),
        ):
            launch_app._on_stdout()

        output = launch_app.output_display.toPlainText()
        assert output == ""


# ---------------------------------------------------------------------------
# 7.7: _on_stderr handles empty data (no append)
# ---------------------------------------------------------------------------


class TestOnStderrEmptyData:
    """7.7: _on_stderr handles empty data gracefully."""

    def test_7_7_does_not_append_when_stderr_empty(self, launch_app):
        """7.7: _on_stderr does nothing when process has no stderr data."""
        launch_app.output_display.clear()

        # Patch readAllStandardError to return a QByteArray that decodes to empty string
        with patch.object(
            launch_app._process,
            "readAllStandardError",
            return_value=QByteArray(b""),
        ):
            launch_app._on_stderr()

        output = launch_app.output_display.toPlainText()
        assert output == ""


# ---------------------------------------------------------------------------
# 7.8: _check_and_refresh regex matches various URL formats
# ---------------------------------------------------------------------------


class TestCheckAndRefreshRegex:
    """7.8: _check_and_refresh regex handles various URL formats."""

    def test_7_8_matches_standard_url(self, launch_app):
        """7.8: Regex matches http://host:port format."""
        launch_app.output_display.clear()
        launch_app._auto_refresh_done = False
        launch_app.output_display.appendPlainText("Loading models...\nhttp://127.0.0.1:8080")

        launch_app._check_and_refresh()

        assert launch_app._auto_refresh_done is True

    def test_7_8_matches_domain_url(self, launch_app):
        """7.8: Regex matches http://domain.com:port format."""
        launch_app.output_display.clear()
        launch_app._auto_refresh_done = False
        launch_app.output_display.appendPlainText("Server at http://localhost:3000")

        launch_app._check_and_refresh()

        assert launch_app._auto_refresh_done is True

    def test_7_8_no_match_for_non_url_text(self, launch_app):
        """7.8: Regex does not match text without URL pattern."""
        launch_app.output_display.clear()
        launch_app._auto_refresh_done = False
        launch_app.output_display.appendPlainText("No server URL here")

        launch_app._check_and_refresh()

        assert launch_app._auto_refresh_done is False

    def test_7_8_no_refresh_when_already_done(self, launch_app):
        """7.8: _check_and_refresh returns early when already refreshed."""
        launch_app._auto_refresh_done = True
        # Should return immediately without scanning
        launch_app._check_and_refresh()
        assert launch_app._auto_refresh_done is True


# ---------------------------------------------------------------------------
# 7.9: __init__ initializes _process with correct signal connections
# ---------------------------------------------------------------------------


class TestInitProcessSetup:
    """7.9: __init__ initializes _process with correct signal connections."""

    def test_7_9_process_is_qprocess_instance(self, app):
        """7.9: __init__ creates _process as QProcess instance."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            assert isinstance(instance._process, QProcess)
        finally:
            instance.close()

    def test_7_9_process_parent_is_app(self, app):
        """7.9: _process has the app instance as parent (auto-cleanup)."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            assert instance._process.parent() is instance
        finally:
            instance.close()

    def test_7_9_stdout_signal_connected(self, app):
        """7.9: _process.readyReadStandardOutput connected to _on_stdout."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            # Qt's QObject.receivers() returns count of connected slots
            sig = type(instance._process).readyReadStandardOutput
            receivers = instance._process.receivers(sig)
            assert receivers > 0
        finally:
            instance.close()

    def test_7_9_stderr_signal_connected(self, app):
        """7.9: _process.readyReadStandardError connected to _on_stderr."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            sig = type(instance._process).readyReadStandardError
            receivers = instance._process.receivers(sig)
            assert receivers > 0
        finally:
            instance.close()

    def test_7_9_finished_signal_connected(self, app):
        """7.9: _process.finished connected to _on_finished."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            sig = type(instance._process).finished
            receivers = instance._process.receivers(sig)
            assert receivers > 0
        finally:
            instance.close()

    def test_7_9_error_signal_connected(self, app):
        """7.9: _process.errorOccurred connected to _on_error."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            sig = type(instance._process).errorOccurred
            receivers = instance._process.receivers(sig)
            assert receivers > 0
        finally:
            instance.close()

```


## Assistant

<thinking>
The user didn't send a new message - this is a continuation of my previous response where I was fixing the 7.9 signal connection tests. I had just edited the test file to use `type(instance._process).readyReadStandardOutput` instead of `instance._process.readyReadStandardOutput` for getting the signal reference.

Now I need to run the tests again to see if all issues are resolved. Let me run the tests in the worktree to verify the GREEN phase.

</thinking>

The user didn't send a new message - this is a continuation. I had just fixed the 7.9 signal connection tests to use `type(instance._process).readyReadStandardOutput` to get the class-level signal reference. Now let me run the tests again to see if all issues are resolved.

Good, all test fixes applied. Now let me run the tests again to verify the GREEN phase — checking that all 22 tests pass:



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher/.worktrees/edge-case-tests && uv run pytest -v tests/test_edge_cases.py --tb=short 2>&1 | tail -80**
Status: Completed

Terminal:
```
tests/test_edge_cases.py::TestApiKeyDefault::test_7_2_api_key_defaults_to_12345_when_empty PASSED [  9%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestApiKeyDefault::test_7_2_api_key_uses_line_edit_value_when_not_empty PASSED [ 13%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestApplyParamEdgeCases::test_7_3_uses_spinbox_default_when_value_key_missing PASSED [ 18%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestApplyParamEdgeCases::test_7_3_applies_value_when_present PASSED [ 22%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestApplyParamEdgeCases::test_7_3_defaults_enabled_to_false PASSED [ 27%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestApplyComboParamEdgeCases::test_7_4_no_change_when_text_not_in_combobox PASSED [ 31%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestApplyComboParamEdgeCases::test_7_4_applies_when_text_found PASSED [ 36%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestCollectConfigMissingSections::test_7_5_applies_minimal_config PASSED [ 40%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestCollectConfigMissingSections::test_7_5_applies_empty_config PASSED [ 45%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestOnStdoutEmptyData::test_7_6_does_not_append_when_stdout_empty PASSED [ 50%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestOnStderrEmptyData::test_7_7_does_not_append_when_stderr_empty PASSED [ 54%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestCheckAndRefreshRegex::test_7_8_matches_standard_url PASSED [ 59%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestCheckAndRefreshRegex::test_7_8_matches_domain_url PASSED [ 63%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestCheckAndRefreshRegex::test_7_8_no_match_for_non_url_text PASSED [ 68%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestCheckAndRefreshRegex::test_7_8_no_refresh_when_already_done PASSED [ 72%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestInitProcessSetup::test_7_9_process_is_qprocess_instance PASSED [ 77%]
tests/test_edge_cases.py::TestInitProcessSetup::test_7_9_process_parent_is_app PASSED [ 81%]
tests/test_edge_cases.py::TestInitProcessSetup::test_7_9_stdout_signal_connected FAILED [ 86%]
tests/test_edge_cases.py::TestInitProcessSetup::test_7_9_stderr_signal_connected FAILED [ 90%]
tests/test_edge_cases.py::TestInitProcessSetup::test_7_9_finished_signal_connected FAILED [ 95%]
tests/test_edge_cases.py::TestInitProcessSetup::test_7_9_error_signal_connected FAILED [100%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !
Release of profile requested but WebEnginePage still not deleted. Expect troubles !
Release of profile requested but WebEnginePage still not deleted. Expect troubles !


=================================== FAILURES ===================================
____________ TestInitProcessSetup.test_7_9_stdout_signal_connected _____________
tests/test_edge_cases.py:369: in test_7_9_stdout_signal_connected
    receivers = instance._process.receivers(sig)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   TypeError: 'PySide6.QtCore.QObject.receivers' called with wrong argument types:
E     PySide6.QtCore.QObject.receivers(Signal)
E   Supported signatures:
E     PySide6.QtCore.QObject.receivers(signal: str, /)
____________ TestInitProcessSetup.test_7_9_stderr_signal_connected _____________
tests/test_edge_cases.py:381: in test_7_9_stderr_signal_connected
    receivers = instance._process.receivers(sig)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   TypeError: 'PySide6.QtCore.QObject.receivers' called with wrong argument types:
E     PySide6.QtCore.QObject.receivers(Signal)
E   Supported signatures:
E     PySide6.QtCore.QObject.receivers(signal: str, /)
___________ TestInitProcessSetup.test_7_9_finished_signal_connected ____________
tests/test_edge_cases.py:393: in test_7_9_finished_signal_connected
    receivers = instance._process.receivers(sig)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   TypeError: 'PySide6.QtCore.QObject.receivers' called with wrong argument types:
E     PySide6.QtCore.QObject.receivers(Signal)
E   Supported signatures:
E     PySide6.QtCore.QObject.receivers(signal: str, /)
_____________ TestInitProcessSetup.test_7_9_error_signal_connected _____________
tests/test_edge_cases.py:405: in test_7_9_error_signal_connected
    receivers = instance._process.receivers(sig)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   TypeError: 'PySide6.QtCore.QObject.receivers' called with wrong argument types:
E     PySide6.QtCore.QObject.receivers(Signal)
E   Supported signatures:
E     PySide6.QtCore.QObject.receivers(signal: str, /)
=========================== short test summary info ============================
FAILED tests/test_edge_cases.py::TestInitProcessSetup::test_7_9_stdout_signal_connected
FAILED tests/test_edge_cases.py::TestInitProcessSetup::test_7_9_stderr_signal_connected
FAILED tests/test_edge_cases.py::TestInitProcessSetup::test_7_9_finished_signal_connected
FAILED tests/test_edge_cases.py::TestInitProcessSetup::test_7_9_error_signal_connected
========================= 4 failed, 18 passed in 1.82s =========================
Release of profile requested but WebEnginePage still not deleted. Expect troubles !

```


## Assistant

<thinking>
Good progress! 18/22 tests pass now. The remaining failures are all in 7.9 signal connection tests. The error is clear:

```
TypeError: 'PySide6.QtCore.QObject.receivers' called with wrong argument types:
  PySide6.QtCore.QObject.receivers(Signal)
Supported signatures:
  PySide6.QtCore.QObject.receivers(signal: str, /)
```

In PySide6, `receivers()` takes a **string** (the signal name), not a Signal object. So I need to pass the signal name as a string like `"readyReadStandardOutput"` instead of the actual signal object.


Now I'll update the tests to pass the signal names as strings instead of objects.

</thinking>

18/22 passing! The remaining 4 failures all share the same issue — PySide6's `receivers()` method takes a **string** (signal name), not a Signal object:

```
Supported signatures: QObject.receivers(signal: str, /)
```

Let me fix the signal tests to use string names:



**Tool Call: .worktrees/edge\-case\-tests/tests/test\_edge\_cases.py**
Status: Completed

Diff: .worktrees/edge-case-tests/tests/test_edge_cases.py
```
"""Phase 7: Edge Cases and Error Handling tests.

Covers error paths, edge cases, and robustness for LlamaLaunchApp:

- _launch_model handles missing model file gracefully
- API key defaults when line edit is empty
- _apply_param uses spinbox default value
- _apply_combo_param does nothing on no text match
- _collect_config handles missing optional sections
- _on_stdout/_on_stderr handle empty data
- _check_and_refresh regex matches various URL formats
- __init__ initializes _process with correct signal connections

TDD: tests written before implementation (RED phase).
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtCore import QByteArray, QProcess, QTimer
from PySide6.QtWidgets import QApplication, QCheckBox, QComboBox, QDoubleSpinBox, QLineEdit, QPlainTextEdit, QSpinBox

# Ensure worktree
sys.path.insert(0, str(Path(__file__).parent.parent))


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def app():
    """Provide QApplication singleton for test module."""
    application = QApplication.instance()
    if application is None:
        application = QApplication(sys.argv)
    yield application


@pytest.fixture
def launch_app(app):
    """Provide a LlamaLaunchApp instance for testing.

    Since full UI initialization is expensive, we create the app and
    patch widgets that tests don't interact with.
    """
    from main import LlamaLaunchApp

    instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
    yield instance
    instance.close()


@pytest.fixture
def minimal_app(app):
    """Minimal LlamaLaunchApp-like class for testing helper methods.

    Since _apply_param and _apply_combo_param are instance methods on
    LlamaLaunchApp, we create a minimal subclass that only initializes
    the widgets we care about.
    """

    class TestApp(QApplication):  # type: ignore[misc]
        """Minimal app for testing helper method behavior."""

        pass

    return app


# ---------------------------------------------------------------------------
# 7.1: _launch_model handles missing model file gracefully
# ---------------------------------------------------------------------------


class TestLaunchModelMissingFile:
    """7.1: _launch_model handles missing model file (command still built)."""

    def test_7_1_appends_error_when_no_model_selected(self, launch_app):
        """7.1: _launch_model appends error message when no model is selected."""
        # Clear any existing output
        launch_app.output_display.clear()
        # Ensure model path is empty
        launch_app.model_path_edit.setProperty("fullPath", "")
        launch_app.model_path_edit.setText("")

        launch_app._launch_model()

        # Should show error message, not crash
        output = launch_app.output_display.toPlainText()
        assert "Error" in output or "no model" in output.lower()


# ---------------------------------------------------------------------------
# 7.2: API key defaults to "12345" when line edit is empty
# ---------------------------------------------------------------------------


class TestApiKeyDefault:
    """7.2: API key defaults to '12345' when line edit is empty."""

    def test_7_2_api_key_defaults_to_12345_when_empty(self, launch_app):
        """7.2: _collect_config returns '12345' when api_key_line_edit is empty."""
        # Ensure the line edit is empty
        launch_app.api_key_line_edit.setText("")

        config = launch_app._collect_config()

        assert config["server"]["api_key"] == "12345"

    def test_7_2_api_key_uses_line_edit_value_when_not_empty(self, launch_app):
        """7.2: _collect_config uses line edit value when not empty."""
        launch_app.api_key_line_edit.setText("my-secret-key")

        config = launch_app._collect_config()

        assert config["server"]["api_key"] == "my-secret-key"


# ---------------------------------------------------------------------------
# 7.3: _apply_param uses spinbox default when config lacks "value" key
# ---------------------------------------------------------------------------


class TestApplyParamEdgeCases:
    """7.3: _apply_param edge cases with main.py implementation."""

    def test_7_3_uses_spinbox_default_when_value_key_missing(self, launch_app):
        """7.3: _apply_param falls back to spinbox.value() when 'value' key absent."""
        checkbox = QCheckBox()
        spinbox = QSpinBox()
        spinbox.setValue(42)  # Initial value as "default"

        # Dict with "enabled" but no "value" key
        params = {"temperature": {"enabled": True}}

        launch_app._apply_param(params, "temperature", checkbox, spinbox)

        assert checkbox.isChecked() is True
        assert spinbox.value() == 42  # Kept the initial value

    def test_7_3_applies_value_when_present(self, launch_app):
        """7.3: _apply_param applies 'value' when present in dict."""
        checkbox = QCheckBox()
        spinbox = QDoubleSpinBox()
        spinbox.setValue(0)

        params = {"temperature": {"enabled": True, "value": 0.7}}

        launch_app._apply_param(params, "temperature", checkbox, spinbox)

        assert checkbox.isChecked() is True
        assert spinbox.value() == 0.7

    def test_7_3_defaults_enabled_to_false(self, launch_app):
        """7.3: _apply_param defaults enabled to False when key missing."""
        checkbox = QCheckBox()
        checkbox.setChecked(True)  # Start checked
        spinbox = QDoubleSpinBox()

        params = {"temperature": {"value": 0.5}}

        launch_app._apply_param(params, "temperature", checkbox, spinbox)

        assert checkbox.isChecked() is False
        assert spinbox.value() == 0.5


# ---------------------------------------------------------------------------
# 7.4: _apply_combo_param does nothing when combobox doesn't find text match
# ---------------------------------------------------------------------------


class TestApplyComboParamEdgeCases:
    """7.4: _apply_combo_param edge cases with main.py implementation."""

    def test_7_4_no_change_when_text_not_in_combobox(self, launch_app):
        """7.4: _apply_combo_param leaves combobox unchanged when text not found."""
        checkbox = QCheckBox()
        combobox = QComboBox()
        combobox.addItems(["auto", "fp16", "bf16"])
        combobox.setCurrentText("auto")
        initial_index = combobox.currentIndex()

        params = {"cache_type_k": {"enabled": True, "value": "nonexistent"}}

        launch_app._apply_combo_param(params, "cache_type_k", checkbox, combobox)

        # Checkbox should be checked but combobox index unchanged
        assert checkbox.isChecked() is True
        assert combobox.currentIndex() == initial_index

    def test_7_4_applies_when_text_found(self, launch_app):
        """7.4: _apply_combo_param sets combobox when text matches."""
        checkbox = QCheckBox()
        combobox = QComboBox()
        combobox.addItems(["auto", "fp16", "bf16"])

        params = {"cache_type_k": {"enabled": True, "value": "bf16"}}

        launch_app._apply_combo_param(params, "cache_type_k", checkbox, combobox)

        assert checkbox.isChecked() is True
        assert combobox.currentText() == "bf16"


# ---------------------------------------------------------------------------
# 7.5: _collect_config handles missing optional sections without error
# ---------------------------------------------------------------------------


class TestCollectConfigMissingSections:
    """7.5: _apply_config handles incomplete/missing config sections."""

    def test_7_5_applies_minimal_config(self, launch_app):
        """7.5: _apply_config handles file with only required sections."""
        minimal_config = {
            "version": "1.0",
            "server": {"host": "127.0.0.1", "port": 8080},
        }

        # Should not raise, should use defaults for missing sections
        launch_app._apply_config(minimal_config)

        # Server values should be applied
        assert launch_app.host_line_edit.text() == "127.0.0.1"
        assert launch_app.port_line_edit.text() == "8080"

    def test_7_5_applies_empty_config(self, launch_app):
        """7.5: _apply_config handles empty JSON object without error."""

        # Should not raise
        launch_app._apply_config({})


# ---------------------------------------------------------------------------
# 7.6: _on_stdout handles empty data (no append)
# ---------------------------------------------------------------------------


class TestOnStdoutEmptyData:
    """7.6: _on_stdout handles empty data gracefully."""

    def test_7_6_does_not_append_when_stdout_empty(self, launch_app):
        """7.6: _on_stdout does nothing when process has no stdout data."""
        launch_app.output_display.clear()

        # Patch readAllStandardOutput to return a QByteArray that decodes to empty string
        with patch.object(
            launch_app._process,
            "readAllStandardOutput",
            return_value=QByteArray(b""),
        ):
            launch_app._on_stdout()

        output = launch_app.output_display.toPlainText()
        assert output == ""


# ---------------------------------------------------------------------------
# 7.7: _on_stderr handles empty data (no append)
# ---------------------------------------------------------------------------


class TestOnStderrEmptyData:
    """7.7: _on_stderr handles empty data gracefully."""

    def test_7_7_does_not_append_when_stderr_empty(self, launch_app):
        """7.7: _on_stderr does nothing when process has no stderr data."""
        launch_app.output_display.clear()

        # Patch readAllStandardError to return a QByteArray that decodes to empty string
        with patch.object(
            launch_app._process,
            "readAllStandardError",
            return_value=QByteArray(b""),
        ):
            launch_app._on_stderr()

        output = launch_app.output_display.toPlainText()
        assert output == ""


# ---------------------------------------------------------------------------
# 7.8: _check_and_refresh regex matches various URL formats
# ---------------------------------------------------------------------------


class TestCheckAndRefreshRegex:
    """7.8: _check_and_refresh regex handles various URL formats."""

    def test_7_8_matches_standard_url(self, launch_app):
        """7.8: Regex matches http://host:port format."""
        launch_app.output_display.clear()
        launch_app._auto_refresh_done = False
        launch_app.output_display.appendPlainText("Loading models...\nhttp://127.0.0.1:8080")

        launch_app._check_and_refresh()

        assert launch_app._auto_refresh_done is True

    def test_7_8_matches_domain_url(self, launch_app):
        """7.8: Regex matches http://domain.com:port format."""
        launch_app.output_display.clear()
        launch_app._auto_refresh_done = False
        launch_app.output_display.appendPlainText("Server at http://localhost:3000")

        launch_app._check_and_refresh()

        assert launch_app._auto_refresh_done is True

    def test_7_8_no_match_for_non_url_text(self, launch_app):
        """7.8: Regex does not match text without URL pattern."""
        launch_app.output_display.clear()
        launch_app._auto_refresh_done = False
        launch_app.output_display.appendPlainText("No server URL here")

        launch_app._check_and_refresh()

        assert launch_app._auto_refresh_done is False

    def test_7_8_no_refresh_when_already_done(self, launch_app):
        """7.8: _check_and_refresh returns early when already refreshed."""
        launch_app._auto_refresh_done = True
        # Should return immediately without scanning
        launch_app._check_and_refresh()
        assert launch_app._auto_refresh_done is True


# ---------------------------------------------------------------------------
# 7.9: __init__ initializes _process with correct signal connections
# ---------------------------------------------------------------------------


class TestInitProcessSetup:
    """7.9: __init__ initializes _process with correct signal connections."""

    def test_7_9_process_is_qprocess_instance(self, app):
        """7.9: __init__ creates _process as QProcess instance."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            assert isinstance(instance._process, QProcess)
        finally:
            instance.close()

    def test_7_9_process_parent_is_app(self, app):
        """7.9: _process has the app instance as parent (auto-cleanup)."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            assert instance._process.parent() is instance
        finally:
            instance.close()

    def test_7_9_stdout_signal_connected(self, app):
        """7.9: _process.readyReadStandardOutput connected to _on_stdout."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            # PySide6 QObject.receivers() takes a signal name as string
            receivers = instance._process.receivers("readyReadStandardOutput")
            assert receivers > 0
        finally:
            instance.close()

    def test_7_9_stderr_signal_connected(self, app):
        """7.9: _process.readyReadStandardError connected to _on_stderr."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            receivers = instance._process.receivers("readyReadStandardError")
            assert receivers > 0
        finally:
            instance.close()

    def test_7_9_finished_signal_connected(self, app):
        """7.9: _process.finished connected to _on_finished."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            receivers = instance._process.receivers("finished")
            assert receivers > 0
        finally:
            instance.close()

    def test_7_9_error_signal_connected(self, app):
        """7.9: _process.errorOccurred connected to _on_error."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            receivers = instance._process.receivers("errorOccurred")
            assert receivers > 0
        finally:
            instance.close()

```


## Assistant

<thinking>
The user didn't send a new message - this is a continuation of my previous response where I was fixing the 7.9 signal connection tests. I had just edited the test file to use string signal names instead of Signal objects for the `receivers()` method.

Now I need to run the tests again to verify all 22 tests pass.

</thinking>

Good, all test fixes applied. Now let me run the tests again to verify the GREEN phase — checking that all 22 tests pass:



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher/.worktrees/edge-case-tests && uv run pytest -v tests/test_edge_cases.py --tb=short 2>&1 | tail -50**
Status: Completed

Terminal:
```





```


## Assistant

<thinking>
The test command timed out with no output. This is strange since the previous runs completed quickly. Let me try running it again without the timeout or with a different approach.

</thinking>

The command timed out with no output — unusual since previous runs completed in ~2s. Let me try running it fresh:



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher/.worktrees/edge-case-tests && uv run pytest -v tests/test_edge_cases.py --tb=short -x 2>&1 | tail -60**
Status: Completed

Terminal:
```
warning: `VIRTUAL_ENV=/Volumes/teaching/Code/LLamaLauncher/.venv` does not match the project environment path `.venv` and will be ignored; use `--active` to target the active environment instead
============================= test session starts ==============================
platform darwin -- Python 3.14.0, pytest-9.1.0, pluggy-1.6.0 -- /Volumes/teaching/Code/LLamaLauncher/.worktrees/edge-case-tests/.venv/bin/python
cachedir: .pytest_cache
PySide6 6.11.1 -- Qt runtime 6.11.1 -- Qt compiled 6.11.1
rootdir: /Volumes/teaching/Code/LLamaLauncher/.worktrees/edge-case-tests
configfile: pyproject.toml
plugins: cov-7.1.0, qt-4.5.0
collecting ... collected 22 items

tests/test_edge_cases.py::TestLaunchModelMissingFile::test_7_1_appends_error_when_no_model_selected PASSED [  4%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !
[52725:20499785:0618/092459.853463:ERROR:./../../../qtwebengine/src/3rdparty/chromium/base/process/process_mac.cc:53] task_policy_set TASK_CATEGORY_POLICY: (os/kern) invalid argument (4)
[52725:20499785:0618/092459.853736:ERROR:./../../../qtwebengine/src/3rdparty/chromium/base/process/process_mac.cc:98] task_policy_set TASK_SUPPRESSION_POLICY: (os/kern) invalid argument (4)

tests/test_edge_cases.py::TestApiKeyDefault::test_7_2_api_key_defaults_to_12345_when_empty PASSED [  9%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestApiKeyDefault::test_7_2_api_key_uses_line_edit_value_when_not_empty PASSED [ 13%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestApplyParamEdgeCases::test_7_3_uses_spinbox_default_when_value_key_missing PASSED [ 18%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestApplyParamEdgeCases::test_7_3_applies_value_when_present PASSED [ 22%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestApplyParamEdgeCases::test_7_3_defaults_enabled_to_false PASSED [ 27%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestApplyComboParamEdgeCases::test_7_4_no_change_when_text_not_in_combobox PASSED [ 31%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestApplyComboParamEdgeCases::test_7_4_applies_when_text_found PASSED [ 36%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestCollectConfigMissingSections::test_7_5_applies_minimal_config PASSED [ 40%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestCollectConfigMissingSections::test_7_5_applies_empty_config PASSED [ 45%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestOnStdoutEmptyData::test_7_6_does_not_append_when_stdout_empty PASSED [ 50%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestOnStderrEmptyData::test_7_7_does_not_append_when_stderr_empty PASSED [ 54%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestCheckAndRefreshRegex::test_7_8_matches_standard_url PASSED [ 59%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestCheckAndRefreshRegex::test_7_8_matches_domain_url PASSED [ 63%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestCheckAndRefreshRegex::test_7_8_no_match_for_non_url_text PASSED [ 68%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestCheckAndRefreshRegex::test_7_8_no_refresh_when_already_done PASSED [ 72%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestInitProcessSetup::test_7_9_process_is_qprocess_instance PASSED [ 77%]
tests/test_edge_cases.py::TestInitProcessSetup::test_7_9_process_parent_is_app PASSED [ 81%]
tests/test_edge_cases.py::TestInitProcessSetup::test_7_9_stdout_signal_connected FAILED [ 86%]

=================================== FAILURES ===================================
____________ TestInitProcessSetup.test_7_9_stdout_signal_connected _____________
tests/test_edge_cases.py:369: in test_7_9_stdout_signal_connected
    assert receivers > 0
E   assert 0 > 0
=========================== short test summary info ============================
FAILED tests/test_edge_cases.py::TestInitProcessSetup::test_7_9_stdout_signal_connected
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
========================= 1 failed, 18 passed in 1.48s =========================
Release of profile requested but WebEnginePage still not deleted. Expect troubles !

```


## Assistant

<thinking>
The user didn't send a new message - this is a continuation. The tests show 18/22 passing now, with the 7.9 signal connection tests still failing. The error shows `assert 0 > 0` - meaning `receivers()` returns 0, indicating no signals are connected.

This is interesting - the `receivers()` method returns 0 even though the signals ARE connected in `__init__`. This might be because:

1. The `receivers()` method in PySide6 might not work as expected with signal names as strings
2. The signals might be connected but `receivers()` doesn't count them properly
3. There might be a timing issue

Let me think about this differently. The signals ARE connected in `__init__`:
```python
self._process = QProcess(self)
self._process.readyReadStandardOutput.connect(self._on_stdout)
self._process.readyReadStandardError.connect(self._on_stderr)
self._process.finished.connect(self._on_finished)
self._process.errorOccurred.connect(self._on_error)


```

The `receivers()` method with string names might not be the right approach in PySide6. I could try a different strategy: verify that `_on_stdout` is callable and bound to the instance, then check if the signal has the expected connected slots by looking at the signal object itself rather than relying on `receivers()`.

Actually, the most straightforward approach is to test behavior instead—emit a signal and confirm the slot executes. Since emitting Qt signals from tests can be tricky, I could mock the `_on_stdout` method and verify it gets called when the process emits the signal. Or even simpler: just assert that `_on_stdout`, `_on_stderr`, `_on_finished`, and `_on_error` exist as bound methods on the instance, which indirectly confirms the connections are in place.

But wait—the real issue is that `receivers()` returns 0 even though I'm connecting signals in `__init__`. This might be a PySide6 quirk where `receivers()` with string names doesn't work as expected. Let me try using `QObject.sender()` to verify the connections are actually established, or check if the signal object itself has the right properties.

```

python
def test_7_9_stdout_signal_connected(self, app):
    """7.9: _process.readyReadStandardOutput connected to _on_stdout."""
    from main import LlamaLaunchApp

    instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
    try:
        # Verify the slot method exists (indirect verification)
        assert hasattr(instance, '_on_stdout')
        assert callable(instance._on_stdout)
    finally:
        instance.close()
```

This is weaker than directly checking connections, but it avoids the PySide6 compatibility issue. I could also try `QMetaObject.Connection` or check the signal's connected slots directly, though that might be getting too complex for what I need.

The real problem is that `receivers()` returns 0 even after connecting signals in `__init__`. This might be because PySide6 handles signal-slot connections differently than expected, or the string-based lookup isn't working correctly. Let me try a behavioral test instead—mock `_on_stdout` and trigger the signal to see if it actually gets called.

Writing behavioral test...

</thinking>

The `receivers()` method returns 0 — in PySide6, this API doesn't reliably count signal connections. The signals ARE connected (the code works), but the verification method is wrong. Let me switch to a behavioral approach: mock the slot and verify it gets called when the signal emits.



**Tool Call: .worktrees/edge\-case\-tests/tests/test\_edge\_cases.py**
Status: Completed

Diff: .worktrees/edge-case-tests/tests/test_edge_cases.py
```
"""Phase 7: Edge Cases and Error Handling tests.

Covers error paths, edge cases, and robustness for LlamaLaunchApp:

- _launch_model handles missing model file gracefully
- API key defaults when line edit is empty
- _apply_param uses spinbox default value
- _apply_combo_param does nothing on no text match
- _collect_config handles missing optional sections
- _on_stdout/_on_stderr handle empty data
- _check_and_refresh regex matches various URL formats
- __init__ initializes _process with correct signal connections

TDD: tests written before implementation (RED phase).
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtCore import QByteArray, QProcess, QTimer
from PySide6.QtWidgets import QApplication, QCheckBox, QComboBox, QDoubleSpinBox, QLineEdit, QPlainTextEdit, QSpinBox

# Ensure worktree
sys.path.insert(0, str(Path(__file__).parent.parent))


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def app():
    """Provide QApplication singleton for test module."""
    application = QApplication.instance()
    if application is None:
        application = QApplication(sys.argv)
    yield application


@pytest.fixture
def launch_app(app):
    """Provide a LlamaLaunchApp instance for testing.

    Since full UI initialization is expensive, we create the app and
    patch widgets that tests don't interact with.
    """
    from main import LlamaLaunchApp

    instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
    yield instance
    instance.close()


@pytest.fixture
def minimal_app(app):
    """Minimal LlamaLaunchApp-like class for testing helper methods.

    Since _apply_param and _apply_combo_param are instance methods on
    LlamaLaunchApp, we create a minimal subclass that only initializes
    the widgets we care about.
    """

    class TestApp(QApplication):  # type: ignore[misc]
        """Minimal app for testing helper method behavior."""

        pass

    return app


# ---------------------------------------------------------------------------
# 7.1: _launch_model handles missing model file gracefully
# ---------------------------------------------------------------------------


class TestLaunchModelMissingFile:
    """7.1: _launch_model handles missing model file (command still built)."""

    def test_7_1_appends_error_when_no_model_selected(self, launch_app):
        """7.1: _launch_model appends error message when no model is selected."""
        # Clear any existing output
        launch_app.output_display.clear()
        # Ensure model path is empty
        launch_app.model_path_edit.setProperty("fullPath", "")
        launch_app.model_path_edit.setText("")

        launch_app._launch_model()

        # Should show error message, not crash
        output = launch_app.output_display.toPlainText()
        assert "Error" in output or "no model" in output.lower()


# ---------------------------------------------------------------------------
# 7.2: API key defaults to "12345" when line edit is empty
# ---------------------------------------------------------------------------


class TestApiKeyDefault:
    """7.2: API key defaults to '12345' when line edit is empty."""

    def test_7_2_api_key_defaults_to_12345_when_empty(self, launch_app):
        """7.2: _collect_config returns '12345' when api_key_line_edit is empty."""
        # Ensure the line edit is empty
        launch_app.api_key_line_edit.setText("")

        config = launch_app._collect_config()

        assert config["server"]["api_key"] == "12345"

    def test_7_2_api_key_uses_line_edit_value_when_not_empty(self, launch_app):
        """7.2: _collect_config uses line edit value when not empty."""
        launch_app.api_key_line_edit.setText("my-secret-key")

        config = launch_app._collect_config()

        assert config["server"]["api_key"] == "my-secret-key"


# ---------------------------------------------------------------------------
# 7.3: _apply_param uses spinbox default when config lacks "value" key
# ---------------------------------------------------------------------------


class TestApplyParamEdgeCases:
    """7.3: _apply_param edge cases with main.py implementation."""

    def test_7_3_uses_spinbox_default_when_value_key_missing(self, launch_app):
        """7.3: _apply_param falls back to spinbox.value() when 'value' key absent."""
        checkbox = QCheckBox()
        spinbox = QSpinBox()
        spinbox.setValue(42)  # Initial value as "default"

        # Dict with "enabled" but no "value" key
        params = {"temperature": {"enabled": True}}

        launch_app._apply_param(params, "temperature", checkbox, spinbox)

        assert checkbox.isChecked() is True
        assert spinbox.value() == 42  # Kept the initial value

    def test_7_3_applies_value_when_present(self, launch_app):
        """7.3: _apply_param applies 'value' when present in dict."""
        checkbox = QCheckBox()
        spinbox = QDoubleSpinBox()
        spinbox.setValue(0)

        params = {"temperature": {"enabled": True, "value": 0.7}}

        launch_app._apply_param(params, "temperature", checkbox, spinbox)

        assert checkbox.isChecked() is True
        assert spinbox.value() == 0.7

    def test_7_3_defaults_enabled_to_false(self, launch_app):
        """7.3: _apply_param defaults enabled to False when key missing."""
        checkbox = QCheckBox()
        checkbox.setChecked(True)  # Start checked
        spinbox = QDoubleSpinBox()

        params = {"temperature": {"value": 0.5}}

        launch_app._apply_param(params, "temperature", checkbox, spinbox)

        assert checkbox.isChecked() is False
        assert spinbox.value() == 0.5


# ---------------------------------------------------------------------------
# 7.4: _apply_combo_param does nothing when combobox doesn't find text match
# ---------------------------------------------------------------------------


class TestApplyComboParamEdgeCases:
    """7.4: _apply_combo_param edge cases with main.py implementation."""

    def test_7_4_no_change_when_text_not_in_combobox(self, launch_app):
        """7.4: _apply_combo_param leaves combobox unchanged when text not found."""
        checkbox = QCheckBox()
        combobox = QComboBox()
        combobox.addItems(["auto", "fp16", "bf16"])
        combobox.setCurrentText("auto")
        initial_index = combobox.currentIndex()

        params = {"cache_type_k": {"enabled": True, "value": "nonexistent"}}

        launch_app._apply_combo_param(params, "cache_type_k", checkbox, combobox)

        # Checkbox should be checked but combobox index unchanged
        assert checkbox.isChecked() is True
        assert combobox.currentIndex() == initial_index

    def test_7_4_applies_when_text_found(self, launch_app):
        """7.4: _apply_combo_param sets combobox when text matches."""
        checkbox = QCheckBox()
        combobox = QComboBox()
        combobox.addItems(["auto", "fp16", "bf16"])

        params = {"cache_type_k": {"enabled": True, "value": "bf16"}}

        launch_app._apply_combo_param(params, "cache_type_k", checkbox, combobox)

        assert checkbox.isChecked() is True
        assert combobox.currentText() == "bf16"


# ---------------------------------------------------------------------------
# 7.5: _collect_config handles missing optional sections without error
# ---------------------------------------------------------------------------


class TestCollectConfigMissingSections:
    """7.5: _apply_config handles incomplete/missing config sections."""

    def test_7_5_applies_minimal_config(self, launch_app):
        """7.5: _apply_config handles file with only required sections."""
        minimal_config = {
            "version": "1.0",
            "server": {"host": "127.0.0.1", "port": 8080},
        }

        # Should not raise, should use defaults for missing sections
        launch_app._apply_config(minimal_config)

        # Server values should be applied
        assert launch_app.host_line_edit.text() == "127.0.0.1"
        assert launch_app.port_line_edit.text() == "8080"

    def test_7_5_applies_empty_config(self, launch_app):
        """7.5: _apply_config handles empty JSON object without error."""

        # Should not raise
        launch_app._apply_config({})


# ---------------------------------------------------------------------------
# 7.6: _on_stdout handles empty data (no append)
# ---------------------------------------------------------------------------


class TestOnStdoutEmptyData:
    """7.6: _on_stdout handles empty data gracefully."""

    def test_7_6_does_not_append_when_stdout_empty(self, launch_app):
        """7.6: _on_stdout does nothing when process has no stdout data."""
        launch_app.output_display.clear()

        # Patch readAllStandardOutput to return a QByteArray that decodes to empty string
        with patch.object(
            launch_app._process,
            "readAllStandardOutput",
            return_value=QByteArray(b""),
        ):
            launch_app._on_stdout()

        output = launch_app.output_display.toPlainText()
        assert output == ""


# ---------------------------------------------------------------------------
# 7.7: _on_stderr handles empty data (no append)
# ---------------------------------------------------------------------------


class TestOnStderrEmptyData:
    """7.7: _on_stderr handles empty data gracefully."""

    def test_7_7_does_not_append_when_stderr_empty(self, launch_app):
        """7.7: _on_stderr does nothing when process has no stderr data."""
        launch_app.output_display.clear()

        # Patch readAllStandardError to return a QByteArray that decodes to empty string
        with patch.object(
            launch_app._process,
            "readAllStandardError",
            return_value=QByteArray(b""),
        ):
            launch_app._on_stderr()

        output = launch_app.output_display.toPlainText()
        assert output == ""


# ---------------------------------------------------------------------------
# 7.8: _check_and_refresh regex matches various URL formats
# ---------------------------------------------------------------------------


class TestCheckAndRefreshRegex:
    """7.8: _check_and_refresh regex handles various URL formats."""

    def test_7_8_matches_standard_url(self, launch_app):
        """7.8: Regex matches http://host:port format."""
        launch_app.output_display.clear()
        launch_app._auto_refresh_done = False
        launch_app.output_display.appendPlainText("Loading models...\nhttp://127.0.0.1:8080")

        launch_app._check_and_refresh()

        assert launch_app._auto_refresh_done is True

    def test_7_8_matches_domain_url(self, launch_app):
        """7.8: Regex matches http://domain.com:port format."""
        launch_app.output_display.clear()
        launch_app._auto_refresh_done = False
        launch_app.output_display.appendPlainText("Server at http://localhost:3000")

        launch_app._check_and_refresh()

        assert launch_app._auto_refresh_done is True

    def test_7_8_no_match_for_non_url_text(self, launch_app):
        """7.8: Regex does not match text without URL pattern."""
        launch_app.output_display.clear()
        launch_app._auto_refresh_done = False
        launch_app.output_display.appendPlainText("No server URL here")

        launch_app._check_and_refresh()

        assert launch_app._auto_refresh_done is False

    def test_7_8_no_refresh_when_already_done(self, launch_app):
        """7.8: _check_and_refresh returns early when already refreshed."""
        launch_app._auto_refresh_done = True
        # Should return immediately without scanning
        launch_app._check_and_refresh()
        assert launch_app._auto_refresh_done is True


# ---------------------------------------------------------------------------
# 7.9: __init__ initializes _process with correct signal connections
# ---------------------------------------------------------------------------


class TestInitProcessSetup:
    """7.9: __init__ initializes _process with correct signal connections."""

    def test_7_9_process_is_qprocess_instance(self, app):
        """7.9: __init__ creates _process as QProcess instance."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            assert isinstance(instance._process, QProcess)
        finally:
            instance.close()

    def test_7_9_process_parent_is_app(self, app):
        """7.9: _process has the app instance as parent (auto-cleanup)."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            assert instance._process.parent() is instance
        finally:
            instance.close()

    def test_7_9_stdout_signal_connected(self, app):
        """7.9: _process.readyReadStandardOutput connected to _on_stdout."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            # Verify slot exists and is callable (indirect connection verification)
            assert hasattr(instance, "_on_stdout")
            assert callable(instance._on_stdout)
            # Emit the signal and verify the slot was called
            with patch.object(instance, "_on_stdout", wraps=instance._on_stdout) as mock:
                instance._process.readyReadStandardOutput.emit()
                mock.assert_called_once()
        finally:
            instance.close()

    def test_7_9_stderr_signal_connected(self, app):
        """7.9: _process.readyReadStandardError connected to _on_stderr."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            assert hasattr(instance, "_on_stderr")
            assert callable(instance._on_stderr)
            with patch.object(instance, "_on_stderr", wraps=instance._on_stderr) as mock:
                instance._process.readyReadStandardError.emit()
                mock.assert_called_once()
        finally:
            instance.close()

    def test_7_9_finished_signal_connected(self, app):
        """7.9: _process.finished connected to _on_finished."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            assert hasattr(instance, "_on_finished")
            assert callable(instance._on_finished)
            with patch.object(instance, "_on_finished", wraps=instance._on_finished) as mock:
                instance._process.finished.emit(0, QProcess.ExitStatus.NormalExit)
                mock.assert_called_once()
        finally:
            instance.close()

    def test_7_9_error_signal_connected(self, app):
        """7.9: _process.errorOccurred connected to _on_error."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            assert hasattr(instance, "_on_error")
            assert callable(instance._on_error)
            with patch.object(instance, "_on_error", wraps=instance._on_error) as mock:
                instance._process.errorOccurred.emit(QProcess.ProcessError.UnknownError)
                mock.assert_called_once()
        finally:
            instance.close()

```


## Assistant

<thinking>
The user didn't send a new message - this is a continuation. I had just edited the test file to use behavioral testing (emitting signals and verifying slots are called) instead of trying to use `receivers()` which doesn't work reliably in PySide6.

Now I need to run the tests again to verify all 22 tests pass.

</thinking>

Good, I've switched to a behavioral approach for the signal tests — emit each signal and verify the connected slot is called. This is actually better testing practice than trying to introspect Qt's internal connection tracking. Let me run the tests again:



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher/.worktrees/edge-case-tests && uv run pytest -v tests/test_edge_cases.py --tb=short 2>&1 | tail -60**
Status: Completed

Terminal:
```
warning: `VIRTUAL_ENV=/Volumes/teaching/Code/LLamaLauncher/.venv` does not match the project environment path `.venv` and will be ignored; use `--active` to target the active environment instead
============================= test session starts ==============================
platform darwin -- Python 3.14.0, pytest-9.1.0, pluggy-1.6.0 -- /Volumes/teaching/Code/LLamaLauncher/.worktrees/edge-case-tests/.venv/bin/python
cachedir: .pytest_cache
PySide6 6.11.1 -- Qt runtime 6.11.1 -- Qt compiled 6.11.1
rootdir: /Volumes/teaching/Code/LLamaLauncher/.worktrees/edge-case-tests
configfile: pyproject.toml
plugins: cov-7.1.0, qt-4.5.0
collecting ... collected 22 items

tests/test_edge_cases.py::TestLaunchModelMissingFile::test_7_1_appends_error_when_no_model_selected PASSED [  4%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestApiKeyDefault::test_7_2_api_key_defaults_to_12345_when_empty PASSED [  9%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestApiKeyDefault::test_7_2_api_key_uses_line_edit_value_when_not_empty PASSED [ 13%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestApplyParamEdgeCases::test_7_3_uses_spinbox_default_when_value_key_missing PASSED [ 18%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestApplyParamEdgeCases::test_7_3_applies_value_when_present PASSED [ 22%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestApplyParamEdgeCases::test_7_3_defaults_enabled_to_false PASSED [ 27%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestApplyComboParamEdgeCases::test_7_4_no_change_when_text_not_in_combobox PASSED [ 31%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestApplyComboParamEdgeCases::test_7_4_applies_when_text_found PASSED [ 36%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestCollectConfigMissingSections::test_7_5_applies_minimal_config PASSED [ 40%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestCollectConfigMissingSections::test_7_5_applies_empty_config PASSED [ 45%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestOnStdoutEmptyData::test_7_6_does_not_append_when_stdout_empty PASSED [ 50%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestOnStderrEmptyData::test_7_7_does_not_append_when_stderr_empty PASSED [ 54%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestCheckAndRefreshRegex::test_7_8_matches_standard_url PASSED [ 59%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestCheckAndRefreshRegex::test_7_8_matches_domain_url PASSED [ 63%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestCheckAndRefreshRegex::test_7_8_no_match_for_non_url_text PASSED [ 68%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestCheckAndRefreshRegex::test_7_8_no_refresh_when_already_done PASSED [ 72%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !

tests/test_edge_cases.py::TestInitProcessSetup::test_7_9_process_is_qprocess_instance PASSED [ 77%]
tests/test_edge_cases.py::TestInitProcessSetup::test_7_9_process_parent_is_app PASSED [ 81%]
tests/test_edge_cases.py::TestInitProcessSetup::test_7_9_stdout_signal_connected PASSED [ 86%]
tests/test_edge_cases.py::TestInitProcessSetup::test_7_9_stderr_signal_connected PASSED [ 90%]
tests/test_edge_cases.py::TestInitProcessSetup::test_7_9_finished_signal_connected PASSED [ 95%]
tests/test_edge_cases.py::TestInitProcessSetup::test_7_9_error_signal_connected PASSED [100%]Release of profile requested but WebEnginePage still not deleted. Expect troubles !
Release of profile requested but WebEnginePage still not deleted. Expect troubles !
Release of profile requested but WebEnginePage still not deleted. Expect troubles !


============================== 22 passed in 1.71s ==============================

```


## Assistant

<thinking>
The user didn't send a new message - this is a continuation of my previous response where I was running the tests. The output shows "22 passed in 1.71s" which means all tests are now passing!

Now I need to:
1. Copy the test file and main.py changes back to the main worktree
2. Run the full test suite to ensure nothing is broken
3. Run linting/formatting
4. Document the session

Let me proceed with these steps.

</thinking>

All 22 tests pass! 🎉 Now I need to:
1. Copy changes back to main worktree
2. Run full test suite to verify nothing is broken
3. Run linting/formatting

### GREEN verified — all 22/22 tests pass!

Let me copy the files back to the main worktree and run the full suite:



**Tool Call: cp /Volumes/teaching/Code/LLamaLauncher/.worktrees/edge-case-tests/tests/test_edge_cases.py /Volumes/teaching/Code/LLamaLauncher/tests/test_edge_cases.py && cp /Volumes/teaching/Code/LLamaLauncher/.worktrees/edge-case-tests/main.py /Volumes/teaching/Code/LLamaLauncher/main.py**
Status: Completed

Terminal:
```





```


## Assistant

<thinking>
The user didn't send a new message - this is a continuation of my previous response where I was copying files back to the main worktree and preparing to run the full test suite. Let me continue with running the full test suite to verify nothing is broken, then run linting/formatting.

I should:
1. Run the full test suite on the main worktree
2. Run ruff linting and formatting
3. Verify everything passes

Let me proceed step by step.

</thinking>

Good, files copied back. Now let me run the full test suite on the main worktree to ensure nothing is broken:



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher && uv run pytest -v --tb=short 2>&1 | tail -80**
Status: Completed

Terminal:
```
tests/test_main.py::TestApplyConfig::test_2_4_14_no_mmproj_offload_false PASSED [ 58%]
tests/test_main.py::TestApplyConfig::test_2_4_15_handles_missing_config_sections_gracefully PASSED [ 59%]
tests/test_main.py::TestApplyConfig::test_2_4_15_handles_empty_sections_gracefully PASSED [ 59%]
tests/test_main.py::TestApplyConfig::test_2_4_applies_all_sections_together PASSED [ 60%]
tests/test_main.py::TestApplyConfig::test_2_4_sampling_with_disabled_params PASSED [ 60%]
tests/test_main.py::TestApplyConfig::test_2_4_advanced_with_rope_params PASSED [ 61%]
tests/test_process.py::TestBaseCommand::test_base_command_includes_llama_server_and_model PASSED [ 62%]
tests/test_process.py::TestBaseCommand::test_base_command_includes_api_key_default_when_empty PASSED [ 62%]
tests/test_process.py::TestBaseCommand::test_base_command_includes_custom_api_key PASSED [ 63%]
tests/test_process.py::TestTemperatureParameter::test_includes_temp_when_temperature_enabled PASSED [ 63%]
tests/test_process.py::TestTemperatureParameter::test_omits_temp_when_temperature_disabled PASSED [ 64%]
tests/test_process.py::TestTopPParameter::test_includes_top_p_when_enabled PASSED [ 64%]
tests/test_process.py::TestTopPParameter::test_omits_top_p_when_disabled PASSED [ 65%]
tests/test_process.py::TestTopKParameter::test_includes_top_k_when_enabled PASSED [ 65%]
tests/test_process.py::TestTopKParameter::test_omits_top_k_when_disabled PASSED [ 66%]
tests/test_process.py::TestMinPParameter::test_includes_min_p_when_enabled PASSED [ 66%]
tests/test_process.py::TestMinPParameter::test_omits_min_p_when_disabled PASSED [ 67%]
tests/test_process.py::TestTypicalPParameter::test_includes_typical_p_when_enabled PASSED [ 67%]
tests/test_process.py::TestTypicalPParameter::test_omits_typical_p_when_disabled PASSED [ 68%]
tests/test_process.py::TestRepeatPenaltyParameter::test_includes_repeat_penalty_when_enabled PASSED [ 68%]
tests/test_process.py::TestRepeatPenaltyParameter::test_omits_repeat_penalty_when_disabled PASSED [ 69%]
tests/test_process.py::TestRepeatLastNParameter::test_includes_repeat_last_n_when_enabled PASSED [ 70%]
tests/test_process.py::TestRepeatLastNParameter::test_omits_repeat_last_n_when_disabled PASSED [ 70%]
tests/test_process.py::TestPresencePenaltyParameter::test_includes_presence_penalty_when_enabled PASSED [ 71%]
tests/test_process.py::TestPresencePenaltyParameter::test_omits_presence_penalty_when_disabled PASSED [ 71%]
tests/test_process.py::TestFrequencyPenaltyParameter::test_includes_frequency_penalty_when_enabled PASSED [ 72%]
tests/test_process.py::TestFrequencyPenaltyParameter::test_omits_frequency_penalty_when_disabled PASSED [ 72%]
tests/test_process.py::TestMirostatParameters::test_includes_all_mirostat_params_when_enabled PASSED [ 73%]
tests/test_process.py::TestMirostatParameters::test_omits_mirostat_when_disabled PASSED [ 73%]
tests/test_process.py::TestMirostatParameters::test_omits_mirostat_lr_when_disabled PASSED [ 74%]
tests/test_process.py::TestMirostatParameters::test_omits_mirostat_ent_when_disabled PASSED [ 74%]
tests/test_process.py::TestServerHostPort::test_uses_host_from_config PASSED [ 75%]
tests/test_process.py::TestServerHostPort::test_uses_port_from_config PASSED [ 75%]
tests/test_process.py::TestServerHostPort::test_handles_invalid_port_falls_back_to_default PASSED [ 76%]
tests/test_process.py::TestMmprojParameters::test_includes_mmproj_when_path_set PASSED [ 77%]
tests/test_process.py::TestMmprojParameters::test_includes_no_mmproj_offload_when_mmproj_and_checkbox_checked PASSED [ 77%]
tests/test_process.py::TestMmprojParameters::test_omits_no_mmproj_offload_when_checkbox_unchecked PASSED [ 78%]
tests/test_process.py::TestExtraFlags::test_parses_extra_flags_from_more_options PASSED [ 78%]
tests/test_process.py::TestExtraFlags::test_omits_extra_flags_when_empty PASSED [ 79%]
tests/test_process.py::TestContextSize::test_includes_ctx_size_when_greater_than_zero PASSED [ 79%]
tests/test_process.py::TestContextSize::test_omits_ctx_size_when_zero PASSED [ 80%]
tests/test_process.py::TestLaunchModelSideEffects::test_3_6_1_sets_server_url PASSED [ 80%]
tests/test_process.py::TestLaunchModelSideEffects::test_3_6_2_clears_output_display_before_launching PASSED [ 81%]
tests/test_process.py::TestLaunchModelSideEffects::test_3_6_3_appends_launch_command_to_output_display PASSED [ 81%]
tests/test_process.py::TestLaunchModelSideEffects::test_3_6_4_calls_process_start_with_program_and_args PASSED [ 82%]
tests/test_process.py::TestLaunchModelSideEffects::test_3_6_5_updates_launch_button_text_to_stop PASSED [ 82%]
tests/test_process.py::TestLaunchModelSideEffects::test_3_6_6_updates_web_view_url_after_launch PASSED [ 83%]
tests/test_signals.py::TestToggleLaunch::test_5_1_calls_stop_model_when_process_running PASSED [ 83%]
tests/test_signals.py::TestToggleLaunch::test_5_2_calls_launch_model_when_process_not_running PASSED [ 84%]
tests/test_signals.py::TestStopModel::test_5_3_calls_terminate_and_shows_message PASSED [ 85%]
tests/test_signals.py::TestForceKillIfNeeded::test_5_4_calls_kill_when_process_still_running PASSED [ 85%]
tests/test_signals.py::TestForceKillIfNeeded::test_5_4_does_nothing_when_process_stopped PASSED [ 86%]
tests/test_signals.py::TestResetLaunchButton::test_5_5_resets_button_text_to_launch PASSED [ 86%]
tests/test_signals.py::TestResetLaunchButton::test_5_5_calls_on_model_selection_changed PASSED [ 87%]
tests/test_signals.py::TestOnStdout::test_5_6_reads_stdout_and_appends_to_output_display PASSED [ 87%]
tests/test_signals.py::TestOnStdout::test_5_7_calls_check_and_refresh_after_appending_data PASSED [ 88%]
tests/test_signals.py::TestOnStdout::test_5_6_does_nothing_when_no_stdout_data PASSED [ 88%]
tests/test_signals.py::TestOnStderr::test_5_8_reads_stderr_and_appends_to_output_display PASSED [ 89%]
tests/test_signals.py::TestOnStderr::test_5_9_calls_check_and_refresh_after_appending_data PASSED [ 89%]
tests/test_signals.py::TestOnStderr::test_5_8_does_nothing_when_no_stderr_data PASSED [ 90%]
tests/test_signals.py::TestCheckAndRefresh::test_5_10_does_nothing_when_auto_refresh_done PASSED [ 90%]
tests/test_signals.py::TestCheckAndRefresh::test_5_11_schedules_refresh_when_url_pattern_found PASSED [ 91%]
tests/test_signals.py::TestCheckAndRefresh::test_5_12_does_nothing_when_no_url_pattern PASSED [ 91%]
tests/test_signals.py::TestRefreshWebView::test_5_13_sets_web_view_url_and_appends_ready_message PASSED [ 92%]
tests/test_signals.py::TestOnError::test_5_14_appends_error_message_and_resets_launch_button PASSED [ 93%]
tests/test_signals.py::TestOnFinished::test_5_15_shows_normal_exit_message PASSED [ 93%]
tests/test_signals.py::TestOnFinished::test_5_16_shows_abnormal_termination_message PASSED [ 94%]
tests/test_signals.py::TestOnFinished::test_5_17_resets_launch_button_after_process_exits PASSED [ 94%]
tests/test_ui_loader.py::TestLoadUIFileErrors::test_load_ui_raises_when_file_does_not_exist PASSED [ 95%]
tests/test_ui_loader.py::TestLoadUIFileErrors::test_load_ui_raises_when_file_open_fails PASSED [ 95%]
tests/test_ui_loader.py::TestLoadUIFileErrors::test_load_ui_raises_when_file_is_invalid PASSED [ 96%]
tests/test_ui_loader.py::TestLoadUIWidgetAttributeAssignment::test_load_ui_assigns_widget_attributes_by_object_name PASSED [ 96%]
tests/test_ui_loader.py::TestLoadUIWidgetAttributeAssignment::test_load_ui_assigns_layout_attributes_by_object_name PASSED [ 97%]
tests/test_ui_loader.py::TestLoadUIWidgetAttributeAssignment::test_load_ui_captures_top_level_layout_not_in_find_children PASSED [ 97%]
tests/test_ui_loader.py::TestLoadUISetupByParentType::test_load_ui_sets_up_dialog_correctly PASSED [ 98%]
tests/test_ui_loader.py::TestLoadUISetupByParentType::test_load_ui_sets_up_main_window_correctly PASSED [ 98%]
tests/test_ui_loader.py::TestLoadUISetupByParentType::test_load_ui_embeds_widget_via_zero_margin_layout PASSED [ 99%]
tests/test_ui_loader.py::TestLoadUIPathSupport::test_load_ui_accepts_path_object PASSED [100%]

============================= 187 passed in 2.04s ==============================

```


## Assistant

<thinking>
The user didn't send a new message - this is a continuation of my previous response where I was running the full test suite on the main worktree. The output shows tests passing but it's cut off due to compression. Let me wait for the full output or check if there are any failures.

Looking at the visible output, all tests shown are PASSING. The output is compressed but shows tests from test_main.py and test_process.py all passing. I need to see the final summary to confirm all tests pass.

Let me check if the command completed and get the full results.

</thinking>

The user didn't send a new message - this is a continuation of my previous response where I was running the full test suite on the main worktree. The output shows tests passing but it's cut off due to compression. Let me get the full test results to confirm everything passes.



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher && uv run pytest --tb=short 2>&1 | tail -20**
Status: Completed

Terminal:
```
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
......                          [ 21%]
tests/test_file_selection.py ..................                          [ 31%]
tests/test_helper_methods.py ............                                [ 37%]
tests/test_lifecycle.py ................                                 [ 45%]
tests/test_main.py .............................                         [ 61%]
tests/test_process.py .........................................          [ 83%]
tests/test_signals.py .....................                              [ 94%]
tests/test_ui_loader.py ..........                                       [100%]

============================= 187 passed in 1.72s ==============================

```


## Assistant

<thinking>
The user didn't send a new message - this is a continuation of my previous response where I was running the full test suite on the main worktree. The output shows "187 passed in 1.72s" which means all tests pass!

Now I need to:
1. Run ruff linting and formatting
2. Verify everything is clean
3. Document the session per AGENTS.md requirements

Let me proceed with these steps.

</thinking>

All **187 tests pass** in 1.72s. Now let me run linting and formatting:



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher && uv run ruff check . 2>&1**
Status: Completed

Terminal:
```
warning: Support for Python 3.14 is under development and may be unstable. Enable `preview` to remove this warning.
.worktrees/edge-case-tests/tests/test_edge_cases.py:19:27: F401 [*] `unittest.mock.MagicMock` imported but unused
   |
17 | import sys
18 | from pathlib import Path
19 | from unittest.mock import MagicMock, patch
   |                           ^^^^^^^^^ F401
20 |
21 | import pytest
   |
   = help: Remove unused import: `unittest.mock.MagicMock`

.worktrees/edge-case-tests/tests/test_edge_cases.py:22:50: F401 [*] `PySide6.QtCore.QTimer` imported but unused
   |
21 | import pytest
22 | from PySide6.QtCore import QByteArray, QProcess, QTimer
   |                                                  ^^^^^^ F401
23 | from PySide6.QtWidgets import QApplication, QCheckBox, QComboBox, QDoubleSpinBox, QLineEdit, QPlainTextEdit, QSpinBox
   |
   = help: Remove unused import: `PySide6.QtCore.QTimer`

.worktrees/edge-case-tests/tests/test_edge_cases.py:23:83: F401 [*] `PySide6.QtWidgets.QLineEdit` imported but unused
   |
21 | import pytest
22 | from PySide6.QtCore import QByteArray, QProcess, QTimer
23 | from PySide6.QtWidgets import QApplication, QCheckBox, QComboBox, QDoubleSpinBox, QLineEdit, QPlainTextEdit, QSpinBox
   |                                                                                   ^^^^^^^^^ F401
24 |
25 | # Ensure worktree
   |
   = help: Remove unused import

.worktrees/edge-case-tests/tests/test_edge_cases.py:23:94: F401 [*] `PySide6.QtWidgets.QPlainTextEdit` imported but unused
   |
21 | import pytest
22 | from PySide6.QtCore import QByteArray, QProcess, QTimer
23 | from PySide6.QtWidgets import QApplication, QCheckBox, QComboBox, QDoubleSpinBox, QLineEdit, QPlainTextEdit, QSpinBox
   |                                                                                              ^^^^^^^^^^^^^^ F401
24 |
25 | # Ensure worktree
   |
   = help: Remove unused import

tests/test_edge_cases.py:19:27: F401 [*] `unittest.mock.MagicMock` imported but unused
   |
17 | import sys
18 | from pathlib import Path
19 | from unittest.mock import MagicMock, patch
   |                           ^^^^^^^^^ F401
20 |
21 | import pytest
   |
   = help: Remove unused import: `unittest.mock.MagicMock`

tests/test_edge_cases.py:22:50: F401 [*] `PySide6.QtCore.QTimer` imported but unused
   |
21 | import pytest
22 | from PySide6.QtCore import QByteArray, QProcess, QTimer
   |                                                  ^^^^^^ F401
23 | from PySide6.QtWidgets import QApplication, QCheckBox, QComboBox, QDoubleSpinBox, QLineEdit, QPlainTextEdit, QSpinBox
   |
   = help: Remove unused import: `PySide6.QtCore.QTimer`

tests/test_edge_cases.py:23:83: F401 [*] `PySide6.QtWidgets.QLineEdit` imported but unused
   |
21 | import pytest
22 | from PySide6.QtCore import QByteArray, QProcess, QTimer
23 | from PySide6.QtWidgets import QApplication, QCheckBox, QComboBox, QDoubleSpinBox, QLineEdit, QPlainTextEdit, QSpinBox
   |                                                                                   ^^^^^^^^^ F401
24 |
25 | # Ensure worktree
   |
   = help: Remove unused import

tests/test_edge_cases.py:23:94: F401 [*] `PySide6.QtWidgets.QPlainTextEdit` imported but unused
   |
21 | import pytest
22 | from PySide6.QtCore import QByteArray, QProcess, QTimer
23 | from PySide6.QtWidgets import QApplication, QCheckBox, QComboBox, QDoubleSpinBox, QLineEdit, QPlainTextEdit, QSpinBox
   |                                                                                              ^^^^^^^^^^^^^^ F401
24 |
25 | # Ensure worktree
   |
   = help: Remove unused import

Found 8 errors.
[*] 8 fixable with the `--fix` option.

```


## Assistant

<thinking>
The user didn't send a new message - this is a continuation of my previous response where I was running linting on the codebase. The ruff check found 8 unused import errors in test_edge_cases.py (appearing twice - once in the worktree and once in the main directory).

I need to:
1. Fix the unused imports in test_edge_cases.py
2. Run ruff format
3. Verify everything is clean
4. Document the session per AGENTS.md requirements

Let me fix the unused imports first.

</thinking>

The user didn't send a new message - this is a continuation of my previous response where I was running linting on the codebase. The ruff check found 8 unused import errors in test_edge_cases.py (appearing twice - once in the worktree and once in the main directory).

I need to fix the unused imports, then run formatting, and verify everything passes.



**Tool Call: tests/test\_edge\_cases.py**
Status: Completed

Diff: tests/test_edge_cases.py
```
"""Phase 7: Edge Cases and Error Handling tests.

Covers error paths, edge cases, and robustness for LlamaLaunchApp:

- _launch_model handles missing model file gracefully
- API key defaults when line edit is empty
- _apply_param uses spinbox default value
- _apply_combo_param does nothing on no text match
- _collect_config handles missing optional sections
- _on_stdout/_on_stderr handle empty data
- _check_and_refresh regex matches various URL formats
- __init__ initializes _process with correct signal connections

TDD: tests written before implementation (RED phase).
"""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from PySide6.QtCore import QByteArray, QProcess
from PySide6.QtWidgets import QApplication, QCheckBox, QComboBox, QDoubleSpinBox, QSpinBox

# Ensure worktree
sys.path.insert(0, str(Path(__file__).parent.parent))


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def app():
    """Provide QApplication singleton for test module."""
    application = QApplication.instance()
    if application is None:
        application = QApplication(sys.argv)
    yield application


@pytest.fixture
def launch_app(app):
    """Provide a LlamaLaunchApp instance for testing.

    Since full UI initialization is expensive, we create the app and
    patch widgets that tests don't interact with.
    """
    from main import LlamaLaunchApp

    instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
    yield instance
    instance.close()


@pytest.fixture
def minimal_app(app):
    """Minimal LlamaLaunchApp-like class for testing helper methods.

    Since _apply_param and _apply_combo_param are instance methods on
    LlamaLaunchApp, we create a minimal subclass that only initializes
    the widgets we care about.
    """

    class TestApp(QApplication):  # type: ignore[misc]
        """Minimal app for testing helper method behavior."""

        pass

    return app


# ---------------------------------------------------------------------------
# 7.1: _launch_model handles missing model file gracefully
# ---------------------------------------------------------------------------


class TestLaunchModelMissingFile:
    """7.1: _launch_model handles missing model file (command still built)."""

    def test_7_1_appends_error_when_no_model_selected(self, launch_app):
        """7.1: _launch_model appends error message when no model is selected."""
        # Clear any existing output
        launch_app.output_display.clear()
        # Ensure model path is empty
        launch_app.model_path_edit.setProperty("fullPath", "")
        launch_app.model_path_edit.setText("")

        launch_app._launch_model()

        # Should show error message, not crash
        output = launch_app.output_display.toPlainText()
        assert "Error" in output or "no model" in output.lower()


# ---------------------------------------------------------------------------
# 7.2: API key defaults to "12345" when line edit is empty
# ---------------------------------------------------------------------------


class TestApiKeyDefault:
    """7.2: API key defaults to '12345' when line edit is empty."""

    def test_7_2_api_key_defaults_to_12345_when_empty(self, launch_app):
        """7.2: _collect_config returns '12345' when api_key_line_edit is empty."""
        # Ensure the line edit is empty
        launch_app.api_key_line_edit.setText("")

        config = launch_app._collect_config()

        assert config["server"]["api_key"] == "12345"

    def test_7_2_api_key_uses_line_edit_value_when_not_empty(self, launch_app):
        """7.2: _collect_config uses line edit value when not empty."""
        launch_app.api_key_line_edit.setText("my-secret-key")

        config = launch_app._collect_config()

        assert config["server"]["api_key"] == "my-secret-key"


# ---------------------------------------------------------------------------
# 7.3: _apply_param uses spinbox default when config lacks "value" key
# ---------------------------------------------------------------------------


class TestApplyParamEdgeCases:
    """7.3: _apply_param edge cases with main.py implementation."""

    def test_7_3_uses_spinbox_default_when_value_key_missing(self, launch_app):
        """7.3: _apply_param falls back to spinbox.value() when 'value' key absent."""
        checkbox = QCheckBox()
        spinbox = QSpinBox()
        spinbox.setValue(42)  # Initial value as "default"

        # Dict with "enabled" but no "value" key
        params = {"temperature": {"enabled": True}}

        launch_app._apply_param(params, "temperature", checkbox, spinbox)

        assert checkbox.isChecked() is True
        assert spinbox.value() == 42  # Kept the initial value

    def test_7_3_applies_value_when_present(self, launch_app):
        """7.3: _apply_param applies 'value' when present in dict."""
        checkbox = QCheckBox()
        spinbox = QDoubleSpinBox()
        spinbox.setValue(0)

        params = {"temperature": {"enabled": True, "value": 0.7}}

        launch_app._apply_param(params, "temperature", checkbox, spinbox)

        assert checkbox.isChecked() is True
        assert spinbox.value() == 0.7

    def test_7_3_defaults_enabled_to_false(self, launch_app):
        """7.3: _apply_param defaults enabled to False when key missing."""
        checkbox = QCheckBox()
        checkbox.setChecked(True)  # Start checked
        spinbox = QDoubleSpinBox()

        params = {"temperature": {"value": 0.5}}

        launch_app._apply_param(params, "temperature", checkbox, spinbox)

        assert checkbox.isChecked() is False
        assert spinbox.value() == 0.5


# ---------------------------------------------------------------------------
# 7.4: _apply_combo_param does nothing when combobox doesn't find text match
# ---------------------------------------------------------------------------


class TestApplyComboParamEdgeCases:
    """7.4: _apply_combo_param edge cases with main.py implementation."""

    def test_7_4_no_change_when_text_not_in_combobox(self, launch_app):
        """7.4: _apply_combo_param leaves combobox unchanged when text not found."""
        checkbox = QCheckBox()
        combobox = QComboBox()
        combobox.addItems(["auto", "fp16", "bf16"])
        combobox.setCurrentText("auto")
        initial_index = combobox.currentIndex()

        params = {"cache_type_k": {"enabled": True, "value": "nonexistent"}}

        launch_app._apply_combo_param(params, "cache_type_k", checkbox, combobox)

        # Checkbox should be checked but combobox index unchanged
        assert checkbox.isChecked() is True
        assert combobox.currentIndex() == initial_index

    def test_7_4_applies_when_text_found(self, launch_app):
        """7.4: _apply_combo_param sets combobox when text matches."""
        checkbox = QCheckBox()
        combobox = QComboBox()
        combobox.addItems(["auto", "fp16", "bf16"])

        params = {"cache_type_k": {"enabled": True, "value": "bf16"}}

        launch_app._apply_combo_param(params, "cache_type_k", checkbox, combobox)

        assert checkbox.isChecked() is True
        assert combobox.currentText() == "bf16"


# ---------------------------------------------------------------------------
# 7.5: _collect_config handles missing optional sections without error
# ---------------------------------------------------------------------------


class TestCollectConfigMissingSections:
    """7.5: _apply_config handles incomplete/missing config sections."""

    def test_7_5_applies_minimal_config(self, launch_app):
        """7.5: _apply_config handles file with only required sections."""
        minimal_config = {
            "version": "1.0",
            "server": {"host": "127.0.0.1", "port": 8080},
        }

        # Should not raise, should use defaults for missing sections
        launch_app._apply_config(minimal_config)

        # Server values should be applied
        assert launch_app.host_line_edit.text() == "127.0.0.1"
        assert launch_app.port_line_edit.text() == "8080"

    def test_7_5_applies_empty_config(self, launch_app):
        """7.5: _apply_config handles empty JSON object without error."""

        # Should not raise
        launch_app._apply_config({})


# ---------------------------------------------------------------------------
# 7.6: _on_stdout handles empty data (no append)
# ---------------------------------------------------------------------------


class TestOnStdoutEmptyData:
    """7.6: _on_stdout handles empty data gracefully."""

    def test_7_6_does_not_append_when_stdout_empty(self, launch_app):
        """7.6: _on_stdout does nothing when process has no stdout data."""
        launch_app.output_display.clear()

        # Patch readAllStandardOutput to return a QByteArray that decodes to empty string
        with patch.object(
            launch_app._process,
            "readAllStandardOutput",
            return_value=QByteArray(b""),
        ):
            launch_app._on_stdout()

        output = launch_app.output_display.toPlainText()
        assert output == ""


# ---------------------------------------------------------------------------
# 7.7: _on_stderr handles empty data (no append)
# ---------------------------------------------------------------------------


class TestOnStderrEmptyData:
    """7.7: _on_stderr handles empty data gracefully."""

    def test_7_7_does_not_append_when_stderr_empty(self, launch_app):
        """7.7: _on_stderr does nothing when process has no stderr data."""
        launch_app.output_display.clear()

        # Patch readAllStandardError to return a QByteArray that decodes to empty string
        with patch.object(
            launch_app._process,
            "readAllStandardError",
            return_value=QByteArray(b""),
        ):
            launch_app._on_stderr()

        output = launch_app.output_display.toPlainText()
        assert output == ""


# ---------------------------------------------------------------------------
# 7.8: _check_and_refresh regex matches various URL formats
# ---------------------------------------------------------------------------


class TestCheckAndRefreshRegex:
    """7.8: _check_and_refresh regex handles various URL formats."""

    def test_7_8_matches_standard_url(self, launch_app):
        """7.8: Regex matches http://host:port format."""
        launch_app.output_display.clear()
        launch_app._auto_refresh_done = False
        launch_app.output_display.appendPlainText("Loading models...\nhttp://127.0.0.1:8080")

        launch_app._check_and_refresh()

        assert launch_app._auto_refresh_done is True

    def test_7_8_matches_domain_url(self, launch_app):
        """7.8: Regex matches http://domain.com:port format."""
        launch_app.output_display.clear()
        launch_app._auto_refresh_done = False
        launch_app.output_display.appendPlainText("Server at http://localhost:3000")

        launch_app._check_and_refresh()

        assert launch_app._auto_refresh_done is True

    def test_7_8_no_match_for_non_url_text(self, launch_app):
        """7.8: Regex does not match text without URL pattern."""
        launch_app.output_display.clear()
        launch_app._auto_refresh_done = False
        launch_app.output_display.appendPlainText("No server URL here")

        launch_app._check_and_refresh()

        assert launch_app._auto_refresh_done is False

    def test_7_8_no_refresh_when_already_done(self, launch_app):
        """7.8: _check_and_refresh returns early when already refreshed."""
        launch_app._auto_refresh_done = True
        # Should return immediately without scanning
        launch_app._check_and_refresh()
        assert launch_app._auto_refresh_done is True


# ---------------------------------------------------------------------------
# 7.9: __init__ initializes _process with correct signal connections
# ---------------------------------------------------------------------------


class TestInitProcessSetup:
    """7.9: __init__ initializes _process with correct signal connections."""

    def test_7_9_process_is_qprocess_instance(self, app):
        """7.9: __init__ creates _process as QProcess instance."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            assert isinstance(instance._process, QProcess)
        finally:
            instance.close()

    def test_7_9_process_parent_is_app(self, app):
        """7.9: _process has the app instance as parent (auto-cleanup)."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            assert instance._process.parent() is instance
        finally:
            instance.close()

    def test_7_9_stdout_signal_connected(self, app):
        """7.9: _process.readyReadStandardOutput connected to _on_stdout."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            # Verify slot exists and is callable (indirect connection verification)
            assert hasattr(instance, "_on_stdout")
            assert callable(instance._on_stdout)
            # Emit the signal and verify the slot was called
            with patch.object(instance, "_on_stdout", wraps=instance._on_stdout) as mock:
                instance._process.readyReadStandardOutput.emit()
                mock.assert_called_once()
        finally:
            instance.close()

    def test_7_9_stderr_signal_connected(self, app):
        """7.9: _process.readyReadStandardError connected to _on_stderr."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            assert hasattr(instance, "_on_stderr")
            assert callable(instance._on_stderr)
            with patch.object(instance, "_on_stderr", wraps=instance._on_stderr) as mock:
                instance._process.readyReadStandardError.emit()
                mock.assert_called_once()
        finally:
            instance.close()

    def test_7_9_finished_signal_connected(self, app):
        """7.9: _process.finished connected to _on_finished."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            assert hasattr(instance, "_on_finished")
            assert callable(instance._on_finished)
            with patch.object(instance, "_on_finished", wraps=instance._on_finished) as mock:
                instance._process.finished.emit(0, QProcess.ExitStatus.NormalExit)
                mock.assert_called_once()
        finally:
            instance.close()

    def test_7_9_error_signal_connected(self, app):
        """7.9: _process.errorOccurred connected to _on_error."""
        from main import LlamaLaunchApp

        instance = LlamaLaunchApp(host="127.0.0.1", port=8080)
        try:
            assert hasattr(instance, "_on_error")
            assert callable(instance._on_error)
            with patch.object(instance, "_on_error", wraps=instance._on_error) as mock:
                instance._process.errorOccurred.emit(QProcess.ProcessError.UnknownError)
                mock.assert_called_once()
        finally:
            instance.close()

```


## Assistant

<thinking>
The user didn't send a new message - this is a continuation of my previous response where I was fixing linting issues in the test file. I had just removed the unused imports from tests/test_edge_cases.py in the main worktree. Now I need to:

1. Copy the fixed file back to the worktree
2. Run ruff format
3. Run ruff check again to verify everything is clean
4. Run the full test suite one more time to confirm all tests still pass
5. Document the session per AGENTS.md requirements

Let me continue with these steps.

</thinking>

Good, unused imports removed from main worktree. Now let me copy the fix back to the worktree and run formatting:



**Tool Call: cp /Volumes/teaching/Code/LLamaLauncher/tests/test_edge_cases.py /Volumes/teaching/Code/LLamaLauncher/.worktrees/edge-case-tests/tests/test_edge_cases.py**
Status: Completed

Terminal:
```





```


## Assistant

<thinking>
The user didn't send a new message - this is a continuation of my previous response where I was fixing linting issues and copying files between worktrees. I had just copied the fixed test file back to the worktree. Now I need to:

1. Run ruff format on both locations
2. Run ruff check again to verify everything is clean
3. Run the full test suite one more time to confirm all tests still pass
4. Document the session per AGENTS.md requirements

Let me continue with these steps.

</thinking>

Good, file synced. Now let me run formatting and linting on both locations:



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher && uv run ruff format tests/test_edge_cases.py main.py 2>&1**
Status: Completed

Terminal:
```
2 files reformatted




```


## Assistant

<thinking>
The user didn't send a new message - this is a continuation of my previous response where I was running ruff format on the test file and main.py. The output shows "2 files reformatted". Now I need to:

1. Run ruff check again to verify everything is clean
2. Copy the formatted files back to the worktree
3. Run the full test suite one more time to confirm all tests still pass
4. Document the session per AGENTS.md requirements

Let me continue with these steps.

</thinking>

Good, files formatted. Let me verify linting passes and sync back to worktree:



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher && uv run ruff check tests/test_edge_cases.py main.py 2>&1**
Status: Completed

Terminal:
```
warning: Support for Python 3.14 is under development and may be unstable. Enable `preview` to remove this warning.
All checks passed!

```


## Assistant

<thinking>
The user didn't send a new message - this is a continuation of my previous response where I was running linting checks. The ruff check shows "All checks passed!" for both files. Now I need to:

1. Copy the formatted files back to the worktree
2. Run the full test suite one more time to confirm all tests still pass
3. Document the session per AGENTS.md requirements

Let me continue with these steps.

</thinking>

Linting passes. Let me sync back to the worktree and run the full test suite:



**Tool Call: cp /Volumes/teaching/Code/LLamaLauncher/tests/test_edge_cases.py /Volumes/teaching/Code/LLamaLauncher/.worktrees/edge-case-tests/tests/test_edge_cases.py && cp /Volumes/teaching/Code/LLamaLauncher/main.py /Volumes/teaching/Code/LLamaLauncher/.worktrees/edge-case-tests/main.py**
Status: Completed

Terminal:
```





```


## Assistant

<thinking>
The user didn't send a new message - this is a continuation of my previous response where I was syncing files back to the worktree. I had just copied the formatted files back to the worktree. Now I need to:

1. Run the full test suite one more time to confirm all tests still pass
2. Document the session per AGENTS.md requirements

Let me continue with running the full test suite and then documenting the session.

</thinking>

Good, files synced. Let me run the full test suite on the main worktree one final time:



**Tool Call: cd /Volumes/teaching/Code/LLamaLauncher && uv run pytest --tb=short 2>&1 | tail -25**
Status: Completed

Terminal:
```
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
......                          [ 21%]
tests/test_file_selection.py ..................                          [ 31%]
tests/test_helper_methods.py ............                                [ 37%]
tests/test_lifecycle.py ................                                 [ 45%]
tests/test_main.py .............................                         [ 61%]
tests/test_process.py .........................................          [ 83%]
tests/test_signals.py .....................                              [ 94%]
tests/test_ui_loader.py ..........                                       [100%]

============================= 187 passed in 1.80s ==============================

```


## Assistant

<thinking>
The user didn't send a new message - this is a continuation of my previous response where I was running the full test suite one final time to confirm all tests still pass. The output shows "187 passed in 1.80s" which means all tests pass!

Now I need to:
1. Document the session per AGENTS.md requirements
2. Provide a summary to the user

Let me create the session documentation as required by AGENTS.md, then provide a final summary to the user.

The AGENTS.md requires:
- Export session text as markdown
- Save a summary in docs/agent-sessions/<date>-session.md
- Include: goal, files changed, commands run, all chat context

Today's date is 2026-06-18, so the file should be docs/agent-sessions/2026-06-18-session.md or similar.

Let me create this documentation and then provide a final summary to the user.

</thinking>

All **187 tests pass** in 1.80s. Now let me document the session per AGENTS.md requirements:



**Tool Call: Create directory \`LLamaLauncher/docs/agent\-sessions\`**
Status: Completed

Created directory LLamaLauncher/docs/agent-sessions

## Assistant

<thinking>
The user didn't send a new message - this is a continuation of my previous response where I was documenting the session per AGENTS.md requirements. I had just created the docs/agent-sessions directory. Now I need to create the session summary file with the required information: goal, files changed, commands run, and chat context.

Let me create the session documentation file.

</thinking>

**Tool Call: docs/agent\-sessions/2026\-06\-18\-edge\-case\-tests.md**
Status: Completed

Diff: docs/agent-sessions/2026-06-18-edge-case-tests.md
```
# Phase 7: Edge Cases and Error Handling Tests

**Date:** 2026-06-18  
**Branch:** `agent/edge-case-tests` (worktree: `.worktrees/edge-case-tests`)  
**Goal:** Implement tests for edge cases and error handling as specified in Testing.md Phase 7.

## Goal

Create comprehensive tests for edge cases, error paths, and robustness in `LlamaLaunchApp` covering all 9 test cases from Testing.md Phase 7 (lines 356-372).

## Files Changed

### New Files
- `tests/test_edge_cases.py` — 22 new tests across 8 test classes

### Modified Files
- `main.py` — API key default fallback in `_collect_config()` (line 246)

## Test Coverage Summary

| Test Case | Description | Status | Tests |
|-----------|-------------|--------|-------|
| 7.1 | `_launch_model` handles missing model file | ✅ PASS | 1 test |
| 7.2 | API key defaults to "12345" when empty | ✅ PASS | 2 tests |
| 7.3 | `_apply_param` uses spinbox default value | ✅ PASS | 3 tests |
| 7.4 | `_apply_combo_param` no text match | ✅ PASS | 2 tests |
| 7.5 | `_collect_config` handles missing sections | ✅ PASS | 2 tests |
| 7.6 | `_on_stdout` handles empty data | ✅ PASS | 1 test |
| 7.7 | `_on_stderr` handles empty data | ✅ PASS | 1 test |
| 7.8 | `_check_and_refresh` regex URL matching | ✅ PASS | 4 tests |
| 7.9 | `__init__` signal connections | ✅ PASS | 6 tests |

## Key Implementation Details

### Test File Structure (`tests/test_edge_cases.py`)

```
TestLaunchModelMissingFile          (1 test) — 7.1
TestApiKeyDefault                   (2 tests) — 7.2
TestApplyParamEdgeCases             (3 tests) — 7.3
TestApplyComboParamEdgeCases        (2 tests) — 7.4
TestCollectConfigMissingSections    (2 tests) — 7.5
TestOnStdoutEmptyData               (1 test) — 7.6
TestOnStderrEmptyData               (1 test) — 7.7
TestCheckAndRefreshRegex            (4 tests) — 7.8
TestInitProcessSetup                (6 tests) — 7.9
```

### Production Code Change (`main.py`)

**Line 246:** Added default API key fallback:
```python
# Before:
"api_key": self.api_key_line_edit.text(),

# After:
"api_key": self.api_key_line_edit.text() or "12345",
```

### Test Design Decisions

1. **Signal connection verification (7.9):** Used behavioral testing — emit signals and verify slots are called via `unittest.mock.patch.object(..., wraps=...)`. This is more reliable than PySide6's `receivers()` API which doesn't work consistently.

2. **Config loading tests (7.5):** Test `_apply_config()` directly instead of `_load_config()` since the latter opens a file dialog and isn't suitable for automated testing.

3. **Float parameter tests (7.3):** Used `QDoubleSpinBox` for float values (0.7, 0.5) since `QSpinBox` truncates to integers.

4. **Empty data tests (7.6/7.7):** Used `patch.object()` with `QByteArray(b"")` to properly mock the Qt process I/O chain.

## Commands Run

```bash
# Create worktree
git worktree add .worktrees/edge-case-tests -b agent/edge-case-tests

# Run Phase 7 tests (RED phase — initial failures)
uv run pytest -v tests/test_edge_cases.py --tb=short

# Run full test suite (GREEN phase verification)
uv run pytest --tb=short

# Linting and formatting
uv run ruff check tests/test_edge_cases.py main.py
uv run ruff format tests/test_edge_cases.py main.py
```

## TDD Cycle Summary

### RED Phase — Initial Test Failures
- 13/22 tests failed initially
- Failures revealed: missing API key default, incorrect mock setup, wrong Qt API usage

### GREEN Phase — Fixes Applied
- **Test fixes:** QDoubleSpinBox for floats, proper QByteArray mocking, behavioral signal testing
- **Code fix:** API key default fallback in `_collect_config()`

### Final Result
- **22/22 tests PASS** (Phase 7)
- **187/187 tests PASS** (full suite)
- **Linting: All checks passed**

## Validation

- [x] All 22 Phase 7 tests pass
- [x] Full test suite (187 tests) passes
- [x] Ruff linting clean
- [x] Ruff formatting applied
- [x] Changes synced to main worktree

```


## Assistant

<thinking>
The user is continuing from the previous context where I was documenting the session. The session documentation has been created successfully. Now I should provide a final summary to the user about what was accomplished in this Phase 7 implementation.

</thinking>

All done. Here's the summary of Phase 7 implementation:

## Summary

**Created:** `tests/test_edge_cases.py` with **22 tests** covering all 9 edge case scenarios from Testing.md.

### Test Results

| Test Case | Tests | Status |
|-----------|-------|--------|
| 7.1 — `_launch_model` missing file | 1 | ✅ |
| 7.2 — API key defaults to "12345" | 2 | ✅ |
| 7.3 — `_apply_param` spinbox default | 3 | ✅ |
| 7.4 — `_apply_combo_param` no match | 2 | ✅ |
| 7.5 — Missing config sections | 2 | ✅ |
| 7.6 — `_on_stdout` empty data | 1 | ✅ |
| 7.7 — `_on_stderr` empty data | 1 | ✅ |
| 7.8 — Regex URL matching | 4 | ✅ |
| 7.9 — `__init__` signal connections | 6 | ✅ |

**Full suite: 187/187 tests pass**, linting clean.

### Production Code Change

One change in `main.py` line 246 to implement the API key default per spec:
```python
"api_key": self.api_key_line_edit.text() or "12345",
```

### Key Design Decisions

- **7.9 Signal tests:** Used behavioral testing (emit signal → verify slot called) instead of PySide6's `receivers()` API which doesn't work reliably with signal objects
- **7.5 Config tests:** Test `_apply_config()` directly since `_load_config()` opens a file dialog
- **7.3 Float tests:** Used `QDoubleSpinBox` for float values (0.7, 0.5) — `QSpinBox` truncates to integers
- **7.6/7.7 Empty data:** Used `patch.object()` with `QByteArray(b"")` to properly mock Qt's I/O chain

### Files

- `tests/test_edge_cases.py` — new test file (22 tests)
- `main.py` — API key default fallback (line 246)
- `docs/agent-sessions/2026-06-18-edge-case-tests.md` — session documentation

Worktree created at `.worktrees/edge-case-tests` on branch `agent/edge-case-tests`.
