$(document).ready(function(){
    highlightRed([" introducing special tracks", "Also gluten-free"]);
    console.log(getTitle())
});



function getTitle(){

    var title = $("title").html();
    var reputableArticles = [];
    var reputableURL = [];
    
      var parsedQuery = title.split(" ").join("+").replace(/<[^<>]*>/g, "").replace(/[|-]/g, '');
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
          var clusterRaw = [];
          var counter = 0;
        data.value.forEach(function(article) {
           // console.log(article.url);
            $.get(article.url, function(datum) {
                //var data = $(data);
                //console.log($("p", datum).html());
                var allContent = $.map($("p", datum), function(element){
                    return $(element).html();
                });
                console.log(allContent);
                stringAllContent = allContent.join(" ").replace(/<[^<>]*>/g, " ").replace(/[^a-zA-Z. ]/g, ' ');
                clusterRaw.push(stringAllContent);
                //console.log(clusterRaw);
                
                
            }).always(function(){
                if (counter++ === data.value.length-1)  {
                    console.log(clusterRaw);
                }         
            });
            //reputableURL.push(article.url);
        });

      });

      reputableURL.forEach(function(url){
        $.get(url, function(data){
            //var data = $(data);
            console.log(data);
        })
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
