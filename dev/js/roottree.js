/* Requires JQuery */

/* based off of http://codewiz.biz/article/post/Creating+your+own+JavaScript+Library#.VBSq6WRdWRg */

window.RootTree = (function() {
    function RootTree(properties) {
	console.log('roottree constructor');
	var watchers = {};
	// to do read cookie and set user
	this._client = 'b4177d68cbd64e44b6b81765727dc6d5'
	var url = 'http://localhost:8001/api/sessions/';

	var registerWatcher = function(session_id, settings) {
	    watchers[session_id] = jQuery.extend(true, {}, settings);
	    watchers[session_id].timer = window.setInterval(
		function(session_id, settings) {
		    return function() {
			// poll the server
			var getData = {
			    client: this._client,
			    developer: this._developer
			};
			jQuery.ajax({
			    type: 'GET',
			    url: url,
			    data: getData,
			    success: function(data) {
				console.log('received confirmation that command ran');
				setttings.success(data);
			    },
			    error: function(jqXHR, textStatus, errorThrown) {
				console.error('client reported an error',
					     jqXHR, textStatus, errorThrown);
				settings.error(errorThrown);
			    },
			    complete: function(jqXHR, status) {
				clearWatcher(session_id);
			    },
			    dataType: 'json',
			    crossDomain: true
			});
		    }
		}(session_id, settings), 100);
	};

	var clearWatcher = function(session_id) {
	    window.clearInterval(watchers[session_id].timer);
	    delete watchers[session_id];
	};

	this.init = function(dev_key){
	    this._developer = dev_key;
	    // for now developer uuid and dev key are the same.
	};

	this.run = function(command, settings){
	    var postData = {
		command: command,
		args: settings.args,
		kwargs: settings.kwargs,
		client: this._client,
		developer: this._developer
	    };
	    jQuery.ajax({
		type: 'POST',
		url: url,
		data: postData,
		dataType: 'json',
		crossDomain: true,
		beforeSend: function (xhr){
		    xhr.setRequestHeader('X-CSRFToken', 'xbdBtMOyAzeEDC3H2xdW7lTwvkIEiA4I');
		},
		success: function(data){
		    console.log('successfully gave the server the command', data);
		    // register this command and wait for it
		},
		error: function(jqXHR, textStatus, errorThrown) {
		    console.error('error giving command to server',
				  jqXHR, textStatus, errorThrown);
		    settings.error(errorThrown);
		},
	    });
	};
    };
    return new RootTree();
}());
