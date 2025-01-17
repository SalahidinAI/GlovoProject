from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationInlineModelAdmin
from .models import *


class StoreContactInline(admin.TabularInline):
    model = StoreContact
    extra = 1


class StoreWebsiteInline(admin.TabularInline):
    model = StoreWebsite
    extra = 1


class StoreAddressInline(admin.TabularInline, TranslationInlineModelAdmin):
    model = StoreAddress
    extra = 1


class GeneralMedia:
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Store)
class StoreAdmin(TranslationAdmin, GeneralMedia):
    inlines = [StoreContactInline, StoreWebsiteInline, StoreAddressInline]


@admin.register(Combo)
class ComboAdmin(TranslationAdmin, GeneralMedia):
    pass


@admin.register(Product)
class ProductAdmin(TranslationAdmin, GeneralMedia):
    pass


class CartProductInline(admin.TabularInline):
    model = CartProduct
    extra = 1


class CartComboInline(admin.TabularInline):
    model = CartCombo
    extra = 1


class CartAdmin(admin.ModelAdmin):
    inlines = [CartProductInline, CartComboInline]


@admin.register(Category)
class CategoryAdmin(TranslationAdmin, GeneralMedia):
    pass


admin.site.register(User)
# admin.site.register(Category, CategoryAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order)
admin.site.register(Courier)
admin.site.register(StoreReview)
admin.site.register(CourierRating)