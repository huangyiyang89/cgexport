import struct
import os
from PIL import Image
from enum import Enum
from typing import List
from functools import lru_cache
from typing import Dict


class ActionType(Enum):
    IDLE = 0
    WALK = 1
    RUN_PREPARE = 2
    RUN = 3
    RUN_FINISH = 4
    ATTACK = 5
    SPELL = 6
    CAST = 7
    HURT = 8
    GUARD = 9
    FALL = 10
    SIT = 11
    WAVE = 12
    HAPPY = 13
    ANGRY = 14
    SAD = 15
    NOD = 16
    STONE = 17
    SCISSORS = 18
    PAPER = 19
    FISH = 20


class Graphic:

    _defalult_palette = [
        0,
        0,
        0,
        0,
        0,
        128,
        0,
        128,
        0,
        0,
        128,
        128,
        128,
        0,
        128,
        128,
        0,
        0,
        128,
        128,
        0,
        192,
        192,
        192,
        192,
        220,
        192,
        240,
        202,
        166,
        0,
        0,
        222,
        0,
        95,
        255,
        160,
        255,
        255,
        210,
        95,
        0,
        255,
        210,
        80,
        40,
        225,
        40,
        164,
        247,
        133,
        150,
        226,
        122,
        136,
        205,
        110,
        122,
        184,
        99,
        108,
        163,
        87,
        94,
        142,
        76,
        245,
        232,
        240,
        245,
        215,
        219,
        245,
        197,
        197,
        245,
        180,
        176,
        245,
        163,
        154,
        245,
        146,
        133,
        245,
        128,
        111,
        245,
        111,
        90,
        225,
        101,
        82,
        205,
        92,
        73,
        185,
        82,
        65,
        165,
        72,
        56,
        145,
        62,
        48,
        125,
        53,
        39,
        105,
        43,
        31,
        85,
        33,
        22,
        255,
        241,
        209,
        248,
        229,
        195,
        241,
        217,
        181,
        234,
        205,
        167,
        228,
        193,
        154,
        221,
        181,
        140,
        214,
        169,
        126,
        207,
        157,
        112,
        242,
        180,
        126,
        229,
        166,
        112,
        216,
        151,
        98,
        203,
        137,
        84,
        191,
        123,
        71,
        178,
        109,
        57,
        165,
        94,
        43,
        152,
        80,
        29,
        223,
        226,
        217,
        200,
        205,
        190,
        178,
        184,
        163,
        155,
        163,
        136,
        133,
        142,
        108,
        110,
        121,
        81,
        88,
        100,
        54,
        65,
        79,
        27,
        229,
        177,
        247,
        209,
        158,
        241,
        190,
        138,
        236,
        170,
        119,
        230,
        151,
        100,
        224,
        131,
        80,
        219,
        112,
        61,
        213,
        92,
        42,
        207,
        243,
        218,
        155,
        237,
        207,
        133,
        230,
        197,
        111,
        224,
        186,
        89,
        218,
        175,
        66,
        212,
        164,
        44,
        205,
        154,
        22,
        199,
        143,
        0,
        184,
        131,
        0,
        169,
        120,
        0,
        140,
        97,
        0,
        125,
        85,
        0,
        110,
        73,
        0,
        95,
        62,
        0,
        225,
        194,
        119,
        209,
        178,
        109,
        192,
        162,
        99,
        176,
        146,
        89,
        160,
        129,
        79,
        143,
        113,
        69,
        127,
        97,
        60,
        111,
        81,
        50,
        94,
        65,
        40,
        78,
        49,
        30,
        62,
        32,
        20,
        45,
        16,
        10,
        29,
        0,
        0,
        237,
        249,
        220,
        218,
        242,
        198,
        182,
        229,
        141,
        146,
        217,
        85,
        128,
        204,
        84,
        111,
        192,
        84,
        93,
        179,
        83,
        75,
        166,
        82,
        69,
        153,
        76,
        63,
        139,
        69,
        55,
        122,
        60,
        47,
        104,
        52,
        39,
        87,
        43,
        31,
        69,
        34,
        23,
        52,
        26,
        15,
        34,
        17,
        186,
        232,
        218,
        173,
        219,
        207,
        160,
        207,
        195,
        148,
        194,
        184,
        135,
        181,
        173,
        122,
        168,
        161,
        109,
        156,
        150,
        97,
        143,
        139,
        84,
        130,
        127,
        71,
        118,
        116,
        58,
        105,
        104,
        45,
        92,
        93,
        33,
        79,
        82,
        20,
        67,
        70,
        7,
        54,
        59,
        160,
        200,
        246,
        149,
        190,
        237,
        137,
        180,
        227,
        126,
        169,
        218,
        114,
        159,
        208,
        103,
        149,
        199,
        91,
        139,
        189,
        80,
        129,
        180,
        69,
        118,
        171,
        57,
        108,
        161,
        46,
        98,
        152,
        34,
        88,
        142,
        23,
        77,
        133,
        11,
        67,
        123,
        0,
        57,
        114,
        227,
        248,
        255,
        207,
        237,
        248,
        186,
        226,
        241,
        166,
        215,
        234,
        146,
        203,
        228,
        126,
        192,
        221,
        105,
        181,
        214,
        85,
        170,
        207,
        74,
        154,
        191,
        64,
        139,
        174,
        53,
        123,
        158,
        43,
        107,
        142,
        32,
        91,
        125,
        21,
        76,
        109,
        11,
        60,
        92,
        0,
        44,
        76,
        250,
        250,
        250,
        224,
        224,
        224,
        199,
        199,
        199,
        173,
        173,
        173,
        148,
        148,
        148,
        122,
        122,
        122,
        97,
        97,
        97,
        71,
        71,
        71,
        46,
        46,
        46,
        20,
        20,
        20,
        216,
        216,
        197,
        199,
        200,
        175,
        181,
        185,
        153,
        164,
        169,
        131,
        146,
        153,
        108,
        129,
        138,
        86,
        111,
        122,
        64,
        220,
        224,
        225,
        205,
        211,
        213,
        191,
        199,
        202,
        176,
        187,
        190,
        162,
        175,
        179,
        148,
        162,
        167,
        133,
        150,
        156,
        119,
        138,
        144,
        104,
        126,
        133,
        90,
        113,
        121,
        76,
        101,
        110,
        61,
        89,
        98,
        47,
        77,
        87,
        32,
        64,
        75,
        73,
        22,
        202,
        53,
        3,
        196,
        245,
        229,
        184,
        242,
        223,
        166,
        240,
        216,
        149,
        237,
        210,
        132,
        239,
        219,
        140,
        228,
        208,
        133,
        217,
        197,
        125,
        206,
        186,
        118,
        195,
        175,
        111,
        184,
        165,
        103,
        173,
        154,
        96,
        162,
        143,
        89,
        151,
        132,
        81,
        140,
        121,
        74,
        255,
        255,
        222,
        255,
        255,
        190,
        255,
        255,
        159,
        255,
        255,
        127,
        255,
        255,
        95,
        255,
        255,
        63,
        255,
        252,
        0,
        255,
        236,
        0,
        255,
        216,
        0,
        255,
        197,
        0,
        255,
        178,
        0,
        255,
        158,
        0,
        255,
        139,
        0,
        255,
        119,
        0,
        255,
        100,
        0,
        255,
        100,
        0,
        245,
        86,
        0,
        235,
        72,
        1,
        225,
        58,
        1,
        215,
        44,
        1,
        205,
        30,
        1,
        195,
        16,
        2,
        167,
        2,
        2,
        149,
        2,
        2,
        131,
        1,
        1,
        113,
        1,
        1,
        76,
        1,
        1,
        40,
        0,
        0,
        243,
        223,
        223,
        224,
        195,
        194,
        204,
        167,
        165,
        185,
        139,
        136,
        166,
        111,
        106,
        146,
        83,
        77,
        150,
        195,
        245,
        95,
        160,
        30,
        70,
        125,
        195,
        30,
        85,
        155,
        55,
        65,
        70,
        30,
        35,
        40,
        240,
        251,
        255,
        165,
        110,
        58,
        128,
        128,
        128,
        0,
        0,
        255,
        0,
        255,
        0,
        0,
        255,
        255,
        255,
        0,
        0,
        255,
        128,
        255,
        255,
        255,
        0,
        255,
        255,
        255,
    ]
    _palette_cache = {}

    @staticmethod
    def read_palette_file(path) -> list[int]:
        if path in Graphic._palette_cache:
            return Graphic._palette_cache[path]
        head = [
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x80,
            0x00,
            0x80,
            0x00,
            0x00,
            0x80,
            0x80,
            0x80,
            0x00,
            0x80,
            0x80,
            0x00,
            0x00,
            0x80,
            0x80,
            0x00,
            0xC0,
            0xC0,
            0xC0,
            0xC0,
            0xDC,
            0xC0,
            0xF0,
            0xCA,
            0xA6,
            0x00,
            0x00,
            0xDE,
            0x00,
            0x5F,
            0xFF,
            0xA0,
            0xFF,
            0xFF,
            0xD2,
            0x5F,
            0x00,
            0xFF,
            0xD2,
            0x50,
            0x28,
            0xE1,
            0x28,
        ]
        foot = [
            0x96,
            0xC3,
            0xF5,
            0x5F,
            0xA0,
            0x1E,
            0x46,
            0x7D,
            0xC3,
            0x1E,
            0x55,
            0x9B,
            0x37,
            0x41,
            0x46,
            0x1E,
            0x23,
            0x28,
            0xF0,
            0xFB,
            0xFF,
            0xA5,
            0x6E,
            0x3A,
            0x80,
            0x80,
            0x80,
            0x00,
            0x00,
            0xFF,
            0x00,
            0xFF,
            0x00,
            0x00,
            0xFF,
            0xFF,
            0xFF,
            0x00,
            0x00,
            0xFF,
            0x80,
            0xFF,
            0xFF,
            0xFF,
            0x00,
            0xFF,
            0xFF,
            0xFF,
        ]
        with open(path, "rb") as file:
            data = file.read()
        if len(data) != 708:
            raise ValueError(f"Invalid palette file, size: {len(data)}")
        middle = list(data)
        # trans to rgb
        for i in range(0, len(middle), 3):
            middle[i], middle[i + 2] = middle[i + 2], middle[i]
        palette = head + middle[:-36] + foot
        Graphic._palette_cache[path] = palette
        return palette

    def __init__(self, path: str, sequence: int):
        self.path = path
        self.dir_path = os.path.dirname(path)
        self.info_path = path.replace("Graphic", "GraphicInfo")
        self.sequence = sequence
        with open(self.info_path, "rb") as file:
            data = file.seek(self.sequence * 40, os.SEEK_SET)
            data = file.read(40)

        record = struct.unpack("<lLLllLLbbb5bL", data)
        if self.sequence != record[0]:
            raise ValueError(f"Sequence mismatch: {self.sequence} != {record[0]}")

        # sequence=record[0],
        self.address = record[1]
        block_length = record[2]
        self.offset_x = record[3]
        self.offset_y = record[4]
        self.width = record[5]
        self.height = record[6]
        # area_east=record[7],
        # area_south=record[8],
        # flag=record[9],
        # unknown=list(record[10:15]),
        # map_number=record[15]

    def __decode(self, graphic_bytes, length):
        decoded_data = []
        i_pos = 0
        while i_pos < length:
            # Extract high 4 bits of the first byte
            high_nibble = graphic_bytes[i_pos] & 0xF0

            if high_nibble == 0x00:
                # 0x0n: n consecutive characters follow
                count = graphic_bytes[i_pos] & 0x0F
                i_pos += 1
                for _ in range(count):
                    decoded_data.append(graphic_bytes[i_pos])
                    i_pos += 1

            elif high_nibble == 0x10:
                # 0x1n: n*0x100 + x consecutive characters
                count = (graphic_bytes[i_pos] & 0x0F) * 0x100 + graphic_bytes[i_pos + 1]
                i_pos += 2
                for _ in range(count):
                    decoded_data.append(graphic_bytes[i_pos])
                    i_pos += 1

            elif high_nibble == 0x20:
                # 0x2n: n*0x10000 + x*0x100 + y consecutive characters
                count = (
                    (graphic_bytes[i_pos] & 0x0F) * 0x10000
                    + graphic_bytes[i_pos + 1] * 0x100
                    + graphic_bytes[i_pos + 2]
                )
                i_pos += 3
                for _ in range(count):
                    decoded_data.append(graphic_bytes[i_pos])
                    i_pos += 1

            elif high_nibble == 0x80:
                # 0x8n: n consecutive X characters
                count = graphic_bytes[i_pos] & 0x0F
                x = graphic_bytes[i_pos + 1]
                decoded_data.extend([x] * count)
                i_pos += 2

            elif high_nibble == 0x90:
                # 0x9n: n*0x100 + m consecutive X characters
                count = (graphic_bytes[i_pos] & 0x0F) * 0x100 + graphic_bytes[i_pos + 2]
                x = graphic_bytes[i_pos + 1]
                decoded_data.extend([x] * count)
                i_pos += 3

            elif high_nibble == 0xA0:
                # 0xAn: n*0x10000 + m*0x100 + z consecutive X characters
                count = (
                    (graphic_bytes[i_pos] & 0x0F) * 0x10000
                    + graphic_bytes[i_pos + 2] * 0x100
                    + graphic_bytes[i_pos + 3]
                )
                x = graphic_bytes[i_pos + 1]
                decoded_data.extend([x] * count)
                i_pos += 4

            elif high_nibble == 0xC0:
                # 0xCn: n consecutive background color (0)
                count = graphic_bytes[i_pos] & 0x0F
                decoded_data.extend([0] * count)
                i_pos += 1

            elif high_nibble == 0xD0:
                # 0xDn: n*0x100 + m consecutive background color (0)
                count = (graphic_bytes[i_pos] & 0x0F) * 0x100 + graphic_bytes[i_pos + 1]
                decoded_data.extend([0] * count)
                i_pos += 2

            elif high_nibble == 0xE0:
                # 0xEn: n*0x10000 + x*0x100 + y consecutive background color (0)
                count = (
                    (graphic_bytes[i_pos] & 0x0F) * 0x10000
                    + graphic_bytes[i_pos + 1] * 0x100
                    + graphic_bytes[i_pos + 2]
                )
                decoded_data.extend([0] * count)
                i_pos += 3

            else:
                # Skip invalid high nibble
                i_pos += 1
        return bytes(decoded_data)

    def __to_image(self, image_bytes, palette: List[int]) -> Image.Image:
        try:
            rgba_data = bytearray(self.width * self.height * 4)
            flipped_indices = [
                (self.height - i // self.width - 1) * self.width + i % self.width
                for i in range(self.width * self.height)
            ]

            if len(image_bytes) < self.width * self.height:
                raise ValueError(
                    f"Graphic bytes length {len(image_bytes)} is less than image size {self.width * self.height}"
                )

            if len(palette) < 768:  # 256 colors * 3 channels
                raise ValueError(f"Palette length {len(palette)} is invalid")

            for i, idx in enumerate(flipped_indices):
                cIdx = image_bytes[i] * 3
                if cIdx + 2 >= len(palette):
                    raise IndexError(f"Color index {cIdx} out of palette range")

                r, g, b = palette[cIdx], palette[cIdx + 1], palette[cIdx + 2]
                pixel_pos = idx * 4
                rgba_data[pixel_pos] = r
                rgba_data[pixel_pos + 1] = g
                rgba_data[pixel_pos + 2] = b
                rgba_data[pixel_pos + 3] = 255 if (r != 0 or g != 0 or b != 0) else 0

            return Image.frombytes("RGBA", (self.width, self.height), bytes(rgba_data))

        except (ValueError, IndexError) as e:
            print(f"Error converting image: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return None

    def read(self, palette: List[int] = None) -> Image.Image:
        data = self.__read_bytes()
        if palette is None:
            palette = self._defalult_palette
        image = self.__to_image(data, palette)
        return image

    def __read_bytes(self):
        with open(self.path, "rb") as file:
            data = file.seek(self.address, os.SEEK_SET)
            data = file.read(16)
            # magicNumber=record[0],
            # version=record[1]
            # unknown=record[2],
            # width=record[3],
            # height=record[4],
            # blocklength=record[5],
            # data=data,
            record = struct.unpack("<2sbblll", data)
            bytes_length = record[5] - 16
            data = file.read(bytes_length)
            version = record[1]
            if version:
                data = self.__decode(data, len(data))
            return data


class Action:
    def __init__(
        self, direction, action_type: ActionType, duration, graphics: list[Graphic]
    ):
        self.direction = direction
        self.type = action_type
        self.duration = duration
        self.graphics = graphics


class Anime:

    def __init__(self, file_path: str, graphic_file_path: str, sequence: int):
        if not os.path.exists(file_path):
            raise ValueError(f"Invalid path: {file_path}")
        if sequence < 0:
            raise ValueError("Sequence must be non-negative")

        self._path = file_path
        self._dir_path = os.path.dirname(file_path)
        self._info_path = file_path.replace("Anime", "AnimeInfo")
        self._graphic_file_path = graphic_file_path
        self._sequence = sequence
        self._id: int = None
        self._address: int = None
        self._actions: List[Action] = []

        self.__load_info()
        self.__load_actions()

    @staticmethod
    def find_by_id(
        file_path: str, graphic_file_path: str, id: int
    ) -> "Anime":
        info_path = file_path.replace("Anime", "AnimeInfo")
        if not os.path.exists(info_path):
            raise ValueError(f"Invalid path: {info_path}")
        if id < 0:
            raise ValueError("Anime ID must be non-negative")
        sequence = 0
        with open(info_path, "rb") as file:
            while True:
                data = file.read(12)
                if len(data) < 12:
                    break
                record = struct.unpack("<IIHH", data)
                if record[0] == id:
                    return Anime(file_path, graphic_file_path, sequence)
                sequence += 1
            
            

    @property
    def id(self) -> int:
        return self._id

    @property
    def actions(self) -> List[Action]:
        return self._actions

    def __load_info(self) -> int:
        try:
            with open(self._info_path, "rb") as file:
                file.seek(self._sequence * 12, os.SEEK_SET)
                data = file.read(12)
                if len(data) < 12:
                    raise ValueError(f"Invalid data size in {self._info_path}")
                record = struct.unpack("<IIHH", data)
                self._id = record[0]
                self._address = record[1]
                return record[2]
        except FileNotFoundError:
            raise FileNotFoundError(f"AnimeInfo file not found: {self._info_path}")
        except struct.error as e:
            raise ValueError(f"Failed to unpack info data: {e}")

    def __load_actions(self) -> None:
        try:
            actions_count = self.__load_info()
            with open(self._path, "rb") as file:
                file.seek(self._address, os.SEEK_SET)
                for _ in range(actions_count):
                    data = file.read(12)
                    if len(data) < 12:
                        raise ValueError(f"Invalid action data size in {self._path}")
                    record = struct.unpack("<HHII", data)
                    graphic_count = record[3]
                    graphics = []
                    for _ in range(graphic_count):
                        frame_data = file.read(10)
                        if len(frame_data) < 10:
                            raise ValueError(f"Invalid frame data size in {self._path}")
                        frame_record = struct.unpack("<I6s", frame_data)
                        graphic_sequence = frame_record[0]
                        graphic = self.__create_graphic(
                            self._graphic_file_path, graphic_sequence
                        )
                        graphics.append(graphic)
                    action = Action(
                        direction=record[0],
                        action_type=ActionType(record[1]),
                        duration=record[2],
                        graphics=graphics,
                    )
                    self._actions.append(action)
        except FileNotFoundError:
            raise FileNotFoundError(f"Anime file not found: {self._path}")
        except struct.error as e:
            raise ValueError(f"Failed to unpack action data: {e}")

    @staticmethod
    @lru_cache(maxsize=100)
    def __create_graphic(file_path: str, sequence: int) -> Graphic:
        return Graphic(file_path, sequence)

    def create_spritesheet(self, output_dir: str = "output") -> None:
        """为每种actiontype创建一张大图，包含8行（按direction排列），每种actiontype单独计算最大帧数"""

        output_dir += f"/{self.id}/"
        os.makedirs(output_dir, exist_ok=True)

        # 第一步：计算所有图像的边界框，确定统一帧画布大小
        min_x = 0
        min_y = 0
        max_x = 0
        max_y = 0

        # 同时记录每种actiontype的帧数
        actiontype_frames: Dict[Enum, int] = {}
        # 记录每种actiontype的动画时间
        actiontype_durations: Dict[Enum, int] = {}

        for action in self.actions:
            actiontype = action.type
            if actiontype not in actiontype_frames:
                actiontype_frames[actiontype] = len(action.graphics)
            
            if actiontype not in actiontype_durations:
                actiontype_durations[actiontype] = action.duration

            for graphic in action.graphics:
                try:
                    # 计算图像的实际边界（考虑偏移）
                    left = graphic.offset_x
                    right = graphic.offset_x + graphic.width
                    top = graphic.offset_y
                    bottom = graphic.offset_y + graphic.height

                    # 更新最小和最大坐标
                    min_x = min(min_x, left)
                    min_y = min(min_y, top)
                    max_x = max(max_x, right)
                    max_y = max(max_y, bottom)
                except Exception as e:
                    print(
                        f"计算边界框失败（动作：{action.type.name}, 方向：{action.direction}）：{e}"
                    )
                    continue

        # 计算每个帧的画布大小（全局统一）
        frame_width = max_x - min_x
        frame_height = max_y - min_y

        # 第二步：按actiontype分组action
        actiontype_groups: Dict[Enum, Dict[int, List[Graphic]]] = {}
        for action in self.actions:
            actiontype = action.type
            direction = action.direction
            if actiontype not in actiontype_groups:
                actiontype_groups[actiontype] = {
                    i: [] for i in range(8)
                }  # 初始化8个方向
            actiontype_groups[actiontype][direction] = action.graphics

        # 第三步：为每种actiontype生成大图
        for actiontype, directions in actiontype_groups.items():
            # 获取该actiontype的最大帧数
            frames_count = actiontype_frames.get(actiontype, 0)
            duration = actiontype_durations.get(actiontype, 0)
            fps = int(1000 * frames_count / duration) if duration > 0 else 0
            if frames_count == 0:
                print(f"动作类型 {actiontype.name} 无有效帧，跳过")
                continue

            # 计算大图尺寸：8行，每行高度为frame_height，宽度为frame_width * max_frames
            sprite_width = frame_width * frames_count
            sprite_height = frame_height * 8

            # 创建大图（透明背景）
            sprite_sheet = Image.new(
                "RGBA", (sprite_width, sprite_height), (0, 0, 0, 0)
            )

            # 遍历每个方向（0到7）
            for direction in range(8):
                graphics = directions.get(direction, [])
                if not graphics:
                    print(f"动作类型 {actiontype.name} 方向 {direction} 无图像，跳过")
                    continue

                # 遍历该方向的每个graphic（帧）
                for frame_idx, graphic in enumerate(graphics):
                    try:
                        # 读取图像
                        image = graphic.read()

                        # 计算帧在 sprite sheet 上的位置
                        # 行：direction * frame_height
                        # 列：frame_idx * frame_width
                        paste_x = frame_idx * frame_width + (graphic.offset_x - min_x)
                        paste_y = direction * frame_height + (graphic.offset_y - min_y)

                        # 粘贴图像
                        sprite_sheet.paste(image, (paste_x, paste_y))
                    except Exception as e:
                        print(
                            f"粘贴图像失败（动作类型：{actiontype.name}, 方向：{direction}, 帧：{frame_idx}）：{e}"
                        )
                        continue

            # 保存 sprite sheet
            filename = (
                f"{str(self.id)}_{actiontype.name}_{frame_width}_{frame_height}_{frames_count}_{fps}.png"
            )
            output_path = os.path.join(output_dir, filename)
            try:
                sprite_sheet.save(output_path, format="PNG")
                print(f"保存 sprite sheet：{output_path}")
            except Exception as e:
                print(f"保存 sprite sheet 失败（动作类型：{actiontype.name}）：{e}")


if __name__ == "__main__":
    #example usage
    game_bin_path = "C:/BlueCrossgate/bin/"
    anime = Anime("C:/BlueCrossgate/bin/AnimeEX_1.Bin", "C:/BlueCrossgate/bin/GraphicEX_5.bin", 0)
    anime2 = Anime.find_by_id("C:/BlueCrossgate/bin/AnimeEX_1.Bin", "C:/BlueCrossgate/bin/GraphicEX_5.bin", 107101)
    if anime2:
        anime2.create_spritesheet()
