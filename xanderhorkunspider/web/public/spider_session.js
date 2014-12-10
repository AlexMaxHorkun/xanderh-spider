$("#start-button").on("click", function (e) {
    var $button = $(e.target);
    var maxP = new Number($("#spider-options #max_processes :input").val());
    var websiteId = $button.attr("website-id");
    if (maxP < 0) {
        maxP = 5;
    }
    $.get("/spider_session", {max_processes: maxP, website: websiteId}, function (data) {
        $("#spider-info").append(data);
    });
});