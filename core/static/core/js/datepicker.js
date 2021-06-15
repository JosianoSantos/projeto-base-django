$(document).ready(function () {
    // Confguração global
    $.fn.datepicker.defaults.format = 'dd/mm/yyyy';
    $.fn.datepicker.defaults.useCurrent = true;
    $.fn.datepicker.defaults.todayHighlight = true;
    $.fn.datepicker.defaults.autoclose = true;
    $.fn.datepicker.defaults.language = 'pt-BR';
    $.fn.datepicker.defaults.clearBtn = true;
    $.fn.datepicker.defaults.forceParse = true;

    aplicarDatepicker();
});

function aplicarDatepicker() {

    let datepicker = $('.datepicker');

    datepicker.datepicker('destroy');

    datepicker.datepicker();

    // Remove o autocomplete dos campos, para evitar o surgimento das datas já usadas
    // em outros formulários, que o browser sugere.
    datepicker.on('focus', function (e) {
        e.preventDefault();
        $(this).attr("autocomplete", "off");
    });
}

function aplicarDatepickerFormset() {

    setTimeout(function () {
        let datepicker = $('.datepicker-formset');

        datepicker.datepicker('destroy');

        datepicker.datepicker();

        // Remove o autocomplete dos campos, para evitar o surgimento das datas já usadas
        // em outros formulários, que o browser sugere.
        datepicker.on('focus', function (e) {
            e.preventDefault();
            $(this).attr("autocomplete", "off");
        });
    },200);

}