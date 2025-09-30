import 'package:flutter/material.dart';
import '../models/task.dart';
import '../utils/formatters.dart';
import '../widgets/task_card.dart';
import 'add_task_screen.dart';
import 'edit_task_screen.dart';
import 'package:google_fonts/google_fonts.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});
  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> with TickerProviderStateMixin {
  final List<Task> _tasks = [];
  late AnimationController _fabController;

  @override
  void initState() {
    super.initState();
    _fabController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 200),
    );
  }

  @override
  void dispose() {
    _fabController.dispose();
    super.dispose();
  }

  Future<void> _openAddTask() async {
    final Task? newTask = await Navigator.of(context).push<Task>(
      PageRouteBuilder(
        pageBuilder: (context, animation, secondaryAnimation) => const AddTaskScreen(),
        transitionsBuilder: (context, animation, secondaryAnimation, child) {
          final curved = CurvedAnimation(parent: animation, curve: Curves.easeOutCubic);
          final slide = Tween<Offset>(begin: const Offset(0.0, 1.0), end: Offset.zero).animate(curved);
          final fade = Tween<double>(begin: 0.0, end: 1.0).animate(curved);
          return SlideTransition(position: slide, child: FadeTransition(opacity: fade, child: child));
        },
        transitionDuration: const Duration(milliseconds: 400),
      ),
    );
    if (newTask != null) {
      setState(() => _tasks.insert(0, newTask));
    }
  }

  void _toggleDone(int index) => setState(() => _tasks[index].isDone = !_tasks[index].isDone);
  void _removeTask(int index) => setState(() => _tasks.removeAt(index));

  Future<void> _editTask(int index) async {
    final task = _tasks[index];
    final result = await Navigator.of(context).push<bool>(
      PageRouteBuilder(
        pageBuilder: (context, animation, secondaryAnimation) => EditTaskScreen(task: task),
        transitionsBuilder: (context, animation, secondaryAnimation, child) {
          final curved = CurvedAnimation(parent: animation, curve: Curves.easeOutCubic);
          final slide = Tween<Offset>(begin: const Offset(0.0, 1.0), end: Offset.zero).animate(curved);
          final fade = Tween<double>(begin: 0.0, end: 1.0).animate(curved);
          return SlideTransition(position: slide, child: FadeTransition(opacity: fade, child: child));
        },
        transitionDuration: const Duration(milliseconds: 400),
      ),
    );
    if (result == true) setState(() {}); // Refresh UI after edit
  }

  @override
  Widget build(BuildContext context) {
    final pending = _tasks.where((t) => !t.isDone).toList();
    final completed = _tasks.where((t) => t.isDone).toList();
    final totalTasks = _tasks.length;
    final completedCount = completed.length;

    return Scaffold(
      backgroundColor: const Color(0xFFF8F9FA),
      body: SafeArea(
        child: Column(children: [
          _buildHeader(context, totalTasks, completedCount),
          Expanded(
            child: _tasks.isEmpty
                ? _buildEmptyState(context)
                : _buildTaskList(pending, completed),
          ),
        ]),
      ),
      floatingActionButton: ScaleTransition(
        scale: Tween<double>(begin: 0.0, end: 1.0).animate(
          CurvedAnimation(parent: _fabController, curve: Curves.easeOutBack),
        ),
        child: FloatingActionButton.extended(
          onPressed: _openAddTask,
          backgroundColor: Theme.of(context).colorScheme.primary,
          elevation: 8,
          icon: const Icon(Icons.add, color: Colors.white),
          label: Text(
            'New Task',
            style: GoogleFonts.poppins(
              color: Colors.white,
              fontSize: 16,
              fontWeight: FontWeight.w600,
            ),
          ),
        ),
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
    );
  }

  Widget _buildHeader(BuildContext context, int total, int completed) {
    return Container(
      padding: const EdgeInsets.fromLTRB(24, 20, 24, 32),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [
            Theme.of(context).colorScheme.primary,
            Theme.of(context).colorScheme.primary.withOpacity(0.8),
          ],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: const BorderRadius.vertical(bottom: Radius.circular(32)),
        boxShadow: [
          BoxShadow(
            color: Theme.of(context).colorScheme.primary.withOpacity(0.3),
            blurRadius: 20,
            offset: const Offset(0, 10),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                formattedDate(DateTime.now()),
                style: GoogleFonts.poppins(
                  color: Colors.white.withOpacity(0.9),
                  fontSize: 14,
                  fontWeight: FontWeight.w400,
                ),
              ),
              if (total > 0)
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.2),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Text(
                    '$completed/$total',
                    style: GoogleFonts.poppins(
                      color: Colors.white,
                      fontSize: 13,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
            ],
          ),
          const SizedBox(height: 16),
          Text(
            'My Tasks',
            style: GoogleFonts.poppins(
              color: Colors.white,
              fontSize: 32,
              fontWeight: FontWeight.w700,
              letterSpacing: -0.5,
            ),
          ),
          if (total > 0) ...[
            const SizedBox(height: 12),
            ClipRRect(
              borderRadius: BorderRadius.circular(8),
              child: LinearProgressIndicator(
                value: total > 0 ? completed / total : 0,
                backgroundColor: Colors.white.withOpacity(0.3),
                valueColor: const AlwaysStoppedAnimation<Color>(Colors.white),
                minHeight: 6,
              ),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildEmptyState(BuildContext context) {
    _fabController.forward();
    return Center(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(
            padding: const EdgeInsets.all(32),
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.primary.withOpacity(0.1),
              shape: BoxShape.circle,
            ),
            child: Icon(
              Icons.task_alt_rounded,
              size: 80,
              color: Theme.of(context).colorScheme.primary,
            ),
          ),
          const SizedBox(height: 24),
          Text(
            'No tasks yet',
            style: GoogleFonts.poppins(
              fontSize: 24,
              fontWeight: FontWeight.w600,
              color: Colors.black87,
            ),
          ),
          const SizedBox(height: 8),
          Text(
            'Tap the button below to add your first task',
            style: GoogleFonts.poppins(
              fontSize: 14,
              color: Colors.black54,
            ),
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }

  Widget _buildTaskList(List<Task> pending, List<Task> completed) {
    _fabController.forward();
    return ListView(
      padding: const EdgeInsets.fromLTRB(20, 20, 20, 100),
      children: [
        if (pending.isNotEmpty) ...[
          _buildSectionHeader('Active Tasks', pending.length, Colors.blue),
          const SizedBox(height: 12),
          ...List.generate(pending.length, (i) {
            final task = pending[i];
            final idx = _tasks.indexOf(task);
                            return TweenAnimationBuilder<double>(
              tween: Tween(begin: 0.0, end: 1.0),
              duration: Duration(milliseconds: 300 + (i * 50)),
              curve: Curves.easeOutCubic,
              builder: (context, value, child) {
                return Transform.translate(
                  offset: Offset(0, 20 * (1 - value)),
                  child: Opacity(
                    opacity: value,
                    child: child,
                  ),
                );
              },
              child: TaskCard(
                task: task,
                onToggle: () => _toggleDone(idx),
                onDelete: () => _removeTask(idx),
                onEdit: () => _editTask(idx),
              ),
            );
          }),
          const SizedBox(height: 24),
        ],
        if (completed.isNotEmpty) ...[
          _buildSectionHeader('Completed', completed.length, Colors.green),
          const SizedBox(height: 12),
          ...List.generate(completed.length, (i) {
            final task = completed[i];
            final idx = _tasks.indexOf(task);
            return TaskCard(
              task: task,
              onToggle: () => _toggleDone(idx),
              onDelete: () => _removeTask(idx),
              onEdit: () => _editTask(idx),
            );
          }),
        ],
      ],
    );
  }

  Widget _buildSectionHeader(String title, int count, Color accentColor) {
    return Row(
      children: [
        Container(
          width: 4,
          height: 20,
          decoration: BoxDecoration(
            color: accentColor,
            borderRadius: BorderRadius.circular(2),
          ),
        ),
        const SizedBox(width: 12),
        Text(
          title,
          style: GoogleFonts.poppins(
            fontSize: 18,
            fontWeight: FontWeight.w700,
            color: Colors.black87,
          ),
        ),
        const SizedBox(width: 8),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
          decoration: BoxDecoration(
            color: accentColor.withOpacity(0.15),
            borderRadius: BorderRadius.circular(12),
          ),
          child: Text(
            count.toString(),
            style: GoogleFonts.poppins(
              fontSize: 12,
              fontWeight: FontWeight.w600,
              color: accentColor,
            ),
          ),
        ),
      ],
    );
  }
}