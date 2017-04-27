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
    MAGIC_NUMBER = 0x4F424D43 # OBMC
    VERSION = 1
    SEVERITY_DEBUG = 'DEBUG'
    SEVERITY_INFO = 'INFO'
    SEVERITY_ERR = 'ERROR'

    # pylint: disable=too-many-arguments
    def __init__(
            self,
            severity=SEVERITY_INFO,
            message='',
            sensor_type='',
            sensor_number=0,
            association='',
            debug_data=''):
        self.severity = severity
        self.message = message
        self.sensor_type = sensor_type
        self.sensor_number = sensor_number
        self.association = association
        self.debug_data = debug_data
        self.logid = 0
        self.time = 0
        self.reported_by = 'BMC'
    # pylint: enable=too-many-arguments

    def __str__(self):
        return '%d %s %s %s %s %s %s %s %s' % (
            self.logid,
            self.time,
            self.reported_by,
            self.severity,
            self.message,
            self.sensor_type,
            self.sensor_number,
            self.association,
            self.debug_data)

    def _get_logid(self):
        return self._logid

    def _set_logid(self, logid):
        self._logid = int(logid)

    logid = property(_get_logid, _set_logid)

    def _get_severity(self):
        return self._severity

    def _set_severity(self, severity):
        # FIXME use predefined severity
        # if not (severity == self.SEVERITY_DEBUG or \
        #         severity == self.SEVERITY_INFO or \
        #         severity == self.SEVERITY_ERR):
        #     raise ValueError('invalid severity')
        # self._severity = severity
        self._severity = str(severity)

    severity = property(_get_severity, _set_severity)

    def _get_message(self):
        return self._message

    def _set_message(self, message):
        self._message = str(message)

    message = property(_get_message, _set_message)

    def _get_sensor_type(self):
        return self._sensor_type

    def _set_sensor_type(self, sensor_type):
        self._sensor_type = str(sensor_type)

    sensor_type = property(_get_sensor_type, _set_sensor_type)

    def _get_sensor_number(self):
        return self._sensor_number

    def _set_sensor_number(self, sensor_number):
        if isinstance(sensor_number, str) and sensor_number[:2] == '0x':
            self._sensor_number = sensor_number
            return
        if isinstance(sensor_number, unicode) and sensor_number[:2] == '0x':
            self._sensor_number = sensor_number
            return
        self._sensor_number = str('0x%02X' % int(sensor_number))

    sensor_number = property(_get_sensor_number, _set_sensor_number)

    def _get_association(self):
        return self._association

    def _set_association(self, association):
        self._association = str(association)

    association = property(_get_association, _set_association)

    def _get_debug_data(self):
        return self._debug_data

    def _set_debug_data(self, debug_data):
        self._debug_data = str(debug_data)

    debug_data = property(_get_debug_data, _set_debug_data)

    def _get_time(self):
        return self._time.strftime('%Y:%m:%d %H:%M:%S')

    def _set_time(self, timestamp):
        self._time = datetime.datetime.fromtimestamp(timestamp)

    time = property(_get_time, _set_time)

    def _get_reported_by(self):
        return self._reported_by

    def _set_reported_by(self, reporter):
        self._reported_by = str(reporter)

    reported_by = property(_get_reported_by, _set_reported_by)

    @staticmethod
    def _load_string(string_length, stream):
        '''
        TODO
        '''
        string, = struct.unpack(
            '@%dsx' % (string_length - 1),
            stream[:string_length])
        return (string, stream[string_length:])

    @classmethod
    def load(cls, stream):
        '''
        TODO
        '''
        magic_number, version, logid, tv_sec, _, message_len, \
            severity_len, sensor_type_len, sensor_number_len, \
            association_len, reporter_len, debug_data_len = \
            struct.unpack('@IHHIIHHHHHHHxx', stream[:32])
        if not (magic_number == cls.MAGIC_NUMBER and version == cls.VERSION):
            return None
        stream = stream[32:]
        log = cls()
        log.logid = logid
        log.message, stream = cls._load_string(message_len, stream)
        log.severity, stream = cls._load_string(severity_len, stream)
        log.sensor_type, stream = cls._load_string(sensor_type_len, stream)
        log.sensor_number, stream = cls._load_string(sensor_number_len, stream)
        log.association, stream = cls._load_string(association_len, stream)
        log.reported_by, stream = cls._load_string(reporter_len, stream)
        log.debug_data = stream[:debug_data_len]
        log.timestamp = tv_sec
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
            str(log.association),
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

    def remove_log(self, logid):
        '''
        Remove a log by ID.
        '''
        raise NotImplementedError()
