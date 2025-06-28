# output/formatter.py
import json

def format_as_json(results):
    return json.dumps(results, indent=2)

def format_as_markdown(results):
    output = "# Lintinel Report\n\n"
    for result in results:
        output += f"## {result['name']}\n"
        output += f"{result['description']}\n\n"
        if 'issues' in result and result['issues']:
            for issue in result['issues']:
                output += f"- {issue}\n"
        else:
            output += "- ✅ No issues found\n"
        output += "\n"
    return output

