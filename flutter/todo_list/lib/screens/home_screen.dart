import 'package:flutter/material.dart';
import '../models/task.dart';
import '../utils/formatters.dart';
import '../widgets/task_card.dart';
import 'add_task_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});
  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final List<Task> _tasks = [];

  Future<void> _openAddTask() async {
    final Task? newTask = await Navigator.of(context).push<Task>(
      PageRouteBuilder(
        pageBuilder: (context, animation, secondaryAnimation) => const AddTaskScreen(),
        transitionsBuilder: (context, animation, secondaryAnimation, child) {
          final curved = CurvedAnimation(parent: animation, curve: Curves.easeInOut);
          final slide = Tween<Offset>(begin: const Offset(1.0, 0.0), end: Offset.zero).animate(curved);
          final fade = Tween<double>(begin: 0.0, end: 1.0).animate(curved);
          return SlideTransition(position: slide, child: FadeTransition(opacity: fade, child: child));
        },
        transitionDuration: const Duration(milliseconds: 300),
      ),
    );
    if (newTask != null) setState(() => _tasks.insert(0, newTask));
  }

  void _toggleDone(int index) => setState(() => _tasks[index].isDone = !_tasks[index].isDone);
  void _removeTask(int index) => setState(() => _tasks.removeAt(index));

  @override
  Widget build(BuildContext context) {
    final pending = _tasks.where((t) => !t.isDone).toList();
    final completed = _tasks.where((t) => t.isDone).toList();

    return Scaffold(
      backgroundColor: Colors.grey[100],
      body: SafeArea(
        child: Column(children: [
          Container(
            padding: const EdgeInsets.fromLTRB(20, 24, 20, 28),
            width: double.infinity,
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.primary,
              borderRadius: const BorderRadius.vertical(bottom: Radius.circular(18)),
            ),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text(formattedDate(DateTime.now()), style: const TextStyle(color: Colors.white70, fontSize: 14)),
              const SizedBox(height: 8),
              const Text('My Todo List', style: TextStyle(color: Colors.white, fontSize: 26, fontWeight: FontWeight.bold)),
            ]),
          ),
          Expanded(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              child: _tasks.isEmpty
                  ? Center(
                      child: Column(mainAxisSize: MainAxisSize.min, children: [
                        Icon(Icons.task_alt, size: 64, color: Theme.of(context).colorScheme.primary),
                        const SizedBox(height: 12),
                        const Text('No tasks yet', style: TextStyle(fontSize: 18)),
                        const SizedBox(height: 8),
                        TextButton(onPressed: _openAddTask, child: const Text('Add your first task'))
                      ]),
                    )
                  : ListView(children: [
                      if (pending.isNotEmpty) ...[
                        const Padding(padding: EdgeInsets.only(bottom: 8), child: Text('Tasks', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold))),
                        ...List.generate(pending.length, (i) {
                          final task = pending[i];
                          final idx = _tasks.indexOf(task);
                          return TaskCard(task: task, onToggle: () => _toggleDone(idx), onDelete: () => _removeTask(idx));
                        }),
                        const SizedBox(height: 12),
                      ],
                      if (completed.isNotEmpty) ...[
                        const Padding(padding: EdgeInsets.only(bottom: 8), child: Text('Completed', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold))),
                        ...List.generate(completed.length, (i) {
                          final task = completed[i];
                          final idx = _tasks.indexOf(task);
                          return TaskCard(task: task, onToggle: () => _toggleDone(idx), onDelete: () => _removeTask(idx));
                        }),
                      ],
                      const SizedBox(height: 80),
                    ]),
            ),
          ),
        ]),
      ),
        bottomSheet: SafeArea(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            child: SizedBox(
              width: double.infinity,
              height: 52,
              child: ElevatedButton(
                onPressed: _openAddTask,
                style: ElevatedButton.styleFrom(
                  shape: const StadiumBorder(),
                  backgroundColor: Theme.of(context).colorScheme.primary,
                  elevation: 4,
                ),
                child: const Text('Add New Task', style: TextStyle(fontSize: 16, color: Colors.white)),
              ),
            ),
          ),
        ),
    );
  }
}