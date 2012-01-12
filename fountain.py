import random
from droplet import Droplet
from math import ceil
from utils import xor, randChunkNums

class Fountain:
    def __init__(self, data, chunk_size=32, seed=None):
        self.data = data
        self.chunk_size = chunk_size
        self.num_chunks = int(ceil(len(data) / float(chunk_size)))
        self.seed = seed
        random.seed(seed)
        
    def droplet(self):
        self.updateSeed()
        chunk_nums = randChunkNums(self.num_chunks)
        data = None
        for num in chunk_nums:
            if data is None:
                data = self.chunk(num)
            else:
                data = xor(data, self.chunk(num))
        
        return Droplet(data, self.seed, self.num_chunks)
        
    def chunk(self, num):
        start = self.chunk_size * num
        end = min(self.chunk_size * (num+1), len(self.data))
        return self.data[start:end]
        
    def updateSeed(self):
        self.seed = random.randint(0,2**31-1)
        random.seed(self.seed)
