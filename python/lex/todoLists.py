class TodoLists:
  def __init__(self):
      self.lists = []  # List to hold multiple lists

  def add_list(self, todo_list):
      self.lists.append(todo_list)

  def remove_list(self, todo_list):
      self.lists.remove(todo_list)

  def get_lists(self):
      return self.lists