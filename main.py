from json import load
from random import choice
from re import search
from time import sleep
from typing import Tuple


def print_and_clear(
    output: str, clear_screen: bool = True, sleep_time: int = 1
) -> None:
    if output is not None:
        print(output)
        sleep(sleep_time)
        # очистить строку выше
        print("\033[F\r\033[K", end="")
    if clear_screen is True:
        # очистить экран
        print("\033[H\033[J", end="")


def check_hangman_entry(entry: str, used_letters: list[str]) -> bool:
    if len(entry) > 1 or bool(search("[а-яА-ЯёЁ]", entry)) is False:
        print_and_clear("Неправильный ввод.")
        return False
    if entry in used_letters:
        print_and_clear("Вы уже использовали эту букву.")
        return False
    return True


def announce_result(win: bool, true_word: str) -> None:
    if win is False:
        print_and_clear(f"\nВы проиграли! Правильное слово: {true_word}", sleep_time=2)
    else:
        print_and_clear(f"\nВы победили! Правильное слово: {true_word}", sleep_time=2)


def check_game_over(
    mistakes_count: int, true_word: str, hidden_word: list[str], max_mistakes: int
) -> bool:
    player_won: bool = true_word == "".join(hidden_word)
    if mistakes_count == max_mistakes:
        announce_result(win=False, true_word=true_word)
        return True
    if player_won is True:
        announce_result(win=True, true_word=true_word)
        return True
    return False


def player_turn(
    true_word: str, mistakes_count: int, hidden_word: list[str], used_letters: list[str]
) -> Tuple[str, int]:
    letter: str = input().strip().lower()
    if check_hangman_entry(letter, used_letters):
        used_letters.append(letter)
        if letter in true_word:
            for i in range(len(hidden_word)):
                if letter == true_word[i]:
                    hidden_word[i] = letter
        else:
            mistakes_count += 1
            print_and_clear("Такой буквы нет в загаданном слове.", clear_screen=False)
        print_and_clear("")
    return letter, mistakes_count


def print_game_screen(
    hangman_stages: list[list[str]],
    mistakes_count: int,
    hidden_word: list[str],
    letter: str,
):
    print("\n".join(hangman_stages[mistakes_count]))
    print("".join(hidden_word))
    print(f"Всего ошибок: {mistakes_count}. Последний ввод: {letter}.")
    print("Введите букву русского алфавита: ", end="")


def game_cycle(
    true_word: str,
    mistakes_count: int,
    hidden_word: list[str],
    used_letters: list[str],
    hangman_stages: list[list[str]],
) -> None:
    game_in_progress: bool = True
    letter: str = "-"
    while game_in_progress:
        print_game_screen(hangman_stages, mistakes_count, hidden_word, letter)
        if check_game_over(
            mistakes_count,
            true_word,
            hidden_word,
            max_mistakes=(len(hangman_stages) - 1),
        ):
            game_in_progress = False
        else:
            letter, mistakes_count = player_turn(
                true_word, mistakes_count, hidden_word, used_letters
            )


def init_newgame_or_exit(words: list[str], hangman_stages: list[list[str]]) -> None:
    while True:
        player_entry: str = input("Начать новую игру или выйти? (newgame/exit) ")
        if player_entry == "newgame":
            true_word: str = choice(words)
            mistakes_count: int = 0
            hidden_word: list[str] = ["_"] * len(true_word)
            used_letters: list[str] = []
            game_cycle(
                true_word, mistakes_count, hidden_word, used_letters, hangman_stages
            )
        elif player_entry == "exit":
            return
        else:
            print_and_clear("Неправильный ввод.")


if __name__ == "__main__":
    with open("words.txt", "r", encoding="utf-8") as f:
        words_file: list[str] = [
            line.strip().lower() for line in f if line.strip().isalpha()
        ]

    with open("hangman_stages.json", "r", encoding="utf-8") as f:
        hangman_stages_file: list[list[str]] = load(f)

    if not words_file or not hangman_stages_file:
        print("words.txt или hangman_stages.json пуст.")
    else:
        init_newgame_or_exit(words_file, hangman_stages_file)
