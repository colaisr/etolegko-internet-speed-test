from legko.web.doc_renderer import product_docs_link_fixup, render_product_doc_markdown


def test_link_fixup_to_app_routes():
    md = "See [editor](02-stream-offer-editor.md) for details."
    fixed = product_docs_link_fixup(md)
    html = render_product_doc_markdown(fixed)
    assert 'href="/docs/02-stream-offer-editor"' in html