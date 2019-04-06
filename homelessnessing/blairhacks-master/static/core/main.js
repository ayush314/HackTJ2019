$(document).ready(function () {
    var html = $('html');
    var navbar = $('#navbar');
    var content = $('#content');
    var texts = content.children();
    var scrolling = false;
    var lastScroll = 0;
    var scaleM = .7;

    if ($(window).width() <= 768) {
        scaleM = 1;
    }


    content.css({
        'margin-top': scaleM * navbar.height()
    });


    var footer = $('#footer');
    footer.css({
        'margin-top': Math.max(0, $(window).height() - (footer.height() + footer.offset().top))
    });

    function preventDefault(e) {
        e = e || window.event;
        if (e.preventDefault)
            e.preventDefault();
        e.returnValue = false;
    }

    function disable_scrolling() {
        html.css({'overflow-y': 'hidden'});
        html.css({'margin-right': 'calc(100vw - 100%)'});
        if (window.addEventListener) // older FF
            window.addEventListener('DOMMouseScroll', preventDefault, false);
        window.onwheel = preventDefault; // modern standard
        window.onmousewheel = document.onmousewheel = preventDefault; // older browsers, IE
        window.ontouchmove = preventDefault; // mobile
        scrolling = true;
    }

    function enable_scrolling() {
        html.css({'overflow-y': 'scroll'});
        $('html').css({'margin-right': '0'});
        if (window.removeEventListener)
            window.removeEventListener('DOMMouseScroll', preventDefault, false);
        window.onmousewheel = document.onmousewheel = null;
        window.onwheel = null;
        window.ontouchmove = null;
        scrolling = false;
    }

    var updatePage = function () {
        var windowHeight = $(window).innerHeight();

        // Scroll snapping code
        if ($(this).scrollTop() < windowHeight - 10 && !scrolling) {
            disable_scrolling();
            var delta = $(this).scrollTop() - lastScroll;
            if (delta < 0) {
                $('html, body').animate({scrollTop: 0}, 750,
                    function () {
                        enable_scrolling();
                    });
            }
            else if (delta > 0) {
                $('html, body').animate({scrollTop: windowHeight}, 750,
                    function () {
                        enable_scrolling();
                    });
            }
        }


        var pFade = $(this).scrollTop() / windowHeight;
        var scaleV = Math.max(1 - (1 - scaleM) * pFade, scaleM);
        if ($(window).width() <= 768) {
            scaleV = 1;
        }
        navbar.css({
            'transform': 'translateY(' + -Math.min($(this).scrollTop() - (1 - scaleV) / 2 * navbar.height(), windowHeight - (.5 + scaleM / 2) * navbar.height() + 1) + 'px) scaleY(' + scaleV + ')',
            'background-color': 'rgba(170, 0, 0,' + Math.min(pFade, 1) + ')'
        });
        navbar.children().css({
            'transform': 'scaleX(' + scaleV + ')'
        });


        for (var i = 0; i < texts.length; i++) {
            var text_block = $(texts[i]).children();

            for (var j = 0; j < text_block.length; j++) {
                var text = $(text_block[j]);

                var percentVisible = 1 - Math.sqrt(Math.sqrt((Math.max(0, text.offset().top + text.height() - $(this).scrollTop() - windowHeight) + Math.max(0, $(this).scrollTop() + scaleM * navbar.height() - text.offset().top)) / text.height()));

                if ($(window).width() <= 768) {
                    percentVisible = 1;
                }

                text.css({
                    'opacity': Math.max(0, percentVisible)
                });
            }
        }

        lastScroll = $(this).scrollTop();
    };

    if (window.location.pathname == '/') {
        // Smooth scrolling on front page
        $('a[href*="#"]')
        // Remove links that don't actually link to anything
            .not('[href="#"]')
            .not('[href="#0"]')
            .click(function (event) {
                // On-page links
                if (
                    location.pathname.replace(/^\//, '') === this.pathname.replace(/^\//, '')
                    &&
                    location.hostname === this.hostname
                ) {
                    // Figure out element to scroll to
                    var target = $(this.hash);
                    var navbar_height = $('#navbar').height();
                    target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
                    // Does a scroll target exist?
                    if (target.length) {
                        // Only prevent default if animation is actually gonna happen
                        event.preventDefault();
                        disable_scrolling();
                        $('html, body').animate({
                            scrollTop: target.offset().top - scaleM * navbar_height
                        }, 1000, function () {
                            // Callback after animation
                            // Must change focus!
                            var $target = $(target);
                            $target.focus();
                            enable_scrolling();
                        });
                    }
                }
            });


        $(document).scroll(updatePage);

        updatePage();
        updatePage();
        enable_scrolling();
    }
});

