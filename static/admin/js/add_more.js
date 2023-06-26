// passenger Name //
var counter = 1;

function add_more_field() {
    counter += 1
    html = '<hr> <div class="form-row" id="row' + counter + '">\
                <div class="col-md-2 mb-4">\
                    <label>Passenger</label>\
                    <select name="passenger'+ counter + '" class="form-control slct_type" id="slct_type'+ counter +'" onchange="getPassengerType('+ counter +')" required>\
    <option value ="">--Select--</option>\
    <option value="adult">Adult</option>\
     <option value="child">Child</option>\
     <option value="infant">Infant</option>\
                    </select>\
                </div>\
                <div class="col-md-2 mb-4">\
                    <label>Title</label>\
                    <select name="title'+ counter + '" id="slct_title'+ counter + '" class="slct_title form-control" required>\
                    </select >\
                </div>\
                <div class="col-md-4 mb-4">\
                    <label>First Name</label>\
                    <input type="text" class="form-control" name="first_name'+ counter + '" placeholder="First Name" required>\
                </div>\
                <div class="col-md-4 mb-4">\
                    <label>Last Name</label>\
                    <input type="text" class="form-control" name="last_name'+ counter + '"  placeholder="Last Name" required>\
                </div>\
                <div class="col-md-4 mb-4">\
                    <label>Seat no</label>\
                    <input type="text" class="form-control" name="seat_no'+ counter + '" placeholder="Seat no" required>\
                </div>\
                <div class="col-md-4 mb-4">\
                    <label>Date of birth</label>\
                    <input type="date" class="form-control" name="date_of_birth'+ counter + '"  placeholder="Date of birth" required>\
                </div>\
                <div class="col-md-4 mb-4">\
                    <label>Passport no:</label>\
                    <input type="text" class="form-control" name="passport'+ counter + '"  placeholder="Passport no" required>\
                </div>\
            </div>'
    $('#passenger_form').append(html);
    document.getElementById("passenger_form_count").value = counter;





}

// passenger Name End //

// add Adult ,child ,infant//



// var list1 = document.querySelector('.slct_type');

// 	list1.options[0] = new Option('--Select--', '');
// 	list1.options[1] = new Option('Adult', 'adult');
// 	list1.options[2] = new Option('Child', 'child');
// 	list1.options[3] = new Option('Infant', 'infant');

function getPassengerType(id) {
    var list1 = document.getElementById('slct_type' + id);
    var list2 = document.getElementById('slct_title' + id);
    var list1SelectedValue = list1.options[list1.selectedIndex].value;

    if (list1SelectedValue == 'adult') {

        list2.options.length = 0;
        list2.options[0] = new Option('--Select--', '');
        list2.options[1] = new Option('Mr', 'Mr');
        list2.options[2] = new Option('Mrs', 'Mrs');
        list2.options[3] = new Option('Ms', 'Ms');

    }
    else if (list1SelectedValue == 'child') {

        list2.options.length = 0;
        list2.options[0] = new Option('--Select--', '');
        list2.options[1] = new Option('Master', 'Master');
        list2.options[2] = new Option('Miss', 'Miss');

    }
    else if (list1SelectedValue == 'infant') {

        list2.options.length = 0;
        list2.options[0] = new Option('--Select--', '');
        list2.options[1] = new Option('Master', 'Master');
        list2.options[2] = new Option('Miss', 'Miss');

    }
    else if (list1SelectedValue == '') {

        list2.options.length = 0;

    }
}



populateAirlineNameDropdown(1);
populateAirportNameDropdown(1);



// slct_airline.options[0] = new Option("--Select--", "");
// slct_origin_airport.options[0] = new Option("--Select--", "");
// slct_dest_airport.options[0] = new Option("--Select--", "");

//populate airport_name dropdown

function populateAirportNameDropdown(id) {
var slct_origin_airport = document.getElementById('origin_airport' + id);

var slct_dest_airport = document.getElementById('dest_airport' + id);

    fetch('../../static/flight/airport_list.json')
        .then((response) => response.json())
        .then((json) => {
            airport_list = json;

            for (var i = 0; i <= airport_list.length; i++) {

                slct_origin_airport.options[i + 1] = new Option(airport_list[i].name, airport_list[i].name);
                slct_dest_airport.options[i + 1] = new Option(airport_list[i].name, airport_list[i].name);

            }


        });

}


//populate airline_name dropdown

function populateAirlineNameDropdown(id) {

    var slct_airline = document.getElementById('airline_name' + id);

    fetch('../../static/flight/airlines.json')
        .then((response) => response.json())
        .then((json) => {
            airline_list = json;
            for (var i = 0; i <= airline_list.length; i++) {

                slct_airline.options[i + 1] = new Option(airline_list[i].name, airline_list[i].name);

            }

        });
}

function getFlightCode(id) {

    var list1 = document.getElementById('airline_name' + id);
    var list1SelectedValue = list1.options[list1.selectedIndex].value;


    fetch('../../static/flight/airlines.json')
        .then((response) => response.json())
        .then((json) => {
            airline_list = json;

            index = airline_list.findIndex(x => x.name === list1SelectedValue);

            document.getElementById('flight_code' + id).value = airline_list[index].code
        });

}

function getOriginAirportCode(id) {

    var list1 = document.getElementById('origin_airport' + id);
    var list1SelectedValue = list1.options[list1.selectedIndex].value;
    

    fetch('../../static/flight/airport_list.json')
        .then((response) => response.json())
        .then((json) => {
            airport_list = json;

            index = airport_list.findIndex(x => x.name === list1SelectedValue);

            document.getElementById('source' + id).value = airport_list[index].code
            
        });

}

function getDestAirportCode(id) {
    

    var list2 = document.getElementById('dest_airport' + id);
    var list2SelectedValue = list2.options[list2.selectedIndex].value;


    fetch('../../static/flight/airport_list.json')
        .then((response) => response.json())
        .then((json) => {
            airport_list = json;

            index = airport_list.findIndex(x => x.name === list2SelectedValue);

            document.getElementById('destination' + id).value = airport_list[index].code
        });

}





// End //


// Airline info //

var counter = 1;
function add_more() {
    counter += 1
    html = ' <hr> <div class="form-row mb-4" id = "rows' + counter + '" >\
            <div class="form-group col-md-12">\
                <label>Airline name:</label>\
                <select id="airline_name' + counter + '" name="airline'+ counter + '" class="form-control" onchange="getFlightCode('+ counter +')" required>\
                     <option value ="">--Select--</option>\
                </select>\
            </div>\
            <div class="form-group col-md-6">\
                <label>Origin airport</label>\
                <select id="origin_airport' + counter + '" name="origin_airport'+ counter + '" class="form-control" onchange="getOriginAirportCode('+ counter +')" required>\
                    <option value ="">--Select--</option>\
                </select>\
            </div>\
            <div class="form-group col-md-6">\
                <label>Destination airport</label>\
                <select id="dest_airport' + counter + '" name="dest_airport'+ counter + '" class="form-control" onchange="getDestAirportCode('+ counter +')" required>\
                    <option value ="">--Select--</option>\
                </select>\
            </div>\
            <div class="form-group col-md-4">\
                <label>Flight code</label>\
                <input type="text" class="form-control" name="flight_code'+ counter + '" id="flight_code'+ counter + '" placeholder="Flight code" readonly>\
            </div>\
            <div class="form-group col-md-4">\
                <label for="in_flight_no">Flight number</label>\
                <input type="text" class="form-control" name="flight_number'+ counter + '" id="in_flight_no" placeholder="Flight Number" required>\
            </div>\
            <div class="form-group col-md-4">\
                <label>Stop</label>\
                <select id="stop" class="form-control" name="stop1" required>\
                <option value="True">True</option>\
                <option value="False" selected>False</option>\
                </select>\
            </div>\
            <div class="form-group col-md-6">\
                <label for="in_departure_date">Departure date:</label>\
                <input type="date" class="form-control" name="departure_date'+ counter + '" id="in_departure_date" required>\
            </div>\
            <div class="form-group col-md-6">\
                <label for="in_departure_time">Departure time:</label>\
                <input type="time" class="form-control" name="departure_time'+ counter + '" id="in_departure_time" required>\
            </div>\
            <div class="form-group col-md-6">\
                <label for="in_arrival_date">Arrival date:</label>\
                <input type="date" class="form-control" name="arrival_date'+ counter + '" id="in_arrival_date" required>\
            </div>\
            <div class="form-group col-md-6">\
                <label for="in_arrival_time">Arrival time:</label>\
                <input type="time" class="form-control" name="arrival_time'+ counter + '" id="in_arrival_time" required>\
            </div>\
            <div class="form-group col-md-6">\
                <label>Src</label>\
               <input type="text" class="form-control" name="src'+ counter + '" id="source'+ counter + '" placeholder="Source" readonly>\
            </div>\
            <div class="form-group col-md-6">\
                <label>Dest</label>\
               <input type="text" class="form-control" name="dest'+ counter + '" id="destination'+ counter + '" placeholder="Destination" readonly>\
            </div>\
            </div>'
    
    $('#airline_form').append(html);
    document.getElementById("airline_form_count").value = counter;
    populateAirlineNameDropdown(counter);
    populateAirportNameDropdown(counter);
}


