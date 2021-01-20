echo This script gather COVID-19 twitter data of a specific date

cd data
mkdir -p raw
cd raw
curl -LJ -o $1.tsv.gz https://github.com/thepanacealab/covid19_twitter/blob/master/dailies/$1/$1-dataset.tsv.gz?raw=true
echo
gzip -d $1.tsv.gz
python ../../src/data/collection_script/get_IDs.py $1
rm $1.tsv
twarc hydrate $1.txt > $1.json