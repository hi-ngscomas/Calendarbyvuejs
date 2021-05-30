$(document).ready(function() { //first read the values of the #altfield
    var dates = $('#altField').val().split(',');
    //second set your multiDatesPicker with the dates of step 1 and an altfield
    $('#with-altField').multiDatesPicker({
        dateFormat: "mm/dd/yy",
        addDates: dates,
        numberOfMonths: [1, 2],
        altField: '#altField',
    });
});

function changeUp(id) {
    var elem = document.getElementById('tablepromotion');
    $.POST("/changeup", {
        id: id
    });
    elem.refresh();
};

function changeDown(id) {
    var elem = document.getElementById('tablepromotion');
    $.POST("/changedown", {
        id: id
    });
    elem.refresh();
};