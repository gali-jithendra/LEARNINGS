import requests
import os
import re

USERNAME = os.environ.get("LEETCODE_USERNAME")
SESSION = os.environ.get("LEETCODE_SESSION")

headers = {
    "cookie": f"LEETCODE_SESSION={SESSION}",
    "content-type": "application/json",
    "referer": "https://leetcode.com"
}

url = "https://leetcode.com/graphql"

# Get recent accepted submissions
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

data = resp.json()["data"]["recentAcSubmissionList"]

os.makedirs("1_SQL", exist_ok=True)

for item in data:
    sub_id = item["id"]
    title = item["title"]
    slug = item["titleSlug"]

    # Fetch submission code
    sub_query = """
    query submissionDetails($id: Int!) {
      submissionDetails(submissionId: $id) {
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
        json={"query": sub_query, "variables": {"id": int(sub_id)}},
    )

    sub_data = sub_resp.json()

    if not sub_data.get("data"):
        continue

    code = sub_data["data"]["submissionDetails"]["code"]
    lang = sub_data["data"]["submissionDetails"]["lang"]["name"]

    # Only SQL problems
    if "SQL" not in lang:
        continue

    filename = re.sub(r"[^a-zA-Z0-9]", "_", title) + ".sql"

    with open(f"1_SQL/{filename}", "w") as f:
        f.write(f"-- {title}\n")
        f.write(f"-- https://leetcode.com/problems/{slug}/\n\n")
        f.write(code)

print("SQL sync complete")
