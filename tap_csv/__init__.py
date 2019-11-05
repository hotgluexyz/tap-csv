#!/usr/bin/env python3

import singer
import csv
import sys
import argparse
import json
import os
import copy


REQUIRED_CONFIG_KEYS = ['files']
STATE = {}
CONFIG = {}

logger = singer.get_logger()

def write_schema_from_header(entity, header, keys):
    schema =    {
                    "type": "object",
                    "properties": {}
                }
    header_map = []
    for column in header:
        #for now everything is a string; ideas for later:
        #1. intelligently detect data types based on a sampling of entries from the raw data
        #2. by default everything is a string, but allow entries in config.json to hard-type columns by name
        schema["properties"][column] = {"type": "string" }
        header_map.append(column)

    singer.write_schema(entity, schema, keys)

    return header_map

def process_file(fileInfo):
    #determines if file in question is a file or directory and processes accordingly
    if not os.path.exists(fileInfo["file"]):
        logger.info(fileInfo["file"] + " does not exist, skipping")
        return
    if os.path.isdir(fileInfo["file"]):
        fileInfo["file"] = os.path.normpath(fileInfo["file"]) + os.sep #ensures directories end with trailing slash
        logger.info("Syncing all CSV files in directory '" + fileInfo["file"] + "' recursively")
        for filename in os.listdir(fileInfo["file"]):
            subInfo = copy.deepcopy(fileInfo)
            subInfo["file"] = fileInfo["file"] + filename
            process_file(subInfo) #recursive call
    else:
        sync_file(fileInfo)

def sync_file(fileInfo):
    if fileInfo["file"][-4:] != ".csv":
        logger.info("Skipping non-csv file '" + fileInfo["file"] + "'")
        logger.info("Please provide a CSV file that ends with '.csv'; e.g. 'users.csv'")
        return

    logger.info("Syncing entity '" + fileInfo["entity"] + "' from file: '" + fileInfo["file"] + "'")
    with open(fileInfo["file"], "r") as f:
        needsHeader = True
        reader = csv.reader(f)
        for row in reader:
            if(needsHeader):
                header_map = write_schema_from_header(fileInfo["entity"], row, fileInfo["keys"])
                needsHeader = False
            else:
                record = {}
                for index, column in enumerate(row):
                    record[header_map[index]] = column
                if len(record) > 0: #skip empty lines
                    singer.write_record(fileInfo["entity"], record)

    singer.write_state(STATE) #moot instruction, state always empty

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Config file', required=False)
    parser.add_argument('-s', '--state', help='State file', required=False)
    parser.add_argument("-p", "--properties", help="Property selections", required=False)
    parser.add_argument("--catalog", help="Catalog file", required=False)
    parser.add_argument("-d", "--discover", action='store_true', help="Do schema discovery", required=False)
    return parser.parse_args()

def load_json(path):
    with open(path) as f:
        return json.load(f)

def check_config(config, required_keys):
    missing_keys = [key for key in required_keys if key not in config]
    if missing_keys:
        logger.error("tap-csv: Config is missing required keys: {}".format(missing_keys))
        exit(1)

def do_sync():
    logger.info("Starting sync")

    csv_files_definition = CONFIG.get("csv_files_definition", None)
    if csv_files_definition:
        if os.path.isfile(csv_files_definition):
            csv_files = load_json(csv_files_definition)
        else:
            logger.error("tap-csv: '{}' file not found".format(csv_files_definition))
            exit(1)
    else:
        check_config(CONFIG, REQUIRED_CONFIG_KEYS)
        csv_files = CONFIG['files']

    for fileInfo in csv_files:
        process_file(fileInfo)
    logger.info("Sync completed")

def main():
    args = parse_args()

    if args.discover:
        catalog = {'streams': []}
        print(json.dumps(catalog, indent=2))
    elif not args.config:
        logger.error("tap-csv: the following arguments are required: -c/--config")
        exit(1)
    else:
        config = load_json(args.config)

        if args.state:
            state = load_json(args.state)
        else:
            state = {}

        CONFIG.update(config)
        STATE.update(state)
        do_sync()


if __name__ == '__main__':
    main()
