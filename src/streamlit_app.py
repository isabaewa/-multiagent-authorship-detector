"""
Веб-интерфейс системы определения авторства на базе Streamlit.

Предоставляет форму ввода данных (три эталонных эссе и проверяемый текст)
и запускает CrewAI-команду для анализа. Результат отображается
в виде развёрнутого отчёта о вероятности авторства.

Запуск:
    streamlit run src/streamlit_app.py
"""

import streamlit as st
from src.crew_setup import authorship_crew


def configure_page() -> None:
    """Настройка параметров страницы Streamlit."""
    st.set_page_config(
        page_title="Определение авторства",
        page_icon="🎓",
        layout="wide",
    )


def render_sidebar() -> None:
    """Боковая панель с информацией о системе."""
    with st.sidebar:
        st.header("ℹ️ О системе")
        st.markdown(
            """
Система определяет вероятность авторства текста на основе
стилистического анализа. Два AI-агента работают последовательно:

1. **Анализатор стиля** — изучает три эталонных эссе
   и создаёт стилистический профиль автора.

2. **Детектор авторства** — сравнивает профиль
   с проверяемым текстом и оценивает вероятность авторства.

### Как пользоваться

1. Вставьте **три эссе** известного автора
2. Вставьте **проверяемый текст**
3. Нажмите **«Запустить анализ»**

### Советы

- Чем объёмнее эталонные эссе, тем точнее анализ
- Желательно использовать эссе на разные темы
- Проверяемый текст должен быть достаточно длинным (от 200 слов)
            """
        )
        st.divider()
        st.caption("Проект для портфолио · CrewAI + Gemini")


def render_input_section() -> tuple[str, str, str, str]:
    """Отрисовка полей ввода. Возвращает кортеж текстов эссе и проверяемого текста."""
    st.header("📝 Эталонные эссе автора")
    st.caption("Вставьте три текста, достоверно написанные проверяемым автором.")

    col1, col2, col3 = st.columns(3)

    with col1:
        essay1 = st.text_area(
            "Эссе 1",
            height=200,
            placeholder="Вставьте первое эссе автора…",
            label_visibility="visible",
        )
    with col2:
        essay2 = st.text_area(
            "Эссе 2",
            height=200,
            placeholder="Вставьте второе эссе автора…",
            label_visibility="visible",
        )
    with col3:
        essay3 = st.text_area(
            "Эссе 3",
            height=200,
            placeholder="Вставьте третье эссе автора…",
            label_visibility="visible",
        )

    st.header("🔎 Проверяемый текст")
    st.caption("Вставьте текст, авторство которого нужно проверить.")

    suspicious_text = st.text_area(
        "Проверяемый текст",
        height=250,
        placeholder="Вставьте текст для проверки авторства…",
        label_visibility="collapsed",
    )

    return essay1, essay2, essay3, suspicious_text


def render_results(result) -> None:
    """Отрисовка блока результатов анализа."""
    st.header("📊 Результат анализа")
    st.markdown(result.raw)


def main() -> None:
    """Главная функция приложения."""
    configure_page()
    render_sidebar()

    st.title("🎓 Определение авторства текста")
    st.markdown(
        "Система анализа стиля письма для проверки авторства "
        "на основе нескольких эталонных текстов."
    )

    essay1, essay2, essay3, suspicious_text = render_input_section()

    # Проверяем, что все поля заполнены
    all_filled = all([
        essay1.strip(),
        essay2.strip(),
        essay3.strip(),
        suspicious_text.strip(),
    ])

    st.divider()

    if st.button("🚀 Запустить анализ", disabled=not all_filled, type="primary"):
        inputs = {
            "essay1": essay1,
            "essay2": essay2,
            "essay3": essay3,
            "suspicious_text": suspicious_text,
        }

        with st.spinner("⏳ Агенты работают… Это может занять 1–3 минуты."):
            try:
                result = authorship_crew.kickoff(inputs=inputs)
                render_results(result)
            except ValueError as e:
                st.error(f"Ошибка конфигурации: {e}")
            except ConnectionError:
                st.error(
                    "Не удалось подключиться к API. "
                    "Проверьте интернет-соединение и API-ключ."
                )
            except Exception as e:
                st.error(f"Произошла ошибка при работе CrewAI: {e}")


if __name__ == "__main__":
    main()