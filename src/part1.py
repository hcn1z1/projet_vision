"""Encode and decode the text inside a GRAYSCALE image (for now!)
"""
"""
    *  TODO: find the image format that don't compress so we will not have issues when"sending" things
    *  TODO: use isascsii to check if the characters are okay
        ref: https://realpython.com/python-encodings-guide/
    
"""
import cv2
import argparse
import numpy as np

def parse_args():  
    '''
    my argumets!!
    '''
    parser = argparse.ArgumentParser(description="Image text encoding script.")
    # Path
    parser.add_argument('--impath', nargs='?',default='../img/2000.png',
                        help='Image path')
    #TODO: maybe supprimer!(il faut gerer la taille des donné!)
    parser.add_argument('--path_text', nargs='?',default='./tests/',
                    help='path to the textfile you want to send?')
    parser.add_argument('--text', nargs='?',default='tahya vision',
                    help='path to the textfile you want to send?')

    return parser.parse_args()


def clear_bit(value, bit_index):
    """Set the bit in bit_index to 0.

    Keyword arguments:
    value --  the value as integer. ex: 0b11111111 .
    bit_index -- the bit in the value we want to set to 0.

    Returns:
        the value with the bit_index set to 0.

    Note:
        Thanks to RealPython for the function.
            Check the README references for details.
    """

    return value & ~(1 << bit_index)


def set_bit(value:int, bit_index):
    """Set the bit in bit_index to 1.

    Keyword arguments:
    value --  the value in binary. ex: 0b11111111 .
    bit_index -- the bit in the value we want to set to 1.

    Returns:
        the value with the bit_index set to 1.

    Note:
        Thanks to RealPython for the function.
            Check the README references for details.
    """

    return value | (1 << bit_index)


def get_bit(value:int, bit_index):
    """Get the bit in bit_index to 1.

    Keyword arguments:
    value --  the value as an integer.
    bit_index -- the bit in the value we want to get to 1.

    Returns:
        the value of the bit at bit_index.

    Note:
        Thanks to RealPython for the function.
            Check the README references for details.
        - when the bit_index is greater than the size in bytes of the value, it doenes't throw any error!
    """

    return (value >> bit_index) & 1


def put_bit_in_value(value:int , bit_value, bit_index = 0):
    """Put a bit_value(0 or 1), in the bit_index of a value

    Keyword arguments:
    value --  the value as an integer( the pixel value).
    bit_index -- the bit in the value we want to set to bit_value.
    vit_value -- the value we want to set in the bit_index

    Returns:
        the value with the new bit value in bit_index changed.

    """
    if(bit_value == 1 ):
        value = set_bit(value, bit_index=bit_index)
    else:
        value =  clear_bit(value, bit_index=bit_index)
    return value


def encode_img(text:str, img):
    """Encode the text inside the image."""
    # check if the length is enough or not! 
    print("img shape before encoding ",img.shape)
    h , w= img.shape 
    max_length  = (w * h) / 8
    # int(text_ascii,2) to put from binary to int maybe use numpy 
    if( len(text) < max_length ):
        for i in range(len(text)):#used this cause i need i as a number later
            for j in range(8):
                char_i_j_th_bit = get_bit( ord(text[i])  , bit_index = j )

                #print("the char bit  ",char_i_j_th_bit)
                _i = (i*8+j)//w
                _j = (i*8+j)%w
                img_pixel = img[_i][_j]
                
                #print("img [",k_i,"]","[",k_j,"] = ",img_pixel)
                #print("my img_pixel type before: ",type(img_pixel))
                print("id img[x][y]: ", hex( id( img[_i][_j]) ) )
                #print("img pixel before ", bin(img_pixel))
                img_pixel = put_bit_in_value(img_pixel, char_i_j_th_bit)
                img_pixel = img_pixel.astype(np.uint8) 
                
                img[_i][_j] = img_pixel
                print("id img_pixel",hex(id(img_pixel)))

                #print("img pixel after ", bin(img_pixel))
                    
                #print("the pixel type after: ",type(img_pixel))
                print("\n\n-----------------------------------\n-----------------------------------") 
    else:
        exit("Text too big for the image!")
    return img


def decode_img(img):
    """Decode the text inside the image .
    
    Keyword arguments:
    img -- the image with the code inside

    Returns:
        the text encoded in the image
    
    Note:
    """
    h , w= img.shape 
    img = img.flatten()
    #print("the flatten image:\n",img)
    text=""
    for i in range(0,len(img),8):
        car = chr(255)
        car_ascii= ord(car)
        for j in range(8):
            # get the first pixel
            last_bit_img = get_bit(img[i+j],0)

            car_ascii = put_bit_in_value(value = car_ascii, bit_value=last_bit_img ,bit_index =j) 

        #car = chr(new_val)
        car = chr(car_ascii)
        text = text + car 
        # i don't get why it works but it works, 
        # if we delete this if we will see weird things!
        if(car=="\0"): 
            break
    print("\n\n\n\n\n the text is : ",text)


def main():
    # read the image
    args = parse_args()
    img = cv2.imread(args.impath,cv2.IMREAD_GRAYSCALE)

    #img = cv2.resize(img, (8,8), interpolation = cv2.INTER_AREA)
    print("the image\n",img)
    print("le parcours:\n")
    #print(type(img))#numpy.ndarray
    if img is not None:
        encoded_img = encode_img(img=img,text=args.text)
        cv2.imwrite('../img/encoded_img.png',encoded_img)
        decode_img(encoded_img)
        # TODO: save the image!
    else:
        exit("ERROR NO image or somthing!")
    

if __name__ == '__main__':
    main()