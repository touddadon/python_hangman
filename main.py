from random import randint
from time import sleep
from re import search

def print_hangman(stage=0):
    hangman = [
        "  +--+",
        "  |  O",
        "  | /|\\",
        "  | / \\",
        "  |",
        "--+-----"
    ]
    if stage > 0:
        print('\n'.join(hangman[0:stage]))
    print(" \n"*(6-stage))

def print_and_clear(output='', clear_screen=True, sleep_time=1):
    if output is not None:
        print(output)
        sleep(sleep_time)
        print("\033[F\r\033[K", end='')
    if clear_screen is True:
        print("\033[F\033[K"*9, end='')
    return

def play_hangman(words):
    GAME_IN_PROGRESS = False
    while (True):
        if not GAME_IN_PROGRESS:
            choice = input("Начать новую игру или выйти? (newgame/exit) ")
            if choice == "exit":
                break
            else:
                GAME_IN_PROGRESS = True
                true_word = words[randint(0, len(words)-1)]
                letter = '-'
                mistakes_count = 0
                player_won = False
                hangman_stage = 0
                hidden_word = ['_', '_', '_', '_', '_', '_']
                used_letters = []
            print('\033[F\033[K', end='')

        print_hangman(hangman_stage)
        print(''.join(hidden_word))

        player_won = (true_word == ''.join(hidden_word))

        print(f"Всего ошибок: {mistakes_count}. Последняя введенная буква: {letter}. Введите букву русского алфавита: ", end='')
        if hangman_stage < 6 and not(player_won):
            letter = input()
        else:
            print()

        if hangman_stage == 6:
            print_and_clear(f"Вы проиграли! Правильное слово: {true_word}", sleep_time=2)
            GAME_IN_PROGRESS = False
            continue
        elif player_won is True:
            print_and_clear(f"Вы победили! Правильное слово: {true_word}", sleep_time=2)
            GAME_IN_PROGRESS = False
            continue

        if letter == "exit":
            print("Выходим...")
            sleep(1)
            break
        elif len(letter) > 1 or bool(search("[а-яА-Я]", letter)) is False:
            print_and_clear("Неправильный ввод!")
            continue
        elif letter in used_letters:
            print_and_clear("Вы уже использовали эту букву.")
            continue

        used_letters.append(letter)
        if letter in true_word:
            for i in range(len(hidden_word)):
                if letter == true_word[i]:
                    hidden_word[i] = letter
        else:
            hangman_stage += 1
            print_and_clear("Такой буквы нет в загаданном слове.", clear_screen=False)
            mistakes_count += 1

        print_and_clear()

if __name__ == "__main__":
    with open('words.txt', 'r', encoding='utf-8') as f:
        words = [line.strip().lower() for line in f if len(line.strip()) == 6]
    if not words:
        print("Файл со словами пуст.")
    else:
        play_hangman(words)