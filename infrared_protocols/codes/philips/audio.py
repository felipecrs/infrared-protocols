"""Command codes for Philips audio devices (receivers, tuners, and CD players).

Codes are taken from Philips receiver, tuner, and CD player entries in the IRDB.
"""

from enum import Enum

from ...commands import Command
from ...commands.rc5 import RC5Command

PHILIPS_AUDIO_ADDRESS = 0x10
PHILIPS_TUNER_ADDRESS = 0x11
PHILIPS_CD_ADDRESS = 0x14


class PhilipsAudioCode(Enum):
    """Philips audio IR command codes for receivers, tuners, and CD players.

    Code values are ``(address, command)`` pairs. Address 0x10 entries are
    receiver controls, address 0x11 entries are tuner controls, and address 0x14
    entries are CD controls.
    """

    MUTE = (PHILIPS_AUDIO_ADDRESS, 0x0D)
    DISPLAY = (PHILIPS_AUDIO_ADDRESS, 0x0F)
    VOLUME_UP = (PHILIPS_AUDIO_ADDRESS, 0x10)
    VOLUME_DOWN = (PHILIPS_AUDIO_ADDRESS, 0x11)
    SPEAKERS = (PHILIPS_AUDIO_ADDRESS, 0x1D)
    UP = (PHILIPS_AUDIO_ADDRESS, 0x50)
    DOWN = (PHILIPS_AUDIO_ADDRESS, 0x51)
    OK = (PHILIPS_AUDIO_ADDRESS, 0x52)
    LEFT = (PHILIPS_AUDIO_ADDRESS, 0x55)
    RIGHT = (PHILIPS_AUDIO_ADDRESS, 0x56)

    NUM_0 = (PHILIPS_TUNER_ADDRESS, 0x00)
    NUM_1 = (PHILIPS_TUNER_ADDRESS, 0x01)
    NUM_2 = (PHILIPS_TUNER_ADDRESS, 0x02)
    NUM_3 = (PHILIPS_TUNER_ADDRESS, 0x03)
    NUM_4 = (PHILIPS_TUNER_ADDRESS, 0x04)
    NUM_5 = (PHILIPS_TUNER_ADDRESS, 0x05)
    NUM_6 = (PHILIPS_TUNER_ADDRESS, 0x06)
    NUM_7 = (PHILIPS_TUNER_ADDRESS, 0x07)
    NUM_8 = (PHILIPS_TUNER_ADDRESS, 0x08)
    NUM_9 = (PHILIPS_TUNER_ADDRESS, 0x09)
    MINUS = (PHILIPS_TUNER_ADDRESS, 0x0A)
    STANDBY = (PHILIPS_TUNER_ADDRESS, 0x0C)
    TUNER_DISPLAY = (PHILIPS_TUNER_ADDRESS, 0x0F)
    FAST_FORWARD = (PHILIPS_TUNER_ADDRESS, 0x1E)
    REWIND = (PHILIPS_TUNER_ADDRESS, 0x1F)
    PRESET_TRACK_UP = (PHILIPS_TUNER_ADDRESS, 0x20)
    PRESET_TRACK_DOWN = (PHILIPS_TUNER_ADDRESS, 0x21)
    I_II = (PHILIPS_TUNER_ADDRESS, 0x25)
    SCAN = (PHILIPS_TUNER_ADDRESS, 0x2B)
    TUNER = (PHILIPS_TUNER_ADDRESS, 0x3F)

    CD = (PHILIPS_CD_ADDRESS, 0x3F)

    def to_command(self, repeat_count: int = 0, *, toggle: int = 0) -> Command:
        """Build an RC-5 command for this Philips audio code.

        Flip ``toggle`` between successive presses of the same key, otherwise
        the receiver reads the second press as a repeat of the first and
        ignores it.
        """
        address, command = self.value
        return RC5Command(
            address=address,
            command=command,
            toggle=toggle,
            repeat_count=repeat_count,
        )
