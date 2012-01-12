import random
from utils import randChunkNums

class Droplet:
	def __init__(self, data, seed, num_chunks):
		self.data = data
		self.seed = seed
		self.num_chunks = num_chunks
		
	def chunkNums(self):
		random.seed(self.seed)
		return randChunkNums(self.num_chunks)
