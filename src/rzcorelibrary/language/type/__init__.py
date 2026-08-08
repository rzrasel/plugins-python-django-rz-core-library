from enum import Enum

class EnumLessonType(Enum):
    DAYS_OF_THE_WEEK = ("days_of_the_week", 1)
    MONTHS_OF_THE_YEAR = ("months_of_the_year", 2)
    SIX_SEASON = ("six_season", 3)
    RAINBOW_COLORS_NAME = ("rainbow_colors_name", 4)
    SOLAR_SYSTEM_PLANETS = ("solar_system_planets", 5)
    HUMAN_BODY_PARTS = ("human_body_parts", 6)
    EMPTY = ("empty", -1)

    def __init__(self, slug: str, serial: int):
        self.slug = slug
        self.serial = serial

    @classmethod
    def find_slug(cls, value: str):
        for item in cls:
            if item.slug == value:
                return item
        return None