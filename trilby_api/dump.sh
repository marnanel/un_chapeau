#!/bin/bash

python manage.py dumpdata trilby_api --indent 4 --output trilby_api/fixtures/alicebobcarol.json
