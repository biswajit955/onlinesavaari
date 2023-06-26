class Service {
    constructor(obj, renderel, person) {
        console.log(obj);
        this.paxinfo = obj.searchQuery.paxInfo;
        this.paxobj = {};
        this.routedata = obj.tripInfos.map(el => {
            return {
                airdetails: el.sI[0]['fD'],
                da: el.sI[0]['da'],
                dt: el.sI[0]['dt'],
                aa: el.sI[el.sI.length - 1]['aa'],
                at: el.sI[el.sI.length - 1]['at'],
            }
        })
        this.bookingId = obj.bookingId;
        this.routeinfo = obj.searchQuery.routeInfos;
        this.trip = obj.tripInfos;
        this.rel = renderel;
        this.route = ['ONWARD', 'RETURN', "2", "3", "4"];
        this.meal = {};
        this.bagg = {};
        this.tripinfo = {};
        this.selection = {};
        this.bagselection = {};
        this.person = person;
        this.insurance = 0;
        this.seatmap;
        this.amount = $('input[name="amount"]').val()
        this.apiamount= $('input[name="apiamount"]').val()
        this.test = (check) => {
            let totalamount = parseFloat(this.amount);
            let totalapiamount = parseFloat(this.apiamount);
            console.log(this.bagselection, this.selection)
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
                console.log(amount)
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
            console.log($('input[name="amount"]').val(), $('input[name="apiamount"]').val())
        }
    }

    paxobjsetter() {
        for (const [k, v] of Object.entries(this.paxinfo)) {
            for (let i = 1; i <= v; i++){
                this.paxobj[`${k}_${i}`] = {}
            }
        }
        console.log(this.paxobj)
    }

    seatstart(it, el) {
        if (it['seatmap']['sData']) {            
            let row = it['seatmap']['sData']['column']
            console.log(row)
            var r = document.querySelector(':root')
            r.style.setProperty('--grid', (row));
            let col = it['seatmap']['sData']['row']
            let isAsile = true
            return it['seatmap']['sInfo'].filter(el => el.seatPosition.column <= row && el.seatPosition.row == col).map(it => {
                let ws = ""
                if (it["isAisle"] && isAsile) {
                    ws = `<div class="seat-li row-no wt-sp"></div>`
                }
                isAsile && it["isAisle"] ? isAsile = false : isAsile = true
                return `
                <div class="seat-li row-no">
                    ${it.code.split("")[it.code.split("").length - 1]}
                </div>
                ${ws}
                `;
            }).join("")
        }
    }

    seatloc(item, el, showinx) {
        console.log(item)
        if (item['seatmap']['sData']) { 
            let col = item['seatmap']['sData']['column']
            return item['seatmap']['sInfo'].map((it, inx) => {
                return `
                <a data-code=${it.code} data-show="showseat${item.bid}" data-route="${item.route}" data-bid="${item.bid}" data-way="${el}" data-placement="top" class="p-0 grid-cell seatclick" style="position:relative;border: 0; cursor: pointer;grid-column:${it.seatPosition.row};grid-row:${it.seatPosition.column}" type="button" title="${it.seatNo} ${it.amount}" data-animation="true" data-loop="${inx}" data-seatno="${it.seatNo}" data-seatRow="${it.seatPosition.row}" data-seatColumn="${it.seatPosition.column}" data-isBooked="${it.isBooked}" data-isLegroom="${it.isLegroom || false}" data-amount="${it.amount}" ${!it.isBooked ? `class="availableSeat" data-selected="false"` : "" }>
                <img src=${it.isBooked ? "/static/main/images/icon/seat/booked.png" : "/static/main/images/icon/seat/available.png"} />
                </a>
                `;
            }).join("")
        } else {
            return `${item['seatmap']['nt']}`
        }
    }

    seatchangerender(bid, code, amount, per, bool) {
        console.log(code, amount, per, bool)
        console.log(Object.keys(this.paxobj).map(el => this.paxobj[el][bid] ? this.paxobj[el][bid]['code'] == per['code'] : false))
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

    renderseat() {
        const seatperson = (bid) => {
            return `<ul>${
                Object.keys(this.paxobj).map((el) => {
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
            }</ul>`

        }
        let render = Object.keys(this.seatmap).map((el, inx) => {
            return this.seatmap[el].map((it, i) => {
                let row = 0
                if (it['seatmap']['sData']) { 
                    row = it['seatmap']['sData']['column']
                }              
                return `
                <div class="tab-pane fade ${inx == 0 && i == 0 ? "show active" : ""}" id="${Object.keys(this.tripinfo)[inx]}${i}seat" role="tabpanel" aria-labelledby="justify-pills-contact-tab">
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
                                ${this.seatloc(it, el, (i+inx))}
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
            }).join("")
        }).join("")
        let renddata = `
        <ul class="nav nav-pills mb-3 mt-3 nav-fill" id="justify-pills-tab" role="tablist">
            ${this.seattag()}
        </ul>
        <div class="tab-content" id="justify-pills-tabContent">
        ${render}
        </div>
        `;
        $('#border-top-contact').html("")
        $('#border-top-contact').append(renddata)
        this.seatcheck()
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
            let seatnum = $(this).attr("data-seatno") 
            seatcode = $(this).attr("data-code") 
            seatamount = $(this).attr("data-amount")
            let bid = $(this).attr("data-bid")
            current['code'] = seatcode;
            current['amount'] = seatamount;
            current['bid'] = bid
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
                console.log(bid, person, code, amount)
                console.log("change done")
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
                console.log(paxobj)
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

    seatdata() {
        if (!this.seatmap) {            
            $.ajax({
                type: "GET",
                url: "/flight/select_seat/",
                contentType: "application/json",
                dataType: 'json',
                data: {
                    bookingId:this.bookingId
                },
                success: (res) => {
                    console.log(res)
                    
                    if (!res['errors']) {                        
                        this.seatmap = res;
                        let newdata = {}
                        this.trip.map((el, inx) => {
                            let data = el.sI.map(itm => {
                                return {
                                    'bid': itm.id,
                                    'route': `${itm.da.code}-${itm.aa.code}`
                                }
                            });
                            for (const [k, v] of Object.entries(this.seatmap.tripSeatMap.tripSeat)) {
                                data.map(el => {
                                    if (k == el.bid) {
                                        el['seatmap'] = v
                                    }
                                })
                            }
                            newdata[this.route[inx]] = data
                        })
                        this.seatmap = newdata;
                        console.log(this.seatmap)
                        this.renderseat()
                    } else {
                        $('#border-top-contact').html(`<h5 style="color:red";>${res.errors[0].message}</h5>`)
                    }
                },
            })
        } else {
            console.log(this.seatmap)
            this.renderseat()
        }
    }

    dataset() {
        this.trip.map((el, inx) => {
            if (el.sI[0].ssrInfo) {
                if (el.sI[0].ssrInfo.MEAL) {                    
                    this.meal[this.route[inx]] = el.sI.map(itm => { 
                        let data = itm.ssrInfo.MEAL.map(all => {
                            all['bid'] = itm.id
                            return all
                        })
                        return data
                    })
                }
            }
        });
        console.log(this.trip);
        this.trip.map((el, inx) => {
            if (el.sI[0].ssrInfo) {
                if (el.sI[0].ssrInfo.BAGGAGE) {                    
                    this.bagg[this.route[inx]] = el.sI.map(itm => { 
                        let data = itm.ssrInfo.BAGGAGE.map(all => {
                            all['bid'] = itm.id
                            return all
                        })
                        console.log(data);
                        return data
                    })
                }
            }
        });
        this.trip.map((el, inx) => {
            console.log(inx,"iiii");
            this.tripinfo[this.route[inx]] = el.sI.map(itm => `${itm.da.code}-${itm.aa.code}`);
        })
        console.log(this.tripinfo);
    }

    mealtag() {
        return Object.values(this.tripinfo).map((el, inx) => {
            return el.map((route, i) => {
                return `
                <li class="nav-item">
                    <a class="nav-link ${inx == 0 && i == 0 ? "active" : ""}" id="justify-pills-home-tab" data-toggle="pill" href="#${Object.keys(this.tripinfo)[inx]}${i}" role="tab" aria-controls="justify-pills-home" aria-selected="${inx == 0 && i == 0}">${Object.keys(this.tripinfo)[inx]}: ${route}</a>
                </li>
                `
            }).join("")
        }).join("")
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

    routerend(route, way, inx, i) {
        return route.map((el , index) => {
            return `
            <div class="carousel-item ${index == 0 ? "active" : ""}">
                <div class="col-md-4">
                    <div class="card card-body p-0">
                    <div class="service-item">
                        <span class="food-type veg"></span>
                        <img class="img-fluid" src="/static/main/images/icon/food/3.png">
                        <div class="info-sec">
                            <p class="m-0"><b>${el.code}</b></p>
                            <p class="m-0">${el.desc}</p>
                            <p class="small">₹
                            ${el.amount || "Free Meal"}
                            </p>
                            <input data-bid=${el.bid} data-route=${this.tripinfo[way][inx]} data-way=${way}${inx} data-amount=${el.amount ? el.amount * this.person : 0 } data-code=${el.code} type="radio" class="btn-check hidden" name="options" id="option${index}${inx}${i}" autocomplete="off" value="${el.code}">
                            <label class="btn btn-secondary m-0" for="option${index}${inx}${i}" style="margin-left:-11px;">
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
    mealrend() {
        let data = Object.values(this.meal).map((el, inx) => {
            return el.map((route, i) => {
                return `
                <div class="tab-pane fade ${inx == 0 && i == 0 ? "show active" : ""}" id="${Object.keys(this.meal)[inx]}${i}" role="tabpanel" aria-labelledby="justify-pills-home-tab">
                <div class="container text-center my-3">
                <div class="row mx-auto my-auto">
                    <div id="recipeCarousel${Object.keys(this.meal)[inx]}${i}" class="carousel carousel1 slide w-100" data-ride="carousel">
                    <div class="carousel-inner w-100" role="listbox">
                    ${this.routerend(route, Object.keys(this.meal)[inx], i, inx)}
                    </div>
                        <a class="carousel-control-prev w-auto" href="#recipeCarousel${Object.keys(this.meal)[inx]}${i}" role="button" data-slide="prev">
                            <span class="carousel-control-prev-icon bg-dark border border-dark p-2" aria-hidden="true"></span>
                            <span class="sr-only">Previous</span>
                        </a>
                        <a class="carousel-control-next w-auto" href="#recipeCarousel${Object.keys(this.meal)[inx]}${i}" role="button" data-slide="next">
                            <span class="carousel-control-next-icon bg-dark border border-dark p-2" aria-hidden="true"></span>
                            <span class="sr-only">Next</span>
                        </a>
                    </div>
                </div>
            </div>
                </div>
                `
            }).join("")
        }).join("")
        return `
        <div class="tab-content" id="justify-pills-tabContent">
        ${data}   
        </div>
        `
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
                            <p class="m-0"><b>${el.code}</b></p>
                            <p class="m-0">${el.desc}</p>
                            <p class="small">₹
                            ${el.amount}
                            </p>
                            <input id="option${way}${index}" name="options" data-way=${way} data-amount=${el.amount} data-code=${el.code} data-bid=${el.bid} type="radio" class="btn-check hidden" autocomplete="off" value="${el.code}">
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



// class Service {
//     constructor(obj, renderel, person) {
//         this.paxinfo = obj["SOAP:Envelope"]?.["SOAP:Body"]?.["air:AirMerchandisingOfferAvailabilityRsp"]?.["air:AirSolution"]?.["air:SearchTraveler"] ?? [];
//         console.log(this.paxinfo);
//         this.paxobj = {};
//         this.rel = renderel;
//         this.seatmap;
//         this.insurance = 0;
//         this.amount = $('input[name="amount"]').val()
//         this.apiamount = $('input[name="apiamount"]').val()
//         this.route = ['ONWARD', 'RETURN', "2", "3", "4"];
//         this.bagg = {};
//         this.trip = obj["SOAP:Envelope"]?.["SOAP:Body"]?.["air:AirMerchandisingOfferAvailabilityRsp"]?.["air:OptionalServices"]?.["air:OptionalService"] ?? [];
//         console.log(this.trip);