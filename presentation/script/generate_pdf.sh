#!/bin/bash

pandoc -t beamer --filter pandoc-include-code presentation.md -o presentation.pdf
