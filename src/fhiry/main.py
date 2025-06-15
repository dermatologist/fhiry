"""
Copyright (c) 2025 Bell Eapen

This software is released under the MIT License.
https://opensource.org/licenses/MIT
"""

import json
import sys
from pathlib import Path

import click
import pandas as pd


@click.command()
@click.option(
    "--input",
    "-i",
    "input_path",
    type=click.Path(exists=True, file_okay=False),
    help="Input folder with FHIR bundles or ndjson files.",
)
@click.option(
    "--output",
    "-o",
    "output_path",
    type=click.Path(),
    help="Output file path for the dataframe (CSV/JSON/Parquet).",
)
@click.option(
    "--flatten", is_flag=True, help="Flatten FHIR resources for LLM/text output."
)
@click.option("--url", help="FHIR server base URL for search.")
@click.option(
    "--search-type", help="FHIR resource type for server search (e.g. Condition)."
)
@click.option(
    "--resource-types",
    help="Comma separated list of FHIR resource types (e.g. Encounter,Condition).",
)
@click.option("--query", help="FHIR search parameters as JSON string.")
@click.option(
    "--config-file", type=click.Path(exists=True), help="Path to configuration file."
)
def cli(
    input_path,
    output_path,
    flatten,
    url,
    search_type,
    resource_types,
    query,
    config_file,
):
    """
    Process FHIR data from folder or FHIR server and output as dataframe.
    """
    if url:
        from fhiry.fhirsearch import Fhirsearch

        params = json.loads(query) if query else {}
        fs = Fhirsearch(fhir_base_url=url)
        df = fs.search(resource_type=search_type, search_parameters=params)
    elif input_path:
        import fhiry.parallel as fp

        # read config file to config_json
        config = {"REMOVE": ["text.div", "meta"], "RENAME": {}}
        config_json = json.dumps(config)
        if config_file:
            try:
                with open(config_file, "r") as f:
                    config_json = json.load(f)
            except Exception as e:
                click.echo(f"Error reading config file: {e}", err=True)
                sys.exit(1)
        # Try ndjson first, fallback to process
        ndjson_files = list(Path(input_path).glob("*.ndjson"))
        if ndjson_files:
            df = fp.ndjson(input_path, config_json=config_json)
        else:
            df = fp.process(input_path, config_json=config_json)
        if df.empty:
            click.echo("No data found.", err=True)
            sys.exit(1)
    else:
        click.echo("Please provide either --input or --url.", err=True)
        sys.exit(1)

    if df is None or df.empty:
        click.echo("No data found in the input.", err=True)
        sys.exit(1)

    if flatten:
        from fhiry.flattenfhir import FlattenFhir

        # Flatten each row's resource
        df["flattened"] = df["resource"].apply(
            lambda r: FlattenFhir(r).flattened if r else None
        )

    if output_path:
        ext = Path(output_path).suffix.lower()
        # Filter on resourceTypes if specified
        if resource_types:
            try:
                resource_types = [rt.strip() for rt in resource_types.split(",")]
                col = (
                    "resource.resourceType"
                    if "resource.resourceType" in df.columns
                    else "resourceType"
                )
                df = df[df[col].isin(resource_types)]
            except Exception as e:
                click.echo(f"Error filtering resource types: {e}", err=True)
                sys.exit(1)
        if ext == ".csv":
            df.to_csv(output_path, index=False)
        elif ext == ".xlsx":
            if resource_types:
                try:
                    # filter on resource types and send to separate sheets
                    with pd.ExcelWriter(output_path) as writer:
                        for rt in resource_types:
                            _df = df[df["resourceType"] == rt].copy()
                            _df.dropna(axis=1, thresh=0.1, inplace=True)
                            _df.to_excel(writer, sheet_name=rt, index=False)
                except Exception as e:
                    click.echo(f"Error writing to Excel: {e}", err=True)
                    sys.exit(1)
            else:
                df.to_excel(output_path, index=False)
        elif ext == ".parquet":
            df.to_parquet(output_path, index=False)
        else:
            click.echo(
                "Unsupported output file format. Use .csv, .json, or .parquet.",
                err=True,
            )
            sys.exit(1)
        click.echo(f"Output written to {output_path}")
    else:
        click.echo(df.info())
        click.echo(df.head().to_string())


if __name__ == "__main__":
    cli()
