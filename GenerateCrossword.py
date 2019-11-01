import os
import numpy as np

# currently an example
# port to database to be created
wordList = {'permission': [['允许'], {}],
            'campus': [['校园'], {}],
            'agonize': [['痛'], {}],
            'cue': [['线索'], {}],
            'audible': [['听'], {}],
            'innocent': [['无辜'], {}],
            'minister': [['牧师'], {}],
            'taxi': [['出租车'], {}],
            'iterator': [['迭代器'], {}],
            'mad': [['迭代器'], {}],
            }

for new in wordList:
    wordList[new][1]['len'] = new.__len__()
    # print(new, new.__len__())

print(wordList)

sortedList = sorted(wordList, key=lambda d: d.__len__(), reverse=True)

print('sorted: ', sortedList)

toBePlaced = sortedList

print('to be placed: ', toBePlaced)
print(' ')

placed = {}  # store already placed word, in dict
crossword = []

# start generating!
while toBePlaced:
    new = toBePlaced[0]

    new_len = new.__len__()
    isplaced = False
    crossed = False
    crashed = False
    loc_x = None
    loc_y = None
    i_old = None
    i_new = None
    new_start_x = None
    new_start_y = None

    # the first word, directly put it in
    if not placed:
        cur_dir = 0
        placed[new] = {'dir': cur_dir, 'startPos': [0, 0]}
        if cur_dir == 0:
            crossword.append([])
            for i in range(0, new_len):
                crossword[0].append(new[i])
        elif cur_dir == 1:
            for i in range(0, new_len):
                crossword.append([new[i]])
        isplaced = True
        toBePlaced.remove(new)

    else:
        crossed = False
        for old in placed:
            print('Placing:', new, ' Checking: ', old)
            cur_dir = placed[old]['dir']
            n_row = crossword.__len__()
            n_col = crossword[0].__len__()

            crossed = False  # whether the new word intersect with the current words
            crashed = False  # whether the new word will crash with other words
            ext_head = None  # how many rows or columns need to be extended
            ext_tail = None  # how many rows or columns need to be extended

            for letter in new:
                crashed = False
                if old.find(letter) > -1:
                    crossed = True
                    i_old = old.find(letter)  # idx of the letter in the old word
                    i_new = new.find(letter)  # idx of the letter in the new word

                    head = i_new  # how many letters in the new word before the intersecting letter
                    tail = new_len - i_new - 1  # how many letters in the new word after the intersecting letter

                    if cur_dir == 0:  # cross
                        loc_x = placed[old]['startPos'][0]
                        loc_y = placed[old]['startPos'][1] + i_old

                        # check along previous rows
                        for i in range(0, loc_x - head):
                            if crossword[i][loc_y] is not '#' \
                                    or (loc_y - 1 >= 0 and crossword[i][loc_y - 1] is not '#') \
                                    or (loc_y + 1 < n_col and crossword[i][loc_y + 1] is not '#'):
                                print('Crashed!')
                                crashed = True
                                break

                        # check following rows
                        for i in range(loc_x + 1, loc_x + tail + 1):
                            if i >= n_row:  # exceeding # row of current crossword
                                break

                            elif crossword[i][loc_y] is not '#' \
                                    or (loc_y - 1 >= 0 and crossword[i][loc_y - 1] is not '#') \
                                    or (loc_y + 1 < n_col and crossword[i][loc_y + 1] is not '#'):
                                print('Crashed!')
                                crashed = True
                                break

                        # how many rows extend
                        ext_head = max(0, head - loc_x)
                        ext_tail = max(0, tail + loc_x + 1 - n_row)

                    elif cur_dir == 1:  # down
                        loc_x = placed[old]['startPos'][0] + i_old
                        loc_y = placed[old]['startPos'][1]

                        # check along previous columns
                        for i in range(0, loc_y - head):
                            if crossword[loc_x][i] is not '#' \
                                    or (loc_x - 1 >= 0 and crossword[loc_x - 1][i] is not '#') \
                                    or (loc_x + 1 < n_row and crossword[loc_x + 1][i] is not '#'):
                                print('Crashed!')
                                crashed = True
                                break

                        # check along following cols
                        for i in range(loc_y + 1, loc_y + tail + 1):
                            if i >= n_col:
                                break
                            elif crossword[loc_x][i] is not '#' \
                                    or (loc_x - 1 >= 0 and crossword[loc_x - 1][i] is not '#') \
                                    or (loc_x + 1 < n_row and crossword[loc_x + 1][i] is not '#'):
                                print('Crashed!')
                                crashed = True
                                break

                        # how many columns to extend
                        ext_head = max(0, head - loc_y)
                        ext_tail = max(0, tail + loc_y + 1 - n_col)
                    else:
                        print('ERROR IN PLACEMENT DIRECTION!')

                    # updated the crossword and placed the new word
                    if crossed is True and crashed is False:
                        new_dir = 1 - cur_dir
                        newline = []
                        if new_dir == 1:  # down
                            # starting pos of new word
                            new_start_x = loc_x - i_new + ext_head
                            new_start_y = loc_y

                            # insert new rows
                            for i in range(ext_head):
                                crossword.insert(0, ['#'] * crossword[0].__len__())

                            for i in range(ext_tail):
                                crossword.append(['#'] * crossword[0].__len__())

                            # place new word
                            for i in range(new_len):
                                replace = new[i]
                                crossword[new_start_x + i][new_start_y] = replace

                        if new_dir == 0:  # cross
                            # starting pos of new word
                            new_start_x = loc_x
                            new_start_y = loc_y - i_new + ext_head

                            # insert new cols
                            for i in range(0, crossword.__len__()):
                                # crossword.insert(0, ['#'] * crossword[0].__len__())
                                for j in range(ext_head):
                                    crossword[i].insert(0, '#')
                                for j in range(ext_tail):
                                    crossword[i].append('#')

                            # place new word
                            for i in range(0, new_len):
                                crossword[new_start_x][new_start_y + i] = new[i]

                        isplaced = True

                        break

                    if isplaced:  # successfully placed, remove
                        break

            if isplaced:
                print('+++++++ ', new, ' PLACED!\n')
                # update old word's position
                if new_dir == 1:  # down
                    placed[old]['startPos'][0] += ext_head
                elif new_dir == 0:  # cross
                    placed[old]['startPos'][1] += ext_head

                # update list
                placed[new] = {'dir': new_dir, 'startPos': [new_start_x, new_start_y]}

                # successfully placed, remove
                toBePlaced.remove(new)
                break
            else:  # not placed, put at the back of the list
                print('------- ', new, ' FAILED!\n')
                toBePlaced.remove(new)
                toBePlaced.append(new)

            print('to be placed: ', toBePlaced)

# print final crossword
for i in range(crossword.__len__()):
    newline = ''
    for j in range(0, crossword[0].__len__()):
        newline = newline + crossword[i][j]
        # print(crossword[i][j])

    print(newline)

print(' ')
print('not placed: ', toBePlaced)
print('placed: ', placed)










