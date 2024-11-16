#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 18:52:24 2024

@author: chris
"""
# streamlit run /Users/chris/Documents/GitRepos/numberGrid/numberGrid/Game.py

import streamlit as st
ss = st.session_state

import Board
if not 'BOARD' in ss: ss['BOARD'] = Board.Board('test')
board = ss['BOARD']
# if not 'GRID' in ss: ss['GRID'] = board.asDataFrame()
# grid = ss['GRID']

import time


import pandas as pd
import numpy as np

GUESSES = 'GUESSES'


def view():
    st.header('Number grid')

    # Button for a new board
    with st.sidebar:
        keys = {'nVisible': 2, 'inclMult': True, 'inclSub': True, 'allowNeg': True}
        for k, v in keys.items():
            if not k in ss: ss[k] = v
        nVisible = st.number_input('Visible', 0, 9, key='nVisible', on_change=reset)
        inclMult = st.checkbox('Include multiplication', key='inclMult', on_change=reset)
        inclSub = st.checkbox('Include subtraction', key='inclSub', on_change=reset)
        allowNeg = st.checkbox('Allow negative answers', key='allowNeg', on_change=reset)
        if st.button('New board'):
            reset()

    if not GUESSES in ss:
        ss[GUESSES] = [None] * len(board._numbers)
    g = ss[GUESSES]
    nums = board._numbers
    for n in board.getVisible():
        idx = nums.index(n)
        g[idx] = n

    grid = board.asDataFrame()
    # vis = [str() for _ in board._visible]
    vis = board._visible
    
    # Create display
    st.write('Solve this...')
    # Create array of containers
    with st.container(border=True):
        ctns = []
        for r in range(grid.shape[0]):
            row = []
            stCols = st.columns(grid.shape[1])
            for c in range(grid.shape[1]):
                row.append(stCols[c].container(border=not grid.values[r, c] is None))
            ctns.append(row)
    # ctns = pd.DataFrame(ctns).values
    
    guessIdx = 0
    for r, row in enumerate(ctns):
        for c, ctn in enumerate(row):
            isAns = (r == len(ctns) - 1) or (c == len(row) - 1)
            isGuess = (r % 2 == 0) and (c % 2 == 0) and not isAns 
            val = grid.iloc[r, c]
            
            if isGuess:
                # st.write('r, c', r, c)
                if val in board._visible:
                    # st.write(r, c, type(r), type(c))
                    ctns[r][c].write(val)
                    g[guessIdx] = val
                else:
                    k = f'{r}_{c}'
                    guess = ctns[r][c].number_input('label hidden', 1, 9, None, placeholder='???',
                                                    key=k, label_visibility='collapsed', )
                    g[guessIdx] = guess
                guessIdx += 1
            elif val == Board.BLANK:
                pass
            elif val == 'x':
                ctns[r][c].write(val)
            elif isAns:
               ctns[r][c].write(f' = {val:.0f}')
            else:
                ctns[r][c].write(f'\{val}')
                
                
                    
            
    # st.write(board._numbers)
    # st.write(g)
    status = pd.DataFrame({'guess': g, 'answer': board._numbers})
    if all(status['guess'] == status['answer']):
        st.balloons()
        st.snow()
    if st.checkbox('Show answers'):
        st.write(status)
    
    
    
    
    
    
    # # Populate containers, taking inputs
    # guess = 0
    # for i in range(grid.shape[0]):
    #     for j in range(grid.shape[1]):
    #         isBoard = (i < grid.shape[0] - 1) and (j < grid.shape[1] - 1)
    #         isGuess = (i % 2 == 0) and (j % 2 == 2) & (i != grid.shape[0] - 1) & (j != grid.shape[1] - 1)
    #         if isGuess: guess += 1
    #         val = valToStr(grid.values[i, j])
            
            
    #         if val == Board.HIDDEN:
    #             k = f'{i}_{j}'
    #             if not k in ss:
    #                 ss[k] = None
    #                 print(f'set ss[{k}] to {ss[k]}')
    #             ctns[i, j].number_input('label_hidden', 1, 9, None,
    #                                     key=k, label_visibility='collapsed',
    #                                     on_change=updateGuesses, args=(guess, k))
    #             # guess += 1
    #         elif val == Board.BLANK:
    #             pass
    #         elif val in vis and isBoard:
    #             ctns[i, j].write(val)
    #             # guess += 1
    #         elif isBoard:
    #             ctns[i, j].write(f'{val}')
    #         elif not isBoard:
    #             ctns[i, j].write(f'= {val}')
    #         else:
    #             msg = 'Did not expect this:\n\t'
    #             msg += f'val: {val}, i: {i}, j: {j}, guess: {guess}'
    #             raise Exception(msg)
    #             # if (j == grid.shape[0] - 1) and (i % 2 == 0):
    #             #     ctns[i, j].write(f'= {val}')
    #             # elif (i == grid.shape[0] - 1) and (j % 2 == 0):
    #             #     ctns[i, j].write(f'= {val}')
            
            
    
    # st.header('Checking guesses')    
    # if checkGuesses(board):
        
    #     st.balloons()
    #     time.sleep(0.5)
    #     st.button('Next puzzle', on_click=reset)
    # else:
    #     st.header(':blue[Keep going...]')
    #     # st.snow()    












def valToStr(val):
    if val in ['+', '-', '/']:
        val = f'\{val}'
    try:
        val = str(int(val))
    except:
        pass
    # if val is np.nan: val = ''
    return val

def updateGuesses(idx, k):
    guesses = ss[GUESSES]
    # st.header('updatetGuesses')
    # st.write(idx, k, ss[k])
    # st.write(guesses)
    # # st.write(idx, i, j)
    # # st.write('Index is None:', idx is None)
    # # st.write(ss[f'{i}_{j}'])
    # # st.write('----')
    # # st.write(len(guesses))
    # # st.write(idx)
    # # st.write(guesses)
    guesses[idx] = ss[k]
    # st.write(idx, k, ss[k])
    # st.write(guesses)
    
    
def checkGuesses(board):
    guesses = ss[GUESSES]
    ans = board._numbers
    st.write(pd.DataFrame({'guesses': guesses, 'answers': ans}))
    if len(guesses) != len(ans): return False
    board._complete = True
    board._finish = time.time()
    t = board._finish - board._boardStart
    st.header(f'Completed in {t} seconds')
    # st.header('Logging game...')
    # board.logGame()
    
    
    return all([str(b) == str(g) for b, g in zip(ans, guesses)])

def reset():
    keys = ['nVisible', 'inclMult', 'inclSub', 'allowNeg']
    kwargs = {}
    for k in keys:
        kwargs[k] = ss[k]
    
    board.newBoard(**kwargs)
    grid = board.asDataFrame()
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            k = f'{i}_{j}'
            ss[k] = None
            # if k in ss: ss[k] = None
    del ss[GUESSES]

def setVisible():
    visible_prev = board.getVisible()
    board.setVisible(ss['nVisible'])
    visible_after = board.getVisible()
    guesses = ss[GUESSES]
    for v in visible_prev:
        if v in visible_after: continue
        guesses = ss[GUESSES]
        idx = guesses.index(v)
        guesses[idx] = None
    
    



# def view():
#     st.header('Number grid')

#     # Button for a new board
#     with st.sidebar:
#         st.number_input('Visible', 0, 9, value=2, key='nVisible', on_change=setVisible)
#         if st.button('Rerun'):
#             reset()

#     if not GUESSES in ss:
#         ss[GUESSES] = [None] * len(board._numbers)
#     g = ss[GUESSES]
#     nums = board._numbers
#     for n in board.getVisible():
#         idx = nums.index(n)
#         g[idx] = n
    
#     # with st.expander('Solution', True):
#     #     st.info('For dev, will be deleted')
#     #     st.write(board.asDataFrame(True))
#     #     st.write('Visible:', board._visible)

#     grid = board.asDataFrame()
    
#     # Create display
#     st.write('Solve this...')
#     with st.container(border=True):
#         ctns = []
#         for r in range(grid.shape[0]):
#             row = []
#             stCols = st.columns(grid.shape[1])
#             for c in range(grid.shape[1]):
#                 row.append(stCols[c].container(border=not grid.values[r, c] is None))
#             ctns.append(row)
    
    
#     ctns = pd.DataFrame(ctns).values
#     guess = 0
#     for i in range(grid.shape[0]):
#         for j in range(grid.shape[1]):
#             if (i == grid.shape[0] - 1) and (j % 2 == 0): ctns[i, j].write('equals')
#             val = valToStr(grid.values[i, j])
            
#             if val == Board.HIDDEN:
#                 ctns[i, j].number_input('label_hidden', 1, 9, value=None,
#                                         key=f'{i}_{j}', label_visibility='collapsed',
#                                         on_change=updateGuesses, args=(guess, i, j))
#                 guess += 1
#             elif val == Board.BLANK:
#                 pass
#             elif val in board._visible and i < grid.shape[0] - 1 and j < grid.shape[1]:
#                 ctns[i, j].write(val)
#                 guess += 1
#             else:
#                 ctns[i, j].write(val)
            
#     # with st.container(border=True):
#     #     st.header('Checks')
#     #     st.write(checkGuesses(board))
#     #     st.subheader('Guesses')
#     #     st.write(ss[GUESSES])
#     #     st.subheader('Answers')
#     #     st.write(board._numbers)
    
#     st.header('Checking guesses')    
#     if checkGuesses(board):
        
#         st.balloons()
#         time.sleep(0.5)
#         st.button('Next puzzle', on_click=reset)
#     else:
#         st.header(':blue[Keep going...]')
#         # st.snow()
    
    
    
    
    
    
    

view()