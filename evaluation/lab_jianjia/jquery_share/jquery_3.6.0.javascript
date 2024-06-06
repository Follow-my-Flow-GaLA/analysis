(function(){
var s = {
	url: "http://google.com"
}, options = {
	'content-type':'text/plain'
}, preservedScriptAttributes = [
	'url', 'src'
], key, script = document.createElement( "script" ); 
for (key in options) { s[key] = options[key] };

if (s.crossDomain === null) return;

var callback_flag = false; // Used to switch between callback and non-callback when testing the static tool

if (!callback_flag) {
	// non-callback version
	s.src = s.url; 
	preservedScriptAttributes.forEach(function(i){
		script.setAttribute(i, s[i]);
	})
	if (s.dataType === 'script') {
		document.head.appendChild( script ).parentNode.removeChild( script );}	
} else {
	// callback version
	var xhr = new window.XMLHttpRequest();
	xhr.open('GET', s.url, true); 
	xhr.onload = function() {
		// No error handling for simplicity
		script.text = xhr.responseText;
		if (s.dataType === 'script') {
			document.head.appendChild( script ).parentNode.removeChild( script );}
	}
	xhr.send();
}
})();
