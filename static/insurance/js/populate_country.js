
//populate country dropdown



    var slct_country = document.getElementById('country');

    fetch('../../static/insurance/country_list.json')
        .then((response) => response.json())
        .then((json) => {
            country_list = json;
            for (var i = 0; i <= country_list.length; i++) {
                slct_country.options[i + 1] = new Option(country_list[i].name, country_list[i].code);
            }
        });
