$(document).ready(function(){
    highlightRed([" introducing special tracks", "Also gluten-free"]);
});

function highlightRed(flaggedText) {
    jQuery.each( flaggedText, function( i, val ) {
        var replaced = $("body").html().replace(val, '<span style="background-color: coral;" class="hoverableFakeNews">' +  val + '</span>');
        $("body").html(replaced);
      });
    
    //$( "#highlightFakeNews" ).toggle( "highlight" );   
}
