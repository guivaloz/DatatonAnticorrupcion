
# Dataton Anticorrupcion 2018

### Objetivo

Es un ejercicio sobre cómo alimentar los datos abiertos de CompraNet a una base de datos PostgreSQL.

Todo el conjunto está preparado para trabajar con contenedores Docker y carga una instancia de PGAdmin4.

Tiene dos componentes principales:

1. Scripts para la creación y alimentación de la BD con Click de Python.
2. Un sistema web que usa Flask, que también programado en Python.

### Screenshots

Por agregar.

### Instalación

Por escribir.

### Secciones del código destacables

La definición del modelo de la tabla está en `dataton_anticorrupcion/blueprints/contrataciones_abiertas/models.py`

    ocid = db.Column(db.String())
    tag = db.Column(db.String())
    date = db.Column(db.DateTime())
    buyer_name = db.Column(db.String())
    parties = db.Column(db.JSON())
    contracts = db.Column(db.JSON())
    contracts_title = db.Column(db.String())
    contracts_amount = db.Column(db.Float())
    contracts_supplier = db.Column(db.String())

El script de alimentación debe concordar con la definición del modelo, está en `cli/commands/cmd_compranet.py`

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

### Licencia de Software Libre

Es Software Libre con licencia GNU GENERAL PUBLIC LICENSE, Version 3. Lea el archivo LICENSE.
