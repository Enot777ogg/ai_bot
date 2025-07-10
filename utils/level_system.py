def calculate_level(xp: int) -> int:
    level = 1
    required = 1000
    while xp >= required:
        xp -= required
        level += 1
        required = int(required * 2.5)
    return level
