import hangman_helper as hh

##############################################
# GLOBAL VARIABLES - MESSAGES AND OTHER VARIABLES
ERROR_MESSAGE_ONE = "The input must be one lowercase letter"
ERROR_MESSAGE_TWO = "The letter was already chosen"
HINT_LENGTH = hh.HINT_LENGTH
NEW_GAME_MESSAGE = "WELCOME TO THIS NEW GAME"
ROUND_WON = "YOU WON!!!"
ROUND_LOST = "YOU LOST :.( The word was: "
INITIAL_POINTS = hh.POINTS_INITIAL
LETTER = hh.LETTER
WORD = hh.WORD
HINT = hh.HINT
GAME_LOST = "You survived {} games and then lost Do you wanna play again?"
GAME_WON = "Score: {}, Games: {} Do you wanna play again?"
LETTER_IN_WORD = "The letter {} is in the word"
LETTER_NOT_IN_WORD = "The letter {} is not in the word"
HINT_MESSAGE = "You used a hint (facepalm moment)"
WRONG_WORD_MESSAGE = "This is not the right word"
##############################################


# FUNCTIONS
def update_word_pattern(word, pattern, letter):
    """
    Takes in the correct word, current pattern and letter guessed and
    returns the new pattern with the _ changed with the letter where suitable.
    :param word: String that contains the correct word
    :param pattern: String that is the current pattern of letters and _
    :param letter: String with current letter guessed by the user
    :return: String that is the new pattern of letters and _
    """
    pattern_list = [i for i in pattern]
    for i in range(len(word)):
        if word[i] == letter:
            pattern_list[i] = letter
    pattern = "".join(pattern_list)
    return pattern


def filter_same_letters_and_position(word, pattern):
    """
    Takes in possible word and the pattern and checks whether all the
    letters in pattern are in the same positions as in the possible word and
    that these letters do not appear anywhere else in the possible word and
    returns the boolean value based on these checks
    :param word: String that is a possible word
    :param pattern: String that is the current pattern of letters and _
    :return: Boolean representing whether it is a possible word after checks
    """
    set1 = {i for i in pattern if i != "_"}
    for i in range(len(pattern)):
        if pattern[i] != "_" and pattern[i] != word[i]:
            return False
        elif pattern[i] == "_" and word[i] in set1:
            return False
    return True


def filter_wrong_guess(word, wrong_guess_lst):
    """
    Takes in possible word and checks whether it has any letters that are in
    the wrong letter list and returns the boolean value based on this check.
    :param word: String that is a possible word
    :param wrong_guess_lst: List containing all wrong letters guessed so far
    :return: Boolean representing whether it is a possible word after checks
    """
    for letter in wrong_guess_lst:
        if letter in word:
            return False
    return True


def filter_words_list(words, pattern, wrong_guess_lst):
    """
    Takes in possible words, current pattern and wrong guess list and
    returns the possible words based on the information given to the user.
    :param words: List of all words
    :param pattern: String that is the current pattern of letters and _
    :param wrong_guess_lst: List containing all wrong letters guessed so far
    :return: List of all possible words after check
    """
    total_list = []
    for word in words:
        if len(word) == len(pattern):
            if not filter_same_letters_and_position(word, pattern):
                continue
            elif not filter_wrong_guess(word, wrong_guess_lst):
                continue
            else:
                total_list.append(word)
    return total_list


def add_points(pattern, new):
    """
    Takes in the old and new patterns and returns the number of points to
    add based on how many letters were revealed
    :param pattern: String that is the old pattern of letters and _
    :param new: String that is the current pattern of letters and _
    :return: Number of points to add
    """
    counter = 0
    for i in range(len(new)):
        if new[i] != pattern[i]:
            counter += 1
    add = (counter * (counter + 1)) // 2
    return add


def letter_input(user_input, pattern, word, wrong_guess_lst, score):
    """
    Takes in the user input, pattern word wrong guess list and score and
    returns the updated pattern, updated wrong guess list, updated and
    message to send to user based on whether the input is unaccepted,
    repeated,  incorrect or correct.
    :param user_input: String that user inputted
    :param pattern: String that is the current pattern of letters and _
    :param word: String that contains the correct word
    :param wrong_guess_lst: List containing all wrong letters guessed so far
    :param score: Number that is the player's current score
    :return: updated pattern, updated wrong guess list , updated score and
    message to send to the user
    """
    if len(user_input) != 1 or not user_input.islower():
        msg = ERROR_MESSAGE_ONE
    elif user_input in wrong_guess_lst or user_input in pattern:
        msg = ERROR_MESSAGE_TWO
    else:
        score -= 1
        if user_input in word:
            new = update_word_pattern(word, pattern, user_input)
            score += add_points(pattern, new)
            pattern = new
            msg = LETTER_IN_WORD.format(user_input)
        else:
            wrong_guess_lst.append(user_input)
            msg = LETTER_NOT_IN_WORD.format(user_input)
    return pattern, wrong_guess_lst, score, msg


def word_input(user_input, pattern, word, score):
    """
    Takes in the user input, pattern, word and score and checks if the user
    input is the word, if so then it adds the correct amount of points and
    then it returns the updated pattern and score.
    :param user_input: String that user inputted
    :param pattern: String that is the current pattern of letters and _
    :param word: String that contains the correct word
    :param score: Number that is the player's current score
    :return: updated pattern, updated score and message
    """
    score -= 1
    msg = WRONG_WORD_MESSAGE
    if user_input == word:
        score += add_points(pattern, user_input)
        return word, score, msg
    return pattern, score, msg


def hint_input(pattern, words_list, wrong_guess_lst, score):
    """
    Takes in pattern, all possible words, wrong guess list and score and
    filters the words that are not possible. It then reduces the hint list
    to a readable size if there are too many possibilities and returns
    the updated score
    :param pattern: String that is the current pattern of letters and _
    :param words_list: List of all words
    :param wrong_guess_lst: List containing all wrong letters guessed so far
    :param score: Number that is the player's current score
    :return: updated score and message
    """
    score -= 1
    hint_list = filter_words_list(words_list, pattern, wrong_guess_lst)
    if len(hint_list) > HINT_LENGTH:
        list_length = len(hint_list)
        list1 = []
        for i in range(HINT_LENGTH):
            list1.append(hint_list[(i*list_length)//HINT_LENGTH])
    else:
        list1 = hint_list
    hh.show_suggestions(list1)
    msg = HINT_MESSAGE
    return score, msg, hint_list


def run_single_game(words_list, score):
    """
    Takes in the words_list and score and starts a new game. It generates a
    random word which the user tries to guess. Each loop the user can either
    guess a letter, a word or ask for a hint. At the end of the game the
    function outputs a message to the user of whether they won or lost.  It
    then returns the updated score.
    :param words_list: List of all words
    :param score: Number that is the player's current score.
    :return: updated score
    """
    word = hh.get_random_word(words_list)
    pattern = "_"*len(word)
    wrong_guess_lst = []
    msg = NEW_GAME_MESSAGE
    while "_" in pattern and score > 0:
        hh.display_state(pattern, wrong_guess_lst, score, msg)
        type_of_input, user_input = hh.get_input()
        if type_of_input == LETTER:
            pattern, wrong_guess_lst, score, msg = letter_input(
                user_input, pattern, word, wrong_guess_lst, score)
        elif type_of_input == WORD:
            pattern, score, msg = word_input(user_input, pattern, word, score)
        elif type_of_input == HINT:
            score, msg, words_list= hint_input(pattern, words_list,
                                    wrong_guess_lst, score)
        else:
            exit()
    if score == 0:
        msg = ROUND_LOST + str(word)
    else:
        msg = ROUND_WON
    hh.display_state(pattern, wrong_guess_lst, score, msg)
    return score


def main():
    """
    This function loads the words list of the game and sets up the initial
    game score and number of games. Then it runs the game until the user
    gets wants to stop, between each game displaying a message of the score
    and games won or of how many games the user won until a loss depending
    on whether they won or lost.
    :return: None
    """
    words = hh.load_words()
    score = INITIAL_POINTS
    again = True
    number_of_games = 0
    while again:
        score = run_single_game(words, score)
        number_of_games += 1
        if score <= 0:
            msg = GAME_LOST.format(number_of_games)
            score = INITIAL_POINTS
            number_of_games = 0
        else:
            msg = GAME_WON.format(score, number_of_games)
        again = hh.play_again(msg)
#############################################################


# MAIN PROGRAM
if __name__ == "__main__":
    main()
