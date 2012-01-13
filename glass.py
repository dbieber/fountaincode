from utils import xor

class Glass:
    def __init__(self, num_chunks):
        self.entries = []
        self.droplets = []
        self.num_chunks = num_chunks
        self.chunks = [None] * num_chunks
        
    def addDroplet(self, d):
        self.droplets.append(d)
        entry = [d.chunkNums(), d.data]
        self.entries.append(entry)
        self.updateEntry(entry)
        
    def updateEntry(self, entry):
        for chunk_num in entry[0]:
            if self.chunks[chunk_num] is not None:
                entry[1] = xor(entry[1], self.chunks[chunk_num])
                entry[0].remove(chunk_num)
        if len(entry[0]) == 1:
            self.chunks[entry[0][0]] = entry[1]
            self.entries.remove(entry)
            for d in self.entries:
                if entry[0][0] in d[0]:
                    self.updateEntry(d)
                    
    def getString(self):
        return ''.join(x or ' _ ' for x in self.chunks)
        
    def isDone(self):
        return None not in self.chunks

    def chunksDone(self):
        count = 0
        for c in self.chunks:
            if c is not None:
                count+=1