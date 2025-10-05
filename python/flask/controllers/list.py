from flask import Blueprint, render_template, request, redirect, url_for, flash
import os
import json

list_bp = Blueprint('list', __name__)

@list_bp.route('/list/<int:list_index>/')
def view_list(list_index):
  PARENT_DIR = os.path.dirname(os.path.dirname(__file__))
  filename = os.path.join(PARENT_DIR, "data", "data.json")

  if not os.path.exists(filename):
    flash('No lists available.', 'error')
    return redirect(url_for('home.home'))
  
  with open(filename, 'r', encoding='utf-8') as file:
    try:
      data = json.load(file)
      todo_lists = data.get("todo-lists", [])

      if 0 <= list_index < len(todo_lists):
        selected_list = todo_lists[list_index]
        return render_template(
          'list.html',
          list_index=list_index,
          list_name=selected_list.get("list_name", "List"),
          category=selected_list.get("category", "Other"),
          description=selected_list.get("description", ""),
          tasks=selected_list.get("tasks", []),
        )
      else:
        flash('List not found.', 'error')
        return redirect(url_for('home.home'))
    except json.JSONDecodeError:
      flash('Error reading data file.', 'error')
      return redirect(url_for('home.home'))
    
@list_bp.route('/list/<int:list_index>/add_task/', methods=['POST'])
def add_task(list_index):

  task = request.form.get('new_task')

  if not task:
    flash('Task name cannot be empty!', 'error')
    return redirect(url_for('list.view_list', list_index=list_index))

  PARENT_DIR = os.path.dirname(os.path.dirname(__file__))
  filename = os.path.join(PARENT_DIR, "data", "data.json")

  if not os.path.exists(filename):
    flash('No lists available.', 'error')
    return redirect(url_for('home.home'))

  with open(filename, 'r+', encoding='utf-8') as file:
    try:
      data = json.load(file)
      todo_lists = data.get("todo-lists", [])
      task = task.strip()
      new_task = {
        "task": task,
        "completed": False
      }
      if 0 <= list_index < len(todo_lists):
        todo_lists[list_index].setdefault("tasks", []).append(new_task)
        data["todo-lists"] = todo_lists
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()  # ensures no leftover old data
        flash('Task added successfully!', 'success')
      
    except json.JSONDecodeError:
      flash('Error reading data file.', 'error')

  return redirect(url_for('list.view_list', list_index=list_index))

@list_bp.route('/list/<int:list_index>/toggle_task/<int:task_index>/', methods=['POST'])
def toggle_task(list_index, task_index):
  toggle_value = request.form.get("toggle")
  is_checked = toggle_value is not None

  PARENT_DIR = os.path.dirname(os.path.dirname(__file__))
  filename = os.path.join(PARENT_DIR, "data", "data.json")

  if not os.path.exists(filename):
    flash('No lists available.', 'error')
    return redirect(url_for('home.home'))

  with open(filename, 'r+', encoding='utf-8') as file:
    try:
      data = json.load(file)
      todo_lists = data.get("todo-lists", [])

      if 0 <= list_index < len(todo_lists):
        tasks = todo_lists[list_index].get("tasks", [])
        if 0 <= task_index < len(tasks):
          tasks[task_index]["completed"] = is_checked
          data["todo-lists"] = todo_lists
          file.seek(0)
          json.dump(data, file, indent=4)
          file.truncate()  # ensures no leftover old data
          flash('Task status updated!', 'success')
        else:
          flash('Task not found.', 'error')
      else:
        flash('List not found.', 'error')

    except json.JSONDecodeError:
      flash('Error reading data file.', 'error')

  return redirect(url_for('list.view_list', list_index=list_index))

@list_bp.route('/list/<int:list_index>/delete_task/<int:task_index>/', methods=['POST'])
def delete_task(list_index, task_index):
  PARENT_DIR = os.path.dirname(os.path.dirname(__file__))
  filename = os.path.join(PARENT_DIR, "data", "data.json")

  if not os.path.exists(filename):
    flash('No lists available.', 'error')
    return redirect(url_for('home.home'))

  with open(filename, 'r+', encoding='utf-8') as file:
    try:
      data = json.load(file)
      todo_lists = data.get("todo-lists", [])

      if 0 <= list_index < len(todo_lists):
        tasks = todo_lists[list_index].get("tasks", [])
        if 0 <= task_index < len(tasks):
          tasks.pop(task_index)
          data["todo-lists"] = todo_lists
          file.seek(0)
          json.dump(data, file, indent=4)
          file.truncate()  # ensures no leftover old data
          flash('Task deleted successfully!', 'success')
        else:
          flash('Task not found.', 'error')
      else:
        flash('List not found.', 'error')

    except json.JSONDecodeError:
      flash('Error reading data file.', 'error')

  return redirect(url_for('list.view_list', list_index=list_index))