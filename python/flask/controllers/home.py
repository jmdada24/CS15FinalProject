from flask import Blueprint, render_template, request, redirect, url_for, flash
import os
import json

home_bp = Blueprint('home', __name__)

PARENT_DIR = os.path.dirname(os.path.dirname(__file__))
filename = os.path.join(PARENT_DIR, "data", "data.json")

@home_bp.route('/')
def home():
  if os.path.exists(filename):
    with open(filename, 'r', encoding='utf-8') as file:
      try:
        data = json.load(file)
        todo_lists = data.get("todo-lists", [])
      except json.JSONDecodeError:
        todo_lists = []
  
  else:
    todo_lists = []
  
  return render_template(
    'index.html',
    title='Home',
    todo_lists=todo_lists
  )

@home_bp.route('/delete/<int:list_index>/', methods=['POST'])
def delete_list(list_index):
  
  if os.path.exists(filename):
    with open(filename, 'r+', encoding='utf-8') as file:
      try:
        data = json.load(file)
        todo_lists = data.get("todo-lists", [])
      except json.JSONDecodeError:
        todo_lists = []

      if 0 <= list_index < len(todo_lists):
        todo_lists.pop(list_index)
        data["todo-lists"] = todo_lists
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()  # ensures no leftover old data

  return redirect(url_for('home.home'))
