from flyteidl.admin import schedule_pb2 as _schedule_pb2

from flytekit.models import common as _common


class Schedule(_common.FlyteIdlEntity):
    class FixedRateUnit(object):
        MINUTE = _schedule_pb2.MINUTE
        HOUR = _schedule_pb2.HOUR
        DAY = _schedule_pb2.DAY

        @classmethod
        def enum_to_string(cls, int_value):
            """
            :param int_value:
            :rtype: Text
            """
            if int_value == cls.MINUTE:
                return "MINUTE"
            elif int_value == cls.HOUR:
                return "HOUR"
            elif int_value == cls.DAY:
                return "DAY"
            else:
                return "{}".format(int_value)

    class FixedRate(_common.FlyteIdlEntity):
        def __init__(self, value, unit):
            """
            :param int value:
            :param int unit: enum value from FixedRateUnit
            """
            self._value = value
            self._unit = unit

        @property
        def value(self):
            """
            :rtype: int
            """
            return self._value

        @property
        def unit(self):
            """
            :rtype: int
            """
            return self._unit

        def to_flyte_idl(self):
            """
            :rtype: flyteidl.admin.schedule_pb2.FixedRate
            """
            return _schedule_pb2.FixedRate(value=self.value, unit=self.unit)

        @classmethod
        def from_flyte_idl(cls, pb2_object):
            """
            :param flyteidl.admin.schedule_pb2.FixedRate pb2_object:
            :rtype: Schedule.FixedRate
            """
            return cls(pb2_object.value, pb2_object.unit)

    def __init__(self, kickoff_time_input_arg, cron_expression=None, rate=None):
        """
        One of cron_expression or fixed rate must be specified.

        :param Text kickoff_time_input_arg:
        :param Text cron_expression: [Optional]
        :param Schedule.FixedRate rate: [Optional]
        """
        self._kickoff_time_input_arg = kickoff_time_input_arg
        self._cron_expression = cron_expression
        self._rate = rate

    @property
    def kickoff_time_input_arg(self):
        return self._kickoff_time_input_arg

    @property
    def cron_expression(self):
        """
        :rtype: Text
        """
        return self._cron_expression

    @property
    def rate(self):
        """
        :rtype: Schedule.FixedRate
        """
        return self._rate

    @property
    def schedule_expression(self):
        return self.cron_expression or self.rate

    def to_flyte_idl(self):
        """
        :rtype: flyteidl.admin.schedule_pb2.Schedule
        """
        return _schedule_pb2.Schedule(
            kickoff_time_input_arg=self.kickoff_time_input_arg,
            cron_expression=self.cron_expression,
            rate=self.rate.to_flyte_idl() if self.rate is not None else None,
        )

    @classmethod
    def from_flyte_idl(cls, pb2_object):
        """
        :param flyteidl.admin.schedule_pb2.Schedule pb2_object:
        :rtype: Schedule
        """
        return cls(
            pb2_object.kickoff_time_input_arg,
            cron_expression=pb2_object.cron_expression if pb2_object.HasField("cron_expression") else None,
            rate=Schedule.FixedRate.from_flyte_idl(pb2_object.rate) if pb2_object.HasField("rate") else None,
        )
