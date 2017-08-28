# -*- coding: utf-8 -*-

# pylint: disable=missing-docstring

from obmc.sensor_data_record import SensorDataRecord

class BaseSensorDataRecordPool(object):
    def __init__(self):
        self.sdrs = []
        self.index_sensor_name = {}
        self.index_sensor_number = {}

    def _add(self, sdr):
        sdr.autofill()
        index = self._index_sensor_number(sdr.sensor_number)
        self.sdrs.append(sdr)
        self.index_sensor_name[sdr.sensor_name] = sdr
        self.index_sensor_number[index] = sdr

    @staticmethod
    def _index_sensor_number(sensor_number):
        assert isinstance(sensor_number, int)
        return '0x%02X' % sensor_number

    def get_by_sensor_name(self, sensor_name):
        return self.index_sensor_name[sensor_name]

    def get_by_sensor_number(self, sensor_number):
        index = self._index_sensor_number(sensor_number)
        return self.index_sensor_number[index]

class SensorDataRecordPool(BaseSensorDataRecordPool):
    def __init__(self):
        super(SensorDataRecordPool, self).__init__()
        self._init_inlet_temp_sensors()
        self._init_fan_tach_sensors()
        self._init_pwm_sensors()
        self._init_hsc_sensors()
        self._init_gpu_temp_sensors()
        self._init_psu_sensors()
        self._init_discrete_sensors()
        self._init_plx_switch_sensors()
        self._init_mdot2_temp_sensors()
        self._init_fpga1_temp_sensors()
        self._init_fpga2_temp_sensors()

    def _init_inlet_temp_sensors(self):
        self._create_inlet_temp('FIO Inlet Temp 1', 0x05)
        self._create_inlet_temp('FIO Inlet Temp 2', 0x06)

    def _init_fan_tach_sensors(self):
        self._create_fan_tach('Fan Tach 1', 0x11)
        self._create_fan_tach('Fan Tach 2', 0x12)
        self._create_fan_tach('Fan Tach 3', 0x13)
        self._create_fan_tach('Fan Tach 4', 0x14)
        self._create_fan_tach('Fan Tach 5', 0x15)
        self._create_fan_tach('Fan Tach 6', 0x16)
        self._create_fan_tach('Fan Tach 7', 0x17)
        self._create_fan_tach('Fan Tach 8', 0x18)
        self._create_fan_tach('Fan Tach 9', 0x19)
        self._create_fan_tach('Fan Tach 10', 0x1A)
        self._create_fan_tach('Fan Tach 11', 0x1B)
        self._create_fan_tach('Fan Tach 12', 0x1C)

    def _init_pwm_sensors(self):
        self._create_pwm('PWM 1', 0x1D)
        self._create_pwm('PWM 2', 0x1E)
        self._create_pwm('PWM 3', 0x1F)
        self._create_pwm('PWM 4', 0x20)
        self._create_pwm('PWM 5', 0x21)
        self._create_pwm('PWM 6', 0x22)

    def _init_hsc_sensors(self):
        self._create_hsc_vout('HSC1 VOUT', 0x23)
        self._create_hsc_temp('HSC1 Temp', 0x24)
        self._create_hsc_vout('HSC2 STBY VOUT', 0x25)
        self._create_hsc_temp('HSC2 STBY Temp', 0x26)
        self._create_hsc_gpu_vout('HSC3 GPU1 VOUT', 0x27)
        self._create_hsc_gpu_temp('HSC3 GPU1 Temp', 0x28)
        self._create_hsc_gpu_vout('HSC4 GPU2 VOUT', 0x29)
        self._create_hsc_gpu_temp('HSC4 GPU2 Temp', 0x2A)
        self._create_hsc_gpu_vout('HSC5 GPU3 VOUT', 0x2B)
        self._create_hsc_gpu_temp('HSC5 GPU3 Temp', 0x2C)
        self._create_hsc_gpu_vout('HSC6 GPU4 VOUT', 0x2D)
        self._create_hsc_gpu_temp('HSC6 GPU4 Temp', 0x2E)
        self._create_hsc_gpu_vout('HSC7 GPU5 VOUT', 0x2F)
        self._create_hsc_gpu_temp('HSC7 GPU5 Temp', 0x30)
        self._create_hsc_gpu_vout('HSC8 GPU6 VOUT', 0x31)
        self._create_hsc_gpu_temp('HSC8 GPU6 Temp', 0x32)
        self._create_hsc_gpu_vout('HSC9 GPU7 VOUT', 0x33)
        self._create_hsc_gpu_temp('HSC9 GPU7 Temp', 0x34)
        self._create_hsc_gpu_vout('HSC10 GPU8 VOUT', 0x35)
        self._create_hsc_gpu_temp('HSC10 GPU8 Temp', 0x36)

    def _init_plx_switch_sensors(self):
        self._create_plx_switch('PLX Switch 1 Temp', 0x37)
        self._create_plx_switch('PLX Switch 2 Temp', 0x38)
        self._create_plx_switch('PLX Switch 3 Temp', 0x39)
        self._create_plx_switch('PLX Switch 4 Temp', 0x3A)

    def _init_gpu_temp_sensors(self):
        self._create_gpu_temp('GPU1 Temp', 0x41)
        self._create_gpu_temp('GPU2 Temp', 0x42)
        self._create_gpu_temp('GPU3 Temp', 0x43)
        self._create_gpu_temp('GPU4 Temp', 0x44)
        self._create_gpu_temp('GPU5 Temp', 0x45)
        self._create_gpu_temp('GPU6 Temp', 0x46)
        self._create_gpu_temp('GPU7 Temp', 0x47)
        self._create_gpu_temp('GPU8 Temp', 0x48)

    def _init_psu_sensors(self):
        self._create_psu_pout('PSU1 Power Output', 0x50)
        self._create_psu_vout('PSU1 Voltage Output', 0x51)
        self._create_psu_temp('PSU1 Temp2', 0x52)
        self._create_psu_pout('PSU2 Power Output', 0x53)
        self._create_psu_vout('PSU2 Voltage', 0x54)
        self._create_psu_temp('PSU2 Temp2', 0x55)
        self._create_psu_pout('PSU3 Power Output', 0x56)
        self._create_psu_vout('PSU3 Voltage', 0x57)
        self._create_psu_temp('PSU3 Temp2', 0x58)
        self._create_psu_pout('PSU4 Power Output', 0x59)
        self._create_psu_vout('PSU4 Voltage', 0x5A)
        self._create_psu_temp('PSU4 Temp2', 0x5B)
        self._create_psu_pout('PSU5 Power Output', 0x5C)
        self._create_psu_vout('PSU5 Voltage', 0x5D)
        self._create_psu_temp('PSU5 Temp2', 0x5E)
        self._create_psu_pout('PSU6 Power Output', 0x5F)
        self._create_psu_vout('PSU6 Voltage', 0x60)
        self._create_psu_temp('PSU6 Temp2', 0x61)

    def _init_discrete_sensors(self):
        self._create_event_log('Event Log', 0x80)
        self._create_ntp_status('NTP Status', 0x81)
        self._create_bmc_health('BMC Health', 0x82)
        self._create_psu_status('PSU1 Status', 0x83)
        self._create_psu_status('PSU2 Status', 0x84)
        self._create_psu_status('PSU3 Status', 0x85)
        self._create_psu_status('PSU4 Status', 0x86)
        self._create_psu_status('PSU5 Status', 0x87)
        self._create_psu_status('PSU6 Status', 0x88)
        self._create_management_subsystem_health(
            'Management Subsystem Health',
            0x89)
        self._create_entity_presence('Entity Presence', 0x8A)
        self._create_system_throttle('System Throttle', 0x8B)
        self._create_session_audit('Session Audit', 0x8C)
        self._create_system_event('System Event', 0x8D)

    def _init_mdot2_temp_sensors(self):
        self._create_mdot2_temp('M.2 1 Temp', 0x70)
        self._create_mdot2_temp('M.2 2 Temp', 0x71)
        self._create_mdot2_temp('M.2 3 Temp', 0x72)
        self._create_mdot2_temp('M.2 4 Temp', 0x73)

    def _init_fpga1_temp_sensors(self):
        self._create_fpga1_temp('FPGA Die Temp', 0x74)

    def _init_fpga2_temp_sensors(self):
        self._create_fpga2_temp('FPGA Ambient Temp', 0x75)

    def _create_inlet_temp(self, sensor_name, sensor_number):
        sdr = SensorDataRecord()
        sdr.sensor_number = sensor_number
        sdr.sensor_type = 0x01
        sdr.event_type = 0x01
        sdr.assertion_event_mask = SensorDataRecord.SUPPORT_UC_GOING_HIGH
        sdr.deassertion_event_mask = SensorDataRecord.SUPPORT_UC_GOING_HIGH
        sdr.sensor_unit_1 = SensorDataRecord.UNIT_1_SIGNED_2_COMPLEMENT
        sdr.sensor_unit_2 = SensorDataRecord.UNIT_DEGREE_C
        sdr.sensor_unit_3 = SensorDataRecord.UNIT_UNSPECIFIED
        sdr.m_factor = 1
        sdr.b_factor = 0
        sdr.b_exp = 0
        sdr.r_exp = 0
        sdr.sensor_maximum_reading = None
        sdr.sensor_minimum_reading = None
        sdr.unr_threshold = None
        sdr.uc_threshold = sdr.compress_raw_reading(37)
        sdr.unc_threshold = None
        sdr.lnr_threshold = None
        sdr.lc_threshold = None
        sdr.lnc_threshold = None
        sdr.sensor_name = sensor_name
        self._add(sdr)

    def _create_fan_tach(self, sensor_name, sensor_number):
        sdr = SensorDataRecord()
        sdr.sensor_number = sensor_number
        sdr.sensor_type = 0x04
        sdr.event_type = 0x01
        sdr.assertion_event_mask = SensorDataRecord.SUPPORT_LC_GOING_HIGH
        sdr.deassertion_event_mask = SensorDataRecord.SUPPORT_LC_GOING_HIGH
        sdr.sensor_unit_1 = SensorDataRecord.UNIT_1_UNSIGNED
        sdr.sensor_unit_2 = SensorDataRecord.UNIT_RPM
        sdr.sensor_unit_3 = SensorDataRecord.UNIT_UNSPECIFIED
        sdr.m_factor = 1
        sdr.b_factor = 0
        sdr.b_exp = 0
        sdr.r_exp = -2
        sdr.sensor_maximum_reading = None
        sdr.sensor_minimum_reading = None
        sdr.unr_threshold = None
        sdr.uc_threshold = None
        sdr.unc_threshold = None
        sdr.lnr_threshold = None
        sdr.lc_threshold = sdr.compress_raw_reading(3800)
        sdr.lnc_threshold = None
        sdr.sensor_name = sensor_name
        self._add(sdr)

    def _create_pwm(self, sensor_name, sensor_number):
        sdr = SensorDataRecord()
        sdr.sensor_number = sensor_number
        sdr.sensor_type = 0x04
        sdr.event_type = 0x01
        sdr.assertion_event_mask = SensorDataRecord.SUPPORT_LC_GOING_HIGH
        sdr.deassertion_event_mask = SensorDataRecord.SUPPORT_LC_GOING_HIGH
        sdr.sensor_unit_1 = (
            SensorDataRecord.UNIT_1_NOT_ANALOG |
            SensorDataRecord.UNIT_1_PERCENTAGE)
        sdr.sensor_unit_2 = SensorDataRecord.UNIT_UNSPECIFIED
        sdr.sensor_unit_3 = SensorDataRecord.UNIT_UNSPECIFIED
        sdr.m_factor = 1
        sdr.b_factor = 0
        sdr.b_exp = 0
        sdr.r_exp = 0
        sdr.sensor_maximum_reading = None
        sdr.sensor_minimum_reading = None
        sdr.unr_threshold = None
        sdr.uc_threshold = None
        sdr.unc_threshold = None
        sdr.lnr_threshold = None
        sdr.lc_threshold = sdr.compress_raw_reading(18)
        sdr.lnc_threshold = None
        sdr.sensor_name = sensor_name
        self._add(sdr)

    def _create_hsc_vout(self, sensor_name, sensor_number):
        sdr = SensorDataRecord()
        sdr.sensor_number = sensor_number
        sdr.sensor_type = 0x02
        sdr.event_type = 0x01
        sdr.assertion_event_mask = (
            SensorDataRecord.SUPPORT_LC_GOING_HIGH |
            SensorDataRecord.SUPPORT_UC_GOING_HIGH)
        sdr.deassertion_event_mask = (
            SensorDataRecord.SUPPORT_LC_GOING_HIGH |
            SensorDataRecord.SUPPORT_UC_GOING_HIGH)
        sdr.sensor_unit_1 = SensorDataRecord.UNIT_1_UNSIGNED
        sdr.sensor_unit_2 = SensorDataRecord.UNIT_VOLTS
        sdr.sensor_unit_3 = SensorDataRecord.UNIT_UNSPECIFIED
        sdr.m_factor = 16
        sdr.b_factor = -40
        sdr.b_exp = 0
        sdr.r_exp = 0
        sdr.sensor_maximum_reading = None
        sdr.sensor_minimum_reading = None
        sdr.unr_threshold = None
        sdr.uc_threshold = sdr.compress_raw_reading(13.8)
        sdr.unc_threshold = None
        sdr.lnr_threshold = None
        sdr.lc_threshold = sdr.compress_raw_reading(10.6)
        sdr.lnc_threshold = None
        sdr.sensor_name = sensor_name
        self._add(sdr)

    def _create_hsc_temp(self, sensor_name, sensor_number):
        sdr = SensorDataRecord()
        sdr.sensor_number = sensor_number
        sdr.sensor_type = 0x01
        sdr.event_type = 0x01
        sdr.assertion_event_mask = SensorDataRecord.SUPPORT_UC_GOING_HIGH
        sdr.deassertion_event_mask = SensorDataRecord.SUPPORT_UC_GOING_HIGH
        sdr.sensor_unit_1 = SensorDataRecord.UNIT_1_UNSIGNED
        sdr.sensor_unit_2 = SensorDataRecord.UNIT_DEGREE_C
        sdr.sensor_unit_3 = SensorDataRecord.UNIT_UNSPECIFIED
        sdr.m_factor = 1
        sdr.b_factor = 0
        sdr.b_exp = 0
        sdr.r_exp = 0
        sdr.sensor_maximum_reading = None
        sdr.sensor_minimum_reading = None
        sdr.unr_threshold = None
        sdr.uc_threshold = sdr.compress_raw_reading(125)
        sdr.unc_threshold = None
        sdr.lnr_threshold = None
        sdr.lc_threshold = None
        sdr.lnc_threshold = None
        sdr.sensor_name = sensor_name
        self._add(sdr)

    def _create_hsc_gpu_vout(self, sensor_name, sensor_number):
        sdr = SensorDataRecord()
        sdr.sensor_number = sensor_number
        sdr.sensor_type = 0x02
        sdr.event_type = 0x01
        sdr.assertion_event_mask = (
            SensorDataRecord.SUPPORT_LC_GOING_HIGH |
            SensorDataRecord.SUPPORT_UC_GOING_HIGH)
        sdr.deassertion_event_mask = (
            SensorDataRecord.SUPPORT_LC_GOING_HIGH |
            SensorDataRecord.SUPPORT_UC_GOING_HIGH)
        sdr.sensor_unit_1 = SensorDataRecord.UNIT_1_SIGNED_2_COMPLEMENT
        sdr.sensor_unit_2 = SensorDataRecord.UNIT_VOLTS
        sdr.sensor_unit_3 = SensorDataRecord.UNIT_UNSPECIFIED
        sdr.m_factor = 8
        sdr.b_factor = -113
        sdr.b_exp = 0
        sdr.r_exp = 0
        sdr.sensor_maximum_reading = None
        sdr.sensor_minimum_reading = None
        sdr.unr_threshold = None
        sdr.uc_threshold = sdr.compress_raw_reading(13.8)
        sdr.unc_threshold = None
        sdr.lnr_threshold = None
        sdr.lc_threshold = sdr.compress_raw_reading(10.6)
        sdr.lnc_threshold = None
        sdr.sensor_name = sensor_name
        self._add(sdr)

    def _create_hsc_gpu_temp(self, sensor_name, sensor_number):
        sdr = SensorDataRecord()
        sdr.sensor_number = sensor_number
        sdr.sensor_type = 0x01
        sdr.event_type = 0x01
        sdr.assertion_event_mask = SensorDataRecord.SUPPORT_UC_GOING_HIGH
        sdr.deassertion_event_mask = SensorDataRecord.SUPPORT_UC_GOING_HIGH
        sdr.sensor_unit_1 = SensorDataRecord.UNIT_1_UNSIGNED
        sdr.sensor_unit_2 = SensorDataRecord.UNIT_DEGREE_C
        sdr.sensor_unit_3 = SensorDataRecord.UNIT_UNSPECIFIED
        sdr.m_factor = 1
        sdr.b_factor = -30
        sdr.b_exp = 0
        sdr.r_exp = 0
        sdr.sensor_maximum_reading = None
        sdr.sensor_minimum_reading = None
        sdr.unr_threshold = None
        sdr.uc_threshold = sdr.compress_raw_reading(125)
        sdr.unc_threshold = None
        sdr.lnr_threshold = None
        sdr.lc_threshold = None
        sdr.lnc_threshold = None
        sdr.sensor_name = sensor_name
        self._add(sdr)

    def _create_plx_switch(self, sensor_name, sensor_number):
        sdr = SensorDataRecord()
        sdr.sensor_number = sensor_number
        sdr.sensor_type = 0x01
        sdr.event_type = 0x01
        sdr.assertion_event_mask = SensorDataRecord.SUPPORT_UC_GOING_HIGH
        sdr.deassertion_event_mask = SensorDataRecord.SUPPORT_UC_GOING_HIGH
        sdr.sensor_unit_1 = SensorDataRecord.UNIT_1_UNSIGNED
        sdr.sensor_unit_2 = SensorDataRecord.UNIT_DEGREE_C
        sdr.sensor_unit_3 = SensorDataRecord.UNIT_UNSPECIFIED
        sdr.m_factor = 1
        sdr.b_factor = 0
        sdr.b_exp = 0
        sdr.r_exp = 0
        sdr.sensor_maximum_reading = None
        sdr.sensor_minimum_reading = None
        sdr.unr_threshold = None
        sdr.uc_threshold = sdr.compress_raw_reading(111)
        sdr.unc_threshold = None
        sdr.lnr_threshold = None
        sdr.lc_threshold = None
        sdr.lnc_threshold = None
        sdr.sensor_name = sensor_name
        self._add(sdr)

    def _create_gpu_temp(self, sensor_name, sensor_number):
        sdr = SensorDataRecord()
        sdr.sensor_number = sensor_number
        sdr.sensor_type = 0x01
        sdr.event_type = 0x01
        sdr.assertion_event_mask = SensorDataRecord.SUPPORT_UC_GOING_HIGH
        sdr.deassertion_event_mask = SensorDataRecord.SUPPORT_UC_GOING_HIGH
        sdr.sensor_unit_1 = SensorDataRecord.UNIT_1_UNSIGNED
        sdr.sensor_unit_2 = SensorDataRecord.UNIT_DEGREE_C
        sdr.sensor_unit_3 = SensorDataRecord.UNIT_UNSPECIFIED
        sdr.m_factor = 1
        sdr.b_factor = 0
        sdr.b_exp = 0
        sdr.r_exp = 0
        sdr.sensor_maximum_reading = None
        sdr.sensor_minimum_reading = None
        sdr.unr_threshold = None
        sdr.uc_threshold = sdr.compress_raw_reading(81)
        sdr.unc_threshold = None
        sdr.lnr_threshold = None
        sdr.lc_threshold = None
        sdr.lnc_threshold = None
        sdr.sensor_name = sensor_name
        self._add(sdr)

    def _create_psu_pout(self, sensor_name, sensor_number):
        sdr = SensorDataRecord()
        sdr.sensor_number = sensor_number
        sdr.sensor_type = 0x09
        sdr.event_type = 0x01
        sdr.assertion_event_mask = SensorDataRecord.SUPPORT_UC_GOING_HIGH
        sdr.deassertion_event_mask = SensorDataRecord.SUPPORT_UC_GOING_HIGH
        sdr.sensor_unit_1 = SensorDataRecord.UNIT_1_UNSIGNED
        sdr.sensor_unit_2 = SensorDataRecord.UNIT_WATTS
        sdr.sensor_unit_3 = SensorDataRecord.UNIT_UNSPECIFIED
        sdr.m_factor = 1
        sdr.b_factor = 0
        sdr.b_exp = 0
        sdr.r_exp = -1
        sdr.sensor_maximum_reading = None
        sdr.sensor_minimum_reading = None
        sdr.unr_threshold = None
        sdr.uc_threshold = sdr.compress_raw_reading(1760)
        sdr.unc_threshold = None
        sdr.lnr_threshold = None
        sdr.lc_threshold = None
        sdr.lnc_threshold = None
        sdr.sensor_name = sensor_name
        self._add(sdr)

    def _create_psu_vout(self, sensor_name, sensor_number):
        sdr = SensorDataRecord()
        sdr.sensor_number = sensor_number
        sdr.sensor_type = 0x09
        sdr.event_type = 0x01
        sdr.assertion_event_mask = (
            SensorDataRecord.SUPPORT_LC_GOING_HIGH |
            SensorDataRecord.SUPPORT_UC_GOING_HIGH)
        sdr.deassertion_event_mask = (
            SensorDataRecord.SUPPORT_LC_GOING_HIGH |
            SensorDataRecord.SUPPORT_UC_GOING_HIGH)
        sdr.sensor_unit_1 = SensorDataRecord.UNIT_1_UNSIGNED
        sdr.sensor_unit_2 = SensorDataRecord.UNIT_VOLTS
        sdr.sensor_unit_3 = SensorDataRecord.UNIT_UNSPECIFIED
        sdr.m_factor = 10
        sdr.b_factor = 0
        sdr.b_exp = 0
        sdr.r_exp = 0
        sdr.sensor_maximum_reading = None
        sdr.sensor_minimum_reading = None
        sdr.unr_threshold = None
        sdr.uc_threshold = sdr.compress_raw_reading(14.25)
        sdr.unc_threshold = None
        sdr.lnr_threshold = None
        sdr.lc_threshold = sdr.compress_raw_reading(10.5)
        sdr.lnc_threshold = None
        sdr.sensor_name = sensor_name
        self._add(sdr)

    def _create_psu_temp(self, sensor_name, sensor_number):
        sdr = SensorDataRecord()
        sdr.sensor_number = sensor_number
        sdr.sensor_type = 0x09
        sdr.event_type = 0x01
        sdr.assertion_event_mask = SensorDataRecord.SUPPORT_UC_GOING_HIGH
        sdr.deassertion_event_mask = SensorDataRecord.SUPPORT_UC_GOING_HIGH
        sdr.sensor_unit_1 = SensorDataRecord.UNIT_1_UNSIGNED
        sdr.sensor_unit_2 = SensorDataRecord.UNIT_DEGREE_C
        sdr.sensor_unit_3 = SensorDataRecord.UNIT_UNSPECIFIED
        sdr.m_factor = 1
        sdr.b_factor = 0
        sdr.b_exp = 0
        sdr.r_exp = 0
        sdr.sensor_maximum_reading = None
        sdr.sensor_minimum_reading = None
        sdr.unr_threshold = None
        sdr.uc_threshold = sdr.compress_raw_reading(95)
        sdr.unc_threshold = None
        sdr.lnr_threshold = None
        sdr.lc_threshold = None
        sdr.lnc_threshold = None
        sdr.sensor_name = sensor_name
        self._add(sdr)

    def _create_event_log(self, sensor_name, sensor_number):
        sdr = SensorDataRecord()
        sdr.sensor_number = sensor_number
        sdr.sensor_type = 0x10
        sdr.event_type = 0x6F
        sdr.assertion_event_mask = 0
        sdr.deassertion_event_mask = 0
        sdr.sensor_unit_1 = SensorDataRecord.UNIT_1_NOT_ANALOG
        sdr.sensor_unit_2 = None
        sdr.sensor_unit_3 = None
        sdr.m_factor = None
        sdr.b_factor = None
        sdr.b_exp = None
        sdr.r_exp = None
        sdr.sensor_maximum_reading = None
        sdr.sensor_minimum_reading = None
        sdr.unr_threshold = None
        sdr.uc_threshold = None
        sdr.unc_threshold = None
        sdr.lnr_threshold = None
        sdr.lc_threshold = None
        sdr.lnc_threshold = None
        sdr.sensor_name = sensor_name
        self._add(sdr)

    def _create_ntp_status(self, sensor_name, sensor_number):
        sdr = SensorDataRecord()
        sdr.sensor_number = sensor_number
        sdr.sensor_type = 0x12
        sdr.event_type = 0x71
        sdr.assertion_event_mask = 0
        sdr.deassertion_event_mask = 0
        sdr.sensor_unit_1 = SensorDataRecord.UNIT_1_NOT_ANALOG
        sdr.sensor_unit_2 = None
        sdr.sensor_unit_3 = None
        sdr.m_factor = None
        sdr.b_factor = None
        sdr.b_exp = None
        sdr.r_exp = None
        sdr.sensor_maximum_reading = None
        sdr.sensor_minimum_reading = None
        sdr.unr_threshold = None
        sdr.uc_threshold = None
        sdr.unc_threshold = None
        sdr.lnr_threshold = None
        sdr.lc_threshold = None
        sdr.lnc_threshold = None
        sdr.sensor_name = sensor_name
        self._add(sdr)

    def _create_bmc_health(self, sensor_name, sensor_number):
        sdr = SensorDataRecord()
        sdr.sensor_number = sensor_number
        sdr.sensor_type = 0x28
        sdr.event_type = 0x70
        sdr.assertion_event_mask = 0
        sdr.deassertion_event_mask = 0
        sdr.sensor_unit_1 = SensorDataRecord.UNIT_1_NOT_ANALOG
        sdr.sensor_unit_2 = None
        sdr.sensor_unit_3 = None
        sdr.m_factor = None
        sdr.b_factor = None
        sdr.b_exp = None
        sdr.r_exp = None
        sdr.sensor_maximum_reading = None
        sdr.sensor_minimum_reading = None
        sdr.unr_threshold = None
        sdr.uc_threshold = None
        sdr.unc_threshold = None
        sdr.lnr_threshold = None
        sdr.lc_threshold = None
        sdr.lnc_threshold = None
        sdr.sensor_name = sensor_name
        self._add(sdr)

    def _create_psu_status(self, sensor_name, sensor_number):
        sdr = SensorDataRecord()
        sdr.sensor_number = sensor_number
        sdr.sensor_type = 0x08
        sdr.event_type = 0x6F
        sdr.assertion_event_mask = 0
        sdr.deassertion_event_mask = 0
        sdr.sensor_unit_1 = SensorDataRecord.UNIT_1_NOT_ANALOG
        sdr.sensor_unit_2 = None
        sdr.sensor_unit_3 = None
        sdr.m_factor = None
        sdr.b_factor = None
        sdr.b_exp = None
        sdr.r_exp = None
        sdr.sensor_maximum_reading = None
        sdr.sensor_minimum_reading = None
        sdr.unr_threshold = None
        sdr.uc_threshold = None
        sdr.unc_threshold = None
        sdr.lnr_threshold = None
        sdr.lc_threshold = None
        sdr.lnc_threshold = None
        sdr.sensor_name = sensor_name
        self._add(sdr)

    # pylint: disable=invalid-name
    def _create_management_subsystem_health(self, sensor_name, sensor_number):
        sdr = SensorDataRecord()
        sdr.sensor_number = sensor_number
        sdr.sensor_type = 0x28
        sdr.event_type = 0x6F
        sdr.assertion_event_mask = 0
        sdr.deassertion_event_mask = 0
        sdr.sensor_unit_1 = SensorDataRecord.UNIT_1_NOT_ANALOG
        sdr.sensor_unit_2 = None
        sdr.sensor_unit_3 = None
        sdr.m_factor = None
        sdr.b_factor = None
        sdr.b_exp = None
        sdr.r_exp = None
        sdr.sensor_maximum_reading = None
        sdr.sensor_minimum_reading = None
        sdr.unr_threshold = None
        sdr.uc_threshold = None
        sdr.unc_threshold = None
        sdr.lnr_threshold = None
        sdr.lc_threshold = None
        sdr.lnc_threshold = None
        sdr.sensor_name = sensor_name
        self._add(sdr)
    # pylint: enable=invalid-name

    def _create_entity_presence(self, sensor_name, sensor_number):
        sdr = SensorDataRecord()
        sdr.sensor_number = sensor_number
        sdr.sensor_type = 0x25
        sdr.event_type = 0x6F
        sdr.assertion_event_mask = 0
        sdr.deassertion_event_mask = 0
        sdr.sensor_unit_1 = SensorDataRecord.UNIT_1_NOT_ANALOG
        sdr.sensor_unit_2 = None
        sdr.sensor_unit_3 = None
        sdr.m_factor = None
        sdr.b_factor = None
        sdr.b_exp = None
        sdr.r_exp = None
        sdr.sensor_maximum_reading = None
        sdr.sensor_minimum_reading = None
        sdr.unr_threshold = None
        sdr.uc_threshold = None
        sdr.unc_threshold = None
        sdr.lnr_threshold = None
        sdr.lc_threshold = None
        sdr.lnc_threshold = None
        sdr.sensor_name = sensor_name
        self._add(sdr)

    def _create_system_throttle(self, sensor_name, sensor_number):
        sdr = SensorDataRecord()
        sdr.sensor_number = sensor_number
        sdr.sensor_type = 0xC0
        sdr.event_type = 0x03
        sdr.assertion_event_mask = 0
        sdr.deassertion_event_mask = 0
        sdr.sensor_unit_1 = SensorDataRecord.UNIT_1_NOT_ANALOG
        sdr.sensor_unit_2 = None
        sdr.sensor_unit_3 = None
        sdr.m_factor = None
        sdr.b_factor = None
        sdr.b_exp = None
        sdr.r_exp = None
        sdr.sensor_maximum_reading = None
        sdr.sensor_minimum_reading = None
        sdr.unr_threshold = None
        sdr.uc_threshold = None
        sdr.unc_threshold = None
        sdr.lnr_threshold = None
        sdr.lc_threshold = None
        sdr.lnc_threshold = None
        sdr.sensor_name = sensor_name
        self._add(sdr)

    def _create_session_audit(self, sensor_name, sensor_number):
        sdr = SensorDataRecord()
        sdr.sensor_number = sensor_number
        sdr.sensor_type = 0x2A
        sdr.event_type = 0x6F
        sdr.assertion_event_mask = 0
        sdr.deassertion_event_mask = 0
        sdr.sensor_unit_1 = SensorDataRecord.UNIT_1_NOT_ANALOG
        sdr.sensor_unit_2 = None
        sdr.sensor_unit_3 = None
        sdr.m_factor = None
        sdr.b_factor = None
        sdr.b_exp = None
        sdr.r_exp = None
        sdr.sensor_maximum_reading = None
        sdr.sensor_minimum_reading = None
        sdr.unr_threshold = None
        sdr.uc_threshold = None
        sdr.unc_threshold = None
        sdr.lnr_threshold = None
        sdr.lc_threshold = None
        sdr.lnc_threshold = None
        sdr.sensor_name = sensor_name
        self._add(sdr)

    def _create_system_event(self, sensor_name, sensor_number):
        sdr = SensorDataRecord()
        sdr.sensor_number = sensor_number
        sdr.sensor_type = 0x12
        sdr.event_type = 0x72
        sdr.assertion_event_mask = 0
        sdr.deassertion_event_mask = 0
        sdr.sensor_unit_1 = SensorDataRecord.UNIT_1_NOT_ANALOG
        sdr.sensor_unit_2 = None
        sdr.sensor_unit_3 = None
        sdr.m_factor = None
        sdr.b_factor = None
        sdr.b_exp = None
        sdr.r_exp = None
        sdr.sensor_maximum_reading = None
        sdr.sensor_minimum_reading = None
        sdr.unr_threshold = None
        sdr.uc_threshold = None
        sdr.unc_threshold = None
        sdr.lnr_threshold = None
        sdr.lc_threshold = None
        sdr.lnc_threshold = None
        sdr.sensor_name = sensor_name
        self._add(sdr)

    def _create_mdot2_temp(self, sensor_name, sensor_number):
        sdr = SensorDataRecord()
        sdr.sensor_number = sensor_number
        sdr.sensor_type = 0x01
        sdr.event_type = 0x01
        sdr.assertion_event_mask = SensorDataRecord.SUPPORT_UC_GOING_HIGH
        sdr.deassertion_event_mask = SensorDataRecord.SUPPORT_UC_GOING_HIGH
        sdr.sensor_unit_1 = SensorDataRecord.UNIT_1_UNSIGNED
        sdr.sensor_unit_2 = SensorDataRecord.UNIT_DEGREE_C
        sdr.sensor_unit_3 = SensorDataRecord.UNIT_UNSPECIFIED
        sdr.m_factor = 1
        sdr.b_factor = 0
        sdr.b_exp = 0
        sdr.r_exp = 0
        sdr.sensor_maximum_reading = None
        sdr.sensor_minimum_reading = None
        sdr.unr_threshold = None
        sdr.uc_threshold = sdr.compress_raw_reading(85)
        sdr.unc_threshold = None
        sdr.lnr_threshold = None
        sdr.lc_threshold = None
        sdr.lnc_threshold = None
        sdr.sensor_name = sensor_name
        self._add(sdr)

    def _create_fpga1_temp(self, sensor_name, sensor_number):
        sdr = SensorDataRecord()
        sdr.sensor_number = sensor_number
        sdr.sensor_type = 0x01
        sdr.event_type = 0x01
        sdr.assertion_event_mask = SensorDataRecord.SUPPORT_UC_GOING_HIGH
        sdr.deassertion_event_mask = SensorDataRecord.SUPPORT_UC_GOING_HIGH
        sdr.sensor_unit_1 = SensorDataRecord.UNIT_1_UNSIGNED
        sdr.sensor_unit_2 = SensorDataRecord.UNIT_DEGREE_C
        sdr.sensor_unit_3 = SensorDataRecord.UNIT_UNSPECIFIED
        sdr.m_factor = 1
        sdr.b_factor = 0
        sdr.b_exp = 0
        sdr.r_exp = 0
        sdr.sensor_maximum_reading = None
        sdr.sensor_minimum_reading = None
        sdr.unr_threshold = None
        sdr.uc_threshold = sdr.compress_raw_reading(83)
        sdr.unc_threshold = None
        sdr.lnr_threshold = None
        sdr.lc_threshold = None
        sdr.lnc_threshold = None
        sdr.sensor_name = sensor_name
        self._add(sdr)

    def _create_fpga2_temp(self, sensor_name, sensor_number):
        sdr = SensorDataRecord()
        sdr.sensor_number = sensor_number
        sdr.sensor_type = 0x01
        sdr.event_type = 0x01
        sdr.assertion_event_mask = SensorDataRecord.SUPPORT_UC_GOING_HIGH
        sdr.deassertion_event_mask = SensorDataRecord.SUPPORT_UC_GOING_HIGH
        sdr.sensor_unit_1 = SensorDataRecord.UNIT_1_UNSIGNED
        sdr.sensor_unit_2 = SensorDataRecord.UNIT_DEGREE_C
        sdr.sensor_unit_3 = SensorDataRecord.UNIT_UNSPECIFIED
        sdr.m_factor = 1
        sdr.b_factor = 0
        sdr.b_exp = 0
        sdr.r_exp = 0
        sdr.sensor_maximum_reading = None
        sdr.sensor_minimum_reading = None
        sdr.unr_threshold = None
        sdr.uc_threshold = sdr.compress_raw_reading(83)
        sdr.unc_threshold = None
        sdr.lnr_threshold = None
        sdr.lc_threshold = None
        sdr.lnc_threshold = None
        sdr.sensor_name = sensor_name
        self._add(sdr)

SDRS = SensorDataRecordPool()
