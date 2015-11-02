$(document).ready(function(){
    refreshInterviews()

    window.setInterval(function(){
        refreshInterviews()
    }, 5000);
});

window.slotId = false;

function addOnClick(){
    $(".choose-interview").click(function(){
        window.slotId = $(this).data('slotid')
    });
}

function drawTable(data){
    $("#interview-slots-table > tbody").empty();
    var source = $("#interview-slots-template").html();
    var template = Handlebars.compile(source);
    data.forEach(function(slot){
        var html = template(slot);
        $("#interview-slots-table > tbody").append(html);
    });
}

function refreshInterviews(){
    $.ajax({
        url: "/api/get-interview-slots/",
        type: 'GET',
        success: function(res) {
            drawTable(res)
            addOnClick()
        }
    });
}
