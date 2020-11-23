import pandas as pd
import argparse
import json
import os


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


def add_stream(catalog, df, stream_name):
    # Build the stream
    stream = {
        "schema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {}
        },
        "metadata": []
    }

    stream["stream"] = stream_name
    stream["tap_stream_id"] = stream_name

    for col_name in df.columns:
        stream["schema"]["properties"][col_name] = {
            "type": "string"
        }

        stream["metadata"].append({
            "breadcrumb": [
                "properties",
                col_name
            ],
            "metadata": {
                "inclusion": "automatic",
                "selected-by-default": True
            }
        })

    # Add to catalog
    catalog["streams"].append(stream)


def discover_file(path, catalog, name=None):
    if path.endswith('.csv'):
        stream_name = path if name is None else name
        df = pd.read_csv(path)
        add_stream(catalog, df, stream_name)
    else:
        xl = pd.ExcelFile(path)

        # Read every sheet as it's own stream
        for sheet in xl.sheet_names:
            df = xl.parse(sheet)
            add_stream(catalog, df, sheet)


def discover(config):
    # Get all files from config.json
    files = config.get("files", None)

    if not files:
        print("tap-csv: config has no files specified")
        exit(1)

    # Generate catalog
    catalog = {'streams': []}

    for f in files:
        # Read the CSV/Excel file into Dataframe
        df = None

        if os.path.isdir(f['path']):
            for filename in os.listdir(f['path']):
                discover_file(os.path.join(f['path'], filename), catalog, filename)
        else:
            discover_file(f['path'], catalog)

    return catalog


def main():
    args = parse_args()

    if not args.config:
        print("tap-csv: the following arguments are required: -c/--config")
        exit(1)

    # Load config
    config = load_json(args.config)

    if args.discover:
        catalog = discover(config)
        print(json.dumps(catalog, indent=2))
    else:
        print("tap-csv: unsupported arg given.")


if __name__ == '__main__':
    main()
