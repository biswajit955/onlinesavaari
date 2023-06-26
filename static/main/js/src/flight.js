export class Renderflight {
    constructor(obj, el, url, usertype = 'None', token) {
        this.all_com = obj.comm.filter(el => el.airline_type.includes('All'))
        this.err = { mes: "" };
        this.gds_ref = obj.gds_ref;
        this.spice_token = obj.spice_token;
        this.akasa_token = obj.akasa_token;
        this.person = obj.Person;
        this.child = obj.child;
        this.adult = obj.adult;
        this.infant = obj.infant;
        this.radio1 = obj.radio1;
        this.tocode = obj.toCityOrAirport;
        this.fromcode = obj.fromCityOrAirport;
        this.usertype = usertype;
        this.search_request = obj.search_request;
        this.oldarr = obj.data.searchResult.tripInfos;
        this.type = Object.keys(obj.data.searchResult.tripInfos);
        this.renderel = el;
        this.sortlist = { sort_arrive: false, sort_depart: false, sort_duration: false, sort_price: true };
        this.lastchange = false;
        this.url = url;
        this.sdata = obj.search_sdata || {};
        this.trip = !(this.type.length == 1) ? this.oldarr : !this.sdata['data'] ? Object.values(this.oldarr)[0] : (Object.values(this.oldarr)[0].map((el, id) => {
            let change = this.sdata.data.find(it => it.flight_number.includes(el.sI[0].fD.fN) && it.flight_number.includes(el.sI[0].fD.aI.code))
            if (change) {
                console.log(id)
                let obj = {
                    "fd": {
                        "ADULT": {
                            "fC": {
                                "TAF": 302,
                                "NCM": 159.43,
                                "TF": change.price,
                                "NF": 11903.27,
                                "BF": change.price
                            },
                            "afC": {
                                "TAF": {
                                    "YR": 340,
                                    "MF": 15,
                                    "MFT": 2.7,
                                    "OT": 390,
                                    "AGST": 555
                                },
                                "NCM": {
                                    "TDS": -8.39,
                                    "OT": 167.82
                                }
                            },
                            "sR": 6,
                            "bI": {
                                "iB": "15 Kg",
                                "cB": "7 Kg"
                            },
                            "rT": 1,
                            "cc": "ECONOMY",
                            "cB": "G",
                            "fB": "GIP",
                            "mI": false
                        }
                    },
                    "fareIdentifier": "series",
                    "id": `${change.ticket_id}`,
                    "msri": [],
                    "messages": [],
                    "tai": {
                        "tbi": {
                            "557": [
                                {
                                    "ADULT": {
                                        "iB": "15 Kg",
                                        "cB": "7 Kg"
                                    }
                                }
                            ],
                            "558": [
                                {
                                    "ADULT": {
                                        "iB": "15 Kg",
                                        "cB": "7 Kg"
                                    }
                                }
                            ]
                        }
                    }
                }
                el.totalPriceList.push(obj)
            }
            return el
        }))
        this.token = token.token
        this.akasa_fare =  obj['akasaa_data'] ? obj['akasaa_data']['data'] ? Object.values(obj.akasaa_data.data.faresAvailable) : [] : []
        this.corp = !this.usertype ? ['COUPON', 'SME', 'CORPORATE', 'CORP_CONNECT', 'OFFER_FARE_WITHOUT_PNR', 'TACTICAL'] : [];
        this.norefund = ['OFFER_FARE_WITHOUT_PNR', 'series']
        this.afterfl = this.type.length == 1 ? this.trip : { ...this.trip }
        this.akasa_data = (obj['akasaa_data'] && obj['akasaa_data']['data']) ? obj['akasaa_data']['data']['results'][0]['trips'].length > 0 ? Object.values(obj.akasaa_data.data.results[0].trips[0].journeysAvailableByMarket)[0] : [] : [];
        this.test = () => {
            if (this.akasa_data.length > 0) {
                this.trip.push(...this.akasa_data.map(el => {
                    let fkey = el.fares.map(el => el.fareAvailabilityKey);
                    return {
                        "comm": false,
                        "sI": el.segments.map(it => {
                            return {
                                "skey": it.segmentKey,
                                "id": "akasa",
                                "fD": {
                                    "aI": {
                                        "code": it.identifier.carrierCode,
                                        "name": "Akasa Air",
                                        "isLcc": true
                                    },
                                    "fN": it.identifier.identifier,
                                    "eT": "7MA"
                                },
                                "stops": it.stops,
                                "duration": 130,
                                "da": {
                                    "code": it.designator.origin,
                                    "name": it.legs[0].designator.origin,
                                    "cityCode": it.designator.origin,
                                    "city": it.legs[0].designator.origin,
                                    "country": "",
                                    "countryCode": "IN",
                                    "terminal": ""
                                },
                                "aa": {
                                    "code": it.designator.destination,
                                    "name":  it.legs[0].designator.destination,
                                    "cityCode": it.designator.destination,
                                    "city": "Mumbai",
                                    "country": "India",
                                    "countryCode": "IN",
                                    "terminal": "Terminal T1"
                                },
                                "dt": it.designator.departure,
                                "at": it.designator.arrival,
                                "iand": false,
                                "isRs": false,
                                "sN": el.stops,
                            }
                        }),
                        "totalPriceList": this.akasa_fare.filter(it => fkey.includes(it.fareAvailabilityKey)).map(item => {
                        let price = item.fares[0].passengerFares[0].fareAmount + obj['markup_akasa']
                            return {
                                "fd": {
                                    "ADULT": {
                                        "fC": {
                                            "BF": item.fares[0].passengerFares[0].serviceCharges[0].amount,
                                            "NCM": 32.57,
                                            "TF": price,
                                            "TAF": item.fares[0].passengerFares[0].serviceCharges[1].amount,
                                            "NF": 4870.13
                                        },
                                        "afC": {
                                            "NCM": {
                                                "TDS": -1.71,
                                                "OT": 34.28
                                            },
                                            "TAF": {
                                                "MF": 15,
                                                "AGST": 216,
                                                "OT": 489,
                                                "MFT": 2.7
                                            }
                                        },
                                        "sR": el.fares.find(e => e.fareAvailabilityKey == item.fareAvailabilityKey)['details'][0]['availableCount'],
                                        "bI": {
                                            "iB": "15 Kg",
                                            "cB": "7 Kg"
                                        },
                                        "rT": 1,
                                        "cc": "ECONOMY",
                                        "cB": "SP",
                                        "fB": "Z2O7MBIX",
                                        "mI": false
                                    }
                                },
                                "fareIdentifier": item.fares[0]['productClass'],
                                "id": el.journeyKey,
                                "fkey": item.fareAvailabilityKey,
                                "msri": [],
                                "tai": {
                                    "tbi": {
                                        "444": [
                                            {
                                                "ADULT": {
                                                    "iB": "15 Kg",
                                                    "cB": "7 Kg"
                                                }
                                            }
                                        ]
                                    }
                                }
                            }
                        })
                    }
                }))
            }
        }
        this.gds = !!obj['gds_data']
        this.gds_fare = !this.gds || obj['gds_data']['SOAP:Envelope']['SOAP:Body']['air:LowFareSearchRsp']['air:AirPricingSolution']
        this.gds_seg = !this.gds || obj['gds_data']['SOAP:Envelope']['SOAP:Body']['air:LowFareSearchRsp']['air:AirSegmentList']['air:AirSegment']
        this.gds_data = !this.gds || this.trip.splice(1, 0, ...this.gds_fare.map(el => {
            console.log(el)
            let si = Object.values(el['air:Journey']['air:AirSegmentRef']).map(it => {
                let data = this.gds_seg.find(el => el.Key == it)
                let newdata = data
                if (data) {                    
                    newdata = {}
                    for (let i in data) {
                        if (typeof(data[i]) != 'object') {
                            newdata[i] = data[i]
                        }
                    }
                }
                return newdata
            }).filter(it => it);
            if (si.length > 0) { 
                console.log(si)
                si = si.map(it => { 
                    it['ProviderCode'] = '1G'
                    return it
                })
                return {
                    "test": "this is gds",
                    "text": true,
                    "sI": si.map(it => {
                        return {
                            "skey": JSON.stringify(it),
                            "id": "GDS",
                            "fD": {
                                "aI": {
                                    "code": it.Carrier,
                                    "name": it.Carrier,
                                    "isLcc": true
                                },
                                "fN": it.FlightNumber,
                                "eT": "7MA"
                            },
                            "stops": 0,
                            "duration": it.FlightTime,
                            "da": {
                                "code": it.Origin,
                                "name": it.Origin,
                                "cityCode": it.Origin,
                                "city": it.Origin,
                                "country": "",
                                "countryCode": "IN",
                                "terminal": ""
                            },
                            "aa": {
                                "code": it.Destination,
                                "name":  it.Destination,
                                "cityCode": it.Destination,
                                "city": it.Destination,
                                "country": "India",
                                "countryCode": "IN",
                                "terminal": "Terminal T1"
                            },
                            "dt": it.DepartureTime.replace(":00.000+05:30", ""),
                            "at": it.ArrivalTime.replace(":00.000+05:30", ""),
                            "iand": false,
                            "isRs": false,
                            "sN": 0
                        }
                    }),
                    "totalPriceList":[{
                            "fd": {
                                "ADULT": {
                                    "fC": {
                                        "BF": parseFloat(el.BasePrice.replace("INR", "")),
                                        "NCM": 32.57,
                                        "TF": Array.isArray(el['air:AirPricingInfo']) ? parseFloat(el['air:AirPricingInfo'][0].TotalPrice.replace("INR", "")) : parseFloat(el['air:AirPricingInfo'].TotalPrice.replace("INR", "")),
                                        "TAF": parseFloat(el.Taxes.replace("INR", "")),
                                        "NF": 4870.13
                                    },
                                    "afC": {
                                        "NCM": {
                                            "TDS": -1.71,
                                            "OT": 34.28
                                        },
                                        "TAF": {
                                            "MF": 15,
                                            "AGST": 216,
                                            "OT": 489,
                                            "MFT": 2.7
                                        }
                                    },
                                    "sR": 0,
                                    "bI": {
                                        "iB": "15 Kg",
                                        "cB": "7 Kg"
                                    },
                                    "rT": 1,
                                    "cc": 0,
                                    "cB": "SP",
                                    "fB": "Z2O7MBIX",
                                    "mI": false
                                }
                            },
                            "fareIdentifier": "GDS",
                            "id": el.key,
                            "msri": [],
                            "tai": {
                                "tbi": {
                                    "444": [
                                        {
                                            "ADULT": {
                                                "iB": "15 Kg",
                                                "cB": "7 Kg"
                                            }
                                        }
                                    ]
                                }
                            }
                        }]
                    }
            }
            return null
        }).filter(el => !!el))
        this.checkspice = (obj) => {
            if ((obj['Journeys']['Journey'].length > 0) || (!Array.isArray(obj['Journeys']['Journey']))) {
                if (!Array.isArray(obj['Journeys']['Journey'])) {
                    obj.Journeys.Journey = [obj.Journeys.Journey]
                }
                let data = obj.Journeys.Journey.map(el => {
                    let seg = el.Segments.Segment
                    if (!Array.isArray(seg)) {
                        seg = [seg]
                    }
                    if (seg[0]['Fares']) {                        
                        let si = seg.map(it => { 
                            return {
                                    "skey": it.SegmentSellKey,
                                    "STD": it.STD,
                                    "ActionStatusCode": it.ActionStatusCode,
                                    "id": "Spicejet",
                                    "fD": {
                                        "aI": {
                                            "code": it.FlightDesignator["a:CarrierCode"],
                                            "name": "SpiceJet",
                                            "isLcc": true
                                        },
                                        "fN": it.FlightDesignator["a:FlightNumber"],
                                        "eT": "7MA"
                                    },
                                    "stops": 0,
                                    "duration": 130,
                                    "da": {
                                        "code": it.DepartureStation,
                                        "name": it.DepartureStation,
                                        "cityCode": it.DepartureStation,
                                        "city": it.DepartureStation,
                                        "country": "",
                                        "countryCode": "IN",
                                        "terminal": ""
                                    },
                                    "aa": {
                                        "code": it.ArrivalStation,
                                        "name": it.ArrivalStation,
                                        "cityCode": it.ArrivalStation,
                                        "city": "Mumbai",
                                        "country": "India",
                                        "countryCode": "IN",
                                        "terminal": "Terminal T1"
                                    },
                                    "dt": it.STD,
                                    "at": it.STA,
                                    "iand": false,
                                    "isRs": false,
                                    "sN": 0
                            }
                        })
                        let fares = seg[0]["Fares"]["Fare"]
                        if (!Array.isArray(fares)) {
                            fares = [fares]
                        }
                        let air = {
                            "jkey": el.JourneySellKey,
                            "text": true,
                            "sI": si,
                            "totalPriceList": fares.map(e => {
                                let fare = e.PaxFares.PaxFare
                                if (Array.isArray(fare)) {
                                    fare = e.PaxFares.PaxFare[0]
                                }
                                return {
                                    "fd": {
                                        "ADULT": {
                                            "fC": {
                                                "BF": parseFloat(fare.ServiceCharges.BookingServiceCharge[0].Amount),
                                                "TAF": parseFloat(fare.ServiceCharges.BookingServiceCharge[1].Amount),
                                                "TF": parseFloat(fare.ServiceCharges.BookingServiceCharge[0].Amount) + parseFloat(fare.ServiceCharges.BookingServiceCharge[1].Amount),
                                                "NF": 16819.7
                                            },
                                            "afC": {
                                                "TAF": {
                                                    "OT": 1277,
                                                    "MFT": 2.7,
                                                    "MF": 15,
                                                    "YQ": 750
                                                }
                                            },
                                            "sR": 43,
                                            "bI": {
                                                "iB": "15 Kg",
                                                "cB": "7 Kg"
                                            },
                                            "rT": 1,
                                            "cc": "ECONOMY",
                                            "cB": "GS",
                                            "fB": "AO9RBINE",
                                            "mI": false
                                        }
                                    },
                                    "fareIdentifier": "spicejet",
                                    "id": e.FareSellKey,
                                    "msri": [],
                                    "tai": {
                                        "tbi": {
                                            "111": [
                                                {
                                                    "ADULT": {
                                                        "iB": "15 Kg",
                                                        "cB": "7 Kg"
                                                    }
                                                }
                                            ]
                                        }
                                    }
                                }
                            })
                        }
                        return air
                    }
                })
                data = data.filter(el => el)
                console.log(data)
                const newArray = [].concat(...data)
                this.trip.splice(1, 0, ...newArray)                        
            }
        }
    }
    // this.sdata.find(it => it.flight_number.includes(el.sI[0].fD.fN) && it.flight_number.includes(el.sI[0].fD.aI.code))
    filter(value, obj) {
        if (this.type.length == 1) {            
            let trip = this.trip;
            let p = (value['price'].split(' - ')).map(pr => parseFloat(pr.replace('₹', "")))
            trip = trip.filter(a => {
                let el_a = a.totalPriceList[0].fd.ADULT.fC.TF;
                return ((el_a >= p[0]) && (el_a <= p[1]));
            })
    
            let t = value['fl_time'] ? value['fl_time'].map(el => el.split(' - ').map(it => parseInt(it.split(':')[0]))) : false;
    
            !t || console.log(t) 
            // console.log((new Date(trip[0].sI[0].dt)).getHours())
    
            let s = value['fl_stop'] ? value['fl_stop'].map(el => parseInt(el)) : false
            !s || (trip = trip.filter(st => s.includes(st.sI[st.sI.length - 1].sN)))
    
            let a = value['airline']
            !a || (trip = trip.filter(air => a.includes(air.sI[0].fD.aI.name)))
    
            this.afterfl = trip
            console.log('test')
            console.log(trip)
            this.sortrend(trip, false)
        } else {
            let tripr = Object.values(this.trip)
            let keys = Object.keys(this.trip)
            for (let i = 0; i < tripr.length; i++) {
                let trip = tripr[i]
                let key = keys[i]
                let p = (value['price'].split(' - ')).map(pr => parseFloat(pr.replace('₹', "")))
                trip = trip.filter(a => {
                    let el_a = a.totalPriceList[0].fd.ADULT.fC.TF;
                    return ((el_a >= p[0]) && (el_a <= p[1]));
                })
                
                let t = value['fl_time'] ? value['fl_time'].map(el => el.split(' - ').map(it => parseInt(it.split(':')[0]))) : false;
                
                // !t || (trip = trip.filter(a => (new Date(a.sI[0].dt)).getHours() >= t[0]) 
                // console.log((new Date(trip[0].sI[0].dt)).getHours())
                
                let s = value['fl_stop'] ? value['fl_stop'].map(el => parseInt(el)) : false
                !s || (trip = trip.filter(st => s.includes(st.sI[st.sI.length - 1].sN)))
                
                let a = value['airline']
                !a || (trip = trip.filter(air => a.includes(air.sI[0].fD.aI.name)))
                
                this.afterfl[Object.keys(this.afterfl)[i]] = trip
                console.log('test')
                this.sortrend(trip, key)
                console.log(trip, keys, this.afterfl, this.trip)
            }
        }
        $('body').removeClass('overflown');
        $(".listing-filter").removeClass("active");
        this.checkchecker()
    }

    minmaxp() {
        let min;
        let max;
        if (this.type.length == 1) {
            max = Math.max.apply(Math, this.trip.map(it => it.totalPriceList[0].fd.ADULT.fC.TF))
            min = Math.min.apply(Math, this.trip.map(it => it.totalPriceList[0].fd.ADULT.fC.TF))
        }
        else {
            max = Math.max(...Object.values(this.trip).map(el => {
                return Math.max.apply(Math, el.map(it => {
                    return it.totalPriceList[0].fd.ADULT.fC.TF
                }))
            }));
            min = Math.min(...Object.values(this.trip).map(el => {
                return Math.min.apply(Math, el.map(it => {
                    return it.totalPriceList[0].fd.ADULT.fC.TF
                }))
            }));
        }
        return [min, max]
    }
    allairline() {
        let allair = Object.values(this.oldarr).reduce((arr, data) => {
            data.map(el => {
                arr.push(...el.sI.map(item => item.fD.aI.name))
            })
            arr.push("SpiceJet")
            return arr
        }, []).reduce(function(obj, item) {
            if (!obj[item]) {
              obj[item] = 0;
            }
            obj[item]++;
            return obj;
        }, {});
        console.log(allair)
        return Object.keys(allair)
    }
    sortrender() {
        let typ = this.type;
        let rendit;
        if (typ.length == 1) {
            rendit = `<div class="filter-box">
            <div class="sort-label">Sort By:</div>
            <div class="sort-nav">
                    <div class="s-li" id="sort_depart" data-name=${typ[0]}>
                        <p>DEPART</p>
                    </div>
                    <div class="s-li" id="sort_arrive" data-name=${typ[0]}>
                        <p>ARRIVE</p>
                    </div>
                    <div class="s-li" id="sort_duration" data-name=${typ[0]}>
                        <p>DURATION</p>
                    </div>
            </div>
            <div class="price-filter" id="sort_price" data-name=${typ[0]}>
                <div class="s-li">
                    PRICE PER ADULT
                </div>
            </div>
        </div>
        <div id="fl-render" ></div>`
        } else {
            function divlen() {
                return typ.reverse().map(el => {
                    return `
                    <div class="col-lg-6">
                        <div class="filter-box">
                            <div class="sort-nav">
                                    <div class="s-li" id="sort_depart" data-name=${el}>
                                        <p>DEPART</p>
                                    </div>
                                    <div class="s-li" id="sort_arrive" data-name=${el}>
                                        <p>ARRIVE</p>
                                    </div>
                                    <div class="s-li" id="sort_duration" data-name=${el}>
                                        <p>DURATION</p>
                                    </div>
                            </div>
                            <div class="price-filter" id="sort_price" data-name=${el}>
                                <div class="s-li">
                                    PRICE PER ADULT
                                </div>
                            </div>
                        </div>
                        <div id="fl-render${el}"></div>
                    </div>
                    `
                }).join("")
            }
            rendit = `
            <div class="overflowx">
            <div class="row flex-nowrap">
            ${divlen()}
            </div>
            </div>
            `
        }
        this.renderel.html(rendit)
    }

    findDur(tm) {
        let dt = new Date(tm[0].dt)
		let at = new Date(tm[tm.length - 1].at)
		let min = Math.floor((((at - dt)/1000)%3600)/60)
		let hour = Math.floor(((at - dt)/1000)/3600)
		return `${hour}h ${min}m`
    }
    maproute(v, cc){
        return v.map((el, inx) => `
        ${el['skey'] ? `<input type="hidden" name="skey${inx ? inx : ""}" value='${el.skey}'></input>`: ""}
        ${el['STD'] ? `<input type="hidden" name="STD" value="${el.STD}"></input>` : ""}
        <input type="hidden" name="flight_no${inx == 0? "" : inx}" value="${el.fD.aI.code}"></input>
		<div class="sec1">
			<div class="name">
				<img src="${this.url}${el.fD.aI.code}.png" alt="">
				<div>${el.fD.aI.name},<span>${cc}</span></div>
				<div class="small">${el.STD}</div>
			</div>
			<div class="services">
				<div class="active">
					<i class="la la-cutlery"></i>
				</div>
				<div>
					<i class="la la-wifi"></i>
				</div>
				<div>
					<i class="la la-toilet"></i>
				</div>
				<div>
					<i class="la la-plug"></i>
				</div>
				<div>
					<i class="la la-play"></i>
				</div>
			</div>
		</div>
		<div class="sec2">
			<div class="all-info">
				<div>${ el.da.name }</div>
				<div><b>${el.dt.replace("T", " ")}</b></div>
				<div class="small"><b></b></div>
				<div class="small">${el.da.name},${el.da.terminal}</div>
			</div>
			<div class="total-time small">
				<div>
					<i class="la la-clock"></i>
				</div>
				<div>
					<span></span>
					<i class="la la-plane-departure"></i>
				</div>
				<div>Non Stop</div>
			</div>
			<div class="all-info">
				<div>${ el.aa.name }</div>
				<div><b>${(el.at.replace("T", " "))}</b></div>
				<div class="small"><b></b></div>
				<div class="small">${el.aa.name},${el.aa.terminal}</div>
			</div>
		</div>
		<div class="sec3">
			<div class="packadge">
				
				<div>
					Checkin Baggage:
					<b>
						<i class="la la-suitcase"></i>
					</b>
				</div>
				<div>
					<b>
						<i class="la la-cutlery"></i>
							Free Meal
					</b>
				</div>
			</div>
		</div>
		`).join("")
    }
    
    faredetail(fare) {
        return Object.keys(fare).map(el => {
            return `
            <tr>
                <td>${el}</td>
                <td><i class="la la-rupee"></i><span>${fare[el].fC.BF}</span></td>
                <td><i class="la la-rupee"></i><span>${fare[el].fC.TAF}</span></td>
            </tr>
            `;
        }).join("")
    }

    flightdetails(flight, index){
		return `
        <div id="flights-details${index}" class="flights-details">
        <div class="head-sec">
            <h4 class="m-0">Flight Details</h4>
        </div>
        <div class="body-sec">
            <div class="row">
                <div class="col-lg-8 col-md-7 left-sec">
                    <div class="flight-info">
                    ${this.maproute(flight.sI, flight.totalPriceList[0].fd.ADULT.cc)}
                        </div>
                    </div>
                <div class="col-lg-4 col-md-5 right-sec">
                    <div class="tab-box-two">
                        <ul class="nav nav-pills" role="tablist">
                            <li class="nav-item">
                                <a class="nav-link active" id="tab-one${index}" data-toggle="pill" href="#one-tab${index}" role="tab" aria-controls="one-tab${index}"
                                    aria-selected="true">Fare Summary</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" id="tab-two${index}" data-toggle="pill" href="#two-tab${index}" role="tab" aria-controls="two-tab${index}"
                                    aria-selected="false">Fare
                                    Rules</a>
                            </li>
                        </ul>
                        <div class="tab-content">
                        <div class="tab-pane fade show active" id="one-tab${index}" role="tabpanel" aria-labelledby="tab-one${index}">
                            <table>
                                <thead>
                                    <tr>
                                        <th>Fare Summary</th>
                                        <th>Base Fare</th>
                                        <th>Fees & Taxes</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${this.faredetail(flight.totalPriceList[0].fd)}
                                </tbody>
                            </table>
                            <hr>
                            <div class="total">
                                <div>You Pay:</div>
                                <div><b><i class="la la-rupee"></i><span>${flight.totalPriceList[0].fd.ADULT.fC.TF}</span></b></div>
                            </div>
                            <hr>
                            <p class="small m-0">Note: Total fare displayed above has been rounded off and may show a slight difference from actual
                                fare.</p>
                        </div>

                        <div class="tab-pane fade" id="two-tab${index}" role="tabpanel" aria-labelledby="tab-two${index}">
                            <div class="scrolls">
                                <h4>${flight.sI[0].da.code}-${flight.sI[flight.sI.length - 1].aa.code}</h4>
                                <hr>
                                <p><b>Airline Cancellation Fee</b></p>
                                <table>
                                    <thead>
                                        <tr>
                                            <th>Duration *</th>
                                            <th>Per Passenger</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>0 hour to 2 hours</td>
                                            <td>Non-Refundable</td>
                                        </tr>
                                        <tr>
                                            <td>4 hours to 4 days</td>
                                            <td><i class="la la-rupee"></i> 3,500</td>
                                        </tr>
                                        <tr>
                                            <td>>4 days</td>
                                            <td><i class="la la-rupee"></i> 3,000</td>
                                        </tr>
                                    </tbody>
                                </table>
                                <hr>
                                <p><b>Airline Date Change Fee</b></p>
                                <table>
                                    <thead>
                                        <tr>
                                            <th>Duration *</th>
                                            <th>Per Passenger</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>4 hours to 4 days</td>
                                            <td>Non-Refundable</td>
                                        </tr>
                                        <tr>
                                            <td>4 hours to 4 days</td>
                                            <td><i class="la la-rupee"></i> 3,500</td>
                                        </tr>
                                        <tr>
                                            <td>>4 days</td>
                                            <td><i class="la la-rupee"></i> 3,000</td>
                                        </tr>
                                    </tbody>
                                </table>
                                <div class="bg-text">
                                    <p class="mb-0 small">We would recommend that you reschedule/cancel your tickets atleast 72 hours prior to the
                                        flight
                                        departure
                                    </p>
                                </div>
                                <hr>
                                <p><b>Savari Service Fee*</b></p>
                                <p class="small">(charged per passenger in addition to airline fee as applicable)</p>
                                <table>
                                    <tbody>
                                        <tr>
                                            <td>Online Cancellation Service Fee</td>
                                            <td><i class="la la-rupee"></i> 400</td>
                                        </tr>
                                        <tr>
                                            <td>Offline Cancellation Service Fee</td>
                                            <td><i class="la la-rupee"></i> 400</td>
                                        </tr>
                                        <tr>
                                            <td>Online Rescheduling Service Fee</td>
                                            <td><i class="la la-rupee"></i> 400</td>
                                        </tr>
                                        <tr>
                                            <td>Offline Rescheduling Service Fee</td>
                                            <td><i class="la la-rupee"></i> 1,250</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                            <hr>
                            <p class="small">* Prior to the date/time of departure.</p>
                            <p class="small">**Please note: Savari service fee is over and above the airline cancellation fee due to which refund
                                type
                                may vary.
                            </p>
                        </div>

                        <div class="mt-4">
                            <button type="button" onclick="bookflight('${flight.totalPriceList[0].id}', 'one-way', '${index}','normal');" class="btn btn-block btn-white">Book Now</button>
                        </div>
                    </div>
                    </div>
                </div>
            </div>
        </div>
    </div>`
    }

    tablefare(fare, inx) {
        let corp = this.corp;
        return `<table class="table table-bordered">
            <thead>
                <tr>
                    <th>Services</th>
                    <th>Checked Bag</th>
                    <th>Hand Bag</th>
                    <th>Seat Selection</th>
                    <th>Date Change</th>
                    <th>Cancellation</th>
                    <th>Meal</th>
                    <th>Price</th>
                    <th>Book</th>
                </tr>
            </thead>
            <tbody>
            ${fare.filter(it => !corp.includes(it.fareIdentifier)).sort((x, y) => {
                return x.fd.ADULT.fC.TF - y.fd.ADULT.fC.TF;
            }).map(a => {
                let typ = {
                    'series': 'series',
                    'EC': 'akasa',
                    'AV': 'akasa',
                    'GDS': 'gds',
                }
                let spice = a.fareIdentifier == 'spicejet' ? 'spicejet' : false;
                let type = Object.keys(typ).includes(a.fareIdentifier) ? typ[a.fareIdentifier] : 'normal';
                return `<tr>
                <th scope="row">${a.fareIdentifier}</th>
                <td>${a.fd.ADULT.bI.iB}</td>
                <td>${a.fd.ADULT.bI.cB}</td>
                <td>Extra Charge</td>
                <td>${type == "series" ? "unchangeable" : "Extra Charge"}</td>
                <td>${type == "series" ? "No Refund" : "Extra Charge"}</td>
                <td>${a.fd.ADULT.mI ? 'Free Meal' : 'Paid Meal'}</td>
                <td><i class="la la-rupee"></i>${a.fd.ADULT.fC.TF}</td>
                <td>
                <button type="button" onclick="bookflight('${a.id}','one-way' ,'${inx}','${spice || type}')" class="btn btn-red">Book Now</button>
                </td>
                </tr>`
            }).join("")}
                
            </tbody>
            <input type="hidden" name="reviewId" value="">
            <input type="hidden" name="token" value="${this.token}"></input>
            <input type="hidden" name="akasa_token" value="${this.akasa_token}"></input>
            <input type="hidden" name="spice_token" value="${this.spice_token}"></input>
            
        </table>`;
	}

    flrender(renderdata) {
        let url = this.url;
        let corp = this.corp
        console.log(this.all_com, this.com)
        if (Object.keys(this.type).length == 1) {            
            let data = this.sortfunc()['sort_price'](false).map((el, inx) => {
                let sort = el.totalPriceList.filter(it => !corp.includes(it.fareIdentifier))
                return `
                <div class="listing-box box-one hide${inx} ${sort.length == 0 ? 'hide' : ''}">
                <form id="form_${inx}">
				<input type="hidden" name="Person" value="${this.person}">
				<input type="hidden" name="adult" value="${this.adult}">
				<input type="hidden" name="child" value="${this.child}">
				<input type="hidden" name="infant" value="${this.infant}">
				<input type="hidden" name="toCityOrAirport" value="${this.tocode}">
				<input type="hidden" name="fromCityOrAirport" value="${this.fromcode}">
                ${el.text ? `<input type="hidden" name="gds_ref" value='${this.gds_ref}'>` : "" }
				<input type="hidden" name="travelDateseries" value=${ this.sdata["data"] ? !this.sdata.data[0] || this.sdata.data[0].departure_date : ""}>
                ${el.totalPriceList[0].fkey ? `<input type = "hidden" name = "fkey" value = "${el.totalPriceList[0].fkey}" ></ >` : ""}
                ${el.totalPriceList[0].fkey ? `<input type = "hidden" name = "jkey" value = "${el.totalPriceList[0].id}" ></ >` : ""}
                ${el['jkey'] ? `<input type="hidden" name="jkey" value="${el.jkey}"></input>`: ""}
                <div class="basic-info">
                    <div class="row align-items-center">
                        <div class="col-lg-4 col-md-3 col-6 order-1 sec1 pr-0">
                            <div class="flight-name">
                                <img src="${url}${el.sI[0].fD.aI.code}.png" alt="">
                                <div><b>${el.sI[0].fD.aI.name}</b></div>
                                <div class="small">${el.sI[0].fD.aI.code}-${el.sI[0].fD.fN}</div>
                            </div>
                        </div>
                        <div class="col-lg-5 col-md-5 col-12 order-3 order-md-2 sec2 px-2">
                            <div class="flight-time">
                                <div class="time">
                                    <div><b>${(el.sI[0].dt).replace('T', " ")}</b></div>
                                    <div class="small">${el.sI[0].da.name}</div>
                                </div>
                                <div class="stops">
                                    <span></span>
                                    <span></span>
                                </div>
                                <div class="time">
                                    <div><b>${(el.sI[el.sI.length - 1].at).replace('T', " ")}</b></div>
                                    <div class="small">${el.sI[el.sI.length - 1].aa.name}</div>
                                </div>
                            </div>
                            <div class="total-time">
                                <div><b style="white-space: nowrap;">${this.findDur(el.sI)}</b></div>
                                <div class="small">${el.sI[el.sI.length - 1].sN} Stop</div>
                            </div>
                        </div>
                        <div class="col-lg-3 col-md-4 col-6 order-2 order-md-2 sec3 pl-0">
                            <div class="total-price">
                                <div><b><i class="la la-rupee"></i>${ Math.min.apply(Math, el.totalPriceList.filter(it => !corp.includes(it.fareIdentifier)).map(el => el.fd.ADULT.fC.TF))}</b></div>
                                <a href="javascript:void(0)" onclick="toggleFunction('${inx}');" class="btn btn-red">View Fares</a>
                            </div>
                        </div>
                    </div>
                    <div class="divider-sec">
                        <span class="m-0 cashback">${!el.test ? "YOU CAN BOOK THIS FLIGHT" : ""}</span>
                        <a href="javascript:void(0)" onClick="toggleFlightDetails('${inx}');">Flights details</a>
                    </div>
                </div>
                ${this.flightdetails(el, inx)}
                <div id="fare-details${inx}" class="fare-details" style="padding:1em;">
                    <div class="table-responsive">
                        ${!sort || this.tablefare(el.totalPriceList, inx)}
                    </div>
                    <p class="small">
                        Available on additional charge. - Included in Fare - Not Included - Middle seat will be vacant.
                    </p>
                    <p class="small mb-0">
                        Disclaimer: Benefits shown are as per details shared by the Airline. <br>
                        * Full refund of Airline cancellation charges up to <i class="la la-rupee"></i>5,000 (per passanger per sector) on cancellation
                        <p><span style="font-size:0.72rem">* OFFER FARE & SERIES FARE ARE SUBJECT TO AVAILABILITY BOOKING CONFORMATION MAY TAKE UPTO 30 MINUTES.</span></p>
                    </p>
                </div>
            </div>
            </form></div>`;
            }).join("")
            data != [] ? this.renderel.find('#fl-render').html(data) : this.renderel.find('#fl-render').html('<h1>Sorry no result found</h1>')
        }
        else {
            Object.keys(renderdata).map((it, inx) => {
                
                let data = this.sortfunc(it)['sort_price'](false).map((el, i) => {
                    return `
                    <div class="listing-box-two box-one">
                        <div class="basic-info">
                        <div class="sec2">
                            <div class="row align-items-center">
                                <div class="col-lg-6 col-12 left-sec">
                                    <div class="flight-name">
                                        <img style="object-fit:cover;" src="${url}${el.sI[0].fD.aI.code}.png" alt="">
                                        <div class="flight-time">
                                            <div class="time">
                                                <b>${(el.sI[0].dt).replace('T', " ")}</b>
                                                <div class="small">${el.sI[0].fD.aI.name}</div>
                                            </div>
                                            <div class="stops">
                                                <span></span>
                                                <span></span>
                                            </div>
                                            <div class="time">
                                                <b>${(el.sI[el.sI.length - 1].at).replace('T', " ")}</b>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-lg-6 col-12 right-sec">
                                    <div class="total-price">
                                        <div class="time">
                                            <b>${this.findDur(el.sI)}</b>
                                            <div class="small">${el.sI[el.sI.length - 1].sN}stop</div>
                                        </div>
                                        <div class="price">
                                            <b>₹ ${el.totalPriceList[0].fd.ADULT.fC.TF}</b>
                                            <label class="custom-radio">
                                                <input data-ddate=${el.sI[0].dt} data-adate=${el.sI[el.sI.length - 1].at} data-check="${it}" data-name=${el.sI[0].fD.aI.name} data-code=${el.sI[0].fD.aI.code} name="flight1" type="radio" data-key=${el.totalPriceList[0].id} data-dtime=${(el.sI[0].dt).split("T")[1]} data-atime=${(el.sI[el.sI.length - 1].at).split("T")[1]} data-dur="${this.findDur(el.sI)}" data-price=${el.totalPriceList[0].fd.ADULT.fC.TF} data-stop=${el.sI[el.sI.length - 1].sN} value="" ${i == 0 ? "checked" : ""}>
                                                <span class="checkmark"></span>
                                            </label>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="divider-sec">
                            <a href="javascript:void(0)" onClick="toggleReturnFlightDetails${inx + 1}('${i}');">Flights details</a>
                        </div>
                    </div>
                    <div id="return-flights-details${inx + 1}${i}" class="flights-details">
                    <div class="tab-box-four">
                        <ul class="nav nav-pills" role="tablist">
                            <li class="nav-item">
                                <a class="nav-link active" id="tab-one" data-toggle="pill" href="#one-tab${i}${inx}" role="tab" aria-controls="one-tab1"
                                    aria-selected="true">Fare Summary</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" id="tab-two" data-toggle="pill" href="#two-tab${i}${inx}" role="tab" aria-controls="two-tab1"
                                    aria-selected="false">Fare
                                    Rules</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" id="tab-three" data-toggle="pill" href="#three-tab${i}${inx}" role="tab" aria-controls="three-tab1"
                                    aria-selected="false">Fare Summary</a>
                            </li>
                        </ul>
                        <div class="tab-content">
                            <div class="tab-pane fade show active bg-white" id="one-tab${i}${inx}" role="tabpanel" aria-labelledby="tab-one">
                                <div class="flight-info">
                                ${this.maproute(el.sI, el.totalPriceList[0].fd.ADULT.cc)}
                                </div>
                            </div>

                            <div class="tab-pane fade" id="two-tab${i}${inx}" role="tabpanel" aria-labelledby="tab-two">
                                <table>
                                    <thead>
                                        <tr>
                                            <th>Fare Summary</th>
                                            <th>Base Fare</th>
                                            <th>Fees & Taxes</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        ${this.faredetail(el.totalPriceList[0].fd)}
                                    </tbody>
                                </table>
                                <hr>
                                <div class="total">
                                    <div>You Pay:</div>
                                    <div><b><i class="la la-rupee"></i>${el.totalPriceList[0].fd.ADULT.fC.TF}</b></div>
                                </div>
                                <hr>
                                <p class="small m-0">Note: Total fare displayed above has been rounded off and may show a slight difference from
                                    actual
                                    fare.</p>
                            </div>

                            <div class="tab-pane fade" id="three-tab${i}${inx}" role="tabpanel" aria-labelledby="tab-three">
                                <div class="scrolls">
                                    <h4>${el.sI[0].da.code}-${el.sI[el.sI.length - 1].aa.code}</h4>
                                    <hr>
                                    <p><b>Airline Cancellation Fee</b></p>
                                    <table>
                                        <thead>
                                            <tr>
                                                <th>Duration *</th>
                                                <th>Per Passenger</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr>
                                                <td>0 hour to 2 hours</td>
                                                <td>Non-Refundable</td>
                                            </tr>
                                            <tr>
                                                <td>4 hours to 4 days</td>
                                                <td><i class="la la-rupee"></i> 3,500</td>
                                            </tr>
                                            <tr>
                                                <td>>4 days</td>
                                                <td><i class="la la-rupee"></i> 3,000</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                    <hr>
                                    <p><b>Airline Date Change Fee</b></p>
                                    <table>
                                        <thead>
                                            <tr>
                                                <th>Duration *</th>
                                                <th>Per Passenger</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr>
                                                <td>4 hours to 4 days</td>
                                                <td>Non-Refundable</td>
                                            </tr>
                                            <tr>
                                                <td>4 hours to 4 days</td>
                                                <td><i class="la la-rupee"></i> 3,500</td>
                                            </tr>
                                            <tr>
                                                <td>>4 days</td>
                                                <td><i class="la la-rupee"></i> 3,000</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                    <div class="bg-text">
                                        <p class="mb-0 small">We would recommend that you reschedule/cancel your tickets atleast 72 hours prior to the
                                            flight
                                            departure
                                        </p>
                                    </div>
                                    <hr>
                                    <p><b>Savari Service Fee (YSF)**</b></p>
                                    <p class="small">(charged per passenger in addition to airline fee as applicable)</p>
                                    <table>
                                        <tbody>
                                            <tr>
                                                <td>Online Cancellation Service Fee</td>
                                                <td><i class="la la-rupee"></i> 400</td>
                                            </tr>
                                            <tr>
                                                <td>Offline Cancellation Service Fee</td>
                                                <td><i class="la la-rupee"></i> 400</td>
                                            </tr>
                                            <tr>
                                                <td>Online Rescheduling Service Fee</td>
                                                <td><i class="la la-rupee"></i> 400</td>
                                            </tr>
                                            <tr>
                                                <td>Offline Rescheduling Service Fee</td>
                                                <td><i class="la la-rupee"></i> 1,250</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                                <hr>
                                <p class="small">* Prior to the date/time of departure.</p>
                                <p class="small">**Please note: Savari service fee is over and above the airline cancellation fee due to which
                                    refund type
                                    may vary.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
                </div>`;
                }).join("")
                data != [] ? this.renderel.find(`#fl-render${it}`).html(
                    `<form class="flight1" id="flight1" action="/flight/review_flight/" method="get">
                        <input type="hidden" name="radio1" value=${this.radio1}>
                        <input type="hidden" name="Person" value="${this.person}">
                        <input type="hidden" name="rtype" value="normal">
                        <input type="hidden" name="toCityOrAirport" value="${this.tocode}">
                        <input type="hidden" name="fromCityOrAirport" value="${this.fromcode}">
                        ${data}
                    </form>`
                ) : this.renderel.find(`#fl-render${it}`).html('<h1>Sorry no result found</h1>')
            })
        }
    }

    checkchecker() {
        let errmsg = this.err
        let total = 0;
        console.log('ajax call done')
        let keys = []
        let datamap = this.el_chk_chng().map((el, inx) => {
            let id = el.attr('data-check')
            let key = el.attr('data-key')
            keys.push(key)
            let dtime = el.attr('data-dtime')
            let atime = el.attr('data-atime')
            let dur = el.attr('data-dur')
            let price = el.attr('data-price')
            let stop = el.attr('data-stop')
            let code = el.attr('data-code')
            let name = el.attr('data-name')
            total += parseFloat(price)
            total = Math.round(total)
            $("#flight1").find(`[name="key${inx || ''}"]`).remove();
            $("#flight1").prepend(`<input type="hidden" name="key${inx || ''}" value=${key}>`)
            // return { id, key, dtime, atime, dur, price, stop, elmt }
            return `
            <div id="footer_${id}" class="flight-name multi1-date col-lg-4">
                <img src="${this.url}${code}.png" alt="">
                <div class="flight-time">
                    <div class="time">
                        <b>${dtime}</b>
                        <div class="small">${name}</div>
                    </div>
                    <div class="stops">
                        <span></span>
                    </div>
                    <div class="time">
                        <b>${atime}</b>
                    </div>
                </div>
                <div class="total-time">
                    <b>${dur}</b>
                    <div class="small">${stop} Stop</div>
                </div>
            </div>
            `
        }).join("")
        $('#footer-booking').remove()
        $('#flight1').append(`
        <section id="footer-booking" class="listing-summary">
            <div class="container">
            <div class="row align-items-center">
            <div class="col-lg-9 col-md-8 left-sec" style="padding: 1em;">
            <div class="content main-content row flex-nowrap overflowx ${this.type.length > 2 ? 'justify-content-between' : ''}">
            ${datamap}
            </div>
            </div>
            <div class="col-lg-3 col-md-4 right-sec">
            <div class="content">
            <div class="total-price">
                <span class="small">Total Fare:</span>
                <h4 class="mb-2">${total}</h4>
            </div>
            <button class="btn btn-block btn-white">Book Now</button>
            </div>
            </div>
            </div>
        </section>
        `)
        console.log(keys)
        $.ajax({
            type: "GET",
            url: "/flight/review_flight/",
            data: {
                'ajax': 'ajax',
                'allkey': JSON.stringify(keys)
            },
            beforeSend: function(){
                $('body').addClass('active')
                errmsg['mes'] = ''
            },
            success: function (res) {
                $('body').removeClass('active')
                if (res['errors']) {
                    errmsg['mes'] = res['errors'][0].message
                }
            },
            error: function() {
                $('body').removeClass('active')
                errmsg['mes'] = ''
            }
        });
    }

    // <div class="small">Earn eCash: <span>₹ 500</span></div>

    footer() {
        return `
        <section id="footer-booking" class="listing-summary">
            <div class="container">
            <div class="row align-items-center">
            <div class="col-lg-9 col-md-8 left-sec" style="padding: 1em;">
            <div class="content main-content">
            ${Object.keys(this.trip).map((el, inx) => {
                return `
                ${inx == 0 ? "" : '<div class="divide-dash"></div>'}
                <div id="footer_${el}" class="flight-name start-date">
                <img src="{% static 'main/images/airline/4.png' %}" alt="">
                <div class="flight-time">
                    <div class="time">
                        <b>15:30</b>
                        <div class="small">Go First</div>
                    </div>
                    <div class="stops">
                        <span></span>
                    </div>
                    <div class="time">
                        <b>20:45</b>
                    </div>
                </div>
                <div class="total-time">
                    <b>5h 15m</b>
                    <div class="small">1 Stop</div>
                </div>
            </div>
                `
            }).join("")}
            </div>
            </div>
            <div class="col-lg-3 col-md-4 right-sec">
            <div class="content">
            <div class="total-price">
                <span class="small">Total Fare:</span>
                <h4 class="mb-2">5h 15m</h4>
            </div>
            <button class="btn btn-block btn-white">Book Now</button>
            </div>
            </div>
            </div>
        </section>
        `
    }

    sortrend(renderdata, it) {
        let corp = this.corp;
        if (!it) {
            let data = renderdata.map((el, inx) => {
                let sort = el.totalPriceList.filter(it => !corp.includes(it.fareIdentifier))
                return `<div class="listing-box box-one ${sort.length == 0 ? 'hide' : ''}">
                <form id="form_${inx}">
				<input type="hidden" name="Person" value="${this.person}">
				<input type="hidden" name="adult" value="${this.adult}">
				<input type="hidden" name="child" value="${this.child}">
				<input type="hidden" name="infant" value="${this.infant}">
				<input type="hidden" name="toCityOrAirport" value="${this.tocode}">
				<input type="hidden" name="fromCityOrAirport" value="${this.fromcode}">
                <input type="hidden" name="travelDateseries" value=${ this.sdata["data"] ? this.sdata.data[0].departure_date : ""}>
                ${el.text ? `<input type="hidden" name="gds_ref" value='${this.gds_ref}'>` : "" }
                ${el.totalPriceList[0].fkey ? `<input type = "hidden" name = "fkey" value = "${el.totalPriceList[0].fkey}" ></ >` : ""}
                ${el.totalPriceList[0].fkey ? `<input type = "hidden" name = "jkey" value = "${el.totalPriceList[0].id}" ></ >` : ""}
                ${el['jkey'] ? `<input type="hidden" name="jkey" value="${el.jkey}"></input>`: ""}
                <div class="basic-info">
                    <div class="row align-items-center">
                        <div class="col-lg-4 col-md-3 col-6 order-1 sec1 pr-0">
                            <div class="flight-name">
                                <img src="${url}${el.sI[0].fD.aI.code}.png" alt="">
                                <div><b>${el.sI[0].fD.aI.name}</b></div>
                                <div class="small">${el.sI[0].fD.aI.code}-${el.sI[0].fD.fN}</div>
                            </div>
                        </div>
                        <div class="col-lg-5 col-md-5 col-12 order-3 order-md-2 sec2 px-2">
                            <div class="flight-time">
                                <div class="time">
                                    <div><b>${(el.sI[0].dt).replace('T', " ")}</b></div>
                                    <div class="small">${el.sI[0].da.name}</div>
                                </div>
                                <div class="stops">
                                    <span></span>
                                    <span></span>
                                </div>
                                <div class="time">
                                    <div><b>${(el.sI[el.sI.length - 1].at).replace('T', " ")}</b></div>
                                    <div class="small">${el.sI[el.sI.length - 1].aa.name}</div>
                                </div>
                            </div>
                            <div class="total-time">
                                <div><b style="white-space: nowrap;">${this.findDur(el.sI)}</b></div>
                                <div class="small">${el.sI[el.sI.length - 1].sN} Stop</div>
                            </div>
                        </div>
                        <div class="col-lg-3 col-md-4 col-6 order-2 order-md-2 sec3 pl-0">
                            <div class="total-price">
                                <div><b><i class="la la-rupee"></i>${ Math.min.apply(Math, el.totalPriceList.filter(it => !corp.includes(it.fareIdentifier)).map(el => el.fd.ADULT.fC.TF))}</b></div>
                                <a href="javascript:void(0)" onclick="toggleFunction('${inx}');" class="btn btn-red">View Fares</a>
                            </div>
                        </div>
                    </div>
                    <div class="divider-sec">
                        <a href="javascript:void(0)" onClick="toggleFlightDetails('${inx}');">Flights details</a>
                    </div>
                </div>
                ${this.flightdetails(el, inx)}
                <div id="fare-details${inx}" class="fare-details" style="padding:1em;">
                    <div class="table-responsive">
                    ${!sort || this.tablefare(el.totalPriceList, inx)}
                    </div>
                    <p class="small">
                        Available on additional charge. - Included in Fare - Not Included - Middle seat will be vacant.
                    </p>
                    <p class="small mb-0">
                        Disclaimer: Benefits shown are as per details shared by the Airline. <br>
                        * Full refund of Airline cancellation charges up to <i class="la la-rupee"></i>5,000 (per passanger per sector) on cancellation
                    </p>
                </div>
            </form></div>`;
            }).join("")
            data != [] ? this.renderel.find('#fl-render').html(data) : this.renderel.find('#fl-render').html('<h1>Sorry no result found</h1>')
        } else {    
            let data = renderdata.map((el, inx) => {
                return `
                <div class="listing-box-two box-one">
                    <div class="basic-info">
                    <div class="sec2">
                        <div class="row align-items-center">
                            <div class="col-lg-6 col-12 left-sec">
                                <div class="flight-name">
                                    <img style="object-fit:cover;" src="${url}${el.sI[0].fD.aI.code}.png" alt="">
                                    <div class="flight-time">
                                        <div class="time">
                                            <b>${(el.sI[0].dt).replace('T', " ")}</b>
                                            <div class="small">${el.sI[0].fD.aI.name}</div>
                                        </div>
                                        <div class="stops">
                                            <span></span>
                                            <span></span>
                                        </div>
                                        <div class="time">
                                            <b>${(el.sI[el.sI.length - 1].at).replace('T', " ")}</b>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-lg-6 col-12 right-sec">
                                <div class="total-price">
                                    <div class="time">
                                        <b>${this.findDur(el.sI)}</b>
                                        <div class="small">${el.sI[el.sI.length - 1].sN}stop</div>
                                    </div>
                                    <div class="price">
                                        <b>₹ ${el.totalPriceList[0].fd.ADULT.fC.TF}</b>
                                        <label class="custom-radio">
                                            <input data-ddate=${el.sI[0].dt} data-adate=${el.sI[length - 1].at} data-check="${it}" data-name=${el.sI[0].fD.aI.name} data-code=${el.sI[0].fD.aI.code} name="flight1" type="radio" data-key=${el.totalPriceList[0].id} data-dtime=${(el.sI[0].dt).split("T")[1]} data-atime=${(el.sI[el.sI.length - 1].at).split("T")[1]} data-dur="${this.findDur(el.sI)}" data-price=${el.totalPriceList[0].fd.ADULT.fC.TF} data-stop=${el.sI[el.sI.length - 1].sN} value="" ${inx == 0 ? "checked" : ""}>
                                            <span class="checkmark"></span>
                                        </label>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="divider-sec">
                        <a href="javascript:void(0)" onClick="toggleReturnFlightDetails1(${inx});">Flights details</a>
                    </div>
                </div>
            </div>`;
            }).join("")
            data != [] ? this.renderel.find(`#fl-render${it}`).html(
                `<form class="flight1" id="flight1" action="/flight/review_flight/" method="get">
                    <input type="hidden" name="radio1" value=${this.radio1}>
                    <input type="hidden" name="Person" value="${this.person}">
                    <input type="hidden" name="rtype" value="normal">
                    <input type="hidden" name="toCityOrAirport" value="${this.tocode}">
                    <input type="hidden" name="fromCityOrAirport" value="${this.fromcode}">
                    ${data}
                </form>`
            ) : this.renderel.find(`#fl-render${it}`).html('<h1>Sorry no result found</h1>')
            this.checkchecker()
            this.formcheck()
        }
    }

    formcheck() {
        this.renderel.find('.flight1').submit(function (e) { 
            e.preventDefault()
            let time = this.el_chk_chng().map(el => {
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
    }

    sortfunc(data) {
        let trip = this.type.length == 1 ? this.afterfl : this.afterfl[data]
        let sdata = this.data;
        let corp = this.corp;
        return {
            sort_arrive: function (isChange) {
                console.log(isChange)
                return trip.sort((a, b) => {
                    let el_a = new Date(a.sI[a.sI.length - 1].at);
                    let el_b = new Date(b.sI[b.sI.length - 1].at);
                    return !isChange ? el_a < el_b ? -1 : 1 : el_a > el_b ? -1 : 1;
                })
            },
            sort_depart: function (isChange) {
                return trip.sort((a, b) => {
                    let el_a = new Date(a.sI[0].dt);
                    let el_b = new Date(b.sI[0].dt);
                    return !isChange ? el_a < el_b ? -1 : 1 : el_a > el_b ? -1 : 1;
                })
            },
            sort_duration: function (isChange) {
                return trip.sort((a, b) => {
                    let el_a =  (new Date(a.sI[a.sI.length - 1].at)) - (new Date(a.sI[0].dt));
                    let el_b =  (new Date(b.sI[b.sI.length - 1].at)) - (new Date(b.sI[0].dt));
                    return !isChange ? el_a < el_b ? -1 : 1 : el_a > el_b ? -1 : 1;
                })
            },
            sort_price: function (isChange) { 
                let all = trip.sort((a, b) => {
                    let el_a = Math.min.apply(Math, a.totalPriceList.filter(it => !corp.includes(it.fareIdentifier)).map(el => el.fd.ADULT.fC.TF));
                    let el_b = Math.min.apply(Math, b.totalPriceList.filter(it => !corp.includes(it.fareIdentifier)).map(el => el.fd.ADULT.fC.TF));
                    return !isChange ? el_a < el_b ? -1 : 1 : el_a > el_b ? -1 : 1;
                })
                return all
            }
        }
    }

    sort(prev, data) {
        console.log(data)
        let srname = Object.keys(this.sortlist).find(el => this.sortlist[el] == true)
        this.lastchange = !prev[srname] == this.sortlist[srname] || this.lastchange ? false : true;
        if (this.type.length == 1) {
            this.sortrend(this.sortfunc(data)[srname](this.lastchange), false)
        } else {
            this.sortrend(this.sortfunc(data)[srname](this.lastchange), data);
        }
    }
    elsort() {
        // console.log(Object.keys(this.sortlist), this.renderel.find('#sort_depart').text('done'))
        return this.type.map(el => this.renderel.find(`[data-name="${el}"]`))
    }

    el_chk_chng() {
        return this.type.map(el => { 
            return this.renderel.find(`[data-check="${el}"]:checked`)
        })
    }
    all_chk_func() {
        return this.type.map(el => { 
            return this.renderel.find(`[data-check="${el}"]`)
        })
    }
}
