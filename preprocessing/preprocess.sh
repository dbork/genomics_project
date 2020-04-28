#!/bin/bash

echo 'Please enter data subdirectory.'

read subdir

for filename in ~/Documents/genomics_project/code/data/$subdir/*.txt.gz; do
	gunzip $filename
done

python raw_to_expression_matrix.py $subdir
