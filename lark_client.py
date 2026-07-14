import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

LARK_BASE_URL = "https://open.larksuite.com/open-apis"


class LarkClient:
    def __init__(self):
        self.app_id = os.getenv("LARK_APP_ID")
        self.app_secret = os.getenv("LARK_APP_SECRET")
        self._token = None
        self._token_expires = 0

    def _get_tenant_access_token(self):
        if self._token and time.time() < self._token_expires:
            return self._token

        resp = requests.post(
            f"{LARK_BASE_URL}/auth/v3/tenant_access_token/internal",
            json={"app_id": self.app_id, "app_secret": self.app_secret},
        )
        data = resp.json()
        if data.get("code") != 0:
            raise Exception(f"Auth failed: {data.get('msg')}")

        self._token = data["tenant_access_token"]
        self._token_expires = time.time() + data.get("expire", 7200) - 60
        return self._token

    def _headers(self):
        return {
            "Authorization": f"Bearer {self._get_tenant_access_token()}",
            "Content-Type": "application/json; charset=utf-8",
        }

    def get_all_users(self, department_id=None, page_size=50):
        all_users = []
        page_token = None

        while True:
            params = {"page_size": page_size}
            if department_id:
                params["department_id"] = department_id
            if page_token:
                params["page_token"] = page_token

            resp = requests.get(
                f"{LARK_BASE_URL}/contact/v3/users",
                headers=self._headers(),
                params=params,
            )
            data = resp.json()

            if data.get("code") != 0:
                raise Exception(f"Lark API error: {data.get('msg')}")

            items = data.get("data", {}).get("items", [])
            all_users.extend(items)

            if not data.get("data", {}).get("has_more"):
                break
            page_token = data.get("data", {}).get("page_token")

        return all_users

    def get_departments(self, page_size=50):
        all_depts = []
        page_token = None

        while True:
            params = {"page_size": page_size}
            if page_token:
                params["page_token"] = page_token

            resp = requests.get(
                f"{LARK_BASE_URL}/contact/v3/departments",
                headers=self._headers(),
                params=params,
            )
            data = resp.json()

            if data.get("code") != 0:
                raise Exception(f"Lark API error: {data.get('msg')}")

            items = data.get("data", {}).get("items", [])
            all_depts.extend(items)

            if not data.get("data", {}).get("has_more"):
                break
            page_token = data.get("data", {}).get("page_token")

        return all_depts

    def query_attendance(self, user_ids, date_from, date_to, employee_type="employee_id"):
        resp = requests.post(
            f"{LARK_BASE_URL}/attendance/v1/user_tasks/query",
            headers=self._headers(),
            params={"employee_type": employee_type, "ignore_invalid_users": "true"},
            json={
                "user_ids": user_ids,
                "check_date_from": date_from,
                "check_date_to": date_to,
            },
        )
        return resp.json()
