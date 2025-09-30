import 'package:flutter/material.dart';
import '../models/task.dart';

String monthName(int m) {
  const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  return months[m - 1];
}

String formattedDate(DateTime date) => '${monthName(date.month)} ${date.day}, ${date.year}';

String formatTaskDateTime(Task t) {
  final parts = <String>[];
  if (t.date != null) parts.add('${monthName(t.date!.month)} ${t.date!.day}');
  if (t.time != null) {
    final h = t.time!.hourOfPeriod == 0 ? 12 : t.time!.hourOfPeriod;
    final m = t.time!.minute.toString().padLeft(2, '0');
    final ampm = t.time!.period == DayPeriod.am ? 'AM' : 'PM';
    parts.add('$h:$m $ampm');
  }
  return parts.join(' · ');
}