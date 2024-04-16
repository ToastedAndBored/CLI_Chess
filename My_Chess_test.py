import My_Chess as chess
import log as logging
from log import log, defpad, newpad, clear, show, reset_colors, dump, trim_deep
import test
from itertools import chain
import sys
import math


@test.test
def test_remove_chars_whitelist():
	cases = [
		["123456abcd12345", "12", "1212"],
		["123456abcd12345", "13", "1313"],
		[
			"\n\t1 □□□□□□□□\n\t2 □□□□□□□□\n\t3 □□□□□□□□\n\t4 □□□□□□♚□\n\t5 □□□□□♙♙□\n\t6 □□♔□□□□□\n\t7 □□□□□□□□\n\t8 □□□□□□□□\n\t  12345678\n",
			"♜♞♝♛♚♟♙♖♘♗♕♔□\n",
			"\n□□□□□□□□\n□□□□□□□□\n□□□□□□□□\n□□□□□□♚□\n□□□□□♙♙□\n□□♔□□□□□\n□□□□□□□□\n□□□□□□□□\n\n",
		],
	]
	for case in cases:
		result = chess.remove_chars_whitelist(case[0], case[1])
		if result != case[2]:
			return case, result

@test.test
def test_new_board():
	cases = [
		[
			"\n♜♞♝♛♚♝♞♜\n♟♟♟♟♟♟♟♟\n□□□□□□□□\n□□□□□□□□\n□□□□□□□□\n□□□□□□□□\n♙♙♙♙♙♙♙♙\n♖♘♗♕♔♗♘♖\n\n",
			["♜♞♝♛♚♝♞♜", "♟♟♟♟♟♟♟♟", "□□□□□□□□","□□□□□□□□","□□□□□□□□","□□□□□□□□","♙♙♙♙♙♙♙♙","♖♘♗♕♔♗♘♖"],
		],
		[
			"\n\t1 □□□□□□□□\n\t2 □□□□□□□□\n\t3 □□□□□♚□□\n\t4 □□□□□□□□\n\t5 □□□□□□□□\n\t6 □□♔□□♙♙□\n\t7 □□□□□□□□\n\t8 □□□□□□□□\n\t12345678\n\n",
			["□□□□□□□□","□□□□□□□□","□□□□□♚□□","□□□□□□□□","□□□□□□□□","□□♔□□♙♙□","□□□□□□□□","□□□□□□□□"]
		],
		[
			"\n♜♞♝♛♚♝♞♜\n♟♟♟♟♟♟♟♟\n□□□□□□□□\n□□□□□□□□\n□□□□□□□□\n♙♙♙♙♙♙♙♙\n♖♘♗♕♔♗♘♖\n\n",
			Exception("WRONG INIT ROWS COUNT"),
		],
		[
			"♜♞♝♛♚♝♞♜\n♟♟♟♟♟♟♟♟\n□□□□□□□□\n□□  □□□□\n□□□□□□□□\n□□□□□□□□\n♙♙♙♙♙♙♙♙\n♖♘♗♕♔♗♘♖\n\n",
			Exception("WRONG INIT LINE SIZE"),
		],
		[
			"♜♞♝♛♚♝♞♜\n♟♟♟♟♟♟♟\n□□□□□□□□\n□□□□□□□□\n□□□□□□□□\n□□□□□□□□\n♙♙♙♙♙♙♙♙\n♖♘♗♕♔♗♘♖\n\n",
			Exception("WRONG INIT LINE SIZE"),
		],
	]
	for case_num, case in enumerate(cases):
		inp = case[0]
		out = case[1]
		if isinstance(out, Exception):
			exc = None
			try:
				chess.new_board(inp)
			except Exception as e:
				exc = e
			if exc is None:
				return f"In case {case_num} shoud be raised '{out}' but it didnt"
			if str(exc) != str(out):
				return f"In case {case_num} shoud be raised '{out}' but was raised '{exc}'"
			continue
		out = list(map(lambda x: list(x), out))
		case[1] = out
		result = chess.new_board(inp)
		for i in range(len(result)):
			if out[i] != result[i]:
				return f"In case {case_num} on line {i} difference:\n'{out[i]}'\n'{result[i]}'"
		if result != out:
			return case, result

@test.test
def test_collision():
	cases = [
		[
			"""
			  01234567
			0 ♗□□□□□□□
			1 □□□□□□□□
			2 □□□□□□□□
			3 □□□□□□□□
			4 □□□□♗□□□
			5 □□□□□□□□
			6 ♙♙♙♙♙♙♙♙
			7 ♖♘♗♕♔♗♘♖
			""",
			[0, 0],
			[4, 4],
			True, # No collisions
		],
		[
			"""
			  01234567
			0 ♗□□□□□□□
			1 □□□□□□□□
			2 □□□□□□□□
			3 □□□□□□□□
			4 □□□□♗□□□
			5 □□□□□□□□
			6 ♙♙♙♙♙♙♙♙
			7 ♖♘♗♕♔♗♘♖
			""",
			[4, 4],
			[0, 0],
			True, # No collisions
		],
		[
			"""
			  01234567
			0 ♗□□□□□□□
			1 □□□□□□□□
			2 □□□□□□□□
			3 □□□□□□□□
			4 □□□□□□□□
			5 □□□□□□□□
			6 □□□□□□□□
			7 □□□□□□□□
			""",
			[0, 0],
			[10, 10],
			IndexError('list index out of range'),
		],
	]
	for case in cases:
		result = 0
		if isinstance(case[3],Exception):
			case[3] = str(case[3])
			try:
				chess.collision(chess.new_board(case[0]), case[1], case[2])
			except Exception as e:
				result = str(e)
		else:
			result = chess.collision(chess.new_board(case[0]), case[1], case[2])
		if result != case[3]:
			return case, result

# gen_board([[y, x, p], [y1, x1, p1]]) -> board 
# ["♜□□□□□□□", "♖□□□□□□□", "□□□□□□□□","□□□□□□□□","□□□□□□□□","□□□□□□□□","□□□□□□□□","□□□□□□□□"]
def gen_board(*args):
	board = chess.new_board(
		"""
			  01234567
			0 □□□□□□□□
			1 □□□□□□□□
			2 □□□□□□□□
			3 □□□□□□□□
			4 □□□□□□□□
			5 □□□□□□□□
			6 □□□□□□□□
			7 □□□□□□□□
			""")
	for piece in args:
		board[piece[0]][piece[1]] = piece[2]
	return board

# ♛ = "♛"
# gen_board((1, 2, ♜), (4, 5, ♛))
def verticalHorizontal(piece, color, opposite, victims):
	for y in range(0,8):
		for x in range(0,8):
			for h in range(0,8):
					if h != y:
						# Step to void
						yield [[[y,x],[h,x]],gen_board((y,x,piece)),color,True]
						# Attac
						yield [[[y,x],[h,x]],gen_board((y,x,piece), (h,x,victims[0])),color,True]
						# Wrong order (color)
						yield [[[y,x],[h,x]],gen_board((y,x,piece)),opposite,False]
						# Blocked
						yield [[[y,x],[h,x]],gen_board((y,x,piece), (math.ceil((h+y)/2),x,piece), (math.floor((h+y)/2),x,piece)),color,False]
					if h != x:
						# Step to void
						yield [[[y,x],[y,h]],gen_board((y,x,piece)),color,True]
						# Attac
						yield [[[y,x],[y,h]],gen_board((y,x,piece), (y,h,victims[0])),color,True]
						# Wrong order (color)
						yield [[[y,x],[y,h]],gen_board((y,x,piece)),opposite,False]
						# Blocked
						yield [[[y,x],[y,h]],gen_board((y,x,piece), (y,math.ceil((h+x)/2),piece), (y, math.floor((h+x)/2),piece)),color,False]

def diagonal(piece, color, opposite_color, victims):
	for y in range(0,8):
		for x in range(0,8):
			for h in range(-8,8):
					ny = y+h
					nx = x+h
					nnx = x-h
					if ny == y or nx == x or nnx == x:
						continue
					if ny < 0 or ny > 7 or nx < 0 or nx > 7 or nnx < 0 or nnx > 7:
						continue
					# Step to void ⇗⇙ 
					yield [[[y,x],[ny,nx]],gen_board((y,x,piece)),color,True]
					# Step to void ⇘⇖
					yield [[[y,x],[ny,nnx]],gen_board((y,x,piece)),color,True]
					# Attac
					yield [[[y,x],[ny,nx ]],gen_board((y,x,piece), (ny,nx ,victims[0])),color,True]
					yield [[[y,x],[ny,nnx]],gen_board((y,x,piece), (ny,nnx,victims[0])),color,True]
					# Blocked
					if abs(h) == 1:
						continue # No space between attacker and victim
					h = h//2
					by = y+h
					bx = x+h
					bnx = x-h
					yield [[[y,x],[ny,nx ]],gen_board((y,x,piece), (by,bx ,piece), (ny,nx ,victims[0])),color,False]
					yield [[[y,x],[ny,nnx]],gen_board((y,x,piece), (by,bnx,piece), (ny,nnx,victims[0])),color,False]

def kingTurn(piece, color, opposite_color, victims):
	for y in range(0,8):
		for x in range(0,8):
			for yy in range(0,8):
				for xx in range(0,8):
					if (abs(y-yy)<=1 and abs(x-xx)<=1) and ((y-yy)!=0 or (x-xx)!=0):
						# Step to void
						yield [[[y,x],[yy,xx]],gen_board((y,x,piece)),color,True]
						# Attac
						yield [[[y,x],[yy,xx]],gen_board((y,x,piece),(yy,xx,victims[0])),color,True]
						# Blocked
						yield [[[y,x],[yy,xx]],gen_board((y,x,piece),(yy,xx,piece)),color,False]
					else:
						yield [[[y,x],[yy,xx]],gen_board((y,x,piece)),color,False]

def knightTurn(piece, color, opposite_color, victims):
	for y in range(0,8):
		for x in range(0,8):
			for yy in range(0,8):
				for xx in range(0,8):
					if (abs(y-yy)==1 and abs(x-xx)==2) or (abs(x-xx)==1 and abs(y-yy)==2):
						# Step to void
						yield [[[y,x],[yy,xx]],gen_board((y,x,piece)),color,True]
						# Attac
						yield [[[y,x],[yy,xx]],gen_board((y,x,piece),(yy,xx,victims[0])),color,True]
						# Blocked
						yield [[[y,x],[yy,xx]],gen_board((y,x,piece),(yy,xx,piece)),color,False]
					else:
						yield [[[y,x],[yy,xx]],gen_board((y,x,piece)),color,False]	

def outOfBounds(piece, color):
	for y in range(-1,9):
		for x in range(-1,9):
			if 0<=x<=8 or 0<=y<=8:
				continue
			yield [[[1,2],[x,y]],gen_board((1,2,piece)),color,False]
			yield [[[x,y],[1,2]],gen_board((1,2,piece)),color,False]

def wrongTower(piece,color):
	for y in range(0,8):
		for x in range(0,8):	
			for yy in range(0,8):
				for xx in range(0,8):
					if yy==y or xx==x:
						continue
					#Wrong mechanical turn for Tower
					yield [[[y,x],[yy,xx]],gen_board((y,x,piece)),color,False]

def wrongBishop(piece,color):
	for y in range(0,8):
		for x in range(0,8):	
			for yy in range(0,8):
				for xx in range(0,8):
					if abs(y-yy)==abs(x-xx):
						continue
					yield [[[y,x],[yy,xx]],gen_board((y,x,piece)),color,False]

def wrongQueen(piece,color):
	for y in range(0,8):
		for x in range(0,8):	
			for yy in range(0,8):
				for xx in range(0,8):
					if abs(y-yy)==abs(x-xx):
						continue
					if yy==y or xx==x:
						continue
					yield [[[y,x],[yy,xx]],gen_board((y,x,piece)),color,False]
@defpad
def gen_case(piece):
	color, opposite, victims = \
		("black", "white", chess.white_p) \
		if piece in chess.black_p else \
		("white", "black", chess.black_p)
	for ob in outOfBounds(piece,color):
		yield ob
	if piece in ["♜", "♛", "♖", "♕"]:
		for vh in verticalHorizontal(piece,color,opposite,victims):
			yield vh
	if piece in ["♝", "♛", "♗", "♕"]:
		for d in diagonal(piece,color,opposite,victims):
			yield d
	if piece in ["♜","♖"]:
		for wvh in wrongTower(piece,color):
			yield wvh
	if piece in ["♝","♗"]:
		for wd in wrongBishop(piece,color):
			yield wd
	if piece in ["♕","♛"]:
		for wq in wrongQueen(piece,color):
			yield wq
	if piece in ['♚','♔']:
		for kt in kingTurn(piece,color,opposite,victims):
			yield kt
	if piece in ['♞','♘']:
		for kt in knightTurn(piece,color,opposite,victims):
			yield kt
	
@test.test
def test_pawn():
	cases = [
			[[[7,1],[6,1]],
			["♜♞♝♛♚♝♞♜", "♟♟♟♟♟♟♟♟", "□□□□□□□□","□□□□□□□□","□□□□□□□□","□□□□□□□□","♙♙♙♙♙♙♙♙","♖♘♗♕♔♗♘♖"],
			"white",
			True]
		]
	for case in cases:
		case[0][0][0]-=1
		case[0][0][1]-=1
		case[0][1][0]-=1
		case[0][1][1]-=1
		result = chess.check_step(case[0],case[1],case[2])
		if result != case[3]:
			return case, result

@test.test
def test_tower():
	cases = chain(gen_case("♖"), gen_case("♜"))
	for case in cases:
		result = chess.check_step(case[0],case[1],case[2])
		if result != case[3]:
			return case, result

@test.test
def test_bishop():
	trim_deep(3)
	log("Log from test_bishop Yay")
	cases = chain(gen_case("♗"), gen_case("♝"))
	for case in cases:
		with newpad():
			result = chess.check_step(case[0],case[1],case[2])
		if result != case[3]:
			msg = str(case[0])+" "+str(case[2:])+"\n"+str(result)+"\n"+chess.print_board(case[1])
			return msg
		#else:
		#	msg = str(case[0])+" "+str(case[2:])+"\n"+str(result)+"\n"+chess.print_board(case[1])
	#return "allways fails"
			

@test.test
def test_knight():
	trim_deep(3)
	log("Log from test_knight Yay")
	cases = chain(gen_case("♞"), gen_case("♘"))
	for case in cases:
		with newpad():
			result = chess.check_step(case[0],case[1],case[2])
		if result != case[3]:
			msg = str(case[0])+" "+str(case[2:])+"\n"+str(result)+"\n"+chess.print_board(case[1])
			return msg

@test.test
def test_queen():
	log("Log from test_queen Yay")
	cases = chain(gen_case("♕"), gen_case("♛"))
	for case in cases:
		result = False
		try:
			result = chess.check_step(case[0],case[1],case[2])
		except IndexError:
			pass
		if result != case[3]:
			msg = str(case[0])+" "+str(case[2:])+"\n"+str(result)+"\n"+chess.print_board(case[1])
			return msg

@test.test
def test_king():
	trim_deep(3)
	log("Log from test_king Yay")
	cases = chain(gen_case("♚"), gen_case("♔"))
	for case in cases:
		with newpad():
			result = chess.check_step(case[0],case[1],case[2])
		if result != case[3]:
			msg = str(case[0])+" "+str(case[2:])+"\n"+str(result)+"\n"+chess.print_board(case[1])
			return msg

@test.test
def test_apply_step():
	pass

if __name__ == "__main__":
    test.run()

