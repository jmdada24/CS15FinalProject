# Task Storage System

## Overview

This Flutter todo app uses **local JSON file storage** for persistent, offline data management.

## How It Works

### 📂 Storage Location

Tasks are stored in a JSON file at:
- **Android**: `/data/data/com.example.todo_list/app_flutter/tasks.json`
- **iOS**: `Application Documents Directory/tasks.json`
- **Windows/Linux/macOS**: `Documents/tasks.json`

### 🔧 Architecture

```
lib/
├── services/
│   └── task_storage.dart    # Handles all file I/O operations
├── models/
│   └── task.dart            # Task model with JSON serialization
└── screens/
    └── home_screen.dart     # Loads/saves tasks automatically
```

### ⚙️ CRUD Operations

#### **Create** - Add New Task
```dart
await _storage.addTask(_tasks, newTask);
```

#### **Read** - Load All Tasks
```dart
final tasks = await _storage.loadTasks();
```

#### **Update** - Modify Task
```dart
task.title = "Updated Title";
await _storage.saveTasks(_tasks);
```

#### **Delete** - Remove Task
```dart
await _storage.deleteTask(_tasks, task);
```

## JSON Structure

```json
[
  {
    "title": "Buy groceries",
    "notes": "Milk, eggs, bread",
    "date": "2025-10-15T00:00:00.000",
    "time": {"hour": 14, "minute": 30},
    "category": "Shopping",
    "isDone": false
  },
  {
    "title": "Workout",
    "notes": "",
    "date": null,
    "time": null,
    "category": "Fitness",
    "isDone": true
  }
]
```

## Features

✅ **Automatic Persistence** - Tasks saved on every change  
✅ **Offline First** - No internet required  
✅ **Fast Loading** - Tasks load instantly on app start  
✅ **Safe Operations** - Error handling for corrupted files  
✅ **Cross-Platform** - Works on Android, iOS, Windows, macOS, Linux

## Usage

### In HomeScreen

```dart
// Load tasks when app starts
@override
void initState() {
  super.initState();
  _loadTasks();
}

Future<void> _loadTasks() async {
  final tasks = await _storage.loadTasks();
  setState(() {
    _tasks.addAll(tasks);
  });
}

// Save after any change
void _toggleDone(int index) async {
  setState(() => _tasks[index].isDone = !_tasks[index].isDone);
  await _storage.saveTasks(_tasks); // Auto-save
}
```

## Dependencies

Add to `pubspec.yaml`:

```yaml
dependencies:
  path_provider: ^2.1.1  # Access local file system
```

Then run:

```bash
flutter pub get
```

## Testing Storage

### View stored tasks file:

**Android (via ADB):**
```bash
adb shell
run-as com.example.todo_list
cat app_flutter/tasks.json
```

**iOS Simulator:**
```bash
# Find app container
xcrun simctl get_app_container booted com.example.todo_list data
# Then navigate to Documents/tasks.json
```

**Desktop:**
```bash
# Windows
C:\Users\<username>\Documents\tasks.json

# macOS/Linux
~/Documents/tasks.json
```

## Error Handling

The storage service includes error handling:
- Creates file if it doesn't exist
- Returns empty list if file is corrupted
- Logs errors to console for debugging

## Future Enhancements

- [ ] Add backup/restore functionality
- [ ] Export tasks to CSV/PDF
- [ ] Import tasks from other apps
- [ ] Cloud sync (Firebase/Supabase)
- [ ] Encryption for sensitive tasks

---

**Storage works automatically - just use the app normally and all changes are saved!** 💾✨
