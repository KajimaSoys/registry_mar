$(document).ready(function(jQuery) {
    jQuery(function ($) {
        $('#id_date_start_0').mask('99.99.9999', {placeholder: 'дд.мм.гггг'});
        $('#id_date_start_1').mask('99:99:99', {placeholder: 'чч:мм:сс'});
        $('#id_date_stop_0').mask('99.99.9999', {placeholder: 'дд.мм.гггг'});
        $('#id_date_stop_1').mask('99:99:99', {placeholder: 'чч:мм:сс'});
    });
});