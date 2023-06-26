import { Renderflight } from "./src/flight.js";
import { Combo } from "./src/combo.js"

let caltime;
$.ajax({
  type: "GET",
  url: "/flight/loader/",
  data: json,
  beforeSend: function(){
    caltime = new Date();
  },
  success: function (res) {
    $('#flight-list').removeClass('active')
    $('#flight-list').html("")
    let urlreload = window.location.href;
    window.sessionStorage.setItem('search_result', urlreload)
    window.sessionStorage.setItem('stimer', timer);
    console.log(res, ((new Date()) - caltime) / 1000)
    if (res.data.searchResult.tripInfos['COMBO']) {
      const c = new Combo(res, $('#flight-list'), url, userdata, json)
      console.log(c.trip)
      c.sortrender()
      c.flrender(c.all)
    }
    else {
      const fl = new Renderflight(res, $('#flight-list'), url, userdata, json)
      fl.test()
      console.log(fl.akasa_data, fl.trip, fl.akasa_fare, fl.gds_data,fl.gds_fare)
      setpricerange(fl.minmaxp())
      $('.filter-list2').html("")
      $('.filter-list2').html((fl.allairline()).map(it => {
        return `
        <li>
          <label class="custom-checkbox">${it}
            <input type="checkbox" value="${it}" name="airline">
            <span class="checkmark"></span>
          </label>
        </li>
        `;
      }))
      if (res['spice_serach']) {
        fl.checkspice(res['spice_serach'])
      }
      fl.sortrender()
      fl.flrender(fl.trip)
      console.log(fl.el_chk_chng())
      fl.el_chk_chng().map(el => el.change(function(){console.log(this.checked, )}))
      fl.all_chk_func().map(el => el.change(function () {
        fl.checkchecker()
      }))
      fl.checkchecker()
      fl.elsort().forEach(element => element.click(function () {
        let prev = {...fl.sortlist};
        Object.keys(fl.sortlist).forEach(el => fl.sortlist[el] = false)
        fl.sortlist[$(this).attr('id')] = true;
        fl.sort(prev, $(this).attr('data-name'))
        fl.all_chk_func().map(el => el.change(function () {
          fl.checkchecker()
        }))
        $('#flight-list').find('.flight1').submit(function (e) { 
          e.preventDefault()
          let time = fl.el_chk_chng().map(el => {
            return [(new Date($(el).attr('data-ddate'))), (new Date($(el).attr('data-adate')))]
          })
          let diff = time.reverse().map((el, inx) => {
            if (!(inx >= (time.length - 1))) {
              return (el[0] - time[inx + 1][1])/1000
            }
          })
          diff = diff.filter(Number)
          let check = diff.every(el => el >= 14400)
          if (check) {
            document.getElementById('flight1').submit()
          }
      
        })
      }))
      filterdata(fl)
    }
  }
});

function filterdata(main_class) {
  let data = {}
  $('#filter-form').on('submit', function (e) {
    data = {}
    e.preventDefault()
    $(this).find('input').each(function () {
      let name = $(this).attr('name');
      let v = this.value
      
      if ($(this).prop('checked') || name == 'price') {
        if (name == 'price') {
          data[name] = v;
        }
        else {
          !data[name] ? data[name] = [v] : data[name].push(v)
        }
      }
    })
    main_class.filter(data, main_class.trip)
    main_class.all_chk_func().map(el => el.change(function () {
      main_class.checkchecker()
    }))
  })
  $('#flight-list').find('.flight1').submit(function (e) { 
    console.log(main_class.err['mes'])
    e.preventDefault()
    let time = main_class.el_chk_chng().map(el => {
      return [(new Date($(el).attr('data-ddate'))), (new Date($(el).attr('data-adate')))]
    })
    let diff = time.reverse().map((el, inx) => {
      if (!(inx >= (time.length - 1))) {
        return (el[0] - time[inx + 1][1])/1000
      }
    })
    diff = diff.filter(Number)
    let check = diff.every(el => el >= 14400)
    if ((check) && !(main_class.err['mes'])) {
      document.getElementById('flight1').submit()
    } else {
      swal({
        title: 'We are Sorry!',
        text: 'We could not confirm your flight(s).please choose another flight',
        timer: 2000,
        padding: '2em',
        onOpen: function () {
          swal.showLoading()
        }
      }).then(function (result) {
        if (
          // Read more about handling dismissals
          result.dismiss === swal.DismissReason.timer
        ) {
          console.log('I was closed by the timer')
        }
      })
    }
  })
}

function setpricerange(arr) {
    $("#price-range").slider({
        range: true,
        min: arr[0],
        max: arr[1],
        values: arr,
        slide: function (event, ui) {
            $("#amount").val("₹" + ui.values[0] + " - ₹" + ui.values[1]);
        }
    });
    $("#amount").val("₹" + $("#price-range").slider("values", 0) +
        " - ₹" + $("#price-range").slider("values", 1));
}
