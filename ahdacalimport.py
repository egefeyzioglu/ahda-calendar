#!/usr/bin/env python3

import argparse
import openpyxl

def main():
    parser = argparse.ArgumentParser(
            prog="ahdacalimport.py",
            description="Import AHDA shift calendar to provided database",
            )
    parser.add_argument("filename")
    parser.add_argument("db_uri")

    parser.parse_args()


if __name__ == "__main__":
    main()

