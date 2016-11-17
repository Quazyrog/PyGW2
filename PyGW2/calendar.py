"""
Why do we hate Asuras:

  ,,Friends and fellows. Due to recent (amazing!) reasoning by scholars of the Astronomagical Society, we are
  pleased to announce that we have added the five hidden days to our calendar year! That's five extra days we've
  recognized for you to advance your work before the annual review. Gifts and gratitude are unnecessary. We
  merely acknowledged them officially; we did not create them. May all your projects be almost as successful as
  ours.''

No comment. This library treats all years as if they had 365 days.
"""
import datetime
import enum
import math



@enum.unique
class MauvelianSeason(enum.Enum):
    ZEPHYR = 0
    PHOENIX = 1
    SCION = 2
    COLOSSUS = 3

    def __str__(self):
        if self is MauvelianSeason.ZEPHYR:
            return "Season of Zephyr"
        if self is MauvelianSeason.PHOENIX:
            return "Season of Phoenix"
        if self is MauvelianSeason.SCION:
            return "Season of Scion"
        if self is MauvelianSeason.COLOSSUS:
            return "Season of Colossus"

    @property
    def daysRange(self):
        """
        Return range object with numbers of days in this season.
        """
        if self is MauvelianSeason.ZEPHYR:
            return range(1, 91)
        if self is MauvelianSeason.PHOENIX:
            return range(91, 181)
        if self is MauvelianSeason.SCION:
            return range(181, 271)
        if self is MauvelianSeason.COLOSSUS:
            return range(271, 366)

    @staticmethod
    def seasonOf(day_of_year):
        if not 1 <= day_of_year <= 365:
            raise ValueError("day not in [1; 365] range")
        if day_of_year <= 180:
            if day_of_year <= 90:
                return MauvelianSeason.ZEPHYR
            return MauvelianSeason.PHOENIX
        else:
            if day_of_year <= 270:
                return MauvelianSeason.SCION
            return MauvelianSeason.COLOSSUS


class MauvelianDate:
    """
    A date in Mauvelian Calendar (years all have 365 days, like in GW2).
    """

    def __init__(self, year, day, season=None):
        """
        Initialize with given date in Mauvelian Callendar.

        The year argument should be positive for AE years and negative for BE (year=0 is invalid). If no season is
        given, then day should be in range [1; 365]. If season is given (as MauvelianSeason enum object), then day is
        assumed to be a day of this season. For example (year=1, day=95) is same as
        (year=1, day=5, season=MauvelianSeason.PHOENIX).
        """
        #Year cannot be 0
        if year == 0:
            raise ValueError("year cannot be 0")

        #If season given: shift day value
        if season is not None:
            if not 1 <= day <= len(season.daysRange):
                raise ValueError("Day is not valid for this season")
            day += season.daysRange.start - 1

        #Check day and save data
        if not 1 <= day <= 365:
            raise ValueError("day not in [1; 365] range")
        if year > 0:
            self._day = day + 365 * (year - 1)
        else:
            self._day = -day - 365 * (year + 1)

    @property
    def year(self):
        """
        Return year from date (negative for years before exodus).
        """
        if self._day > 0:
            return math.ceil(self._day / 365)
        return math.floor(self._day / 365)

    @property
    def dayOfYear(self):
        """
        Return day of year from date (integer from [1; 365] range).
        """
        d = abs(self._day % 365)
        if d == 0:
            return 365
        return d

    @property
    def dayOfSeason(self):
        """
        Return day of season from date (integer from [1; 90] range or [1; 95] for Colossus).
        """
        return self.dayOfYear - MauvelianSeason.seasonOf(self.dayOfYear).daysRange.start + 1

    @property
    def season(self):
        """
        Return seson from date (object of MauvelianSeason enum-class).
        """
        return MauvelianSeason.seasonOf(self.dayOfYear)

    def __str__(self):
        if self._day > 0:
            return "%i %s, %iAE" % (self.dayOfSeason, str(self.season), self.year)
        return "%i %s, %iBE" % (self.dayOfSeason, str(self.season), -self.year)

    def __lt__(self, other):
        return self._day < other._day

    def __gt__(self, other):
        return self._day > other._day

    def __eq__(self, other):
        return self._day == other._day

    def addDays(self, days):
        """
        Add given number of days to self; return (modified) self.
        """
        self._day += days
        if self._day == 0:
            if days > 0:
                self._day = 1
            else:
                self._day = 1
        return self

    def daysBetween(self, other):
        """
        Reuturn difference in days between this date and the other.
        """
        return abs(self._day - other._day)

    def __add__(self, days):
        return MauvelianDate(self.year, self.dayOfYear).addDays(days)

    def __sub__(self, other):
        if isinstance(other, MauvelianDate):
            return self.daysBetween(other)
        #if not date, then days subtraction
        return self - other


class DateConverter:
    _reference = (None, None)

    def setReferencePoint(self, real_date, mauvelian_date):
        """
        Set reference point and use it to convert between real and Mauvelian date.

        real_date should be datetime.date; mauvelian_date should be MauvelianDate.
        """
        if (not isinstance(real_date, datetime.date) or not isinstance(mauvelian_date, MauvelianDate)) \
           and not (isinstance(real_date, NoneType) and isinstance(mauvelian_date, NoneType)):
            raise TypeError
        self._reference = (real_date, mauvelian_date)

    def realToMauvelian(self, real_date):
        """
        Convert real date to Mauvelian date.

        To do this, you must set (valid) reference point firstly.
        """
        if self._reference[0] is None or self._reference[1] is None:
            raise RuntimeError("Reference point not set")
        delta_days = (real_date - self._reference[0]).days
        return self._reference[1] + delta_days

    def mauvelianToReal(self, mauvelian_date):
        """
        Convert Mauvelian date to real date.

        To do this, you must set (valid) reference point firstly.
        """
        if self._reference[0] is None or self._reference[1] is None:
            raise RuntimeError("Reference point not set")
        delta_days = mauvelian_date - self._reference[1]
        dd = mauvelian_date - self._reference[1]
        return self._reference[0] + datetime.timedelta(days=delta_days)
        

#Test
if __name__ == "__main__":
    #Davros' birth date
    date1 = MauvelianDate(1306, 76, MauvelianSeason.SCION)
    #He was born in 256th day of year
    assert(date1.dayOfYear == 256)
    date2 = MauvelianDate(1318, 128)
    assert(date1 < date2)
    assert(date2.season == MauvelianSeason.PHOENIX)
    assert(date2.daysBetween(date1) == 365 * 11 + 109 + 128)
    assert(date1 + 365 * 11 + 109 + 128 == date2)

    #Test converter
    converter = DateConverter()
    real = datetime.date(2016, 11, 5)
    mauvelian = MauvelianDate(1328, 35, MauvelianSeason.COLOSSUS)
    converter.setReferencePoint(real, mauvelian)
    assert(converter.realToMauvelian(real) == mauvelian)
    assert(converter.mauvelianToReal(mauvelian) == real)
    mauvelian2 = MauvelianDate(1328, 41, MauvelianSeason.COLOSSUS)
    converted_real = converter.mauvelianToReal(mauvelian2)
    assert(converted_real == datetime.date(2016, 11, 11))
