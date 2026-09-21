"""Простой терминальный FAQ-бот для репетиции."""

from pathlib import Path
import re


FAQ_FILE = Path(__file__).with_name("faq.txt")
TOPICS = {
    "время": {"когда", "сколько", "время", "начало", "начнется", "начинается", "часов", "дата"},
    "команда": {"команда", "команду", "команде", "участник", "участников", "состав", "собрать"},
    "трек": {"трек", "трека", "треке", "направление", "выбрать", "выбор"},
    "сдача": {"сдать", "сдача", "сдавать", "отправить", "загрузить", "решение", "репозиторий", "github"},
    "призы": {"приз", "призы", "награда", "награды", "победитель"},
}
def words(text: str) -> set[str]:
    return set(re.findall(r"[a-zа-я0-9]+", text.lower().replace("ё", "е")))


def load_answers() -> dict[str, str]:
    blocks = FAQ_FILE.read_text(encoding="utf-8").strip().split("\n\n")
    if len(blocks) != len(TOPICS):
        raise ValueError("В faq.txt должно быть ровно пять пар вопрос–ответ")
    answers = {}
    for topic, block in zip(TOPICS, blocks):
        lines = block.splitlines()
        if len(lines) != 2 or not lines[0].startswith("Вопрос: ") or not lines[1].startswith("Ответ: "):
            raise ValueError(f"Неверный формат пары: {topic}")
        answers[topic] = lines[1].removeprefix("Ответ: ")
    return answers


def answer(question: str, answers: dict[str, str]) -> str:
    tokens = words(question)
    scores = {topic: len(tokens & keywords) for topic, keywords in TOPICS.items()}
    best = max(scores.values())
    if best == 0 or list(scores.values()).count(best) > 1:
        return "не знаю"
    topic = max(scores, key=scores.get)
    return answers[topic]


def main() -> None:
    answers = load_answers()
    print("FAQ-бот репетиции. Задайте вопрос (выход — 'выход').")
    while True:
        try:
            question = input("Вы: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if question.lower() in {"выход", "exit", "quit"}:
            break
        print("Бот:", answer(question, answers))


if __name__ == "__main__":
    main()
