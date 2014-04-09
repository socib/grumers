# coding: utf-8
from modeltranslation.translator import translator, TranslationOptions
from models import Page


class PageTranslationOptions(TranslationOptions):
    fields = ('title', 'title_menu', 'introduction', 'content',)

translator.register(Page, PageTranslationOptions)
