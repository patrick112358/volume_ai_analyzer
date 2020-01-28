from enum import Enum

class ModelType(Enum):
    YOLO = 1
    YOLO_TINY = 2
    RES_NET = 3

class DetectionSpeed(Enum):
    NORMAL = "normal"
    FAST = "fast"
    FASTER = "faster"
    FLASH = "flash"

class ClassType(Enum):
    CLASS_A = "SMALL"
    CLASS_B = "CAR"
    CLASS_C = "BIGGER CAR"
    CLASS_D = "TRUCK"

class VehicleType(Enum):
    CAR = "car"
    MOTORCYCLE = "motorcycle"
    BICYCLE = "bicycle"
    BUS = "bus"
    TRUCK = "truck"

class CLASS_A_RANGE(Enum):
    FROM = "1"
    TO = "10"

class CLASS_B_RANGE(Enum):
    FROM = "11"
    TO = "25"

class CLASS_C_RANGE(Enum):
    FROM = "26"
    TO = "30"

class CLASS_D_RANGE(Enum):
    FROM = "31"
    TO = "50"