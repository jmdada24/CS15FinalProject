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

class _TaskCardState extends State<TaskCard> {
  @override
  Widget build(BuildContext context) {
    final seed = Theme.of(context).colorScheme.primary;
    final isDone = widget.task.isDone;

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
          onTap: widget.onEdit, // Clicking anywhere on card opens edit screen
          borderRadius: BorderRadius.circular(20),
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Row(
              children: [
                // Category icon - CLICKABLE to toggle completion (stops propagation)
                GestureDetector(
                  onTap: () {
                    widget.onToggle(); // Only toggle, don't open edit
                  },
                  child: _buildCategoryIcon(seed, isDone),
                ),
                const SizedBox(width: 14),
                
                // Task title and subtitle
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
                
                const SizedBox(width: 12),
                
                // Action buttons: Edit and Delete ONLY
                Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    // Edit button (explicitly shown for clarity)
                    GestureDetector(
                      onTap: widget.onEdit, // Redundant but clear
                      child: Container(
                        padding: const EdgeInsets.all(8),
                        decoration: BoxDecoration(
                          color: seed.withOpacity(0.1),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Icon(
                          Icons.edit_rounded,
                          color: seed,
                          size: 24,
                        ),
                      ),
                    ),
                    const SizedBox(width: 8),
                    
                    // Delete button (stops propagation to prevent opening edit)
                    GestureDetector(
                      onTap: () {
                        showDialog(
                          context: context,
                          builder: (ctx) => AlertDialog(
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
                            title: Text('Delete Task', style: GoogleFonts.poppins(fontWeight: FontWeight.w600)),
                            content: Text('Are you sure?', style: GoogleFonts.poppins()),
                            actions: [
                              TextButton(
                                onPressed: () => Navigator.pop(ctx),
                                child: Text('Cancel', style: GoogleFonts.poppins(color: Colors.grey)),
                              ),
                              ElevatedButton(
                                onPressed: () {
                                  Navigator.pop(ctx);
                                  widget.onDelete();
                                },
                                style: ElevatedButton.styleFrom(
                                  backgroundColor: Colors.redAccent,
                                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                                ),
                                child: Text('Delete', style: GoogleFonts.poppins(color: Colors.white)),
                              ),
                            ],
                          ),
                        );
                      },
                      child: Container(
                        padding: const EdgeInsets.all(8),
                        decoration: BoxDecoration(
                          color: Colors.red.withOpacity(0.1),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: const Icon(
                          Icons.delete_rounded,
                          color: Colors.redAccent,
                          size: 24,
                        ),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildCategoryIcon(Color seed, bool isDone) {
    // If completed, show green checkmark. Otherwise show category icon.
    final IconData icon = isDone ? Icons.check_circle_rounded : _getCategoryIcon();
    final Color bgColor = isDone ? Colors.green.withOpacity(0.15) : _getCategoryColor().withOpacity(0.15);
    final Color iconColor = isDone ? Colors.green : _getCategoryColor();

    return AnimatedContainer(
      duration: const Duration(milliseconds: 300),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: bgColor,
        borderRadius: BorderRadius.circular(14),
      ),
      child: Icon(icon, size: 22, color: iconColor),
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