# Splints (Simple Pattern Lints)
Language-Agnostic LSP implementation providing IDE linting with customisable formatting/messages based on user-defined regex patterns

# Installation
```sh
pip install splints
```

[PyPI Package](https://pypi.org/project/splints)

# Defining Rules
Add lint rules to a file named `splints.yaml` at the root of your repo. The location can be overridden by setting the environment variable `SPLINTS_RULES`


### Required properties
- pattern (string): The regex expression used to find text matching this lint rule
- message (string): A description of the lint rule

### Optional properties
- code (string): An optional identifier for the lint rule
- include_globs (list of strings): The lint rule will be active in files matching these globs. Defaults to `["*"]`
- exclude_globs: (list of strings): The lint rule will be deactivated in files matching these globs - overrides `include_globs`. Defaults to `[]`
- severity ("error", "warning", "info", "hint"): Changes how your LSP client formats the popup window
- tags ("deprecated", "unnecessary"): Changes how your LSP client formats the popup message text
- replacement_options (list of PatternReplacement objects - see below): The replacement options provided when your IDE requests a code action.

#### PatternReplacement properties
- description (string): Describe what the replacement will do. If no description is provided the description will be set to the replacement outcome.
- pattern (string): Matches text to replace from the characters matched by its parent lint rule pattern. Defaults to `"(\n|.)*"` (replaces all characters)
- replacement (string): A string or regex expression that describes the text replacement.
- imports (list of strings): A list of lines to add to the top of the file to import dependencies of the replacement.

### Example Rule Definitions
#### Warn against type ignores
```yaml
- pattern: '# type: ignore'
  message: 'Type ignores are only allowed in exceptional circumstances'
```
<img width="651" height="82" alt="Screenshot 2025-09-02 at 11 07 06" src="https://github.com/user-attachments/assets/0f6d7c86-5b49-4393-b919-606f25a39604" />

#### Disallow use of Any in Python files
```yaml
- pattern: ': Any'
  message: 'Any should rarely be used as a type decorator. Use a more descriptive type'
  include_globs: ['*.py']
```
<img width="587" height="73" alt="Screenshot 2025-09-02 at 11 09 28" src="https://github.com/user-attachments/assets/1fdbd0c8-35bb-4d25-af9c-8f9d0700af69" />

#### Disallow external use of private properties/methods
```yaml
- pattern: '(?<!self)\._[^_]\w+'
  message: 'Do not reference private properties/methods directly'
  include_globs: ['*.py']
  severity: error
```
<img width="833" height="123" alt="Screenshot 2025-09-02 at 11 10 35" src="https://github.com/user-attachments/assets/fb0d6b33-dfac-4bb6-b8ca-daa9209fd4d5" />

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
<img width="662" height="162" alt="Screenshot 2025-09-02 at 11 15 35" src="https://github.com/user-attachments/assets/9160f3b2-ac66-47c5-9ef2-b1d999016fc8" />

##### Text Replacement

<img width="447" height="35" alt="Screenshot 2025-09-02 at 11 16 06" src="https://github.com/user-attachments/assets/3a9c03fa-ecfb-424b-b1ad-d4dbb4d308db" />

#### Ensure zip() uses strict=True
```yaml
- pattern: 'zip\((?!.*strict\s*=\s*True)[^)]*\)'
  message: 'zip must be used with strict=True'
  replacement_options:
  - description: Use strict=True
    pattern: 'zip\((.*)\)'
    replacement: 'zip(\1, strict=True)'
```
<img width="662" height="168" alt="Screenshot 2025-09-02 at 11 18 27" src="https://github.com/user-attachments/assets/68e9cd60-fef5-4b3a-ae43-e6368643e561" />

##### Text Replacement

<img width="194" height="33" alt="Screenshot 2025-09-02 at 11 18 38" src="https://github.com/user-attachments/assets/d690c6c1-e45f-42a9-982d-b6129a94b8e4" />

#### Replace Enum with StrEnum/IntEnum
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
<img width="324" height="73" alt="Screenshot 2025-09-02 at 11 21 25" src="https://github.com/user-attachments/assets/f937b7fa-2ca2-4017-98a6-80cb6bc9b4ca" />
<img width="672" height="162" alt="Screenshot 2025-09-02 at 11 21 35" src="https://github.com/user-attachments/assets/988a569f-e08a-47cd-9e9b-bc2cbef727c3" />

##### Text Replacement

<img width="261" height="97" alt="Screenshot 2025-09-02 at 11 21 54" src="https://github.com/user-attachments/assets/2cf8f202-0a6a-45a0-b8f5-ecea699f339e" />
