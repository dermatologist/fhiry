import click
import sys
import json
from pathlib import Path


@click.command()
@click.option('--input', '-i', 'input_path', type=click.Path(exists=True, file_okay=False), help='Input folder with FHIR bundles or ndjson files.')
@click.option('--output', '-o', 'output_path', type=click.Path(), help='Output file path for the dataframe (CSV/JSON/Parquet).')
@click.option('--flatten', is_flag=True, help='Flatten FHIR resources for LLM/text output.')
@click.option('--url', help='FHIR server base URL for search.')
@click.option('--resource-type', help='FHIR resource type for server search (e.g., Patient, Condition).')
@click.option('--query', help='FHIR search parameters as JSON string.')
def cli(input_path, output_path, flatten, url, resource_type, query):
    """
    Process FHIR data from folder or FHIR server and output as dataframe.
    """
    if url:
        from fhiry.fhirsearch import Fhirsearch
        params = json.loads(query) if query else {}
        fs = Fhirsearch(fhir_base_url=url)
        df = fs.search(resource_type=resource_type, search_parameters=params)
    elif input_path:
        import fhiry.parallel as fp
        # Try ndjson first, fallback to process
        ndjson_files = list(Path(input_path).glob("*.ndjson"))
        if ndjson_files:
            df = fp.ndjson(input_path)
        else:
            df = fp.process(input_path)
    else:
        click.echo("Please provide either --input or --url.", err=True)
        sys.exit(1)

    if flatten:
        from fhiry.flattenfhir import FlattenFhir
        # Flatten each row's resource
        df['flattened'] = df['resource'].apply(lambda r: FlattenFhir(r).flattened if r else None)

    if output_path:
        ext = Path(output_path).suffix.lower()
        if ext == ".csv":
            df.to_csv(output_path, index=False)
        elif ext == ".json":
            df.to_json(output_path, orient="records", lines=True)
        elif ext == ".parquet":
            df.to_parquet(output_path, index=False)
        else:
            click.echo("Unsupported output file format. Use .csv, .json, or .parquet.", err=True)
            sys.exit(1)
        click.echo(f"Output written to {output_path}")
    else:
        click.echo(df.info())
        click.echo(df.head().to_string())

if __name__ == "__main__":
    cli()