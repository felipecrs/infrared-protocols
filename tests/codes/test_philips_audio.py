"""Tests for the Philips audio command codes."""

import pytest

from infrared_protocols.codes.philips.audio import (
    PHILIPS_AUDIO_ADDRESS,
    PHILIPS_CD_ADDRESS,
    PHILIPS_TUNER_ADDRESS,
    PhilipsAudioCode,
)
from infrared_protocols.commands.rc5 import RC5Command


def test_philips_audio_codes_are_unique() -> None:
    """Every code must be distinct, since duplicates become silent aliases."""
    members = PhilipsAudioCode.__members__
    assert len(members) == len(set(members.values()))


@pytest.mark.parametrize(
    ("code", "address", "command"),
    [
        pytest.param(PhilipsAudioCode.MUTE, PHILIPS_AUDIO_ADDRESS, 0x0D, id="mute"),
        pytest.param(
            PhilipsAudioCode.VOLUME_UP, PHILIPS_AUDIO_ADDRESS, 0x10, id="volume_up"
        ),
        pytest.param(PhilipsAudioCode.UP, PHILIPS_AUDIO_ADDRESS, 0x50, id="up"),
        pytest.param(PhilipsAudioCode.NUM_0, PHILIPS_TUNER_ADDRESS, 0x00, id="num_0"),
        pytest.param(
            PhilipsAudioCode.STANDBY, PHILIPS_TUNER_ADDRESS, 0x0C, id="standby"
        ),
        pytest.param(PhilipsAudioCode.TUNER, PHILIPS_TUNER_ADDRESS, 0x3F, id="tuner"),
        pytest.param(PhilipsAudioCode.CD, PHILIPS_CD_ADDRESS, 0x3F, id="cd"),
    ],
)
def test_philips_audio_code_to_command(
    code: PhilipsAudioCode, address: int, command: int
) -> None:
    """Each code builds an RC-5 command with its address and function."""
    built = code.to_command(repeat_count=1, toggle=1)
    assert isinstance(built, RC5Command)
    assert built.address == address
    assert built.command == command
    assert built.toggle == 1
    assert built.repeat_count == 1


def test_philips_audio_code_to_command_defaults() -> None:
    """A code with no arguments must build a single unrepeated RC-5 frame."""
    command = PhilipsAudioCode.MUTE.to_command()
    assert isinstance(command, RC5Command)
    assert command.address == PHILIPS_AUDIO_ADDRESS
    assert command.command == 0x0D
    assert command.toggle == 0
    assert command.repeat_count == 0
    assert command.modulation == 36000


def test_philips_audio_code_passes_through_toggle_and_repeats() -> None:
    """Toggle and repeat count must reach the encoded frame."""
    command = PhilipsAudioCode.VOLUME_UP.to_command(2, toggle=1)
    assert isinstance(command, RC5Command)
    assert command.toggle == 1
    assert command.repeat_count == 2


def test_philips_audio_code_matches_raw_timings() -> None:
    """The built command produces expected RC-5 timings."""
    built = PhilipsAudioCode.VOLUME_UP.to_command()
    expected = RC5Command(address=PHILIPS_AUDIO_ADDRESS, command=0x10).get_raw_timings()
    assert built.get_raw_timings() == expected


def test_philips_audio_tuner_digits_are_contiguous() -> None:
    """Digits 0 through 9 on the tuner address occupy consecutive codes."""
    digits = [
        PhilipsAudioCode.NUM_0,
        PhilipsAudioCode.NUM_1,
        PhilipsAudioCode.NUM_2,
        PhilipsAudioCode.NUM_3,
        PhilipsAudioCode.NUM_4,
        PhilipsAudioCode.NUM_5,
        PhilipsAudioCode.NUM_6,
        PhilipsAudioCode.NUM_7,
        PhilipsAudioCode.NUM_8,
        PhilipsAudioCode.NUM_9,
    ]
    assert [code.value for code in digits] == [
        (PHILIPS_TUNER_ADDRESS, i) for i in range(10)
    ]
