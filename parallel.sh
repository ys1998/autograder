#!/bin/bash

src_dir='Lab2'
n=10

nr=$( wc -l $src_dir/roll_list.txt | cut -d' ' -f1 )
nj=$(( $nr / $n ))

cp $src_dir/roll_list.txt temp_roll_list.txt

for i in $( seq 1 $n ); do
	mkdir _job_$i
	cp -rf $src_dir/* _job_$i
	head -n $nj temp_roll_list.txt > _job_$i/roll_list.txt
	tail -n +$(( $nj+1 )) temp_roll_list.txt > __temp
	mv __temp temp_roll_list.txt
done

if (( $nr % $n != 0 )); then
	mkdir _job_$(( $n+1 ))
	cp -rf $src_dir/* _job_$(( $n+1 ))
	mv temp_roll_list.txt _job_$(( $n+1 ))/roll_list.txt
else
	rm temp_roll_list.txt
fi

for f in $( find -name '_job_*' ); do 
	( 
		pushd $f; 
		python3 grade.py; 
		popd; 
	) & 
done; 

wait;

mv _job_1/marks.tsv $src_dir
for i in $( seq 2 $n ); do
	tail -n +2 _job_$i/marks.tsv >> $src_dir/marks.tsv;
done

rm -rf _job_*;