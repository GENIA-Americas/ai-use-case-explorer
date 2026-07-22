import os

os.environ["DATABASE_URL"] = "sqlite:///./test_use_cases.db"
os.environ["ADMIN_API_KEYS"] = "devadminkey1"

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

ADMIN_HEADERS = {"X-Admin-Key": "devadminkey1"}

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


def test_create_requires_admin_key():
    resp = client.post("/use-cases", json=SAMPLE)
    assert resp.status_code == 401


def test_create_rejects_wrong_admin_key():
    resp = client.post("/use-cases", json=SAMPLE, headers={"X-Admin-Key": "not-the-real-key"})
    assert resp.status_code == 401


def test_create_and_get_use_case():
    created = client.post("/use-cases", json=SAMPLE, headers=ADMIN_HEADERS).json()
    assert created["title"] == SAMPLE["title"]

    resp = client.get(f"/use-cases/{created['id']}")
    assert resp.status_code == 200


def test_filter_by_industry():
    client.post("/use-cases", json=SAMPLE, headers=ADMIN_HEADERS)
    resp = client.get("/use-cases", params={"industry": "Finance"})
    assert resp.status_code == 200
    assert all(item["industry"] == "Finance" for item in resp.json())


def test_delete_requires_admin_key():
    created = client.post("/use-cases", json=SAMPLE, headers=ADMIN_HEADERS).json()
    resp = client.delete(f"/use-cases/{created['id']}")
    assert resp.status_code == 401
    assert client.get(f"/use-cases/{created['id']}").status_code == 200


def test_delete_use_case():
    created = client.post("/use-cases", json=SAMPLE, headers=ADMIN_HEADERS).json()
    del_resp = client.delete(f"/use-cases/{created['id']}", headers=ADMIN_HEADERS)
    assert del_resp.status_code == 204
    assert client.get(f"/use-cases/{created['id']}").status_code == 404


def test_missing_use_case_404():
    assert client.get("/use-cases/999999").status_code == 404
