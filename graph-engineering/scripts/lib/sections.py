import re


def extract_section(content, heading):
    """
    Extract the content within a specific '## heading' section of a markdown document.

    Args:
        content: The full markdown text.
        heading: The exact heading line to match, e.g. "## Inputs" or "## Process".

    Returns:
        The trimmed content between the heading and the next '## ' heading (or end of file).
        Returns an empty string if the heading is not found.
    """
    pattern = rf"^{re.escape(heading)}\s*\n(.*?)(?=^## |\Z)"
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    if not match:
        return ""
    
    body = match.group(1).strip()
    return f"{heading}\n\n{body}" if body else heading
