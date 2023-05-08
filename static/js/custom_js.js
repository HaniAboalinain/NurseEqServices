$(document).ready(function(){
  $("#id_eq_count, #id_eq_name").change(function(){
    let selectedValue = $("#id_eq_name option:selected").text().slice(-4);
    let eq_count = $("#id_eq_count").val();
    let price = eq_count * selectedValue;
    $("#id_price").val(price);
  });
});
