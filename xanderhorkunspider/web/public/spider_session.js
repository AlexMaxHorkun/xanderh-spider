$("#start-button").on("click", function (e) {
    var $button = $(e.target);
    var maxP = new Number($("#spider-options #max_processes :input").val());
    var websiteId = $("#spider-session").attr("website-id");
    if (maxP < 0) {
        maxP = 5;
    }
    $.get("/spider_session", {max_processes: maxP, website: websiteId}, function (data) {
        $("#spider-info").append(data);
    });
});
var spiderId = parseInt($("#spider-info").attr("spider-id"));
if (spiderId) {
    $.get("/spider_session", {spider_id: spiderId, website: $("#spider-session").attr("website-id")}, function (data) {
        $("#spider-info").append(data);
    });
}