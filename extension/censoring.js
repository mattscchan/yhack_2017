$(document).ready(function(){
    console.log("asdasd");
    highlightRed([" introducing special tracks", "Also gluten-free"]);
    console.log(getTitle())
});



function getTitle(){

    var title = $("title").html();
    var reputableArticles = [];
    var reputableURL = [];
    
      var parsedQuery = title.split(" ").join("+").replace(/<[^<>]*>/g, "");
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
        data.value.forEach(function(article) {
            reputableURL.push(article.url);
        });
      });

      reputableURL.forEach(function(){

      });
      var data = {"target":"John Doe",
                  "cluster":""}
      

      $.ajax({
        url: "https://api.cognitive.microsoft.com/bing/v7.0/news/search",
        method: "POST",
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        data : JSON.stringify(data),
      }).done(function(data) {
        
      });

      

    return title;
}

function highlightRed(flaggedText) {
    jQuery.each( flaggedText, function( i, val ) {
        var replaced = $("body").html().replace(val, '<span style="background-color: coral;" class="hoverableFakeNews">' +  val + '</span>');
        $("body").html(replaced);
      });
    
}
