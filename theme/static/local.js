$(document).ready(function() {
    // Every image referenced from a Markdown document
    $(".body img, .article img").each(function() {
        $(this).wrap('<figure style="width:'+(this.width+1)+'px;"></figure>')
        if($(this).attr("alt")) {
            // Let's put a caption if there is one
            $(this).after('<figcaption>'+$(this).attr("alt")+'</figcaption>');
        }
    });
});
