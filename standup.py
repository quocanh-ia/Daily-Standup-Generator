import subprocess
from datetime import datetime

def get_git_commits(limit=5):
    result = subprocess.run(
        ["git", "log", f"-{limit}", "--pretty=format:%s"],
        capture_output=True,
        text=True
    )
    commits = result.stdout.strip().split("\n")
    return [c for c in commits if c]

def generate_standup():
    today = datetime.now().strftime("%Y-%m-%d")
    commits = get_git_commits()

    standup = []
    standup.append(f"# Daily Standup ({today})\n")

    standup.append("## Yesterday")
    if commits:
        for c in commits:
            standup.append(f"- {c}")
    else:
        standup.append("- No commits found")

    standup.append("\n## Today")
    standup.append("- Continue current tasks")
    standup.append("- Review code / improve features")

    standup.append("\n## Blockers")
    standup.append("- None")

    return "\n".join(standup)

if __name__ == "__main__":
    content = generate_standup()
    with open("standup.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ standup.md generated successfully")
