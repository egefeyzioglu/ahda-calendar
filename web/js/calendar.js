function timeToRow(time,row_count,total_hrs = 24) {
    const hrs = Number(time.substring(0,2));
    const min = Number(time.substring(2,4));
    const rows_per_hr = row_count/total_hrs;
    const mins_per_row = 60/rows_per_hr;
    return Math.round(hrs * rows_per_hr + min / mins_per_row);
}

function createShiftElem(shift) {
    shift_elem_html = `
    
    `;
}

window.addEventListener("load", (_) => {
    const our_initials = "JD";
    const shifts = [
        { shift_id: 1, week_no: "202548", begin_time: "0800", end_time: "1600", initials: "JD", track: "W1", day: "0" },
        { shift_id: 100, week_no: "202548", begin_time: "1100", end_time: "1600", initials: "JD", track: "W1", day: "2" },
        { shift_id: 101, week_no: "202548", begin_time: "0930", end_time: "1400", initials: "JD", track: "W1", day: "3" },
        { shift_id: 2, week_no: "202548", begin_time: "1600", end_time: "2000", initials: "SM", track: "W2", day: "0" },
        { shift_id: 3, week_no: "202548", begin_time: "0900", end_time: "1700", initials: "AL", track: "PH1", day: "1" },
        { shift_id: 4, week_no: "202548", begin_time: "0700", end_time: "1400", initials: "MK", track: "PH2", day: "2" },
        { shift_id: 5, week_no: "202548", begin_time: "1200", end_time: "2000", initials: "TB", track: "FL", day: "3" },
        { shift_id: 6, week_no: "202548", begin_time: "0800", end_time: "1200", initials: "t.b./r.c./JD", track: "BO", day: "4" },
        { shift_id: 7, week_no: "202548", begin_time: "1930", end_time: "2300", initials: "RC", track: "15", day: "5" },
        { shift_id: 8, week_no: "202548", begin_time: "0000", end_time: "0800", initials: "HN", track: "BR", day: "6" },
        { shift_id: 9, week_no: "202548", begin_time: "1400", end_time: "2200", initials: "GS", track: "W1", day: "2" },
        { shift_id: 10, week_no: "202548", begin_time: "1800", end_time: "2300", initials: "LH", track: "W2", day: "1" },
        { shift_id: 11, week_no: "202548", begin_time: "0600", end_time: "1400", initials: "EP", track: "PH1", day: "3" },
        { shift_id: 12, week_no: "202548", begin_time: "1500", end_time: "2300", initials: "JP", track: "FL", day: "4" }
    ];
    // [].forEach.call(document.getElementsByClassName("calendar-inner"), function (time_strip) {
    //     const num_time_labels = 29;
    //     const time_labels = [...Array(num_time_labels).keys()].map((i)=>{
    //         let d = document.createElement("div");
    //         d.classList.add("calendar-time-strip--label");
    //         d.style.gridColumn = 1;
    //         d.style.gridRowStart = i * 2 + 1;
    //         d.style.gridRowEnd = i * 2 + 4;
    //         return d;
    //     });
    //     time_labels.map((lbl)=>{time_strip.appendChild(lbl)})
    // });
    // const calendar_inner = document.getElementById("calendar-inner");
    // shifts.forEach((shift)=>{
    //     if(!shift.initials.endsWith(our_initials)) return;
    //     const shift_elem = document.createElement("div");
    //     // console.log(shift)
    //     shift_elem.classList.add("shift");
    //     shift_elem.style.gridColumn = Number(shift.day) + 2;
    //     shift_elem.style.gridRowStart = timeToRow(shift.begin_time, 48, 24);
    //     shift_elem.style.gridRowEnd = timeToRow(shift.end_time, 48, 24);
    //     // console.log(shift_elem);
    //     calendar_inner.appendChild(shift_elem);
    // });
})