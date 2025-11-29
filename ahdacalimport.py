#!/usr/bin/env python3

import argparse
import openpyxl
import datetime
def load_calendar(filename):
    file = openpyxl.load_workbook(filename)
    
    schedule = file["Schedule"]

    # Get starting date
    sun_date = schedule["B2"].value

    # Get tracks for each day
    tracks = {}
    for i in range(6):
        todays_tracks = []
        tracks_offset = sum(len(v) for _,v in tracks.items())
        # tracks_offset = 1
        this_track = ""
        today = sun_date + datetime.timedelta(i,0,0)
        j = 0
        # Assume every day begins with the same track
        # TODO: Don't assume this
        while True:
            this_track = {"date": today, "col_offset": tracks_offset+j, "value":schedule["B3"].offset(row=0,column=tracks_offset+j).value}
            if this_track["value"] in [t["value"] for t in todays_tracks]: break
            todays_tracks.append(this_track)
            j+=1;
        tracks[today] = todays_tracks

    # How many slots do we have per track
    num_time_slots = 0
    while True:
        cur_val = schedule["A4"].offset(row=num_time_slots,column=0).value 
        if cur_val == "Daily Totals": break
        num_time_slots += 1

    # For each track, load the shifts
    shifts = []
    for _,todays_tracks in tracks.items():
        for track in todays_tracks:
            this_shift_initials = schedule["B3"].offset(row=1,column=track["col_offset"]).value
            this_shift_begin_i = 1
            i = 1
            while i < num_time_slots:
                cur_initials = schedule["B3"].offset(row=i,column=track["col_offset"]).value
                if not cur_initials or len(cur_initials) == 0:
                    i += 1
                    continue
                if this_shift_initials and this_shift_initials != cur_initials:
                    # New shift
                    shifts.append({
                        "track": track,
                        "begin": schedule["A4"].offset(row=this_shift_begin_i - 1, column=0).value,
                        "end": schedule["A4"].offset(row=i-2, column=0).value,
                        "initials": this_shift_initials})
                i += 1
    
    return shifts


def main():
    parser = argparse.ArgumentParser(
            prog="ahdacalimport.py",
            description="Import AHDA shift calendar to provided database",
            )
    parser.add_argument("filename")
    parser.add_argument("db_uri")
    # shifts = load_calendar(args.filename)

    parser.parse_args()


if __name__ == "__main__":
    main()

