from PIL import Image
import string, os,sys
# Opens the bmp image and verifies its a proper file
def open_bmp(input_image):
   while True: # Loops until valid image is provided
    path = input_image
    path = path.replace('\\', '/') #Formats the directory for proper use
    try: # Checks directory for file
        im = Image.open(path)
    except FileNotFoundError: # Handles file not found error and reprompts
       raise ValueError("File not found. Please check the path and try again.")
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
    elif os.access(im.filename, os.W_OK) == False: # Ensures file is writable
        print("File is not writable, please check the file permissions")
        continue
    else: # Returns the image if everything is valid
        return im
# Embeds a message into the bmp file and stores the message length in the bottom right using LSB
def encode_bmp(input_image, output_image, input_message):
    testim = open_bmp(input_image) # Opens the image
    pixels = testim.load() #Loads all of the RGB values into an array
    #Used to keep track of the array indexes for future use
    image_index_x = 0 
    image_index_y = 0
    array_index = 0
    final_message = ""
    message = input_message
    # Verifies message is of proper length and is ASCII
    if len(message) > 512:
            raise ValueError("Message is longer than 512 characters")
    if not message.isascii():
        raise ValueError("Message must only contain ASCII characters")
    #Formats the entire message into binary for LSB
    for i in range(len(message)):
        curr_char = format(ord(message[i]), '08b')
        final_message += curr_char
    # Goes through the entire message and adds it to the image
    while array_index < len(final_message):
            R, G, B = pixels[image_index_x,image_index_y]
            new_r = R
            new_g = G
            new_b = B
            if array_index < len(final_message): # Ensures file does not go over length
                new_r_binary = format(R,'08b') #Formats the int to binary
                new_r_binary = new_r_binary[:-1] + final_message[array_index] # Adds the current message bit to the end of the RGB
                new_r = int(new_r_binary, 2) # Converts it back to int
                array_index +=1 #Moves to the next bit
            if array_index < len(final_message):
                new_g_binary = format(G,'08b')
                new_g_binary = new_g_binary[:-1] + final_message[array_index]
                new_g = int(new_g_binary, 2)
                array_index += 1
            if array_index < len(final_message):
                new_b_binary = format(B, '08b')
                new_b_binary = new_b_binary[:-1] + final_message[array_index]
                new_b = int(new_b_binary, 2)
                array_index += 1
            if image_index_x >= testim.size[0]-1: #If we hit the end, it goes to the next row and starts again
                pixels[image_index_x, image_index_y] = (new_r, new_g, new_b)
                image_index_x = 0
                image_index_y +=1
            else: #Adds the RGB values back to the image
                pixels[image_index_x, image_index_y] = (new_r, new_g, new_b)
                image_index_x +=1
    message = format(len(final_message), '016b') #Formats the message length in 16 bit to store more values
    #Encodes the message length into the bottom right
    def encode_pixel(pixel_index, message, message_index):
        x = testim.size[0] - pixel_index
        y = testim.size[1] - 1
        R, G, B = pixels[x, y]
        #Sets the R pixel
        R_binary = format(R, '08b')
        R_binary = R_binary[:-1] + message[message_index]
        R = int(R_binary, 2)
        # Sets the G pixel
        G_binary = format(G, '08b')
        G_binary = G_binary[:-1] + message[message_index + 1]
        G = int(G_binary, 2)
        #Sets the B pixel
        B_binary = format(B, '08b')
        B_binary = B_binary[:-1] + message[message_index + 2]
        B = int(B_binary, 2)
        pixels[x, y] = (R, G, B)
    #Goes through pixels 6-1 in the bottom right
    for i in range(5):
        encode_pixel(6-i, message,i*3)
    
    # Manually sets the last pixel
    R6, G6, B6 = pixels[testim.size[0] - 1, testim.size[1] - 1]
    R6_binary = format(R6, '08b')
    R6_binary = R6_binary[:-1] + message[15]
    R6 = int(R6_binary, 2)
    pixels[testim.size[0] - 1, testim.size[1] - 1] = (R6, G6, B6)

    try: # Checks directory for file
        im = Image.open(output_image)
    except FileNotFoundError: # Handles file not found error and reprompts
       raise ValueError("File not found. Please check the path and try again.")
    testim.save(output_image)
def main():
    if len(sys.argv) == 4: #Verifies that argument list is of proper size
        encode_bmp(sys.argv[1], sys.argv[2], sys.argv[3])
    else: #Lets the user they used the wrong number of arguments
        print("Invalid arguments used")
if __name__ == "__main__": # Runs the main method
    main()