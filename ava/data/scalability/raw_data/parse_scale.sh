DIR=.
OUTDIR=$DIR
scale=16
b="scale_${scale}"

grep "^[0-9]\+\.[0-9]\+" $OUTDIR/$b.txt | \
    awk '{ total += $1; count++ } END {
           if (count > 0)
               print total/count;
           else
               print -1
         }' \
