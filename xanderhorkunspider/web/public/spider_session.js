$("#start-button").on("click", function (e) {
    var $button = $(e.target);
    var maxP = new Number($("#spider-options #max_processes :input").val());
    var websiteId = $button.attr("website-id");
    if (maxP < 0) {
        maxP = 5;
    }
    $.ajax("/spider_session", {
        data: {
            max_processes: maxP,
            website: websiteId
        },
        type: "GET"
    });
});