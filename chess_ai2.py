from stockfish import Stockfish
import json
import time
import random

# reads config.json file
config_file = open("config.json")
config = json.load(config_file)
stockfish_path = config["stockfish_path"]
config_file.close()

stockfish_parameters={
    "Debug Log File": "",
    "Contempt": 0,
    "Min Split Depth": 0,
    "Threads": 3, # More threads will make the engine stronger, but should be kept at less than the number of logical processors on your computer.
    "Ponder": "false",
    "Hash": 4096, # Default size is 16 MB. It's recommended that you increase this value, but keep it as some power of 2. E.g., if you're fine using 2 GB of RAM, set Hash to 2048 (11th power of 2).
    "MultiPV": 1,
    "Skill Level": 20,
    "Move Overhead": 10,
    "Minimum Thinking Time": 100,
    "Slow Mover": 100,
    "UCI_Chess960": "false",
    "UCI_LimitStrength": "false",
    "UCI_Elo": 3190
}

def letter_to_xpos(letter): # convert letter to x position on the map
    letter = letter.lower()
    if letter == 'a':
        return 0
    if letter == 'b':
        return 1
    if letter == 'c':
        return 2
    if letter == 'd':
        return 3
    if letter == 'e':
        return 4
    if letter == 'f':
        return 5
    if letter == 'g':
        return 6
    if letter == 'h':
        return 7

    raise ValueError("Invalid letter.")

def pieces_to_map(input_map, input_pieces, color): # adds the input peaces to the input map
    for key, items in input_pieces.items():
        for coords in items:
            letter = coords[0:1]
            xpos = letter_to_xpos(letter)
            ypos = 8 - int(coords[1:2])

            code = ''

            if key == 'Pawns':
                code = 'P'
            elif key == 'Queen':
                code = 'Q'
            elif key == 'King':
                code = 'K'
            elif key == 'Knights':
                code = 'N'
            elif key == 'Bishops':
                code = 'B'
            elif key == 'Rooks':
                code = 'R'
            else:
                raise Exception(f'Undefined Input Pieces Key: {key}')
            
            if color == 'black':
                code = code.lower()
            
            input_map[ypos][xpos] = code

            # print(f'adding \'{key}\' ({code}) item ({coords}) -> ({ypos}|{xpos})')
    
    return input_map

def get_fen(bottom_pieces, top_pieces): # creates a fen string for the game layout
    chesspieces = [[0 for x in range(8)] for y in range(8)]

    chesspieces = pieces_to_map(chesspieces, bottom_pieces, 'white')
    chesspieces = pieces_to_map(chesspieces, top_pieces, 'black')

    fen = ''

    for ylist in chesspieces:
        counter = 0
        for i in ylist:
            if i == 0:
                counter = counter + 1
            elif counter >= 1 and not i == 0:
                fen = fen + str(counter)

                counter = 0
                fen = fen + i

            else:
                fen = fen + i

        if counter >= 1:
            fen = fen + str(counter)

        fen = fen + '/'

    fen = fen[0:(len(fen) - 1)] + ' w - - 0 1'

    return fen

def get_best_move(bottom_pieces, top_pieces,fen_string,opp,win_or_not): # calculates the best move

    stockfish = Stockfish(path=stockfish_path,depth=25,parameters=stockfish_parameters)

    #fen_string = get_fen(bottom_pieces, top_pieces,)
    print(fen_string)
    stockfish.set_fen_position(fen_string)

    if win_or_not:
        move = stockfish.get_best_move(2000)
    else:

        num = random.randint(0, 100)    #生成随机数
        print("生成随机数%d"%num)

    
        move_list=stockfish.get_top_moves(4)
        print("最优走法：%s"%move_list)
        move=stockfish.get_best_move(2000) if num<=opp else move_list[3]["Move"]    #按照概率来进行选择最优
    print(move)

    move = move.upper()
    print(move)

    split_strings = []
    n  = 2
    for index in range(0, len(move), n):

        split_strings.append(move[index : index + n])

    stockfish = None

    return split_strings[0], split_strings[1],fen_string
    
    
def compare_fen(bottom_pieces,top_pieces,fen_string_list,num_list,current_top_num,last_top_pos):
    
    print(list(fen_string_list.queue)[1])
    try:
        if json.dumps(top_pieces)!=last_top_pos and json.dumps(top_pieces)==list(fen_string_list.queue)[1] and list(fen_string_list.queue)[1]==list(fen_string_list.queue)[0]  and list(num_list.queue)[0]==list(num_list.queue)[1] and current_top_num==list(num_list.queue)[1]:    #用三个截图的fen来判断是否采取下棋的操作
            print("start!!!!!!!!")
            return False
        else:
            time.sleep(0.8)
            return True
            
    except Exception as e:
        print(f"ERROR: {e}")
        time.sleep(0.5)
        return True

def fen_build(KQ_kq_bottom,KQ_kq_top,bottom_pieces,top_pieces,color):
    fen_string = get_fen(bottom_pieces, top_pieces, ).replace("-","KQkq",1)
    if color=="W":
       if top_pieces["King"]!=["E8"] and  KQ_kq_top=="kq":
           KQ_kq_top=""
       if bottom_pieces["King"]!=["E1"] and KQ_kq_bottom=="KQ":
           KQ_kq_bottom=""
       if KQ_kq_bottom=="" and KQ_kq_top=="":
           fen_string=fen_string.replace("KQkq","-",1)
           return (fen_string,KQ_kq_bottom,KQ_kq_top)
       else:
           fen_string=fen_string.replace("KQkq",KQ_kq_bottom+KQ_kq_top,1)
           return(fen_string,KQ_kq_bottom,KQ_kq_top)

    else:
       if top_pieces["King"]!=["D8"] and  KQ_kq_top=="KQ":
           KQ_kq_top=""
       if bottom_pieces["King"]!=["D1"] and KQ_kq_bottom=="kq":
           KQ_kq_bottom=""
       if KQ_kq_bottom=="" and KQ_kq_top=="":
           fen_string=fen_string.replace("KQkq","-",1)
           return (fen_string,KQ_kq_bottom,KQ_kq_top)
       else:
           fen_string = fen_string.replace("KQkq", KQ_kq_top+KQ_kq_bottom, 1)
           return(fen_string,KQ_kq_bottom,KQ_kq_top)
        
    
