import My_Chess as chess
from itertools import chain
import sys
import math


CHLOG = False
LOG = []

def chlogon(on):
	global CHLOG
	CHLOG = on

def chlog(*args, **kwargs):
	if CHLOG:
		LOG.append((args, kwargs))

def log(*args, **kwargs):
	LOG.append((args, kwargs))

def show_log(lg):
	print("------LOG START-----")
	for l in lg:
		print(*l[0], **l[1])
	print("-------LOG END------")

chess.log = chlog
chess.DEBUG = True

tests = []

def test(t):
	global tests
	tests.append(t)

@test
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

@test
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

@test
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

def gen_case(piece):
	color, opposite, victims = \
		("black", "white", chess.white_p) \
		if piece in chess.black_p else \
		("white", "black", chess.black_p)
	# Check out of bounds
	for y in range(-1,9):
		for x in range(-1,9):
			if 0<=x<=8 or 0<=y<=8:
				continue
			yield [[[1,2],[x,y]],gen_board((1,2,piece)),color,False]
			yield [[[x,y],[1,2]],gen_board((1,2,piece)),color,False]
	# Check wrong color
	yield [[[1,1],[2,2]],gen_board((1,1,piece),(2,2,piece)),opposite,False]
	# Check Turn
	for y in range(0,8):
		for x in range(0,8):
			#Check Vertical and Horizontal
			if piece in ["♜", "♛", "♖", "♕"]:
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
					if piece in ["♜","♖"]:
						for j in range(0,8):
							if h==y or j==x:
								continue
							#Wrong turn for Tower
							yield [[[y,x],[h,j]],gen_board((y,x,piece)),color,False]
				#Check Dioganal
				if piece in ["♝", "♛", "♗", "♕"]:
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
						if piece in ["♝","♗"]:
							# Blocked
							yield [[[y,x],[ny,nx ]],gen_board((y,x,piece), (math.ceil(ny/2),nx ,piece), (math.floor(ny/2),nx ,piece)),color,False]
							yield [[[y,x],[ny,nnx]],gen_board((y,x,piece), (math.ceil(ny/2),nnx,piece), (math.floor(ny/2),nnx,piece)),color,False]
							for j in range(0,8):
									if h!=y or j!=x:
										continue
									#Wrong turn for Bishop
									yield [[[y,x],[y,nx ]],gen_board((y,x,piece)),color,False]
									yield [[[y,x],[y,nnx]],gen_board((y,x,piece)),color,False]
									yield [[[y,x],[ny,x]],gen_board((y,x,piece)),color,False]
									yield [[[y,x],[ny,x]],gen_board((y,x,piece)),color,False]
			if piece in ["♕","♛"]:
				for h in range(0,8):
					ny = y+h
					nx = x+h
					nnx = x-h
					if ny == y or nx == x or nnx == x:
						continue
					if ny < 0 or ny > 7 or nx < 0 or nx > 7 or nnx < 0 or nnx > 7:
						continue
					for j in range(0,8):
						if h!=y or j!=x:
						#Wrong turn for Queen
							yield [[[y,x],[y,nx ]],gen_board((y,x,piece)),color,False, "commet"]
							#yield [[[y,x],[y,nnx]],gen_board((y,x,piece)),color,False]
							#yield [[[y,x],[ny,x]],gen_board((y,x,piece)),color,False]
							#yield [[[y,x],[ny,x]],gen_board((y,x,piece)),color,False]
							log('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
						else:
							log('a')
							#yield [[[y,x],[h,j]],gen_board((y,x,piece)),color,False]
						pass
				#     проверка под углом
				#	отдельная логика для коня пешки
				pass # yield

@test
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

@test
def test_tower():
	cases = chain(gen_case("♖"), gen_case("♜"))
	for case in cases:
		result = chess.check_step(case[0],case[1],case[2])
		if result != case[3]:
			return case, result

@test
def test_bishop():
	log("Log from test_bishop Yay")
	cases = chain(gen_case("♗"), gen_case("♝"))
	for case in cases:
		result = chess.check_step(case[0],case[1],case[2])
		if result != case[3]:
			return case, result

@test
def test_knight():
	pass

@test
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

@test
def test_king():
	pass

@test
def test_apply_step():
	pass

def main():
	global LOG
	global CHLOG
	results = []
	ok = True
	for test in tests:
		LOG = []
		CHLOG = False
		name = str(test).split(" ")[1]
		print(("="*10)+name+("="*10))
		name = name.removeprefix("test_")
		try:
			result = test()
			status = 1
			if result is None:
				status = 0
			else:
				ok = False
			results.append((name, status, result, LOG))
		except Exception as e:
			ok = False
			results.append((name, 2, e, LOG))
	results.sort(key=lambda x: x[1])
	print("\n")
	for result in results:
		if result[1] == 2:
			print(f"{result[0]} \033[91m[EXCEPT]\033[0m")
			show_log(result[3])
			raise result[2]
		if result[1] == 1:
			print(f"{result[0]} \033[91m[ERR]\033[0m")
			show_log(result[3])
			print(result[2])
		else:
			print(f"{result[0]} \033[92m[OK]\033[0m")
	print("\n")
	if ok:
		print("\033[92mAll tests were passed!!11!\033[0m")

if __name__ == "__main__":
    main()

