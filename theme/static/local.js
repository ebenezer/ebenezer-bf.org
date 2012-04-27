$(document).ready(function() {
    // Every image referenced from a Markdown document
    $(".body img, .article img").each(function() {

        // do not turn the image into a figure if alt="no-figure"
        if($(this).attr("alt") == "no-figure") {return;}

        $(this).wrap('<figure style="width:'+(this.width+1)+'px;"></figure>')
        if($(this).attr("alt")) {
            // Let's put a caption if there is one
            $(this).after('<figcaption>'+$(this).attr("alt")+'</figcaption>');
        }
    });
});
