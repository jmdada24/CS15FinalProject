class List:
  def __init__(self, name):
    self.name = name
    self.tasks = []

  def add_task(self, task):
    self.tasks.append(task)

  def remove_task(self, task):
    self.tasks.remove(task)

  def __str__(self):
    return f"""List{{
      name: {self.name}, 
      tasks: {[str(task) for task in self.tasks]}
    }}"""