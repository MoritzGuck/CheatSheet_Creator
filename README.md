# CheatSheet_Creator

A program that creates cheatsheets from JSON-files.

## Set-up

CheatSheet_Creator relies on ReportLabs open source libary. You can install it like this from your terminal: 

    $ cd CheatSheet_Creator
    $ python -m virtualenv .
    $ . bin/activate
    $ pip install reportlab

A userguide for reportlab can be found here: https://www.reportlab.com/docs/reportlab-userguide.pdf

## Run the code

Create a PDF-cheatsheet by running in your terminal

    python pdf_generator.py
