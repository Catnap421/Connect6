# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 22:03:34 2021
@author: Creation Yun
"""

from enum import IntEnum
from typing import Union


class Connect6ProtocolSettings(IntEnum):
    PROTOCOL_HEADER_SIZE = 4
    PROTOCOL_VER = 0
    MAX_NAME_LENGTH = 100
    BOARD_SIZE = 19


class ProtocolType(IntEnum):
    GAME_START = 0
    PUT = 1
    TURN = 2
    GAME_OVER = 3
    ERROR = 4
    TIMEOUT = 5
    GAME_DISCARD = 6


class ErrorType(IntEnum):
    ERROR_SERVER_INTERNAL_ERROR = 0
    ERROR_PROTOCOL_NOT_VALID = 1
    ERROR_EXCEED_COORDINATE_RANGE = 2
    ERROR_GAME_NOT_STARTED = 3
    ERROR_EXCEED_CAPACITY = 4
    ERROR_EXCEED_NAME_LENGTH = 5
    ERROR_OTHER_PLAYER_DISCONNECTED = 6
    ERROR_GAME_ALREADY_STARTED = 7
    ERROR_MISUSE_FUNCTION = 0xFF


class GameResultType(IntEnum):
    RESULT_GAME_DISCARDED = 0
    RESULT_WIN_OR_LOSE = 1
    RESULT_DRAW = 2
    RESULT_CONNECTION_ERROR = 3
    RESULT_TIMEOUT = 4


class Connect6ProtocolHdr:
    def __init__(self, version: int = Connect6ProtocolSettings.PROTOCOL_VER.value,
                 _type: int = 0, player_num: int = 0, data_length: int = 0):
        self.version = version
        self._type = _type
        self.player_num = player_num
        self.data_length = data_length


class GameStartData:
    def __init__(self, req_res_flag: int = 0, name_length: int = 0, name: str = ""):
        self.req_res_flag = req_res_flag
        self.name_length = name_length
        self.name = name


class PutTurnData:
    def __init__(self, coord_num: int = 0, xy: list = None):
        if xy is None:
            xy = []
        self.coord_num = coord_num
        self.xy = xy


class GameOverData:
    def __init__(self, result: int = 0, coord_num: int = 0, xy: list = None):
        if xy is None:
            xy = []
        self.result = result
        self.coord_num = coord_num
        self.xy = xy


def hdr_parsing(payload: Union[bytes, str, bytearray]):
    header = Connect6ProtocolHdr()

    if payload is None:
        return ErrorType.ERROR_MISUSE_FUNCTION, None

    payload_size = len(payload)

    if payload_size < Connect6ProtocolSettings.PROTOCOL_HEADER_SIZE:
        return ErrorType.ERROR_PROTOCOL_NOT_VALID, None

    if type(payload) is str:
        _payload = bytes(payload, encoding='utf-8')
    else:
        _payload = payload

    header.version = _payload[0]
    header.type = _payload[1]
    header.player_num = _payload[2]
    header.data_length = _payload[3]

    return 0, header


def game_start_data_parsing(data_payload: Union[bytes, str, bytearray]):
    data = GameStartData()

    if data_payload is None:
        return ErrorType.ERROR_MISUSE_FUNCTION, None

    data_payload_size = len(data_payload)

    if data_payload_size < 2:
        return ErrorType.ERROR_PROTOCOL_NOT_VALID, None

    if type(data_payload) is str:
        _data_payload = bytes(data_payload, encoding='utf-8')
    else:
        _data_payload = data_payload

    data.req_res_flag = _data_payload[0]
    data.name_length = _data_payload[1]

    if data_payload_size < data.name_length + 2:
        return ErrorType.ERROR_PROTOCOL_NOT_VALID, None

    if data.name_length > Connect6ProtocolSettings.MAX_NAME_LENGTH:
        return ErrorType.ERROR_EXCEED_NAME_LENGTH, None

    data.name = _data_payload[2: 2 + data.name_length].decode('utf-8')

    return 0, data


def put_turn_data_parsing(data_payload: Union[bytes, str, bytearray]):
    data = PutTurnData()

    if data_payload is None:
        return ErrorType.ERROR_MISUSE_FUNCTION, None

    data_payload_size = len(data_payload)

    if data_payload_size < 1:
        return ErrorType.ERROR_PROTOCOL_NOT_VALID, None

    if type(data_payload) is str:
        _data_payload = bytes(data_payload, encoding='utf-8')
    else:
        _data_payload = data_payload

    data.coord_num = _data_payload[0]

    if data_payload_size < data.coord_num * 2 + 1:
        return ErrorType.ERROR_PROTOCOL_NOT_VALID, None

    if data.coord_num > 2:
        return ErrorType.ERROR_PROTOCOL_NOT_VALID, None

    data.xy = [0] * (data.coord_num * 2)

    for i in range(data.coord_num):
        if _data_payload[2*i + 1] >= Connect6ProtocolSettings.BOARD_SIZE:
            return ErrorType.ERROR_EXCEED_COORDINATE_RANGE, None

        data.xy[2*i] = _data_payload[2*i + 1]

        if _data_payload[2*i + 2] >= Connect6ProtocolSettings.BOARD_SIZE:
            return ErrorType.ERROR_EXCEED_COORDINATE_RANGE, None

        data.xy[2*i + 1] = _data_payload[2*i + 2]

    return 0, data


def game_over_data_parsing(data_payload: Union[bytes, str, bytearray]):
    data = GameOverData()

    if data_payload is None:
        return ErrorType.ERROR_MISUSE_FUNCTION, None

    data_payload_size = len(data_payload)

    if data_payload_size < 2:
        return ErrorType.ERROR_PROTOCOL_NOT_VALID, None

    if type(data_payload) is str:
        _data_payload = bytes(data_payload, encoding='utf-8')
    else:
        _data_payload = data_payload

    data.coord_num = _data_payload[0]

    if data_payload_size < data.coord_num * 2 + 2:
        return ErrorType.ERROR_PROTOCOL_NOT_VALID, None

    if data.coord_num > 6:
        return ErrorType.ERROR_PROTOCOL_NOT_VALID, None

    data.xy = [0] * (data.coord_num * 2)

    for i in range(data.coord_num):
        if _data_payload[2*i + 2] >= Connect6ProtocolSettings.BOARD_SIZE:
            return ErrorType.ERROR_EXCEED_COORDINATE_RANGE, None

        data.xy[2*i] = _data_payload[2*i + 2]

        if _data_payload[2*i + 3] >= Connect6ProtocolSettings.BOARD_SIZE:
            return ErrorType.ERROR_EXCEED_COORDINATE_RANGE, None

        data.xy[2*i + 1] = _data_payload[2*i + 3]

    return 0, data


def error_data_parsing(data_payload: Union[bytes, str, bytearray]):
    if data_payload is None:
        return ErrorType.ERROR_MISUSE_FUNCTION, None

    data_payload_size = len(data_payload)

    if data_payload_size < 1:
        return ErrorType.ERROR_PROTOCOL_NOT_VALID, None

    if type(data_payload) is str:
        _data_payload = bytes(data_payload, encoding='utf-8')
    else:
        _data_payload = data_payload

    error_type = ErrorType(_data_payload[0])

    return 0, error_type


def make_game_start_payload(player_num: int, data: GameStartData):
    if data is None:
        return ErrorType.ERROR_MISUSE_FUNCTION, None

    if data.name_length > Connect6ProtocolSettings.MAX_NAME_LENGTH:
        return ErrorType.ERROR_EXCEED_NAME_LENGTH, None

    # Header field
    payload_arr = [
        Connect6ProtocolSettings.PROTOCOL_VER.value,  # Version
        ProtocolType.GAME_START.value,                # Type
        player_num,                                   # PlayerNum
        data.name_length + 2                          # DataLength
    ]

    # Data field
    payload_arr += [
        data.req_res_flag,
        data.name_length
    ]
    for i in range(data.name_length):
        payload_arr.append(ord(data.name[i]))

    payload = bytes(payload_arr)

    return 0, payload


def make_put_payload(player_num: int, data: PutTurnData):
    if data is None:
        return ErrorType.ERROR_MISUSE_FUNCTION, None

    # Header and data field
    payload_arr = [
        Connect6ProtocolSettings.PROTOCOL_VER.value,  # Version
        ProtocolType.PUT.value,                       # Type
        player_num,                                   # PlayerNum
        data.coord_num * 2 + 1,                       # DataLength
        data.coord_num                                # Data.CoordNum
    ]

    # Remained data field
    for i in range(data.coord_num):
        if data.xy[2*i] >= Connect6ProtocolSettings.BOARD_SIZE:
            return ErrorType.ERROR_EXCEED_COORDINATE_RANGE, None

        payload_arr.append(data.xy[2*i])

        if data.xy[2*i + 1] >= Connect6ProtocolSettings.BOARD_SIZE:
            return ErrorType.ERROR_EXCEED_COORDINATE_RANGE, None

        payload_arr.append(data.xy[2*i+1])

    payload = bytes(payload_arr)

    return 0, payload


def make_turn_payload(player_num: int, data: PutTurnData):
    if data is None:
        return ErrorType.ERROR_MISUSE_FUNCTION, None

    # Header and data field
    payload_arr = [
        Connect6ProtocolSettings.PROTOCOL_VER.value,  # Version
        ProtocolType.TURN.value,                      # Type
        player_num,                                   # PlayerNum
        data.coord_num * 2 + 1,                       # DataLength
        data.coord_num                                # Data.CoordNum
    ]

    # Remained data field
    for i in range(data.coord_num):
        if data.xy[2*i] >= Connect6ProtocolSettings.BOARD_SIZE:
            return ErrorType.ERROR_EXCEED_COORDINATE_RANGE, None

        payload_arr.append(data.xy[2*i])

        if data.xy[2*i + 1] >= Connect6ProtocolSettings.BOARD_SIZE:
            return ErrorType.ERROR_EXCEED_COORDINATE_RANGE, None

        payload_arr.append(data.xy[2*i+1])

    payload = bytes(payload_arr)

    return 0, payload


def make_game_over_payload(player_num: int, data: GameOverData):
    if data is None:
        return ErrorType.ERROR_MISUSE_FUNCTION, None

    # Header and data field
    payload_arr = [
        Connect6ProtocolSettings.PROTOCOL_VER.value,  # Version
        ProtocolType.GAME_OVER.value,                 # Type
        player_num,                                   # PlayerNum
        data.coord_num * 2 + 2,                       # DataLength
        data.result,                                  # Data.Result
        data.coord_num                                # Data.CoordNum
    ]

    # Remained data field
    for i in range(data.coord_num):
        if data.xy[2*i] >= Connect6ProtocolSettings.BOARD_SIZE:
            return ErrorType.ERROR_EXCEED_COORDINATE_RANGE, None

        payload_arr.append(data.xy[2*i])

        if data.xy[2*i + 1] >= Connect6ProtocolSettings.BOARD_SIZE:
            return ErrorType.ERROR_EXCEED_COORDINATE_RANGE, None

        payload_arr.append(data.xy[2*i+1])

    payload = bytes(payload_arr)

    return 0, payload


def make_error_payload(player_num: int, error_type: ErrorType):
    if error_type is None:
        return ErrorType.ERROR_MISUSE_FUNCTION, None

    # Header and data field
    payload_arr = [
        Connect6ProtocolSettings.PROTOCOL_VER.value,  # Version
        ProtocolType.ERROR.value,                     # Type
        player_num,                                   # PlayerNum
        1,                                            # DataLength
        error_type                                    # Data.ErrorType
    ]

    payload = bytes(payload_arr)

    return 0, payload


def make_timeout_payload(player_num: int):
    # Header field
    payload_arr = [
        Connect6ProtocolSettings.PROTOCOL_VER.value,  # Version
        ProtocolType.TIMEOUT.value,                   # Type
        player_num,                                   # PlayerNum
        0                                             # DataLength
    ]

    payload = bytes(payload_arr)

    return 0, payload


def make_game_discard_payload(player_num: int):
    # Header field
    payload_arr = [
        Connect6ProtocolSettings.PROTOCOL_VER.value,  # Version
        ProtocolType.GAME_DISCARD.value,              # Type
        player_num,                                   # PlayerNum
        0                                             # DataLength
    ]

    payload = bytes(payload_arr)

    return 0, payload