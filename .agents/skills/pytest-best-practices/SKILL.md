---
name: pytest-best-practices
description: Use when writing or maintaining Python tests with pytest.
---

# Pytest Best Practices

## Overview

Use pytest to create fast, readable, maintainable tests that verify
behavior.

This skill applies after the TDD process has decided what needs testing.

Focus: - Writing idiomatic pytest - Designing maintainable tests - Using
fixtures correctly - Avoiding brittle tests - Keeping tests readable -
Managing complex test environments with nox

------------------------------------------------------------------------

# Test Structure

## Follow Arrange-Act-Assert

Every test should clearly separate:

1.  Arrange - setup test data/state
2.  Act - execute the behavior
3.  Assert - verify the result

Good:

``` python
def test_user_registration_rejects_duplicate_email():
    service = UserService()
    service.create_user("test@example.com")

    result = service.create_user("test@example.com")

    assert result.error == "Email already exists"
```

------------------------------------------------------------------------

# Test Naming

Test names should describe behavior.

Good:

``` python
def test_payment_fails_when_card_is_expired():
    ...
```

Bad:

``` python
def test_payment():
    ...
```

------------------------------------------------------------------------

# Assertions

Prefer direct assertions:

``` python
assert user.name == "Alice"
assert response.status_code == 200
```

Test behavior, not implementation details.

------------------------------------------------------------------------

# One Behaviour Per Test

Tests should verify one thing.

Good:

``` python
def test_discount_is_applied_to_members():
    price = calculate_price(100, member=True)

    assert price == 90
```

------------------------------------------------------------------------

# Fixtures

Use fixtures for reusable setup:

``` python
import pytest

@pytest.fixture
def user():
    return User(name="Alice")
```

Keep fixtures isolated and avoid shared mutable state.

------------------------------------------------------------------------

# Parametrized Tests

Use parametrization for multiple inputs:

``` python
@pytest.mark.parametrize(
    "email",
    ["", "invalid", "missing@domain"]
)
def test_invalid_emails_are_rejected(email):
    assert validate_email(email) is False
```

------------------------------------------------------------------------

# Exception Testing

Use pytest.raises:

``` python
with pytest.raises(FileNotFoundError):
    load_file("missing.txt")
```

------------------------------------------------------------------------

# Mocking

Mock only external boundaries:

-   Network calls
-   Filesystem
-   Time
-   External services

Avoid mocking your own code because it tests the mock rather than the
behavior.

------------------------------------------------------------------------

# Temporary Files

Use tmp_path:

``` python
def test_save_file(tmp_path):
    path = tmp_path / "data.txt"

    save_data(path, "hello")

    assert path.read_text() == "hello"
```

------------------------------------------------------------------------

# Nox for Complex Test Workflows

Use nox when tests need multiple environments, Python versions, external
services, or repeatable automation.

Nox creates isolated test sessions using virtual environments.

Common uses:

-   Testing against multiple Python versions
-   Running linting and formatting checks
-   Running integration tests
-   Testing optional dependencies
-   Reproducing CI pipelines locally

Example `noxfile.py`:

``` python
import nox


@nox.session(python=["3.10", "3.11", "3.12"])
def tests(session):
    session.install(".[test]")
    session.run("pytest")
```

Run:

``` bash
nox
```

------------------------------------------------------------------------

## Separate Test Sessions

Keep different types of tests separate.

Example:

``` python
@nox.session
def unit(session):
    session.install(".[test]")
    session.run("pytest", "tests/unit")


@nox.session
def integration(session):
    session.install(".[test]")
    session.run("pytest", "tests/integration")
```

Run:

``` bash
nox -s unit
nox -s integration
```

------------------------------------------------------------------------

## Running External Services

For integration tests, use nox to manage setup.

Example:

``` python
@nox.session
def database_tests(session):
    session.install(".[test]")

    session.run(
        "pytest",
        "tests/database"
    )
```

Keep environment setup reproducible.

Avoid tests that only work because a developer machine happens to be
configured correctly.

------------------------------------------------------------------------

## Nox Best Practices

Good:

-   Keep sessions small and focused
-   Match CI environments locally
-   Pin important dependencies
-   Use sessions for repeatable workflows
-   Keep unit tests fast and separate from integration tests

Avoid:

-   Putting all test logic inside `noxfile.py`
-   Replacing pytest with nox
-   Running slow integration tests for every small change

Nox orchestrates tests. Pytest defines tests.

------------------------------------------------------------------------

# Test Files

Recommended structure:

    project/
        src/
            users.py

        tests/
            test_users.py

Naming:

    test_<module>.py
    test_<behavior>()

------------------------------------------------------------------------

# Running Tests

Focused:

``` bash
uv run pytest tests/test_users.py
```

Single test:

``` bash
uv run pytest tests/test_users.py::test_create_user
```

Verbose:

``` bash
uv run pytest -v
```

Stop on first failure:

``` bash
uv run pytest -x
```

------------------------------------------------------------------------

# Coverage

Use coverage to find missing tests:

``` bash
uv run pytest --cov=src
```

Do not chase 100% coverage blindly.

Prefer: - Important behaviour covered - Edge cases covered - Failure
modes covered

------------------------------------------------------------------------

# Common Pytest Mistakes

  Mistake                   Better Approach
  ------------------------- ----------------------------
  Testing private methods   Test public behaviour
  Large fixtures            Smaller focused fixtures
  Shared state              Fresh fixtures
  Too many mocks            Test real code
  Duplicate cases           Parametrize
  Weak assertions           Assert meaningful outcomes

------------------------------------------------------------------------

# Final Checklist

-   [ ] Test name explains behaviour
-   [ ] Test follows Arrange-Act-Assert
-   [ ] Test verifies behaviour, not implementation
-   [ ] Fixtures used correctly
-   [ ] Tests are isolated
-   [ ] Parametrize repeated cases
-   [ ] Mocks only used at boundaries
-   [ ] Nox used for complex/repeatable workflows
-   [ ] Assertions verify meaningful results
-   [ ] pytest passes successfully

A good pytest suite should be:

-   Fast
-   Clear
-   Deterministic
-   Maintainable
-   Trustworthy


# Pytest installation
``` bash
uv install --dev pytest
```
