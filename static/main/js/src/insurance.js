class Insurance{
    constructor(ins, person) {
        this.check = false
        this.trip = ins['tripInfos']
        this.person = person
        this.amount = 0
        this.ins_type = {
            domestic: {
                category: "de5ee71c-098f-4cc0-b486-e69391cc9fa8",
                plancode: "6e6a5880-54dd-4846-bb64-d8bb7de38099",
                price: {
                    ADULT_ALL: {
                        basePrice: 135,
                        total_base: 110.7,
                        service_tax: 24.3,
                        total_charges: 135,
                    }
                }
            },
            international: {
                category: "6b123144-2e3a-490e-baeb-b59f09327b7c",
                plancode: "02eb3430-22a1-4b72-9f6a-2943b4180bb7",
                price: {
                    ADULT_40: {
                        basePrice: 873,
                        total_base: 715.86,
                        service_tax: 137.14,
                        total_charges: 873,
                    },
                    ADULT_60: {
                        basePrice: 973,
                        total_base: 797.86,
                        service_tax: 175.14,
                        total_charges: 973,
                    },
                    ADULT_70: {
                        basePrice: 1489,
                        total_base: 1220.98,
                        service_tax: 268.02,
                        total_charges: 1489,
                    },
                }
            }
        }
        this.isDom = this.trip.every(el => el.sI.every(it => (it.aa['country'] == "India") && (it.da['country'] == "India")))
        this.maindata = {}
    }
    pax(data) {
        this.check = true
        let type = this.isDom ? "domestic" : "international";
        console.log(type)
        for (let i = 0; i < this.person; i++){
            let age = (new Date()).getFullYear - (new Date(data[`dob${i ? i + 1 : ""}`]));
            this.maindata[`person_${i + 1}`] = this.trip.map(el => {
                console.log(el)
                let age = this.isDom ? false : (new Date()).getFullYear() - (new Date(data[`dob${i ? i + 1 : ""}`])).getFullYear();
                console.log(age)
                if (age) {
                    let chgage = !(age <= 40) || '40';
                    (chgage == '40') || (chgage = (!(age <= 60) || '60'));
                    (chgage == '60' || chgage == '40') || (chgage = '70');
                    age = chgage;
                }
                this.amount += this.ins_type[type]['price'][`ADULT_${age || "ALL"}`]['basePrice'];
                return {
                    pp: data[`pp${i ? i + 1 : ""}`],
                    title: data[`title${i ? i + 1 : ""}`],
                    first_name: data[`first_name${i ? i + 1 : ""}`],
                    last_name: data[`last_name${i ? i + 1 : ""}`],
                    dob: data[`dob${i ? i + 1 : ""}`],
                    price: {
                        basePrice: this.ins_type[type]['price'][`ADULT_${age || "ALL"}`]['basePrice'],
                        total_base: this.ins_type[type]['price'][`ADULT_${age || "ALL"}`]['total_base'],
                        service_tax: this.ins_type[type]['price'][`ADULT_${age || "ALL"}`]['service_tax'],
                        total_charges: this.ins_type[type]['price'][`ADULT_${age || "ALL"}`]['total_charges'],
                        
                    },
                    category: this.ins_type[type]['category'],
                    plancode: this.ins_type[type]['plancode'],
                    tripdate: {
                        departuredate: el.sI[0].dt,
                        arrivaldate: el.sI[el.sI.length - 1].at,
                    },
                    tripType: type,
                }
            })
        }
        console.log(this.maindata, this.amount)
    }
}