import requests
import os
import json
import re

USERNAME = os.environ.get("LEETCODE_USERNAME")
SESSION = os.environ.get("LEETCODE_SESSION")

headers = {
    "cookie": f"LEETCODE_SESSION={SESSION}",
    "content-type": "application/json",
    "referer": "https://leetcode.com"
}

url = "https://leetcode.com/graphql"

query = """
query recentAcSubmissions($username: String!) {
  recentAcSubmissionList(username: $username) {
    id
    title
    titleSlug
    timestamp
  }
}
"""

resp = requests.post(
    url,
    headers=headers,
    json={"query": query, "variables": {"username": USERNAME}},
)

data = resp.json()

os.makedirs("1_SQL", exist_ok=True)

for item in data["data"]["recentAcSubmissionList"]:
    title = item["title"]
    slug = item["titleSlug"]

    # fetch submission details
    sub_query = """
    query submissionDetails($slug: String!) {
      question(titleSlug: $slug) {
        title
        topicTags {
          name
        }
      }
    }
    """

    q = requests.post(
        url,
        headers=headers,
        json={"query": sub_query, "variables": {"slug": slug}},
    )

    qdata = q.json()

    tags = [t["name"] for t in qdata["data"]["question"]["topicTags"]]

    if "Database" not in tags:
        continue

    filename = re.sub(r"[^a-zA-Z0-9]", "_", title) + ".sql"

    with open(f"1_SQL/{filename}", "w") as f:
        f.write(f"-- {title}\n-- https://leetcode.com/problems/{slug}/\n\n-- SQL Solution Placeholder\n")

print("Sync complete")
