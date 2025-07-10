def ask_gpt(message: str, memory: str = "") -> str:
    try:
        messages = [
            {"role": "system", "content": "Ты умный AI-ассистент. Помни контекст беседы."},
        ]

        if memory:
            messages.append({"role": "user", "content": f"Вот история: {memory}"})

        messages.append({"role": "user", "content": message})

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=800,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Ошибка: {e}"

