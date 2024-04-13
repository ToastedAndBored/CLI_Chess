def abcd():
	yield "a"
	yield "b"
	yield "c"
	yield "d"


y = abcd()

for i in y:
	print(i)

