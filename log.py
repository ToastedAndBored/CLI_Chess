_PAD = 0
_LOG = []
_LOG_DEEP = 999999 # Just very large number

PAD_INC = 1

# Clears $_LOG
def clear():
	global _LOG
	global _PAD
	_LOG = []
	_PAD = 0
	_LOG_DEEP = 999999

def trim_deep(deep):
	global _LOG_DEEP
	_LOG_DEEP = deep

# Returns $_LOG
def dump():
	return _LOG

# Update $_PAD
def pad(c):
	global _PAD
	_PAD += c

# Just a boilerolate to work with "with" statement
class _NewPad:
	def __init__(self, count):
		self.count = count
	def __enter__(self):
		global _PAD
		_PAD+=self.count
	def __exit__(self, *args):
		global _PAD
		_PAD-=self.count

# Same as "_NewPad()" but looks nice
def newpad(count=PAD_INC):
	return _NewPad(count)

# Decoreator that add padding to all log.log calls nested in function
def defpad(func):
	def wrapped(*args, **kwargs):
		with newpad():
			return func(*args, **kwargs)
	return wrapped

# Just like print() but returns a string
def format_print(*args):
	ret = ""
	for i, arg in enumerate(args):
		if i > 0:
			ret += " "
		ret += str(arg)
	return ret

# Shift each line in $text $rows spaces left
def shift_text(text, rows):
	ret = ""
	for line in text.splitlines():
		ret += rows*" "+line+"\n"
	return ret

# Log
def log(*args, print=False):
	global _LOG
	if _PAD > _LOG_DEEP:
		return
	if print:
		print(shift_text(format_print(*args), _PAD))
	else:
		_LOG.append(shift_text(format_print(*args), _PAD))

# Reset terminal colors to normal
def reset_colors():
	pass # TODO

# Prints $_LOG
def show(lg=_LOG):
	for e in lg:
		reset_colors()
		print(e, end="")
	reset_colors()
	print()







