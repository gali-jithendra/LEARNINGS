import requests
import os

USERNAME = os.environ.get("LEETCODE_USERNAME")

url = "https://leetcode.com/graphql"

query = """
query getUserProfile($username: String!) {
  matchedUser(username: $username) {
    submitStats {
      acSubmissionNum {
        difficulty
        count
      }
    }
  }
}
"""

variables = {"username": USERNAME}

response = requests.post(url, json={"query": query, "variables": variables})
data = response.json()

with open("LEARNINGS/1_SQL/progress.json", "w") as f:
    f.write(str(data))
