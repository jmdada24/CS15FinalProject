import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../models/task.dart';
import '../utils/formatters.dart';

class TaskCard extends StatefulWidget {
  final Task task;
  final VoidCallback onToggle;
  final VoidCallback onDelete;
  final VoidCallback onEdit;

  const TaskCard({
    super.key,
    required this.task,
    required this.onToggle,
    required this.onDelete,
    required this.onEdit,
  });

  @override
  State<TaskCard> createState() => _TaskCardState();
}

class _TaskCardState extends State<TaskCard> with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  bool _isExpanded = false;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 200),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _toggleExpand() {
    setState(() {
      _isExpanded = !_isExpanded;
      if (_isExpanded) {
        _controller.forward();
      } else {
        _controller.reverse();
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final seed = Theme.of(context).colorScheme.primary;
    final isDone = widget.task.isDone;
    final hasNotes = widget.task.notes.isNotEmpty;

    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      decoration: BoxDecoration(
        color: isDone ? Colors.grey.shade50 : Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: isDone ? Colors.black.withOpacity(0.03) : Colors.black.withOpacity(0.06),
            blurRadius: 12,
            offset: const Offset(0, 4),
          ),
        ],
        border: Border.all(
          color: isDone ? Colors.grey.shade200 : Colors.grey.shade100,
          width: 1.5,
        ),
      ),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          onTap: widget.onEdit,
          borderRadius: BorderRadius.circular(20),
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              children: [
                Row(
                  children: [
                    _buildCategoryIcon(seed, isDone),
                    const SizedBox(width: 14),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            widget.task.title,
                            style: GoogleFonts.poppins(
                              fontSize: 16,
                              fontWeight: FontWeight.w600,
                              color: isDone ? Colors.grey.shade500 : Colors.black87,
                              decoration: isDone ? TextDecoration.lineThrough : null,
                            ),
                          ),
                          if (widget.task.date != null || widget.task.time != null) ...[
                            const SizedBox(height: 4),
                            Row(
                              children: [
                                Icon(
                                  Icons.schedule_rounded,
                                  size: 14,
                                  color: isDone ? Colors.grey.shade400 : seed,
                                ),
                                const SizedBox(width: 4),
                                Text(
                                  formatTaskDateTime(widget.task),
                                  style: GoogleFonts.poppins(
                                    fontSize: 12,
                                    color: isDone ? Colors.grey.shade400 : Colors.black54,
                                    fontWeight: FontWeight.w500,
                                  ),
                                ),
                              ],
                            ),
                          ],
                        ],
                      ),
                    ),
                    const SizedBox(width: 8),
                    _buildActionButtons(seed, isDone, hasNotes),
                  ],
                ),
                if (hasNotes)
                  AnimatedSize(
                    duration: const Duration(milliseconds: 200),
                    curve: Curves.easeInOut,
                    child: _isExpanded
                        ? Column(
                            children: [
                              const SizedBox(height: 12),
                              Container(
                                width: double.infinity,
                                padding: const EdgeInsets.all(12),
                                decoration: BoxDecoration(
                                  color: seed.withOpacity(0.05),
                                  borderRadius: BorderRadius.circular(12),
                                ),
                                child: Text(
                                  widget.task.notes,
                                  style: GoogleFonts.poppins(
                                    fontSize: 13,
                                    color: Colors.black87,
                                    height: 1.5,
                                  ),
                                ),
                              ),
                            ],
                          )
                        : const SizedBox.shrink(),
                  ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildCategoryIcon(Color seed, bool isDone) {
    final icon = _getCategoryIcon();
    final bgColor = isDone ? Colors.grey.shade200 : _getCategoryColor().withOpacity(0.15);
    final iconColor = isDone ? Colors.grey.shade400 : _getCategoryColor();

    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: bgColor,
        borderRadius: BorderRadius.circular(14),
      ),
      child: Icon(icon, size: 22, color: iconColor),
    );
  }

  Widget _buildActionButtons(Color seed, bool isDone, bool hasNotes) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        IconButton(
          icon: Container(
            padding: const EdgeInsets.all(6),
            decoration: BoxDecoration(
              color: seed.withOpacity(0.1),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Icon(
              Icons.edit_rounded,
              color: seed,
              size: 20,
            ),
          ),
          onPressed: widget.onEdit,
          padding: EdgeInsets.zero,
          constraints: const BoxConstraints(),
          tooltip: 'Edit Task',
        ),
        const SizedBox(width: 4),
        IconButton(
          icon: AnimatedContainer(
            duration: const Duration(milliseconds: 200),
            padding: const EdgeInsets.all(6),
            decoration: BoxDecoration(
              color: isDone ? Colors.green.withOpacity(0.15) : seed.withOpacity(0.1),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Icon(
              isDone ? Icons.check_circle_rounded : Icons.circle_outlined,
              color: isDone ? Colors.green : seed,
              size: 20,
            ),
          ),
          onPressed: widget.onToggle,
          padding: EdgeInsets.zero,
          constraints: const BoxConstraints(),
        ),
        const SizedBox(width: 8),
        IconButton(
          icon: Container(
            padding: const EdgeInsets.all(6),
            decoration: BoxDecoration(
              color: Colors.red.withOpacity(0.1),
              borderRadius: BorderRadius.circular(8),
            ),
            child: const Icon(
              Icons.delete_rounded,
              color: Colors.redAccent,
              size: 20,
            ),
          ),
          onPressed: () {
            showDialog(
              context: context,
              builder: (context) => AlertDialog(
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(20),
                ),
                title: Text(
                  'Delete Task',
                  style: GoogleFonts.poppins(fontWeight: FontWeight.w600),
                ),
                content: Text(
                  'Are you sure you want to delete this task?',
                  style: GoogleFonts.poppins(),
                ),
                actions: [
                  TextButton(
                    onPressed: () => Navigator.pop(context),
                    child: Text(
                      'Cancel',
                      style: GoogleFonts.poppins(color: Colors.grey),
                    ),
                  ),
                  ElevatedButton(
                    onPressed: () {
                      Navigator.pop(context);
                      widget.onDelete();
                    },
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.redAccent,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                    ),
                    child: Text(
                      'Delete',
                      style: GoogleFonts.poppins(color: Colors.white),
                    ),
                  ),
                ],
              ),
            );
          },
          padding: EdgeInsets.zero,
          constraints: const BoxConstraints(),
        ),
      ],
    );
  }

  IconData _getCategoryIcon() {
    switch (widget.task.category) {
      case 'Home':
        return Icons.home_rounded;
      case 'Shopping':
        return Icons.shopping_cart_rounded;
      case 'Work':
        return Icons.work_rounded;
      case 'Fitness':
        return Icons.fitness_center_rounded;
      default:
        return Icons.label_rounded;
    }
  }

  Color _getCategoryColor() {
    switch (widget.task.category) {
      case 'Home':
        return Colors.green;
      case 'Shopping':
        return Colors.orange;
      case 'Work':
        return Colors.blue;
      case 'Fitness':
        return Colors.purple;
      default:
        return Colors.grey;
    }
  }
}