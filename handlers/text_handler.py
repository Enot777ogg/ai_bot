from utils.level_system import calculate_level

# ...
    # Добавим XP за каждое сообщение (100 XP)
    user.xp += 100
    new_level = calculate_level(user.xp)
    if new_level > user.level:
        user.level = new_level
        await update.message.reply_text(f"🎉 Поздравляю! Ты достиг {new_level} уровня!")

    db.commit()
