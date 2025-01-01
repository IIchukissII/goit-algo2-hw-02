from typing import List, Dict
from dataclasses import dataclass

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int

def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера

    Args:
        print_jobs: Список завдань на друк
        constraints: Обмеження принтера

    Returns:
        Dict з порядком друку та загальним часом
    """
    # Перетворення вхідних даних на об'єкти PrintJob
    jobs = [PrintJob(**job) for job in print_jobs]

    # Сортування завдань за пріоритетом (1 - найвищий), а потім за часом друку
    jobs.sort(key=lambda job: (job.priority, job.print_time))

    max_volume = constraints["max_volume"]
    max_items = constraints["max_items"]

    print_order = []
    total_time = 0
    
    while jobs:
        current_volume = 0
        current_items = 0
        batch = []

        for job in jobs[:]:
            if (current_volume + job.volume <= max_volume) and (current_items + 1 <= max_items):
                batch.append(job)
                current_volume += job.volume
                current_items += 1

        # Якщо немає доступних завдань для друку в поточному циклі, завершити
        if not batch:
            break

        # Розрахунок часу для поточного батчу як максимальний час серед завдань у групі
        batch_time = max(job.print_time for job in batch)
        total_time += batch_time

        # Додати ID завдань до порядку друку
        print_order.extend(job.id for job in batch)

        # Видалити оброблені завдання з черги
        jobs = [job for job in jobs if job not in batch]

    return {
        "print_order": print_order,
        "total_time": total_time
    }

# Тестування
def test_printing_optimization():
    test_cases = [
        {
            "name": "Тест 1 (однаковий пріоритет)",
            "jobs": [
                {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
                {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
                {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
            ]
        },
        {
            "name": "Тест 2 (різні пріоритети)",
            "jobs": [
                {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},
                {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
                {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}
            ]
        },
        {
            "name": "Тест 3 (перевищення обмежень)",
            "jobs": [
                {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
                {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
                {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
            ]
        }
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    for test in test_cases:
        print(f"{test['name']}:")
        result = optimize_printing(test["jobs"], constraints)
        print(f"Порядок друку: {result['print_order']}")
        print(f"Загальний час: {result['total_time']} хвилин\n")


if __name__ == "__main__":
    test_printing_optimization()
