var getStatus = function() {
	var URL = "http://localhost/cgi-bin/crawler/status.py";
	var requestsPerMin = 60;
	var statusTypes = ["crawled", "tocrawl", "keywords", "images", "dbsize", "threads"];
	var request;

	this.start = function() {
		request = setInterval(function() {
			$.ajax({
				url: URL,
				dataType: 'JSON',
				method: "GET",
				data: {process: 'STATUS'},
				success: function(data) {
					if(data.success) {
						updateStatus(data.message);
					}
				},

				failed: function(err) {

				}
			});
		}, 60*1000 / requestsPerMin);
	}

	this.stop = function() {
		clearInterval(request);
	}

	function updateStatus(obj) {
		obj = JSON.parse(obj);
		$("#crawled").html("" + obj.crawled);
		$("#tocrawl").html("" + obj.tocrawl);
		$("#keywords").html("" + obj.keywords);
		$("#images").html("" + obj.images);

		if(typeof obj.threads != "undefined")
			chart.addPoint(parseInt(obj.threads));
		else
			chart.addPoint(0);

		if(obj.logs.count > 0) {
			for(var i = 0; i < obj.logs.count; i++)
				console.log(obj.logs.logs[i].type, obj.logs.logs[i].message);
		}
	}
}