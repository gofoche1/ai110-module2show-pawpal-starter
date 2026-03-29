from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    owner = Owner(name="Jordan")

    pet1 = Pet(name="Mochi", species="dog")
    pet2 = Pet(name="Boba", species="cat")

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    # add at least 3 tasks with different durations
    task1 = Task(description="Morning walk", duration_minutes=30, frequency="daily")
    task2 = Task(description="Brush fur", duration_minutes=15, frequency="daily")
    task3 = Task(description="Vet appointment prep", duration_minutes=45, frequency="weekly")

    pet1.add_task(task2)  # cat task
    pet2.add_task(task1)  # dog walk
    pet2.add_task(task3)  # dog vet

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

    print("\nOwner tasks summary:")
    print(scheduler.summarize_owner_tasks(owner))


if __name__ == "__main__":
    main()