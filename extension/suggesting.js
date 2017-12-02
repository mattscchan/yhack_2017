console.log('Suggesting.js loaded');

var numOfHoverables = 0;

$(document).ready(function() {

  // Get title of article
  var title = $('h1.headline a').html();
  console.log(title);
  highlightAndSuggest(title);
});

var highlightYellow = function(string, index) {
  var replaced = $("body").html().replace(string, '<span style="background-color: yellow;" title="tooltip" class="hoverableSuggestableFakeNews-' + index +'">' + string + '</span>');
  $("body").html(replaced);
};

var highlightAndSuggest = function(string) {

  var index = numOfHoverables + 1;

  highlightYellow(string, index);

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
    $( ".hoverableSuggestableFakeNews-" + index ).tooltip({
      content: generateListOfLinks(data),
      show: null, // show immediately
      open: function(event, ui)
      {
        if (typeof(event.originalEvent) === 'undefined')
        {
          return false;
        }

        var $id = $(ui.tooltip).attr('id');

        // close any lingering tooltips
        $('div.ui-tooltip').not('#' + $id).remove();

        // ajax function to pull in data and add it to the tooltip goes here
      },
      close: function(event, ui)
      {
        ui.tooltip.hover(function()
            {
              $(this).stop(true).fadeTo(400, 1);
            },
            function()
            {
              $(this).fadeOut('400', function()
              {
                $(this).remove();
              });
            });
      }
    });
  });
};

var generateListOfLinks = function(data) {
  var links = "<h3>Relevant articles</h3>";
  data.value.slice(-5).forEach(function(article) {
    links = links + '<li><a href="'+ article.url +'"><b>[' + article.provider[0].name + '</b>] ' + article.name + '</a></li>';
  });
  return links;
};
