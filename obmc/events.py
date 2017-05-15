# -*- coding: utf-8 -*-

# pylint: disable=attribute-defined-outside-init
# pylint: disable=missing-docstring

import datetime
import dbus
import fcntl
import struct

# pylint: disable=too-few-public-methods
# pylint: disable=too-many-instance-attributes
class Event(object):
    SEVERITY_INFO = 6
    SEVERITY_WARN = 4
    SEVERITY_CRIT = 2

    SIZE = 17

    # pylint: disable=invalid-name
    THRESHOLD_OR_GENERIC_EVENT_NAMES = ((
        # 0x00 RESERVED
    ), ( # 0x01
        'Lower Non-Critical Going Low',
        'Lower Non-Critical Going High',
        'Lower Critical Going Low',
        'Lower Critical Going High',
        'Lower Non-Recoverable Going Low',
        'Lower Non-Recoverable Going High',
        'Higher Non-Critical Going Low',
        'Higher Non-Critical Going High',
        'Higher Critical Going Low',
        'Higher Critical Going High',
        'Higher Non-Recoverable Going Low',
        'Higher Non-Recoverable Going High',
    ), ( # 0x02
        'Transition To Idle',
        'Transition To Active',
        'Transition To Busy',
    ), ( # 0x03
        'State Deasserted',
        'State Asserted',
    ), ( # 0x04
        'Predictive Failure Deasserted',
        'Predictive Failure Asserted',
    ), ( # 0x05
        'Limit Not Exceeded',
        'Limit Exceeded',
    ), ( # 0x06
        'Performance Met',
        'Performance Lags',
    ), ( # 0x07
        'Transition To OK',
        'Transition To Non-Critical From OK',
        'Transition To Critical From Less Severe',
        'Transition To Non-Recoverable From Less Severe',
        'Transition To Non-Critical From More Severe',
        'Transition To Critical From Non-Recoverable',
        'Transition To Non-Recoverable',
        'Monitor',
        'Informational',
    ), ( # 0x08
        'Device Removed / Device Absent',
        'Device Inserted / Device Present',
    ), ( # 0x09
        'Device Disabled',
        'Device Enabled',
    ), ( # 0x0A
        'Transition To Running',
        'Transition To In Test',
        'Transition To Power Off',
        'Transition To On Line',
        'Transition To Off Line',
        'Transition To Off Duty',
        'Transition To Degraded',
        'Transition To Power Save',
        'Install Error',
    ), ( # 0x0B
        'Fully Redundant',
        'Redundancy Lost',
        'Redundancy Degraded',
        'Non-Redundant: Sufficient Resources From Redundant',
        'Non-Redundant: Sufficient Resources From Insufficient Resources',
        'Non-Redundant: Insufficient Resources',
        'Redundancy Degraded From Fully Redundant',
        'Redundancy Degraded From Non-Redundant',
    ), ( # 0x0C
        'D0 Power State',
        'D1 Power State',
        'D2 Power State',
        'D3 Power State',
    ))
    # pylint: enable=invalid-name
    SENSOR_SPECIFIC_EVENT_NAMES = ((
        # index 0 RESERVED
    ), ( # 0x01
    ), ( # 0x02
    ), ( # 0x03
    ), ( # 0x04
    ), ( # 0x05
        'General Chassis Intrusion',
        'Drive Bay Intrusion',
        'I/O Card Area Intrusion',
        'Processor Area Intrusion',
        'LAN Leash Lost',
        'Unauthorized Dock',
        'FAN Area Intrusion',
    ), ( # 0x06
        'Secure Mode Violation Attemp',
        'Pre-Boot Password Violation - User Password',
        'Pre-Boot Password Violation Attemp - Setup Password',
        'Pre-Boot Password Violation - Network Bootk Password',
        'Other Pre-Boot Password Violation',
        'Out-Of-Band Access Password Violation',
    ), ( # 0x07
        'IERR',
        'Thermal Trip',
        'FRB1 / BIST Failure',
        'FRB2 / Hang In POST Failure',
        'FRB3 / Processor Startup / Initialization Failure',
        'Configuration Error',
        'SM BIOS Uncorrectable CPU-Complex Error',
        'Processor Presence Detected',
        'Processor Disabled',
        'Terminator Presence Detected',
        'Processor Automatically Throttled',
        'Machine Check Exception',
        'Correctable Machine Check Error',
    ), ( # 0x08
        'Presence Detected',
        'Power Supply Failure Detected',
        'Predictive Failure',
        'Power Supply Input Lost',
        'Power Supply Input Lost Or Out-Of-Range',
        'Power Supply Input Out-Of-Range, But Present',
        'Configuration Error',
        'Power Supply Inactive',
    ), ( # 0x09
        'Power Off / Power Down',
        'Power Cycle',
        '240VA Power Down',
        'Interlock Power Down',
        'AC Lost / Power Input Lost',
        'Soft Power Control Failure',
        'Power Unit Failure Detected',
        'Predictive Failure',
    ), ( # 0x0A
    ), ( # 0x0B
    ), ( # 0x0C
        'Correctable ECC / Other Correctable Memory Error',
        'Uncorrectable ECC / Other Uncorrectable Memory Error',
        'Parity',
        'Memory Scrub Failed',
        'Memory Device Disabled',
        'Correctable ECC / Other Correctable Memory Error Logging Limit '
        'Reached',
        'Presence Detected',
        'Configuration Error',
        'Spare',
        'Memory Automatically Throttled',
        'Critical Overtemperature',
    ), ( # 0x0D
        'Drive Presence',
        'Drive Fault',
        'Predictive Failure',
        'Hot Spare',
        'Consistency Check / Parity Check In Progress',
        'In Critical Array',
        'In Failed Array',
        'Rebuild / Remap In Progress',
        'Rebuild / Remap Aborted',
    ), ( # 0x0E
    ), ( # 0x0F
        'System Firmware Error',
        'System Firmware Hang',
        'System Firmware Progress',
    ), ( # 0x10
        'Correctable Memory Error Logging Disabled',
        'Event Type Logging Disabled',
        'Log Area Reset / Cleared',
        'All Event Logging Disabled',
        'SEL Full',
        'SEL Almost Full',
        'Correctable Machine Check Error Logging Disabled',
    ), ( # 0x11
        'BIOS Watchdog Reset',
        'OS Watchdog Reset',
        'OS Watchdog Shut Down',
        'OS Watchdog Power Down',
        'OS Watchdog Power Cycle',
        'OS Watchdog NMI / Diagnostic Interrupt',
        'OS Watchdog Expired, Status Only',
        'OS Watchdog Pre-Timeout Interrupt, Non-NMI',
    ), ( # 0x12
        'System Reconfigured',
        'OEM System Boot Event',
        'Undetermined System Hardware Failure',
        'Entry Added To Auxiliary Log',
        'PEF Action',
        'Timestamp Clock Synchronization',
    ), ( # 0x13
        'Front Panel NMI / Diagnostic Interrupt',
        'Bus Timeout',
        'I/O Channel Check NMI',
        'Software NMI',
        'PCI PERR',
        'PCI SERR',
        'EISA Fall Safe Timeout',
        'Bus Correctable Error',
        'Bus Uncorrectable Error',
        'Fatal NMI',
        'Bus Fatal Error',
        'Bus Degraded',
    ), ( # 0x14
        'Power Button Pressed',
        'Sleep Button Pressed',
        'Reset Button Pressed',
        'FRU Latch Open',
        'FRU Service Request Button',
    ), ( # 0x15
    ), ( # 0x16
    ), ( # 0x17
    ), ( # 0x18
    ), ( # 0x19
        'Soft Power Control Failure',
        'Thermal Trip',
    ), ( # 0x1A
    ), ( # 0x1B
        'Cable / Interconnect Is Connected',
        'Configuration Error',
    ), ( # 0x1C
    ), ( # 0x1D
        'Initiated By Power Up',
        'Initiated By Hard Reset',
        'Initiated By Warm Reset',
        'User Requested PXE Boot',
        'Automatic Boot To Diagnostic',
        'OS / Runtime Software Initiated Hard Reset',
        'OS / Runtime Software Initiated Warm Reset',
        'System Restart',
    ), ( # 0x1E
        'No Bootable Media',
        'Non-Bootable Diskette Left In Drive',
        'PXE Server Not Found',
        'Invalid Boot Sector',
        'Timeout Waiting For User Selection Of Boot Source',
    ), ( # 0x1F
        'A: Boot Completed',
        'C: Boot Completed',
        'PXE Boot Completed',
        'Diagnostic Boot Completed',
        'CD-ROM Boot Completed',
        'ROM Boot Completed',
        'Boot Completed',
        'Base OS / Hypervisor Installation Started',
        'Base OS / Hypervisor Installation Completed',
        'Base OS / Hypervisor Installation Aborted',
        'Base OS / Hypervisor Installation Failed',
    ), ( # 0x20
        'Critical Stop During OS Load / Initialization',
        'Runtime Critical Stop',
        'OS Graceful Stop',
        'OS Graceful Shutdown',
        'Soft Shutdown Initiated By PEF',
        'Agent Not Responding',
    ), ( # 0x21
        'Fault Status Asserted',
        'Identify Status Asserted',
        'Slot / Connector Device Installed / Attached',
        'Slot / Connector Ready For Device Installation',
        'Slot / Connector Ready For Device Removal',
        'Slot Power Is Off',
        'Slot / Connector Device Removal Request',
        'Interlock Asserted',
        'Slot Is Disabled',
        'Slot Holds Spare Device',
    ), ( # 0x22
        'S0 / G0',
        'S1',
        'S2',
        'S3',
        'S4',
        'S5 / G2',
        'S4 / S5',
        'G3 / Mechanical Off',
        'Sleeping In An S1, S2, Or S3 States',
        'G1 Sleeping',
        'S5 Entered By Override',
        'Legacy On State',
        'Legacy Off State',
        None,
        None,
        'Unknown',
    ), ( # 0x23
        'Time Expired',
        'Hard Reset',
        'Power Down',
        'Power Cycle',
        None,
        None,
        None,
        None,
        'Timer Interrupt',
    ), ( # 0x24
        'Platform Generated Page',
        'Platform Generated LAN Alert',
        'Platform Event Trap Generated',
        'Platform Generated SNMP Trap',
    ), ( # 0x25
        'Entity Present',
        'Entity Absent',
        'Entity Disabled',
    ), ( # 0x26
    ), ( # 0x27
        'LAN Heartbeat Lost',
        'LAN Heartbeat',
    ), ( # 0x28
        'Sensor Access Degraded Or Unavailable',
        'Controller Access Degraded Or Unavailable',
        'Management Controller Offline',
        'Management Controller Unavailable',
        'Sensor Failure',
        'FRU Failure',
    ), ( # 0x29
        'Battery Low',
        'Battery Failed',
        'Battery Presence Detected',
    ), ( # 0x2A
        'Sensor Activated',
        'Sensor Deactivated',
        'Invalid Username Or Password',
        'Invalid Password Disable',
    ), ( # 0x2B
        'Sensor Access Degraded Or Unavailable',
        'Controller Access Degraded Or Unavailable',
        'Management Controller Offline',
        'Management Controller Unavailable',
        'Sensor Failure',
        'FRU Failure',
    ), ( # 0x2C
        'FRU Not Installed',
        'FRU Inactive',
        'FRU Activation Requested',
        'FRU Activation In Progress',
        'FRU Active',
        'FRU Deactivation Requested',
        'FRU Deactivation In Progress',
        'FRU Communication Lost',
    ))
    SENSOR_SPECIFIC_OEM_EVENT_NAMES = ()
    OEM_EVENT_NAMES = ((
        # 0x70
    ), (
        # 0x71
    ), (
        # 0x72
    ), (
        # 0x73
    ), (
        # 0x74
    ), (
        # 0x75
    ), (
        # 0x76
    ), (
        # 0x77
    ), (
        # 0x78
    ), (
        # 0x79
    ), (
        # 0x7A
    ), (
        # 0x7B
    ), (
        # 0x7C
    ), (
        # 0x7D
    ), (
        # 0x7E
    ), (
        # 0x7F
    ))
    SENSOR_TYPE_NAMES = (
        None, # reserved
        'Temperature',
        'Voltage',
        'Current',
        'Fan',
        'Chassis Intrusion',
        'Platform Security',
        'Processor',
        'Power Supply',
        'Power Unit',
        'Cooling Device',
        'Other Units-Based Sensor',
        'Memory',
        'Drive Slot',
        'POST Memory Resize',
        'System Firmware Progress',
        'Event Logging Disabled',
        'Watchdog 1',
        'System Event',
        'Critical Interrupt',
        'Button / Switch',
        'Module / Board',
        'Microcontroller / Coprocessor',
        'Add-In Card',
        'Chassis',
        'Chip Set',
        'Other FRU',
        'Cable / Interconnect',
        'Terminator',
        'System Boot / Restart Initiated',
        'Boot Error',
        'Base OS Boot / Installation Status',
        'OS Stop / Shutdown',
        'Slot / Connector',
        'System ACPI Power State',
        'Watchdog 2',
        'Platform Alert',
        'Entity Presence',
        'Monitor ASIC / IC',
        'LAN',
        'Management Subsystem Health',
        'Battery',
        'Session Audit',
        'Version Change',
        'FRU State')
    EVENT_DATA_2_MESSAGE = {
        '#0F#00': (
            'unspecified',
            'no system memory is physically installed in the system',
            'no usable system memory',
            'unrecoverable hard-disk / atapi / ide device failure',
            'unrecoverable system-board failure',
            'unrecoverable diskette subsystem failure',
            'unrecoverable hard-disk controller failure',
            'unrecoverable ps/2 or usb keyboard failure',
            'removable boot media not found',
            'unrecoverable video controller failure',
            'no video device detected',
            'firmware (bios) rom corruption detected',
            'cpu voltage mismatch',
            'cpu speed matching failure'),
        '#0F#02': (
            'unspecified',
            'memory initialization',
            'hard-disk initialization',
            'secondary processor(s) initialization',
            'user authentication',
            'user-initialized system setup',
            'usb resource configuration',
            'pci resource configuration',
            'option rom initialization',
            'video initialization',
            'cache initialization',
            'sm bus initialization',
            'keyboard controller initialization',
            'embedded controller / management controller initialization',
            'docking station attachment',
            'enabling docking station',
            'docking station ejection',
            'disabling docking station',
            'calling operating system wake-up vector',
            'starting operating system boot process',
            'baseboard or motherboard initialization',
            'reserved',
            'floppy initialization',
            'keyboard test',
            'pointing device test',
            'primary processor initialization',
            ),
    }
    EVENT_DATA_3_MESSAGE = {
        '#08#06': (
            'vendor mismatch',
            'revision mismatch',
            'processor missing',
            'power supply rating mismatch',
            'voltage rating mismatch'),
    }

    # pylint: disable=too-many-arguments
    def __init__(
            self,
            severity=SEVERITY_INFO,
            sensor_type=0,
            sensor_number=0,
            event_dir_type=0,
            event_data_1=0,
            event_data_2=0,
            event_data_3=0):
        self.severity = severity
        self.sensor_type = sensor_type
        self.sensor_number = sensor_number
        self.event_dir_type = event_dir_type
        self.event_data_1 = event_data_1
        self.event_data_2 = event_data_2
        self.event_data_3 = event_data_3
        self.logid = 0
        self.time = 0
    # pylint: enable=too-many-arguments

    def __str__(self):
        if self.severity == self.SEVERITY_INFO:
            severity = 'INFO'
        elif self.severity == self.SEVERITY_WARN:
            severity = 'WARNING'
        elif self.severity == self.SEVERITY_CRIT:
            severity = 'CRITICAL'
        else:
            severity = 'INVALID_SEVERITY'
        return '%d %s %s 0x%02X 0x%02X 0x%02X 0x%02X 0x%02X' % (
            self.logid,
            self.time,
            severity,
            self.sensor_type,
            self.sensor_number,
            self.event_data_1,
            self.event_data_2,
            self.event_data_3)

    def _get_logid(self):
        return self._logid

    def _set_logid(self, logid):
        self._logid = int(logid)

    logid = property(_get_logid, _set_logid)

    def _get_time(self):
        return self._time

    def _set_time(self, timestamp):
        self._time = datetime.datetime.fromtimestamp(timestamp)

    time = property(_get_time, _set_time)

    def _get_severity(self):
        return self._severity

    def _set_severity(self, severity):
        if not (severity == self.SEVERITY_INFO or \
                severity == self.SEVERITY_WARN or \
                severity == self.SEVERITY_CRIT):
            raise ValueError('invalid severity %d' % severity)
        self._severity = severity

    severity = property(_get_severity, _set_severity)

    def stringify_severity(self):
        if self.severity == self.SEVERITY_INFO:
            return 'Info'
        elif self.severity == self.SEVERITY_WARN:
            return 'Warning'
        elif self.severity == self.SEVERITY_CRIT:
            return 'Critical'
        else:
            raise ValueError('invalid severity level %d' % self.severity)

    def _get_sensor_type(self):
        return self._sensor_type

    def _set_sensor_type(self, sensor_type):
        '''
        sensor_type must be of type uint8.
        '''
        if not 0 <= sensor_type <= 255:
            raise ValueError('sensor type %d out of range' % sensor_type)
        self._sensor_type = sensor_type

    sensor_type = property(_get_sensor_type, _set_sensor_type)

    # pylint: disable=too-many-return-statements
    def stringify_sensor_type(self):
        if 0x01 <= self.sensor_type <= 0x2C:
            return self.SENSOR_TYPE_NAMES[self.sensor_type]
        elif self.sensor_type == 0x00 or 0x2D <= self.sensor_type <= 0xBF:
            return 'RESERVED'
        else:
            raise NotImplementedError(
                'unknown name for sensor type 0x%02X' % self.sensor_type)
    # pylint: enable=too-many-return-statements

    def _get_sensor_number(self):
        return self._sensor_number

    def _set_sensor_number(self, sensor_number):
        '''
        sensor_number must be of type uint8.
        '''
        if not 0 <= sensor_number <= 255:
            raise ValueError('sensor number %d out of range' % sensor_number)
        self._sensor_number = sensor_number

    sensor_number = property(_get_sensor_number, _set_sensor_number)

    def _get_event_dir_type(self):
        return self._event_dir_type

    def _set_event_dir_type(self, event_dir_type):
        '''
        event_dir_type must be of type uint8.
        '''
        if not 0 <= event_dir_type <= 255:
            raise ValueError('event_dir_type %d out of range' % event_dir_type)
        self._event_dir_type = event_dir_type

    event_dir_type = property(_get_event_dir_type, _set_event_dir_type)

    def _get_event_dir(self):
        return self._event_dir_type >> 7

    event_dir = property(_get_event_dir)

    def _get_event_type(self):
        return self._event_dir_type & 0x7F

    event_type = property(_get_event_type)

    def _get_event_data_1(self):
        return self._event_data_1

    def _set_event_data_1(self, event_data_1):
        '''
        event_data_1 must be of type uint8_t.
        '''
        if not 0 <= event_data_1 <= 255:
            raise TypeError('event data 1 %d out of range' % event_data_1)
        self._event_data_1 = event_data_1

    event_data_1 = property(_get_event_data_1, _set_event_data_1)

    def _get_event_offset(self):
        return self.event_data_1 & 0x0F

    event_offset = property(_get_event_offset)

    def _get_event_data_2_usage(self):
        return (self.event_data_1 & 0xC0) >> 6

    event_data_2_usage = property(_get_event_data_2_usage)

    def _get_event_data_3_usage(self):
        return (self.event_data_1 & 0x30) >> 4

    event_data_3_usage = property(_get_event_data_3_usage)

    def _get_event_data_2(self):
        return self._event_data_2

    def _set_event_data_2(self, event_data_2):
        '''
        event_data_2 must be of type uint8_t.
        '''
        if not 0 <= event_data_2 <= 255:
            raise TypeError('event data 2 %d out of range' % event_data_2)
        self._event_data_2 = event_data_2

    event_data_2 = property(_get_event_data_2, _set_event_data_2)

    def _get_event_data_3(self):
        return self._event_data_3

    def _set_event_data_3(self, event_data_3):
        '''
        event_data_3 must be of type uint8_t.
        '''
        if not 0 <= event_data_3 <= 255:
            raise TypeError('event data 3 %d out of range' % event_data_3)
        self._event_data_3 = event_data_3

    event_data_3 = property(_get_event_data_3, _set_event_data_3)

    @staticmethod
    def _load_uint16(stream):
        uint8, = struct.unpack('@H', stream[:2])
        return (uint8, stream[2:])

    @staticmethod
    def _load_uint32(stream):
        uint8, = struct.unpack('@I', stream[:4])
        return (uint8, stream[4:])

    @staticmethod
    def _load_uint8(stream):
        uint8, = struct.unpack('@B', stream[:1])
        return (uint8, stream[1:])

    @classmethod
    def load(cls, stream):
        '''
        Create an Event instance from binary stream.
        '''
        log = cls()
        log.logid, stream = cls._load_uint16(stream)
        log.time, stream = cls._load_uint32(stream)
        _, stream = cls._load_uint32(stream)
        log.severity, stream = cls._load_uint8(stream)
        log.sensor_type, stream = cls._load_uint8(stream)
        log.sensor_number, stream = cls._load_uint8(stream)
        log.event_dir_type, stream = cls._load_uint8(stream)
        log.event_data_1, stream = cls._load_uint8(stream)
        log.event_data_2, stream = cls._load_uint8(stream)
        log.event_data_3, stream = cls._load_uint8(stream)
        return log

    # pylint: disable=invalid-name
    def _stringify_threshold_or_generic_event_name(self, event_offset):
        event_names = self.THRESHOLD_OR_GENERIC_EVENT_NAMES[self.event_type]
        if not 0 <= event_offset < len(event_names):
            # FIXME raise ValueError
            return ('invalid event offset %d (sensor 0x%02X, event tpye '
                    '0x%02X)' % (
                        event_offset, self.sensor_number, self.event_type))
            # raise ValueError(
            #     'invalid event offset %d (sensor 0x%02X, event tpye '
            #     '0x%02X)' % (
            #         event_offset, self.sensor_number, self.event_type))
        return event_names[event_offset]
    # pylint: enable=invalid-name

    # pylint: disable=invalid-name
    def _stringify_sensor_specific_event_name(self, event_offset):
        if 0x00 <= self.sensor_type <= 0x2C:
            event_names = self.SENSOR_SPECIFIC_EVENT_NAMES[self.sensor_type]
        elif 0x2D <= self.sensor_type <= 0xBF:
            # FIXME raise ValueError
            return 'reserved sensor type 0x%02X (sensor 0x%02X)' % (
                self.sensor_type, self.sensor_number)
            # raise ValueError(
            #     'reserved sensor type 0x%02X (sensor 0x%02X)' % (
            #         self.sensor_type, self.sensor_number))
        elif 0xC0 <= self.sensor_type <= 0xFF:
            offset = self.sensor_type - 0xC0
            event_names = self.SENSOR_SPECIFIC_OEM_EVENT_NAMES[offset]
        if not 0 <= event_offset < len(event_names):
            # FIXME raise ValueError
            return ('invalid event offset %d (sensor 0x%02X, event type 0x6F, '
                    'sensor type 0x%02X)' % (
                        event_offset, self.sensor_number, self.sensor_type))
            # raise ValueError(
            #     'invalid event offset %d (sensor 0x%02X, event type 0x6F, '
            #     'sensor type 0x%02X)' % (
            #         event_offset, self.sensor_number, self.sensor_type))
        return event_names[event_offset]
    # pylint: enable=invalid-name

    def _stringify_oem_event_name(self, event_offset):
        event_names = self.OEM_EVENT_NAMES[self.event_type - 0x70]
        if not 0 <= event_offset < len(event_names):
            # FIXME raise ValueError
            return ('invalid event offset %d (sensor 0x%02X, event type 0x%02X,'
                    ' sensor type 0x%02X)' % (
                        event_offset, self.sensor_number, self.event_type,
                        self.sensor_type))
            # raise ValueError(
            #     'invalid event offset %d (sensor 0x%02X, event type 0x%02X, '
            #     'sensor type 0x%02X)' % (
            #         event_offset, self.sensor_number, self.event_type,
            #         self.sensor_type))
        return event_names[event_offset]

    def _stringify_event_name(self, event_offset):
        if self.event_type == 0x00:
            # FIXME raise ValueError
            return 'reserved event type 0x00 (sensor 0x%02X)' % (
                self.sensor_number)
            # raise ValueError(
            #     'reserved event type 0x00 (sensor 0x%02X)' % (
            #         self.sensor_number))
        elif 0x01 <= self.event_type <= 0x0C:
            return self._stringify_threshold_or_generic_event_name(event_offset)
        elif 0x0D <= self.event_type <= 0x6E:
            # FIXME raise ValueError
            return 'reserved event type 0x%02X (sensor 0x%02X)' % (
                self.event_type, self.sensor_number)
            # raise ValueError(
            #     'reserved event type 0x%02X (sensor 0x%02X)' % (
            #         self.event_type, self.sensor_number))
        elif self.event_type == 0x6F:
            return self._stringify_sensor_specific_event_name(event_offset)
        elif 0x70 <= self.event_type <= 0x7F:
            return self._stringify_oem_event_name(event_offset)
        else:
            # FIXME raise ValueError
            return 'invalid event type %d (sensor 0x%02X)' % (
                self.event_type, self.sensor_number)
            # raise ValueError(
            #     'invalid event type %d (sensor 0x%02X)' % (
            #         self.event_type, self.sensor_number))

    # pylint: disable=invalid-name
    def _stringify_threshold_event_data_2(self):
        if self.event_data_2_usage == 0b00:
            return ''
        elif self.event_data_2_usage == 0b01:
            return ', trigger reading 0x%02X' % self.event_data_2
        elif self.event_data_2_usage == 0b10:
            return ', OEM event data 2 0x%02X' % self.event_data_2
        else:
            return (', sensor-specific event extension code 0x%02X '
                    'from event data 2' % self.event_data_2)
    # pylint: enable=invalid-name

    # pylint: disable=invalid-name
    def _stringify_threshold_event_data_3(self):
        if self.event_data_3_usage == 0b00:
            return ''
        elif self.event_data_3_usage == 0b01:
            return ', threshold 0x%02X' % self.event_data_3
        elif self.event_data_3_usage == 0b10:
            return ', OEM event data 3 0x%02X' % self.event_data_3
        else:
            return (', sensor-specific event extension code 0x%02X '
                    'from event data 3' % self.event_data_3)
    # pylint: enable=invalid-name

    # pylint: disable=invalid-name
    # pylint: disable=too-many-return-statements
    # pylint: disable=too-many-branches
    def _stringify_sensor_specific_event_data_2(self):
        # TODO implement
        if self.sensor_type == 0x05 and self.event_offset == 0x04:
            return ', NIC %d' % (self.event_data_2 + 1)
        elif self.sensor_type == 0x0F and self.event_offset == 0x00:
            return ', ' + self.EVENT_DATA_2_MESSAGE['#0F#00'][self.event_data_2]
        elif self.sensor_type == 0x0F and self.event_offset == 0x02:
            return ', ' + self.EVENT_DATA_2_MESSAGE['#0F#02'][self.event_data_2]
        elif self.sensor_type == 0x10 and self.event_offset == 0x00:
            return ', todo'
        elif self.sensor_type == 0x10 and self.event_offset == 0x01:
            return ', todo'
        elif self.sensor_type == 0x10 and self.event_offset == 0x06:
            return ', todo'
        elif self.sensor_type == 0x12 and self.event_offset == 0x03:
            return ', todo'
        elif self.sensor_type == 0x12 and self.event_offset == 0x04:
            return ', todo'
        elif self.sensor_type == 0x12 and self.event_offset == 0x05:
            return ', todo'
        elif self.sensor_type == 0x19 and self.event_offset == 0x00:
            return ', todo'
        elif self.sensor_type == 0x1D and self.event_offset == 0x07:
            return ', todo'
        elif self.sensor_type == 0x21 and self.event_offset == 0x09:
            return ', todo'
        elif self.sensor_type == 0x23 and self.event_offset == 0x08:
            return ', todo'
        elif self.sensor_type == 0x28 and self.event_offset == 0x04:
            return ', todo'
        elif self.sensor_type == 0x28 and self.event_offset == 0x05:
            return ', todo'
        elif self.sensor_type == 0x2A and self.event_offset == 0x03:
            return ', todo'
        elif self.sensor_type == 0x2B and self.event_offset == 0x07:
            return ', todo'
        elif self.sensor_type == 0x2C and self.event_offset == 0x07:
            return ', todo'
        return ''
    # pylint: enable=too-many-branches
    # pylint: enable=too-many-return-statements
    # pylint: enable=invalid-name

    # pylint: disable=invalid-name
    def _stringify_discrete_event_data_2(self):
        if self.event_data_2_usage == 0b00:
            return ''
        elif self.event_data_2_usage == 0b01:
            return ', previous state %s' % self._stringify_event_name(
                self.event_data_2 & 0x0F)
        elif self.event_data_2_usage == 0b10:
            return ', OEM event data 2 0x%02X' % self.event_data_2
        else:
            if self.event_type == 0x6F:
                return self._stringify_sensor_specific_event_data_2()
            else:
                return (', sensor-specific event extension code 0x%02X '
                        'from event data 2' % self.event_data_2)
    # pylint: enable=invalid-name

    # pylint: disable=invalid-name
    # pylint: disable=too-many-return-statements
    # pylint: disable=too-many-branches
    def _stringify_sensor_specific_event_data_3(self):
        # TODO implement
        if self.sensor_type == 0x08 and self.event_offset == 0x06:
            error_type = self.event_data_3 & 0x0F
            if 0x00 <= error_type <= 0x04:
                return ', ' + self.EVENT_DATA_3_MESSAGE['#08#06'][error_type]
            else:
                # FIXME raise ValueError
                return ('reserved error type 0x%02X (sensor 0x%02X, '
                        'event data 2 0x%02X)' % (
                            error_type, self.sensor_number, self.event_data_3))
                # raise ValueError(
                #     'reserved error type 0x%02X (sensor 0x%02X, '
                #     'event data 2 0x%02X)' % (
                #         error_type, self.sensor_number, self.event_data_3))
        elif self.sensor_type == 0x0C and self.event_offset == 0x08:
            return ', memory module 0x%02X' % self.event_data_3
        elif self.sensor_type == 0x10 and self.event_offset == 0x01:
            return ', todo'
        elif self.sensor_type == 0x10 and self.event_offset == 0x05:
            return ', todo'
        elif self.sensor_type == 0x10 and self.event_offset == 0x06:
            return ', todo'
        elif self.sensor_type == 0x19 and self.event_offset == 0x00:
            return ', todo'
        elif self.sensor_type == 0x1D and self.event_offset == 0x07:
            return ', todo'
        elif self.sensor_type == 0x21 and self.event_offset == 0x09:
            return ', todo'
        elif self.sensor_type == 0x28 and self.event_offset == 0x05:
            return ', todo'
        elif self.sensor_type == 0x2A and self.event_offset == 0x03:
            return ', todo'
        return ''
    # pylint: enable=too-many-branches
    # pylint: enable=too-many-return-statements
    # pylint: enable=invalid-name

    # pylint: disable=invalid-name
    def _stringify_discrete_event_data_3(self):
        if self.event_data_3_usage == 0b00:
            return ''
        elif self.event_data_3_usage == 0b01:
            # FIXME raise ValueError
            return ('reserved event data 3 usage 0b01 (sensor 0x%02X, event '
                    'type 0x%02X)' % (
                        self.sensor_number, self.event_type))
            # raise ValueError(
            #     'reserved event data 3 usage 0b01 (sensor 0x%02X, event type '
            #     '0x%02X)' % (
            #         self.sensor_number, self.event_type))
        elif self.event_data_3_usage == 0b10:
            return ', OEM event data 3 0x%02X' % self.event_data_3
        else:
            if self.event_type == 0x6F:
                return self._stringify_sensor_specific_event_data_3()
            else:
                return (', sensor-specific event extension code 0x%02X '
                        'from event data 3' % self.event_data_3)
    # pylint: enable=invalid-name

    def _stringify_oem_event_data_2(self):
        if self.event_data_2_usage == 0b00:
            return ''
        elif self.event_data_2_usage == 0b01:
            return ', previous state 0x%02X' % self.event_data_2
        elif self.event_data_2_usage == 0b10:
            return ', OEM event data 2 0x%02X' % self.event_data_2
        else:
            # FIXME raise ValueError
            return ('reserved event data 3 usage 0b11 (sensor 0x%02X, event '
                    'type 0x%02X)' % (
                        self.sensor_number, self.event_type))
            # raise ValueError(
            #     'reserved event data 3 usage 0b11 (sensor 0x%02X, event type '
            #     '0x%02X)' % (
            #         self.sensor_number, self.event_type))

    def _stringify_oem_event_data_3(self):
        if self.event_data_3_usage == 0b00:
            return ''
        elif self.event_data_3_usage == 0b01:
            # FIXME raise ValueError
            return ('reserved event data 3 usage 0b01 (sensor 0x%02X, event '
                    'type 0x%02X)' % (
                        self.sensor_number, self.event_type))
            # raise ValueError(
            #     'reserved event data 3 usage 0b01 (sensor 0x%02X, event type '
            #     '0x%02X)' % (
            #         self.sensor_number, self.event_type))
        elif self.event_data_3_usage == 0b10:
            return ', OEM event data 2 0x%02X' % self.event_data_2
        else:
            # FIXME raise ValueError
            return ('reserved event data 3 usage 0b11 (sensor 0x%02X, event '
                    'type 0x%02X)' % (
                        self.sensor_number, self.event_type))
            # raise ValueError(
            #     'reserved event data 3 usage 0b11 (sensor 0x%02X, event type '
            #     '0x%02X)' % (
            #         self.sensor_number, self.event_type))

    def _stringify_event_data(self):
        if self.event_type == 0x00:
            # FIXME raise ValueError
            return 'reserved event type 0x00 (sensor 0x%02X)' % (
                self.sensor_number)
            # raise ValueError(
            #     'reserved event type 0x00 (sensor 0x%02X)' % (
            #         self.sensor_number))
        elif self.event_type == 0x01:
            return (self._stringify_threshold_event_data_2() +
                    self._stringify_threshold_event_data_3())
        elif 0x02 <= self.event_type <= 0x0C:
            return (self._stringify_discrete_event_data_2() +
                    self._stringify_discrete_event_data_3())
        elif 0x0D <= self.event_type <= 0x6E:
            # FIXME raise ValueError
            return 'reserved event type 0x%02X (sensor 0x%02X)' % (
                self.event_type, self.sensor_number)
            # raise ValueError(
            #     'reserved event type 0x%02X (sensor 0x%02X)' % (
            #         self.event_type, self.sensor_number))
        elif self.event_type == 0x6F:
            return (self._stringify_discrete_event_data_2() +
                    self._stringify_discrete_event_data_3())
        elif 0x70 <= self.event_type <= 0x7F:
            return (self._stringify_oem_event_data_2() +
                    self._stringify_oem_event_data_3())
        else:
            # FIXME raise ValueError
            return 'invalid event type %d (sensor 0x%02X)' % (
                self.event_type, self.sensor_number)
            # raise ValueError(
            #     'invalid event type %d (sensor 0x%02X)' % (
            #         self.event_type, self.sensor_number))

    def assemble_message(self):
        # TODO add sensor name to message
        return 'Sensor (0x%02X) %s event %s%s' % (
            self.sensor_number,
            'deasserted' if self.event_dir else 'asserted',
            self._stringify_event_name(self.event_offset),
            self._stringify_event_data())
# pylint: enable=too-few-public-methods
# pylint: enable=too-many-instance-attributes

class EventManager(object):
    SERVICE_NAME = 'org.openbmc.records.events'
    LOCK_PATH = '/var/lib/obmc/events/lock'
    LOGS_PATH = '/var/lib/obmc/events/logs'
    LOG_FOLDER = '/var/lib/obmc/events'

    def __init__(self):
        self._bus = dbus.SystemBus()
        self._events = self._bus.get_object(
            self.SERVICE_NAME,
            '/org/openbmc/records/events')

    def _get_event_object(self, logid):
        object_path = '/org/openbmc/records/events/%d' % logid
        return self._bus.get_object(self.SERVICE_NAME, object_path)

    def add_log(self, log):
        '''
        Add log, modify and return its logid.
        If succeeds, a log ID between 1 and 65535 is returned.
        If fails, 0 is returned.
        '''
        log.logid = self._events.acceptBMCMessage(
            log.severity,
            log.sensor_type,
            log.sensor_number,
            log.event_dir_type,
            log.event_data_1,
            log.event_data_2,
            log.event_data_3,
            dbus_interface='org.openbmc.recordlog')
        return log.logid

    def get_log(self, logid):
        '''
        Get a log by ID.
        If event doesn't exist, None is returned.

        NOTE: instead of communicate with DBus, this function reads log from
        file system for the sake of performance.
        '''
        try:
            with open(self.LOCK_PATH) as lock_file:
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
                with open(self.LOGS_PATH) as logs_file:
                    logs_file.seek(self.log_position(logid))
                    content = logs_file.read(Event.SIZE)
                    event = Event.load(content)
                    return event if event.logid == logid else None
        except StandardError:
            return None

    def get_log_ids(self):
        '''
        Return a tuple of log IDs ordered by timestamp.
        '''
        logids = self._events.getAllLogIds(
            dbus_interface='org.openbmc.recordlog')
        return tuple(int(x) for x in logids)

    @staticmethod
    def log_position(logid):
        return Event.SIZE * (logid - 1)

    def remove_all_logs(self, sensor_number):
        '''
        Remove all logs.
        sensor_number is the sensor number of SEL device.
        '''
        return self._events.clear(
            sensor_number,
            dbus_interface='org.openbmc.recordlog')

    def remove_log(self, logid):
        '''
        Remove a log by ID.
        '''
        self._events.delete(logid, dbus_interface='org.openbmc.recordlog')
