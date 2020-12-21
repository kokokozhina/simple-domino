from random import shuffle
from pip._vendor.distlib.compat import raw_input

player_name = ""
field = list()
market = list()
bot_hand = [[0] * 7 for _ in range(7)]
player_hand = [[0] * 7 for _ in range(7)]
is_players_move = 0  # 0 for bot, 1 for player


def init_market():
    for i in range(7):
        for j in range(i, 7):
            market.append((i, j))
    shuffle(market)


def deal_bones_to_player(player):
    for i in range(7):
        (x, y) = market.pop()
        player[x][y] = 1
        player[y][x] = 1


def get_double_or_smallest_bone(player):
    for i in range(7):
        if player[i][i]:
            return i, i
    bone = (7, 7)
    for i in range(7):
        for j in range(i + 1, 7):
            if player[i][j] and (bone[0] + bone[1] > i + j):
                bone = (i, j)
    return bone


def deal_dominoes():
    init_market()
    deal_bones_to_player(bot_hand)
    deal_bones_to_player(player_hand)


def remove_bone_from_hand(player, bone):
    (x, y) = bone
    player[x][y] = 0
    player[y][x] = 0


def add_bone_to_hand(player, bone):
    (x, y) = bone
    player[x][y] = 1
    player[y][x] = 1


def change_move():
    global is_players_move
    is_players_move ^= 1


def start_game():
    show_hand(player_hand, player_name)
    bot_bone = get_double_or_smallest_bone(bot_hand)
    player_bone = get_double_or_smallest_bone(player_hand)
    if bot_bone[0] == bot_bone[1] and player_bone[0] == player_bone[1]:
        if bot_bone[0] < player_bone[0]:
            print(f"Domino Bot moves first with ( {bot_bone[0]} | {bot_bone[1]} ).")
            remove_bone_from_hand(bot_hand, bot_bone)
            field.append(bot_bone)
            change_move()
        else:
            print(f"{player_name} moves first with ( {player_bone[0]} | {player_bone[1]} ).")
            remove_bone_from_hand(player_hand, player_bone)
            field.append(player_bone)
    elif bot_bone[0] == bot_bone[1]:
        print(f"Domino Bot moves first with ( {bot_bone[0]} | {bot_bone[1]} ).")
        remove_bone_from_hand(bot_hand, bot_bone)
        field.append(bot_bone)
        change_move()
    elif player_bone[0] == player_bone[1]:
        print(f"{player_name} moves first with ( {player_bone[0]} | {player_bone[1]} ).")
        remove_bone_from_hand(player_hand, player_bone)
        field.append(player_bone)
    elif bot_bone[0] + bot_bone[1] < player_bone[0] + player_bone[1]:
        print(f"Domino Bot moves first with ( {bot_bone[0]} | {bot_bone[1]} ).")
        remove_bone_from_hand(bot_hand, bot_bone)
        field.append(bot_bone)
        change_move()
    else:
        print(f"{player_name} moves first with ( {player_bone[0]} | {player_bone[1]} ).")
        remove_bone_from_hand(player_hand, player_bone)
        field.append(player_bone)


def show_hand(player, name):
    print(f"Here is your hand, {name}:")
    for i in range(7):
        for j in range(i, 7):
            if player[i][j]:
                print(f'( {i} | {j} )')


def parse_validate_fit_raw_bone(raw_bone):
    try:
        (x, y, z) = raw_bone.split()
        (x, y) = (int(x), int(y))
        head = get_head()
        tail = get_tail()
        if x < 0 or x > 6 or y < 0 or y > 6 or z != 'h' and z != 't' or not player_hand[x][y] or \
            z == 'h' and head != x and head != y or z == 't' and tail != x and tail != y:
            return False
        else:
            remove_bone_from_hand(player_hand, (x, y))
            if z == 'h':
                field.insert(0, (y, x) if head == x else (x, y))
            else:
                field.append((x, y) if tail == x else (y, x))
            print(f"{player_name} puts  ( {x} | {y} ).")
            return True
    except Exception:
        return False


def check_fish():
    if len(field) == 0:
        return False
    head = get_head()
    tail = get_tail()
    head_counter = 0
    tail_counter = 0
    for (i, j) in field:
        head_counter += 1 if (i == head or j == head) else 0
        tail_counter += 1 if (i == tail or j == tail) else 0
    return head_counter == 7 and tail_counter == 7


def get_head():
    return field[0][0]


def get_tail():
    return field[-1][-1]


def check_hand(player):
    head = get_head()
    tail = get_tail()
    for i in range(7):
        for j in range(i, 7):
            if player[i][j] and is_bone_fits(i, j, head, tail):
                return True
    return False


def move_as_player_successfully():
    show_hand(player_hand, player_name)
    can_move = check_hand(player_hand)
    if can_move:
        while 1:
            raw_bone = raw_input('Please type which bone you choose and type h to set the bone to the head, \n'
                                 'e.g., 3 4 h for the bone ( 3 | 4 ), or t to set the bone to the tail, \n'
                                 'e.g., 3 4 t: ')
            status = parse_validate_fit_raw_bone(raw_bone)
            if status:
                return True
            else:
                print("Incorrect bone. Let\'s try again.")
    else:
        print("No bone to move. Let\'s go to market.")
        if len(market) == 0:
            print("Market is empty, no moves then.")
            return True
        while 1:
            try:
                num = int(input(f'Please type number from 1 to {len(market)} to get a bone from market: '))
                if num < 1 or num > len(market):
                    print("Incorrect number. Let\'s try again.")
                else:
                    bone = market[num - 1]
                    print(f"You receive a bone {bone}.")
                    add_bone_to_hand(player_hand, bone)
                    del market[num - 1]
                    return False
            except Exception:
                print("Incorrect number. Let\'s try again.")


def is_bone_fits(i, j, head, tail):
    return i == head or i == tail or j == head or j == tail


def select_fit_bone_as_bot():
    head = get_head()
    tail = get_tail()
    for i in range(6, -1, -1):
        for j in range(6, i - 1, -1):
            if bot_hand[i][j] and is_bone_fits(i, j, head, tail):
                print(f'Domino Bot puts ( {i} | {j} )')
                if i == head:
                    field.insert(0, (j, i))
                elif j == head:
                    field.insert(0, (i, j))
                elif i == tail:
                    field.append((i, j))
                elif j == tail:
                    field.append((j, i))
                remove_bone_from_hand(bot_hand, (i, j))
                return


def move_as_bot_successfully():
    show_hand(bot_hand, "Domino Bot")  # to play an understandable game
    can_move = check_hand(bot_hand)
    if can_move:
        select_fit_bone_as_bot()
        return True
    else:
        print("No bone to move. Domino Bot goes to market.")
        if len(market) == 0:
            print("Market is empty, no moves then.")
            return True
        bone = market[0]
        print(f"Domino Bot gets a bone.")
        add_bone_to_hand(bot_hand, bone)
        del market[0]
        return False


def play_as_player():
    print(f"{player_name}, your turn!")
    while not move_as_player_successfully():
        pass


def play_as_bot():
    print(f"Domino Bot, your turn!")
    while not move_as_bot_successfully():
        pass


def show_field():
    print("Here's a field: ")
    print('{ ' + ' '.join([f'( {i} | {j} )' for (i, j) in field]) + ' }')


def play_game():
    while 1:
        show_field()
        if is_hand_empty(player_hand) or is_hand_empty(bot_hand):
            return
        if check_fish():
            print("Fish!")
            return
        if is_players_move:
            play_as_player()
        else:
            play_as_bot()
        change_move()


def is_hand_empty(player):
    for i in range(7):
        for j in range(i, 7):
            if player[i][j]:
                return False
    return True


def count_hand(player):
    score = 0
    for i in range(7):
        for j in range(i, 7):
            if player[i][j]:
                score += i + j
    if score == 0 and player[0][0]:
        score = 25
    return score


def celebrate_winner():
    bot_score = count_hand(bot_hand)
    player_score = count_hand(player_hand)
    print(f"Domino Bot score = {bot_score}, {player_name} score = {player_score}")
    print(f"{player_name if bot_score > player_score else 'Domino Bot'} wins! Thanks for the game.")


def run():
    deal_dominoes()
    start_game()
    play_game()
    celebrate_winner()


if __name__ == '__main__':
    player_name = input(f'Please introduce yourself: ')
    print(f'Hi, {player_name}, nice to meet you! I\'m Domino Bot. Let\'s play.')
    run()
