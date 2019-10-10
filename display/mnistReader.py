import gzip

with gzip.open('../mnist/t10k-images-idx3-ubyte.gz', 'rb') as f:
    file_content = f.read()

def getImageArray2DTest(position,array):
    pos = 16 + (position-1)*28*28
    for k in range(0,28):
        for j in range(0,28):
           array[k][j] = int.from_bytes(file_content[pos:pos+1], byteorder='big')
           pos = pos+1 

def displayImageConsole(imageArray):
    for k in range(0,28):
        for j in range(0,28):
            print("%3d"%imageArray[k][j], end="", flush=True)
        print()

w, h = 28, 28;
Matrix = [[0 for x in range(w)] for y in range(h)] 
getImageArray2DTest(1,Matrix)
displayImageConsole(Matrix)

