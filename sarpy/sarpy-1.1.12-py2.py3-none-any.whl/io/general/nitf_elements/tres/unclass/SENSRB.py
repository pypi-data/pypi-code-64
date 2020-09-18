# -*- coding: utf-8 -*-

import logging
from ..tre_elements import TREExtension, TREElement

__classification__ = "UNCLASSIFIED"
__author__ = "Thomas McCullough"


def get_ref_type_length(typ_val):
    typ_val = typ_val.lower()
    if typ_val in ['06a', '06c']:
        return 11
    elif typ_val == '06b':
        return 12
    elif typ_val in ['06d', '06e', '06f']:
        return 8
    elif typ_val in [
            '07b', '07d', '07h', '08a', '08b', '08c', '08d', '08e', '08f', '08g',
            '08h', '08i', '09a', '09b', '09c', '09d']:
        return 10
    elif typ_val in ['07c', '07f', '07g', '10a', '10b', '10c']:
        return 9
    else:
        logging.error(
            'An unknown type value {} was found when deserializing a SENSRB TRE object. '
            'Something may fail in this deserialization.')
        return None


class POINT(TREElement):
    def __init__(self, value):
        super(POINT, self).__init__()
        self.add_field('P_ROW', 'd', 8, value)
        self.add_field('P_COLUMN', 'd', 8, value)
        self.add_field('P_LATITUDE', 'd', 10, value)
        self.add_field('P_LONGITUDE', 'd', 11, value)
        self.add_field('P_ELEVATION', 'd', 6, value)
        self.add_field('P_RANGE', 'd', 8, value)


class POINT_SET(TREElement):
    def __init__(self, value):
        super(POINT_SET, self).__init__()
        self.add_field('POINT_SET_TYPE', 's', 25, value)
        self.add_field('POINT_COUNT', 'd', 3, value)
        self.add_loop('POINTs', self.POINT_COUNT, POINT, value)


class TIME_STAMP(TREElement):
    def __init__(self, value, time_len):
        super(TIME_STAMP, self).__init__()
        self.add_field('TIME_STAMP_TIME', 'd', 12, value)
        if time_len is not None:
            self.add_field('TIME_STAMP_VALUE', 'd', time_len, value)


class TIME_STAMPED_DATA(TREElement):
    def __init__(self, value):
        super(TIME_STAMPED_DATA, self).__init__()
        self.add_field('TIME_STAMP_TYPE', 's', 3, value)
        self.add_field('TIME_STAMP_COUNT', 'd', 4, value)
        self.add_loop(
            'TIME_STAMPs', self.TIME_STAMP_COUNT, TIME_STAMP, value,
            get_ref_type_length(self.TIME_STAMP_TYPE))


class PIXEL_REFERENCE(TREElement):
    def __init__(self, value, pixel_ref_len):
        super(PIXEL_REFERENCE, self).__init__()
        self.add_field('PIXEL_REFERENCE_ROW', 'd', 8, value)
        self.add_field('PIXEL_REFERENCE_COLUMN', 'd', 8, value)
        if pixel_ref_len is not None:
            self.add_field('PIXEL_REFERENCE_VALUE', 'd', pixel_ref_len, value)


class PIXEL_REFERENCED_DATA(TREElement):
    def __init__(self, value):
        super(PIXEL_REFERENCED_DATA, self).__init__()
        self.add_field('PIXEL_REFERENCE_TYPE', 's', 3, value)
        self.add_field('PIXEL_REFERENCE_COUNT', 'd', 4, value)
        self.add_loop(
            'PIXEL_REFERENCEs', self.PIXEL_REFERENCE_COUNT, PIXEL_REFERENCE, value,
            get_ref_type_length(self.PIXEL_REFERENCE_TYPE))


class UNCERTAINTY(TREElement):
    def __init__(self, value):
        super(UNCERTAINTY, self).__init__()
        self.add_field('UNCERTAINTY_FIRST_TYPE', 's', 11, value)
        self.add_field('UNCERTAINTY_SECOND_TYPE', 's', 11, value)
        self.add_field('UNCERTAINTY_VALUE', 's', 10, value)


class PARAMETER(TREElement):
    def __init__(self, value):
        super(PARAMETER, self).__init__()
        self.add_field('PARAMETER_VALUE', 'b', self.PARAMETER_SIZE, value)


class ADDITIONAL_PARAMETER(TREElement):
    def __init__(self, value):
        super(ADDITIONAL_PARAMETER, self).__init__()
        self.add_field('PARAMETER_NAME', 's', 25, value)
        self.add_field('PARAMETER_SIZE', 'd', 3, value)
        self.add_field('PARAMETER_COUNT', 'd', 4, value)
        self.add_loop('PARAMETERs', self.PARAMETER_COUNT, PARAMETER, value)


class SENSRBType(TREElement):
    def __init__(self, value):
        super(SENSRBType, self).__init__()

        self.add_field('GENERAL_DATA', 's', 1, value)
        if self.GENERAL_DATA == 'Y':
            self.add_field('SENSOR', 's', 25, value)
            self.add_field('SENSOR_URI', 's', 32, value)
            self.add_field('PLATFORM', 's', 25, value)
            self.add_field('PLATFORM_URI', 's', 32, value)
            self.add_field('OPERATION_DOMAIN', 's', 10, value)
            self.add_field('CONTENT_LEVEL', 'd', 1, value)
            self.add_field('GEODETIC_SYSTEM', 's', 5, value)
            self.add_field('GEODETIC_TYPE', 's', 1, value)
            self.add_field('ELEVATION_DATUM', 's', 3, value)
            self.add_field('LENGTH_UNIT', 's', 2, value)
            self.add_field('ANGULAR_UNIT', 's', 3, value)
            self.add_field('START_DATE', 'd', 8, value)
            self.add_field('START_TIME', 'd', 14, value)
            self.add_field('END_DATE', 'd', 8, value)
            self.add_field('END_TIME', 'd', 14, value)
            self.add_field('GENERATION_COUNT', 'd', 2, value)
            self.add_field('GENERATION_DATE', 'd', 8, value)
            self.add_field('GENERATION_TIME', 'd', 10, value)

        self.add_field('SENSOR_ARRAY_DATA', 's', 1, value)
        if self.SENSOR_ARRAY_DATA == 'Y':
            self.add_field('DETECTION', 's', 20, value)
            self.add_field('ROW_DETECTORS', 'd', 8, value)
            self.add_field('COLUMN_DETECTORS', 'd', 8, value)
            self.add_field('ROW_METRIC', 'd', 8, value)
            self.add_field('COLUMN_METRIC', 'd', 8, value)
            self.add_field('FOCAL_LENGTH', 'd', 8, value)
            self.add_field('ROW_FOV', 'd', 8, value)
            self.add_field('COLUMN_FOV', 'd', 8, value)
            self.add_field('CALIBRATED', 's', 1, value)

        self.add_field('SENSOR_CALIBRATION_DATA', 's', 1, value)
        if self.SENSOR_CALIBRATION_DATA == 'Y':
            self.add_field('CALIBRATION_UNIT', 's', 2, value)
            self.add_field('PRINCIPAL_POINT_OFFSET_X', 'd', 9, value)
            self.add_field('PRINCIPAL_POINT_OFFSET_Y', 'd', 9, value)
            self.add_field('RADIAL_DISTORT_1', 's', 12, value)
            self.add_field('RADIAL_DISTORT_2', 's', 12, value)
            self.add_field('RADIAL_DISTORT_3', 's', 12, value)
            self.add_field('RADIAL_DISTORT_LIMIT', 'd', 9, value)
            self.add_field('DECENT_DISTORT_1', 's', 12, value)
            self.add_field('DECENT_DISTORT_2', 's', 12, value)
            self.add_field('AFFINITY_DISTORT_1', 's', 12, value)
            self.add_field('AFFINITY_DISTORT_2', 's', 12, value)
            self.add_field('CALIBRATION_DATE', 'd', 8, value)

        self.add_field('IMAGE_FORMATION_DATA', 's', 1, value)
        if self.IMAGE_FORMATION_DATA == 'Y':
            self.add_field('METHOD', 's', 15, value)
            self.add_field('MODE', 's', 3, value)
            self.add_field('ROW_COUNT', 'd', 8, value)
            self.add_field('COLUMN_COUNT', 'd', 8, value)
            self.add_field('ROW_SET', 'd', 8, value)
            self.add_field('COLUMN_SET', 'd', 8, value)
            self.add_field('ROW_RATE', 'd', 10, value)
            self.add_field('COLUMN_RATE', 'd', 10, value)
            self.add_field('FIRST_PIXEL_ROW', 'd', 8, value)
            self.add_field('FIRST_PIXEL_COLUMN', 'd', 8, value)
            self.add_field('TRANSFORM_PARAMS', 'd', 1, value)
            if self.TRANSFORM_PARAMS >= 1:
                self.add_field('TRANSFORM_PARAM_1', 's', 12, value)
            if self.TRANSFORM_PARAMS >= 2:
                self.add_field('TRANSFORM_PARAM_2', 's', 12, value)
            if self.TRANSFORM_PARAMS >= 3:
                self.add_field('TRANSFORM_PARAM_3', 's', 12, value)
            if self.TRANSFORM_PARAMS >= 4:
                self.add_field('TRANSFORM_PARAM_4', 's', 12, value)
            if self.TRANSFORM_PARAMS >= 5:
                self.add_field('TRANSFORM_PARAM_5', 's', 12, value)
            if self.TRANSFORM_PARAMS >= 6:
                self.add_field('TRANSFORM_PARAM_6', 's', 12, value)
            if self.TRANSFORM_PARAMS >= 7:
                self.add_field('TRANSFORM_PARAM_7', 's', 12, value)
            if self.TRANSFORM_PARAMS >= 8:
                self.add_field('TRANSFORM_PARAM_8', 's', 12, value)
        self.add_field('REFERENCE_TIME', 'd', 12, value)
        self.add_field('REFERENCE_ROW', 'd', 8, value)
        self.add_field('REFERENCE_COLUMN', 'd', 8, value)
        self.add_field('LATITUDE_OR_X', 'd', 11, value)
        self.add_field('LONGITUDE_OR_Y', 'd', 12, value)
        self.add_field('ALTITUDE_OR_Z', 'd', 11, value)
        self.add_field('SENSOR_X_OFFSET', 'd', 8, value)
        self.add_field('SENSOR_Y_OFFSET', 'd', 8, value)
        self.add_field('SENSOR_Z_OFFSET', 'd', 8, value)

        self.add_field('ATTITUDE_EULER_ANGLES', 's', 1, value)
        if self.ATTITUDE_EULER_ANGLES == 'Y':
            self.add_field('SENSOR_ANGLE_MODEL', 'd', 1, value)
            self.add_field('SENSOR_ANGLE_1', 'd', 10, value)
            self.add_field('SENSOR_ANGLE_2', 'd', 9, value)
            self.add_field('SENSOR_ANGLE_3', 'd', 10, value)
            self.add_field('PLATFORM_RELATIVE', 's', 1, value)
            self.add_field('PLATFORM_HEADING', 'd', 9, value)
            self.add_field('PLATFORM_PITCH', 'd', 9, value)
            self.add_field('PLATFORM_ROLL', 'd', 10, value)

        self.add_field('ATTITUDE_UNIT_VECTORS', 's', 1, value)
        if self.ATTITUDE_UNIT_VECTORS == 'Y':
            self.add_field('ICX_NORTH_OR_X', 'd', 10, value)
            self.add_field('ICX_EAST_OR_Y', 'd', 10, value)
            self.add_field('ICX_DOWN_OR_Z', 'd', 10, value)
            self.add_field('ICY_NORTH_OR_X', 'd', 10, value)
            self.add_field('ICY_EAST_OR_Y', 'd', 10, value)
            self.add_field('ICY_DOWN_OR_Z', 'd', 10, value)
            self.add_field('ICZ_NORTH_OR_X', 'd', 10, value)
            self.add_field('ICZ_EAST_OR_Y', 'd', 10, value)
            self.add_field('ICZ_DOWN_OR_Z', 'd', 10, value)

        self.add_field('ATTITUDE_QUATERNION', 's', 1, value)
        if self.ATTITUDE_QUATERNION == 'Y':
            self.add_field('ATTITUDE_Q1', 'd', 10, value)
            self.add_field('ATTITUDE_Q2', 'd', 10, value)
            self.add_field('ATTITUDE_Q3', 'd', 10, value)
            self.add_field('ATTITUDE_Q4', 'd', 10, value)

        self.add_field('SENSOR_VELOCITY_DATA', 's', 1, value)
        if self.SENSOR_VELOCITY_DATA == 'Y':
            self.add_field('VELOCITY_NORTH_OR_X', 'd', 9, value)
            self.add_field('VELOCITY_EAST_OR_Y', 'd', 9, value)
            self.add_field('VELOCITY_DOWN_OR_Z', 'd', 9, value)

        self.add_field('POINT_SET_DATA', 'd', 2, value)
        self.add_loop('POINT_SETs', self.POINT_SET_DATA, POINT_SET, value)

        self.add_field('TIME_STAMPED_DATA_SETS', 'd', 2, value)
        self.add_loop('TIME_STAMPED_DATAs', self.TIME_STAMPED_DATA_SETS, TIME_STAMPED_DATA, value)

        self.add_field('PIXEL_REFERENCED_DATA_SETS', 'd', 2, value)
        self.add_loop('PIXEL_REFERENCED_DATAs', self.PIXEL_REFERENCED_DATA_SETS, PIXEL_REFERENCED_DATA, value)

        self.add_field('UNCERTAINTY_DATA', 'd', 3, value)
        self.add_loop('UNCERTAINTYs', self.UNCERTAINTY_DATA, UNCERTAINTY, value)

        self.add_field('ADDITIONAL_PARAMETER_DATA', 'd', 3, value)
        self.add_loop('ADDITIONAL_PARAMETERs', self.ADDITIONAL_PARAMETER_DATA, ADDITIONAL_PARAMETER, value)


class SENSRB(TREExtension):
    _tag_value = 'SENSRB'
    _data_type = SENSRBType
