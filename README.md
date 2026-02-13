# mdformat-hugo

[![PyPI](https://img.shields.io/pypi/v/mdformat-hugo?style=flat-square)](https://pypi.org/project/mdformat-hugo/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/mdformat-hugo.svg)](https://pypi.org/project/mdformat-hugo/)
[![check](https://github.com/gaborbernat/mdformat-hugo/actions/workflows/check.yaml/badge.svg)](https://github.com/gaborbernat/mdformat-hugo/actions/workflows/check.yaml)

Mdformat plugin for Hugo-flavored Markdown. Formats Hugo content files while preserving shortcodes and markdown
attributes.

## Features

This plugin adds support for Hugo-specific markdown syntax:

### Shortcode Formatting

Hugo shortcodes are formatted with normalized whitespace.

**Input:**

```markdown
{{<  ref   "documentation.md"  >}}
{{%   note   %}}
```

**Output:**

```markdown
{{< ref "documentation.md" >}}
{{% note %}}
```

Both `{{< >}}` (no markdown processing) and `{{% %}}` (markdown processed) shortcode styles are supported.

### Markdown Attributes

Hugo extends standard Markdown with [markdown attributes](https://gohugo.io/content-management/markdown-attributes/) --
a syntax for attaching HTML attributes (IDs, classes, and key-value pairs) to rendered elements. Attributes are written
in curly braces after the element they modify, e.g., `{#my-id .my-class key=value}`.

This plugin normalizes attribute order and formatting:

1. **IDs** (`#id`) come first
1. **Classes** (`.class`) follow, sorted alphabetically
1. **Key-value pairs** (`key=value`) come last, sorted alphabetically by key
1. Values containing spaces or `=` are quoted: `key="hello world"`; otherwise unquoted: `key=value`

**Headings:**

```markdown
## Introduction {.zebra .apple #intro}
```

Formats to:

```markdown
## Introduction {#intro .apple .zebra}
```

**Images:**

```markdown
![Logo](logo.png){width=300 .img-fluid height=200}
```

Formats to:

```markdown
![Logo](logo.png){.img-fluid height=200 width=300}
```

**Code blocks:**

````
```python {linenos=table .highlight #code}
def hello():
    print("world")
```
````

Formats to:

````
```python {#code .highlight linenos=table}
def hello():
    print("world")
```
````

### Additional Features

This plugin bundles support for Hugo markdown features and code block formatting via dependencies:

**Markdown syntax:**

- [mdformat-gfm](https://github.com/hukkin/mdformat-gfm) - GFM tables, strikethrough, task lists, autolinks
- [mdformat-front-matters](https://github.com/kyleking/mdformat-front-matters) - TOML/YAML/JSON frontmatter
- [mdformat-gfm-alerts](https://github.com/KyleKing/mdformat-gfm-alerts) - Blockquote alerts (`[!NOTE]`, `[!WARNING]`)
- [mdformat-footnote](https://github.com/executablebooks/mdformat-footnote) - Pandoc-style footnotes
- [mdformat-deflist](https://github.com/executablebooks/mdformat-deflist) - Definition lists

**Code block formatting:**

- [mdformat-ruff](https://github.com/Freed-Wu/mdformat-ruff) - Format Python code blocks with ruff
- [mdformat-shfmt](https://github.com/hukkin/mdformat-shfmt) - Format shell code blocks with shfmt
- [mdformat-config](https://github.com/hukkin/mdformat-config) - Format JSON, YAML, TOML code blocks
- [mdformat-web](https://github.com/hukkin/mdformat-web) - Format HTML, CSS, JavaScript code blocks
- [mdformat-pyproject](https://github.com/csala/mdformat-pyproject) - Format pyproject.toml in code blocks

## Usage

```bash
mdformat content/
```
