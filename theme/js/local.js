$(document).ready(function() {
    // Every image referenced from a Markdown document
    $(".body img, .article img").each(function() {

        // do not turn the image into a figure if alt="no-figure"
        if(($(this).attr("alt") == "no-figure") ||
            ($(this).closest(".thumbnail").length !== 0)) {
            return;
        }

        $(this).wrap('<figure style="width:'+(this.width+1)+'px;"></figure>');
        if($(this).attr("alt")) {
            // Let's put a caption if there is one
            $(this).after('<figcaption>'+$(this).attr("alt")+'</figcaption>');
        }
    });

    var gloaded = false;

    // iterate over div.galleria not in div.gallery
    $("div.galleria").filter(function(){
        return !$(this).parents('div').hasClass('gallery');
    }).each(function(index) {
        // Load the classic theme only once
        if (!gloaded) {
            Galleria.loadTheme(galleria_theme_url);
            gloaded = true;
        }
        // Initialize Galleria
        $('.galleria').galleria({
            flickr: $(this).attr("id"),
            flickrOptions: {
                max: 500
            },
            responsive: true,
            height: 0.5625
        });
    });

    $("div.gallery").each(function(index) {
        // Load the classic theme only once
        if (!gloaded) {
            Galleria.loadTheme(galleria_theme_url);
            gloaded = true;
        }
            
        var flickr = new Galleria.Flickr();
        var gal = $(this).find('div.galleria');
        var loader = $('<div>', { 'class': 'loader' }).hide().appendTo(this);
        var set;

        flickr.setOptions({
            max: 500,
            description: true
        });

        // attach event handler for the menu
        $(this).find('.nav a').not('.dropdown-toggle').click(function(e) {

            e.preventDefault();

            // extract the set id from the link href
            set = this.href.split('/');
            set = set[set.length-2];

            if (gal.data('galleria')) {
                // if galleria has already been initialized: display the loader
                loader.text('Loading "'+$(this).text()+'"').show();
            }

            flickr.set(set, function(data) {

                // hide the loader
                loader.fadeOut('fast');

                if (gal.data('galleria')) {
                    // if galleria has already been initialized: load the new data
                    gal.data('galleria').load(data);
                } else {
                    // else initialize galleria (1st time)
                    gal.galleria({
                        dataSource: data,
                        responsive: true,
                        height: 0.5625
                    });
                }
            });

            // update 'active' class
            $(this).closest('div.gallery').find('.nav li').removeClass('active');
            $(this).parents('li').addClass('active');
        });

        // trigger a click onload so that the first gallery will be displayed when entering
        $(this).find('.nav a').not('.dropdown-toggle').first().click();

    });
});
