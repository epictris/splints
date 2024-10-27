from setuptools import setup

setup(
    name='deprecated-pattern-linter',
    version='0.0.0',
    description='Deprecated Patterns Linter',
    author='',
    author_email='',
    url='',
    packages=['deprecated_pattern_linter'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'deprecated-pattern-linter = deprecated_pattern_linter.server:run',
        ],
    },
)
