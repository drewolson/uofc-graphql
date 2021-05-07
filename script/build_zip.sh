#!/usr/bin/env bash

if [ -z "$1" ]
then
  echo "Usage: ./script/build_zip.sh [filename]"
  exit 1
fi

dir=$(pwd)
output=$dir/output
build=$output/build
rm $output/lambda.zip
mkdir -p $build
pipenv lock --requirements > $build/requirements.txt
pipenv run pip install --target $build/dependencies -r $build/requirements.txt
pushd $build/dependencies
zip -r $output/lambda.zip .
cp $dir/$1 ./lambda_function.py
zip -g $output/lambda.zip lambda_function.py
popd
