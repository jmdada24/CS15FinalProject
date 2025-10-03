import 'package:flutter/material.dart';
import 'package:uuid/uuid.dart';

class Task {
  Task({
    String? id,
    required this.title,
    this.notes = '',
    this.date,
    this.time,
    this.category = 'Other',
    this.isDone = false,
  }) : id = id ?? const Uuid().v4();

  final String id;
  String title;
  String notes;
  DateTime? date;
  TimeOfDay? time;
  String category;
  bool isDone;

  /// Convert Task to JSON (for storage)
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'notes': notes,
      'date': date?.toIso8601String(),
      'time': time != null ? {'hour': time!.hour, 'minute': time!.minute} : null,
      'category': category,
      'isDone': isDone,
    };
  }

  /// Create Task from JSON (for loading)
  factory Task.fromJson(Map<String, dynamic> json) {
    TimeOfDay? timeOfDay;
    if (json['time'] != null) {
      final timeMap = json['time'] as Map<String, dynamic>;
      timeOfDay = TimeOfDay(hour: timeMap['hour'], minute: timeMap['minute']);
    }

    return Task(
      id: json['id'],
      title: json['title'] ?? '',
      notes: json['notes'] ?? '',
      date: json['date'] != null ? DateTime.parse(json['date']) : null,
      time: timeOfDay,
      category: json['category'] ?? 'Other',
      isDone: json['isDone'] ?? false,
    );
  }
}