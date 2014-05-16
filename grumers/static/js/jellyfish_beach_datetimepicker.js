function addMomentChoices(inputId) {
    var dateInput = $(inputId);
    var container = dateInput.parent().parent();
    var select = $('<select class="form-control"></select>');
    select.append('<option value="">' + beach_datetimepicker_lang['select_moment'] + '</option>');
    select.append('<option value="10:00">' + beach_datetimepicker_lang['opening'] + '</option>');
    select.append('<option value="14:00">' + beach_datetimepicker_lang['midday'] + '</option>');
    select.append('<option value="18:00">' + beach_datetimepicker_lang['closing'] + '</option>');
    var div = $('<div class="col-sm-3"></div>');
    div.append(select);
    container.append(div);
    var dtp = dateInput.data('DateTimePicker');
    select.change(function() {
        if (this.value && this.value.length > 0) {
            var currentDate = dtp.getDate().toDate();
            currentDate.setHours(this.value.split(':')[0]);
            currentDate.setMinutes(this.value.split(':')[1]);
            var newDate = moment(currentDate).format(dtp.format);
            dtp.setDate(newDate);
        }
        if (this.value == "18:00"){
            $('fieldset.incidents').show();
        }else{
            $('fieldset.incidents').hide();
        }
    });
    // Initial value for select
    var currentDate = dtp.getDate().toDate();
    select.val(moment(currentDate).format("HH:mm"));
    select.trigger('change');
}