import random

def charN(str, N):
	if N < len(str):
		return str[N]
	return 'X'
	
def xor(str1, str2):
	length = max(len(str1),len(str2))
	return ''.join(chr(ord(charN(str1,i)) ^ ord(charN(str2,i))) for i in xrange(length))

def randChunkNums(num_chunks):
	size = random.randint(1,min(5, num_chunks))
	return random.sample(xrange(num_chunks), size)