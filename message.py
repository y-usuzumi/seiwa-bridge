import os
import subprocess
import pyautogui
import utils
from layer_display import layer_short_name


# K: After HID initialization, send `K:SYN` to the keyboard for status synching.
# S: (Serial) For Python -> Python messaging, e.g. when probing for devices
# I: Keyboard -> Python messages
# A: Arduino -> Python messages

class MessageHandler:
    def __init__(self, env, ui):
        self._env = env
        self._ui = ui

    def handle_msg(self, msg):
        if not msg:
            return
        slices = msg.split(b':')
        if slices[0] == b'S':
            # Internal message
            if slices[1] == b'DEVICE':
                self._handle_device(slices[2:])
        elif slices[0] == b'I':
            if slices[1] == b'SYN':
                # Sync status
                self._handle_syn(slices[2:])
            elif slices[1] == b'EE':
                # EEPROM
                self._handle_ee(slices[2:])
            elif slices[1] == b'ENV':
                # User config
                self._handle_env(slices[2:])
            elif slices[1] == b'LAYER':
                # Layer
                self._handle_layer(slices[2:])
            elif slices[1] == b'CONF':
                # User config save/load
                self._handle_conf(slices[2:])
            elif slices[1] == b'CMD':
                # Arbitrary utils
                self._handle_cmd(slices[2:])
        elif slices[0] == b'A':
            if slices[1] == b'GS':
                # Global switch
                self._handle_global_switch(slices[2:])
            elif slices[1] == b'J':
                # Joystick
                self._handle_joystick(slices[2:])

    def _handle_device(self, slices):
        if not slices:
            return

        if slices[0] == b'PROBE':
            self._ui.notify(b"Probing...", clear=True)
        elif slices[0] == b'OK':
            self._ui.notify(b"Connected", clear=True)

    def _handle_syn(self, slices):
        if not slices:
            return

        if slices[0] == b'EMACS':
            self._env.emacs = slices[1] == b'1'
        elif slices[0] == b'DL':
            self._env.default_layer = slices[1]
        elif slices[0] == b'LL':
            self._env.last_default_layer = slices[1]
        elif slices[0] == b'CAPSLOCK':
            self._env.caps_lock = slices[1] == b'1'
        elif slices[0] == b'NUMLOCK':
            self._env.num_lock = slices[1] == b'1'
        elif slices[0] == b'END':
            self._env.ready = True
            self._ui.notify(b"Keyboard ready")

        print(self._env)

    def _handle_ee(self, slices):
        if not slices:
            return

    def _handle_env(self, slices):
        if not slices:
            return

        if slices[0] == b'CAPSLOCK':
            self._env.caps_lock = slices[1] == b'1'
            self._ui.notify(b"Caps Lock %s" % (b"on" if self._env.caps_lock else b"off"))
        elif slices[0] == b'NUMLOCK':
            self._env.num_lock = slices[1] == b'1'
            self._ui.notify(b"Num Lock %s" % (b"on" if self._env.num_lock else b"off"))
        elif slices[0] == b'EMACS':
            self._env.emacs = slices[1] == b'1'
            if self._env.emacs:
                self._ui.notify(b"Emacs mode")
            else:
                self._ui.notify(b"Vim mode")

    def _handle_layer(self, slices):
        if not slices:
            return

        if slices[0] == b'CTL1':
            self._env.ctl1 = slices[1] == b'1'
            self._ui.refresh_status()
        elif slices[0] == b'CTL2':
            self._env.ctl2 = slices[1] == b'1'
            self._ui.refresh_status()
        elif slices[0] == b'NUMP':
            self._env.nump = int(slices[1])
            self._ui.refresh_status()
        elif slices[0] == b'ZZ':
            self._env.zz = slices[1] == b'1'
            self._ui.refresh_status()
        elif slices[0] == b'PUSH':
            self._env.default_layer = slices[1]
            self._env.last_default_layer = slices[2]
            self._ui.notify(b"Now on %s" % layer_short_name(self._env.default_layer))
        elif slices[0] == b'FLIP':
            self._env.default_layer = slices[1]
            self._env.last_default_layer = slices[2]
            self._ui.notify(b"%s<->%s" % (
                layer_short_name(self._env.last_default_layer),
                layer_short_name(self._env.default_layer)
            ))

    def _handle_conf(self, slices):
        if not slices:
            return

        if slices[0] == b'LOAD':
            self._ui.notify(b"Conf loaded")
        elif slices[0] == b'SAVE':
            self._ui.notify(b"Conf saved")

    def _handle_cmd(self, slices):
        if not slices:
            return

        cmd_num = slices[0]

        if cmd_num == b'1':
            cpu_usage = utils.get_cpu_usage()
            self._ui.notify(b"CPU: %s" % cpu_usage)
        elif cmd_num == b'2':
            mem_usage = utils.get_mem_usage()
            self._ui.notify(b"MEM: %s" % mem_usage)
        elif cmd_num == b'3':
            self._ui.notify(b"Opening Spotify")
            subprocess.Popen("spotify --force-device-scale-factor=2", shell=True, start_new_session=True)
            # subprocess.Popen("sudo -u kj kate", shell=True, start_new_session=True)
        elif cmd_num == b'4':
            pass
        elif cmd_num == b'5':
            pass
        elif cmd_num == b'6':
            pass
        elif cmd_num == b'7':
            pass
        elif cmd_num == b'8':
            pass
        elif cmd_num == b'9':
            pass
        elif cmd_num == b'0':
            pass

    def _handle_global_switch(self, slices):
        if not slices:
            return

    def _handle_joystick(self, slices):
        if not slices:
            return

        if slices[0] == b'XY':
            # Update coordinates
            x = int(slices[1])
            y = int(slices[2])
            move_x = 0 if abs(x) < 20 else (x-20) / 10
            move_y = 0 if abs(y) < 20 else (-y+20) / 10
            pyautogui.move(move_x, move_y, _pause=False)
        elif slices[0] == b'SW':
            # Button press
            sw = slices[1]
            if sw == b'1':
                pyautogui.mouseDown()
            else:
                pyautogui.mouseUp()


