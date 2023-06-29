$(document).ready(function () {
    function attachButton(roomSection) {
        const addAdultButton = roomSection.find(".add-adult");
        const subtractAdultButton = roomSection.find(".sub-adult");
        const adultInput = roomSection.find('input[name^="no_of_adulte"]');

        addAdultButton.click(function () {
            if (parseInt(adultInput.val()) < 10) {
                adultInput.val(parseInt(adultInput.val()) + 1);
            }
        });

        subtractAdultButton.click(function () {
            if (parseInt(adultInput.val()) > 0) {
                adultInput.val(parseInt(adultInput.val()) - 1);
            }
        });

        const addChildButton = roomSection.find(".add-child");
        const subtractChildButton = roomSection.find(".sub-child");
        const childInput = roomSection.find('input[name^="no_of_child"]');

        addChildButton.click(function () {
            if (parseInt(childInput.val()) < 10) {
                childInput.val(parseInt(childInput.val()) + 1);
            }
        });

        subtractChildButton.click(function () {
            if (parseInt(childInput.val()) > 0) {
                childInput.val(parseInt(childInput.val()) - 1);
            }
        });
    }

    $(".add_room").click(function () {
        var n = $(".room-sec").length + 1;
        if (10 < n) {
            alert("You have reached the maximum number of rooms!");
            return false;
        }

        $.ajax({
            type: "GET",
            url: "/Hotel/",
            data: {
                "result": n,
            },
            dataType: "json",
            success: function (data) {
                // any process in data
                alert("successfull")
            },
            failure: function () {
                alert("failure");
            }
        });
        console.log(n);
        var newRoomSection =
            '<div class="room-sec"><div class="add-person"><h5>Room <span class="room-number">' +
            n +
            '</span>:</h5><div class="person-quantity"><span>Adults <small>Above 12 years</small></span><div class="quantity-box"><button type="button" class="sub-adult">-</button><input type="number" required class="num" value="1" name="no_of_adulte' +
            (n) +
            '" /><button type="button" class="add-adult">+</button></div></div><div class="person-quantity"><span>Child <small>Below 12 Years</small></span><div class="quantity-box"><button type="button" class="sub-child">-</button><input type="number" value="0" min="0" max="9" name="no_of_child' +
            (n) +
            '" /><button type="button" class="add-child">+</button></div></div></div><div class="text-right"><a href="javascript:void(0)" class="remove-box">Remove</a></div></div>';

        console.log(newRoomSection);
        var roomSection = $(newRoomSection);
        $(".room_list").append(roomSection);

        attachButton(roomSection);
    });

    $("body").on("click", ".remove-box", function () {
        $(this).parent().parent().remove();
        n--;
    });
    attachButton($(".room-sec"));
});



// Flatpicker
flatpickr('js-flatpickr-time', {
    enableTime: true,
    noCalendar: true,
    altinput: true,
    altformat: "H:i",
    dateFormat: "H:i",
    time_24hr: true,
});

// Select Box
$("#country-select").IconSelectBox(true);

// Quantity Box
$(".add").click(function () {
    if ($(this).prev().val() < 10) {
        $(this)
            .prev()
            .val(+$(this).prev().val() + 1);
    }
});
$(".sub").click(function () {
    if ($(this).next().val() > 1) {
        if ($(this).next().val() > 1)
            $(this)
                .next()
                .val(+$(this).next().val() - 1);
    }
});

// Date Picker
$(function () {
    $(".datepicker").datepicker({
        dateFormat: "dd-mm-yy",
    });
    $(".datepicker").datepicker("setDate", new Date());
    $("#check_out").datepicker(
        "setDate", "+1"
    );
});

// Phone Number
$(document).ready(function () {
    $(".input-phone").intlInputPhone();
});

// Price Range Slilder
$(function () {
    $("#price-range").slider({
        range: true,
        min: 0,
        max: 500,
        values: [75, 300],
        slide: function (event, ui) {
            $("#amount").val("₹" + ui.values[0] + " - ₹" + ui.values[1]);
        },
    });
    $("#amount").val(
        "₹" +
        $("#price-range").slider("values", 0) +
        " - ₹" +
        $("#price-range").slider("values", 1)
    );
});

// Discount Slider
$("#discount-slider").owlCarousel({
    dots: false,
    nav: true,
    navText: [
        "<i class='fa fa-angle-left'></i>",
        "<i class='fa fa-angle-right'></i>",
    ],
    loop: true,
    margin: 15,
    smartSpeed: 1000,
    autoplay: false,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
        },
        556: {
            items: 2,
        },
        992: {
            items: 3,
        },
    },
});

// Hotel List Slider
$(".hotel-list-slider").owlCarousel({
    margin: 0,
    items: 1,
    nav: true,
    navText: [
        "<i class='fa fa-angle-left'></i>",
        "<i class='fa fa-angle-right'></i>",
    ],
    dots: false,
    loop: true,
    smartSpeed: 2000,
    autoplay: true,
    autoplayTimeout: 4000,
    autoplayHoverPause: false,
    responsiveClass: false,
});

// Hotel Details Slider
$(document).ready(function () {
    var bigimage = $("#big-slider");
    var thumbs = $("#thumbs-slider");
    //var totalslides = 10;
    var syncedSecondary = true;

    bigimage
        .owlCarousel({
            items: 1,
            slideSpeed: 2000,
            nav: true,
            autoplay: false,
            autoHeight: true,
            dots: false,
            loop: true,
            responsiveRefreshRate: 200,
            navText: [
                '<i class="fa fa-angle-left" aria-hidden="true"></i>',
                '<i class="fa fa-angle-right" aria-hidden="true"></i>',
            ],
        })
        .on("changed.owl.carousel", syncPosition);

    thumbs
        .on("initialized.owl.carousel", function () {
            thumbs.find(".owl-item").eq(0).addClass("current");
        })
        .owlCarousel({
            loop: true,
            items: 10,
            dots: false,
            nav: false,
            smartSpeed: 200,
            slideSpeed: 500,
            slideBy: 4,
            responsiveRefreshRate: 100,
        })
        .on("changed.owl.carousel", syncPosition2);

    function syncPosition(el) {
        //if loop is set to false, then you have to uncomment the next line
        //var current = el.item.index;

        //to disable loop, comment this block
        var count = el.item.count - 1;
        var current = Math.round(el.item.index - el.item.count / 2 - 0.5);

        if (current < 0) {
            current = count;
        }
        if (current > count) {
            current = 0;
        }
        //to this
        thumbs
            .find(".owl-item")
            .removeClass("current")
            .eq(current)
            .addClass("current");
        var onscreen = thumbs.find(".owl-item.active").length - 1;
        var start = thumbs.find(".owl-item.active").first().index();
        var end = thumbs.find(".owl-item.active").last().index();

        if (current > end) {
            thumbs.data("owl.carousel").to(current, 100, true);
        }
        if (current < start) {
            thumbs.data("owl.carousel").to(current - onscreen, 100, true);
        }
    }

    function syncPosition2(el) {
        if (syncedSecondary) {
            var number = el.item.index;
            bigimage.data("owl.carousel").to(number, 100, true);
        }
    }

    thumbs.on("click", ".owl-item", function (e) {
        e.preventDefault();
        var number = $(this).index();
        bigimage.data("owl.carousel").to(number, 300, true);
    });
});

// Smooth Scroll
$('.scroll')
    .not('[href="#"]')
    .not('[href="#0"]')
    .click(function (event) {
        if (
            location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '')
            &&
            location.hostname == this.hostname
        ) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
            if (target.length) {
                event.preventDefault();
                $('html, body').animate({
                    scrollTop: target.offset().top
                }, 1000, function () {
                    var $target = $(target);
                    $target.focus();
                    if ($target.is(":focus")) {
                        return false;
                    } else {
                        $target.attr('tabindex', '-1');
                        $target.focus();
                    };
                });
            }
        }
    });
