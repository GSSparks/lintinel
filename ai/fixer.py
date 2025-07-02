# ai/fixer.py

from ai.client import call_openai


def suggest_fix(
    file_path: str,
    code: str,
    rule_name: str,
    issue: str,
    tone: str = "mentor"
    ) -> str:

    prompt = f"""
You are an expert DevOps engineer and code reviewer.

A linting rule called "{rule_name}" found this issue:
{issue}

Here is the relevant code snippet from `{file_path}`:


```
{code}
```


Please suggest an improved version of the snippet.

Use a {tone} tone and explain your reasoning before showing the fix.

RULES:

1. Do not offer apologies for not being able to help.
2. Do not offer further help. This is the only interaction you will
have with this particular snippet of code.
3. If there is nothing substantial in the code, a # for example, only
suggest a fix based on the given issue.
4. Respond in markdown format with a heading for "Suggested Fix" and
one for "Explanation". Please make the heading a heading 3 (eg., ###).
5. Do not be chatty. Only give the relevant information to explain and
fix the issue.

""".strip()

    return call_openai(prompt, temperature=0.3)
