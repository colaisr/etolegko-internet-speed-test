import re

import markdown

_MD = markdown.Markdown(
    extensions=["tables", "fenced_code", "sane_lists"],
    output_format="html5",
)


def product_docs_link_fixup(source: str) -> str:
    """Turn same-folder .md links into /docs/{slug} for in-app navigation."""

    def repl(match: re.Match[str]) -> str:
        target = match.group(1)
        if target.startswith("http") or target.startswith("/"):
            return match.group(0)
        if target.endswith(".md"):
            slug = target.removesuffix(".md").split("/")[-1]
            if slug and not slug.startswith("_"):
                return f"](/docs/{slug})"
        return match.group(0)

    return re.sub(r"\]\(([^)]+)\)", repl, source)


def render_product_doc_markdown(source: str) -> str:
    _MD.reset()
    prepared = product_docs_link_fixup(source)
    return _MD.convert(prepared)


def extract_title(markdown_source: str, *, fallback: str) -> str:
    for line in markdown_source.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped.removeprefix("# ").strip()
    return fallback