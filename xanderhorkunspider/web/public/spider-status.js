function Loading(id, url, started, finished) {
    this.url = url;
    this.started = started;
    this.finished = finished;
    this.id = id;
}


function SpiderStatus(url, renderer) {
    this.receiveStatusUrl = url;
    this.loadings = [];
    this.isRunning = false;
    this.renderer = renderer;
    this.isUpdating = false;
    this.websitePagesCount = 0;
    this.websiteId = 0;
    this.spiderId = 0;
    this.stopWhenDone = false;
}

SpiderStatus.prototype.findLoadingById = function (id) {
    for (var i = 0; i < this.loadings.length; i++) {
        if (this.loadings[i].id == id) {
            return this.loadings[i];
        }
    }
};

SpiderStatus.prototype.update = function () {
    if (this.isUpdating) return;
    this.isUpdating = true;
    var self = this;
    var data = {stop_when_done: +this.stopWhenDone};
    if (this.spiderId) {
        data.spider_id = this.spiderId;
    }
    if (this.websiteId) {
        data.website_id = this.websiteId;
    }
    $.get(this.receiveStatusUrl, data, function (data) {
        self.isRunning = data.is_alive;
        self.loadings = [];
        if (data.pages_count) {
            self.websitePagesCount = data.pages_count;
        }
        for (var i = 0; i < data.loadings.length; i++) {
            var loadingData = data.loadings[i];
            var started;
            if (loadingData.started) {
                var startedData = loadingData.started.split(',');
                started = new Date(startedData[0], startedData[1], startedData[2], startedData[3], startedData[4], startedData[5], startedData[6], 0);
            }
            var finished;
            if (loadingData.finished) {
                var finishedData = loadingData.finished.split(',');
                finished = new Date(startedData[0], startedData[1], startedData[2], startedData[3], startedData[4], startedData[5], startedData[6], 0);
            }
            var loading;
            if (loading = self.findLoadingById(loadingData.id)) {
                loading.started = started;
                loading.finished = finished;
            }
            else {
                loading = new Loading(loadingData.id, loadingData.url, started, finished);
                self.loadings.push(loading);
            }
        }
        self.loadings.sort(function (a, b) {
            if (a.started == b.started) {
                return 0;
            }
            return (a.started < b.started) ? 1 : -1;
        });
        self.renderer.render(self.loadings, self.isRunning, self.websitePagesCount);
        setTimeout(function () {
            self.isUpdating = false;
        }, 500);
    });
};


function SpiderStatusRenderer() {
    this.maxLoadingNameLength = 40;
    this.maxItemsShow = 100;
}
SpiderStatusRenderer.prototype.render = function (loadings, isAlive, pagesCount) {
    if (isAlive) {
        $("#spider-status #spider-stance #running").show();
        $("#spider-status #spider-stance #stopped").hide();
    }
    else {
        $("#spider-status #spider-stance #running").hide();
        $("#spider-status #spider-stance #stopped").show();
    }
    console.log("pages count = "+pagesCount);
    if (pagesCount) {
        $("#spider-session #website-pages-count").text(pagesCount);
    }
    $("#spider-status #running-count").text(loadings.length);
    $("#spider-status #loadings").html("");
    var fetchStatus = function (started, finished) {
        var statusText;
        if (started && !finished) {
            statusText = "Running";
        }
        if (!started) {
            statusText = "Waiting";
        }
        if (started && finished) {
            statusText = "Finished";
        }
        return statusText;
    };
    var $loadings = $("#spider-status #loadings");
    $loadings.html("");
    for (var i = 0; i < loadings.length; i++) {
        var loading = loadings[i];
        var loadingName = "";
        if (loading.url.length > this.maxLoadingNameLength) {
            loadingName = loading.url.substr(0, this.maxLoadingNameLength) + "...";
        }
        else {
            loadingName = loading.url;
        }
        $loadings.append('<li page-id="' + loading.id + '" finished="' + (+!!loading.finished) + '">' + loadingName
        + ' <span id="text-status">' + fetchStatus(loading.started, loading.finished) + '</span></li>');
    }
};