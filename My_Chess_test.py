import My_Chess as chess

chess.DEBUG = True


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

def test_pawn():
	pass
def test_tower():
	pass
def test_bishop():
	pass
def test_knight():
	pass
def test_queen():
	pass
def test_king():
	pass

tests = [
	test_remove_chars_whitelist,
	test_new_board,
]

def main():
	results = []
	ok = True
	for test in tests:
		name = str(test).split(" ")[1].removeprefix("test_")
		try:
			result = test()
			status = 1
			if result is None:
				status = 0
			else:
				ok = False
			results.append((name, status, result))
		except Exception as e:
			ok = False
			results.append((name, 2, e))
	results.sort(key=lambda x: x[1])
	print("\n")
	for result in results:
		if result[1] == 2:
			print(f"{result[0]} \033[91m[EXCEPT]\033[0m")
			raise result[2]
		if result[1] == 1:
			print(f"{result[0]} \033[91m[ERR]\033[0m")
			print(result[2])
		else:
			print(f"{result[0]} \033[92m[OK]\033[0m")
	print("\n")
	if ok:
		print("\033[92mAll tests were passed!!11!\033[0m")
if __name__ == "__main__":
    main()


