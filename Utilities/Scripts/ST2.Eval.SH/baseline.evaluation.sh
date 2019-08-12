#!/bin/sh
# NNIdenSys/Results $sh evaluation.sh ST2 RNN 2018.September.14.
list="BG CS DE EL ES FA FR HE HU IT LT MT PL PT RO SV SL TR"
list2="1 2 3 4 5"
for i in $list
        do
            for j in $list2
                do
                     echo "Evaluating:  $i$j"
                    python3 evaluate.py --gold /Users/halsaied/PycharmProjects/MWE.Identification/Results/baseline-cv/$i$j.gold.txt.cupt --pred /Users/halsaied/PycharmProjects/MWE.Identification/Results/baseline-cv/$i$j.txt.cupt --train /Users/halsaied/PycharmProjects/MWE.Identification/Results/baseline-cv/$i$j.train.cupt
                done
        done
