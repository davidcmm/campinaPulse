#!/bin/bash

python geraHtmlTopBottom5.py reg-bai-med-data-agrad.dat Agradavel
mv topbot5.html topbot5-agrad-bai-med.html

python geraHtmlTopBottom5.py reg-bai-med-data-seg.dat Seguro
mv topbot5.html topbot5-seg-bai-med.html

python geraHtmlTopBottom5.py reg-jov-adu-data-agrad.dat Agradavel
mv topbot5.html topbot5-agrad-jov-adu.html

python geraHtmlTopBottom5.py reg-jov-adu-data-seg.dat Seguro
mv topbot5.html topbot5-seg-jov-adu.html

python geraHtmlTopBottom5.py reg-cas-sol-data-agrad.dat Agradavel
mv topbot5.html topbot5-agrad-cas-sol.html

python geraHtmlTopBottom5.py reg-cas-sol-data-seg.dat Seguro
mv topbot5.html topbot5-seg-cas-sol.html

python geraHtmlTopBottom5.py reg-hom-mul-data-agrad.dat Agradavel
mv topbot5.html topbot5-agrad-hom-mul.html

python geraHtmlTopBottom5.py reg-cas-sol-data-seg.dat Seguro
mv topbot5.html topbot5-seg-hom-mul.html
