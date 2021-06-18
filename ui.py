import threading
import display
from layer_display import layer_two_char

_DELAY = 1.5

class UI:
    def __init__(self, ser, env):
        self._ser = ser
        self._env = env
        self._timer = None

    def refresh(self):
        if self._timer is not None:
            return
        self._main_screen()

    def refresh_status(self):
        self._display_status()

    def notify(self, header, content=None, clear=False, refresh_status=True):
        if refresh_status:
            self._display_status()
        self._run_overlay(lambda: self._notify(header, content, clear=clear))

    def _notify(self, header, content=None, clear=False):
        display.send_header(self._ser, header, clear=clear)
        if content:
            display.send_content(self._ser, content, clear=clear)

    def _main_screen(self):
        if not self._env.ready:
            return
        if self._timer is not None:
            self._timer.cancel()
            self._timer = None
        self._display_env()

    def _display_env(self):
        display.send_header(self._ser, b"SeiwaX 6.5 Due")
        self._display_status()

    def _display_status(self):
        layer_display = b"%s/%s" % (layer_two_char(self._env.default_layer), layer_two_char(self._env.last_default_layer))
        capslock_display = b"C" if self._env.caps_lock else b"_"
        numlock_display = b"N" if self._env.num_lock else b"_"
        mode = b"E" if self._env.emacs else b"V"
        ctl_layer_display = self._get_ctl_layer_display()
        display.send_content(self._ser, b"%s  %s%s  %s  %s" % (layer_display, capslock_display, numlock_display, mode, ctl_layer_display))

    def _get_ctl_layer_display(self):
        if self._env.zz:
            return b"Z"
        if self._env.nump == 2:
            return b"N"
        if self._env.nump == 1:
            return b"n"
        if self._env.ctl2:
            return b"2"
        elif self._env.ctl1:
            return b"1"
        return b"_"


    def _run_overlay(self, f):
        if self._timer is not None:
            self._timer.cancel()
        self._timer = threading.Timer(_DELAY, self._main_screen)
        self._timer.start()
        f()
