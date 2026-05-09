from json import JSONDecodeError, load
from random import choice
from re import search


def clear_screen() -> None:
    input("Введите любой текст, чтобы продолжить")
    ansi_clear_screen_literal: str = "\033[H\033[J"
    print(ansi_clear_screen_literal, end="")


def is_entry_wrong_format(entry: str) -> bool:
    return len(entry) > 1 or bool(search("[а-яА-ЯёЁ]", entry)) is False


def is_entry_used_before(entry: str, used_letters: list[str]) -> bool:
    return entry in used_letters


def print_entry_validation(entry: str, used_letters: list[str]) -> None:
    if is_entry_used_before(entry, used_letters):
        print("Вы уже использовали эту букву.")
    elif is_entry_wrong_format(entry):
        print("Неправильный ввод.")
    else:
        print("Такой буквы нет в загаданном слове.")


def unmask_word(hidden_word: list[str], true_word: str, entry: str) -> None:
    for i in range(len(hidden_word)):
        if entry == true_word[i]:
            hidden_word[i] = entry


def process_valid_entry(
    entry: str, true_word: str, hidden_word: list[str], mistakes_count: int
) -> int:
    if entry in true_word:
        unmask_word(hidden_word, true_word, entry)
    else:
        mistakes_count += 1
    return mistakes_count


def is_hangman_entry_valid(entry: str, used_letters: list[str]) -> bool:
    if is_entry_wrong_format(entry) or is_entry_used_before(entry, used_letters):
        return False
    return True


def player_turn(
    true_word: str, mistakes_count: int, hidden_word: list[str], used_letters: list[str]
) -> int:
    entry: str = input().strip().lower()
    if is_hangman_entry_valid(entry, used_letters):
        used_letters.append(entry)
        mistakes_count = process_valid_entry(
            entry, true_word, hidden_word, mistakes_count
        )
    else:
        print_entry_validation(entry, used_letters)
    clear_screen()
    return mistakes_count


def print_game_screen(
    hangman_stages: list[list[str]],
    mistakes_count: int,
    hidden_word: list[str],
    used_letters: list[str],
):
    tries_left = len(hangman_stages) - mistakes_count - 1

    print("\n".join(hangman_stages[mistakes_count]))
    print("".join(hidden_word))
    print(f"Осталось попыток: {tries_left}.")
    if len(used_letters) > 0:
        print(f"Использованные буквы: {", ".join(used_letters)}.")
    print("Введите букву русского алфавита: ", end="")


def announce_result(win: bool, true_word: str) -> None:
    if win is False:
        print(f"\nВы проиграли! Правильное слово: {true_word}")
    else:
        print(f"\nВы победили! Правильное слово: {true_word}")
    clear_screen()


def has_player_lost(mistakes_count: int, max_mistakes: int) -> bool:
    return mistakes_count == max_mistakes


def has_player_won(true_word: str, hidden_word: list[str]) -> bool:
    return true_word == "".join(hidden_word)


def is_game_over(
    mistakes_count: int, true_word: str, hidden_word: list[str], max_mistakes: int
) -> bool:
    if has_player_lost(mistakes_count, max_mistakes) or has_player_won(
        true_word, hidden_word
    ):
        return True
    return False


def game_cycle(
    true_word: str,
    hangman_stages: list[list[str]],
) -> None:
    mistakes_count: int = 0
    hidden_word: list[str] = ["_"] * len(true_word)
    used_letters: list[str] = []
    max_mistakes = len(hangman_stages) - 1
    game_in_progress: bool = not (
        is_game_over(mistakes_count, true_word, hidden_word, max_mistakes)
    )

    while game_in_progress:
        print_game_screen(hangman_stages, mistakes_count, hidden_word, used_letters)
        mistakes_count = player_turn(
            true_word, mistakes_count, hidden_word, used_letters
        )
        game_in_progress = not (
            is_game_over(mistakes_count, true_word, hidden_word, max_mistakes)
        )

    if has_player_lost(mistakes_count, max_mistakes):
        announce_result(win=False, true_word=true_word)
    elif has_player_won(true_word, hidden_word):
        announce_result(win=True, true_word=true_word)


def game_menu(words: list[str], hangman_stages: list[list[str]]) -> None:
    while True:
        player_entry: str = input("Начать новую игру или выйти? (начать/выйти) ")
        if player_entry == "начать":
            true_word: str = choice(words)
            game_cycle(true_word, hangman_stages)
        elif player_entry == "выйти":
            return
        else:
            print("Неправильный ввод.")
            clear_screen()


def get_words(filepath: str) -> list[str]:
    with open(filepath, "r", encoding="utf-8") as f:
        words_file: list[str] = [
            line.strip().lower() for line in f if line.strip().isalpha()
        ]
    if not (words_file):
        raise ValueError(f"{filepath} пуст.")
    return words_file


def get_hangman_stages(filepath: str) -> list[list[str]]:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            hangman_stages_file: list[list[str]] = load(f)
            return hangman_stages_file
    except JSONDecodeError:
        raise Exception(f"{filepath} пуст или невалидный JSON.")


if __name__ == "__main__":
    try:
        words_file: list[str] = get_words("words.txt")
        hangman_stages: list[list[str]] = get_hangman_stages("hangman_stages.json")
        game_menu(words_file, hangman_stages)
    except Exception as e:
        print(e)
