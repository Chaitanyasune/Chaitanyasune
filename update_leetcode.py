import requests
from datetime import datetime

USERNAME = "Chaitanyasune"
README_PATH = "README.md"
MARKER = "<!-- LEETCODE-STATS -->"

query = """
query getUserProfile($username: String!) {
  matchedUser(username: $username) {
    submitStats: submitStatsGlobal {
      acSubmissionNum {
        difficulty
        count
      }
    }
  }
}
"""

variables = {"username": USERNAME}

response = requests.post(
    "https://leetcode.com/graphql",
    json={"query": query, "variables": variables}
)

data = response.json()
stats = data["data"]["matchedUser"]["submitStats"]["acSubmissionNum"]
easy = stats[1]["count"]
medium = stats[2]["count"]
hard = stats[3]["count"]
total = stats[0]["count"]

content = f"""
**LeetCode Stats**  
🟢 Easy: {easy}  
🟠 Medium: {medium}  
🔴 Hard: {hard}  
🏆 Total: {total}  
_Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC_
"""

with open(README_PATH, "r", encoding="utf-8") as f:
    readme = f.read()

before, after = readme.split(MARKER)
new_readme = f"{before}{MARKER}\n{content}\n{MARKER}{after}"

with open(README_PATH, "w", encoding="utf-8") as f:
    f.write(new_readme)
