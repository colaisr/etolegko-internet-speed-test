from starlette.testclient import TestClient

from legko.main import app


def test_docs_index_lists_sections():
    with TestClient(app) as client:
        response = client.get("/docs")
    assert response.status_code == 200
    assert "Документация" in response.text
    assert "00-product-overview" in response.text or "Обзор" in response.text


def test_docs_page_renders_overview():
    with TestClient(app) as client:
        response = client.get("/docs/00-product-overview")
    assert response.status_code == 200
    assert "Legko" in response.text


def test_docs_unknown_slug_404():
    with TestClient(app) as client:
        response = client.get("/docs/not-a-real-page")
    assert response.status_code == 404