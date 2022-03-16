$(document).ready(function(jQuery) {
    jQuery(function ($) {
        $('#id_date').mask('99.99.2022', {placeholder: 'дд.мм.2022'});
        $('#id_start').mask('99:99:00', {placeholder: 'чч:мм:00'});
        $('#id_end').mask('99:99:00', {placeholder: 'чч:мм:00'});
    });
});