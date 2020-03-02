(function() {
  function displaySearchResults(results, store) {
    var searchResults = document.getElementById('search-results');

    if (results.length) { // Are there any results?
      var appendString = '';

      for (var i = 0; i < results.length; i++) {  // Iterate over the results
        var item = store[results[i].ref];
        if (item.image) {
          appendString += `
          <p>
            <a href="${results[i].ref}"><div>
            <img src="/assets/img/${item.image}" width="400px" height="350px" class="centered-and-cropped grayscale"/>
            <p><span class="post-preview-title-italic">${item.title}</span>, <span class="post-preview-author"> ${item.author} </span></p>
            </div></a> 
          </p>
          <hr>
          `;
        } else {
          var url = "../titles/" + item.title_id
          if (item.fragment) {
            url = url + "#" + item.fragment
          }
          appendString += `
            <p>
              <a href="${url}"><div>
              <p>${item.excerpt}</p>
              <p><span class="post-preview-title-italic">${item.title}</span>, <span class="post-preview-author"> ${item.author} </span></p>
              </div></a> 
            </p>
            <hr>
            `;
        }
      }

      searchResults.innerHTML = appendString;
    } else {
      searchResults.innerHTML = 'No se han encontrado resultados.';
    }
  }

  function getQueryVariable(variable) {
    var query = window.location.search.substring(1);
    var vars = query.split('&');

    for (var i = 0; i < vars.length; i++) {
      var pair = vars[i].split('=');

      if (pair[0] === variable) {
        return decodeURIComponent(pair[1].replace(/\+/g, '%20'));
      }
    }
  }

  var searchTerm = getQueryVariable('query');

  if (searchTerm) {
    document.getElementById('search-box').setAttribute("value", searchTerm);

    var idx = lunr(function () {
      this.ref('url');
      this.field('title');
      this.field('author');

    	for (var key in window.store) {
	      this.add({
	        'url': key,
	        'title': window.store[key].title,
	        'author': window.store[key].author
	      });
	    }
    });

	var results = idx.search(searchTerm).slice(0, 20);
    displaySearchResults(results, window.store);
  }
})();