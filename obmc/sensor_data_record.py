# -*- coding: utf-8 -*-

# pylint: disable=attribute-defined-outside-init
# pylint: disable=missing-docstring

# pylint: disable=too-many-instance-attributes
class SensorDataRecord(object):
    EVENT_MASK_BIT_0 = 0b000000000000001
    EVENT_MASK_BIT_1 = 0b000000000000010
    EVENT_MASK_BIT_2 = 0b000000000000100
    EVENT_MASK_BIT_3 = 0b000000000001000
    EVENT_MASK_BIT_4 = 0b000000000010000
    EVENT_MASK_BIT_5 = 0b000000000100000
    EVENT_MASK_BIT_6 = 0b000000001000000
    EVENT_MASK_BIT_7 = 0b000000010000000
    EVENT_MASK_BIT_8 = 0b000000100000000
    EVENT_MASK_BIT_9 = 0b000001000000000
    EVENT_MASK_BIT_10 = 0b000010000000000
    EVENT_MASK_BIT_11 = 0b000100000000000
    EVENT_MASK_BIT_12 = 0b001000000000000
    EVENT_MASK_BIT_13 = 0b010000000000000
    EVENT_MASK_BIT_14 = 0b100000000000000

    SUPPORT_LNC_GOING_LOW = 0b000000000000001
    SUPPORT_LNC_GOING_HIGH = 0b000000000000010
    SUPPORT_LC_GOING_LOW = 0b000000000000100
    SUPPORT_LC_GOING_HIGH = 0b000000000001000
    SUPPORT_LNR_GOING_LOW = 0b000000000010000
    SUPPORT_LNR_GOING_HIGH = 0b000000000100000
    SUPPORT_UNC_GOING_LOW = 0b000000001000000
    SUPPORT_UNC_GOING_HIGH = 0b000000010000000
    SUPPORT_UC_GOING_LOW = 0b000000100000000
    SUPPORT_UC_GOING_HIGH = 0b000001000000000
    SUPPORT_UNR_GOING_LOW = 0b000010000000000
    SUPPORT_UNR_GOING_HIGH = 0b000100000000000

    RETURN_LNC = 0b001000000000000
    RETURN_LC = 0b010000000000000
    RETURN_LNR = 0b100000000000000
    RETURN_UNC = 0b001000000000000
    RETURN_UC = 0b010000000000000
    RETURN_UNR = 0b100000000000000

    UNIT_1_PERCENTAGE = 0b00000001
    UNIT_1_MODIFIER_USAGE_DIVIDE = 0b00000010
    UNIT_1_MODIFIER_USAGE_MULTIPLY = 0b00000100
    UNIT_1_PER_MICROSECOND = 0b00001000
    UNIT_1_PER_MILLISECOND = 0b00010000
    UNIT_1_PER_SECOND = 0b00011000
    UNIT_1_PER_MINUTE = 0b00100000
    UNIT_1_PER_HOUR = 0b00101000
    UNIT_1_PER_DAY = 0b00110000
    UNIT_1_UNSIGNED = 0b00000000
    UNIT_1_SIGNED_1_COMPLEMENT = 0b01000000
    UNIT_1_SIGNED_2_COMPLEMENT = 0b10000000
    UNIT_1_NOT_ANALOG = 0b11000000

    RATE_NAMES = (
        None,
        'per microsecond',
        'per millisecond',
        'per second',
        'per minute',
        'per hour',
        'per day',
    )

    UNIT_UNSPECIFIED = 0
    UNIT_DEGREE_C = 1
    UNIT_DEGREE_F = 2
    UNIT_DEGREE_K = 3
    UNIT_VOLTS = 4
    UNIT_AMPS = 5
    UNIT_WATTS = 6
    UNIT_JOULES = 7
    UNIT_COULOMBS = 8
    UNIT_VA = 9
    UNIT_NITS = 10
    UNIT_LUMEN = 11
    UNIT_LUX = 12
    UNIT_CANDELA = 13
    UNIT_KPA = 14
    UNIT_PSI = 15
    UNIT_NEWTON = 16
    UNIT_CFM = 17
    UNIT_RPM = 18
    UNIT_HZ = 19
    UNIT_MICROSECOND = 21
    UNIT_MILLISECOND = 22
    UNIT_SECOND = 23
    UNIT_HOUR = 24
    UNIT_DAY = 25
    UNIT_WEEK = 26
    UNIT_MIL = 27
    UNIT_INCHES = 28
    UNIT_FEET = 29
    UNIT_CU_IN = 30
    UNIT_CU_FEET = 31
    UNIT_MM = 32
    UNIT_CM = 33
    UNIT_M = 34
    UNIT_CU_CM = 35
    UNIT_CU_M = 36
    UNIT_LITERS = 37
    UNIT_FLUID_OUNCE = 38
    UNIT_RADIANS = 39
    UNIT_STERADIANS = 40
    UNIT_REVOLUTIONS = 41
    UNIT_CYCLES = 42
    UNIT_GRAVITIES = 43
    UNIT_OUNCE = 44
    UNIT_POUND = 45
    UNIT_FT_LB = 46
    UNIT_OZ_IN = 47
    UNIT_GAUSS = 48
    UNIT_GILBERTS = 49
    UNIT_HENRY = 50
    UNIT_MILLIHENRY = 51
    UNIT_FARAD = 52
    UNIT_MICROFARAD = 53
    UNIT_OHMS = 54
    UNIT_SIEMENS = 55
    UNIT_MOLE = 56
    UNIT_BECQUEREL = 57
    UNIT_PPM = 58
    UNIT_DECIBELS = 60
    UNIT_DBA = 61
    UNIT_DBC = 62
    UNIT_GRAY = 63
    UNIT_SIEVERT = 64
    UNIT_COLOR_TEMP_DEG_K = 65
    UNIT_BIT = 66
    UNIT_KILOBIT = 67
    UNIT_MEGABIT = 68
    UNIT_GIGABIT = 69
    UNIT_BYTE = 70
    UNIT_KILOBYTE = 71
    UNIT_MEGABYTE = 72
    UNIT_GIGABYTE = 73
    UNIT_WORD = 74
    UNIT_DWORD = 75
    UNIT_QWORD = 76
    UNIT_LINE = 77
    UNIT_HIT = 78
    UNIT_MISS = 79
    UNIT_RETRY = 80
    UNIT_RESET = 81
    UNIT_OVERRUN_OVERFLOW = 82
    UNIT_UNDERRUN = 83
    UNIT_COLLISIONS = 84
    UNIT_PACKETS = 85
    UNIT_MESSAGES = 86
    UNIT_CHARACTERS = 87
    UNIT_ERROR = 88
    UNIT_CORRECTABLE_ERROR = 89
    UNIT_UNCORRECTABLE_ERROR = 90
    UNIT_FATAL_ERROR = 91
    UNIT_GRAMS = 92

    UNIT_NAMES = (
        '',
        'degrees C',
        'degrees F',
        'degrees K',
        'Volts',
        'Amps',
        'Watts',
        'Joules',
        'Coulombs',
        'VA',
        'Nits',
        'lumen',
        'lux',
        'Candela',
        'kPa',
        'PSI',
        'Newton',
        'CFM',
        'RPM',
        'Hz',
        'microsecond',
        'millisecond',
        'second',
        'minute',
        'hour',
        'day',
        'week',
        'mil',
        'inches',
        'feet',
        'cu in',
        'cu feet',
        'mm',
        'cm',
        'm',
        'cu cm',
        'cu m',
        'liters',
        'fluid ounce',
        'radians',
        'steradians',
        'revolutions',
        'cycles',
        'gravities',
        'ounce',
        'pound',
        'ft-lb',
        'oz-in',
        'gauss',
        'gliberts',
        'henry',
        'millihenry',
        'farad',
        'microfarad',
        'ohms',
        'siemens',
        'mole',
        'becquerel',
        'PPM',
        None,
        'Decibels',
        'DbA',
        'DbC',
        'gray',
        'sievert',
        'color temp deg K',
        'bit',
        'kilobit',
        'megabit',
        'gigabit',
        'byte',
        'kilobyte',
        'megabyte',
        'gigabyte',
        'word',
        'dword',
        'qword',
        'line',
        'hit',
        'miss',
        'retry',
        'reset',
        'overrun / overflow',
        'underrun',
        'collision',
        'packets',
        'messages',
        'characters',
        'error',
        'correctable error',
        'uncorrectable error',
        'fatal error',
        'grams',
    )

    def __init__(self):
        self.sensor_number = None
        self.sensor_type = None
        self.event_type = None
        self.assertion_event_mask = None
        self.deassertion_event_mask = None
        self.sensor_unit_1 = None
        self.sensor_unit_2 = None
        self.sensor_unit_3 = None
        self.m_factor = None
        self.b_factor = None
        self.b_exp = None
        self.r_exp = None
        self.sensor_maximum_reading = None
        self.sensor_minimum_reading = None
        self.unr_threshold = None
        self.uc_threshold = None
        self.unc_threshold = None
        self.lnr_threshold = None
        self.lc_threshold = None
        self.lnc_threshold = None
        self.sensor_name = None
        self.unit_unr = None
        self.unit_uc = None
        self.unit_unc = None
        self.unit_lnr = None
        self.unit_lc = None
        self.unit_lnc = None
        self.unit_name = None

    def _autofill_unit_name(self):
        if self.sensor_unit_1 is None:
            return None
        is_analog = not self.sensor_unit_1 & 0xC0 == self.UNIT_1_NOT_ANALOG
        is_percentage = self.sensor_unit_1 & 0x01 == self.UNIT_1_PERCENTAGE
        assert not (is_analog and is_percentage)
        if is_analog:
            self.unit_name = self.UNIT_NAMES[self.sensor_unit_2]
            rate_unit = self.sensor_unit_1 & 0x38 >> 3
            if rate_unit != 0:
                rate_name = self.RATE_NAMES[rate_unit]
                self.unit_name = '%s %s' % (self.unit_name, rate_name)
            modifier = self.sensor_unit_1 & 0x07
            if modifier == self.UNIT_1_MODIFIER_USAGE_DIVIDE:
                assert self.sensor_unit_3 != self.UNIT_UNSPECIFIED
                modifier_name = self.UNIT_NAMES[self.sensor_unit_3]
                self.unit_name = '%s / %s' % (self.unit_name, modifier_name)
            elif modifier == self.UNIT_1_MODIFIER_USAGE_MULTIPLY:
                assert self.sensor_unit_3 != self.UNIT_UNSPECIFIED
                modifier_name = self.UNIT_NAMES[self.sensor_unit_3]
                self.unit_name = '%s * %s' % (self.unit_name, modifier_name)
        elif is_percentage:
            self.unit_name = '%'

    def _autofill_unit_thresholds(self):
        if self.unr_threshold is not None:
            self.unit_unr = self.decompress_unit_reading(self.unr_threshold)
        if self.uc_threshold is not None:
            self.unit_uc = self.decompress_unit_reading(self.uc_threshold)
        if self.unc_threshold is not None:
            self.unit_unc = self.decompress_unit_reading(self.unc_threshold)
        if self.lnr_threshold is not None:
            self.unit_lnr = self.decompress_unit_reading(self.lnr_threshold)
        if self.lc_threshold is not None:
            self.unit_lc = self.decompress_unit_reading(self.lc_threshold)
        if self.lnc_threshold is not None:
            self.unit_lnc = self.decompress_unit_reading(self.lnc_threshold)

    def autofill(self):
        self._autofill_unit_thresholds()
        self._autofill_unit_name()

    def compress_raw_reading(self, raw_reading):
        assert isinstance(self.m_factor, int)
        assert isinstance(self.b_factor, int)
        assert isinstance(self.b_exp, int)
        assert isinstance(self.r_exp, int)
        assert -512 <= self.m_factor <= 511 and self.m_factor != 0
        assert -512 <= self.b_factor <= 511
        assert -8 <= self.b_exp <= 7
        assert -8 <= self.r_exp <= 7
        unit_reading = int((self.m_factor * float(raw_reading) +
                            self.b_factor * pow(10, self.b_exp)) *
                           pow(10, self.r_exp))
        if self.sensor_unit_1 & 0xC0 == self.UNIT_1_UNSIGNED:
            assert 0 <= unit_reading <= 255
        elif self.sensor_unit_1 & 0xC0 == self.UNIT_1_SIGNED_2_COMPLEMENT:
            assert -128 <= unit_reading <= 127
        elif self.sensor_unit_1 & 0xC0 == self.UNIT_1_SIGNED_1_COMPLEMENT:
            assert -127 <= unit_reading <= 127
        elif self.sensor_unit_1 & 0x01 == self.UNIT_1_PERCENTAGE:
            assert 0 <= unit_reading <= 100
        else:
            assert False
        return unit_reading

    def decompress_unit_reading(self, unit_reading):
        if self.sensor_unit_1 & 0xC0 == self.UNIT_1_UNSIGNED:
            assert 0 <= unit_reading <= 255
        elif self.sensor_unit_1 & 0xC0 == self.UNIT_1_SIGNED_2_COMPLEMENT:
            assert -128 <= unit_reading <= 127
        elif self.sensor_unit_1 & 0xC0 == self.UNIT_1_SIGNED_1_COMPLEMENT:
            assert -127 <= unit_reading <= 127
        elif self.sensor_unit_1 & 0x01 == self.UNIT_1_PERCENTAGE:
            assert 0 <= unit_reading <= 100
        else:
            assert False
        assert isinstance(unit_reading, int)
        assert isinstance(self.m_factor, int)
        assert isinstance(self.b_factor, int)
        assert isinstance(self.b_exp, int)
        assert isinstance(self.r_exp, int)
        assert -512 <= self.m_factor <= 511 and self.m_factor != 0
        assert -512 <= self.b_factor <= 511
        assert -8 <= self.b_exp <= 7
        assert -8 <= self.r_exp <= 7
        raw_reading = ((float(unit_reading) / pow(10, self.r_exp) -
                        (self.b_factor * pow(10, self.b_exp))) /
                       self.m_factor)
        return raw_reading
# pylint: enable=too-many-instance-attributes
