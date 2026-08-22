import re


def extract_section(content, heading, read_to_eof=False):
    """
    Extract the content within a specific '## heading' section of a markdown document.

    Args:
        content: The full markdown text.
        heading: The exact heading line to match, e.g. "## Inputs" or "## Process".
        read_to_eof: If True, extracts everything from the heading to the end of the file.
                     If False, stops at the next '## ' heading.

    Returns:
        The trimmed content starting from the heading.
        Returns an empty string if the heading is not found.
    """
    if read_to_eof:
        pattern = rf"^{re.escape(heading)}\s*\n(.*)\Z"
    else:
        pattern = rf"^{re.escape(heading)}\s*\n(.*?)(?=^## |\Z)"
        
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    if not match:
        return ""
    
    body = match.group(1).strip()
    return f"{heading}\n\n{body}" if body else heading
