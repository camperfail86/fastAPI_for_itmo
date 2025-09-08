from classes import Project, Task, Developer
from typing import List

# Созданная для примера работы база данных
project1 = Project(name = "Интернет-магазин", id = 1000, start_date = "04.09")
task1 = Task(name = "Создание базы данных",  id = 100, difficulty = 4, deadline = "30.09")
task2 = Task(name = "Создание сайта", id = 101, difficulty = 2, deadline = "15.09")
dev1 = Developer(name = "Василий Петрович", task = task1, id = 1, skill = 8, age = 29)
dev2 = Developer(name = "Антон Азаркин", task = task1, id = 2, skill = 7, age = 25)
dev3 = Developer(name = "Кочкин Кирилл", task = task2, id = 3, skill = 5, age = 22)
Projects: List[Project] = [project1]
Tasks: List[Task] = [task1, task2]
Developers: List[Developer] = [dev1, dev2, dev3]