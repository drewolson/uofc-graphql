#!/bin/bash

pandoc -t beamer --filter pandoc-include-code --filter pandoc-plantuml presentation.md -o presentation.pdf
