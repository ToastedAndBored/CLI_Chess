import log

_TESTS = []
_CODE_OK = 0
_CODE_ERR = 1
_CODE_EXC = 2

def test(t):
	global _TESTS
	_TESTS.append(t)

def show_log(lg):
	print("------LOG START-----")
	log.show(lg)
	print("-------LOG END------")

# Test result scheme: {"name", "type", "result", "log"}
# Where:
#  name - test name
#  type = "ok" or "error" or "exception"
#  result - returned object or raised exception
#  log - log dump

def run():
	results = []
	all_passed = True
	for test in _TESTS:
		log.clear()
		name = str(test).split(" ")[1] # Gets function name
		print(("="*10)+name+("="*10))
		name = name.removeprefix("test_")
		try:
			result = test()
			status = _CODE_ERR
			if result is None:
				status = _CODE_OK
			else:
				all_passed = False
			results.append({"name": name, "status": status, "result": result, "log":log.dump()})
		except Exception as e:
			all_passed = False
			results.append({"name": name, "status": _CODE_EXC, "result": e, "log":log.dump()})
	results.sort(key=lambda x: x["status"])
	for result in results:
		name = result["name"]
		if result["status"] == _CODE_EXC:
			print(f"{name} \033[91m[EXCEPT]\033[0m")
			show_log(result["log"])
			raise result["result"]
		if result["status"] == _CODE_ERR:
			print(f"{name} \033[91m[ERR]\033[0m")
			show_log(result["log"])
			print(result["result"])
		else:
			print(f"{name} \033[92m[OK]\033[0m")
	print("\n")
	if all_passed:
		print("\033[92mAll tests were passed!!11!\033[0m")



