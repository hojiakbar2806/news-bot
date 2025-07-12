import re


def trim_html(html: str, max_length: int = 3500):
    paragraphs = re.findall(r"<p.*?>.*?</p>", html, flags=re.DOTALL)
    current = ""
    remainder = ""

    for p in paragraphs:
        if len(current) + len(p) < max_length:
            current += p
        else:
            remainder += p

    return current, remainder
