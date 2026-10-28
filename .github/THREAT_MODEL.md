# Threat model

This model says what mdformat-hugo trusts, where untrusted input enters, and which guarantees hold at each boundary, so
a report can be classified as a vulnerability or a bug. [SECURITY.md](SECURITY.md) covers reporting; if the two
disagree, SECURITY.md wins and we fix this file.

## How mdformat-hugo works

[mdformat](https://github.com/hukkin/mdformat) finds, reads and writes the files and hands each one to this plugin,
which parses it with mdformat's markdown-it-py parser plus this plugin's shortcode rules and renders it back. It runs no
code from the file and makes no network requests. It typically runs as a pre-commit hook, often on pre-commit.ci or in
CI against content from pull requests.

The plugin never expands a shortcode: Hugo does that later, at site build time.

```mermaid
flowchart LR
    user["User, options<br/>(trusted)"] --> fmt["mdformat-hugo"]
    file[("Markdown file<br/>(untrusted content)")] -->|read| fmt
    fmt -->|"formatted text to the same path,<br/>stdout, or a diff"| file
    classDef trusted fill:#cfe4ff,stroke:#1f6feb,color:#0b1f3a;
    classDef boundary fill:#ffe3a3,stroke:#d29200,color:#3a2c00;
    class user,fmt trusted;
    class file boundary;
```

## Compared with similar tools

We drew the boundary where comparable projects in other ecosystems draw theirs. The shared rule, stated by the
[Node.js threat model](https://github.com/nodejs/node/blob/main/SECURITY.md#the-nodejs-threat-model), is that a report
which first needs a trusted element compromised is out of scope; the first triage question, as
[DOMPurify](https://github.com/cure53/DOMPurify/blob/main/SECURITY.md#what-we-consider-a-vulnerability) puts it, is what
the attacker controls.

| Project                                                          | Language   | Where it draws the line                                                                                                                |
| ---------------------------------------------------------------- | ---------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| [Hugo](https://gohugo.io/about/security/)                        | Go         | Templates and configuration are trusted, content files are not, and a build failure from malformed content is not a denial of service. |
| [Prettier](https://github.com/prettier/prettier/security/policy) | JavaScript | Formats untrusted source; reports go through Tidelift, and the policy defines no further scope.                                        |

## Trusted

An attacker who controls any of these already has what mdformat-hugo could give them:

- The user, the command-line options and the list of files to format.
- The Python runtime and the environment the hook runs in.
- mdformat and the other installed mdformat plugins.

## Untrusted inputs

| Input                          | Comes from                         | What mdformat-hugo guarantees                                                        |
| ------------------------------ | ---------------------------------- | ------------------------------------------------------------------------------------ |
| Contents of each Markdown file | Anyone who can open a pull request | Treated as data: parsed and printed, never evaluated or used to choose another path. |

## Threats and controls

| STRIDE                 | Threat                                                      | Control                                                                                              |
| ---------------------- | ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Tampering              | A crafted file makes the formatter write somewhere else.    | The output path is the input path; content never selects a path. mdformat owns the path handling.    |
| Information disclosure | Formatting pulls in another file's content.                 | Mdformat's markdown-it-py parser plus this plugin's shortcode rules resolves no external references. |
| Denial of service      | A short input triggers exponential parsing or a hang in CI. | Treated as a vulnerability when the input is small; report it.                                       |

## Release chain

Releases run on the shared [tox-dev/github-workflows](https://github.com/tox-dev/github-workflows) pipeline. A release
App, not a person, pushes the release commit and tag; the build installs its tools from a hash-checked `pylock.toml`
resolved with a seven-day upload cooldown by default; PyPI receives the files through
[trusted publishing](https://docs.pypi.org/trusted-publishers/) with attestations, and the GitHub Release is immutable.
Every workflow pins third-party actions to a commit SHA.

## Vulnerability or bug

| Report                                                              | Verdict             | Why                                                  |
| ------------------------------------------------------------------- | ------------------- | ---------------------------------------------------- |
| A crafted shortcode makes the plugin execute or read a file         | Vulnerability       | Content must stay data.                              |
| A long run of `{{` makes formatting take minutes                    | Vulnerability       | Small-input hang in CI.                              |
| Formatting reorders shortcode arguments so Hugo renders differently | Bug                 | Changes meaning; fix it in the open.                 |
| Formatted content contains a `<script>` that Hugo later renders     | Not a vulnerability | The plugin formats content; it does not sanitize it. |

## Severity

- **High:** formatting an untrusted Markdown file executes code, reads or writes another file, or makes a network
  request.
- **Medium:** a small input hangs the formatter or exhausts memory.
- **Low:** an uncaught exception, panic or crash on malformed input instead of a clean error.

## Accepted risks

- Formatting is not a safety review: valid but malicious content is reformatted, not removed.

## Keeping this current

Revisit this model when mdformat-hugo gains a new input source, network access, a new way to run code, or a new place it
writes to, and whenever an advisory is published.
