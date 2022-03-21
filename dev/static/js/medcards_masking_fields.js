$(document).ready(function(jQuery) {
    jQuery(function ($) {
        $('#id_number').mask("8 (999) 999-99-99");
        $('#id_year').mask('99.99.9999', {placeholder: 'дд.мм.гггг'});
        let sign = $('input#id_sign');
        let department = $('div[class="form-row field-department"]');
        department.hide()
        if (sign.prop('checked')) {
            department.show();
        }

        sign.on('change', function() {
            if (sign.prop('checked')) {
                department.show();
            } else {
                department.hide();
            }
        })


        // id_sign
    });
});