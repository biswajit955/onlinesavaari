$(function () {
    var settings = {
        rows: 6,
        cols: 30,
        seatWidth: 34,
        seatHeight: 34,
        seatCss: 'seat',
        selectedSeatCss: 'selectedSeat',
        selectingSeatCss: 'selectingSeat'
    };

    var init = function (reservedSeat) {
        var str = [],
            seatNo, className;
        for (i = 0; i < settings.rows; i++) {
            for (j = 0; j < settings.cols; j++) {
                seatNo = (i + j * settings.rows + 1);
                className = settings.seatCss;
                if ($.isArray(reservedSeat) && $.inArray(seatNo, reservedSeat) != -1) {
                    className += ' ' + settings.selectedSeatCss;
                }
                str.push('<li class="' + className + '"' +
                    '>' +
                    '</li>');
            }
        }
        $('#place').html(str.join(''));
    };

    //case I: Show from starting
    //init();

    //Case II: If already booked
    var bookedSeats = [1, 2, 3, 4, 5, 6, 10, 24, 30];
    init(bookedSeats);


    $('.' + settings.seatCss).click(function () {
        if ($(this).hasClass(settings.selectedSeatCss)) {
            alert('This seat is already reserved');
        } else {
            $(this).toggleClass(settings.selectingSeatCss);
        }
    });
});