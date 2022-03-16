$(document).ready(function(jQuery) {
    jQuery(function ($) {
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
        });
    });
});
