from modeltranslation.translator import translator, TranslationOptions
from users.models import Region, City


# For Region
class RegionTranslationOptions(TranslationOptions):
    fields = ("name",)


translator.register(Region, RegionTranslationOptions)


# For City
class CityTranslationOptions(TranslationOptions):
    fields = ("name",)


translator.register(City, CityTranslationOptions)
