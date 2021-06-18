class Env:
    __slots__ = [
        'emacs',
        'default_layer',
        'last_default_layer',
        'caps_lock',
        'num_lock',
        'ctl1',
        'ctl2',
        'zz',
        'nump',
        'ready'
    ]

    def __init__(self):
        self.emacs = False
        self.default_layer = b''
        self.last_default_layer = b''
        self.caps_lock = False
        self.num_lock = False
        self.ctl1 = False
        self.ctl2 = False
        self.zz = False
        self.nump = 0
        self.ready = False

    def __str__(self):
        return "Env(emacs=%s, default layer=%s, last default layer=%s, capslock=%s, numlock=%s, ctl1=%s, ctl2=%s, zz=%s, nump=%s)" % (
            self.emacs, self.default_layer.decode('utf-8'), self.last_default_layer.decode('utf-8'), self.caps_lock, self.num_lock,
            self.ctl1, self.ctl2, self.zz, self.nump
        )

_env = Env()

def get_env():
    return _env
