$(document).ready(function () {
    $('.table').not('.datatable-disabled').DataTable({
        colReorder: true,
        searching: false,
        lengthChange: false,
        aaSorting: [],
        pageLength: 50,
        language: {
            url: '//cdn.datatables.net/plug-ins/1.10.19/i18n/Portuguese-Brasil.json'
        }
    });
});