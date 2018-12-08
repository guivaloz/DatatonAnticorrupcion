import click
import csv
import json
import os
import sys

from dataton_anticorrupcion.app import create_app
from dataton_anticorrupcion.extensions import db

from dataton_anticorrupcion.blueprints.contrataciones_abiertas.models import ContratacionesAbiertas

# Input files
contrataciones_abiertas_cvs_file = 'instance/contratacionesabiertas_bulk_paquete1.csv'

# Create an app context for the database connection
app = create_app()
db.app = app

# Para evitar el error
# _csv.Error: field larger than field limit
# https://stackoverflow.com/questions/15063936/csv-error-field-larger-than-field-limit-131072
# Inicia
maxInt = sys.maxsize
decrement = True

while decrement:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.
    decrement = False
    try:
        csv.field_size_limit(maxInt)
    except OverflowError:
        maxInt = int(maxInt/10)
        decrement = True
# Termina

def seed_contrataciones_abiertas():
    if os.path.isfile(contrataciones_abiertas_cvs_file):
        with open(contrataciones_abiertas_cvs_file) as pointer:
            count = 0
            reader = csv.DictReader(pointer)
            for row in reader:
                # Get contracts
                contracts = json.loads(row['compiledRelease.contracts'])
                contract_first = contracts.pop()
                contract_value_with_tax = contract_first['valueWithTax']
                contract_suppliers = contract_first['suppliers']
                if len(contract_suppliers) > 0:
                    contract_supplier_first = contract_suppliers.pop()
                    contracts_supplier = contract_supplier_first['name']
                else:
                    contracts_supplier = ''
                #contract_details = contract_first['contractDetails']
                # Define register
                contratacion_abierta = {
                    'ocid': row['ocid'],
                    'tag': row['compiledRelease.tag'],
                    'date': row['compiledRelease.date'],
                    'buyer_name': row['compiledRelease.buyer.name'],
                    'parties': row['compiledRelease.parties'],
                    'contracts': row['compiledRelease.contracts'],
                    'contracts_title': contract_first['title'],
                    'contracts_amount': contract_value_with_tax['amount'],
                    'contracts_supplier': contracts_supplier,
                }
                # Save
                ContratacionesAbiertas(**contratacion_abierta).save()
                # Only 1000
                count += 1
                if count >= 1000:
                    break
    else:
        raise Exception('Error: Input file {0} not found.'.format(contrataciones_abiertas_cvs_file))


@click.group()
def cli():
    pass


@click.command()
def seed():
    seed_contrataciones_abiertas()
    return(None)


cli.add_command(seed)
