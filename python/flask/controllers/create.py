from flask import Blueprint, render_template, request, redirect, url_for, flash
import json
import os

create_bp = Blueprint('create', __name__)

@create_bp.route('/create/', methods=['GET'])
def create_list():
  return render_template(
    'create.html',
    title='Create New List'
  )

@create_bp.route('/create/', methods=['POST'])
def submit_list():
    list_name = request.form.get('list_name')
    category = request.form.get('category')
    description = request.form.get('description')

    if not list_name or not category:
      flash('List name and category are required!', 'error')
      return redirect(url_for('create.create_list'))

    new_data = {
      "list_name": list_name,
      "category": category,
      "description": description,
      "tasks": []
    }

    # 🔹 Correct directory setup
    parent_dir = os.path.dirname(os.path.dirname(__file__))
    data_folder = os.path.join(parent_dir, "data")
    os.makedirs(data_folder, exist_ok=True)

    filename = os.path.join(data_folder, "data.json")

    # 🔹 Create file if not exists
    if not os.path.exists(filename):
      with open(filename, 'w', encoding='utf-8') as file:
        json.dump({"todo-lists": [new_data]}, file, indent=4)
      flash('New list created successfully!', 'success')
      return redirect(url_for('home.home'))

    # 🔹 Otherwise append to it
    with open(filename, 'r+', encoding='utf-8') as file:
      try:
        data = json.load(file)
      except json.JSONDecodeError:
        data = {"todo-lists": []}

      data["todo-lists"].append(new_data)
      file.seek(0)
      json.dump(data, file, indent=4)
      file.truncate()

    flash('New list created successfully!', 'success')
    return redirect(url_for('home.home'))

