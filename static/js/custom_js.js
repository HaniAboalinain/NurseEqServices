$(document).ready(function () {
    $("#id_eq_count, #id_eq_name, #id_duration_from, #id_duration_to").change(function () {
        // let from = new Date($('#id_duration_from').val());
        // let day = from.getDate();
        // let month = from.getMonth();
        // let year = from.getFullYear();
        // alert([day, month, year].join('/'));
        let from = new Date($('#id_duration_from').val());
        let to = new Date($('#id_duration_to').val());
        if (from >= to) {
            alert("The 'duration to' field should be after the 'duration from', Please Make sure to enter a valid value.");
            $('#id_duration_to').val('');
            to = '';
        }
        if (to === '') {
            $('#id_price').val('');
        }
        let timeDiff = Math.abs(to.getTime() - from.getTime());
        let diffDays = Math.ceil(timeDiff / (1000 * 3600 * 24));
        let selectedValue = $("#id_eq_name option:selected").text().slice(-12, -7);
        let eq_count = $("#id_eq_count").val();
        let price = eq_count * selectedValue * diffDays;
        $("#id_price").val(price);
    });
});
