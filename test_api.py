from lark_client import LarkClient
import json

lark = LarkClient()
try:
    users = lark.get_all_users()
    print(f"Found {len(users)} users")
    for u in users[:3]:
        print(json.dumps(u, indent=2, default=str))
except Exception as e:
    print(f"Error: {e}")
