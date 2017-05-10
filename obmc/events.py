# -*- coding: utf-8 -*-

# pylint: disable=attribute-defined-outside-init
# pylint: disable=missing-docstring

import datetime
import dbus
import os.path
import struct

# pylint: disable=too-few-public-methods
# pylint: disable=too-many-instance-attributes
class Event(object):
    SEVERITY_DEBUG = 'DEBUG'
    SEVERITY_INFO = 'INFO'
    SEVERITY_ERR = 'ERROR'

    # pylint: disable=too-many-arguments
    def __init__(
            self,
            severity=SEVERITY_INFO,
            message='',
            sensor_type='0',
            sensor_number='0',
            debug_data=''):
        self.severity = str(severity)
        self.message = message
        self.sensor_type = sensor_type
        self.sensor_number = sensor_number
        self.debug_data = debug_data
        self.logid = 0
        self.time = 0
    # pylint: enable=too-many-arguments

    def __str__(self):
        return '%d %s %s %s %s %s %s' % (
            self.logid,
            self.time,
            self.severity,
            self.message,
            self.sensor_type,
            self.sensor_number,
            ' '.join([('%02X' % x) for x in self.debug_data]))

    def _get_logid(self):
        return self._logid

    def _set_logid(self, logid):
        self._logid = int(logid)

    logid = property(_get_logid, _set_logid)

    def _get_severity(self):
        return self._severity

    def _set_severity(self, severity):
        if not (severity == self.SEVERITY_DEBUG or \
                severity == self.SEVERITY_INFO or \
                severity == self.SEVERITY_ERR):
            raise ValueError('invalid severity')
        self._severity = severity

    severity = property(_get_severity, _set_severity)

    def _get_message(self):
        return self._message

    def _set_message(self, message):
        self._message = str(message)

    message = property(_get_message, _set_message)

    def _get_sensor_type(self):
        '''Return sensor type in hexadecimal string'''
        return self._sensor_type

    def _set_sensor_type(self, sensor_type):
        '''
        sensor_type must be a text string representing a hexadecimal number
        ranged from 0 to 255.
        '''
        sensor_type = int(sensor_type, 16)
        if not 0 <= sensor_type <= 255:
            raise ValueError('sensor type %d out of range' % sensor_type)
        self._sensor_type = str('0x%02X' % sensor_type)

    sensor_type = property(_get_sensor_type, _set_sensor_type)

    def _get_sensor_number(self):
        '''Return sensor number in hexadecimal string'''
        return self._sensor_number

    def _set_sensor_number(self, sensor_number):
        '''
        sensor_number must be a text string representing a hexadecimal number
        ranged from 0 to 255.
        '''
        sensor_number = int(sensor_number, 16)
        if not 0 <= sensor_number <= 255:
            raise ValueError('sensor number %d out of range' % sensor_number)
        self._sensor_number = str('0x%02X' % sensor_number)

    sensor_number = property(_get_sensor_number, _set_sensor_number)

    def _get_debug_data(self):
        '''
        Return debug data as a list of uint8_t integers.
        '''
        return self._debug_data

    def _set_debug_data(self, debug_data):
        '''
        debug_data must be either a binary string or a list of uint8_t
        integers. It will be converted and saved internally as a list of
        uint8_t integers.
        '''
        if isinstance(debug_data, str):
            self._debug_data = [struct.unpack('@B', x)[0] for x in debug_data]
        elif isinstance(debug_data, list):
            for data in debug_data:
                if not (isinstance(data, int) and 0x0 <= x <= 0xFF):
                    raise TypeError(
                        'debug_data can be either a binary string or a list '
                        'of uint8_t integers')
            self._debug_data = debug_data
        else:
            raise TypeError(
                'debug_data can be either a binary string or a list '
                'of uint8_t integers')

    debug_data = property(_get_debug_data, _set_debug_data)

    def _get_time(self):
        return self._time.strftime('%Y:%m:%d %H:%M:%S')

    def _set_time(self, timestamp):
        self._time = datetime.datetime.fromtimestamp(timestamp)

    time = property(_get_time, _set_time)

    @staticmethod
    def _load_string(string_length, stream):
        string, = struct.unpack(
            '@%dsx' % (string_length - 1),
            stream[:string_length])
        return (string, stream[string_length:])

    @classmethod
    def load(cls, stream):
        '''
        Create an Event instance from binary stream.
        '''
        logid, tv_sec, _, message_len, \
            severity_len, sensor_type_len, sensor_number_len, \
            debug_data_len = \
            struct.unpack('@HIIHHHHHxx', stream[:24])
        stream = stream[24:]
        log = cls()
        log.logid = logid
        log.message, stream = cls._load_string(message_len, stream)
        log.severity, stream = cls._load_string(severity_len, stream)
        log.sensor_type, stream = cls._load_string(sensor_type_len, stream)
        log.sensor_number, stream = cls._load_string(sensor_number_len, stream)
        log.debug_data = stream[:debug_data_len]
        log.time = tv_sec
        return log
# pylint: enable=too-few-public-methods
# pylint: enable=too-many-instance-attributes

class EventManager(object):
    SERVICE_NAME = 'org.openbmc.records.events'
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
            str(log.severity),
            str(log.message),
            str(log.sensor_type),
            str(log.sensor_number),
            dbus.ByteArray(log.debug_data),
            dbus_interface='org.openbmc.recordlog')
        return log.logid

    def get_log(self, logid):
        '''
        Get a log by ID.
        If event doesn't exist, None is returned.

        NOTE: instead of communicate with DBus, this function reads log from
        file system for the sake of performance.
        '''
        path = os.path.join(self.LOG_FOLDER, str(logid))
        try:
            with open(path) as log_file:
                content = log_file.read()
                return Event.load(content)
        except IOError:
            return None

    def get_log_ids(self):
        '''
        Return a tuple of log IDs ordered by timestamp.
        '''
        logids = self._events.getAllLogIds(
            dbus_interface='org.openbmc.recordlog')
        return tuple(int(x) for x in logids)

    def remove_all_logs(self):
        '''
        Remove all logs.
        '''
        return self._events.clear(dbus_interface='org.openbmc.recordlog')

    def remove_log(self, logid):
        '''
        Remove a log by ID.
        '''
        object_path = '/org/openbmc/records/events/%d' % int(logid)
        event = self._bus.get_object(self.SERVICE_NAME, object_path)
        event.delete(dbus_interface='org.openbmc.Object.Delete')
