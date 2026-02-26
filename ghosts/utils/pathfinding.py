import heapq
import constants
from typing import Tuple, Any

def a_star(grid: list[list[int]], start: Tuple[int, int], goal: Tuple[int, int]) -> list[Tuple[int, int]]:
    """
    Реалізація алгоритму A* для пошуку найкоротшого шляху.
    Якщо ціль недосяжна, повертається шлях до найближчої точки до цільової.
    :param grid: Двовимірний список, що представляє карту (0 - прохід, 1 - стіна).
    :param start: Початкова точка (x, y).
    :param goal: Цільова точка (x, y).
    :return: Список точок [(x1, y1), (x2, y2), ...], що представляє шлях.
    """
    def heuristic(a, b):
        """Обчислення мангеттенської відстані між двома точками."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def neighbors(node):
        """Повертає сусідні клітинки для поточної клітинки."""
        x, y = node
        results = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and grid[ny][nx] == constants.TUNNEL:
                results.append((nx, ny))
        return results

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    closest_point = start  # Найближча точка до цілі
    closest_distance = heuristic(start, goal)

    while open_set:
        _, current = heapq.heappop(open_set)

        # Оновлюємо найближчу точку до цілі
        current_distance = heuristic(current, goal)
        if current_distance < closest_distance:
            closest_point = current
            closest_distance = current_distance

        # Якщо досягли цілі, будуємо шлях
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for neighbor in neighbors(current):
            tentative_g_score = g_score[current] + 1

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                if neighbor not in [item[1] for item in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    # Якщо ціль недосяжна, будуємо шлях до найближчої точки
    path = []
    current = closest_point
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path