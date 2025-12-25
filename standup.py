import os
import json
import subprocess
from datetime import datetime
from collections import Counter

# =========================
# CONFIG (demo-friendly)
# =========================
TIME_WINDOW_MINUTES = 10      # Demo nhanh. Đổi 1440 = 24h
TASK_FILE = "tasks.json"      # Simulate Jira / Teams API response
OUTPUT_DIR = "standups"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# =========================
# GIT COMMITS (time-based)
# =========================
def get_git_commits(minutes):
    """
    Get git commit messages within the last <minutes>
    """
    cmd = [
        "git",
        "log",
        f"--since={minutes} minutes ago",
        "--pretty=format:%s"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    commits = result.stdout.strip().split("\n") if result.stdout else []
    return [c.strip() for c in commits if c.strip()]


# =========================
# LOAD TASKS (JSON)
# =========================
def load_tasks():
    """
    Expected tasks.json format (example):
    {
      "today": [
        {"source": "Jira", "title": "Implement standup generator", "status": "In Progress"},
        {"source": "Teams", "title": "Refactor commit parsing logic", "status": "Done"}
      ],
      "blockers": [
        {"reason": "Waiting for code review approval"}
      ]
    }
    """
    if not os.path.exists(TASK_FILE):
        return {"today": [], "blockers": []}

    with open(TASK_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Safety defaults
    if "today" not in data:
        data["today"] = []
    if "blockers" not in data:
        data["blockers"] = []
    return data


# =========================
# AI-LIKE SUMMARY (mock - counts only)
# =========================
def guess_commit_type(msg: str) -> str:
    """
    Guess conventional commit type by prefix: feat:, fix:, docs:, test:, refactor:, chore:, perf:, style:
    """
    m = msg.strip().lower()
    for t in ["docs", "test", "refactor", "feat", "fix", "chore", "perf", "style"]:
        if m.startswith(t + ":"):
            return t
    return "other"


def normalize_status(s: str) -> str:
    s = str(s).strip().lower()
    if s in ["in progress", "in_progress", "doing"]:
        return "in_progress"
    if s in ["done", "completed"]:
        return "done"
    if s in ["todo", "to do", "backlog", "open"]:
        return "todo"
    return s


def build_ai_summary_lines(commits, tasks, window_minutes):
    """
    Return a list of markdown bullet lines for AI Summary section.
    Counts only (no highlights) + task snapshot.
    """
    today_tasks = tasks.get("today", [])
    blockers = tasks.get("blockers", [])
    done = sum(1 for t in today_tasks if normalize_status(t.get("status", "")) == "done")
    inprog = sum(1 for t in today_tasks if normalize_status(t.get("status", "")) == "in_progress")
    todo = sum(1 for t in today_tasks if normalize_status(t.get("status", "")) == "todo")

    if not commits:
        return [
            f"- 0 commit(s) in last {window_minutes} minutes.",
            f"- Tasks snapshot: {todo} ToDo, {inprog} In Progress, {done} Done; blockers: {len(blockers)}."
        ]

    types = [guess_commit_type(c) for c in commits]
    cnt = Counter(types)

    # Order for display (đẹp + dễ đọc)
    display_order = ["docs", "test", "refactor", "feat", "fix", "chore", "perf", "style", "other"]
    breakdown_parts = [f"{k}={cnt[k]}" for k in display_order if cnt.get(k, 0) > 0]
    breakdown = ", ".join(breakdown_parts)

    return [
        f"- {len(commits)} commit(s) in last {window_minutes} minutes ({breakdown}).",
        f"- Tasks snapshot: {todo} ToDo, {inprog} In Progress, {done} Done; blockers: {len(blockers)}."
    ]


# =========================
# GENERATE STANDUP
# =========================
def generate_standup():
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M")
    date_label = now.strftime("%Y-%m-%d")

    commits = get_git_commits(TIME_WINDOW_MINUTES)
    tasks = load_tasks()

    lines = []
    lines.append(f"# Daily Standup ({date_label})\n")

    # Recent work (time-based)
    lines.append(f"## Recent work (last {TIME_WINDOW_MINUTES} minutes)")
    if commits:
        for c in commits:
            lines.append(f"- {c}")
    else:
        lines.append("- No commits found")

    # AI summary (counts only)
    lines.append("\n## AI Summary")
    for s in build_ai_summary_lines(commits, tasks, TIME_WINDOW_MINUTES):
        lines.append(s)

    # Today tasks
    lines.append("\n## Today")
    today_tasks = tasks.get("today", [])
    if today_tasks:
        for t in today_tasks:
            source = t.get("source", "Unknown")
            title = t.get("title", "Untitled")
            status = t.get("status", "ToDo")
            lines.append(f"- [{source}] {title} ({status})")
    else:
        lines.append("- No planned tasks")

    # Blockers
    lines.append("\n## Blockers")
    blockers = tasks.get("blockers", [])
    if blockers:
        for b in blockers:
            if isinstance(b, dict):
                lines.append(f"- {b.get('reason', 'Unknown blocker')}")
            else:
                lines.append(f"- {str(b)}")
    else:
        lines.append("- None")

    output_path = os.path.join(OUTPUT_DIR, f"standup-{timestamp}.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ Standup generated: {output_path}")


if __name__ == "__main__":
    generate_standup()
