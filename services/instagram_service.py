import os
import json
import urllib.request
import urllib.parse
from datetime import datetime

DEFAULT_INSTAGRAM_ACCOUNT_ID = "17841437441178441"

class InstagramService:
    """
    Official Meta Graph API Service for Instagram Professional Accounts.
    Account: autobizai01 (ID: 17841437441178441).
    Reads credentials strictly from environment variables.
    Redacts access tokens from all logs and error messages.
    """
    def __init__(self):
        self.access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN", "").strip()
        self.account_id = (os.getenv("INSTAGRAM_ACCOUNT_ID") or os.getenv("INSTAGRAM_USER_ID") or DEFAULT_INSTAGRAM_ACCOUNT_ID).strip()

    def _redact_secrets(self, text: str) -> str:
        if not text:
            return ""
        if self.access_token and len(self.access_token) > 4:
            text = text.replace(self.access_token, "[REDACTED]")
        return text

    def get_account_status(self) -> dict:
        if not self.access_token or self.access_token.startswith("your_"):
            return {
                "status": "NOT_CONNECTED",
                "oauth_connected": False,
                "account_name": "autobizai01",
                "account_id": self.account_id or DEFAULT_INSTAGRAM_ACCOUNT_ID,
                "reason": "Missing or placeholder INSTAGRAM_ACCESS_TOKEN in environment (.env)"
            }

        url = f"https://graph.facebook.com/v19.0/{self.account_id}?fields=id,username,name,account_type&access_token={self.access_token}"
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=8) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode('utf-8'))
                    return {
                        "status": "CONNECTED",
                        "oauth_connected": True,
                        "account_name": data.get("username", "autobizai01"),
                        "account_id": data.get("id", self.account_id),
                        "account_type": data.get("account_type", "BUSINESS")
                    }
        except urllib.error.HTTPError as e:
            err_body = ""
            try:
                err_body = e.read().decode('utf-8')
            except Exception:
                pass
            return {
                "status": "NOT_CONNECTED",
                "oauth_connected": False,
                "account_name": "autobizai01",
                "account_id": self.account_id,
                "reason": self._redact_secrets(f"HTTP {e.code}: {e.reason} - {err_body}")
            }
        except Exception as e:
            return {
                "status": "NOT_CONNECTED",
                "oauth_connected": False,
                "account_name": "autobizai01",
                "account_id": self.account_id,
                "reason": self._redact_secrets(f"Connection error: {e}")
            }

        return {
            "status": "NOT_CONNECTED",
            "oauth_connected": False,
            "account_name": "autobizai01",
            "account_id": self.account_id,
            "reason": "Unauthorized"
        }

    def test_connection(self) -> dict:
        status_res = self.get_account_status()
        if status_res["status"] == "CONNECTED":
            return {
                "status": "PASS",
                "account_name": status_res.get("account_name", "autobizai01"),
                "account_id": status_res.get("account_id", self.account_id),
                "account_type": status_res.get("account_type", "BUSINESS"),
                "message": f"Instagram connection PASS — Connected as @{status_res.get('account_name')} (ID: {status_res.get('account_id')})"
            }
        else:
            return {
                "status": "FAIL",
                "account_name": status_res.get("account_name", "autobizai01"),
                "account_id": status_res.get("account_id", self.account_id),
                "reason": self._redact_secrets(status_res.get("reason", "Account validation failed")),
                "message": f"Instagram connection FAIL — {self._redact_secrets(status_res.get('reason'))}"
            }

    def create_media(self, image_url: str, caption: str) -> dict:
        """
        Step 1 of Instagram 2-step publishing flow.
        Creates a Media Container on Instagram.
        """
        if not self.access_token or self.access_token.startswith("your_"):
            return {
                "status": "FAILED",
                "error": "Missing or placeholder INSTAGRAM_ACCESS_TOKEN in environment (.env)"
            }

        params = urllib.parse.urlencode({
            "image_url": image_url,
            "caption": caption,
            "access_token": self.access_token
        }).encode('utf-8')

        url = f"https://graph.facebook.com/v19.0/{self.account_id}/media"
        req = urllib.request.Request(url, data=params, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                container_id = data.get("id")
                if container_id:
                    return {
                        "status": "SUCCESS",
                        "container_id": container_id
                    }
                else:
                    return {
                        "status": "FAILED",
                        "error": "Meta Graph API returned empty container ID"
                    }
        except urllib.error.HTTPError as e:
            err_body = ""
            try:
                err_body = e.read().decode('utf-8')
            except Exception:
                pass
            return {
                "status": "FAILED",
                "error": self._redact_secrets(f"Instagram Container Creation Error (HTTP {e.code}): {err_body}")
            }
        except Exception as e:
            return {
                "status": "FAILED",
                "error": self._redact_secrets(f"Instagram Container Creation Exception: {e}")
            }

    def publish_media(self, container_id: str) -> dict:
        """
        Step 2 of Instagram 2-step publishing flow.
        Publishes the Media Container on Instagram.
        """
        if not self.access_token or self.access_token.startswith("your_"):
            return {
                "status": "FAILED",
                "error": "Missing or placeholder INSTAGRAM_ACCESS_TOKEN in environment (.env)"
            }

        params = urllib.parse.urlencode({
            "creation_id": container_id,
            "access_token": self.access_token
        }).encode('utf-8')

        url = f"https://graph.facebook.com/v19.0/{self.account_id}/media_publish"
        req = urllib.request.Request(url, data=params, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                pub_id = data.get("id")
                if pub_id:
                    return {
                        "status": "SUCCESS",
                        "published_post_id": pub_id,
                        "published_at": datetime.now().isoformat(),
                        "url": f"https://instagram.com/p/{pub_id}"
                    }
                else:
                    return {
                        "status": "FAILED",
                        "error": "Meta Graph API returned empty publication ID"
                    }
        except urllib.error.HTTPError as e:
            err_body = ""
            try:
                err_body = e.read().decode('utf-8')
            except Exception:
                pass
            return {
                "status": "FAILED",
                "error": self._redact_secrets(f"Instagram Media Publish Error (HTTP {e.code}): {err_body}")
            }
        except Exception as e:
            return {
                "status": "FAILED",
                "error": self._redact_secrets(f"Instagram Media Publish Exception: {e}")
            }

    def get_media(self, media_id: str) -> dict:
        if not self.access_token or not media_id:
            return {"status": "FAILED", "error": "Missing access token or media ID"}

        url = f"https://graph.facebook.com/v19.0/{media_id}?fields=id,caption,media_type,media_url,permalink,timestamp&access_token={self.access_token}"
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=8) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                return {
                    "status": "SUCCESS",
                    "media": data
                }
        except Exception as e:
            return {
                "status": "FAILED",
                "error": self._redact_secrets(f"Get Media Error: {e}")
            }

    def get_media_status(self, container_id: str) -> dict:
        if not self.access_token or not container_id:
            return {"status": "FAILED", "error": "Missing access token or container ID"}

        url = f"https://graph.instagram.com/{container_id}?fields=status_code,status&access_token={self.access_token}"
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=8) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                return {
                    "status": "SUCCESS",
                    "data": data
                }
        except urllib.error.HTTPError as e:
            err_body = ""
            try:
                err_body = e.read().decode('utf-8')
            except Exception:
                pass
            return {
                "status": "FAILED",
                "error": self._redact_secrets(f"Get Media Status Error (HTTP {e.code}): {err_body}")
            }
        except Exception as e:
            return {
                "status": "FAILED",
                "error": self._redact_secrets(f"Get Media Status Error: {e}")
            }

