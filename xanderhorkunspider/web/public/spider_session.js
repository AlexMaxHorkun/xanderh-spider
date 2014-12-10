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
var spiderId = parseInt($("#spider-info").attr("spider-id"));
if (spiderId) {
    $.get("/spider_session", {max_processes: maxP, website: websiteId, spider_id: spiderId}, function (data) {
        $("#spider-info").append(data);
    });
}