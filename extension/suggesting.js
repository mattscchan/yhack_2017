console.log('Suggesting.js loaded');

$(document).ready(function() {

  // Get title of article
  var title = $('h1.headline a').html();
  console.log(title);

  getSuggestions(title);


});

var getSuggestions = function(string) {

  var parsedQuery = string.split(" ").join("+").replace(/<[^<>]*>/g, "");
  console.log(parsedQuery);

  $.ajax({
    url: "https://api.cognitive.microsoft.com/bing/v7.0/news/search",
    method: "GET",
    headers: {
      "Ocp-Apim-Subscription-Key": "c87d294a9c8e4effb43d6a3d0ef9859b"
    },
    data: {
      "q": parsedQuery,
      "mkt": "en-us"
    }
  }).done(function(data) {
    console.log(data);
  });
};

var isRelevant = function(title, string) {

};