def calculate_level(xp: int) -> int:
    level = 1
    required = 1000  # на 1 уровень
    while xp >= required:
        level += 1
        xp -= required
        required = int(required * 2.5)
    return level
