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

    $("div.galleria").each(function(index) {
        // Load the classic theme only once
        if (index === 0) {
            Galleria.loadTheme(galleria_theme_url);
        }
        // Initialize Galleria
        $('.galleria').galleria({
            flickr: $(this).attr("id"),
            responsive: true,
            height: 0.5625
        });
    });
});
