// Select Box
$('#country-select').IconSelectBox(true);

// Quantity Box
$('.add').click(function () {
    if ($(this).prev().val() < 10) {
        $(this).prev().val(+$(this).prev().val() + 1);
    }
});
$('.sub').click(function () {
    if ($(this).next().val() > 1) {
        if ($(this).next().val() > 1) $(this).next().val(+$(this).next().val() - 1);
    }
});

// Date Picker
$(function () {
    $(".datepicker").datepicker({
        dateFormat: "dd-mm-yy"
    });
    $(".datepicker").datepicker("setDate", new Date());
});

// Phone Number
$(document).ready(function () {
    $('.input-phone').intlInputPhone();
});

// Offer Slider
$('#offer-slider').owlCarousel({
    dots: false,
    nav: true,
    navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
    loop: true,
    margin: 15,
    smartSpeed: 1000,
    autoplay: false,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
        },
        768: {
            items: 2,
        },
    }
});

// Flight Slider
$('.flights-slider').owlCarousel({
    dots: false,
    nav: true,
    navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
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
    }
});

// Collection Slider
$('.collection-slider').owlCarousel({
    dots: false,
    nav: true,
    navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
    loop: true,
    margin: 15,
    smartSpeed: 1000,
    autoplay: false,
    responsiveClass: true,
    responsive: {
        0: {
            items: 2,
        },
        768: {
            items: 3,
        },
    }
});

// Flight Two Slider
$('.flights2-slider').owlCarousel({
    dots: false,
    nav: true,
    navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
    loop: true,
    margin: 15,
    smartSpeed: 1000,
    autoplay: false,
    responsiveClass: true,
    responsive: {
        0: {
            items: 2,
        },
        556: {
            items: 3,
        },
        992: {
            items: 4,
        },
    }
});