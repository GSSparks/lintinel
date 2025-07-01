# ai/fixer.py

from ai.client import call_openai

def suggest_fix(file_path: str, code: str, rule_name: str, issue: str, tone: str = "mentor") -> str:
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

Do not offer apologies for not being able to help and do not offer further help.
This is the only interaction you will have with this particular snippet of code.

Respond in markdown format with a heading for "Suggested Fix" and one for "Explanation".
Please make the heading a heading 3 (eg., ###).

Do not be too chatty.
""".strip()

    return call_openai(prompt, temperature=0.3)
