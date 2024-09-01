# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# import streamlit as st

import numpy as np
import pandas as pd
import time
# import plotly.express as px

EMPTY = None
HIDDEN = '?'
BLANK = '<BLANK>'

class Board():
    def __init__(self, user, difficulty='easy', nVisible=2, inclMult=True):
        'user and difficulty currently not used'
        self._user = user
        self._difficulty = difficulty
        self._logFile = r'/log.txt'
        self._nVisible = nVisible
        self.reset(user, difficulty)
        self.newBoard()
    
    
    def reset(self, user=None, difficulty=None):
        if  not user is None: self._user = user
        if  not difficulty is None: self._difficulty = difficulty.lower()
        self._played = 0
        self._won = 0
        
    def newBoard(self, nVisible=None, inclMult=True, allowNeg=True):
        '''Board consists of a grid with three rows and three columns.
        Each row / column is a expression with three integers and two operators.
        
        Operators and missing number are currently set at random, but should
        be determined by self._difficulty
        '''
        
        if allowNeg:
            if not nVisible is None: self._nVisible = nVisible
            
            self._numbers = list(range(1, 10))
            np.random.shuffle(self._numbers)
            
            if inclMult:
                opMap = {0: '+', 1: '-', 2: 'x'}
            else:
                opMap = {0: '+', 1: '-'}
            self._operators = np.random.randint(0, len(opMap), 12)
            self._operators = [opMap[op] for op in self._operators]
            
            self._visible = [_ for _ in self._numbers]
            np.random.shuffle(self._visible)
            
            # List of six answers. First three are the rows and second three the columns
            self._answers = self.getAnswers()
            
            self._boardStart = time.time()
            self._complete = False
            self._boardFinish = None
        else:
            ctr = 0
            self.newBoard(nVisible, inclMult, allowNeg=True)
            while min(self._answers) < 0 and ctr < 1000:
                ctr += 1
                self.newBoard(nVisible, inclMult, allowNeg=True)
            print(f'Took {ctr} iterations to get non-negative board')
    
    def getVisible(self):
        'Returns the numbers that are visible (not their indexes)'
        return self._visible[:self._nVisible]
    
    def setVisible(self, n):
        'Sets the numbers that are visible (not their indexes)'
        self._nVisible = n
    
    def getAnswers(self):
        # n = self._numbers
        # op = self._operators
        ans = []
        
        # rows
        for i in range(3):
            exp = self.getExprRow(i, showAll=True, asStr=True)
            exp = exp.replace('x', '*')
            ans.append(eval(exp))

        # cols
        for i in range(3):
            exp = self.getExprCol(i, showAll=True, asStr=True)
            exp = exp.replace('x', '*')
            ans.append(eval(exp))
        
        return ans
        
    def getExprRow(self, row, showAll=False, asStr=False):
        'row should be 0, 1, or 2'
        n = self._numbers
        op = self._operators
        vis = self.getVisible()
        
        i_n = 3 * row
        i_op = 4 * row
        if showAll:
            row = [n[i_n], op[i_op], n[i_n + 1], op[i_op + 1], n[i_n + 2]]
        else:
            row = [n[i_n] if n[i_n] in vis else HIDDEN, op[i_op],
                   n[i_n + 1] if n[i_n + 1] in vis else HIDDEN, op[i_op + 1],
                   n[i_n + 2] if n[i_n + 2] in vis else HIDDEN]
        
        if asStr: row = ' '.join([str(_) for _ in row])
        return row
    
    def getExprCol(self, col, showAll=False, asStr=False):
        'col should be 0, 1, or 2'
        n = self._numbers
        op = self._operators
        
        i_n = col
        i_op = 2 + col
        col = [n[i_n], op[i_op], n[i_n + 3], op[i_op + 5], n[i_n + 6]]
        
        if asStr: col = ' '.join([str(_) for _ in col])
        return col

    def getOpRow(self, row):
        'row should be 0 or 1'
        op = self._operators
        i_op = 3 * row + 2 * (row + 1)
        row = [op[i_op], EMPTY, op[i_op + 1], EMPTY, op[i_op + 2], EMPTY]
        return row

    
    def asDataFrame(self, showAll=False):
        'Returns a 6x6 grid of numbders, operators and results. Empty cells are EMPTY'
        
        ans = self.getAnswers()
        grid = []
        colAns = []
        for i in range(3):
            grid.append(self.getExprRow(i, showAll) + ans[i:i+1])
            if i != 2:
                grid.append(self.getOpRow(i))
            colAns.extend([ans[i + 3], EMPTY])
        grid.append(colAns)
        
        return pd.DataFrame(grid).fillna(BLANK)
    
    def _printBoard(self, showAll=False):
        'Mostly for dev purposes... Print all 5 rows (3 of expressions separated by 2 rows of operators)'
        
        def printOpRow(row):
            'row should be 0 or 1'
            op = self._operators
            i_op = 3 * row + 2 * (row + 1)
            row = f'{op[i_op]}   {op[i_op + 1]}   {op[i_op + 2]}'
            return row
        
        
        expRows = [self.getExprRow(i, showAll, asStr=True) for i in range(3)]
        # Add row answers
        ans = self.getAnswers()
        expRows = [r + ' |  ' + str(ans[i]) for i, r in enumerate(expRows)]

        
        # Add Column answers
        colAns = ''
        for i in range(3):
            colAns += str(ans[i + 3]) + '   '

        board = ' |\n'.join([
                        # Puzzle and row answers
                        expRows[0], printOpRow(0), expRows[1],
                        printOpRow(1), expRows[2],
                        # Spacing 
                        '-' * 9, '\n',
                        # Column answers
                        colAns
                        ])
        return board
    
    def logGame(self):
        print('Logging game')
        if not self._complete: return None
        fp = r'/Users/chris/Documents/projects/numberGrid/log.txt'
        with open(fp) as f:
            log = f.readlines()
            log.append(f"{self._user}, {self._difficulty}, {self._boardStart}, {self._boardFinish}, {self._complete}")
            # f.write()
            # print('logging\n' * 100)
            
            
    
# Simple tests    
if False:
    board = Board('test', 'easy')
    print(board._printBoard(True))
    print(board.getAnswers())
    
    