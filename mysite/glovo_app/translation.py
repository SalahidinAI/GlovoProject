from .models import *
from modeltranslation.translator import TranslationOptions,register

@register(Store)
class StoreTranslationOptions(TranslationOptions):
    fields = ('store_name', 'address')


@register(Product)

class ProductTranslationOptions(TranslationOptions):
    fields = ('product_name',)