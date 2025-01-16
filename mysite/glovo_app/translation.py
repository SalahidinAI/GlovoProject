from .models import *
from modeltranslation.translator import TranslationOptions,register


@register(Store)
class StoreTranslationOptions(TranslationOptions):
    fields = ('store_name', 'description')


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)


@register(StoreAddress)
class StoreAddressTranslationOptions(TranslationOptions):
    fields = ('address',)


@register(Combo)
class ComboTranslationOptions(TranslationOptions):
    fields = ('combo_name', 'description')


@register(ComboProduct)
class ComboTranslationOptions(TranslationOptions):
    fields = ('product_name',)


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('product_name', 'description')