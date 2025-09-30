import 'package:flutter/material.dart';
import '../models/task.dart';
import '../utils/formatters.dart';

class AddTaskScreen extends StatefulWidget {
  const AddTaskScreen({super.key});
  @override
  State<AddTaskScreen> createState() => _AddTaskScreenState();
}

class _AddTaskScreenState extends State<AddTaskScreen> {
  final _titleController = TextEditingController();
  final _notesController = TextEditingController();
  DateTime? _date;
  TimeOfDay? _time;
  String _category = 'Other';
  final List<String> _categories = ['Other', 'Home', 'Shopping', 'Work', 'Fitness'];

  Future<void> _pickDate() async {
    final now = DateTime.now();
    final picked = await showDatePicker(context: context, initialDate: now, firstDate: now.subtract(const Duration(days: 365)), lastDate: now.add(const Duration(days: 365)));
    if (picked != null) setState(() => _date = picked);
  }

  Future<void> _pickTime() async {
    final picked = await showTimePicker(context: context, initialTime: TimeOfDay.now());
    if (picked != null) setState(() => _time = picked);
  }

  void _save() {
    final title = _titleController.text.trim();
    if (title.isEmpty) return;
    final task = Task(title: title, notes: _notesController.text.trim(), date: _date, time: _time, category: _category);
    Navigator.of(context).pop(task);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
          appBar: AppBar(
          title: const Text('Add New Task', style: TextStyle(fontSize: 18, color: Colors.white)),
          backgroundColor: Theme.of(context).colorScheme.primary,
          iconTheme: const IconThemeData(color: Colors.white),
          foregroundColor: Colors.white, // <-- ensures back arrow and text are white
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(children: [
          TextField(
            controller: _titleController,
            decoration: const InputDecoration(labelText: 'Task Title', border: OutlineInputBorder()),
          ),
          const SizedBox(height: 12),
          SizedBox(
            height: 42,
            child: ListView.separated(
              scrollDirection: Axis.horizontal,
              itemCount: _categories.length,
              separatorBuilder: (_, __) => const SizedBox(width: 8),
              itemBuilder: (context, i) {
                final cat = _categories[i];
                final selected = cat == _category;
                return ChoiceChip(
                  label: Text(cat),
                  selected: selected,
                  onSelected: (_) => setState(() => _category = cat),
                );
              },
            ),
          ),
          const SizedBox(height: 12),
          Row(children: [
            Expanded(
              child: OutlinedButton.icon(
                onPressed: _pickDate,
                icon: const Icon(Icons.calendar_today),
                label: Text(_date == null ? 'Date' : formattedDate(_date!)),
              ),
            ),
            const SizedBox(width: 8),
            Expanded(
              child: OutlinedButton.icon(
                onPressed: _pickTime,
                icon: const Icon(Icons.access_time),
                label: Text(_time == null ? 'Time' : _time!.format(context)),
              ),
            ),
          ]),
          const SizedBox(height: 12),
          Expanded(
            child: TextField(
              controller: _notesController,
              decoration: const InputDecoration(border: OutlineInputBorder(), labelText: 'Notes'),
              maxLines: null,
              expands: true,
            ),
          ),
          const SizedBox(height: 12),
          SizedBox(
          width: double.infinity,
          height: 48,
          child: ElevatedButton(
            onPressed: _save,
            style: ElevatedButton.styleFrom(
              shape: const StadiumBorder(),
              backgroundColor: Theme.of(context).colorScheme.primary, // purple background
              elevation: 2,
            ),
            child: const Text(
              'Save',
              style: TextStyle(color: Colors.white, fontSize: 16), // white text
            ),
          ),
        ),
        ]),
      ),
    );
  }
}