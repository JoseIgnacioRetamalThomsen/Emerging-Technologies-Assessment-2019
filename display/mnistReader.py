import gzip


class Reader:

    def __init__(self, labels, images):
        with gzip.open(labels, 'rb') as f:
            self.labels = f.read()
        self.labelMagic = int.from_bytes(self.labels[0:4], byteorder='big')
        self.labelTotal = int.from_bytes(self.labels[4:8], byteorder='big')
        print("Labels Magic Number:" + str(self.labelMagic))
        print("total:" + str(self.labelTotal))
        with gzip.open(images, 'rb') as f:
            self.images = f.read()
        self.imagesMagic = int.from_bytes(self.images[0:4], byteorder='big')
        self.imagesTotal = int.from_bytes(self.images[4:8], byteorder='big')
        self.imagesRow = int.from_bytes(self.images[8:12], byteorder='big')
        self.imagesCol = int.from_bytes(self.images[12:16], byteorder='big')
        print("Images Magic Number:" + str(self.imagesMagic))
        print("total:" + str(self.imagesTotal))
        print("Row/Col: " + str(self.imagesRow)+"/"+str(self.imagesCol))

        self.array = [[0 for x in range(self.imagesRow)]
                      for y in range(self.imagesRow)]

    def displayImageConsole(self, position):
        self.getImageArray2D1(position, self.array)
        for k in range(0, 28):
            for j in range(0, 28):
                print("%2s" % self.array[k][j].hex(), end="", flush=True)
            print()

    def getImageArray2D1(self, position, array):
        pos = 16 + (position-1)*28*28
        for k in range(0, 28):
            for j in range(0, 28):
                array[k][j] = int.from_bytes(
                    self.images[pos:pos+1], byteorder='big')
                #array[k][j] = self.images[pos:pos+1]
                pos = pos+1

    def getImageArray2D2(self, position):
        getImageArray2D1(position, self.array)
        return self.array

    def getLabel(self, position):
        return int.from_bytes(self.labels[position+7:position+8], byteorder='big')

    def printLabel(self, position):
        print(str(self.getLabel(position)))

    def getArray(self):
        return self.array


# reader = Reader('../mnist/train-labels-idx1-ubyte.gz',
#                 '../mnist/train-images-idx3-ubyte.gz')
# reader.printLabel(60000)
# reader.displayImageConsole(60000)

# C:\Users\pepe\Anaconda3\python
