from PIL import Image
import string, os,sys
def open_bmp(input_image):
   while True: # Loops until valid image is provided
    path = input_image
    path = path.replace('\\', '/')
    try: # Checks directory for file
        im = Image.open(path)
    except (FileNotFoundError, OSError): # Handles file not found/os error error and reprompts
       print("File not found or corrupted. Please check the path and try again.")
       continue    
    if im.format != 'BMP': # Ensures proper image format
        print("Incorrect file format, please input a BMP file")
        continue
    elif os.path.getsize(im.filename) > 5000000: # Ensures proper size
        print("File size exceeds 5MB, please input a smaller file")
        continue
    elif os.access(im.filename, os.R_OK) == False: # Ensures file is readable
        print("File is not readable, please check the file permissions")
        continue
    else: # Returns the image if everything is valid
        return im
def decode_bmp(input_image):
    image = open_bmp(input_image) #Opens the image
    pixels = image.load() # Loads the RGB of the image into an array
    length = ""
    #Goes through the bottom right and gets the length from the RGB
    for i in range(5):
        R, G, B = pixels[image.size[0] - 6 + i, image.size[1] - 1]
        R_bin = format(R, '08b')
        G_bin = format(G, '08b')
        B_bin = format(B, '08b')
        length += R_bin[-1] + G_bin[-1] + B_bin[-1]
    #Gets the last bit to make 16
    R,G,B = pixels[image.size[0] - 1, image.size[1] - 1]
    R_bin = format(R, '08b')
    length += R_bin[-1]
    length = int(length, 2) #Formats it to be an int
    #X and Y used to navigate the image
    index_x = 0
    index_y = 0
    word = ""
    message = ""
    #Keeps going through the image decoding the LSB
    while length > 0:
        R,G,B = pixels[index_x, index_y]
        r_bin = R
        g_bin = G
        b_bin = B
        #Checks to make sure there is still another bit
        if length > 0:
            #Gets the last bit and adds it to word
            r_bin = format(R, '08b')
            r_bin = r_bin[-1]
            word += r_bin
            #If there is 8 bits, converts it to a char and adds it to message and resets word
            if len(word) == 8:
                message += chr(int(word, 2))
                word = ""
            length -= 1
        if length > 0:
            g_bin = format(G, '08b')
            g_bin = g_bin[-1]
            word += g_bin
            if len(word) == 8:
                message += chr(int(word, 2))
                word = ""
            length -= 1
        if length > 0:
            b_bin = format(B, '08b')
            b_bin = b_bin[-1]
            word += b_bin
            if len(word) == 8:
                message += chr(int(word, 2))
                word = ""
            length -= 1
        index_x +=1 #Moves to the next part of the array
        if index_x >= image.size[0]: #If we hit the end, we move to the next row and reset
                index_x = 0
                index_y +=1
    print(message) #Returns the decoded message
def main():
    if len(sys.argv) == 2: #Checks to make sure proper number of args are used
        decode_bmp(sys.argv[1])
    else:
        print("Invalid arguments used")
if __name__ == "__main__": #Runs the main method
        main()