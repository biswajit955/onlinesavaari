class Service {
    constructor(obj, renderel, person) {
        this.airSegment = obj["SOAP:Envelope"]?.["SOAP:Body"]?.["air:AirMerchandisingOfferAvailabilityRsp"]?.["air:AirSolution"]?.["air:AirSegment"] ?? [];
        this.paxinfo = obj["SOAP:Envelope"]?.["SOAP:Body"]?.["air:AirMerchandisingOfferAvailabilityRsp"]?.["air:AirSolution"]?.["air:SearchTraveler"] ?? [];
        console.log(this.paxinfo);
        this.paxobj = {};
        this.rel = renderel;
        this.seatmap;
        this.insurance = 0;
        this.amount = $('input[name="amount"]').val()
        this.apiamount = $('input[name="apiamount"]').val()
        this.route = ['ONWARD', 'RETURN', "2", "3", "4"];
        this.bagg = {};
        this.bagselection = {};
        this.meal = {};
        this.tripinfo = {};
        this.trip = obj["SOAP:Envelope"]?.["SOAP:Body"]?.["air:AirMerchandisingOfferAvailabilityRsp"]?.["air:OptionalServices"]?.["air:OptionalService"] ?? [];
        console.log(this.trip);


        this.test = (check) => {
            let totalamount = parseFloat(this.amount);
            let totalapiamount = parseFloat(this.apiamount);
            console.log(this.bagselection, this.selection)
            if (this.bagselection != {}) {
                for (const [k, v] of Object.entries(this.bagselection)) {
                    let amount = parseFloat(v.amount.replace(/[^\d.-]/g, ''));
                    $(`#addonbag${k}`).remove()
                    $('#add-on').append(`
                    <p id="addonbag${k}">
                    <span>
                    BAG ${k} (${v.code})
                    <a onclick="onremoveBag('${k}')" href="javascript:void(0)" class="close">
                    <i class="fa fa-close"></i>
                    </a>
                    </span>
                    <span class="green">(+) ₹ ${amount}</span>
                    </p>
                    `)
                    totalamount +=  parseFloat(amount)
                    totalapiamount +=  parseFloat(amount)
                }
            }
            if (this.paxobj != {}) {
                console.log(this.paxobj);
                let amount = 0;
                Object.keys(this.paxobj).map(el => {
                    if (!$.isEmptyObject(this.paxobj[el])) {
                        amount += Object.values(this.paxobj[el]).reduce((a, b) => {
                            // Remove non-numeric characters using regular expression
                            let numericAmount = parseFloat(b['amount'].replace(/[^\d.-]/g, ''));
                            if (!isNaN(numericAmount)) {
                                a += numericAmount;
                            }
                            return a;
                        }, 0);
                    }
                });
                console.log(amount);

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
                totalamount += parseFloat(amount)
                totalapiamount += parseFloat(amount)
                console.log(totalamount, totalapiamount);
            }

            $('input[name="amount"]').val(totalamount)
            $('input[name="apiamount"]').val(totalapiamount)
            $('#total-flight-amount').text(totalamount + (this.insurance))

        }
    }



    seatloc(item, el, showinx) {
        console.log(item);
        console.log(el);
        if (item['seatmap']) {
            let rows = item['seatmap']['air:Rows']["air:Row"];
            let columnCount = item['seatmap']['column'];
            let rowCount = item['seatmap']['row'];

            let optionalServices = item['seatmap']['air:OptionalServices']['air:OptionalService'];

            let optionalServicesMap = {};
            for (let service of optionalServices) {
                optionalServicesMap[service['Key']] = service['TotalPrice'];
            }

            let output = "";

            for (let row of rows) {
                let rowNumber = parseInt(row["Number"]);
                let columns = row["air:Facility"];

                for (let i = 0; i < columnCount; i++) {
                    let column = columns[i];
                    try {
                        if (column["Type"] === "Seat") {
                            let seatCode = column["SeatCode"];
                            let availability = column["Availability"];
                            let isPaid = column["Paid"];
                            let optionalServiceRef = column["OptionalServiceRef"];
                            let totalPrice = optionalServiceRef ? optionalServicesMap[optionalServiceRef] : "INR0";
                            if (isPaid === "true") {
                                output += `
                                <a data-code="${seatCode}" data-show="showseat${item.bid}" name="paid-available" data-route="${item.route}" data-bid="${item.bid}" data-way="${el}" data-placement="top" class="p-0 grid-cell seatclick" style="position:relative;border: 0; cursor: pointer;grid-column:${(rowNumber - 7) + 1};grid-row:${i + 1}" type="button" title="${seatCode}" data-animation="true" data-loop data-seatno="${seatCode}" data-seatRow="${(rowNumber - 7) + 1}" data-seatColumn="${i + 1}" ${availability === "Available" ? `class="availableSeat" data-amount="${totalPrice}" data-selected="false"` : ""}>
                                    <img src="${availability === "Available" ? "/static/main/images/icon/seat/selected.png" : "/static/main/images/icon/seat/booked.png"}" />
                                </a>
                            `;
                            } else {
                                if (availability === "Available") {
                                    output += `
                                    <a data-code="${seatCode}" data-show="showseat${item.bid}" name="available" data-route="${item.route}" data-bid="${item.bid}" data-way="${el}" data-placement="top" class="p-0 grid-cell seatclick" style="position:relative;border: 0; cursor: pointer;grid-column:${(rowNumber - 7) + 1};grid-row:${i + 1}" type="button" title="${seatCode}" data-animation="true" data-loop data-seatno="${seatCode}" data-seatRow="${(rowNumber - 7) + 1}" data-seatColumn="${i + 1}" ${availability === "Available" ? `class="availableSeat" data-amount="${totalPrice}" data-selected="false"` : ""}>
                                        <img src="${"/static/main/images/icon/seat/available.png"}" />
                                    </a>
                                `;
                                } else{
                                    output += `
                                    <a data-code="${seatCode}" data-show="showseat${item.bid}" style="pointer-events: none; cursor: not-allowed;" data-route="${item.route}" data-bid="${item.bid}" data-way="${el}" data-placement="top" class="p-0 grid-cell seatclick" style="position:relative;border: 0; cursor: pointer;grid-column:${(rowNumber - 7) + 1};grid-row:${i + 1}" type="button" title="${seatCode}" data-animation="true" data-loop data-seatno="${seatCode}" data-seatRow="${(rowNumber - 7) + 1}" data-seatColumn="${i + 1}" ${availability === "Available" ? `class="availableSeat" data-amount="${totalPrice}" data-selected="false"` : ""}>
                                        <img src="${"/static/main/images/icon/seat/booked.png"}" />
                                    </a>
                                `;
                                }
                            }
                        } else {
                            output += `
                                <div style="grid-column:${(rowNumber - 7) + 1};grid-row:${i + 1}"></div>
                            `;
                        }
                    } catch (error) {
                        console.log(error);
                    }
                }
            }

            return output;
        } else {
            return `${item['seatmap']['nt']}`;
        }
    }

    seattag() {
        return Object.values(this.seatmap).map((el, inx) => {
            return el.map((route, i) => {
                console.log(route,i,"lklllllllll");
                return `
                <li class="nav-item">
                    <a class="nav-link ${inx == 0 && i == 0 ? "active" : ""}" id="justify-pills-contact-tab" data-toggle="pill" href="#${i}seat" role="tab" aria-controls="justify-pills-contact" aria-selected="${inx == 0 && i == 0}">:${route.route}</a>
                </li>
                `
            }).join("")
        }).join("")
    }

    seatchangerender(bid, code, amount, per, bool) {
        console.log(this.paxobj);
        let check = {}
        $(`.cn-st${bid} a`).removeClass("seatactive")
        let rend = Object.keys(this.paxobj).map(el => {
            check[el] = !!this.paxobj[el][per['bid']]
            !check[el] || $(`.cn-st${bid} [data-code=${this.paxobj[el][bid]['code']}]`).addClass("seatactive")
            $(`#changeseat${bid} [data-person="${el}"]`).prop('checked', !!this.paxobj[el][per['bid']]);
            check[el] ? "" : $(`#changeseat${bid} .${el}${bid} .seat-details`).html("");
            return per['person'] == el && check[el] ? `<small class="seat-number">${this.paxobj[el][bid]['code']}</small> <small class="">₹${this.paxobj[el][bid]['amount']}</small>` : ""
        })
        console.log(check)
        console.log($(`cn-st${bid} [data-code="${per['code']}"]`))
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
            console.log(id)
            xpost = this.offsetLeft;
            ypost = this.offsetTop;
            console.log(xpost, ypost, "xpost,ypost");
            let seatnum = $(this).attr("data-seatno")
            seatcode = $(this).attr("data-code")
            seatamount = $(this).attr("data-amount")
            let bid = $(this).attr("data-bid")
            console.log(seatnum, seatcode, seatamount, bid, "seatnum,seatcode,seatamount,bid");
            current['code'] = seatcode;
            current['amount'] = seatamount;
            current['bid'] = bid
            console.log(current);
            $(`.${id} .showseat__title`).html(`
            <p class="seat-number">Seat ${seatnum}</p>
            <p class="seat-amount">₹${seatamount}</p>
            `)
            $(`.${id}`).css({ display: "block", top: `${ypost - 10}px`, left: `${xpost + 10 - scroll}px` })
            $(`.${id}`).find(".paxseat").attr('data-seat', seatcode)
            $(`.${id}`).find(".paxseat").attr('data-amount', seatamount)
        })
        $(".seat-layout").scroll(function () {
            if (click) {
                scroll = $(this).scrollLeft()
                let id = $(this).attr("data-id")
                $(`.showseat${id}`).css({ display: "block", top: `${ypost - 10}px`, left: `${xpost + 10 - scroll}px` })
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

    renderseat() {
        /**
         * Generate HTML markup for displaying the list of passengers and their corresponding seat details.
         * @param {string} bid - The flight booking ID.
         * @returns {string} - The generated HTML markup.
         */
        const seatperson = (bid) => {
            return `<ul>${Object.keys(this.paxobj).map((el) => {
                return `
          <li style="padding:1em 0.5em;border-bottom: 1px solid gray;" class="${el}${bid}">
            <div class="n-chk" class="${bid}">
              <label style="display:flex;align-items:center;justify-content: space-between;" class="new-control mr-0 new-checkbox new-checkbox-rounded checkbox-success">
                <input type="checkbox" class="new-control-input paxseat" data-bid="${bid}" data-person="${el}">
                <span class="new-control-indicator" style="top:-3px;"></span>${el.replace("_", " ")}
                <div class="seat-details">
                  ${this.paxobj[el][bid] ? `<small class="seat-number">${pax[el][bid]['code']}</small> <small class="">₹${pax[el][bid]['amount']}</small>` : ""}
                </div>
              </label>
            </div>
          </li>
        `;
            }).join("")
                }</ul>`;
        }

        // Generate HTML markup for each seat map
        let render = Object.keys(this.seatmap).map((el, inx) => {
            return this.seatmap[el].map((it, i) => {
                console.log(this.seatmap);
                let row = 0;
                if (it['seatmap']) {
                    row = it['seatmap']['column'];
                }

                // Generate HTML markup for each seat map section
                return `
                    <div class="tab-pane fade ${inx == 0 && i == 0 ? "show active" : ""}" id="${i}seat" role="tabpanel" aria-labelledby="justify-pills-contact-tab">
                        <div class="seat-booking" style="position:relative;">
                            <div id="showseat" class="showseat showseat${it.bid}" tabindex="102" data-id="${inx + i}">
                                <div class="showseat__title">
                                    <p class="seat-number">Seat 6F</p>
                                    <p class="seat-amount">₹300</p>
                                </div>
                                <div id="changeseat${it.bid}">
                                    ${seatperson(it.bid)}
                                </div>
                                </div>
                                <div class="cn-st cn-st${inx + i} cn-st${it.bid}" tabindex="100" data-id="${inx + i}">
                                <div id="seat-layout" data-id="${inx + i}" class="seat-layout" style="grid-template-rows: repeat(auto-fill, 35px);">
                                    ${this.seatloc(it, el, (i + inx))}
                                </div>
                            </div>
                            <ul class="seat-info">
                                <li style="background-image:url(/static/main/images/icon/seat/available.png);">Free Seat</li>
                                <li style="background-image:url(/static/main/images/icon/seat/booked.png);">Booked Seat</li>
                                <li style="background-image:url(/static/main/images/icon/seat/selected.png);">Paid Seat</li>
                            </ul>
                        </div>
                    </div>
                `;
            }).join("");
        }).join("");

        // Combine all the generated HTML markup and append it to the DOM
        let renddata = `
        <ul class="nav nav-pills mb-3 mt-3 nav-fill" id="justify-pills-tab" role="tablist">
        ${this.seattag()}
        </ul>
        <div class="tab-content" id="justify-pills-tabContent">
        ${render}
        </div> `;
        $('#border-top-contact').html("");
        $('#border-top-contact').append(renddata);

        // Perform seat check functionality
        this.seatcheck();
    }


    paxobjsetter() {
        let adtCount = 0; // Counter for ADT passengers
        let cnnCount = 0; // Counter for CNN passengers
        console.log(this.paxinfo);
        if (Array.isArray(this.paxinfo)) {
            for (const traveler of this.paxinfo) {
                if (traveler["common_v52_0:Name"]) {
                    if (traveler.Code === "ADT") {
                        adtCount++;
                    } else if (traveler.Code === "CNN") {
                        cnnCount++;
                    }
                }
            }
        } else if (typeof this.paxinfo === "object") {
            if (this.paxinfo["common_v52_0:Name"]) {
                if (this.paxinfo.Code === "ADT") {
                    adtCount++;
                } else if (this.paxinfo.Code === "CNN") {
                    cnnCount++;
                }
            }
        }

        for (let i = 1; i <= adtCount; i++) {
            this.paxobj[`ADT_${i}`] = {};
        }

        for (let i = 1; i <= cnnCount; i++) {
            this.paxobj[`CNN_${i}`] = {};
        }

        console.log(this.paxobj);
    }


    seatdata() {
        if (!this.seatmap) {
            $.ajax({
                type: "GET",
                url: "/flight/select_gds_seat/",
                contentType: "application/json",
                dataType: 'json',
                success: (res) => {
                    console.log(res, "response");
                    try {
                        if (!res['errors']) {
                            this.seatmap = res["SOAP:Envelope"]?.["SOAP:Body"]?.["air:SeatMapRsp"];
                            let newdata = {};
                            if (!Array.isArray(this.seatmap)) {
                                this.seatmap = [this.seatmap]; // Create an array with the single object
                            }
                            this.seatmap.forEach((el) => {
                                let data = [el["air:AirSegment"]].map((itm) => {
                                    return {
                                        'bid': itm['FlightNumber'],
                                        'route': `${itm.Origin}-${itm.Destination}`,
                                        'seatmap': {
                                            "row": el["air:OptionalServices"]["air:OptionalService"].length,
                                            "column": el["air:Rows"]["air:Row"].length,
                                            'air:OptionalServices': el["air:OptionalServices"],
                                            'air:Rows': el["air:Rows"],
                                        },
                                    };
                                });
                                newdata['ONWARD'] = data;
                            });
                            this.seatmap = newdata;
                            console.log(this.seatmap);
                            this.renderseat();
                        } else {
                            $('#border-top-contact').html(`<h5 style="color:red;">Seat Map is unavailable on this flight</h5>`);
                        }
                    } catch (error) {
                        $('#border-top-contact').html(`<h5 style="color:red;">Seat Map is unavailable on this flight</h5>`);
                    }
                },
            });
        } else {
            this.renderseat();
        }
    }

    dataset() {
        this.meal = {
            "ONWARD": [this.trip.filter((item) => item.Type === "Meal")]
          };
        this.bagg = {
            "ONWARD": [this.trip.filter((item) => item.Type === "Baggage")]
          };

          this.tripinfo["ONWARD"] = [`${this.airSegment.Origin}-${this.airSegment.Destination}`];

        console.log(this.tripinfo);
    }

    baggtag() {
        console.log(this.tripinfo,"mmmmmmmmm");
        return Object.keys(this.bagg).filter(it => this.bagg[it][0]).map((el, inx) => {
            return `
                <li class="nav-item">
                    <a class="nav-link ${inx == 0 ? "active" : ""}" id="justify-pills-home-tab" data-toggle="pill" href="#bagg${Object.keys(this.tripinfo)[inx]}" role="tab" aria-controls="justify-pills-home" aria-selected="${inx == 0}">${Object.keys(this.tripinfo)[inx]}</a>
                </li>
                `
        }).join("")
    }

    slider() {
        let func = this.test
        let select = this.selection
        let bagselect = this.bagselection
        Object.values(this.meal).map((el, inx) => {
            el.map((itm, i) => {                
                this.rel.find(`#recipeCarousel${Object.keys(this.meal)[inx]}${i}`).carousel({
                    interval: 1000000
                })
            })
        })
        Object.values(this.bagg).map((el, inx) => {
            el.map((itm, i) => {                
                this.rel.find(`#bagg${Object.keys(this.bagg)[inx]}0`).carousel({
                    interval: 1000000
                })
            })
        })
        $('.carousel1 .carousel-item').each(function () {
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
                $(this).change(function () {
                    console.log(this)
                    $(`#${id} label`).removeClass('select')
                    $(`label[for="${$(this).attr('id')}"]`).addClass('select')
                    select[$(this).attr('data-way')] = {
                        "code": $(this).attr('data-code'),
                        "amount": $(this).attr('data-amount'),
                        "route": $(this).attr('data-route'),
                        "bid": $(this).attr('data-bid'),
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
            
            for (var i=0;i<minPerSlide;i++) {
                next=next.next();
                if (!next.length) {
                    next = $(this).siblings(':first');
                }
                
                next.children(':first-child').clone().appendTo($(this));
            }
            $(this).find(`[name="options"]`).map(function () {
                $(this).change(function () {
                    console.log(this)
                    $(`#${id} label`).removeClass('select')
                    $(`label[for="${$(this).attr('id')}"]`).addClass('select')
                    bagselect[$(this).attr('data-way')] = {
                        "code": $(this).attr('data-code'),
                        "amount": $(this).attr('data-amount'),
                        "bid": $(this).attr('data-bid'),
                    }
                    console.log(bagselect)
                    func()
                })
            })
        });
    }

    baggselector(route, way) {
        console.log(route)
        return route.map((el , index) => {
            return `
            <div class="carousel-item ${index == 0 ? "active" : ""}">
                <div class="col-md-4">
                    <div class="card card-body p-0">
                    <div class="service-item">
                        <span class="food-type veg"></span>
                        <img class="img-fluid" src="/static/main/images/icon/bags/3.png">
                        <div class="info-sec">
                            <p class="m-0"><b>${el.ServiceSubCode}</b></p>
                            <p class="m-0">${el.TotalWeight}</p>
                            <p class="small">₹
                            ${el.TotalPrice}
                            </p>
                            <input id="option${way}${index}" name="options" data-way=${way} data-amount=${el.TotalPrice} data-code=${el.ServiceSubCode} data-bid=${el.ProviderCode} type="radio" class="btn-check hidden" autocomplete="off" value="${el.TotalPrice}">
                            <label class="btn btn-secondary m-0" for="option${way}${index}" style="margin-left:-11px;">
                            <span class="label">Select</span>
                            </label>
                        </div>
                    </div>
                    </div>
                </div>
            </div>
            `;
        }).join("")
    }

    baggrend() {
        console.log(this.bagg)
        let data = Object.values(this.bagg).filter(it => it[0]).map((el, inx) => {
            return `
                <div class="tab-pane fade ${inx == 0 ? "show active" : ""}" id="bagg${Object.keys(this.tripinfo)[inx]}" role="tabpanel" aria-labelledby="justify-pills-home-tab">
                <div class="container text-center my-3">
                <div class="row mx-auto my-auto">
                    <div id="bagg${Object.keys(this.bagg)[inx]}0" class="carousel carousel2 slide w-100" data-ride="carousel">
                    <div class="carousel-inner w-100" role="listbox">
                    ${this.baggselector(el[0], Object.keys(this.bagg)[inx])}
                    </div>
                        <a class="carousel-control-prev w-auto" href="#bagg${Object.keys(this.bagg)[inx]}0" role="button" data-slide="prev">
                            <span class="carousel-control-prev-icon bg-dark border border-dark p-2" aria-hidden="true"></span>
                            <span class="sr-only">Previous</span>
                        </a>
                        <a class="carousel-control-next w-auto" href="#bagg${Object.keys(this.bagg)[inx]}0" role="button" data-slide="next">
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

    rend() {
        this.dataset()
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