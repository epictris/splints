# Splints (Simple Pattern Lints)
Language-Agnostic LSP implementation providing IDE linting with customisable formatting/messages based on user-defined regex patterns

# Installation
```sh
pip install splints
```

[PyPI Package](https://pypi.org/project/splints)

# Defining Rules
Add lint rules to a file named `splints.yaml` at the root of your repo. This can be overridden by setting the environment variable `SPLINTS_FILE`


### Example Rule Definitions
#### Warn against type ignores
```yaml
- pattern: '# type: ignore'
  message: 'Type ignores are only allowed in exceptional circumstances'
```

#### Disallow use of Any in python files
```yaml
- pattern: ': Any'
- message: 'Any should rarely be used as a type decorator. Use a more descriptive type'
- include_globs: ['*.py']
```

#### Disallow external use of private properties/methods
```
- pattern: '(?<!self)\._\w+'
  message: 'Do not reference private properties/methods directly. Use public getters and setters instead'
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
