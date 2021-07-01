#!/bin/bash

rm -rf bathhouse flag_part_2* *.jpeg *.zip *.mp3 problem

set -e

mkdir flag_part_2
cd flag_part_2
echo '_dont_forget_5736h1d3}' >> flag_part_2.txt
cd ..
tar -czvf flag_part_2.tar.gz flag_part_2/*

cp source/pre_steg.jpeg .
steghide embed -p 'p4$$w0Rd' -N -ef flag_part_2.tar.gz -cf pre_steg.jpeg -sf post_steg.jpeg

cp source/polish_cow.mp3 .
./embed_image.py

mkdir bathhouse
mv polish_cow.mp3 bathhouse

zip -P 'this_is_the_first_password_so_creative_right' bathhouse.zip bathhouse/*

mkdir problem
mv bathhouse.zip problem

cp source/first_password.pdf .
./xor_file.py
rm first_password.pdf
mv bathhouse_password problem

tar -czvf russian-nesting-bathhouse.zip problem/*

 