import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json
import os

# ==================== SETTINGS ====================

APP_NAME = "PERSONAL COMMAND CENTER"
DATA_FILE = "command_center_data.json"

BG = "#0B1020"
PANEL = "#151F33"
PANEL_LIGHT = "#1D2A42"
CYAN = "#67F5D4"
PURPLE = "#A78BFA"
WHITE = "#F1F5F9"
MUTED = "#94A3B8"
GREEN = "#4ADE80"
RED = "#FB7185"
FONT = "Segoe UI"


# ==================== DATA MANAGEMENT ====================

def load_data():
    default_data = {
        "tasks": [],
        "notes": "",
        "goals": []
    }

    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                saved_data = json.load(file)

            if isinstance(saved_data, dict):
                default_data.update(saved_data)

        except (json.JSONDecodeError, OSError):
            pass

    return default_data


def save_data():
    data = {
        "tasks": tasks,
        "notes": notes_box.get("1.0", "end-1c"),
        "goals": goals
    }

    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except OSError:
        messagebox.showerror(
            "Save Error",
            "Could not save your data. Check folder permissions."
        )


saved_data = load_data()
tasks = saved_data.get("tasks", [])
goals = saved_data.get("goals", [])

if not isinstance(tasks, list):
    tasks = []

if not isinstance(goals, list):
    goals = []


# ==================== MAIN WINDOW ====================

root = tk.Tk()
root.title(APP_NAME)
root.geometry("1100x760")
root.minsize(850, 650)
root.configure(bg=BG)

timer_job = None
timer_running = False
remaining_seconds = 25 * 60
focus_seconds = 25 * 60


# ==================== HELPER FUNCTIONS ====================

def make_label(parent, text, size=11, color=WHITE, bold=False):
    return tk.Label(
        parent,
        text=text,
        font=(FONT, size, "bold" if bold else "normal"),
        bg=parent.cget("bg"),
        fg=color
    )


def make_button(parent, text, command, color=CYAN, fg=BG):
    return tk.Button(
        parent,
        text=text,
        command=command,
        font=(FONT, 10, "bold"),
        bg=color,
        fg=fg,
        activebackground=WHITE,
        activeforeground=BG,
        relief="flat",
        bd=0,
        padx=12,
        pady=8,
        cursor="hand2"
    )


def make_panel(parent, title):
    panel = tk.Frame(parent, bg=PANEL, padx=16, pady=14)
    make_label(panel, title, 12, CYAN, True).pack(anchor="w", pady=(0, 12))
    return panel


def show_page(page_name):
    for page in pages.values():
        page.pack_forget()

    pages[page_name].pack(fill="both", expand=True)
    page_title.config(text=page_name.upper())


def update_clock():
    now = datetime.now()
    clock_label.config(text=now.strftime("%I:%M:%S %p"))
    date_label.config(text=now.strftime("%A, %d %B %Y"))
    root.after(1000, update_clock)


def on_close():
    global timer_job, timer_running

    timer_running = False

    if timer_job is not None:
        root.after_cancel(timer_job)
        timer_job = None

    save_data()
    root.destroy()


# ==================== HEADER ====================

header = tk.Frame(root, bg=BG, padx=24, pady=18)
header.pack(fill="x")

brand = tk.Frame(header, bg=BG)
brand.pack(side="left")

make_label(
    brand, "◈  PERSONAL", 17, CYAN, True
).pack(anchor="w")

make_label(
    brand, "COMMAND CENTER  /  SYSTEM ONLINE", 9, MUTED
).pack(anchor="w", pady=(3, 0))

clock_area = tk.Frame(header, bg=BG)
clock_area.pack(side="right")

clock_label = make_label(clock_area, "--:--:--", 20, WHITE, True)
clock_label.pack(anchor="e")

date_label = make_label(clock_area, "", 9, MUTED)
date_label.pack(anchor="e", pady=(3, 0))

tk.Frame(root, bg=CYAN, height=2).pack(fill="x", padx=24)


# ==================== NAVIGATION ====================

body = tk.Frame(root, bg=BG, padx=24, pady=18)
body.pack(fill="both", expand=True)

sidebar = tk.Frame(body, bg=PANEL, width=190, padx=12, pady=16)
sidebar.pack(side="left", fill="y", padx=(0, 18))
sidebar.pack_propagate(False)

make_label(sidebar, "NAVIGATION", 10, MUTED, True).pack(
    anchor="w", padx=8, pady=(4, 14)
)

content = tk.Frame(body, bg=BG)
content.pack(side="left", fill="both", expand=True)

page_title = make_label(content, "DASHBOARD", 16, WHITE, True)
page_title.pack(anchor="w", pady=(0, 14))

page_area = tk.Frame(content, bg=BG)
page_area.pack(fill="both", expand=True)

pages = {}

for name in ["Dashboard", "Tasks", "Notes", "Focus Timer", "Daily Goals"]:
    pages[name] = tk.Frame(page_area, bg=BG)

    make_button(
        sidebar,
        "▸  " + name,
        lambda n=name: show_page(n),
        color=PANEL_LIGHT,
        fg=WHITE
    ).pack(fill="x", pady=4)


# ==================== DASHBOARD PAGE ====================

dashboard = pages["Dashboard"]

welcome = tk.Frame(dashboard, bg=PANEL, padx=20, pady=20)
welcome.pack(fill="x", pady=(0, 14))

make_label(
    welcome, "WELCOME BACK, OPERATOR.", 19, CYAN, True
).pack(anchor="w")

make_label(
    welcome,
    "Your personal space. Your goals. Your progress.",
    10, MUTED
).pack(anchor="w", pady=(7, 0))

stats = tk.Frame(dashboard, bg=BG)
stats.pack(fill="x", pady=(0, 14))

def create_stat(parent, title, value, accent):
    card = tk.Frame(parent, bg=PANEL, padx=14, pady=15)
    card.pack(side="left", fill="both", expand=True, padx=(0, 10))

    make_label(card, title, 9, MUTED, True).pack(anchor="w")

    value_label = make_label(card, value, 23, accent, True)
    value_label.pack(anchor="w", pady=(8, 0))

    return value_label


task_stat = create_stat(stats, "TOTAL TASKS", "0", CYAN)
done_stat = create_stat(stats, "COMPLETED", "0", GREEN)
goal_stat = create_stat(stats, "GOALS DONE", "0", PURPLE)

quick_panel = make_panel(dashboard, "QUICK ACTIONS")
quick_panel.pack(fill="x", pady=(0, 14))

quick_buttons = tk.Frame(quick_panel, bg=PANEL)
quick_buttons.pack(fill="x")

make_button(
    quick_buttons, "+ New Task", lambda: show_page("Tasks")
).pack(side="left", padx=(0, 8))

make_button(
    quick_buttons, "Open Notes", lambda: show_page("Notes"),
    color=PURPLE, fg=BG
).pack(side="left", padx=8)

make_button(
    quick_buttons, "Start Focus", lambda: show_page("Focus Timer"),
    color=GREEN, fg=BG
).pack(side="left", padx=8)

overview = make_panel(dashboard, "SYSTEM OVERVIEW")
overview.pack(fill="both", expand=True)

overview_text = make_label(
    overview,
    "Stay consistent. Complete one task at a time.",
    11, WHITE
)
overview_text.pack(anchor="w")


# ==================== TASK MANAGER ====================

task_page = pages["Tasks"]

task_panel = make_panel(task_page, "TASK MANAGEMENT")
task_panel.pack(fill="both", expand=True)

task_input_row = tk.Frame(task_panel, bg=PANEL)
task_input_row.pack(fill="x", pady=(0, 12))

task_entry = tk.Entry(
    task_input_row,
    font=(FONT, 11),
    bg=PANEL_LIGHT,
    fg=WHITE,
    insertbackground=CYAN,
    relief="flat"
)
task_entry.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 8))


def add_task(event=None):
    text = task_entry.get().strip()

    if not text:
        return

    tasks.append({"text": text, "done": False})
    task_entry.delete(0, "end")
    refresh_tasks()
    save_data()


make_button(task_input_row, "ADD TASK", add_task).pack(side="right")
task_entry.bind("<Return>", add_task)

task_list_frame = tk.Frame(task_panel, bg=PANEL)
task_list_frame.pack(fill="both", expand=True)

task_canvas = tk.Canvas(
    task_list_frame, bg=PANEL, highlightthickness=0
)
task_scrollbar = tk.Scrollbar(
    task_list_frame, orient="vertical", command=task_canvas.yview
)
task_inner = tk.Frame(task_canvas, bg=PANEL)

task_window = task_canvas.create_window(
    (0, 0), window=task_inner, anchor="nw"
)

task_canvas.configure(yscrollcommand=task_scrollbar.set)

task_canvas.pack(side="left", fill="both", expand=True)
task_scrollbar.pack(side="right", fill="y")


def update_task_scroll(event=None):
    task_canvas.configure(scrollregion=task_canvas.bbox("all"))
    task_canvas.itemconfigure(task_window, width=task_canvas.winfo_width())


task_inner.bind("<Configure>", update_task_scroll)
task_canvas.bind("<Configure>", update_task_scroll)


def refresh_tasks():
    for widget in task_inner.winfo_children():
        widget.destroy()

    if not tasks:
        make_label(
            task_inner, "No tasks yet. Add your first task above.",
            10, MUTED
        ).pack(anchor="w", pady=10)
    else:
        for index, task in enumerate(tasks):
            row = tk.Frame(task_inner, bg=PANEL_LIGHT, padx=10, pady=9)
            row.pack(fill="x", pady=4)

            done_var = tk.BooleanVar(value=task.get("done", False))

            def toggle_task(i=index, var=done_var):
                tasks[i]["done"] = var.get()
                refresh_tasks()
                update_stats()
                save_data()

            tk.Checkbutton(
                row,
                variable=done_var,
                command=toggle_task,
                bg=PANEL_LIGHT,
                activebackground=PANEL_LIGHT,
                selectcolor=BG,
                fg=CYAN
            ).pack(side="left")

            task_text = str(task.get("text", ""))
            task_color = MUTED if task.get("done", False) else WHITE

            make_label(
                row, task_text, 10, task_color
            ).pack(side="left", fill="x", expand=True, padx=5)

            make_button(
                row, "✕",
                lambda i=index: delete_task(i),
                color=RED, fg=BG
            ).pack(side="right")


def delete_task(index):
    if 0 <= index < len(tasks):
        tasks.pop(index)
        refresh_tasks()
        update_stats()
        save_data()


# ==================== NOTES ====================

notes_page = pages["Notes"]

notes_panel = make_panel(notes_page, "QUICK NOTES")
notes_panel.pack(fill="both", expand=True)

make_label(
    notes_panel,
    "Write ideas, reminders, or anything you want to remember.",
    10, MUTED
).pack(anchor="w", pady=(0, 10))

notes_box = tk.Text(
    notes_panel,
    font=(FONT, 11),
    bg=PANEL_LIGHT,
    fg=WHITE,
    insertbackground=CYAN,
    selectbackground=CYAN,
    selectforeground=BG,
    relief="flat",
    wrap="word",
    padx=12,
    pady=12,
    undo=True
)
notes_box.pack(fill="both", expand=True)

notes_box.insert("1.0", str(saved_data.get("notes", "")))


def save_notes(event=None):
    save_data()


notes_box.bind("<KeyRelease>", save_notes)

make_button(
    notes_panel, "SAVE NOTES", save_notes
).pack(anchor="e", pady=(10, 0))


# ==================== FOCUS TIMER ====================

focus_page = pages["Focus Timer"]

focus_panel = make_panel(focus_page, "FOCUS MODE")
focus_panel.pack(fill="both", expand=True)

make_label(
    focus_panel, "ONE TASK. ZERO DISTRACTIONS.", 13, PURPLE, True
).pack(pady=(25, 10))

timer_label = make_label(
    focus_panel, "25:00", 48, CYAN, True
)
timer_label.pack(pady=18)

timer_status = make_label(
    focus_panel, "Ready when you are.", 10, MUTED
)
timer_status.pack(pady=(0, 18))

timer_controls = tk.Frame(focus_panel, bg=PANEL)
timer_controls.pack(pady=10)


def update_timer_display():
    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60
    timer_label.config(text=f"{minutes:02d}:{seconds:02d}")


def timer_tick():
    global remaining_seconds, timer_job, timer_running

    timer_job = None

    if not timer_running:
        return

    if remaining_seconds > 0:
        remaining_seconds -= 1
        update_timer_display()

    if remaining_seconds <= 0:
        timer_running = False
        timer_status.config(text="Focus session complete! Great work.", fg=GREEN)
        messagebox.showinfo("Focus Complete", "Your focus session is complete!")
    else:
        timer_job = root.after(1000, timer_tick)


def start_timer():
    global timer_running, timer_job

    if timer_running:
        return

    if remaining_seconds <= 0:
        timer_status.config(text="Press RESET to start a new session.", fg=RED)
        return

    timer_running = True
    timer_status.config(text="Focus session in progress...", fg=CYAN)
    timer_job = root.after(1000, timer_tick)


def pause_timer():
    global timer_running, timer_job

    timer_running = False

    if timer_job is not None:
        root.after_cancel(timer_job)
        timer_job = None

    timer_status.config(text="Timer paused.", fg=MUTED)


def reset_timer():
    global remaining_seconds, timer_running, timer_job

    timer_running = False

    if timer_job is not None:
        root.after_cancel(timer_job)
        timer_job = None

    remaining_seconds = focus_seconds
    update_timer_display()
    timer_status.config(text="Ready when you are.", fg=MUTED)


def choose_duration(minutes):
    global focus_seconds, remaining_seconds

    pause_timer()
    focus_seconds = minutes * 60
    remaining_seconds = focus_seconds
    update_timer_display()
    timer_status.config(text=f"{minutes}-minute session selected.", fg=MUTED)


make_button(
    timer_controls, "START", start_timer, color=GREEN
).pack(side="left", padx=5)

make_button(
    timer_controls, "PAUSE", pause_timer, color=PURPLE
).pack(side="left", padx=5)

make_button(
    timer_controls, "RESET", reset_timer, color=RED
).pack(side="left", padx=5)

duration_panel = tk.Frame(focus_panel, bg=PANEL)
duration_panel.pack(pady=20)

make_label(duration_panel, "SESSION LENGTH", 9, MUTED, True).pack(pady=5)

duration_buttons = tk.Frame(duration_panel, bg=PANEL)
duration_buttons.pack()

for minutes in [5, 15, 25, 45]:
    make_button(
        duration_buttons,
        f"{minutes} MIN",
        lambda m=minutes: choose_duration(m),
        color=PANEL_LIGHT,
        fg=WHITE
    ).pack(side="left", padx=4, pady=5)


# ==================== DAILY GOALS ====================

goals_page = pages["Daily Goals"]

goals_panel = make_panel(goals_page, "DAILY GOALS")
goals_panel.pack(fill="both", expand=True)

make_label(
    goals_panel, "Small steps create big progress.", 10, MUTED
).pack(anchor="w", pady=(0, 12))

goal_input_row = tk.Frame(goals_panel, bg=PANEL)
goal_input_row.pack(fill="x", pady=(0, 12))

goal_entry = tk.Entry(
    goal_input_row,
    font=(FONT, 11),
    bg=PANEL_LIGHT,
    fg=WHITE,
    insertbackground=CYAN,
    relief="flat"
)
goal_entry.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 8))


def add_goal(event=None):
    text = goal_entry.get().strip()

    if not text:
        return

    goals.append({"text": text, "done": False})
    goal_entry.delete(0, "end")
    refresh_goals()
    save_data()


goal_entry.bind("<Return>", add_goal)
make_button(goal_input_row, "ADD GOAL", add_goal).pack(side="right")

goal_list_frame = tk.Frame(goals_panel, bg=PANEL)
goal_list_frame.pack(fill="both", expand=True)


def refresh_goals():
    for widget in goal_list_frame.winfo_children():
        widget.destroy()

    if not goals:
        make_label(
            goal_list_frame, "No goals yet. Add a goal to get started.",
            10, MUTED
        ).pack(anchor="w", pady=10)
    else:
        for index, goal in enumerate(goals):
            row = tk.Frame(goal_list_frame, bg=PANEL_LIGHT, padx=10, pady=9)
            row.pack(fill="x", pady=4)

            done_var = tk.BooleanVar(value=goal.get("done", False))

            def toggle_goal(i=index, var=done_var):
                goals[i]["done"] = var.get()
                refresh_goals()
                update_stats()
                save_data()

            tk.Checkbutton(
                row,
                variable=done_var,
                command=toggle_goal,
                bg=PANEL_LIGHT,
                activebackground=PANEL_LIGHT,
                selectcolor=BG,
                fg=PURPLE
            ).pack(side="left")

            make_label(
                row,
                str(goal.get("text", "")),
                10,
                MUTED if goal.get("done", False) else WHITE
            ).pack(side="left", fill="x", expand=True, padx=5)

            make_button(
                row, "✕",
                lambda i=index: delete_goal(i),
                color=RED, fg=BG
            ).pack(side="right")


def delete_goal(index):
    if 0 <= index < len(goals):
        goals.pop(index)
        refresh_goals()
        update_stats()
        save_data()


# ==================== DASHBOARD STATISTICS ====================

def update_stats():
    completed_tasks = sum(
        1 for task in tasks if task.get("done", False)
    )
    completed_goals = sum(
        1 for goal in goals if goal.get("done", False)
    )

    task_stat.config(text=str(len(tasks)))
    done_stat.config(text=str(completed_tasks))
    goal_stat.config(text=f"{completed_goals}/{len(goals)}")

    if tasks:
        overview_text.config(
            text=f"You have {len(tasks)} tasks and "
                 f"{completed_tasks} completed. Keep moving forward!"
        )
    else:
        overview_text.config(
            text="Your workspace is ready. Add a task and get started!"
        )


# ==================== START APPLICATION ====================

refresh_tasks()
refresh_goals()
update_stats()
update_clock()
update_timer_display()
show_page("Dashboard")

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()