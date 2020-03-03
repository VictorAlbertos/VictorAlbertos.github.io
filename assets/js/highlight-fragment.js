(function() {
	var query = window.location.href
	var vars = query.split('#')
	if (vars.length <= 1) {
		return
	}

	let element =  document.getElementById(vars[1]+'-target')
	element.classList.add("highlight-fragment")
})();

function go_to_fragment(fragment) {
    window.location.hash = '#' + fragment;
    window.location.reload(true);
 }