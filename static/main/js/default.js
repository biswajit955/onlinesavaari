// Select Box
$('#country-select').IconSelectBox(true);

// Quantity Box
$('.add').click(function () {
    let adult=parseInt(document.getElementById("three-max").value);
    let child=parseInt(document.getElementById("nine-max").value);
    let infant=parseInt(document.getElementById("six-max").value);
    let num1=child+adult;
    let key = $(this).prev().attr("id");
    if(num1 < 9 || key === "six-max") {
        console.log(num1, key)
        if(key === "three-max" || key === "nine-max"){
            $(this).prev().val(+$(this).prev().val() + 1);
        } else if(infant < adult) {
            $(this).prev().val(+$(this).prev().val() + 1);
        } else {
            return;
        }

        var name;
        if(document.getElementById("economy").checked){
            name="Economy";
        }else if(document.getElementById("business").checked){
            name="Business";
        }else{
            name="Premimum Economy";
        }

        adult=parseInt(document.getElementById("three-max").value);
        child=parseInt(document.getElementById("nine-max").value);
        infant=parseInt(document.getElementById("six-max").value);
        var num=infant+child+adult;
        var data=num.toString().concat(" traveller, ").concat(name);
        $("#countData").text(data);
        $("#countData").append('<i class="fa-solid fa-angle-down"></i>');
    }
});
$('.sub').click(function () {
    if ((this.classList.length == 2) && ($(this).next().val() < 2)) return;
    if ($(this).next().val() > 0) {
        if(adult === infant && $(this).next().attr("id") === "three-max" ) {
            $('#six-max').val(0);
        }
        if ($(this).next().val() > 0) $(this).next().val(+$(this).next().val() - 1);

        var name;
        if(document.getElementById("economy").checked){
            name="Economy";
        }else if(document.getElementById("business").checked){
            name="Business";
        }else{
            name = "Premimum Economy";
        }

        var adult=parseInt(document.getElementById("three-max").value);
        var child=parseInt(document.getElementById("nine-max").value);
        var infant=parseInt(document.getElementById("six-max").value);
        var num=infant+child+adult;
        var data=num.toString().concat(" traveller, ").concat(name);
        $("#countData").text(data);
        $("#countData").append('<i class="fa-solid fa-angle-down"></i>');
    }
});



//Date Picker
// $(function () {
//     $(".datepicker").datepicker({
//         dateFormat: "dd-mm-yy"
//     });
//     $(".datepicker").datepicker("setDate", new Date());
// });

$(function () {
    let startDate;
    let returnDate;
    let today = new Date();
    $('#startDate').datepicker({
        dateFormat: 'dd-mm-yy',
    })
    $('#returnDate').datepicker({
        dateFormat: 'dd-mm-yy',
    })
    $( "#multiReturnDate" ).datepicker({ minDate: 0, dateFormat: 'dd-mm-yy'});
    $('#startDate').datepicker('setDate', new Date());
    $('#returnDate').datepicker('setDate', new Date());
    $('#multiReturnDate').datepicker('setDate', new Date());
    $('#startDate').change(function () {
        startDate = $(this).datepicker('getDate');

        $('#returnDate').datepicker('option', 'minDate', startDate);
    });
    $('#returnDate').change(function () {
        returnDate = $(this).datepicker('getDate');
        $('#startDate').datepicker('option', 'maxDate', returnDate);
    });
});

// Phone Number
$(document).ready(function () {
    $('.input-phone').intlInputPhone();
});

// Price Range Slilder
$(function () {
    $("#price-range").slider({
        range: true,
        min: 0,
        max: 100000,
        values: [75, 100000],
        slide: function (event, ui) {
            $("#amount").val("₹" + ui.values[0] + " - ₹" + ui.values[1]);
        }
    });
    $("#amount").val("₹" + $("#price-range").slider("values", 0) +
        " - ₹" + $("#price-range").slider("values", 1));
});

// Listing Filter
$(function () {
    $(".listing-filter-open").click(function () {
        $('body').addClass('overflown');
        $(".listing-filter").addClass("active");
    });
    $(".listing-filter-close").click(function () {
        $('body').removeClass('overflown');
        $(".listing-filter").removeClass("active");
    });
    // $(".flight-details-toggle").click(function () {
    //     $(".flights-details").toggleClass("show");
    // });
    // $(".fare-toggle").click(function () {
    //     $(".fare-details").toggleClass("show");
    // });
    $(".fare-sidebar-open").click(function () {
        $('body').addClass('overflown');
        $(".fare-rules-sidebar").addClass("active");
    });
    $(".fare-sidebar-close").click(function () {
        $('body').removeClass('overflown');
        $(".fare-rules-sidebar").removeClass("active");
    });
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

// Slider Four
$('.slider-four').owlCarousel({
    dots: false,
    nav: true,
    navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
    loop: true,
    margin: 10,
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

// Slider Five
$('.slider-five').owlCarousel({
    dots: false,
    nav: true,
    navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
    loop: true,
    margin: 10,
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
        1024: {
            items: 5,
        },
    }
});

