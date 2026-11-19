import re
from pathlib import Path

PRODUCT_DOCS_DIR_NAME = "ProductDocs"
_SLUG_RE = re.compile(r"^[0-9][0-9a-z-]*$")


def product_docs_root() -> Path:
    # legko/legko/services/product_docs.py → repo root
    return Path(__file__).resolve().parents[3] / PRODUCT_DOCS_DIR_NAME


def normalize_slug(slug: str) -> str | None:
    candidate = slug.strip().removesuffix(".md")
    if not candidate or not _SLUG_RE.fullmatch(candidate):
        return None
    return candidate


def resolve_doc_path(slug: str) -> Path | None:
    normalized = normalize_slug(slug)
    if normalized is None:
        return None
    root = product_docs_root()
    path = (root / f"{normalized}.md").resolve()
    if not str(path).startswith(str(root.resolve())):
        return None
    if not path.is_file():
        return None
    return path


def read_doc_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def list_doc_pages() -> list[dict]:
    root = product_docs_root()
    if not root.is_dir():
        return []
    pages: list[dict] = []
    for path in sorted(root.glob("[0-9]*.md")):
        slug = path.stem
        from legko.web.doc_renderer import extract_title

        source = read_doc_file(path)
        pages.append(
            {
                "slug": slug,
                "title": extract_title(source, fallback=slug),
                "href": f"/docs/{slug}",
            },
        )
    return pages


def read_index_markdown() -> str | None:
    path = product_docs_root() / "README.md"
    if not path.is_file():
        return None
    return read_doc_file(path)