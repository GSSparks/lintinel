![Lintinel Logo](./images/lintinel.png)

**Lintinel** is your AI-powered DevOps assistant that audits your codebase and infrastructure for best practices, compliance, and quality — and makes smart suggestions using modern LLMs.

> Think of it as a friendly, customizable watchdog for your CI pipelines and GitHub PRs.

---

## What It Does

***NOTE*** This project is in the beginning phases of development.

- ✔️ Lints code and infrastructure files (Docker, YAML, Terraform, etc.)
- ✖️ Suggests improvements via AI (OpenAI, Ollama, Claude, etc.)
- ✖️ Integrates with GitHub PRs or runs as a CLI
- ✔️ Uses a flexible plugin-based rule engine
- ✔️ Extensible by contributors with Python-based rules

---

## Installation

### Run Locally (CLI)

```bash
git clone https://github.com/yourusername/lintinel.git
cd lintinel
pip install -r requirements.txt
python main.py /path/to/your/repo
```
### Run with Docker

```bash
docker build -t lintinel .
docker run -v $(pwd):/repo lintinel /repo
```

## Example Rules (Initial Set)
| Rule Type	| Description |
|-----------|-------------|
|Dockerfile	| Warn on unpinned image versions (e.g. ubuntu:latest) |
|Terraform	| Missing description field in variables |
|YAML	    | Inconsistent spacing or syntax |
|Git	    | Missing .gitignore, .editorconfig |
|Custom	    | Easily add your own Python rules! |

## AI Integration (Coming Soon)
- Optional LLM-based explainer for PR feedback
- Auto-suggest clean code or infra improvements
- Configurable AI backend (Ollama, OpenAI, etc.)

## Contributing
We’d love your help!
Fork the repo and clone it
Add a new rule to the rules/ folder
Write a test case for it in tests/
Submit a PR

## Roadmap
- Rule plugin engine (stable)
- GitHub App integration
- First round of AI-based feedback
- Web UI (optional)
- CI/CD integration templates

## License
GPLv3

## Credits
Built by Gary Sparks, with inspiration from DevOps pipelines, AI assistants, and all the great open source linting tools that came before us.

