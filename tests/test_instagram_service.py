import os
import pytest
from unittest.mock import patch, MagicMock
from services.instagram_service import InstagramService
from services.approval_manager import ApprovalManager
from memory.business_memory import BusinessMemory

def test_instagram_service_init_and_redaction():
    service = InstagramService()
    assert service.account_id in ("17841437441178441", os.getenv("INSTAGRAM_ACCOUNT_ID", "17841437441178441"))
    
    # Secret redaction check
    service.access_token = "secret_meta_access_token_9999"
    raw_error = "HTTP 400: Bad Request with secret_meta_access_token_9999 in URL"
    redacted = service._redact_secrets(raw_error)
    assert "secret_meta_access_token_9999" not in redacted
    assert "[REDACTED]" in redacted

def test_instagram_account_status_unconfigured():
    service = InstagramService()
    service.access_token = ""
    res = service.get_account_status()
    assert res["status"] == "NOT_CONNECTED"
    assert res["oauth_connected"] is False
    assert res["account_name"] == "autobizai01"
    assert res["account_id"] == "17841437441178441"

def test_instagram_test_connection_pass():
    service = InstagramService()
    service.access_token = "valid_token"
    
    mock_resp = MagicMock()
    mock_resp.status = 200
    mock_resp.read.return_value = b'{"id": "17841437441178441", "username": "autobizai01", "name": "AutoBiz AI", "account_type": "BUSINESS"}'
    mock_resp.__enter__.return_value = mock_resp
    
    with patch("urllib.request.urlopen", return_value=mock_resp):
        res = service.test_connection()
        assert res["status"] == "PASS"
        assert res["account_name"] == "autobizai01"
        assert res["account_id"] == "17841437441178441"
        assert "PASS" in res["message"]

def test_instagram_test_connection_fail():
    service = InstagramService()
    service.access_token = "invalid_token"
    
    with patch("urllib.request.urlopen", side_effect=Exception("Invalid OAuth access token")):
        res = service.test_connection()
        assert res["status"] == "FAIL"
        assert "FAIL" in res["message"]
        assert "Invalid OAuth access token" in res["reason"]

def test_instagram_two_step_publishing_flow():
    service = InstagramService()
    service.access_token = "valid_token"
    
    # Step 1: create_media
    mock_container_resp = MagicMock()
    mock_container_resp.status = 200
    mock_container_resp.read.return_value = b'{"id": "1790001122334455"}'
    mock_container_resp.__enter__.return_value = mock_container_resp
    
    with patch("urllib.request.urlopen", return_value=mock_container_resp):
        c_res = service.create_media("https://autobiz.local/test.jpg", "Test Instagram Caption")
        assert c_res["status"] == "SUCCESS"
        assert c_res["container_id"] == "1790001122334455"

    # Step 2: publish_media
    mock_publish_resp = MagicMock()
    mock_publish_resp.status = 200
    mock_publish_resp.read.return_value = b'{"id": "180998877665544"}'
    mock_publish_resp.__enter__.return_value = mock_publish_resp
    
    with patch("urllib.request.urlopen", return_value=mock_publish_resp):
        p_res = service.publish_media("1790001122334455")
        assert p_res["status"] == "SUCCESS"
        assert p_res["published_post_id"] == "180998877665544"
        assert "https://instagram.com/p/180998877665544" in p_res["url"]

def test_approval_gating_for_social_publishing():
    memory = BusinessMemory()
    app_mgr = ApprovalManager()
    cycle_id = memory.get_business_state().cycle_id

    # Create approval
    app_id = app_mgr.request_approval(
        action="PUBLISH_INSTAGRAM_POST",
        description="Test Instagram post approval gating",
        cycle_id=cycle_id
    )
    assert isinstance(app_id, int)

    # Verify pending
    pending = app_mgr.get_pending_approvals(cycle_id=cycle_id)
    assert any(a.approval_id == app_id for a in pending)

    # Approve
    success = app_mgr.approve(app_id)
    assert success is True

    # Verify approved state
    approved_app = memory.get_approval(app_id)
    assert approved_app.status == "APPROVED"

def test_instagram_get_media_status():
    service = InstagramService()
    service.access_token = "valid_token"

    mock_resp = MagicMock()
    mock_resp.status = 200
    mock_resp.read.return_value = b'{"status_code": "FINISHED", "status": "FINISHED", "id": "1790001122334455"}'
    mock_resp.__enter__.return_value = mock_resp

    with patch("urllib.request.urlopen", return_value=mock_resp):
        res = service.get_media_status("1790001122334455")
        assert res["status"] == "SUCCESS"
        assert res["data"]["status_code"] == "FINISHED"
        assert res["data"]["id"] == "1790001122334455"

