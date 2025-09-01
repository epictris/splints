# Splints (Simple Pattern Lints)
Language-Agnostic LSP implementation providing IDE linting with customisable formatting/messages based on user-defined regex patterns

# Installation
```sh
pip install splints
```

[PyPI Package](https://pypi.org/project/splints)

# Defining Rules
Add lint rules to a file named `splints.yaml` at the root of your repo. The location can be overridden by setting the environment variable `SPLINTS_FILE`


### Required properties
- pattern (string): The regex expression used to find text matching this lint rule
- message (string): A description of the lint rule

### Optional properties
- code (string): An optional identifier for the lint rule
- include_globs (list of strings): The lint rule will be active in files matching these globs. Defaults to ["*"]
- exclude_globs: (list of strings): The lint rule will be deactivated in files matching these globs - overrides `include_globs`. Defaults to []
- severity ("error", "warning", "info", "hint"): Changes how your LSP client formats the popup window
- tags ("deprecated", "unnecessary"): Changes how your LSP client formats the popup message text
- replacement_options (list of PatternReplacement objects - see below): The replacement options provided when your IDE requests a code action.

#### PatternReplacement properties
- description (string): Describe what the replacement will do. If no description is provided the description will be set to the replacement outcome.
- pattern (string): Matches text to replace from the characters matched by its parent lint rule pattern. Defaults to "(\n|.)*" (replaces all characters)
- replacement (string): A string or regex expression that describes the text replacement.
- imports (list of strings): A list of lines to add to the top of the file to import dependencies of the replacement.

### Example Rule Definitions
#### Warn against type ignores
```yaml
- pattern: '# type: ignore'
  message: 'Type ignores are only allowed in exceptional circumstances'
```

#### Disallow use of Any in Python files
```yaml
- pattern: ': Any'
  message: 'Any should rarely be used as a type decorator. Use a more descriptive type'
  include_globs: ['*.py']
```

#### Disallow external use of private properties/methods
```yaml
- pattern: '(?<!self)\._\w+'
  message: 'Do not reference private properties/methods directly'
  include_globs: ['*.py']
  severity: error
```

#### Disallow raw print statements
```yaml
- pattern: '(?<=\s)print\('
  message: 'Remove raw print statements from production code. Use a logger class instead'
  include_globs: ['*.py']
```

#### Prefer Javascript Spread Syntax
```yaml
- pattern: '\w+\.concat\([\s\r\n]*\w+[\s\r\n]*\)'
  message: "concat should not be used. prefer spread notation ([...oldArr, ...newValues])"
  include_globs: ["*.js", "*.ts", "*.jsx", "*.tsx"]
  replacement_options:
  - description: Convert to spread notation
    pattern: "(\\w+|\\[.*])\\.concat\\([\\s\\r\\n]*(\\w+|\\[.*])[\\s\\r\\n]*\\)"
    replacement: "[...\\1, ...\\2]"
```

#### Ensure zip() uses strict=True
```yaml
- pattern: 'zip\((?!.*strict\s*=\s*True)[^)]*\)'
  message: 'zip must be used with strict=True'
  replacement_options:
  - description: Use strict=True
    pattern: 'zip\((.*)\)'
    replacement: 'zip(\1, strict=True)'
```

#### Prefer StrEnum/IntEnum over Enum
```yaml
- pattern: 'class (\w+)\(Enum'
  message: 'Prefer StrEnum or IntEnum over Enum'
  replacement_options:
  - description: 'Use StrEnum'
    pattern: 'class (\w+)\(Enum'
    replacement: 'class \1(StrEnum'
    imports: [ from enum import StrEnum ]
  - description: 'Use IntEnum'
    pattern: 'class (\w+)\(Enum'
    replacement: 'class \1(IntEnum'
    imports: [ from enum import IntEnum ]
```
