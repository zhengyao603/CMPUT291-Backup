
sort -o pterms.txt -u pterms.txt
sort -o rterms.txt -u rterms.txt
sort -o scores.txt -u scores.txt

cat reviews.txt | perl break.pl | db_load -c duplicates=1 -T -t hash rw.idx
cat pterms.txt | perl break.pl | db_load -c duplicates=1 -T -t btree pt.idx
cat rterms.txt | perl break.pl | db_load -c duplicates=1 -T -t btree rt.idx
cat scores.txt | perl break.pl | db_load -c duplicates=1 -T -t btree sc.idx