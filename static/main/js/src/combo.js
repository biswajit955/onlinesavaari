export class Combo {
    constructor(obj, el, url, usertype = 'None', token) {
        this.person = obj.Person
        this.child = obj.child
        this.adult = obj.adult
        this.infant = obj.infant
        this.radio1 = obj.radio1
        this.tocode = obj.toCityOrAirport
        this.fromcode = obj.fromCityOrAirport
        this.usertype = usertype
        this.search_request = obj.search_request;
        this.trip = obj.data.searchResult.tripInfos['COMBO'].slice(0, 50);
        this.renderel = el;
        this.sortlist = { sort_arrive: false, sort_depart: false, sort_duration: false, sort_price: true }
        this.lastchange = false;
        this.url = url;
        this.all = this.trip.map((obj, inx) => {
            let arr = this.search_request.searchQuery.routeInfos.map(el => [])
			let i = 0;
			obj.sI.map((item, inx) => {
				let next = obj.sI[inx + 1];
				if(!next){
					arr[i].push(item)
				}else if (next.sN == 0) {
					arr[i].push(item)
					i++;
				} else {
					arr[i].push(item)
				}
			})
			let route = this.search_request.searchQuery.routeInfos.map((el, ix) => [`${el.fromCityOrAirport.code}-${el.toCityOrAirport.code}`, arr[ix]])
            let mod = Object.fromEntries(route);
			return {
				fare: obj.totalPriceList,
				mod
			};
		})
    }


    sortrender() {
        let typ = this.type;
        let rendit = `<div class="filter-box">
            <div class="sort-label">Sort By:</div>
            <div class="sort-nav">
                    <div class="s-li" id="sort_depart">
                        <p>DEPART</p>
                    </div>
                    <div class="s-li" id="sort_arrive">
                        <p>ARRIVE</p>
                    </div>
                    <div class="s-li" id="sort_duration">
                        <p>DURATION</p>
                    </div>
            </div>
            <div class="price-filter" id="sort_price">
                <div class="s-li">
                    PRICE PER ADULT
                </div>
            </div>
        </div>
        <div id="fl-render" ></div>`
        this.renderel.html(rendit)
    }

    getroute(obj){
		let routes = Object.values(obj.mod).map(el => el.filter(function(v, i){
			return (i == 0 || i == (el.length - 1))
		}));
		return routes.map(rend => `
		<div class="flight-time" style="padding: 1em 8em;border-bottom: 1px solid #e4e4e4;width: 100%;">
			<div class="time">
				<div style="position:relative;"><span style="position:absolute;top:0;left:-30px;">${rend[0].da.code}</span><b>${dateformat(rend[0].dt)}</b></div>
				<div class="small">${rend[0].da.city}</div>
			</div>
			<div class="stops">
				<span></span>
				<span></span>
			</div>
			<div class="time">
				<div style="position:relative;"><b>${dateformat(rend[rend.length - 1].at)}</b><span style="position:absolute;top:0;right:-30px;">${rend[rend.length - 1].aa.code}</span></div>
				<div class="small">${rend[rend.length - 1].aa.city}</div>
			</div>
			<div class="total-time">
				<div><b style="white-space: nowrap;">${getdur(rend)}</b></div>
				<div class="small">${rend[rend.length - 1].sN} Stop</div>
			</div>
		</div>
		`).join("")
	}
	getfligh(obj){
		return Object.values(obj.mod)[0][0]
    }
    dateformat(time){
		let ft = new Date(time);
		let min = ft.getMinutes() >= 10 ? ft.getMinutes() : "0" + ft.getMinutes();
		let hour = ft.getHours() >= 10 ? ft.getHours() : "0" + ft.getHours();
		return `${hour}:${min}`
    }
    getdur(tm){
		let dt = new Date(tm[0].dt)
		let at = new Date(tm[tm.length - 1].at)
		let min = Math.floor((((at - dt)/1000)%3600)/60)
		let hour = Math.floor(((at - dt)/1000)/3600)
		return `${hour}h ${min}m`
	}
    getroute(obj){
		let routes = Object.values(obj.mod).map(el => el.filter(function(v, i){
			return (i == 0 || i == (el.length - 1))
		}));
		return routes.map(rend => `
		<div class="flight-time" style="padding: 1em 8em;border-bottom: 1px solid #e4e4e4;width: 100%;">
			<div class="time">
				<div style="position:relative;"><span style="position:absolute;top:0;left:-30px;">${rend[0].da.code}</span><b>${this.dateformat(rend[0].dt)}</b></div>
				<div class="small">${rend[0].da.city}</div>
			</div>
			<div class="stops">
				<span></span>
				<span></span>
			</div>
			<div class="time">
				<div style="position:relative;"><b>${this.dateformat(rend[rend.length - 1].at)}</b><span style="position:absolute;top:0;right:-30px;">${rend[rend.length - 1].aa.code}</span></div>
				<div class="small">${rend[rend.length - 1].aa.city}</div>
			</div>
			<div class="total-time">
				<div><b style="white-space: nowrap;">${this.getdur(rend)}</b></div>
				<div class="small">${rend[rend.length - 1].sN} Stop</div>
			</div>
		</div>
		`).join("")
    }
    flightinfo(flt, index) {
        console.log(flt)
		let arr = [];
		for (const [k, v] of Object.entries(flt.mod)){
			arr.push(`
			<div class="route-details${index} ${k} ${arr.length == 0 ? 'sh' : 'hi'}" >
				${this.maproute(v, flt.fare[0].fd.ADULT.cc)}
			</div>
			`)
		}
		return arr.join("")
    }
    tagname(tag, inx){
		return tag.map((el, i) => `
		<li>
			<label class="text-radio tag${inx} ${i == 0 ? 'fttag': ''}">
				<input name="tag" type="radio" onclick="gettag('${el}', ${inx})" data-${el}>
				<span class="checkmark"></span>
				<span class="trip-label">${el}</span>
			</label>
		</li>
		`).join("")
    }
    maproute(v, cc){
		return v.map(el => `
		<div class="sec1">
			<div class="name">
				<img src="{% static 'flight/airline_logo/' %}${el.fD.aI.code}.png" alt="">
				<div>${el.fD.aI.name},<span>${cc}</span></div>
				<div class="small"></div>
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
    flightdetails(flight, index){
		let key = Object.keys(flight.mod);
		return `
		<div id="flights-details${index}" class="flights-details m-0">
            <div class="head-sec m-0">
                <h4>Flight Details</h4>
            </div>
            <div class="body-sec">
                <div class="row m-0">
                    <div class="col-lg-8 col-md-7 left-sec">
						<div class="booking-box">
							<ul class="trip-type-radio">
								${this.tagname(key, index)}
							</ul>
						</div>
                        <div class="flight-info">
							${this.flightinfo(flight, index)}
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
                                            {% if not adult == '0' %}
                                            <tr>
                                            
                                                <td>Adult x {{adult}}</td>
                                                <td><i class="la la-rupee"></i><span class="ad{{ forloop.counter0 }}">{% widthratio i.totalPriceList.0.fd.ADULT.fC.BF 1 adult %}</span></td>
                                                <td><i class="la la-rupee"></i><span class="ad{{ forloop.counter0 }}">{% widthratio i.totalPriceList.0.fd.ADULT.fC.TAF 1 adult %}</span></td>
                                            </tr>
                                            {% endif %}
                                            {% if not child == '0' %}
                                            <tr>
                                                <td>Child x {{child}}</td>
                                                <td><i class="la la-rupee"></i><span class="ad{{ forloop.counter0 }}">{% widthratio i.totalPriceList.0.fd.CHILD.fC.BF 1 child %}</span></td>
                                                <td><i class="la la-rupee"></i> <span class="ad{{ forloop.counter0 }}">{% widthratio i.totalPriceList.0.fd.CHILD.fC.TAF 1 child %}</span></td>
                                            </tr>
                                            {% endif %}
                                            {% if not infant == '0' %}
                                            <tr>
                                                <td>Infant x {{infant}}</td>
                                                <td><i class="la la-rupee"></i><span class="ad{{ forloop.counter0 }}">{% widthratio i.totalPriceList.0.fd.INFANT.fC.BF 1 infant %}</span></td>
                                                <td><i class="la la-rupee"></i> <span class="ad{{ forloop.counter0 }}">{% widthratio i.totalPriceList.0.fd.INFANT.fC.TAF 1 infant %}</span></td>
                                            </tr>
                                            {% endif %}
                                        </tbody>
                                    </table>
                                    <hr>
                                    <div class="total">
                                        <div>You Pay:</div>
                                        <div><b><i class="la la-rupee"></i><span class="ad_total{{ forloop.counter0 }}"></span></b></div>
                                    </div>
                                    <hr>
                                    <p class="small m-0">Note: Total fare displayed above has been rounded off and may show a slight difference from actual
                                        fare.</p>
                                </div>

                                <div class="tab-pane fade" id="two-tab${index}" role="tabpanel" aria-labelledby="tab-two${index}">
                                    <div class="scrolls">
                                        <h4>DEL-GOI-BLR</h4>
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
                                    <p class="small">**Please note: Savari service fee is over and above the airline cancellation fee due to which refund
                                        type
                                        may vary.
                                    </p>
                                </div>

                                <div class="mt-4">
                                    <button type="button" onclick="bookflight('{{i.totalPriceList.0.id}}', '{{radio1}}', '{{forloop.parentloop.counter}}','normal');" class="btn btn-block btn-white">Book Now</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
		`
    }
    tablefare(a, inx){
		return `
		<table class="table table-bordered">
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
				<tr>
					<th scope="row">${a[0].fareIdentifier}</th>
					<td>${a[0].fd.ADULT.bI.iB}</td>
					<td>${a[0].fd.ADULT.bI.cB}</td>
					<td>Extra Charge</td>
					<td>Extra Charge</td>
					<td>Extra Charge</td>
					<td>${a[0].fd.ADULT.mI? 'Free Meal': 'Paid Meal'}</td>
					<td><i class="la la-rupee"></i>${a[0].fd.ADULT.fC.TF}</td>
					<td>
						<button type="button" onclick="bookflight('${a[0].id}','multi-way' ,'${inx}','normal')" class="btn btn-red">Book Now</button>
					</td>
				</tr>
			</tbody>
			<input type="hidden" name="token" value="">
			<input type="hidden" name="reviewId" value="">
		</table>
		`
	}
    flrender(renderdata) {
        let url = this.url;
        let data = renderdata.map((el, inx) => {
            return `
            <form id="form_${inx}" action="{% url 'review_flight' %}" method="GET">
            <input type="hidden" name="radio1" value="multi-way">
            <input type="hidden" name="Person" value="1">
            <input type="hidden" name="adult" value="1">
            <input type="hidden" name="child" value="0">
            <input type="hidden" name="infant" value="0">
            <input type="hidden" name="toCityOrAirport" value="">
            <input class="totalair" type="hidden" name="totalair" value="">
            <div class="listing-box box-one" style="padding: 0;">
                <div class="basic-info">
                    <div class="grid" style="display:grid;grid-template-columns:150px 2fr 1fr">
                        <div class="table-cell airline sec1" style="border-right:1px solid #e4e4e4;padding:1em;">
                            <div class="flight-name" style="display: flex;flex-direction: column;padding-left: 0px;align-items: center;justify-content: center;">
                                <img src="${url}${this.getfligh(el).fD.aI.code}.png" alt="" style="position: static">
                                <div style="text-align:center;"><b>${this.getfligh(el).fD.aI.name}</b></div>
                                <div class="small">${this.getfligh(el).fD.aI.code}-${this.getfligh(el).fD.fN}</div>
                            </div>
                        </div>
                        <div class="table-cell sec2" style="flex-direction:column;border-right:1px solid #e4e4e4;">
                        ${this.getroute(el)}
                        </div>
                        <div class="table-cell sec3" style="padding:1em 2em;display: flex;justify-content: flex-end;align-items: flex-start;">
                            <div class="total-price" style="display:block">
                                <div style="text-align: center;padding-bottom: 0.5em;font-size:1.2rem"><b><i class="la la-rupee"></i>${el.fare[0].fd.ADULT.fC.TF}</b></div>
                                <a href="javascript:void(0)" onclick="toggleFunction('${inx}');" class="btn btn-red" style="padding:0.5em 2em;">View Fares</a>
                            </div>
                        </div>
                    </div>
                    <div class="divider-sec" style="margin:0;padding:10px">
                        <a href="javascript:void(0)" onClick="toggleFlightDetails('${inx}');">Flights details</a>
                    </div>
                </div>
                ${this.flightdetails(el, inx)}
                <div id="fare-details${inx}" class="fare-details" style="padding:1em;">
                    <div class="table-responsive">
                    ${this.tablefare(el.fare, inx)}
                    </div>
                    <p class="small">
                        Available on additional charge. - Included in Fare - Not Included - Middle seat will be vacant.
                    </p>
                    <p class="small mb-0">
                        Disclaimer: Benefits shown are as per details shared by the Airline. <br>
                        * Full refund of Airline cancellation charges up to <i class="la la-rupee"></i>5,000 (per passanger per sector) on cancellation
                    </p>
                </div>
            </div>  
    </form>`;
        }).join("")
        data != [] ? this.renderel.find('#fl-render').html(data) : this.renderel.find('#fl-render').html('<h1>Sorry no result found</h1>')
    }
}