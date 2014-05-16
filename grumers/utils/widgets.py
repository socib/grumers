# coding: utf-8
from django.utils.translation import ugettext_lazy as _
from django.utils import translation
from bootstrap3_datetime.widgets import DateTimePicker


class BeachDateTimePicker(DateTimePicker):

    MOMENT_CHOICES = (
        ('10:00', _('Beach opening')),
        ('14:00', _('Midday - 14h')),
        ('18:00', _('Beach closing')),
    )

    class Media:
        class JsFiles(object):
            def __iter__(self):
                jsfiles = DateTimePicker.Media.js
                for jsfile in jsfiles:
                    yield jsfile

                lang = translation.get_language()
                if lang:
                    lang = lang.lower()
                    if len(lang) > 2:
                        lang = lang[:2]
                    if lang not in ['en', 'ca', 'es']:
                        lang = 'en'
                    yield 'js/locales/jellyfish_beach_datetimepicker.%s.js' % (lang)
                yield 'js/jellyfish_beach_datetimepicker.js'

        js = JsFiles()

    js_template = '''
        <script>
            $(function() {
                $("#%(picker_id)s").datetimepicker(%(options)s);
                addMomentChoices("#%(picker_id)s");
            });
        </script>'''

    def __init__(self, attrs=None, format=None,
                 options=None, div_attrs=None, icon_attrs=None):
        super(BeachDateTimePicker, self).__init__(attrs, format,
                                                  options, div_attrs, icon_attrs)
