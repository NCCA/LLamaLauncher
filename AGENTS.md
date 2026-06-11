# Global Agent Rules 
## Git Workflow
When making code changes ALWAYS follow this process:

1. Ensure current branch is committed if not do not continue until the user has committed and pushed the changes.

2. Create a new worktree before editing:
   git worktree add .worktrees/<short-task-name> -b agent/<short-task-name>

3. Never commit directly to main or master.

4. Use conventional commit messages

5. After finishing changes:
   - run tests
   - run linters
   - ensure project builds


## Session Handling

After each agent run or session :

1. Export the session for traceability:
   export session text as markdown.

2. Save a summary in:
   docs/agent-sessions/<date>-session.md

3. Include:
   - goal
   - files changed
   - commands run
   - all chat context.

## Mandatory Rules

These rules must always be followed:
- NEVER make changes unless the current branch is committed.
- ALWAYS create a git worktree before editing code.
- NEVER modify protected branches.
- ALWAYS run tests before committing.
- ALWAYS export the session on each completed agent run

## Python Rules

### Essential Commands
```bash
# Run all tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src --cov-report=term-missing

# Run single test file
uv run pytest tests/test_vec3.py

# Run single test method
uv run pytest tests/test_vec3.py::TestVec3::test_addition

# Run tests matching pattern
uv run pytest -k "test_addition"

# Verbose test output
uv run pytest -v


# Lint and fix imports
uv run ruff check --select I --fix 

# Format code
uv run ruff format 

# Run all linting checks
uv run ruff check 

```

### Package Management
- **Primary tool**: UV (modern Python package manager)
- **Lock file**: uv.lock for reproducible builds
- **Build system**: uv_build backend
- **Python version**: Requires Python 3.13+

## Code Style Guidelines

### General Principles
- **PEP 8 compliance**: Follow standard Python style guide
- **Type hints**: Required for all function signatures and class attributes
- **Docstrings**: Google-style docstrings for all public classes and methods
- **Import sorting**: Automatic with ruff (`--select I --fix`)
- **Line length**: Default ruff settings (88 characters)

### Import Conventions
```python
# Standard library imports first
import math
from typing import Optional, List

# Third-party imports next
import numpy as np
from PySide6 import QtWidgets
import glfw

# Local imports last
```

### Naming Conventions
- **Classes**: PascalCase (`class Vec3:`, `class ShaderLib:`)
- **Functions/Methods**: snake_case (`def calculate_matrix()`, `def render()`)
- **Variables**: snake_case (`camera_position`, `shader_program`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_LIGHTS`, `DEFAULT_SHADER`)
- **Private members**: Single underscore (`_data`, `_internal_method`)
- **Colour** is the correct spelling for **color** when referring to variable names 

### Type Hints
```python
from typing import Optional, List, Tuple, Union
import numpy as np

def transform_point(point: Vec3, matrix: Mat4) -> Vec3:
    """Transform a 3D point using a 4x4 matrix."""
    return Vec3()

class Camera:
    def __init__(self, position: Vec3, target: Vec3) -> None:
        self.position: Vec3 = position
        self.target: Vec3 = target
```

### Class Structure
```python
class ExampleClass:
    """Example class following PyNGL conventions.
    
    Attributes:
        _data: Internal data storage using __slots__ optimization
        value: Public attribute with type hint
    """
    
    __slots__ = ["_data", "value"]
    
    def __init__(self, initial_value: float = 0.0) -> None:
        """Initialize the example class.
        
        Args:
            initial_value: Starting value for the instance
        """
        self._data = np.array([initial_value], dtype=np.float32)
        self.value = initial_value
    
    def method(self) -> float:
        """Example method with return type hint."""
        return float(self._data[0])
```

### Error Handling
```python
def load_shader(vertex_path: str, fragment_path: str) -> int:
    """Load and compile shader files.
    
    Args:
        vertex_path: Path to vertex shader file
        fragment_path: Path to fragment shader file
        
    Returns:
        OpenGL shader program handle
        
    Raises:
        FileNotFoundError: If shader files don't exist
        RuntimeError: If shader compilation fails
    """
    if not os.path.exists(vertex_path):
        raise FileNotFoundError(f"Vertex shader not found: {vertex_path}")
    
    # Shader loading implementation...
    if not compiled_successfully:
        raise RuntimeError("Shader compilation failed")
```


### Testing Guidelines
- **Framework**: pytest with fixtures for OpenGL context
- **Test naming**: `test_` prefix for test functions and classes
- **Coverage**: Maintain high test coverage (excluding GUI widgets in CI)
- **Test data**: Use files in `tests/files/` for models, textures, shaders
- **OpenGL tests**: Use custom fixtures in `conftest.py` for context setup
- **running tests** : always run the whole test suite on changes
### Performance Optimizations
- Use `__slots__` in data-heavy classes (vectors, matrices)
- Prefer numpy arrays over Python lists for numerical data
- Use appropriate data types (np.float32 for graphics coordinates)
- Minimize Python-OpenGL API calls in tight loops

### Documentation
- **Docstring style**: Google format with Args, Returns, Raises sections
- **API docs**: Generated automatically via mkdocstrings
- **Examples**: Include usage examples in docstrings
- **Type hints**: Essential for documentation generation

### Script Execution
Always use uv shebang for executable scripts:
```python
#!/usr/bin/env -S uv run --script
```


## Development Context

You are an expert in Python programming and related Python technologies such as uv.
You understand modern Python development practices, architectural patterns, and the importance of providing complete context in code generation.

