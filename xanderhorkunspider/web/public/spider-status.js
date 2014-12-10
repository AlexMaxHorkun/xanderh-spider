function Loading(id, url, started, finished) {
    this.url = url;
    this.started = started;
    this.finished = finished;
    this.id = id;
}


function SpiderStatus(url, renderer, spiderId) {
    this.receiveStatusUrl = url;
    this.loadings = [];
    this.isRunnig = false;
    this.renderer = renderer;
    this.isUpdating = false;
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
    $.get(this.receiveStatusUrl, {}, function (data) {
        self.isRunnig = data.is_alive;
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
        self.renderer.render(self.loadings, self.isRunnig);
        setTimeout(function () {
            self.isUpdating = false;
        }, 250);
    });
};


function SpiderStatusRenderer() {
    this.maxLoadingNameLength = 40;
    this.maxItemsShow = 100;
}
SpiderStatusRenderer.prototype.render = function (loadings, isAlive) {
    if (isAlive) {
        $("#spider-status #spider-stance #running").show();
        $("#spider-status #spider-stance #stopped").hide();
    }
    else {
        $("#spider-status #spider-stance #running").hide();
        $("#spider-status #spider-stance #stopped").show();
    }
    $("#spider-status #loadings li[finished='true'], #spider-status #loadings li[finished='1']").remove();
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
    for (var i = 0; i < loadings.length; i++) {
        var loading = loadings[i];
        var $item = $loadings.find("li[page-id='" + loading.id + "']").get(0);
        if ($item) {
            $item = $($item);
            $item.find("#text-status").text(fetchStatus(loading.started, loading.finished));
        }
        else {
            var loadingName = "";
            if (loading.url.length > this.maxLoadingNameLength) {
                loadingName = loading.url.substr(0, this.maxLoadingNameLength) + "...";
            }
            else {
                loadingName = loading.url;
            }
            $loadings.append('<li page-id="' + loading.id + '">' + loadingName
                             + ' <span id="text-status">' + fetchStatus(loading.started, loading.finished) + '</span></li>');
        }
    }
};