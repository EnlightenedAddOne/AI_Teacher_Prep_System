from .create_sql import Todo_List,Session

# 新增任务
def write_data(session, task:str):
    task_title = Todo_List(title=task)
    session.add(task_title)
    session.commit()


# 切换任务完成状态
def turn_state(session:Session,task_id:int):
    task = session.get(Todo_List, task_id)
    if task:
        if task.done:
            task.done = False
            session.commit()
        else:
            task.done = True
            session.commit()
        return True
    else:
        return False


# 直接根据任务ID删除任务
def delete_task_by_id(session: Session, task_id: int):
    # 执行删除操作
    result = session.query(Todo_List).filter(Todo_List.id == task_id).delete()

    # 提交事务
    session.commit()

    # 根据受影响的行数判断是否删除成功
    if result > 0:
        return True
    else:
        return False

def clear_completed_tasks(session):
    result = session.query(Todo_List).filter(Todo_List.done==True)
    for task in result:
        delete_task_by_id(session, task.id)



class ToDo():
    # 当choice==1时输出已完成的任务，0：未完成的任务，其他数：所有任务
    def search_task(session: Session, choice: int):
        tasks_list = []  # 初始化一个空列表来存储任务字典

        if choice == 0:
            # 查询所有未完成的任务
            tasks = session.query(Todo_List).filter(Todo_List.done == False).all()
            for task in tasks:
                tasks_list.append({'id': task.id, 'title': task.title, 'done': task.done})
            if not tasks_list:
                print("No unfinished tasks found.")

        elif choice == 1:
            # 查询所有已完成的任务
            tasks = session.query(Todo_List).filter(Todo_List.done == True).all()
            for task in tasks:
                tasks_list.append({'id': task.id, 'title': task.title, 'done': task.done})
            if not tasks_list:
                print("No finished tasks found.")

        else:
            # 查询所有任务
            tasks = session.query(Todo_List).all()
            for task in tasks:
                tasks_list.append({'id': task.id, 'title': task.title, 'done': task.done})

        # 打印任务列表
        return tasks_list

    def done_list(session: Session):
        done_tasks = ToDo.search_task(session,1)
        return done_tasks

    def undone_list(session: Session):
        undone_tasks = ToDo.search_task(session,0)
        return undone_tasks

    def all_tasks(session: Session):
        alltasks = ToDo.search_task(session,3)
        return alltasks


# def test():
#     session = Session()
#     # write_data(session, "出门")
#     # write_data(session, "买菜做饭")
#     # write_data(session, "做饭")
#     # write_data(session, "出门做饭")
#     clear_completed_tasks(session)
#
#
# if __name__ == '__main__':
#
#     test()