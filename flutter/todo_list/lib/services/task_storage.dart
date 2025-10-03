/// Task Storage Service - Folder-based JSON file persistence
/// Each task is stored as a separate JSON file in a dedicated 'tasks' folder
/// Handles Create, Read, Update, Delete operations for tasks
import 'dart:io';
import 'dart:convert';
import 'package:path_provider/path_provider.dart';
import '../models/task.dart';

class TaskStorage {
  static const String _folderName = 'tasks';
  
  /// Get the tasks folder directory
  Future<Directory> get _tasksFolder async {
    final appDocDir = await getApplicationDocumentsDirectory();
    final tasksDir = Directory('${appDocDir.path}/$_folderName');
    
    // Create the tasks folder if it doesn't exist
    if (!await tasksDir.exists()) {
      await tasksDir.create(recursive: true);
    }
    
    return tasksDir;
  }

  /// Get file path for a specific task
  Future<File> _getTaskFile(String taskId) async {
    final dir = await _tasksFolder;
    return File('${dir.path}/task_$taskId.json');
  }

  /// Load all tasks from the tasks folder
  /// Reads each JSON file and converts to Task objects
  Future<List<Task>> loadTasks() async {
    try {
      final dir = await _tasksFolder;
      final List<Task> tasks = [];
      
      // Check if folder exists
      if (!await dir.exists()) {
        return [];
      }

      // List all JSON files in the tasks folder
      final files = dir.listSync()
          .whereType<File>()
          .where((file) => file.path.endsWith('.json'))
          .toList();

      // Read each file and parse to Task
      for (final file in files) {
        try {
          final contents = await file.readAsString();
          final jsonData = json.decode(contents);
          tasks.add(Task.fromJson(jsonData));
        } catch (e) {
          print('Error loading task from ${file.path}: $e');
          // Continue loading other tasks even if one fails
        }
      }
      
      return tasks;
    } catch (e) {
      print('Error loading tasks: $e');
      return [];
    }
  }

  /// Create a new task - saves as individual JSON file
  Future<void> createTask(Task task) async {
    try {
      final file = await _getTaskFile(task.id);
      final jsonData = task.toJson();
      await file.writeAsString(json.encode(jsonData));
      print('Task created: ${file.path}');
    } catch (e) {
      print('Error creating task: $e');
    }
  }

  /// Update an existing task - overwrites the JSON file
  Future<void> updateTask(Task task) async {
    try {
      final file = await _getTaskFile(task.id);
      final jsonData = task.toJson();
      await file.writeAsString(json.encode(jsonData));
      print('Task updated: ${file.path}');
    } catch (e) {
      print('Error updating task: $e');
    }
  }

  /// Delete a task - removes the JSON file completely
  Future<void> deleteTask(String taskId) async {
    try {
      final file = await _getTaskFile(taskId);
      if (await file.exists()) {
        await file.delete();
        print('Task deleted: ${file.path}');
      }
    } catch (e) {
      print('Error deleting task: $e');
    }
  }

  /// Clear all tasks - deletes all JSON files in the tasks folder
  Future<void> clearAllTasks() async {
    try {
      final dir = await _tasksFolder;
      if (await dir.exists()) {
        final files = dir.listSync()
            .whereType<File>()
            .where((file) => file.path.endsWith('.json'))
            .toList();
        
        for (final file in files) {
          await file.delete();
        }
        print('All tasks cleared');
      }
    } catch (e) {
      print('Error clearing tasks: $e');
    }
  }

  /// Get the tasks folder path (for debugging)
  Future<String> getTasksFolderPath() async {
    final dir = await _tasksFolder;
    return dir.path;
  }
}
