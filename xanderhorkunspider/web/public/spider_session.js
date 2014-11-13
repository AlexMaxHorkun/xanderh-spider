$("#start-button").on("click", function (e) {
    var maxP = new Number($("#spider-options #max_processes :input").val());
    if (maxP < 0) {
        maxP = 5;
    }
    $.ajax("/spider_session", {
        max_processes: maxP,
        type: "GET"
    });
});