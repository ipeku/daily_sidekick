import json
import os
import random
from datetime import datetime, date

DATA_FILE = "tasks.json"
VALID_PRIORITIES = ["low", "medium", "high"]

def supports_color():
    return os.getenv("NO_COLOR") is None and os.name != "nt" or "WT_SESSION" in os.environ or "ANSICON" in os.environ

COLOR = supports_color()
def c(text, code):
    if not COLOR: return text
    return f"\033[{code}m{text}\033[0m"

def green(s):  return c(s, "32")
def red(s):    return c(s, "31")
def yellow(s): return c(s, "33")
def blue(s):   return c(s, "34")
def dim(s):    return c(s, "2")

CELEBRATIONS = [
    "Nice! One step closer 🎉",
    "Boom! Done and dusted ✅",
    "Love that momentum 🚀",
    "Another win for you ✨",
]

TIPS = [
    "Tip: You can keep fields empty to leave them unchanged.",
    "Tip: Use realistic due dates—tiny deadlines beat vague goals.",
    "Tip: 'high' priority is for today-or-else items.",
    "Tip: Clearing completed tasks feels great—try it now and then.",
]

def banner():
    user = os.getenv("USER") or os.getenv("USERNAME") or ""
    hello = f"Hi {user}!" if user else "Hi!"
    print(blue("┌───────────────────────────────────────────────┐"))
    print(blue(" ") + "             Daily Sidekick :)" + blue("                    "))
    print(blue("└───────────────────────────────────────────────┘"))
    print(dim(f"{hello} Let’s make today a bit lighter."))

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            tasks = json.load(f)
            for t in tasks:
                t.setdefault("done", False)
                t.setdefault("priority", "medium")
                t.setdefault("due_date", None)
            return tasks
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4, ensure_ascii=False)

def parse_date_str(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except Exception:
        return None

def human_due(due_str):
    if not due_str:
        return dim("no due date")
    d = parse_date_str(due_str)
    if not d:
        return dim(due_str)
    today = date.today()
    delta = (d - today).days
    if delta == 0:
        return yellow("due today")
    if delta == 1:
        return yellow("due tomorrow")
    if delta > 1:
        return dim(f"due in {delta} days")
    if delta == -1:
        return red("overdue by 1 day")
    return red(f"overdue by {abs(delta)} days")

def format_task_line(i, task):
    status = green("✔") if task.get("done") else red("•")
    prio = task.get("priority", "medium")
    prio_txt = {"low": dim("low"), "medium": "medium", "high": yellow("HIGH")}.get(prio, prio)
    due_txt = human_due(task.get("due_date"))
    title = task.get("title", "")
    return f"{i:>2}. {status} {title}  {dim('[')}{prio_txt}{dim(']')}  {dim('(')}{due_txt}{dim(')')}"

def list_tasks(tasks, only="all"):
    if only == "completed":
        filtered = [t for t in tasks if t.get("done")]
    elif only == "pending":
        filtered = [t for t in tasks if not t.get("done")]
    else:
        filtered = tasks

    if not filtered:
        msg = "No tasks here—fresh start! ✨" if only != "completed" else "No completed tasks yet. You got this! 💪"
        print(green(f"✅ {msg}\n"))
        return

    header = {
        "all": "All tasks",
        "pending": "Pending tasks",
        "completed": "Completed tasks"
    }[only]
    print(blue(f"\n📋 {header}:"))
    for i, task in enumerate(filtered, 1):
        print(format_task_line(i, task))
    print()

def input_priority(default="medium"):
    raw = input(dim(f"Priority (low/medium/high) [{default}]: ")).strip().lower()
    if raw == "":
        return default
    if raw not in VALID_PRIORITIES:
        print(yellow("⚠ Using 'medium' (unknown priority)."))
        return "medium"
    return raw

def input_due_date(default=None):
    raw = input(dim(f"Due date YYYY-MM-DD (optional) [{default or ''}]: ")).strip()
    if raw == "":
        return default
    if parse_date_str(raw):
        return raw
    print(yellow("⚠ Couldn't parse date. Leaving it empty."))
    return default

def add_task(tasks):
    title = input("What do you want to get done? ").strip()
    if not title:
        print(yellow("⚠ Title can't be empty.\n")); return
    priority = input_priority("medium")
    due_date = input_due_date(None)
    tasks.append({"title": title, "done": False, "priority": priority, "due_date": due_date})
    save_tasks(tasks)
    print(green("✅ Added! Tiny progress counts.\n"))

def mark_done(tasks):
    list_tasks(tasks, "pending")
    try:
        idx = int(input("Number to mark as done: ")) - 1
        if idx < 0 or idx >= len(tasks) or tasks[idx].get("done"):
            raise IndexError
        tasks[idx]["done"] = True
        save_tasks(tasks)
        print(green(f"{random.choice(CELEBRATIONS)}\n"))
    except (ValueError, IndexError):
        print(yellow("⚠ That didn't match a pending task.\n"))

def delete_task(tasks):
    list_tasks(tasks, "all")
    try:
        idx = int(input("Number to delete: ")) - 1
        if idx < 0 or idx >= len(tasks):
            raise IndexError
        title = tasks[idx]["title"]
        confirm = input(yellow(f"Delete “{title}”? (y/N): ")).strip().lower()
        if confirm == "y":
            tasks.pop(idx)
            save_tasks(tasks)
            print(green("🗑 Deleted. Breathing room feels nice.\n"))
        else:
            print(dim("Cancelled.\n"))
    except (ValueError, IndexError):
        print(yellow("⚠ Couldn't find that task.\n"))

def edit_task(tasks):
    list_tasks(tasks, "all")
    try:
        idx = int(input("Number to edit: ")) - 1
        task = tasks[idx]
    except (ValueError, IndexError):
        print(yellow("⚠ Couldn't find that task.\n")); return

    print(dim("Press Enter to keep as-is."))
    new_title = input(f"Title [{task.get('title','')}]: ").strip()
    if new_title:
        task["title"] = new_title
    task["priority"] = input_priority(task.get("priority", "medium"))
    task["due_date"] = input_due_date(task.get("due_date"))
    save_tasks(tasks)
    print(green("✏ Updated. Looks better already.\n"))

def search_tasks(tasks):
    q = input("Search for: ").strip().lower()
    results = [t for t in tasks if q in t.get("title", "").lower()]
    if not results:
        print(dim("No matches. Maybe try a shorter keyword?\n")); return
    print(blue("\n🔎 Matches:"))
    for i, t in enumerate(results, 1):
        print(format_task_line(i, t))
    print()

def clear_completed(tasks):
    completed = [t for t in tasks if t.get("done")]
    if not completed:
        print(dim("Nothing to clear. Keep going! 🌱\n")); return
    n = len(completed)
    confirm = input(yellow(f"Clear {n} completed task{'s' if n>1 else ''}? (y/N): ")).strip().lower()
    if confirm == "y":
        tasks[:] = [t for t in tasks if not t.get("done")]
        save_tasks(tasks)
        print(green("🧹 All done—neat and tidy.\n"))
    else:
        print(dim("Cancelled.\n"))

def maybe_tip():
    if random.random() < 0.25:
        print(dim(random.choice(TIPS)))

def main():
    tasks = load_tasks()
    banner()
    while True:
        print("\n" + blue("=== Menu ==="))
        print("1) List all  2) Add  3) Mark done  4) Delete")
        print("5) Edit      6) Search  7) Clear completed")
        print("8) List pending  9) List completed  0) Exit")
        choice = input(dim("Choose (0-9): ")).strip()

        if choice == "1":
            list_tasks(tasks, "all")
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            mark_done(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            edit_task(tasks)
        elif choice == "6":
            search_tasks(tasks)
        elif choice == "7":
            clear_completed(tasks)
        elif choice == "8":
            list_tasks(tasks, "pending")
        elif choice == "9":
            list_tasks(tasks, "completed")
        elif choice == "0":
            print(green("👋 Take care. You did enough for today.\n"))
            break
        else:
            print(yellow("⚠ Invalid choice."))
        maybe_tip()

if __name__ == "__main__":
    main()