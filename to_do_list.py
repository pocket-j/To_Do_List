# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return f'{self.id}. {self.task}'


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
rows = session.query(Table.id, Table.task, Table.deadline).all()


def display():
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")


def missed_tasks():
    print("Missed tasks:")
    today = datetime.today()
    missed_rows = session.query(Table.id, Table.task, Table.deadline).filter(Table.deadline < today.date()).all()
    if len(missed_rows) == 0:
        print("Nothing is missed!")
    else:
        count = 1
        for i in missed_rows:
            print(f'{count}. {i.task}. {i.deadline.strftime("%#d %b")}')
            count += 1
    print()


def delete_tasks():
    print("Choose the number of the task you want to delete:")
    all_rows = session.query(Table.id, Table.task, Table.deadline).order_by(Table.deadline).all()
    if len(all_rows) == 0:
        print("Nothing to do!")
    else:
        count = 1
        for i in all_rows:
            print(f'{count}. {i.task}. {i.deadline.strftime("%#d %b")} ')
            count += 1
        number = int(input())
        specific_row = all_rows[number - 1]
        session.query(Table).filter(Table.id == specific_row[0]).delete()
        session.commit()
        print("The task has been deleted!")


def current_tasks():
    today = datetime.today()
    current_rows = session.query(Table).filter(Table.deadline == today.date()).all()
    print(f'Today {today.day} {today.strftime("%b")}:')
    if len(current_rows) == 0:
        print("Nothing to do!")
    else:
        count = 1
        for i in current_rows:
            print(f'{count}. {i.task}')
            count += 1


def week_tasks():
    today = datetime.today().date()
    for i in range(0, 7):
        i_day = today + timedelta(days=i)
        i_rows = session.query(Table.id, Table.task, Table.deadline).filter(Table.deadline == i_day).order_by(
            Table.deadline).all()
        print(f'{i_day.strftime("%A")} {i_day.day} {i_day.strftime("%b")}')
        if len(i_rows) == 0:
            print("Nothing to do!")
        else:
            count = 1
            for j in i_rows:
                print(f'{count}. {j.task}')
                count += 1
        print()


def all_tasks():
    print("All tasks:")
    all_rows = session.query(Table.id, Table.task, Table.deadline).order_by(Table.deadline).all()
    if len(all_rows) == 0:
        print("Nothing to do!")
    else:
        count = 1
        for i in all_rows:
            print(f'{count}. {i.task}. {i.deadline.strftime("%#d %b")} ')
            count += 1


def add_tasks():
    print("Enter task")
    task_input = input()
    print("Enter deadline")
    task_date = input()
    date_string = datetime.strptime(task_date, "%Y-%m-%d")
    new_row = Table(task=task_input,
                    deadline=date_string)
    session.add(new_row)
    session.commit()
    print("The task has been added!")


while True:
    display()
    user_input = int(input())
    if user_input == 0:
        print("Bye")
        break
    elif user_input == 1:
        current_tasks()
    elif user_input == 2:
        week_tasks()
    elif user_input == 3:
        all_tasks()
    elif user_input == 4:
        missed_tasks()
    elif user_input == 5:
        add_tasks()
    elif user_input == 6:
        delete_tasks()
