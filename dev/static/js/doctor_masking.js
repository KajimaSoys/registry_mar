$(document).ready(function(jQuery) {
    jQuery(function ($) {
        $('#id_phone').mask("8 (999) 999-99-99");
        $('#id_born').mask('9999', {placeholder: 'гггг'})
    });
});