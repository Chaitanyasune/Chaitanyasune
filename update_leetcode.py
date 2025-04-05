import requests
from datetime import datetime

USERNAME = "Chaitanya_Sune"
README_PATH = "README.md"
START_MARKER = "<!-- LEETCODE_STATS:-->"
END_MARKER = "<!-- LEETCODE_STATS:END -->"

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

# Check both markers are present
if START_MARKER not in readme or END_MARKER not in readme:
    raise ValueError("Start or end marker not found in README.")

# Split content between the markers
before = readme.split(START_MARKER)[0]
after = readme.split(END_MARKER)[1]

# Inject content
new_readme = f"{before}{START_MARKER}\n{content}\n{END_MARKER}{after}"

with open(README_PATH, "w", encoding="utf-8") as f:
    f.write(new_readme)
