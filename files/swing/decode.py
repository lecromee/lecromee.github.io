import sys
import os

# A decode of secret messages sent to Swing android application.
# The message is in the format of {{{...}} 
# pass a file to this script and get back a json of original data 



GLOBAL_KEY='4qmvPzFTPBLfodqLRqy8lGbNcR68Ki8V'

def hexToBytes(string):
    result = []
    for x in range(len(string)//2):
        x = x * 2
        c = string[x:x+2]
        c = int(c, 16)
        result.append(c)
    return result


def first_change_xor(byte_list):
    # Just xor everyting with byte 0x37
    result = [] # NOTE: Not sure why it should start with 0, but does the trick for now
    for x in range(0, len(byte_list)):
        byte1 = 0x37
        byte2 = byte_list[x]
        b = byte1 ^ byte2
        result.append(b)
    return result

def second_change_xor(byte_list):
    # XOR everything with prebaked key
    result = ""
    for i, x in enumerate(byte_list):
        key_index = ((i) % len(GLOBAL_KEY))
        key_value = ord(GLOBAL_KEY[key_index])

        b = x ^ key_value 

        result += chr(b)
    return result


def split_by_percent_sign(data):
    index = 0
    for i, x in enumerate(data):
        if x == 0x25:
            index = i
            break
    return index



def convert_and_print(raw):
    # Convert using a prefix key embeded as a 32 byte prefix inside the message
    global_byte_list = hexToBytes(raw)
    global_byte_list = first_change_xor(global_byte_list)

    global_result_string = second_change_xor(global_byte_list)
    global_byte_list = hexToBytes(global_result_string)

    split_index = split_by_percent_sign(global_byte_list)

    small_key = global_byte_list[:split_index]
    data = global_byte_list[split_index + 1:]

    result = ""
    for i, x in enumerate(data):
        key_index = (i % len(small_key))
        key_value = small_key[key_index]

        byte1 = x
        byte2 = key_value
        b = byte1 ^ byte2
        result += chr(b)
    return result


def remove_prefix_and_postfix(data):
    start_index = data.find("{{{")
    end_index = data.find("}}}")
    if start_index != -1:
        start_index = 3
    output = data[start_index:end_index]
    return output


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: {} [filename]'.format(sys.argv[0]))
        exit(13)

    should_remove_prefix = True
    if (len(sys.argv) == 3) and (sys.argv[2] == '-n'):
        should_remove_prefix = False

    filename = sys.argv[1]
    is_file_exists = os.path.exists(filename)
    if is_file_exists:
        raw = ''
        try: 
            with open(filename, 'r') as f:
                raw = f.read()
            if should_remove_prefix:
                raw = remove_prefix_and_postfix(raw)
            output = convert_and_print(raw)
            print(output)
        except Exception as e:
            print("Exception occured: {}", e);
    else:
        print('File "{}" does not exists'.format(sys.argv[1]))
        exit(14)




