class Task: 
  def __init__(self, title, description, checked=False):
    self.title = title 
    self.description = description

  def __str__(self):
    return f"""task{{
      title: {self.title}, 
      description: {self.description}
    }}"""