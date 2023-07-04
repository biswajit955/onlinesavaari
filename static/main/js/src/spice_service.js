class Service {
    constructor(ssr, seat,person,adult,child,infant, rel, apiamount, amount) {
        this.srr = JSON.parse(ssr);
        this.seat = seat;
        this.rel = rel;
        this.apiamount = apiamount;
        this.amount = amount;
        this.seatmap = {};
        this.selection = {};
        this.bagselection = {};
        this.paxobj = {};
        this.insurance = 0;
        this.person=person;
        this.adult=adult;
        this.child=child;
        this.infant=infant;
        this.test = (check) => {
            let totalamount = parseFloat(this.amount);
            let totalapiamount = parseFloat(this.apiamount);
            //console.log(this.bagselection, this.selection)
            // console.log($('#total-flight-amount').text(""))
            if (this.selection != {}) {
                for (const [k, v] of Object.entries(this.selection)) {
                    $(`#addonmeal${k}`).remove()
                    $('#add-on').append(`
                    <p id="addonmeal${k}">
                    <span>
                    Meal (${v.route})
                    <a onclick="onremoveMeal('${k}')" href="javascript:void(0)" class="close">
                    <i class="fa fa-close"></i>
                    </a>
                    </span>
                    <span class="green">(+) ₹ ${v.amount}</span>
                    </p>
                    `)
                    totalamount +=  parseFloat(v.amount)
                    totalapiamount +=  parseFloat(v.amount)
                }
            }
            if (this.bagselection != {}) {
                for (const [k, v] of Object.entries(this.bagselection)) {
                    $(`#addonbag${k}`).remove()
                    $('#add-on').append(`
                    <p id="addonbag${k}">
                    <span>
                    BAG ${k} (${v.code})
                    <a onclick="onremoveBag('${k}')" href="javascript:void(0)" class="close">
                    <i class="fa fa-close"></i>
                    </a>
                    </span>
                    <span class="green">(+) ₹ ${v.amount}</span>
                    </p>
                    `)
                    totalamount +=  parseFloat(v.amount)
                    totalapiamount +=  parseFloat(v.amount)
                }
            }
            if (this.paxobj != {}) {
                // $.isEmptyObject(paxobj[el])
                let amount = 0
                Object.keys(this.paxobj).map(el => {
                    if (!$.isEmptyObject(this.paxobj[el])) {
                        amount += Object.values(this.paxobj[el]).reduce((a, b) => {
                            a += parseFloat(b['amount'])
                            return a
                        }, 0)
                    }
                })
                //console.log(amount)
                $(`#addonseat`).remove()
                $('#add-on').append(`
                <p id="addonseat">
                <span>
                SEAT
                <a onclick="onremoveseat()" href="javascript:void(0)" class="close">
                <i class="fa fa-close"></i>
                </a>
                </span>
                <span class="green">(+) ₹ ${amount}</span>
                </p>
                `)
                totalamount +=  parseFloat(amount)
                totalapiamount +=  parseFloat(amount)
            }
            $('input[name="amount"]').val(totalamount + (this.insurance))
            $('input[name="apiamount"]').val(totalapiamount)
            $('#total-flight-amount').text(totalamount + (this.insurance))
            //console.log($('input[name="amount"]').val(), $('input[name="apiamount"]').val())
        }
    }
    
    seatloc(item, el, showinx) {
        //console.log(item)
        if (item['seatmap']['sData']) { 
            let col = item['seatmap']['sData']['column']
            return item['seatmap']['sInfo'].map((it, inx) => {
                return `
                <a data-code=${it.code} data-show="showseat" data-route="${item.route}" data-placement="top" class="p-0 grid-cell seatclick" style="position:relative;border: 0; cursor: pointer;grid-column:${it.seatPosition.row};grid-row:${it.seatPosition.column}" type="button" title="${it.seatNo} ${it.amount}" data-animation="true" data-loop="${inx}" data-seatno="${it.seatNo}" data-seatRow="${it.seatPosition.row}" data-seatColumn="${it.seatPosition.column}" data-isBooked="${it.isBooked}" data-isLegroom="${it.isLegroom || false}" data-amount="${it.amount}" ${!it.isBooked ? `class="availableSeat" data-selected="false"` : "" }>
                <img src=${it.isBooked ? "/static/main/images/icon/seat/booked.png" : "/static/main/images/icon/seat/available.png"} />
                </a>
                `;
            }).join("")
        } else {
            return `${item['seatmap']['nt']}`
        }
    }

    seatchangerender(bid, code, amount, per, bool) {
        //console.log(code, amount, per, bool)
        //console.log(Object.keys(this.paxobj).map(el => this.paxobj[el][bid] ? this.paxobj[el][bid]['code'] == per['code'] : false))
        let check = {}
        $(`.cn-st${bid} a`).removeClass("seatactive")
        let rend = Object.keys(this.paxobj).map(el => {
            check[el] = !!this.paxobj[el][per['bid']]
            !check[el] || $(`.cn-st${bid} [data-code=${this.paxobj[el][bid]['code']}]`).addClass("seatactive")
            $(`#changeseat${bid} [data-person="${el}"]`).prop('checked', !!this.paxobj[el][per['bid']]);
            check[el] ? "" : $(`#changeseat${bid} .${el}${bid} .seat-details`).html("");
            return per['person'] == el && check[el] ? `<small class="seat-number">${this.paxobj[el][bid]['code']}</small> <small class="">₹${this.paxobj[el][bid]['amount']}</small>` : ""
        })
        //console.log(check)
        //console.log($(`cn-st${bid} [data-code="${per['code']}"]`))
        bool ? $(`#changeseat${bid} .${per['person']}${bid} .seat-details`).html(rend) : $(`#changeseat${bid} .${per['person']}${bid} .seat-details`).html("") 
        bool ? $(`.cn-st${bid} [data-code=${per['code']}]`).addClass("seatactive") : $(`.cn-st${bid} [data-code="${per['code']}"]`).removeClass("seatactive")
        this.test()
    }

    seatcheck() {
        let current = {}
        let paxobj = this.paxobj;
        let scroll = 0;
        let xpost = 0;
        let ypost = 0;
        let click = false;
        let seatcode;
        let seatamount;
        $('#border-top-contact').find('.seatclick').click(function () {
            if ($(this).attr("data-isbooked") == "true") return;
            click = true;
            let id = $(this).attr("data-show")
            //console.log(id)
            xpost = this.offsetLeft;
            ypost = this.offsetTop;
            let seatnum = $(this).attr("data-seatno") 
            seatcode = $(this).attr("data-code") 
            seatamount = $(this).attr("data-amount")
            current['code'] = seatcode;
            current['amount'] = seatamount;
            $(`.${id} .showseat__title`).html(`
            <p class="seat-number">Seat ${seatnum}</p>
            <p class="seat-amount">₹${seatamount}</p>
            `)
            $(`.${id}`).css({ display: "block", top: `${ypost - 10}px`, left:`${xpost + 10 - scroll}px`})
            $(`.${id}`).find(".paxseat").attr('data-seat', seatcode)
            $(`.${id}`).find(".paxseat").attr('data-amount', seatamount)
        })
        $(".seat-layout").scroll(function () {
            if (click) {                
                scroll = $(this).scrollLeft()
                let id = $(this).attr("data-id")
                $(`.showseat${id}`).css({ display: "block", top: `${ypost - 10}px`, left:`${xpost + 10 - scroll}px`})
            }
        });
        $('.showseat').focusin(function () {
            let id = $(this).attr("data-id")
            $(`.cn-st${current['bid']}`).focus();
        })
        $(".cn-st").focusout(function () {
            let id = $(this).attr("data-id")
            if (!$(`.showseat${current['bid']}`).is(":focus,:hover")) {
                $(`.showseat${current['bid']}`).css({ display: "none" })
                click = false;
            }
        });

        $(".paxseat").change(function () {
            let bid = $(this).attr("data-bid")
            let person = $(this).attr("data-person")
            let code = $(this).attr("data-seat")
            current["person"] = person;
            if ($(this).prop('checked') || code != (paxobj[person][bid] ? paxobj[person][bid]['code'] : code)) {             
                let amount = $(this).attr("data-amount")
                //console.log(bid, person, code, amount)
                //console.log("change done")
                Object.keys(paxobj).map(el => {
                    if ((el != person) && !($.isEmptyObject(paxobj[el]))) {
                        paxobj[el][bid] ? !(paxobj[el][bid]['code'] == code) || delete paxobj[el][bid] : "";
                    }
                })
                paxobj[person][bid] = {
                    bid,
                    code,
                    amount,
                }
                //console.log(paxobj)
                runtest(bid, current, true)
            }
            else {
                delete paxobj[person][bid]
                runtest(bid, current, false)
            }
        })
        const runtest = (bid, person, bool) => {
            this.seatchangerender(bid, seatcode, seatamount, person, bool)
        }

    }

    seattag() {
        return Object.values(this.tripinfo).map((el, inx) => {
            return el.map((route, i) => {
                return `
                <li class="nav-item">
                    <a class="nav-link ${inx == 0 && i == 0 ? "active" : ""}" id="justify-pills-contact-tab" data-toggle="pill" href="#${Object.keys(this.tripinfo)[inx]}${i}seat" role="tab" aria-controls="justify-pills-contact" aria-selected="${inx == 0 && i == 0}">${Object.keys(this.tripinfo)[inx]}: ${route}</a>
                </li>
                `
            }).join("")
        }).join("")
    }

    renderseat() {
        // console.log(seat)
        const seatperson = () => {
            return `<ul>${
                Object.keys(this.paxobj).map((el) => {
                    return `
                        <li style="padding:1em 0.5em;border-bottom: 1px solid gray;" class="${el}">
                        <div class="n-chk" class="">
                            <label style="display:flex;align-items:center;justify-content: space-between;" class="new-control mr-0 new-checkbox new-checkbox-rounded checkbox-success">
                            <input type="checkbox" class="new-control-input paxseat" data-person="${el}">
                            <span class="new-control-indicator" style="top:-3px;"></span>${el}
                            <div class="seat-details">

                            </div>
                            </label>
                        </div>
                        </li>
                    `;
                }).join("")
            }</ul>`

        }
        let render = Object.keys(this.seatmap).map((el, inx) => {
            //console.log('el is---',this.seatmap[el])
            let it=this.seatmap[el]
            //return this.seatmap[el].map((it, i) => {
                let row = 0
                if (it['seatmap']['sData']) { 
                    row = it['seatmap']['sData']['column']
                }              
                return `
                <div class="tab-pane fade ${inx == 0 ? "show active" : ""}" role="tabpanel" aria-labelledby="justify-pills-contact-tab">
                    <div class="seat-booking" style="position:relative;">
                        <div id="showseat" class="showseat showseat" tabindex="102" data-id="${inx}">
                            <div class="showseat__title">
                                <p class="seat-number">Seat 6F</p>
                                <p class="seat-amount">₹300</p>
                            </div>
                            <div id="changeseat">
                            ${seatperson()}
                            </div>
                        </div>
                        <div class="cn-st cn-st${inx} cn-st${it.bid}" tabindex="100" data-id="${inx }">
                            <div id="seat-layout" data-id="${inx}" class="seat-layout" style="grid-template-rows: repeat(auto-fill, 35px);">
                                ${this.seatloc(it, el, (inx))}
                            </div>
                        </div>
                        <ul class="seat-info">
                            <li style="background-image:url(/static/main/images/icon/seat/available.png);">Available Seat</li>
                            <li style="background-image:url(/static/main/images/icon/seat/booked.png);">Booked Seat</li>
                            <li style="background-image:url(/static/main/images/icon/seat/selected.png);">Selected Seat</li>
                        </ul>
                    </div>
                </div>
                `;
            //}).join("")
        }).join("")
        let renddata = `
        <ul class="nav nav-pills mb-3 mt-3 nav-fill" id="justify-pills-tab" role="tablist">

        </ul>
        <div class="tab-content" id="justify-pills-tabContent">
        ${render}
        </div>
        `;
        $('#border-top-contact').html("")
        $('#border-top-contact').append(renddata)
        this.seatcheck()
    }
    seatdata() {
        //console.log('seat data---  ',this.seat)
        let el=JSON.parse(this.seat);
        //Object.keys(this.seat['data'][0]['fees']).map(px => {
        Object.keys(el['Envelope']['Body']['GetSeatAvailabilityResponse']['SeatAvailabilityResponse']['SeatGroupPassengerFees']['SeatGroupPassengerFee']).map(px => {
            this.paxobj[px] = {}
        })
        //console.log(this.paxobj)
        //console.log(this.seat)
        //console.log('deperture station--- ',el['Envelope'])

        this.seatmap['ONWARD'] = {
                //route: el['data'][0]['seatMap']['departureStation'] + "-" + el['data'][0]['seatMap']['arrivalStation'],
                route: el['Envelope']['Body']['GetSeatAvailabilityResponse']['SeatAvailabilityResponse']['EquipmentInfos']['EquipmentInfo']['DepartureStation'] + "-" + el['Envelope']['Body']['GetSeatAvailabilityResponse']['SeatAvailabilityResponse']['EquipmentInfos']['EquipmentInfo']['ArrivalStation'],
                seatmap: {
                    "sData": {
                        "row": el['Envelope']['Body']['GetSeatAvailabilityResponse']['SeatAvailabilityResponse']['EquipmentInfos']['EquipmentInfo']['Compartments']['CompartmentInfo']['Length'],
                        "column": el['Envelope']['Body']['GetSeatAvailabilityResponse']['SeatAvailabilityResponse']['EquipmentInfos']['EquipmentInfo']['Compartments']['CompartmentInfo']['Width'],
                    },
                    "sInfo": el['Envelope']['Body']['GetSeatAvailabilityResponse']['SeatAvailabilityResponse']['EquipmentInfos']['EquipmentInfo']['Compartments']['CompartmentInfo']['Seats']['SeatInfo'].filter(fi => !fi['SeatDesignator'].includes("$")).map(st => {
                        return {
                            "seatNo": st['SeatDesignator'],
                            "seatPosition": {
                                "row": parseInt(st['Y']),
                                "column": parseInt(st['X'])
                            },
                            "isBooked": !st['Assignable'],
                            "isLegroom": true,
                            //"isAisle": st['PropertyList'].find(fn => fn['EquipmentProperty'].map( ex => {let v=0; if(ex['TypeCode'] == 'AISLE'){v=1}})) != -1 ? true : false,
                            "isAisle": false,
                            "code": st['SeatDesignator'],
                            "amount":this.seatAmountCalculation(st['SeatGroup'],el),
                            //"amount":el['Envelope']['Body']['GetSeatAvailabilityResponse']['SeatAvailabilityResponse']['SeatGroupPassengerFees']['SeatGroupPassengerFee'][]
                            // "amount": Object.values(el['Envelope']['Body']['GetSeatAvailabilityResponse']['SeatAvailabilityResponse']['SeatGroupPassengerFees']['SeatGroupPassengerFee'] ['fees'])[0]['groups'][st['group']]['fees'][0]['serviceCharges'].reduce((a, b) => {
                            //     let b_p = b.amount
                            //     return a + b_p
                            // }, 0),
                            "ctds": 0,
                            "unitKey": st['SeatGroup']
                        }
                    })
                } 
            }
        
        this.renderseat()
    }

    seatAmountCalculation(seatGrp,el){

        let amount=0
        el['Envelope']['Body']['GetSeatAvailabilityResponse']['SeatAvailabilityResponse']['SeatGroupPassengerFees']['SeatGroupPassengerFee'].map(px => {
            //console.log('pl is--',px)
            if(px['SeatGroup'] == seatGrp){
                if(Array.isArray(px['PassengerFee']['ServiceCharges']['BookingServiceCharge'])){
                    //console.log("amount is ----",parseInt(px['PassengerFee']['ServiceCharges']['BookingServiceCharge'][0]['Amount']))
                    px['PassengerFee']['ServiceCharges']['BookingServiceCharge'].map(xx =>{
                        amount=amount+parseFloat(xx['Amount'])
                    })
                }else{
                    amount=parseFloat(px['PassengerFee']['ServiceCharges']['BookingServiceCharge']['Amount'])
                }
                //amount=parseFloat(px['PassengerFee']['ServiceCharges']['BookingServiceCharge'][0]['Amount']) + parseFloat(px['PassengerFee']['ServiceCharges']['BookingServiceCharge'][1]['Amount']) + parseFloat(px['PassengerFee']['ServiceCharges']['BookingServiceCharge'][2]['Amount']) + parseFloat(px['PassengerFee']['ServiceCharges']['BookingServiceCharge'][3]['Amount'])
            }
        })
        return amount
    }

    mealtag() {
        //console.log("meal----",this.srr)
        //console.log("meal----",JSON.stringify(this.srr))
        let legKey=this.srr['Envelope']['Body']['GetSSRAvailabilityForBookingResponse']['SSRAvailabilityForBookingResponse']['SSRSegmentList']
        if (!Array.isArray(legKey)) {
            legKey = [legKey]
        }
        return legKey.map((el, inx) => {
            return `
                <li class="nav-item">
                    <a class="nav-link ${inx == 0 ? "active" : ""}" id="justify-pills-home-tab" data-toggle="pill" href="#${el['SSRSegment']['LegKey']['DepartureStation']}${el['SSRSegment']['LegKey']['ArrivalStation']}" role="tab" aria-controls="justify-pills-home" aria-selected="${inx == 0}">${el['SSRSegment']['LegKey']['DepartureStation']} : ${el['SSRSegment']['LegKey']['ArrivalStation']}</a>
                </li>
                `
        }).join("")
    }
    baggtag() {
        //return this.srr['data']['legSsrs'].map((el, inx) => {
        let legKey=this.srr['Envelope']['Body']['GetSSRAvailabilityForBookingResponse']['SSRAvailabilityForBookingResponse']['SSRSegmentList']
        if (!Array.isArray(legKey)) {
            legKey = [legKey]
        }
        return legKey.map((el, inx) => {
            return `
                <li class="nav-item">
                    <a class="nav-link ${inx == 0 ? "active" : ""}" id="justify-pills-home-tab" data-toggle="pill" href="#bagg${el['SSRSegment']['LegKey']['DepartureStation']}${el['SSRSegment']['LegKey']['ArrivalStation']}" role="tab" aria-controls="justify-pills-home" aria-selected="${inx == 0}">${el['SSRSegment']['LegKey']['DepartureStation']} : ${el['SSRSegment']['LegKey']['ArrivalStation']}</a>
                </li>
                `
        }).join("")
    }

    routerend(inx, route) {
        let legKey=this.srr['Envelope']['Body']['GetSSRAvailabilityForBookingResponse']['SSRAvailabilityForBookingResponse']['SSRSegmentList']['SSRSegment']['AvailablePaxSSRList']['AvailablePaxSSR']
        if (!Array.isArray(legKey)) {
            legKey = [legKey]
        }
        //${Object.values(el['PaxSSRPriceList']['PaxSSRPrice']['PaxFee']['ServiceCharges']['BookingServiceCharge'])[0]['Amount'] || "Free Meal"}
        //<input data-way="ONWARD" data-route='${route}' data-amount=${Object.values(el['PaxSSRPriceList']['PaxSSRPrice']['PaxFee']['ServiceCharges']['BookingServiceCharge'])[0]['Amount'] ? Object.values(el['PaxSSRPriceList']['PaxSSRPrice']['PaxFee']['ServiceCharges']['BookingServiceCharge'])[0]['Amount'] * Object.values(el['PaxSSRPriceList']['PaxSSRPrice']['PaxFee']['ServiceCharges']['BookingServiceCharge']).length : 0 } data-code='${el.name}' data-unitkey=${JSON.stringify(el['PaxSSRPriceList']['PaxSSRPrice']['PaxFee']['ServiceCharges']['BookingServiceCharge'])} type="radio" class="btn-check hidden" name="options" id="${index}${inx}" autocomplete="off" value="${el.SSRCode}">

        //return this.srr['data']['legSsrs'][inx]['ssrs'].map((el , index) => {
            let count=0
        return legKey.map((el, index) => {

            if(el['PaxSSRPriceList']!=null){
                count++;
                //console.log('routerend----',index);
                let amountData=el['PaxSSRPriceList']['PaxSSRPrice']['PaxFee']['ServiceCharges']['BookingServiceCharge']
                if (!Array.isArray(amountData)) {
                    amountData = [amountData]
                }
                //console.log('amount is-------- ',el['PaxSSRPriceList']['PaxSSRPrice']['PaxFee']['ServiceCharges']['BookingServiceCharge']);
                //${amountData[0]['Amount'] || "Free Meal"}

            return `
            <div class="carousel-item ${count == 1 ? "active" : ""}">
                <div class="col-md-4">
                    <div class="card card-body p-0">
                    <div class="service-item">
                        <span class="food-type veg"></span>
                        <img class="img-fluid" src="/static/main/images/icon/food/3.png">
                        <div class="info-sec">
                            <p class="m-0"><b>${el.SSRCode}</b></p>
                            <p class="m-0">${el.SSRCode}</p>
                            <p class="small">₹
                            ${this.mealPrice(amountData) || "Free Meal"}
                            </p>
                            <input data-way="ONWARD" data-route='${route}' data-amount=${this.mealPrice(amountData) ? this.mealPrice(amountData) * el['PaxSSRPriceList']['PaxSSRPrice']['PaxFee']['ServiceCharges']['BookingServiceCharge'].length : 0 } data-code='${el.SSRCode}' data-unitkey=${el.SSRCode} type="radio" class="btn-check hidden" name="options" id="MEAL${index}${inx}" autocomplete="off" value="${el.SSRCode}">
                            <label class="btn btn-secondary m-0" for="${index}${inx}" style="margin-left:-11px;">
                            <span class="label">Select</span>
                            </label>
                        </div>
                    </div>
                    </div>
                </div>
            </div>
            `;
            }
        }).join("")
    }

    mealPrice(amountData){

        let amt=0.0
        for(let i=0;i<amountData.length;i++){
            amt=amt+parseFloat(amountData[i]['Amount'])
        }
        return amt;
    }

    mealrend() {
        let legKey=this.srr['Envelope']['Body']['GetSSRAvailabilityForBookingResponse']['SSRAvailabilityForBookingResponse']['SSRSegmentList']
        if (!Array.isArray(legKey)) {
            legKey = [legKey]
        }
        //let data = this.srr['data']['legSsrs'].map((el, inx) => {
        let data = legKey.map((el, inx) => {
            //console.log('meal rend--- ',inx)
                return `
                <div class="tab-pane fade ${inx == 0 ? "show active" : ""}" id="${el['SSRSegment']['LegKey']['DepartureStation']}${el['SSRSegment']['LegKey']['ArrivalStation']}" role="tabpanel" aria-labelledby="justify-pills-home-tab">
                <div class="container text-center my-3">
                <div class="row mx-auto my-auto">
                    <div id="recipeCarousel${el['SSRSegment']['LegKey']['DepartureStation']}${el['SSRSegment']['LegKey']['ArrivalStation']}${inx}" class="carousel carousel1 slide w-100" data-ride="carousel">
                    <div class="carousel-inner w-100" role="listbox">
                    ${this.routerend(inx, el['SSRSegment']['LegKey']['DepartureStation'] + el['SSRSegment']['LegKey']['ArrivalStation'])}
                    </div>
                        <a class="carousel-control-prev w-auto" href="#recipeCarousel${el['SSRSegment']['LegKey']['DepartureStation']}${el['SSRSegment']['LegKey']['ArrivalStation']}${inx}" role="button" data-slide="prev">
                            <span class="carousel-control-prev-icon bg-dark border border-dark p-2" aria-hidden="true"></span>
                            <span class="sr-only">Previous</span>
                        </a>
                        <a class="carousel-control-next w-auto" href="#recipeCarousel${el['SSRSegment']['LegKey']['DepartureStation']}${el['SSRSegment']['LegKey']['ArrivalStation']}${inx}" role="button" data-slide="next">
                            <span class="carousel-control-next-icon bg-dark border border-dark p-2" aria-hidden="true"></span>
                            <span class="sr-only">Next</span>
                        </a>
                    </div>
                </div>
            </div>
                </div>
                `
        }).join("")
        // let data = "data"
        return `
        <div class="tab-content" id="justify-pills-tabContent">
        ${data}   
        </div>
        `
    }
    slider() {
        let func = this.test
        let select = this.selection
        let bagselect = this.bagselection
        let legKey=this.srr['Envelope']['Body']['GetSSRAvailabilityForBookingResponse']['SSRAvailabilityForBookingResponse']['SSRSegmentList']
        if (!Array.isArray(legKey)) {
            legKey = [legKey]
        }

        //this.srr['data']['legSsrs'].map((el, inx) => { 
        legKey.map((el, inx) => {
            this.rel.find(`#recipeCarousel${el['SSRSegment']['LegKey']['DepartureStation']}${el['SSRSegment']['LegKey']['ArrivalStation']}${inx}`).carousel({
                interval: 1000000
            })
        })
        //this.srr['data']['legSsrs'].map((el, inx) => { 
        legKey.map((el, inx) => { 
            this.rel.find(`#bagg${el['SSRSegment']['LegKey']['DepartureStation']}${el['SSRSegment']['LegKey']['ArrivalStation']}`).carousel({
                interval: 1000000
            })
        })
        $('.carousel1 .carousel-item').each(function () {
            //console.log(this)
            let id = $(this).parent().parent().attr('id')
            var minPerSlide = 3;
            var next = $(this).next();
            if (!next.length) {
            next = $(this).siblings(':first');
            }
            next.children(':first-child').clone().appendTo($(this));
            
            for (var i=0;i<minPerSlide;i++) {
                next=next.next();
                if (!next.length) {
                    next = $(this).siblings(':first');
                }
                
                next.children(':first-child').clone().appendTo($(this));
            }
            $(this).find(`[name="options"]`).map(function () {
                //console.log($(this))
                $(this).change(function () {
                    //console.log(this)
                    $(`#${id} label`).removeClass('select')
                    $(`label[for="${$(this).attr('id')}"]`).addClass('select')
                    select[$(this).attr('data-route')] = {
                        "code": $(this).attr('data-code'),
                        "amount": $(this).attr('data-amount'),
                        "route": $(this).attr('data-route'),
                        "unitkey": JSON.parse($(this).attr('data-unitkey')),
                    }
                    func()
                })
            })
        });
        $('.carousel2 .carousel-item').each(function () {
            let id = $(this).parent().parent().attr('id')
            var minPerSlide = 3;
            var next = $(this).next();
            if (!next.length) {
            next = $(this).siblings(':first');
            }
            next.children(':first-child').clone().appendTo($(this));
            
            for (var i=0;i<minPerSlide;i++){
                next=next.next();
                if (!next.length) {
                    next = $(this).siblings(':first');
                }
                next.children(':first-child').clone().appendTo($(this));
            }
            $(this).find(`[name="options"]`).map(function () {
                $(this).change(function () {
                    //console.log(id)
                    //console.log(this)
                    $(`#${id} label`).removeClass('select')
                    $(`label[for="${$(this).attr('id')}"]`).addClass('select')
                    bagselect[$(this).attr('data-way')] = {
                        "code": $(this).attr('data-code'),
                        "amount": $(this).attr('data-amount'),
                        "unitkey": JSON.parse($(this).attr('data-unitkey')),
                    }
                    //console.log(bagselect)
                    func()
                })
            })
        });
    }
    baggrend() {
        // console.log(this.bagg)
        let legKey=this.srr['Envelope']['Body']['GetSSRAvailabilityForBookingResponse']['SSRAvailabilityForBookingResponse']['SSRSegmentList']
        if (!Array.isArray(legKey)) {
            legKey = [legKey]
        }
        //return legKey.map((el, inx) => {

        //let data = this.srr['data']['segmentSsrs'].map((el, inx) => {
        let data = legKey.map((el, inx) => {
                return `
                <div class="tab-pane fade ${inx == 0 ? "show active" : ""}" id="bagg${el['SSRSegment']['LegKey']['DepartureStation']}${el['SSRSegment']['LegKey']['ArrivalStation']}" role="tabpanel" aria-labelledby="justify-pills-home-tab">
                <div class="container text-center my-3">
                <div class="row mx-auto my-auto">
                    <div id="bagg${el['SSRSegment']['LegKey']['DepartureStation']}${el['SSRSegment']['LegKey']['ArrivalStation']}${inx}" class="carousel carousel2 slide w-100" data-ride="carousel">
                    <div class="carousel-inner w-100" role="listbox">
                    ${this.baggselector(inx, `${el['SSRSegment']['LegKey']['DepartureStation']}${el['SSRSegment']['LegKey']['ArrivalStation']}`)}
                    </div>
                        <a class="carousel-control-prev w-auto" href="#bagg${el['SSRSegment']['LegKey']['DepartureStation']}${el['SSRSegment']['LegKey']['ArrivalStation']}${inx}" role="button" data-slide="prev">
                            <span class="carousel-control-prev-icon bg-dark border border-dark p-2" aria-hidden="true"></span>
                            <span class="sr-only">Previous</span>
                        </a>
                        <a class="carousel-control-next w-auto" href="#bagg${el['SSRSegment']['LegKey']['DepartureStation']}${el['SSRSegment']['LegKey']['ArrivalStation']}${inx}" role="button" data-slide="next">
                            <span class="carousel-control-next-icon bg-dark border border-dark p-2" aria-hidden="true"></span>
                            <span class="sr-only">Next</span>
                        </a>
                    </div>
                </div>
            </div>
                </div>
                `
        }).join("")
        return `
        <div class="tab-content" id="justify-pills-tabContent">
        ${data}   
        </div>
        `
    }
    baggselector(inx, route) {
        //return this.srr['data']['segmentSsrs'][inx]['ssrs'].map((el , index) => {
        let legKey=this.srr['Envelope']['Body']['GetSSRAvailabilityForBookingResponse']['SSRAvailabilityForBookingResponse']['SSRSegmentList']['SSRSegment']['AvailablePaxSSRList']['AvailablePaxSSR']
        if (!Array.isArray(legKey)) {
            legKey = [legKey]
        }
        //<input data-unitkey=${JSON.stringify(el['PaxSSRPriceList']['PaxSSRPrice']['PaxFee']['ServiceCharges']['BookingServiceCharge'])} data-way=${route} data-amount=${Object.values(el['PaxSSRPriceList']['PaxSSRPrice']['PaxFee']['ServiceCharges']['BookingServiceCharge'])[0]['Amount'] ? Object.values(el['PaxSSRPriceList']['PaxSSRPrice']['PaxFee']['ServiceCharges']['BookingServiceCharge'])[0]['Amount'] * Object.values(el['PaxSSRPriceList']['PaxSSRPrice']['PaxFee']['ServiceCharges']['BookingServiceCharge']).length : 0 } data-code='${el.SSRCode}' type="radio" class="btn-check hidden" name="options" id="bagg${index}${inx}" autocomplete="off" value="${el.SSRCode}">

        let count=0
        return legKey.map((el , index) => {
            if(el['PaxSSRPriceList']!=null){
                count++;
            return `
            <div class="carousel-item ${count == 1 ? "active" : ""}">
                <div class="col-md-4">
                    <div class="card card-body p-0">
                    <div class="service-item">
                        <span class="food-type veg"></span>
                        <img class="img-fluid" src="/static/main/images/icon/bags/3.png">
                        <div class="info-sec">
                            <p class="m-0"><b>${el.SSRCode}</b></p>
                            <p class="m-0">${el.SSRCode}</p>
                            <p class="small">₹
                            ${Object.values(el['PaxSSRPriceList']['PaxSSRPrice']['PaxFee']['ServiceCharges']['BookingServiceCharge'])[0]['Amount'] || "Free Ssr"}
                            </p>
                            <input data-unitkey=${el.SSRCode} data-way=${route} data-amount=${Object.values(el['PaxSSRPriceList']['PaxSSRPrice']['PaxFee']['ServiceCharges']['BookingServiceCharge'])[0]['Amount'] ? Object.values(el['PaxSSRPriceList']['PaxSSRPrice']['PaxFee']['ServiceCharges']['BookingServiceCharge'])[0]['Amount'] * Object.values(el['PaxSSRPriceList']['PaxSSRPrice']['PaxFee']['ServiceCharges']['BookingServiceCharge']).length : 0 } data-code='${el.SSRCode}' type="radio" class="btn-check hidden" name="options" id="bagg${index}${inx}" autocomplete="off" value="${el.SSRCode}">
                            <label class="btn btn-secondary m-0" for="bagg${index}${inx}" style="margin-left:-11px;">
                            <span class="label">Select</span>
                            </label>
                        </div>
                    </div>
                    </div>
                </div>
            </div>
            `;
            }
        }).join("")
    }
    rend() {
        let data = `
        <div class="title-sec">
            <h3 data-toggle="collapse" aria-expanded="false" aria-controls="collapse1">
            <span>
                <img src="/static/main/images/icon/plus-circle.png" alt=""> Service Requests <span>(Optional)</span>
            </span>
            </h3>
        </div>
        <div class="box-one login-box">
        <div class="col-lg-12 col-12 layout-spacing pl-0 pr-0">
            <div class="statbox widget box box-shadow">
                <div class="widget-content widget-content-area border-top-tab">
                    <ul class="nav nav-tabs mb-3 mt-3" id="borderTop" role="tablist">
                        <li class="nav-item">
                            <a class="nav-link active" id="border-top-home-tab" data-toggle="tab" href="#border-top-home" role="tab" aria-controls="border-top-home" aria-selected="true">Meal</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" id="border-top-profile-tab" data-toggle="tab" href="#border-top-profile" role="tab" aria-controls="border-top-profile" aria-selected="false">Baggage</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" id="border-top-contact-tab" data-toggle="tab" href="#border-top-contact" role="tab" aria-controls="border-top-contact" aria-selected="false">Seat</a>
                        </li>
                    </ul>
                    <div class="tab-content" id="borderTopContent">
                        <div class="tab-pane fade show active pt-0" id="border-top-home" role="tabpanel" aria-labelledby="border-top-home-tab">
                            <ul class="nav nav-pills mb-3 mt-3 nav-fill" id="justify-pills-tab" role="tablist">
                               ${this.mealtag()}
                            </ul>
                            ${this.mealrend()}
                        </div>
                        <div class="tab-pane fade pt-0" id="border-top-profile" role="tabpanel" aria-labelledby="border-top-profile-tab">
                            <div class="tab-pane fade show active" id="border-top-home" role="tabpanel" aria-labelledby="border-top-home-tab">
                            <ul class="nav nav-pills mb-3 mt-3 nav-fill" id="justify-pills-tab" role="tablist">
                            ${this.baggtag()}
                            </ul>
                            ${this.baggrend()}
                            </div>
                        </div>
                        <div class="tab-pane fade pt-0" id="border-top-contact" role="tabpanel" aria-labelledby="border-top-contact-tab">
                            <div class="seat-booking"> 
                                <div class="cn-st">
                                    <div id="loader">
                                        <div class="spinner">
                                            <p>loading...</p>
                                            <div class="spinner-area spinner-first"></div>
                                            <div class="spinner-area spinner-second"></div>
                                            <div class="spinner-area spinner-third"></div>
                                        </div>
                                    </div>
                                </div>
                                <ul class="seat-info">
                                    <li style="background-image:url(/static/main/images/icon/seat/available.png);">Available Seat</li>
                                    <li style="background-image:url(/static/main/images/icon/seat/booked.png);">Booked Seat</li>
                                    <li style="background-image:url(/static/main/images/icon/seat/selected.png);">Selected Seat</li>
                                </ul>	
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        </div>
        `
        this.rel.html(data)
    }

}
