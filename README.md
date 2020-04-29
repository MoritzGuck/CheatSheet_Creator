# CheatSheet_Creator

A program that creates minimalist programming-cheatsheets from JSON-  and YAML-files.

## Features

At the moment, the following features are supported:
- Document title (with adaptable size and position)
- Text paragraphs (with adaptable fonts and sizes)
- Table paragraphs (with adaptabe font sizes)

Take a look at the [VS Code Cheatsheet](VS&#32;Code&#32;Cheatsheet.pdf) to get an idea.

All changes to the content of the cheatsheet are made in [content.json](content.json). (This should be self explanatory - if not: raise an issue.)

Changes to the design are made in [design.json](design.json). (A documentation will follow once more adaptations are available.)

## Set-up

CheatSheet_Creator relies on ReportLab's open source libary. You can install it like this from your terminal:

Making your own virtual enviroment:

    $ python -m virtualenv .  
    $ pip install reportlab

Using the virtual environment:

    $ cd CheatSheet_Creator
    $ . bin/activate
    $ cd ..

A userguide for reportlab can be found here: https://www.reportlab.com/docs/reportlab-userguide.pdf

## Run the code

Create a PDF-cheatsheet by running [pdf_generator.py](pdf_generator.py) in your terminal

    $ python pdf_generator.py --c content.json --o ./pdfs/

--c is the file containing the content, --o is the output directory.