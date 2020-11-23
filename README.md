# tap-csv

A [Singer](https://singer.io) tap for extracting data from a CSV/XLSX file.

## Limitations

This tap-csv implementation only handles the generation of a catalog (discover).

## Run

#### Run the application

```bash
tap_csv -c config.json -d
```

Where `config.json` contains an array called `files` that consists of dictionary objects detailing each destination table to be passed to Singer. Each of those entries contains: 
* `path`: Local path to the file to be ingested. Note that this may be a directory, in which case all files in that directory and any of its subdirectories will be recursively processed

Example:

```json
{
	"files": [ 	
		{
			"path" : "/path/to/leads.csv"
		},
		{
			"file" : "/path/to/opportunities.csv"
		}
	]
}
```

## Initial Tap Repo

This tap is based on the following `tap-csv` project: https://gitlab.com/meltano/tap-csv
