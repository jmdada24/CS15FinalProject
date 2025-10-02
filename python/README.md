# Boolean Todo List - PyQt5 Version

A beautiful, modern todo list application built with PyQt5, matching the design and functionality of the Flutter version.

## Features

✅ **Splash Screen** with smooth transition
✅ **Phone-like Frame** (390x844px - iPhone 13 Pro size)
✅ **Modern UI** with purple theme matching Flutter design
✅ **Task Management** - Add, Edit, Delete, Complete tasks
✅ **Categories** - Home, Shopping, Work, Fitness, Other
✅ **Date & Time** selection for tasks
✅ **Notes** support for detailed task descriptions
✅ **Smooth Navigation** between screens
✅ **Clickable Cards** - Click anywhere to edit task
✅ **Category Icon Toggle** - Click icon to mark complete/incomplete

## Folder Structure

```
python/
├── main.py                    # Entry point - run this!
├── config/
│   └── theme.py              # Colors, fonts, styles
├── models/
│   └── task.py               # Task data model
├── screens/
│   ├── splash_screen.py      # Splash screen with animation
│   ├── home_screen.py        # Main todo list screen
│   └── add_task_screen.py    # Add/Edit task screen
├── widgets/
│   └── task_card.py          # Custom task card widget
└── assets/
    └── (logo.png optional)
```

## Requirements

- Python 3.7+
- PyQt5

## Installation

```bash
pip install PyQt5
```

## Running the App

```bash
cd python
python main.py
```

## How to Use

1. **Splash Screen** - Appears for 2 seconds on startup
2. **Home Screen** - View all your tasks (Active & Completed sections)
   - Click **Add New Task** button to create new task
   - Click **category icon** to mark task complete/incomplete
   - Click **anywhere on card** to edit task
   - Click **edit button** to edit task
   - Click **delete button** to remove task
3. **Add Task Screen** - Fill in task details
   - Task Title (required)
   - Category (choose from chips)
   - Date & Time
   - Notes
   - Click **Save** to add task

## Design Features

- **Purple Theme** (#673AB7) matching Flutter deepPurple
- **Poppins-like Font** (Segoe UI for Windows)
- **Rounded Cards** with shadows
- **Category Colors**:
  - 🏠 Home - Green
  - 🛒 Shopping - Orange
  - 💼 Work - Blue
  - 💪 Fitness - Purple
  - 📌 Other - Grey
- **Smooth Animations** and transitions
- **Responsive Icons** that change on complete

## Comparison with Flutter Version

| Feature | Flutter | PyQt5 |
|---------|---------|-------|
| Splash Screen | ✅ | ✅ |
| Phone Frame | Emulator | Fixed 390x844 |
| Purple Theme | ✅ | ✅ |
| Task CRUD | ✅ | ✅ |
| Categories | ✅ | ✅ |
| Date/Time Picker | ✅ | ✅ |
| Card Click to Edit | ✅ | ✅ |
| Icon Toggle Complete | ✅ | ✅ |

## Notes

- Tasks are stored in memory (not persisted)
- To add persistence, integrate SQLite or JSON file storage
- The frame size mimics iPhone 13 Pro dimensions
- All colors and fonts match the Flutter design

## Future Enhancements

- [ ] Data persistence (SQLite/JSON)
- [ ] Edit existing tasks
- [ ] Task filtering and search
- [ ] Notifications/reminders
- [ ] Dark mode toggle
- [ ] Export/Import tasks

---

**Created by:** CS15 Final Project Team
**Date:** October 2025
