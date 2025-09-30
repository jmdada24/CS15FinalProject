import 'package:flutter/material.dart';
import '../models/task.dart';
import '../utils/formatters.dart';

class TaskCard extends StatelessWidget {
  final Task task;
  final VoidCallback onToggle;
  final VoidCallback onDelete;

  const TaskCard({super.key, required this.task, required this.onToggle, required this.onDelete});

  @override
  Widget build(BuildContext context) {
    return Card(
      color: task.isDone ? Colors.grey[200] : Colors.white,
      margin: const EdgeInsets.symmetric(vertical: 6),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: ListTile(
        contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
        leading: CircleAvatar(
          backgroundColor: Theme.of(context).colorScheme.primaryContainer,
          child: _categoryIcon(task.category),
        ),
        title: Text(
          task.title,
          style: TextStyle(
            fontSize: 16,
            decoration: task.isDone ? TextDecoration.lineThrough : null,
            color: task.isDone ? Colors.grey : Colors.black87,
          ),
        ),
        subtitle: (task.date != null || task.time != null)
            ? Text(formatTaskDateTime(task), style: const TextStyle(fontSize: 12))
            : (task.notes.isNotEmpty ? Text(task.notes, maxLines: 1, overflow: TextOverflow.ellipsis) : null),
        trailing: Row(mainAxisSize: MainAxisSize.min, children: [
          IconButton(
            icon: Icon(task.isDone ? Icons.check_box : Icons.check_box_outline_blank, color: Theme.of(context).colorScheme.primary),
            onPressed: onToggle,
          ),
          IconButton(
            icon: const Icon(Icons.delete, color: Colors.redAccent),
            onPressed: onDelete,
          ),
        ]),
      ),
    );
  }

  Widget _categoryIcon(String category) {
    switch (category) {
      case 'Home':
        return const Icon(Icons.home, size: 18);
      case 'Shopping':
        return const Icon(Icons.shopping_cart, size: 18);
      case 'Work':
        return const Icon(Icons.work, size: 18);
      case 'Fitness':
        return const Icon(Icons.fitness_center, size: 18);
      default:
        return const Icon(Icons.label, size: 18);
    }
  }
}