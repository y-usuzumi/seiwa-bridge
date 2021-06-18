def layer_two_char(name):
    if name == b'Idle':
        return b'Id'
    if name == b'Qwerty':
        return b'Qt'
    if name == b'Dvorak':
        return b'Dv'
    if name == b'Dvorak Modified':
        return b'Dm'
    if name == b'Seiwa Duo':
        return b'S2'
    else:
        return b'--'


def layer_short_name(name):
    if name == b'Idle':
        return b'Idle'
    if name == b'Qwerty':
        return b'Qwerty'
    if name == b'Dvorak':
        return b'Dvorak'
    if name == b'Dvorak Modified':
        return b'DvrkMod'
    if name == b'Seiwa Duo':
        return b'Duo'
    else:
        return b'Unknown'
