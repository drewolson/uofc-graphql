#!/usr/bin/env bash

dir=$(pwd)
rm $dir/lambda.zip
rm $dir/requirements.txt
rm -rf $dir/dependencies
pipenv lock --requirements > requirements.txt
pipenv run pip install --target ./dependencies -r ./requirements.txt
pushd ./dependencies
zip -r $dir/lambda.zip .
popd
zip -g lambda.zip $1
rm $dir/requirements.txt
rm -rf $dir/dependencies
