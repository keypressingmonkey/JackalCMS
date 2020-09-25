var Arya = {
    currentPage : 0,
    pageSize : 4,
    totalPages : 100,
    init : function() {
        $('.open-side-menu').click(this.openSideMenu);
        $('body').click(this.toggleSideMenu);
        $('.st-menu').find('>ul').find('>li').find('>a').click(this.sideMenuInteraction);
        $('.close-side-menu').click(this.closeSideMenu);
        setTimeout(function() {
            Arya.initWidgetsHeight();
        }, 100);
        this.resizeSlider();
        this.initSlider();
        this.initNormalSlider();
        this.initStickyPostHeader();
        //$('.st-menu').outerHeight($(window).height());
        if($('body').hasClass('has-infinite-scroll')) {
            $(window).scroll(Arya.initInfiniteScroll);
        }
        $('.sidebar-slider').bind('mousewheel', function(e) {
            var body = $('body');
            if(!body.hasClass('scrolling')) {
                Arya.initMouseMove(e.originalEvent.wheelDelta, true);
                body.addClass('scrolling');
            }
        });
        $('.sidebar-slider').bind('DOMMouseScroll', function(e) {
            var body = $('body');
            if(!body.hasClass('scrolling')) {
                Arya.initMouseMove(e.originalEvent.detail, false);
                body.addClass('scrolling');
            }
        });
    },
    initMouseMove : function(index, inverse) {
          if(index > 0) {
              if(inverse) {
                  Arya.sidebarSlider.goToPrevSlide();
              } else {
                  Arya.sidebarSlider.goToNextSlide();
              }
          } else {
              if(inverse) {
                  Arya.sidebarSlider.goToNextSlide();
              } else {
                  Arya.sidebarSlider.goToPrevSlide();
              }
          }
        setTimeout(function() {
            $('body').removeClass('scrolling');
        }, 1500);
    },
    initInfiniteScroll : function() {
        var windowH = $(window).height();
        var scrollTop = $(window).scrollTop();
        var watchContainer = $('main').find('.left-container');
        if($('body').hasClass('homepage3')) {
            watchContainer = $('main').find('.homepage-articles');
        }
        var treshold = watchContainer.outerHeight() + $('header').outerHeight() + $('.normal-slider-wrap').outerHeight();
        if(treshold * 0.95 < (scrollTop + windowH) ) {
            Arya.startInfiniteScroll();
            $('body').addClass('loading');
        }
    },
    startInfiniteScroll : function() {
        var body = $('body');
        if(body.hasClass('loading')) return false;
        if(Arya.currentPage >= Arya.totalPages) return false;
        if(body.hasClass('homepage3')) {
            Arya.infiniteScrollHomepage3();
        }
        if(body.hasClass('homepage2')) {
            Arya.infiniteScrollHomepage2();
        }
        return true;
    },
    infiniteScrollHomepage3 : function() {
        var appendContainer = $('.homepage-articles').find('.col-sm-12');
        $.ajax({
            method: "GET",
            url : 'dataHomepage3.php',
            dataType : 'json',
            data : {
                page : Arya.currentPage,
                pageSize : Arya.pageSize
            },
            success : function(rsp) {
                Arya.appendContent(rsp, appendContainer);
            }
        });
    },
    infiniteScrollHomepage2 : function() {
        var appendContainer = $('#post-container').find('.left-container');
        $.ajax({
            method: "GET",
            url : 'dataHomepage2.php',
            dataType : 'json',
            data : {
                page : Arya.currentPage,
                pageSize : Arya.pageSize
            },
            success : function(rsp) {
                Arya.appendContent(rsp, appendContainer);
            }
        });
    },
    initWidgetsHeight : function() {
        var container = $('#post-container').find('.left-container').first();
        var widgets = $('.widgets');
        container.removeAttr('style');
        widgets.removeAttr('style');
        var minHeight = container.height() > widgets.height() ? container.height() : widgets.height();
        if($(window).width() >= 768) {
            container.css('min-height', minHeight+'px');
            //widgets.css('min-height', minHeight+'px');
        }
    },
    appendContent : function(rsp, appendContainer) {
        Arya.currentPage++;
        Arya.totalPages = rsp.totalPages;
        setTimeout(function() {
            $('body').removeClass('loading');
        }, 500);
        $.each(rsp.items, function(index, item) {
            var source = $("#article-template").html();
            var template = Handlebars.compile(source);
            var html = template(item);
            html = $(html).hide();
            appendContainer.append(html.fadeIn(300, function() {
                Arya.initWidgetsHeight();
            }));
        });
    },
    openSideMenu : function(e) {
        var body = $('body');
        $('#main-container').css('min-height', $(window).height() + "px");
        //$('.st-menu').outerHeight($(window).height());
        if(body.hasClass('st-menu-open')) {
            body.removeClass('st-menu-open');
            setTimeout(function() {
                body.removeClass('body-overflow');
            }, 300);
        } else {
            setTimeout(function() {
                body.addClass('st-menu-open');
                setTimeout(function() {
                    body.addClass('body-overflow');
                }, 300);
            }, 50);
        }
        e.preventDefault();
    },
    closeSideMenu : function() {
        var body = $('body');
        body.removeClass('st-menu-open');
        setTimeout(function() {
            body.removeClass('body-overflow');
        }, 300);
    },
    toggleSideMenu : function() {
        var body = $('body');
        if(body.hasClass('st-menu-open') && !$('.st-menu').is(':hover')) {
            body.removeClass('st-menu-open');
            setTimeout(function() {
                body.removeClass('body-overflow');
            }, 300);
        }
    },
    sideMenuInteraction : function(e) {
        var el = $(this);
        var next = $(this).next();
        if(next.is('ul')) {
            if(next.is(':visible')) {
                next.slideUp(300);
                el.parent().removeClass('selected');
            } else {
                next.slideDown(300);
                el.parent().addClass('selected');
            }
            e.preventDefault();
        }
    },
    resizeSlider : function() {
        var mainSlider = $('.main-slider');
        var sidebarSlider = $('.sidebar-slider');
        var windowH = $(window).height();
        $('.full-homepage').height(windowH);
        mainSlider.height(windowH);
        sidebarSlider.height(windowH);
        mainSlider.find('article').outerHeight(windowH);
        sidebarSlider.find('article').outerHeight(windowH/3);
        var slideH = windowH/3;
        $('.right-section').find('.bx-viewport').css({
            'padding-top' : slideH + "px"
        });
    },
    initNormalSlider : function() {
        var normalSliderWrap = $('.normal-slider-wrap');
        var slider = $('.normal-slider').bxSlider({
            mode: 'vertical',
            slideSelector : '.slide',
            controls : false,
            pager : false,
            onSlideBefore : function() {
                normalSliderWrap.find('.slider-controls').find('.current-slide').text(slider.getCurrentSlide()+1);
            }
        });
        if(normalSliderWrap.length) {
            normalSliderWrap.find('.slider-controls').find('.current-slide').text(slider.getCurrentSlide()+1);
            normalSliderWrap.find('.slider-controls').find('.count-slides').text(slider.getSlideCount());
            normalSliderWrap.find('.slider-controls').find('.prev').on('click', function() {
                slider.goToPrevSlide();
            });
            normalSliderWrap.find('.slider-controls').find('.next').on('click', function() {
                slider.goToNextSlide();
            });
        }
    },
    initSlider : function() {
        var sidebarSliderContainer = $('.sidebar-slider');
        var rightSection = $('.right-section');
        var mainSlider = $('.main-slider');
        Arya.sidebarSlider = sidebarSliderContainer.bxSlider({
            mode: 'vertical',
            minSlides: 3,
            moveSlides : 1,
            controls : false,
            pager : false,
            onSliderLoad : function() {
                var windowH = $(window).height();
                var slideH = windowH/3;
                $('.right-section').find('.bx-viewport').css({
                    'padding-top' : slideH + "px"
                });
            },
            onSlideBefore : function($slideElement) {
                $('html, body').animate({
                    scrollTop: 0
                }, 500);
                sidebarSliderContainer.find('.active').removeClass('active');
                $slideElement.addClass('active');
                rightSection.find('.slider-controls').find('.current-slide').text(Arya.sidebarSlider.getCurrentSlide()+1);
            },
            onSlideNext : function() {
                var visibleItem = mainSlider.find('.visible');
                var next = visibleItem.next();
                if(!visibleItem.next().is('article')) {
                    next = mainSlider.find('article').first();
                }
                visibleItem.addClass('firstAnim').removeClass('bigIndex');
                next.addClass('bigIndex');
                setTimeout(function() {
                    next.addClass('secondAnim').addClass('visible');
                }, 400);
                setTimeout(function() {
                    visibleItem.removeClass('visible').removeClass('firstAnim');
                    next.removeClass('secondAnim');
                }, 800);
                setTimeout(function() {
                    next.removeClass('bigIndex');
                }, 1200);
            },
            onSlidePrev : function() {
                var visibleItem = mainSlider.find('.visible');
                var prev = visibleItem.prev();
                if(!visibleItem.prev().is('article')) {
                    prev = mainSlider.find('article').last();
                }
                visibleItem.addClass('firstAnim').removeClass('bigIndex');
                prev.addClass('bigIndex');
                setTimeout(function() {
                    prev.addClass('bigIndex').addClass('secondAnim').addClass('visible');
                }, 400);
                setTimeout(function() {
                    visibleItem.removeClass('visible').removeClass('firstAnim');
                    prev.removeClass('secondAnim');
                }, 800);
                setTimeout(function() {
                    prev.removeClass('bigIndex');
                }, 1200);

            }
        });
        sidebarSliderContainer.find('article').on('click', function() {
            var index = $(this).data('slide-index');
            if(Arya.sidebarSlider.getCurrentSlide() != index) {
                var visibleItem = mainSlider.find('.visible');
                var currentSlide = mainSlider.find('article').eq(index);
                Arya.sidebarSlider.goToSlide(index);
                visibleItem.addClass('firstAnim').removeClass('bigIndex');
                currentSlide.addClass('bigIndex');
                setTimeout(function() {
                    currentSlide.addClass('secondAnim').addClass('visible');
                }, 400);
                setTimeout(function() {
                    visibleItem.removeClass('visible').removeClass('firstAnim');
                    currentSlide.removeClass('secondAnim');
                }, 800);
                setTimeout(function() {
                    currentSlide.removeClass('bigIndex');
                }, 1200);
            }
        });
        if(Arya.sidebarSlider.length) {
            rightSection.find('.slider-controls').find('.current-slide').text(Arya.sidebarSlider.getCurrentSlide()+1);
            rightSection.find('.slider-controls').find('.count-slides').text(Arya.sidebarSlider.getSlideCount());
            rightSection.find('.slider-controls').find('.prev').on('click', function() {
                Arya.sidebarSlider.goToPrevSlide();
            });
            rightSection.find('.slider-controls').find('.next').on('click', function() {
                Arya.sidebarSlider.goToNextSlide();
            });
        }
    },
    initStickyPostHeader : function() {
        $postHeader = $('.post-header');
        $headerHeight = $('.image-header').outerHeight();
        $containerWIdth = $('.left-container').outerWidth();
        if ($(window).scrollTop() <= $headerHeight) {
            $postHeader.removeClass('sticky');
        } else {
            $postHeader.addClass('sticky');
            $('.sticky').css('width', $containerWIdth + 'px');
        }
    }
};
$(document).ready(function() {
    "use strict";
   Arya.init();
});
$(window).resize(function() {
    Arya.initWidgetsHeight();    
    Arya.resizeSlider();
    Arya.initStickyPostHeader();
});
$(window).scroll(function(){
    Arya.initStickyPostHeader();
});