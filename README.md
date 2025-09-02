# daily_sidekick

Daily Sidekick 🙂 is a warm, human-friendly **terminal To-Do app** built with Python.  
It helps you manage tasks with priorities, optional due dates, and a sprinkle of motivation through emojis, colors, and gentle tips.  
Stay organized, celebrate progress, and keep your day a little lighter — all from your command line.

> “Tiny progress counts.” ✅

---

## ✨ Features
- 🎨 **Friendly UI**: emojis + ANSI colors (auto-disables if unsupported)  
- 📝 **Task management**: add, edit, delete, mark as done  
- ⏳ **Due dates**: optional `YYYY-MM-DD`, shown as “due today / in 3 days / overdue”  
- 🔺 **Priorities**: `low`, `medium` (default), `high`  
- 🔍 **Search**: quickly find tasks by keyword  
- 🧹 **Clear completed**: spring-clean your finished tasks in one go  
- 💡 **Tips & celebrations**: gentle nudges and random positive messages  
- 💾 **Persistent data**: tasks saved locally in `tasks.json`  

---

## 📦 Requirements
- Python **3.6+** (f-strings required)  
  Recommended: Python **3.8+** (actively supported)  
 
- A terminal that supports ANSI colors (most do).  
  - Set `NO_COLOR=1` to force plain text.  
  - Works in Windows Terminal, PowerShell, macOS, Linux shells.  

---

## 🚀 Installation
Clone this repository and run the script:

```bash
git clone https://github.com/yourusername/daily_sidekick.git
cd daily_sidekick
python todo.py
