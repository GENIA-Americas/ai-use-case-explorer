import os

os.environ["DATABASE_URL"] = "sqlite:///./test_use_cases.db"

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

SAMPLE = {
    "title": "Invoice data extraction",
    "industry": "Finance",
    "category": "automation",
    "description": "Extract line items from invoices using document AI.",
    "complexity": "medium",
    "tags": ["ocr", "finance", "automation"],
}


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_create_and_get_use_case():
    created = client.post("/use-cases", json=SAMPLE).json()
    assert created["title"] == SAMPLE["title"]

    resp = client.get(f"/use-cases/{created['id']}")
    assert resp.status_code == 200


def test_filter_by_industry():
    client.post("/use-cases", json=SAMPLE)
    resp = client.get("/use-cases", params={"industry": "Finance"})
    assert resp.status_code == 200
    assert all(item["industry"] == "Finance" for item in resp.json())


def test_delete_use_case():
    created = client.post("/use-cases", json=SAMPLE).json()
    del_resp = client.delete(f"/use-cases/{created['id']}")
    assert del_resp.status_code == 204
    assert client.get(f"/use-cases/{created['id']}").status_code == 404


def test_missing_use_case_404():
    assert client.get("/use-cases/999999").status_code == 404
