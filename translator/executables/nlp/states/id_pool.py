__author__ = 'NBUCHINA'

counter = 0
modifier = 10
base_id = 1000


def get_float_id(base_id):
    global counter
    global modifier

    ret = base_id + counter
    counter += modifier

    return ret

def reset():
    global counter
    counter=0