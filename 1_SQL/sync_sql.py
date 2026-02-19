import requests
import os
import re
import json

USERNAME = os.environ.get("LEETCODE_USERNAME")
SESSION = os.environ.get("LEETCODE_SESSION")

headers = {
    "cookie": f"LEETCODE_SESSION={SESSION}",
    "content-type": "application/json",
    "referer": "https://leetcode.com",
    "origin": "https://leetcode.com",
    "user-agent": "Mozilla/5.0"
}

url = "https://leetcode.com/graphql"

query = """
query recentAcSubmissions($username: String!) {
  recentAcSubmissionList(username: $username) {
    id
    title
    titleSlug
  }
}
"""

resp = requests.post(
    url,
    headers=headers,
    json={"query": query, "variables": {"username": USERNAME}},
)

data = resp.json()

print("DEBUG submissions:", data)

subs = data.get("data", {}).get("recentAcSubmissionList", [])

os.makedirs("1_SQL", exist_ok=True)

for item in subs:
    sub_id = item["id"]
    title = item["title"]
    slug = item["titleSlug"]

    sub_query = """
    query submissionDetails($submissionId: Int!) {
      submissionDetails(submissionId: $submissionId) {
        code
        lang {
          name
        }
      }
    }
    """

    sub_resp = requests.post(
        url,
        headers=headers,
        json={"query": sub_query, "variables": {"submissionId": int(sub_id)}},
    )

    sub_json = sub_resp.json()

    details = sub_json.get("data", {}).get("submissionDetails")

    if not details:
        continue

    code = details.get("code", "")
    lang = details.get("lang", {}).get("name", "")

    if "SQL" not in lang:
        continue

    filename = re.sub(r"[^a-zA-Z0-9]", "_", title) + ".sql"

    with open(f"1_SQL/{filename}", "w") as f:
        f.write(f"-- {title}\n")
        f.write(f"-- https://leetcode.com/problems/{slug}/\n\n")
        f.write(code)

print("DONE")
