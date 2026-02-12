import bleach

ALLOWED_TAGS = [
    "p","br","strong","em","ul","ol","li","a",
    "h1","h2","h3","h4","blockquote","code","pre"
]

ALLOWED_ATTRS = ["href", "title", "alt"]


def sanitize_html(html: str) -> str:
    return bleach.clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS)
