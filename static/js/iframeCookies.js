var pathParams = window.location.pathname.split('/')
var searchParams = window.location.search
if (searchParams) {
	searchParams = searchParams.slice(1,searchParams.length).split('&')
	searchParams.forEach(function(searchParam) {
		var key = searchParam.split('=')[0]
		var value = searchParam.split('=')[1]
		if (key.indexOf('uuid') > -1) {
			console.log('value', value)
			if (window.parent) {
				window.parent.postMessage({uuid:value}, '*');	
			}
		}
		})
}

	


