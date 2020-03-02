(function() {
	var query = window.location.href
	var vars = query.split('#')
	if (vars.length <= 1) {
		return
	}

	let element =  document.getElementById(vars[1]+'-target')
	let allPs = element.getElementsByTagName("p");
	allPs[allPs.length-1].classList.add("remove-margin-bottom")
	element.classList.add("highlight-fragment")
})();