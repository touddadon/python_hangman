from random import randint
from time import sleep
from re import search
from json import load

def print_and_clear(output='', clear_screen=True, sleep_time=1):
    if output is not None:
        print(output)
        sleep(sleep_time)
        print("\033[F\r\033[K", end='') # подвинуть каретку на строку выше и очистить строку
    if clear_screen is True:
        print("\033[H\033[J", end='') # подвинуть каретку в левый верхний угол и очистить зону от каретки до конца экрана 
    return

def check_hangman_input(input, used_letters):
    if len(input) > 1 or bool(search("[а-яА-Я]", input)) is False:
        print_and_clear("Неправильный ввод.")
        return False
    elif input in used_letters:
        print_and_clear("Вы уже использовали эту букву.")
        return False
    return True

def announce_result(win, true_word):
    if win is False:
        print_and_clear(f"\nВы проиграли! Правильное слово: {true_word}", sleep_time=2)
    else:
        print_and_clear(f"\nВы победили! Правильное слово: {true_word}", sleep_time=2)
    return

def check_game_over(mistakes_count, true_word, hidden_word):
    player_won = (true_word == ''.join(hidden_word))
    if mistakes_count == 6:
        announce_result(win=False, true_word=true_word)
        return True
    elif player_won is True:
        announce_result(win=True, true_word=true_word)
        return True
    return False

def player_turn(true_word, letter, mistakes_count, hidden_word, used_letters):
    letter = input()
    if check_hangman_input(letter, used_letters):
        used_letters.append(letter)
        if letter in true_word:
            for i in range(len(hidden_word)):
                if letter == true_word[i]:
                    hidden_word[i] = letter
        else:
            mistakes_count += 1
            print_and_clear("Такой буквы нет в загаданном слове.", clear_screen=False)
        print_and_clear()

    return letter, mistakes_count

def hangman(true_word, letter, mistakes_count, hidden_word, used_letters, hangman_stages):
    GAME_IN_PROGRESS = True
    while (GAME_IN_PROGRESS):
        print('\n'.join(hangman_stages[mistakes_count]))
        print(''.join(hidden_word))
        print(f"Всего ошибок: {mistakes_count}. Последний ввод: {letter}. Введите букву русского алфавита: ", end='')

        if check_game_over(mistakes_count, true_word, hidden_word):
            GAME_IN_PROGRESS = False
        else:
            letter, mistakes_count = player_turn(true_word, letter, mistakes_count, hidden_word, used_letters)

def init_newgame_or_exit(words, hangman_stages):
    while True:
        choice = input("Начать новую игру или выйти? (newgame/exit) ")
        if choice == "newgame":
            true_word = words[randint(0, len(words)-1)]
            letter = '-'
            mistakes_count = 0
            hidden_word = ['_']*len(true_word)
            used_letters = []
            hangman(true_word, letter, mistakes_count, hidden_word, used_letters, hangman_stages)
        elif choice == "exit":
            return
        else:
            print_and_clear("Неправильный ввод.")        

if __name__ == "__main__":
    with open('words.txt', 'r', encoding='utf-8') as f:
        words = [line.strip().lower() for line in f if line.strip().isalpha()]
    with open('hangman_stages.json', 'r', encoding='utf-8') as f:
        hangman_stages = load(f)
    if not words or not hangman_stages:
        print("words.txt или hangman_stages.json пуст.")
    else:
        init_newgame_or_exit(words, hangman_stages)