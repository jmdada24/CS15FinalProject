import 'package:flutter/material.dart';

class Task {
  Task({
    required this.title,
    this.notes = '',
    this.date,
    this.time,
    this.category = 'Other',
    this.isDone = false,
  });

  final String title;
  String notes;
  DateTime? date;
  TimeOfDay? time;
  String category;
  bool isDone;
}