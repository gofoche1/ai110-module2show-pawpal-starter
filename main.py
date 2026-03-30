from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    owner = Owner(name="Jordan")

    pet1 = Pet(name="StickyRice", species="dog")
    pet2 = Pet(name="Boba", species="bird")

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    # add at least 3 tasks with different durations
    task1 = Task(description="Morning walk", duration_minutes=30, frequency="daily")
    task2 = Task(description="Brush fur", duration_minutes=15, frequency="daily")
    task3 = Task(description="Vet appointment prep", duration_minutes=45, frequency="weekly")
    task4 = Task(description="Feed breakfast", duration_minutes=10, frequency="daily")  # Same time as walk

    # Assign times out of order
    task1.time = "08:00"
    task3.time = "14:00"
    task2.time = "10:00"
    task4.time = "08:00"  # Conflict with task1

    pet1.add_task(task2)  # cat task
    pet2.add_task(task1)  # dog walk
    pet2.add_task(task3)  # dog vet
    pet2.add_task(task4)  # dog feed, same time

    scheduler = Scheduler()
    schedule = scheduler.generate_owner_schedule(owner=owner, available_time=120)

    print("Today's Schedule")
    print("=================")

    if not schedule.tasks:
        print("No tasks fit under the available time yet.")
    else:
        for idx, task in enumerate(schedule.tasks, start=1):
            print(f"{idx}. {task.description} ({task.duration_minutes} min, {task.frequency}, {'Done' if task.completed else 'Pending'})")

        print(f"\nTotal scheduled time: {schedule.total_time} minutes")
        print(f"Available time: 120 minutes")

        # Sort and print by time
        sorted_tasks = scheduler.sort_by_time(schedule.tasks)
        print("\nScheduled tasks sorted by time:")
        for idx, task in enumerate(sorted_tasks, start=1):
            print(f"{idx}. {task.description} at {task.time} ({task.duration_minutes} min, {task.frequency}, {'Done' if task.completed else 'Pending'})")

        # Check for conflicts
        warning = scheduler.detect_time_conflicts(schedule.tasks)
        if warning:
            print(f"\n{warning}")
        else:
            print("\nNo time conflicts in schedule.")

    print("\nOwner tasks summary:")
    print(scheduler.summarize_owner_tasks(owner))

    # Demonstrate filtering
    print("\nFiltered tasks examples:")
    pending_tasks = scheduler.filter_tasks(owner, completion_status=False)
    print(f"Pending tasks: {[t.description for t in pending_tasks]}")
    
    mochi_tasks = scheduler.filter_tasks(owner, pet_name="Mochi")
    print(f"Mochi's tasks: {[t.description for t in mochi_tasks]}")
    
    completed_mochi = scheduler.filter_tasks(owner, completion_status=True, pet_name="Mochi")
    print(f"Mochi's completed tasks: {[t.description for t in completed_mochi]}")

    # Demonstrate marking task complete and recurrence
    print("\nMarking 'Morning walk' as complete:")
    walk_task = next((t for t in pet2.tasks if t.description == "Morning walk"), None)
    if walk_task:
        print(f"Before: {len(pet2.tasks)} tasks for Boba")
        scheduler.mark_task_complete(pet2, walk_task)
        print(f"After: {len(pet2.tasks)} tasks for Boba")
        print("New tasks:")
        for t in pet2.tasks:
            print(f"  {t}")


if __name__ == "__main__":
    main()