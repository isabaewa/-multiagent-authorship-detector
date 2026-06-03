"""
Модуль сборки CrewAI-команды для определения авторства.

Объединяет агентов и задачи в единую CrewAI-команду (crew),
которая выполняет анализ последовательно:
1. Анализатор стиля → создаёт стилистический профиль
2. Детектор авторства → сравнивает профиль с проверяемым текстом

Результат работы команды — оценка вероятности авторства с обоснованием.
"""

from crewai import Crew
from .crew_agents import style_analyzer, authorship_detector
from .crew_tasks import style_analysis_task, authorship_task

# Создание команды из двух агентов и двух задач.
# Задачи выполняются последовательно: сначала анализ стиля,
# затем определение авторства с использованием результата первой задачи.
authorship_crew = Crew(
    agents=[style_analyzer, authorship_detector],
    tasks=[style_analysis_task, authorship_task],
    verbose=True,
)