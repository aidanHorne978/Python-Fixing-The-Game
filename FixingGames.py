import sys
import copy

# Handling input from file and changing it into a 2D integer array
data = sys.stdin.readline().rstrip()
game = []
while data:
    game.append(data.split())
    data = sys.stdin.readline().rstrip()

num_players = len(game[0])
game.append([0] * num_players)

# Checking to make sure the criteria is met
try:
    game = [list(map(int, i)) for i in game]
    for value in game:
        if len(value) != num_players:
            print("Bad format")
            exit()
        game_set = set(value)
        if len(game_set) == len(value):
            print("Bad format")
            exit()
        for j in value:
            if j > num_players:
                print("Bad Values")
                exit()
except ValueError:
    print("Bad values (not all items integer)")

counter = 0
generations = []


def to_matrix(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]


def firstIndex(l):
    lookup = []
    index = 0

    for result in l:
        if result not in lookup:
            lookup.append(result)
        else:
            index = l.index(result)
            lookup.clear()
            break

    return index


def secondIndex(l):
    lookup = []
    index = 0
    for result in l:
        if result not in lookup:
            lookup.append(result)
            index += 1
        else:
            lookup.clear()
            break
    return index


def push(l, row, col):
    l_copy = copy.deepcopy(l)
    temp = 0
    for i in range(row, len(l_copy)):
        current_val = temp
        temp = l_copy[i][col]
        if i == 0:
            l_copy[i][col] = l_copy[num_players - 1][col]
        else:
            l_copy[i][col] = current_val
    return l_copy


def checkColumn(table, column_index):
    count = 0
    for t in table:
        if t[column_index] == 0:
            count += 1

    if count == 1:
        return True
    else:
        return False


def children(table, row_count):
    new_generation = []
    second_index = secondIndex(table[row_count])
    first_index = firstIndex(table[row_count])

    if len(set(table[row_count])) == num_players - 1 and table[row_count].count(0) == 0:
        push_1 = push(table, row_count, first_index)
        push_2 = push(table, row_count, second_index)

        if checkColumn(push_1, first_index):
            new_generation.append(push_1)

        if checkColumn(push_2, second_index):
            new_generation.append(push_2)

    return new_generation


current_generation = [game]
for row in range(num_players - 1):
    next_generation = []
    for table in current_generation:
        for new_table in children(table, row):
            next_generation.append(new_table)
        current_generation = next_generation

count = 0
temp = []
final = []

if len(current_generation) == 0:
    print("Inconsistent results")
    exit()

for result in current_generation:
    for r in result:
        for i in range(len(r)):
            if r[i] == 0:
                r[i] = '_'

for result in current_generation:
    for r in result:
        if count % num_players == 0:
            if count != 0:
                print()
        print(*r)
        count += 1

game_result = ""
for result in current_generation:
    for r in result:
        for i in r:
            game_result += str(i)

final = to_matrix(game_result, num_players)
final = to_matrix(final, num_players)

sorted_temp = []
for game in final:
    if len(set(game)) == num_players:
        sorted_temp.append(sorted(set(game)))

final_score = []
for game in sorted_temp:
    if game not in final_score:
        final_score.append(game)

print()
if len(final_score) > len(current_generation):
    print("Different results: {} ".format(len(current_generation)))
else:
    print("Different results: {} ".format(len(final_score)))