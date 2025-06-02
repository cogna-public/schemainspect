# Architecture

## Overview

Essentially, this package:
1. Connects to a Postgres DB
2. Runs a bunch of SQL to understand the schema of the full DB
3. Adds some additional helpers to provide templates to edit the schema of the DB

## Main class

The main item to look at is the `PostgreSQL DBInspector` in `obj.py`

What it does is
1. Run the queries in `pg/sql` (Editing them depending on the PG version)
2. Store them on the same object

## Other objects
For each item in a database's schema, for example `views`, `tables`, `comments`, there will be a corresponding class in `schemainspect`, along with helpers for `create`, `drop` and possibly other statements

## Depedencies
Each object needs to have their `depends_on` properly populated in order for `migra` to know what has to be deleted and recreated in the case of a destructive migration

This is done through the `deps.sql` query and its relevant parsing methods