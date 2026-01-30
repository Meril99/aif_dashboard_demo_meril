from fastapi.testclient import TestClient
from immudb.client import ImmudbClient
import os

from main_api import app


# -------------------------
# immudb helper (SAFE)
# -------------------------
from typing import Optional, Dict

def immudb_query(sql: str, params: Optional[Dict] = None):
    host = os.getenv("IMMUDB_HOST", "immudb")
    port = os.getenv("IMMUDB_PORT", "3322")

    client = ImmudbClient(f"{host}:{port}")
    client.login(
        os.getenv("IMMUDB_USER", "immudb"),
        os.getenv("IMMUDB_PASSWORD", "immudb"),
    )
    client.useDatabase(b"auditdb")

    try:
        if params:
            return list(client.sqlQuery(sql, params))
        return list(client.sqlQuery(sql))
    finally:
        client.logout()


# -------------------------
# helper: get last comment
# -------------------------
def get_last_comment(client: TestClient):
    resp = client.get("/comments/")
    assert resp.status_code == 200
    comments = resp.json()
    assert len(comments) >= 1
    return comments[-1]


# -------------------------
# ADD
# -------------------------
def test_add_comment_creates_immudb_audit():
    payload = {
        "Name": "test-user",
        "TimeStamp": "2026-01-26T12:00:00",
        "Comments": "hello immudb",
    }

    with TestClient(app) as client:
        resp = client.post("/comments/", json=payload)
        assert resp.status_code == 200
        comment = get_last_comment(client)

    rows = immudb_query(
        """
        SELECT action, entity, entity_id
        FROM comments_audit_v2
        WHERE entity_id = @entity_id
        ORDER BY tx_id DESC
        """,
        {"entity_id": comment["id"]},
    )

    assert len(rows) >= 1
    action, entity, entity_id = rows[0]

    assert action == "ADD"
    assert entity == "Comments"
    assert entity_id == comment["id"]


# -------------------------
# EDIT
# -------------------------
def test_edit_comment_creates_immudb_audit():
    with TestClient(app) as client:
        create_payload = {
            "Name": "edit-user",
            "TimeStamp": "2026-01-26T12:10:00",
            "Comments": "before edit",
        }

        client.post("/comments/", json=create_payload)
        comment = get_last_comment(client)
        comment_id = comment["id"]

        updated = {
            "Name": "edit-user",
            "TimeStamp": "2026-01-26T12:20:00",
            "Comments": "after edit",
        }

        resp = client.put(f"/comments/{comment_id}/", json=updated)
        assert resp.status_code == 200

    rows = immudb_query(
        """
        SELECT action
        FROM comments_audit_v2
        WHERE entity_id = @entity_id
        ORDER BY tx_id DESC
        """,
        {"entity_id": comment_id},
    )

    assert len(rows) >= 1
    (action,) = rows[0]
    assert action == "EDIT"


# -------------------------
# DELETE
# -------------------------
def test_delete_comment_creates_immudb_audit():
    with TestClient(app) as client:
        payload = {
            "Name": "delete-user",
            "TimeStamp": "2026-01-26T12:30:00",
            "Comments": "to be deleted",
        }

        client.post("/comments/", json=payload)
        comment = get_last_comment(client)
        comment_id = comment["id"]

        delete_resp = client.delete(f"/comments/{comment_id}/")
        assert delete_resp.status_code == 200

    rows = immudb_query(
        """
        SELECT action
        FROM comments_audit_v2
        WHERE entity_id = @entity_id
        ORDER BY tx_id DESC
        """,
        {"entity_id": comment_id},
    )

    assert len(rows) >= 1
    (action,) = rows[0]
    assert action == "DELETE"


# -------------------------
# FETCH ALL AUDIT LOGS
# -------------------------
def test_fetch_all_immudb_audit_logs():
    with TestClient(app) as client:
        for i in range(2):
            payload = {
                "Name": f"user-{i}",
                "TimeStamp": "2026-01-26T12:00:00",
                "Comments": f"log {i}",
            }
            resp = client.post("/comments/", json=payload)
            assert resp.status_code == 200

    rows = immudb_query(
        """
        SELECT
            tx_id,
            action,
            entity,
            entity_id,
            payload,
            created_at
        FROM comments_audit_v2
        ORDER BY tx_id DESC
        """
    )

    assert len(rows) >= 2

    tx_id, action, entity, entity_id, payload, created_at = rows[0]

    assert isinstance(tx_id, int)
    assert action in {"ADD", "EDIT", "DELETE"}
    assert entity == "Comments"
    assert isinstance(entity_id, int)
    assert isinstance(payload, str)
    assert isinstance(created_at, int)

    assert rows[0][0] > rows[1][0]
