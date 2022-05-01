import cv2
import mediapipe as mp
import numpy as np
from matplotlib import pyplot as plt
import pygame
import random
import threading
import time

# SETARI GENERALE
capture = cv2.VideoCapture( 0, cv2.CAP_DSHOW )
capture.set( cv2.CAP_PROP_FRAME_WIDTH, 1280 )
capture.set( cv2.CAP_PROP_FRAME_HEIGHT, 720 )

#print( str( capture.get( cv2.CAP_PROP_FRAME_WIDTH ) ) )
#print( str( capture.get( cv2.CAP_PROP_FRAME_HEIGHT ) ) )
# 640 W   X
# 480 H   Y

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
fingerCoord = [(8, 6), (12, 10), (16, 14), (20, 18)]
thumbCoordinate = (4, 2)


# FUNCTIE DE INVERSAT CAMERA
def mirror_this(image_file, gray_scale=False, with_plot=False) :
    image_rgb = image_file
    image_mirror = np.fliplr( image_rgb )
    if with_plot :
        fig = plt.figure( figsize=(10, 20) )
        ax1 = fig.add_subplot( 2, 2, 1 )
        ax1.axis( "off" )
        ax1.title.set_text( 'Original' )
        ax2 = fig.add_subplot( 2, 2, 2 )
        ax2.axis( "off" )
        ax2.title.set_text( "Mirrored" )
        if not gray_scale :
            ax1.imshow( image_rgb )
            ax2.imshow( image_mirror )
        else :
            ax1.imshow( image_rgb, cmap='gray' )
            ax2.imshow( image_mirror, cmap='gray' )
        return True
    return image_mirror


ACTION_STATUS = "IDLE"
ACTION_STATUS_PREV = "IDLE"


def actions(handPoints) :
    global ACTION_STATUS, ACTION_STATUS_PREV

    #

    thumbY = handPoints[4][1]
    thumbX = handPoints[4][0]
    indexX = handPoints[8][0]
    indexY = handPoints[8][1]

    # FINGERS POSSITIONS
    if 426 > indexX > 213 and indexY < 240 :
        INDEX_CENTER = True
    else :
        INDEX_CENTER = False

    if 426 < indexX and indexY < 240 :
        INDEX_LEFT = True
    else :
        INDEX_LEFT = False

    if indexX < 213 and indexY < 240 :
        INDEX_RIGHT = True
    else :
        INDEX_RIGHT = False

    if 426 > thumbX > 213 and thumbY > 240 :
        THUMB_CENTER = True
    else :
        THUMB_CENTER = False

    if 426 < thumbX and thumbY > 240 :
        THUMB_LEFT = True
    else :
        THUMB_LEFT = False

    if thumbX < 213 and thumbY > 240 :
        THUMB_RIGHT = True
    else :
        THUMB_RIGHT = False

    # STATIC
    if THUMB_CENTER == True and INDEX_CENTER == True :
        ACTION_STATUS = "IDLE"
        ACTION_STATUS_PREV = "IDLE"

    # MOVE_LEFT
    elif THUMB_LEFT == True and INDEX_LEFT == True and ACTION_STATUS_PREV == "IDLE" :
        ACTION_STATUS = "MOVE_LEFT"
        ACTION_STATUS_PREV = "MOVE_LEFT"

    # MOVE_RIGHT
    elif THUMB_RIGHT == True and INDEX_RIGHT == True and ACTION_STATUS_PREV == "IDLE" :
        ACTION_STATUS = "MOVE_RIGHT"
        ACTION_STATUS_PREV = "MOVE_RIGHT"

    # ROTATE_LEFT
    elif THUMB_CENTER == True and INDEX_LEFT == True and ACTION_STATUS_PREV == "IDLE" :
        ACTION_STATUS = "ROTATE_LEFT"
        ACTION_STATUS_PREV = "ROTATE_LEFT"

    # ROTATE_RIGHT
    elif THUMB_CENTER == True and INDEX_RIGHT == True and ACTION_STATUS_PREV == "IDLE" :
        ACTION_STATUS = "ROTATE_RIGHT"
        ACTION_STATUS_PREV = "ROTATE_RIGHT"


    """
    if ACTION_STATUS == "IDLE" :
        pass
    elif ACTION_STATUS == "MOVE_LEFT" :
        print( "MOVE_LEFT" )
    elif ACTION_STATUS == "MOVE_RIGHT" :
        print( "MOVE_RIGHT" )
    elif ACTION_STATUS == "ROTATE_LEFT" :
        print( "ROTATE_LEFT" )
    elif ACTION_STATUS == "ROTATE_RIGHT" :
        print( "ROTATE_RIGHT" )
    # print(ACTION_STATUS)
    """

    res = ACTION_STATUS
    ACTION_STATUS = "-------"

    return res

def camera_working() :
    global ACTION_STATUS, ACTION_STATUS_PREV, hands, mpDraw, mpHands, thumbCoordinate, capture
    for i in range(2):
        success, img = capture.read()
        results = hands.process( img )
        landmarks = results.multi_hand_landmarks
        res = "IDLE"

        if landmarks :
            # recunoastere degete si salvare coordonate
            for handLms in landmarks :
                handPoints = []

                # MEMORARE COORDONATE
                for idx, lm in enumerate( handLms.landmark ) :
                    h, w, c = img.shape
                    cx, cy = int( lm.x * w ), int( lm.y * h )
                    handPoints.append( (cx, cy) )

                    # EVIDENTIERE DEGETE
            for i in range( 9 ) :
                cv2.circle( img, handPoints[i], 10, (0, 255, 0), cv2.FILLED )

            # fingerCoord = [ (), (12,10), (16,14), (20,18) ]

            # INTERPRETARE ACTIUNI

            res = actions( handPoints )

        image = mirror_this( img, False, False )

    return (image, res)


# -------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------


pygame.font.init()

s_width = 800
s_height = 700
play_width = 300
play_height = 600
block_size = 30
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

win = pygame.display.set_mode( (s_width, s_height) )
pygame.display.set_caption( 'T E T R I S' )

S = [['.....', '.....', '..00.', '.00..', '.....'],
     ['.....', '..0..', '..00.', '...0.', '.....']]

Z = [['.....', '.....', '.00..', '..00.', '.....'],
     ['.....', '..0..', '.00..', '.0...', '.....']]

I = [['..0..', '..0..', '..0..', '..0..', '.....'],
     ['.....', '0000.', '.....', '.....', '.....']]

O = [['.....', '.....', '.00..', '.00..', '.....']]

J = [['.....', '.0...', '.000.', '.....', '.....'],
     ['.....', '..00.', '..0..', '..0..', '.....'],
     ['.....', '.....', '.000.', '...0.', '.....'],
     ['.....', '..0..', '..0..', '.00..', '.....']]

L = [['.....', '...0.', '.000.', '.....', '.....'],
     ['.....', '..0..', '..0..', '..00.', '.....'],
     ['.....', '.....', '.000.', '.0...', '.....'],
     ['.....', '.00..', '..0..', '..0..', '.....']]

T = [['.....', '..0..', '.000.', '.....', '.....'],
     ['.....', '..0..', '..00.', '..0..', '.....'],
     ['.....', '.....', '.000.', '..0..', '.....'],
     ['.....', '..0..', '.00..', '..0..', '.....'],
     ]
P = [['.....', '..0..', '.000.', '..0..', '.....']]

shapes = [S, Z, I, O, J, L, T, P]
shape_colors = [(255, 60, 60), (255, 150, 60), (255, 255, 50), (160, 255, 128), (0, 180, 255), (166, 120, 255),
                (140, 220, 255), (255, 150, 220)]


class Piece( object ) :
    rows = 20
    columns = 10

    def __init__(self, column, row, shape) :
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index( shape )]
        self.rotation = 0


def create_grid(locked_positions={}) :
    grid = [[(255, 255, 255) for x in range( 10 )] for x in range( 20 )]

    for i in range( len( grid ) ) :
        for j in range( len( grid[i] ) ) :
            if (j, i) in locked_positions :
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape) :
    positions = []
    format = shape.shape[shape.rotation % len( shape.shape )]

    for i, line in enumerate( format ) :
        row = list( line )
        for j, column in enumerate( row ) :
            if column == '0' :
                positions.append( (shape.x + j, shape.y + i) )

    for i, pos in enumerate( positions ) :
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid) :
    accepted_positions = [[(j, i) for j in range( 10 ) if grid[i][j] == (255, 255, 255)] for i in range( 20 )]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format( shape )

    for pos in formatted :
        if pos not in accepted_positions :
            if pos[1] > -1 :
                return False

    return True


def check_lost(positions) :
    for pos in positions :
        x, y = pos
        if y < 1 :
            return True
    return False


def get_shape() :
    global shapes, shape_colors
    return Piece( 5, 0, random.choice( shapes ) )


def draw_text_middle(text, size, color, surface) :
    font = pygame.font.SysFont( 'comicsans', size, bold=True )
    label = font.render( text, 1, color )

    surface.blit( label, (
        top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - label.get_height() / 2) )


def draw_main_menu(size, color, surface) :
    font = pygame.font.SysFont( 'comicsans', size, bold=False )
    font_title = pygame.font.SysFont( 'comicsans', 2 * size, bold=True )

    title = "T E T R I S"
    text1 = "Press Space To Play"
    text2 = "Press Esc to Quit"
    label1 = font.render( text1, 1, color )
    label2 = font.render( text2, 1, color )
    label_title = font_title.render( title, 1, color )

    x1 = s_width / 2 - label1.get_width() / 2
    x2 = s_width / 2 - label2.get_width() / 2
    xt = s_width / 2 - label_title.get_width() / 2
    y1 = s_height / 2 - label1.get_height() + label_title.get_height()
    y2 = s_height / 2 - label2.get_height() + label1.get_height() + label_title.get_height() + 10
    yt = s_height / 2 - label_title.get_height()
    surface.blit( label_title, (xt, yt) )

    surface.blit( label1, (x1, y1) )
    surface.blit( label2, (x2, y2) )


def draw_grid(surface, row, col) :
    sx = top_left_x
    sy = top_left_y
    for i in range( row ) :
        pygame.draw.line( surface, (128, 128, 128), (sx, sy + i * 30),
                          (sx + play_width, sy + i * 30) )
        for j in range( col ) :
            pygame.draw.line( surface, (128, 128, 128), (sx + j * 30, sy),
                              (sx + j * 30, sy + play_height) )


def clear_rows(grid, locked, score) :
    inc = 0
    for i in range( len( grid ) - 1, -1, -1 ) :
        row = grid[i]
        # Clear if there is no white pixels in the row
        if (255, 255, 255) not in row :
            inc += 1
            ind = i
            score[0] = score[0] + 10;
            print( score )
            for j in range( len( row ) ) :
                try :
                    del locked[(j, i)]
                except :
                    continue
    if inc > 0 :
        for key in sorted( list( locked ), key=lambda x : x[1] )[: :-1] :
            x, y = key
            if y < ind :
                newKey = (x, y + inc)
                locked[newKey] = locked.pop( key )


def draw_right_side(shape, surface, score) :
    # Preview Next Shape
    font = pygame.font.SysFont( 'comicsans', 30 )

    label = font.render( 'Next Shape', 1, (255, 255, 255) )

    sx = top_left_x + play_width
    sy = s_height / 2
    l = (s_width - play_width) / 2;
    x = sx + l / 2
    x_line = sx + l / 2 - 2.5 * block_size
    format = shape.shape[shape.rotation % len( shape.shape )]

    for i, line in enumerate( format ) :
        row = list( line )
        for j, column in enumerate( row ) :
            if column == '0' :
                pygame.draw.rect( surface, shape.color,
                                  (x_line + j * block_size, sy + i * block_size, block_size, block_size), 0 )
    for i in range( 6 ) :
        pygame.draw.line( surface, (64, 64, 64), (x_line, sy + i * block_size),
                          (x_line + 6 * block_size, sy + i * block_size) )
        for j in range( 6 ) :
            pygame.draw.line( surface, (64, 64, 64), (x_line + j * block_size, sy),
                              (x_line + j * block_size, sy + 6 * block_size) )
    surface.blit( label, (x - label.get_width() / 2, sy - block_size) )

    # Preview Score
    label1 = font.render( "SCORE", 1, (255, 255, 255) )
    label2 = font.render( score, 1, (255, 255, 255) )

    surface.blit( label1, (x - label1.get_width() / 2, sy + 5 * block_size) )
    surface.blit( label2, (x - label2.get_width() / 2, sy + 6 * block_size) )


def draw_score(surface, score) :
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100
    font = pygame.font.SysFont( 'comicsans', 30 )
    label1 = font.render( "SCORE", 1, (255, 255, 255) )
    label2 = font.render( str( score[0] ), 1, (255, 255, 255) )
    surface.blit( label1, (sx + 35, sy + 150) )
    surface.blit( label2, (sx + 70, sy + 180) )


def draw_window(surface) :
    surface.fill( (64, 64, 64) )
    font = pygame.font.SysFont( 'comicsans', 60 )
    label = font.render( 'T E T R I S I O N', 1, (255, 255, 255) )
    surface.blit( label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30) )
    for i in range( len( grid ) ) :
        for j in range( len( grid[i] ) ) :
            pygame.draw.rect( surface, grid[i][j], (top_left_x + j * 30, top_left_y + i * 30, 30, 30), 0 )
    draw_grid( surface, 20, 10 )
    pygame.draw.rect( surface, (100, 100, 100), (top_left_x, top_left_y, play_width, play_height), 5 )


class ReturnValueThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result = None

    def run(self):
        if self._target is None:
            return  # could alternatively raise an exception, depends on the use case
        try:
            self.result = self._target(*self._args, **self._kwargs)
        except Exception as exc:
            print(f'{type(exc).__name__}: {exc}', file=sys.stderr)  # properly handle the exception

    def join(self, *args, **kwargs):
        super().join(*args, **kwargs)
        return self.result


def main() :
    global grid
    Score = [0]
    locked_positions = {}
    grid = create_grid( locked_positions )

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0

    t1 = ReturnValueThread( target=camera_working )
    t1.start()
    results = t1.join()

    image = results[0]
    action_status = results[1]

    winname = "Finger track"
    cv2.namedWindow( winname )
    cv2.moveWindow( winname, 40, 30 )
    cv2.imshow( winname, image )
    cv2.waitKey( 5 )




    while run :
        fall_speed = 0.3
        grid = create_grid( locked_positions )
        fall_time += clock.get_rawtime()
        clock.tick()


        t1 = ReturnValueThread(target=camera_working)
        t1.start()
        results = t1.join()

        image=results[0]
        action_status = results[1]

        winname = "Finger track"
        cv2.namedWindow( winname )
        cv2.moveWindow( winname, 40, 30 )
        cv2.imshow( winname, image )
        cv2.waitKey(5)

        # FALLING ANIMATIONS
        if fall_time / 3000 >= fall_speed :
            fall_time = 0
            current_piece.y += 1

            if not (valid_space( current_piece, grid )) and current_piece.y > 0 :
                current_piece.y -= 1
                change_piece = True

        # MOVES MADE
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                run = False
                pygame.display.quit()
                quit()

        if action_status == "IDLE" :
            pass
        elif action_status == "MOVE_LEFT" :
            current_piece.x -= 1
            if not valid_space( current_piece, grid ) :
                current_piece.x += 1
        elif action_status == "MOVE_RIGHT" :
            current_piece.x += 1
            if not valid_space( current_piece, grid ) :
                current_piece.x -= 1
        elif action_status == "ROTATE_LEFT" or action_status == "ROTATE_RIGHT" :
            current_piece.rotation = current_piece.rotation + 1 % len( current_piece.shape )
            if not valid_space( current_piece, grid ) :
                current_piece.rotation = current_piece.rotation - 1 % len( current_piece.shape )


        shape_pos = convert_shape_format( current_piece )

        for i in range( len( shape_pos ) ) :
            x, y = shape_pos[i]
            if y > -1 :
                grid[y][x] = current_piece.color

        if change_piece :
            for pos in shape_pos :
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

            clear_rows( grid, locked_positions, Score )

        draw_window( win )
        score = str( Score[0] )
        draw_right_side( next_piece, win, score )
        pygame.display.update()

        if check_lost( locked_positions ) :
            run = False

    draw_text_middle( "You Lost : " + str( Score[0] ), 40, (0, 0, 0), win )
    pygame.display.update()
    pygame.time.delay( 2000 )


def main_menu() :
    clk = 0
    run = True
    main_window = True
    color = (0, 0, 0)

    while run and main_window :
        if clk % 501 == 500 :
            color = random.choice( shape_colors )
        win.fill( color )
        draw_main_menu( 60, (255, 255, 255), win )
        pygame.display.update()

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                run = False
                main_window = False

            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE :
                    main()
                    main_window = False
                elif event.key == pygame.K_ESCAPE :
                    run = False
                    main_window = False
        clk += 1
    if (run == False) :
        pygame.quit()


main_menu()

