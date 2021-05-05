#!/usr/bin/env bash

dir=$(pwd)
output=$dir/.build
rm $dir/lambda.zip
mkdir $output
pipenv lock --requirements > $output/requirements.txt
pipenv run pip install --target $output/dependencies -r $output/requirements.txt
pushd $output/dependencies
zip -r $dir/lambda.zip .
popd
zip -g lambda.zip $1
