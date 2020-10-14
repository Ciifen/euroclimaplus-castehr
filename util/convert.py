import math

def rad2deg(radians):
    """
    Convert radians to angular degrees
    """
    return radians * (180.0 / math.pi)

def deg2rad(degrees):
    """
    Convert angular degrees to radians
    """
    return degrees * (math.pi / 180.0)

def celsius2kelvin(celsius):
    """
    Convert temperature in degrees Celsius to degrees Kelvin.
    """
    return celsius + 273.15


def kelvin2celsius(kelvin):
    """
    Convert temperature in degrees Kelvin to degrees Celsius.
    """
    return kelvin - 273.15

