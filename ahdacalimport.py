#!/usr/bin/env python3

import argparse
import openpyxl
import psycopg2
import datetime
from urllib.parse import urlparse
from configparser import ConfigParser

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


class DbConn:
    def __init__(self, exec_fn, ctx):
        self._execute = exec_fn
        self.ctx = ctx

    def execute(self, sql):
        return self._exec(sql)


def get_db_conn(uri_string):
    uri = urlparse(uri_string, scheme="???")
    if uri.scheme == "postgresql":
        if uri.password and not allow_cli_password:
            raise ValueError("Refusing to read password from command line parameters without --allow-password-uri")
        db = {}
        if db_config_path:
            parser = ConfigParser()
            parser.read(db_config_path)
            if not parser.has_section("postgresql"):
                raise ValueError(f"File {db_config_path} has no section postgresql")
            for param in parser.items("postgresql"):
                db[param[0]] = param[1]
        if uri.username != None: db["username"] = uri.username
        if uri.password != None: db["password"] = uri.password
        if uri.hostname != None: db["host"] = uri.hostname
        if uri.port != None: db["port"] = uri.port
        if uri.path != "" and uri.path != None: db["dbname"] = uri.path.lstrip("/")

        if not db["port"]: db["port"] = 5432

        conn = psycopg2.connect(**db)
        def exec_fn(sql):
            cur = conn.cursor()
            try:
                cur.execute(sql)
                # If the statement returns rows, fetch them
                if cur.description:
                    rows = cur.fetchall()
                    cur.close()
                    return rows
                # Otherwise commit and return affected row count
                conn.commit()
                affected = cur.rowcount
                cur.close()
                return affected
            except Exception:
                # Rollback on error, close cursor and re-raise
                conn.rollback()
                try:
                    cur.close()
                except Exception:
                    pass
                raise

        ret = DbConn(exec_fn, conn)

    else:
        raise ValueError(f"Unsupported URI scheme \"{uri.scheme}\"")


def process_args(args):
    global allow_cli_password
    global db_config_path
    global db_uri_string

    allow_cli_password = args.allow_password_uri
    db_config_path = args.db_config
    db_uri_string = args.db_uri

    if not db_config_path and not db_uri_string:
        raise ValueError("You have to specify at least one of --db-config-path | -c or db_uri")



def main():
    parser = argparse.ArgumentParser(
            prog="ahdacalimport.py",
            description="Import AHDA shift calendar to provided database",
            )
    parser.add_argument("filename")
    parser.add_argument("db_uri", nargs='?')
    parser.add_argument("--allow-password-uri", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("-c", "--db-config")

    args = parser.parse_args()

    process_args(args)

    # shifts = load_calendar(args.filename)

    conn = get_db_conn(args.db_uri)




if __name__ == "__main__":
    main()

