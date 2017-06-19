# pylint: disable=too-many-lines
# -*- coding: utf-8 -*-

# pylint: disable=missing-docstring

import dbus
import fcntl
import os.path
import zipfile

# pylint: disable=too-many-instance-attributes
class BaseEvent(object):
    SEVERITY_CRIT = 'Critical'
    SEVERITY_INFO = 'Info'
    SEVERITY_OKAY = 'OK'
    SEVERITY_WARN = 'Warning'

    ENTITIES = (
        'unspecified',
        'other',
        'unknown',
        'processor',
        'disk or disk array',
        'peripheral bay',
        'system management module',
        'system board',
        'memory module',
        'processor module',
        'power supply',
        'add-in card',
        'front panel board',
        'back panel board',
        'power system board',
        'drive backplane',
        'system internal expansion board',
        'other system board',
        'processor board',
        'power unit / power domain',
        'power module / DC-to-DC converter',
        'power management / power distribution board',
        'chassis back panel board',
        'system chassis',
        'sub-chassis',
        'other chassis board',
        'disk drive bay',
        'peripheral bay',
        'device bay',
        'fan / cooling device',
        'cooling unit / cooling domain',
        'cable / interconnect',
        'memory device',
        'system management software',
        'system firmware',
        'operating system',
        'system bus',
        'group',
        'remote management communication device',
        'external environment',
        'battery',
        'processing blade',
        'connectivity switch',
        'processor / memory module',
        'I/O module',
        'processor / I/O module',
        'management controller firmware',
        'IPMI channel',
        'PCI bus',
        'PCI Express bus',
        'SCSI bus',
        'SATA / SAS bus',
        'processor / front-side bus',
        'real time clock',
        None,
        'air inlet',
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        'air inlet',
        'processor / CPU',
        'baseboard / main system board',
    )
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
        'Upper Non-Critical Going Low',
        'Upper Non-Critical Going High',
        'Upper Critical Going Low',
        'Upper Critical Going High',
        'Upper Non-Recoverable Going Low',
        'Upper Non-Recoverable Going High',
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
        'FRU State',
    )
    # pylint: disable=invalid-name
    SENSOR_SPECIFIC_EVENT_DATA_2_MESSAGE = {
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
            'cpu speed matching failure',
        ),
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
        '#12#03:7:4': (
            'entry added',
            'entry added because event did not be map to standard IPMI event',
            'entry added along with one or more corresponding SEL entries',
            'log cleared',
            'log disabled',
            'log enabled',
        ),
        '#12#03:3:0': (
            'MCA log',
            'OEM 1',
            'OEM 2',
        ),
        '#19#00': (
            'S0 / G0',
            'S1',
            'S2',
            'S3',
            'S4',
            'S5 / G2',
            'S4 / S5',
            'G3 / mechanical off',
            'sleeping in an S1, S2, or S3 states',
            'G1 sleeping',
            'S5 entered by override',
            'legacy ON state',
            'legacy OFF state',
        ),
        '#1D#07': (
            'unknown',
            'chassis control command',
            'reset via pushbutton',
            'power-up via power pushbutton',
            'watchdog expiration',
            'OEM',
            ('automatic power-up on AC being applied due to "always restore" '
             'power restore policy'),
            ('automatic power-up on AC being applied due to "restore previous '
             'power state" power restore policy'),
            'reset via PEF',
            'soft reset',
            'power-up via RTC',
        ),
        '#21#09': (
            'PCI',
            'drive array',
            'external peripheral connector',
            'docking',
            'other standard internal expansion slot',
            'slot associated with entry ID',
            'AdvancedTCA',
            'DIMM/memory device',
            'FAN',
            'PCI Express',
            'SCSI (parallel)',
            'SATA / SAS',
        ),
        '#23#08:7:4': (
            'none',
            'SMI',
            'NMI',
            'messaging interrupt',
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            'unspecified',
        ),
        '#23#08:3:0': (
            None,
            'BIOS FRB2',
            'BIOS/POST',
            'OS Load',
            'SMS/OS',
            'OEM',
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            'unspecified',
        ),
        '#2B#07': (
            'unspecified',
            'management controller device ID',
            'management controller firmware revision',
            'management controller device revision',
            'management controller manufacturer ID',
            'management controller IPMI version',
            'management controller auxiliary firmware ID',
            'management controller firmware boot block',
            'other management controller firmware',
            'system firmware (EFI / BIOS) change',
            'SMBIOS change',
            'operating system change',
            'operating system loader change',
            'service or diagnostic partition change',
            'management software agent change',
            'management software application change',
            'management software middleware change',
            'programmable hardware change',
            'board/FRU component change',
            'board/FRU replaced with equivalent version',
            'board/FRU replaced with newer version',
            'board/FRU replaced with older version',
            'board/FRU hardware configuration change',
        ),
        '#2C:7:4': (
            'normal state change',
            'change commanded by software external to FRU',
            'state change due to operator changing a handle latch',
            'state change due to operator pressing the hot swap push button',
            'state change due to FRU programmatic action',
            'communication lost',
            'communication lost due to local failure',
            'state change due to unexpected extraction',
            'state change due to operator intervention/update',
            'unable to compute IPMB address',
            'unexpcted deactivation',
            None,
            None,
            None,
            None,
            'state change, cause unknown',
        ),
    }
    # pylint: enable=invalid-name
    # pylint: disable=invalid-name
    SENSOR_SPECIFIC_EVENT_DATA_3_MESSAGE = {
        '#08#06': (
            'vendor mismatch',
            'revision mismatch',
            'processor missing',
            'power supply rating mismatch',
            'voltage rating mismatch',
        ),
        '#19#00': (
            'S0 / G0',
            'S1',
            'S2',
            'S3',
            'S4',
            'S5 / G2',
            'S4 / S5',
            'G3 / mechanical off',
            'sleeping in an S1, S2, or S3 states',
            'G1 sleeping',
            'S5 entered by override',
            'legacy ON state',
            'legacy OFF state',
        ),
        '#2A:3:0': (
            'deactivation cause unspecified',
            'session deactivated by Close Session command',
            'session deactivated by timeout',
            'session deactivated by configuration change',
        ),
    }
    # pylint: enable=invalid-name
    OEM_CHANNEL_NAMES = ()
    OEM_USER_NAMES = ()
    # name of entities with entity_id in range [0x90, 0xAF]
    OEM_CHASSIS_ENTITIES = ()
    # name of entities with entity_id in range [0xB0, 0xCF]
    OEM_BOARDSET_ENTITIES = ()
    # name of entities with entity_id in range [0xD0, 0xFF]
    OEM_ENTITIES = ()
    # type of sensors with sensor_type in range [0xC0, 0xFF]
    OEM_SENSOR_TYPE_NAMES = ()
    # name of events with event_type in range [0x70, 0x7F]
    OEM_EVENT_NAMES = ()
    # name of events with event_type 0x6F and sensor_type in range [0xC0, 0xFF]
    OEM_SENSOR_SPECIFIC_EVENT_NAMES = ()
    # message of event with event_data_2_usage 0b10 and event_type in
    # range [0x70, 0x7F]
    OEM_EVENT_DATA_2_MESSAGE = {}
    # message of event with event_data_3_usage 0b10 and event_type in
    # range [0x70, 0x7F]
    OEM_EVENT_DATA_3_MESSAGE = {}
    # pylint: disable=invalid-name
    # message of event with event_data_2_usage 0b10 and event_type 0x6F or in
    # range [0x02, 0x0C]
    OEM_DISCRETE_EVENT_DATA_2_MESSAGE = {}
    # pylint: enable=invalid-name
    # pylint: disable=invalid-name
    # message of event with event_data_3_usage 0b10 and event_type 0x6F or in
    # range [0x02, 0x0C]
    OEM_DISCRETE_EVENT_DATA_3_MESSAGE = {}
    # pylint: enable=invalid-name

    def __init__(self):
        self.logical_timestamp = None
        self.log_id = None
        self.name = None
        self.record_id = None
        self.severity = None
        self.created = None
        self.entry_type = None
        self.entry_code = None
        self.sensor_type = None
        self.sensor_number = None
        self.message = None
        self.event_data_1 = None
        self.event_data_2 = None
        self.event_data_3 = None
        self.raw_data = None

    # pylint: disable=too-many-arguments
    @classmethod
    def _assemble_entry_code(cls,
                             sensor_type,
                             event_dir_type,
                             event_data_1):
        event_type = cls._get_event_type(event_dir_type)
        event_offset = cls._get_event_offset(event_data_1)
        return cls._stringify_event_name(sensor_type, event_type, event_offset)
    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @classmethod
    def _assemble_message(cls,
                          sensor_number,
                          sensor_type,
                          event_dir_type,
                          event_data_1,
                          event_data_2,
                          event_data_3):
        event_dir = cls._get_event_dir(event_dir_type)
        event_type = cls._get_event_type(event_dir_type)
        event_offset = cls._get_event_offset(event_data_1)
        # TODO replace sensor_type with sensor_name (need SDR)
        return '%s sensor 0x%02X %s %s%s' % (
            cls._stringify_sensor_type(sensor_type),
            sensor_number,
            'deasserted' if event_dir else 'asserted',
            cls._stringify_event_name(sensor_type, event_type, event_offset),
            cls._stringify_event_data(sensor_type,
                                      event_type,
                                      event_data_1,
                                      event_data_2,
                                      event_data_3))
    # pylint: enable=too-many-arguments

    @staticmethod
    def _get_event_data_2_usage(event_data_1):
        return (event_data_1 & 0xC0) >> 6

    @staticmethod
    def _get_event_data_3_usage(event_data_1):
        return (event_data_1 & 0x30) >> 4

    @staticmethod
    def _get_event_dir(event_dir_type):
        return event_dir_type >> 7

    @staticmethod
    def _get_event_offset(event_data_1):
        return event_data_1 & 0x0F

    @staticmethod
    def _get_event_type(event_dir_type):
        return event_dir_type & 0x7F

    # pylint: disable=invalid-name
    # pylint: disable=too-many-arguments
    @classmethod
    def _stringify_discrete_event_data_2(cls,
                                         sensor_type,
                                         event_type,
                                         event_data_1,
                                         event_data_2,
                                         event_data_3):
        event_data_2_usage = cls._get_event_data_2_usage(event_data_1)
        if event_data_2_usage == 0b00:
            return ''
        elif event_data_2_usage == 0b01:
            previous_event_offset = event_data_2 & 0x0F
            return ', previous state %s' % cls._stringify_event_name(
                sensor_type, event_type, previous_event_offset)
        elif event_data_2_usage == 0b10:
            index = '#%02X' % event_data_2
            if cls.OEM_DISCRETE_EVENT_DATA_2_MESSAGE.has_key(index):
                return ', ' + cls.OEM_DISCRETE_EVENT_DATA_2_MESSAGE[index]
            else:
                return cls._virtual_stringify_oem_discrete_event_data_2(
                    sensor_type,
                    event_type,
                    event_data_1,
                    event_data_2,
                    event_data_3)
        else:
            if event_type == 0x6F:
                return cls._stringify_sensor_specific_event_data_2(
                    sensor_type,
                    event_type,
                    event_data_1,
                    event_data_2,
                    event_data_3)
            else:
                return (', sensor-specific event extension code 0x%02X '
                        'from event data 2' % event_data_2)
    # pylint: enable=too-many-arguments
    # pylint: enable=invalid-name

    # pylint: disable=invalid-name
    # pylint: disable=too-many-arguments
    @classmethod
    def _stringify_discrete_event_data_3(cls,
                                         sensor_type,
                                         event_type,
                                         event_data_1,
                                         event_data_2,
                                         event_data_3):
        event_data_3_usage = cls._get_event_data_3_usage(event_data_1)
        if event_data_3_usage == 0b00:
            return ''
        elif event_data_3_usage == 0b01:
            raise ValueError('reserved event data 3 usage 0b01')
        elif event_data_3_usage == 0b10:
            index = '#%02X' % event_data_3
            if cls.OEM_DISCRETE_EVENT_DATA_3_MESSAGE.has_key(index):
                return ', ' + cls.OEM_DISCRETE_EVENT_DATA_3_MESSAGE[index]
            else:
                return cls._virtual_stringify_oem_discrete_event_data_3(
                    sensor_type,
                    event_type,
                    event_data_1,
                    event_data_2,
                    event_data_3)
        else:
            if event_type == 0x6F:
                return cls._stringify_sensor_specific_event_data_3(
                    sensor_type,
                    event_type,
                    event_data_1,
                    event_data_2,
                    event_data_3)
            else:
                return (', sensor-specific event extension code 0x%02X '
                        'from event data 3' % event_data_3)
    # pylint: enable=too-many-arguments
    # pylint: enable=invalid-name

    # pylint: disable=too-many-arguments
    @classmethod
    def _stringify_event_data(cls,
                              sensor_type,
                              event_type,
                              event_data_1,
                              event_data_2,
                              event_data_3):
        assert 0x00 <= event_type <= 0x7F
        if event_type == 0x00:
            raise ValueError('reserved event type 0x00')
        elif event_type == 0x01:
            return (cls._stringify_threshold_event_data_2(event_data_1,
                                                          event_data_2) +
                    cls._stringify_threshold_event_data_3(event_data_1,
                                                          event_data_3))
        elif 0x02 <= event_type <= 0x0C:
            return (cls._stringify_discrete_event_data_2(sensor_type,
                                                         event_type,
                                                         event_data_1,
                                                         event_data_2,
                                                         event_data_3) +
                    cls._stringify_discrete_event_data_3(sensor_type,
                                                         event_type,
                                                         event_data_1,
                                                         event_data_2,
                                                         event_data_3))
        elif 0x0D <= event_type <= 0x6E:
            raise ValueError('reserved event type 0x%02X' % event_type)
        elif event_type == 0x6F:
            return (cls._stringify_discrete_event_data_2(sensor_type,
                                                         event_type,
                                                         event_data_1,
                                                         event_data_2,
                                                         event_data_3) +
                    cls._stringify_discrete_event_data_3(sensor_type,
                                                         event_type,
                                                         event_data_1,
                                                         event_data_2,
                                                         event_data_3))
        elif 0x70 <= event_type <= 0x7F:
            return (cls._stringify_oem_event_data_2(event_type,
                                                    event_data_1,
                                                    event_data_2,
                                                    event_data_3) +
                    cls._stringify_oem_event_data_3(event_type,
                                                    event_data_1,
                                                    event_data_2,
                                                    event_data_3))
    # pylint: enable=too-many-arguments

    @classmethod
    def _stringify_event_name(cls, sensor_type, event_type, event_offset):
        assert 0x00 <= event_type <= 0x7F
        if event_type == 0x00:
            raise ValueError('reserved event type 0x00')
        elif 0x01 <= event_type <= 0x0C:
            return cls._stringify_threshold_or_generic_event_name(event_type,
                                                                  event_offset)
        elif 0x0D <= event_type <= 0x6E:
            raise ValueError('reserved event type 0x%02X' % event_type)
        elif event_type == 0x6F:
            return cls._stringify_sensor_specific_event_name(sensor_type,
                                                             event_offset)
        elif 0x70 <= event_type <= 0x7F:
            return cls._stringify_oem_event_name(event_type, event_offset)

    @classmethod
    def _stringify_oem_event_data_2(cls,
                                    event_type,
                                    event_data_1,
                                    event_data_2,
                                    event_data_3):
        event_data_2_usage = cls._get_event_data_2_usage(event_data_1)
        if event_data_2_usage == 0b00:
            return ''
        elif event_data_2_usage == 0b01:
            return ', previous state 0x%02X' % event_data_2
        elif event_data_2_usage == 0b10:
            index = '#%02X' % event_data_2
            if cls.OEM_EVENT_DATA_2_MESSAGE.has_key(index):
                return ', ' + cls.OEM_EVENT_DATA_2_MESSAGE[index]
            else:
                return cls._virtual_stringify_oem_event_data_2(event_type,
                                                               event_data_1,
                                                               event_data_2,
                                                               event_data_3)
        else:
            raise ValueError('reserved event data 2 usage 0b11')

    @classmethod
    def _stringify_oem_event_data_3(cls,
                                    event_type,
                                    event_data_1,
                                    event_data_2,
                                    event_data_3):
        event_data_3_usage = cls._get_event_data_3_usage(event_data_1)
        if event_data_3_usage == 0b00:
            return ''
        elif event_data_3_usage == 0b01:
            raise ValueError('reserved event data 3 usage 0b01')
        elif event_data_3_usage == 0b10:
            index = '#%02X' % event_data_3
            if cls.OEM_EVENT_DATA_3_MESSAGE.has_key(index):
                return ', ' + cls.OEM_EVENT_DATA_3_MESSAGE[index]
            else:
                return cls._virtual_stringify_oem_event_data_3(event_type,
                                                               event_data_1,
                                                               event_data_2,
                                                               event_data_3)
        else:
            raise ValueError('reserved event data 3 usage 0b11')

    @classmethod
    def _stringify_oem_event_name(cls, event_type, event_offset):
        event_names = cls.OEM_EVENT_NAMES[event_type - 0x70]
        return event_names[event_offset]

    # pylint: disable=invalid-name
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-return-statements
    # pylint: disable=too-many-statements
    @classmethod
    def _stringify_sensor_specific_event_data_2(cls,
                                                sensor_type,
                                                event_type,
                                                event_data_1,
                                                event_data_2,
                                                event_data_3):
        event_offset = cls._get_event_offset(event_data_1)
        if sensor_type == 0x05 and event_offset == 0x04:
            return ', NIC %d' % event_data_2
        elif sensor_type == 0x0F and event_offset == 0x00:
            messages = cls.SENSOR_SPECIFIC_EVENT_DATA_2_MESSAGE['#0F#00']
            return ', ' + messages[event_data_2]
        elif sensor_type == 0x0F and event_offset == 0x02:
            messages = cls.SENSOR_SPECIFIC_EVENT_DATA_2_MESSAGE['#0F#02']
            return ', ' + messages[event_data_2]
        elif sensor_type == 0x10 and event_offset == 0x00:
            return ', memory module %d' % event_data_2
        elif sensor_type == 0x10 and event_offset == 0x01:
            all_events = (event_data_3 & 0x20) >> 5
            if (event_data_3 & 0x10) >> 4 == 0:
                event_dir = 'deassertion'
            else:
                event_dir = 'assertion'
            event_type = event_data_2
            if all_events:
                event_name = 'all events of event type 0x%02X' % event_type
            else:
                affected_event_offset = event_data_3 & 0x0F
                event_name = cls._stringify_event_name(
                    sensor_type, event_type, affected_event_offset)
            return ', %s of %s' % (event_dir, event_name)
        elif sensor_type == 0x10 and event_offset == 0x06:
            return ', processor %d' % event_data_2
        elif sensor_type == 0x12 and event_offset == 0x03:
            messages1 = cls.SENSOR_SPECIFIC_EVENT_DATA_2_MESSAGE['#12#03:7:4']
            messages2 = cls.SENSOR_SPECIFIC_EVENT_DATA_2_MESSAGE['#12#03:3:0']
            return ', %s, %s' % (
                messages1[event_data_2],
                messages2[event_data_2])
        elif sensor_type == 0x12 and event_offset == 0x04:
            pef_actions = []
            if event_data_2 & 0x1:
                pef_actions.append('alert')
            if event_data_2 & 0x2:
                pef_actions.append('power off')
            if event_data_2 & 0x4:
                pef_actions.append('reset')
            if event_data_2 & 0x8:
                pef_actions.append('power cycle')
            if event_data_2 & 0x10:
                pef_actions.append('OEM action')
            if event_data_2 & 0x20:
                pef_actions.append('diagnostic interrupt (NMI)')
            if pef_actions:
                return ', PEF actions: %s' % ', '.join(pef_actions)
            else:
                return ''
        elif sensor_type == 0x12 and event_offset == 0x05:
            pair = 'second' if event_data_2 & 0x80 else 'first'
            device = 'SDR' if event_data_2 & 0x0F else 'SEL'
            return ', %s of pair, %s timestamp clock updated' % (pair, device)
        elif sensor_type == 0x19 and event_offset == 0x00:
            messages = cls.SENSOR_SPECIFIC_EVENT_DATA_2_MESSAGE['#19#00']
            return ', requested power state: ' + messages[event_data_2]
        elif sensor_type == 0x1D and event_offset == 0x07:
            restart_cause_index = event_data_2 & 0x0F
            messages = cls.SENSOR_SPECIFIC_EVENT_DATA_2_MESSAGE['#1D#07']
            return ', ' + messages[restart_cause_index]
        elif sensor_type == 0x21 and event_offset == 0x09:
            messages = cls.SENSOR_SPECIFIC_EVENT_DATA_2_MESSAGE['#21#09']
            return ', ' + messages[event_data_2]
        elif sensor_type == 0x23 and event_offset == 0x08:
            messages1 = cls.SENSOR_SPECIFIC_EVENT_DATA_2_MESSAGE['#23#08:7:4']
            messages2 = cls.SENSOR_SPECIFIC_EVENT_DATA_2_MESSAGE['#23#08:3:0']
            return ', type: %s, timer: %s' % (
                messages1[event_data_2],
                messages2[event_data_2])
        elif sensor_type == 0x28 and event_offset == 0x00:
            return ', sensor number 0x%02X' % event_data_2
        elif sensor_type == 0x28 and event_offset == 0x04:
            return ', sensor number 0x%02X' % event_data_2
        elif sensor_type == 0x28 and event_offset == 0x05:
            fru_type = 'logical' if event_data_2 & 0x80 else 'physical'
            if event_data_2 & 0x14:
                bus = 'LUN 0x%02X' % (event_data_2 & 0x14) >> 3
                if event_data_2 & 0x07:
                    bus += ', bus 0x%02X' % (event_data_2 & 0x07)
            else:
                bus = 'IPMB'
            return ', %s FRU, at %s' % (fru_type, bus)
        elif sensor_type == 0x2A:
            user_id = event_data_2 & 0x3F
            if user_id != 0:
                return ', user %s' % cls.OEM_USER_NAMES[user_id]
            else:
                return ', unspecified user'
        elif sensor_type == 0x2B and event_offset == 0x07:
            messages = cls.SENSOR_SPECIFIC_EVENT_DATA_2_MESSAGE['#2B#07']
            return ', ' + messages[event_data_2]
        elif sensor_type == 0x2C:
            cause_index = (event_data_2 & 0xF0) >> 4
            event_offset = event_data_2 & 0x0F
            messages = cls.SENSOR_SPECIFIC_EVENT_DATA_2_MESSAGE['#2C:7:4']
            return ', %s, previous state: %s' % (
                messages[cause_index],
                cls._stringify_sensor_specific_event_name(sensor_type,
                                                          event_offset))
        return ''
    # pylint: enable=too-many-statements
    # pylint: enable=too-many-return-statements
    # pylint: enable=too-many-locals
    # pylint: enable=too-many-branches
    # pylint: enable=too-many-arguments
    # pylint: enable=invalid-name

    # pylint: disable=invalid-name
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-return-statements
    # pylint: disable=unused-argument
    @classmethod
    def _stringify_sensor_specific_event_data_3(cls,
                                                sensor_type,
                                                event_type,
                                                event_data_1,
                                                event_data_2,
                                                event_data_3):
        event_offset = cls._get_event_offset(event_data_1)
        if sensor_type == 0x08 and event_offset == 0x06:
            error_type = event_data_3 & 0x0F
            if 0x00 <= error_type <= 0x04:
                messages = cls.SENSOR_SPECIFIC_EVENT_DATA_3_MESSAGE['#08#06']
                return ', ' + messages[error_type]
            else:
                raise ValueError('reserved error type 0x%02X'% error_type)
        elif sensor_type == 0x0C and event_offset == 0x08:
            return ', memory module 0x%02X' % event_data_3
        elif sensor_type == 0x10 and event_offset == 0x01:
            return '' # has been processed along with event_data_2
        elif sensor_type == 0x10 and event_offset == 0x05:
            if (event_data_3 & 0x80) >> 7:
                return ' (vendor-specific)'
            else:
                return '' # has been processed along with event_data_2
        elif sensor_type == 0x10 and event_offset == 0x06:
            return '' # has been processed along with event_data_2
        elif sensor_type == 0x19 and event_offset == 0x00:
            messages = cls.SENSOR_SPECIFIC_EVENT_DATA_3_MESSAGE['#19#00']
            return ', requested power state: ' + messages[event_data_3]
        elif sensor_type == 0x1D and event_offset == 0x07:
            return ', from channel %d' % event_data_3
        elif sensor_type == 0x21 and event_offset == 0x09:
            return ' %d' % event_data_3
        elif sensor_type == 0x28 and event_offset == 0x05:
            if (event_data_2 & 0x80) >> 7:
                return ', FRU device ID 0x%02X' % event_data_3
            else:
                slave_address = event_data_3 & 0xFE
                return ', slave address 0x%02X' % slave_address
        elif sensor_type == 0x2A:
            cause_index = (event_data_3 & 0x30) >> 4
            messages = cls.SENSOR_SPECIFIC_EVENT_DATA_3_MESSAGE['#2A:3:0']
            channel = event_data_3 & 0x0F
            return ', %s, channel %s' % (
                messages[cause_index],
                cls.OEM_CHANNEL_NAMES[channel])
        return ''
    # pylint: enable=unused-argument
    # pylint: enable=too-many-return-statements
    # pylint: enable=too-many-branches
    # pylint: enable=too-many-arguments
    # pylint: enable=invalid-name

    # pylint: disable=invalid-name
    @classmethod
    def _stringify_sensor_specific_event_name(cls, sensor_type, event_offset):
        assert 0x00 <= sensor_type <= 0xFF
        if 0x00 <= sensor_type <= 0x2C:
            event_names = cls.SENSOR_SPECIFIC_EVENT_NAMES[sensor_type]
        elif 0x2D <= sensor_type <= 0xBF:
            raise ValueError('reserved sensor type 0x%02X' % sensor_type)
        elif 0xC0 <= sensor_type <= 0xFF:
            offset = sensor_type - 0xC0
            event_names = cls.OEM_SENSOR_SPECIFIC_EVENT_NAMES[offset]
        return event_names[event_offset]
    # pylint: enable=invalid-name

    @classmethod
    def _stringify_sensor_type(cls, sensor_type):
        if 0x01 <= sensor_type <= 0x2C:
            return cls.SENSOR_TYPE_NAMES[sensor_type]
        elif 0xC0 <= sensor_type <= 0xFF:
            offset = sensor_type - 0xC0
            return cls.OEM_SENSOR_TYPE_NAMES[offset]
        else:
            raise ValueError('sensor type 0x%02X is reserved' % sensor_type)

    # pylint: disable=invalid-name
    @classmethod
    def _stringify_threshold_event_data_2(cls,
                                          event_data_1,
                                          event_data_2):
        event_data_2_usage = cls._get_event_data_2_usage(event_data_1)
        if event_data_2_usage == 0b00:
            return ''
        elif event_data_2_usage == 0b01:
            # TODO parse reading with SDR
            return ', trigger reading 0x%02X' % event_data_2
        elif event_data_2_usage == 0b10:
            return ', OEM event data 2 0x%02X' % event_data_2
        else:
            return (', sensor-specific event extension code 0x%02X '
                    'from event data 2' % event_data_2)
    # pylint: enable=invalid-name

    # pylint: disable=invalid-name
    @classmethod
    def _stringify_threshold_event_data_3(cls,
                                          event_data_1,
                                          event_data_3):
        event_data_3_usage = cls._get_event_data_3_usage(event_data_1)
        if event_data_3_usage == 0b00:
            return ''
        elif event_data_3_usage == 0b01:
            # TODO parse threshold with SDR
            return ', threshold 0x%02X' % event_data_3
        elif event_data_3_usage == 0b10:
            return ', OEM event data 3 0x%02X' % event_data_3
        else:
            return (', sensor-specific event extension code 0x%02X '
                    'from event data 3' % event_data_3)
    # pylint: enable=invalid-name

    # pylint: disable=invalid-name
    @classmethod
    def _stringify_threshold_or_generic_event_name(cls,
                                                   event_type,
                                                   event_offset):
        event_names = cls.THRESHOLD_OR_GENERIC_EVENT_NAMES[event_type]
        return event_names[event_offset]
    # pylint: enable=invalid-name

    # pylint: disable=invalid-name
    # pylint: disable=unused-argument
    # pylint: disable=too-many-arguments
    @classmethod
    def _virtual_stringify_oem_discrete_event_data_2(cls,
                                                     sensor_type,
                                                     event_type,
                                                     event_data_1,
                                                     event_data_2,
                                                     event_data_3):
        return ', OEM event data 2 0x%02X' % event_data_2
    # pylint: enable=too-many-arguments
    # pylint: enable=unused-argument
    # pylint: enable=invalid-name

    # pylint: disable=invalid-name
    # pylint: disable=unused-argument
    # pylint: disable=too-many-arguments
    @classmethod
    def _virtual_stringify_oem_discrete_event_data_3(cls,
                                                     sensor_type,
                                                     event_type,
                                                     event_data_1,
                                                     event_data_2,
                                                     event_data_3):
        return ', OEM event data 3 0x%02X' % event_data_3
    # pylint: enable=too-many-arguments
    # pylint: enable=unused-argument
    # pylint: enable=invalid-name

    # pylint: disable=invalid-name
    # pylint: disable=unused-argument
    @classmethod
    def _virtual_stringify_oem_event_data_2(cls,
                                            event_type,
                                            event_data_1,
                                            event_data_2,
                                            event_data_3):
        return ', OEM event data 2 0x%02X' % event_data_2
    # pylint: enable=unused-argument
    # pylint: enable=invalid-name

    # pylint: disable=invalid-name
    # pylint: disable=unused-argument
    @classmethod
    def _virtual_stringify_oem_event_data_3(cls,
                                            event_type,
                                            event_data_1,
                                            event_data_2,
                                            event_data_3):
        return ', OEM event data 3 0x%02X' % event_data_3
    # pylint: enable=unused-argument
    # pylint: enable=invalid-name

    # pylint: disable=too-many-arguments
    @classmethod
    def from_binary(cls,
                    severity,
                    sensor_type,
                    sensor_number,
                    event_dir_type,
                    event_data_1,
                    event_data_2=0xFF,
                    event_data_3=0xFF):
        event = cls()
        valid_severities = (cls.SEVERITY_CRIT,
                            cls.SEVERITY_INFO,
                            cls.SEVERITY_OKAY,
                            cls.SEVERITY_WARN)
        assert severity in valid_severities
        event.severity = severity
        event.entry_type = 'SEL' # XXX may change in future spec
        assert 0 <= sensor_type <= 255
        event.sensor_type = cls._stringify_sensor_type(sensor_type)
        assert 0 <= sensor_number <= 255
        event.sensor_number = '0x%02X' % sensor_number
        assert 0 <= event_dir_type <= 255
        assert 0 <= event_data_1 <= 255
        event.event_data_1 = '0x%02X' % event_data_1
        assert 0 <= event_data_2 <= 255
        event.event_data_2 = '0x%02X' % event_data_2
        assert 0 <= event_data_3 <= 255
        event.event_data_3 = '0x%02X' % event_data_3
        event.entry_code = cls._assemble_entry_code(sensor_type,
                                                    event_dir_type,
                                                    event_data_1)
        event.message = cls._assemble_message(sensor_number,
                                              sensor_type,
                                              event_dir_type,
                                              event_data_1,
                                              event_data_2,
                                              event_data_3)
        assert len(event.message) < 256
        event.raw_data = '0x%02X 0x%02X 0x%02X 0x%02X 0x%02X 0x%02X' % (
            sensor_type,
            sensor_number,
            event_dir_type,
            event_data_1,
            event_data_2,
            event_data_3)
        assert len(event.raw_data) == 29
        return event
    # pylint: enable=too-many-arguments

    @classmethod
    def from_file(cls, filepath, timestamp):
        event = cls()
        event.logical_timestamp = timestamp
        with open(filepath) as event_file:
            next_line = lambda: event_file.readline().strip()
            event.log_id = next_line()
            event.name = next_line()
            event.record_id = next_line()
            event.severity = next_line()
            event.created = next_line()
            event.entry_type = next_line()
            event.entry_code = next_line()
            event.sensor_type = next_line()
            event.sensor_number = next_line()
            event.message = next_line()
            event.raw_data = next_line()
        return event
# pylint: enable=too-many-instance-attributes

class Event(BaseEvent):
    OEM_CHANNEL_NAMES = (
        None,
        'Redfish',
        'SSH',
    )
    OEM_USER_NAMES = (
        None,
        'admin',
    )
    OEM_CHASSIS_ENTITIES = ()
    OEM_BOARDSET_ENTITIES = ()
    OEM_ENTITIES = ()
    OEM_SENSOR_TYPE_NAMES = (
        'System Throttle',
    )
    OEM_EVENT_NAMES = ((
        # 0x70 BMC Health
        'BMC Service Restarted',
        'Network Error',
        'Firmware Boot SPI Flash',
        'Hardware Watchdog Expired',
        'Empty FRU',
        'Alignment Traps',
        'BMC CPU Utilization',
        'BMC Memory Utilization',
        'BMC Reset',
        'DRAM ECC Errors',
        'I2C Bus Recovery',
        'Log Rollover',
        'No MAC Address Programmed Or Checksum Error In EEPROM',
        'Firmware Update Started',
        'Firmware Update Completed',
    ), (
        # 0x71 NTP Status
        None,
        'Sync Time from NTP',
        None,
        'NTP Server Sync Failed',
    ), (
        # 0x72 System Event
        'Power On',
        'Power Off',
    ))
    OEM_SENSOR_SPECIFIC_EVENT_NAMES = ()
    OEM_EVENT_DATA_2_MESSAGE = {}
    OEM_EVENT_DATA_3_MESSAGE = {}
    OEM_DISCRETE_EVENT_DATA_2_MESSAGE = {}
    OEM_DISCRETE_EVENT_DATA_3_MESSAGE = {}

    # pylint: disable=invalid-name
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-branches
    # pylint: disable=unused-argument
    @classmethod
    def _virtual_stringify_oem_discrete_event_data_2(cls,
                                                     sensor_type,
                                                     event_type,
                                                     event_data_1,
                                                     event_data_2,
                                                     event_data_3):
        if sensor_type == 0x08:
            events = []
            status_word_high = event_data_2
            if status_word_high & 0x04:
                events.append('FANS')
            if status_word_high & 0x08:
                events.append('POWER_GOOD#')
            if status_word_high & 0x20:
                events.append('INPUT')
            if status_word_high & 0x40:
                events.append('IOUT/POUT')
            if status_word_high & 0x80:
                events.append('VOUT')
            status_word_low = event_data_3
            if status_word_low & 0x02:
                events.append('CML')
            if status_word_low & 0x04:
                events.append('temperature')
            if status_word_low & 0x08:
                events.append('VIN_UV_FAULT')
            if status_word_low & 0x10:
                events.append('IOUT_OC_FAULT')
            if status_word_low & 0x20:
                events.append('VOUT_OV_FAULT')
            if status_word_low & 0x40:
                events.append('OFF')
            if events:
                return ', PSU events: (%s)' % ', '.join(events)
            else:
                return ''
        elif sensor_type == 0x25:
            entity_id = event_data_2
            if 0x00 <= entity_id <= 0x42:
                entity = cls.ENTITIES[entity_id]
            elif 0x43 <= entity_id <= 0x8F:
                raise ValueError('unsupported entity ID %d' % entity_id)
            elif 0x90 <= entity_id <= 0xAF:
                entity = cls.OEM_CHASSIS_ENTITIES[entity_id - 0x90]
            elif 0xB0 <= entity_id <= 0xCF:
                entity = cls.OEM_CHASSIS_ENTITIES[entity_id - 0xB0]
            elif 0xD0 <= entity_id <= 0xFF:
                entity = cls.OEM_CHASSIS_ENTITIES[entity_id - 0xD0]
            return ', %s' % entity
        elif sensor_type == 0xC0:
            power_consumption = (event_data_2 << 8) | event_data_3
            return ', aggregated power consumption %d' % power_consumption
        else:
            raise ValueError('unsupported sensor type 0x%02X' % sensor_type)
    # pylint: enable=unused-argument
    # pylint: enable=too-many-branches
    # pylint: enable=too-many-arguments
    # pylint: enable=invalid-name

    # pylint: disable=invalid-name
    # pylint: disable=too-many-arguments
    # pylint: disable=unused-argument
    @classmethod
    def _virtual_stringify_oem_discrete_event_data_3(cls,
                                                     sensor_type,
                                                     event_type,
                                                     event_data_1,
                                                     event_data_2,
                                                     event_data_3):
        if sensor_type == 0x08:
            return ''
        elif sensor_type == 0x25:
            entity_instance = event_data_3
            return ' %d' % entity_instance
        elif sensor_type == 0xC0:
            return ''
        else:
            raise ValueError('unsupported event type 0x%03X' % event_type)
    # pylint: enable=unused-argument
    # pylint: enable=too-many-arguments
    # pylint: enable=invalid-name

    # pylint: disable=invalid-name
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-return-statements
    @classmethod
    def _virtual_stringify_oem_event_data_2(cls,
                                            event_type,
                                            event_data_1,
                                            event_data_2,
                                            event_data_3):
        event_offset = cls._get_event_offset(event_data_1)
        if event_type == 0x70:
            if event_offset == 0x00:
                return ', service ID %d' % event_data_2
            elif event_offset == 0x01:
                if event_data_2 == 0x01:
                    return ', link down'
                elif event_data_2 == 0x02:
                    return ', link failure'
                else:
                    raise ValueError('unsupported link status 0x%02X' %
                                     event_data_2)
            elif event_offset == 0x02:
                if event_data_2 == 0x01:
                    return ', primary SPI'
                elif event_data_2 == 0x02:
                    return ', secondary SPI'
                else:
                    raise ValueError('unsupported SPI ID 0x%02X' % event_data_2)
            elif event_offset == 0x03:
                return ''
            elif event_offset == 0x04:
                return ', FRU %d' % event_data_2
            elif event_offset == 0x05:
                num_traps = (event_data_2 << 8) | event_data_3
                return ', %d times' % num_traps
            elif event_offset == 0x06:
                utilization = event_data_2
                return ', %d%%' % utilization
            elif event_offset == 0x07:
                memory_usage = event_data_2
                return ', %d MB' % memory_usage
            elif event_offset == 0x08:
                if event_data_2 == 0x01:
                    return ', register / pin reset'
                elif event_data_2 == 0x02:
                    return ', redfish reset'
                else:
                    raise ValueError('unsupported restart type 0x%02X' %
                                     event_data_2)
            elif event_offset == 0x09:
                # TODO implement this when specification is updated
                return ''
            elif event_offset == 0x0A:
                bus = event_data_2
                return ', bus %d' % bus
            elif event_offset == 0x0B:
                rollover_times = event_data_2
                return ', %d times' % rollover_times
            elif event_offset == 0x0C:
                return ''
            elif event_offset == 0x0D:
                if event_data_2 == 0x01:
                    return ', component = BMC'
                elif event_data_2 == 0x02:
                    return ', component = PSU'
                elif event_data_2 == 0x03:
                    return ', component = FPGA'
                else:
                    raise ValueError('unsupported component 0x%02X' %
                                     event_data_2)
            elif event_offset == 0x0E:
                if event_data_2 == 0x01:
                    return ', component = BMC'
                elif event_data_2 == 0x02:
                    return ', component = PSU'
                elif event_data_2 == 0x03:
                    return ', component = FPGA'
                else:
                    raise ValueError('unsupported component 0x%02X' %
                                     event_data_2)
            else:
                raise ValueError('unsupported event offset 0x%02X' %
                                 event_offset)
        else:
            raise ValueError('unsupported event type 0x%02X' % event_type)
    # pylint: enable=too-many-return-statements
    # pylint: enable=too-many-branches
    # pylint: enable=invalid-name

    # pylint: disable=invalid-name
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-return-statements
    @classmethod
    def _virtual_stringify_oem_event_data_3(cls,
                                            event_type,
                                            event_data_1,
                                            event_data_2,
                                            event_data_3):
        event_offset = cls._get_event_offset(event_data_1)
        if event_type == 0x70:
            if event_offset == 0x00:
                return ''
            elif event_offset == 0x01:
                return ''
            elif event_offset == 0x02:
                return ''
            elif event_offset == 0x03:
                return ''
            elif event_offset == 0x04:
                return ''
            elif event_offset == 0x05:
                return ''
            elif event_offset == 0x06:
                return ''
            elif event_offset == 0x07:
                return ''
            elif event_offset == 0x08:
                return ''
            elif event_offset == 0x09:
                return ''
            elif event_offset == 0x0A:
                error_code = event_data_3
                return ', error code %d' % error_code
            elif event_offset == 0x0B:
                return ''
            elif event_offset == 0x0C:
                return ''
            elif event_offset == 0x0D:
                if event_data_2 == 0x01:
                    if event_data_3 == 0x00:
                        return ', primary'
                    elif event_data_3 == 0x01:
                        return ', secondary'
                    else:
                        raise ValueError('unsupported BMC priority 0x%02X' %
                                         event_data_3)
                elif event_data_2 == 0x02:
                    return ', PSU %d' % event_data_3
                elif event_data_2 == 0x03:
                    return ', GPU %d' % event_data_3
                else:
                    raise ValueError('unknown event data 2 0x%02X' %
                                     event_data_2)
            elif event_offset == 0x0E:
                if event_data_2 == 0x01:
                    if event_data_3 == 0x00:
                        return ', primary'
                    elif event_data_3 == 0x01:
                        return ', secondary'
                    else:
                        raise ValueError('unsupported BMC priority 0x%02X' %
                                         event_data_3)
                elif event_data_2 == 0x02:
                    return ', PSU %d' % event_data_3
                elif event_data_2 == 0x03:
                    return ', GPU %d' % event_data_3
                else:
                    raise ValueError('unknown event data 2 0x%02X' %
                                     event_data_2)
            else:
                raise ValueError('unsupported event offset 0x%02X' %
                                 event_offset)
        else:
            raise ValueError('unsupported event type 0x%02X' % event_type)
    # pylint: enable=too-many-return-statements
    # pylint: enable=too-many-branches
    # pylint: enable=invalid-name

class EventManager(object):
    SERVICE_NAME = 'org.openbmc.records.events'
    LOCK_PATH = '/var/lib/obmc/events.lock'
    LOG_DIR_PATH = '/var/lib/obmc/events'
    SNAPSHOT_PATH = '/var/wcs/home/log-snapshot.zip'

    def __init__(self):
        self._bus = dbus.SystemBus()
        self._events = self._bus.get_object(
            self.SERVICE_NAME,
            '/org/openbmc/records/events')

    def clear(self, sensor_number):
        record_id = self._events.clear(
            sensor_number,
            dbus_interface='org.openbmc.recordlog')
        return record_id

    def create(self, event):
        assert isinstance(event.severity, str)
        assert isinstance(event.entry_type, str)
        assert isinstance(event.entry_code, str)
        assert isinstance(event.sensor_type, str)
        assert isinstance(event.sensor_number, str)
        assert isinstance(event.message, str)
        assert isinstance(event.raw_data, str)
        record_id = self._events.create(
            event.severity,
            event.entry_type,
            event.entry_code,
            event.sensor_type,
            event.sensor_number,
            event.message,
            event.raw_data,
            dbus_interface='org.openbmc.recordlog')
        return record_id

    def load_event(self, log_id):
        assert isinstance(log_id, str)
        with open(self.LOCK_PATH) as lock_file:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
            event_timestamp = None
            record_ids, timestamps = self.record_ids_and_logical_timestamps()
            for record_id, timestamp in zip(record_ids, timestamps):
                if record_id == int(log_id):
                    event_timestamp = timestamp
                    break
            if event_timestamp is None:
                raise RuntimeError('failed to locate event %d' % log_id)
            event_path = os.path.join(self.LOG_DIR_PATH, str(event_timestamp))
            event = Event.from_file(event_path, event_timestamp)
            return event

    def load_events(self):
        events = []
        with open(self.LOCK_PATH) as lock_file:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
            _, timestamps = self.record_ids_and_logical_timestamps()
            for timestamp in timestamps:
                event_path = os.path.join(self.LOG_DIR_PATH, str(timestamp))
                event = Event.from_file(event_path, timestamp)
                events.append(event)
        return events

    # pylint: disable=invalid-name
    def record_ids_and_logical_timestamps(self):
        record_ids, timestamps = \
            self._events.get_record_ids_and_logical_timestamps(
                dbus_interface='org.openbmc.recordlog')
        return record_ids, timestamps
    # pylint: enable=invalid-name

    def rollover_count(self):
        rollover_count = self._events.get_rollover_count(
            dbus_interface='org.openbmc.recordlog')
        return rollover_count

    def snapshot(self):
        with open(self.LOCK_PATH) as lock_file:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
            _, timestamps = self.record_ids_and_logical_timestamps()
            with zipfile.ZipFile(self.SNAPSHOT_PATH, 'w') as zip_file:
                for timestamp in timestamps:
                    event_path = os.path.join(self.LOG_DIR_PATH, str(timestamp))
                    zip_file.write(event_path, str(timestamp))
