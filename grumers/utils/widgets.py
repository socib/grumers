# coding: utf-8
from django.utils.translation import ugettext_lazy as _
from bootstrap3_datetime.widgets import DateTimePicker


class BeachDateTimePicker(DateTimePicker):

    MOMENT_CHOICES = (
        ('10:00', _('Beach opening')),
        ('14:00', _('Midday - 14h')),
        ('18:00', _('Beach closing')),
    )

    class Media:
        jsfiles = DateTimePicker.Media.js
        js = [jsfile for jsfile in jsfiles]
        js.extend(['js/jellyfish_beach_datetimepicker.js'])

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
