#!/bin/sh
# NNIdenSys/Results $sh evaluation.sh ST2 RNN 2018.September.14.
dataset=ST2 #$1
list="FR"
xp=SVM #$2
date=Feb.18 #$3
evalMini=trainvsdev.
seed=0
folder = MLP/TrainVsDev/Tendy/0
list="BG DE EL EN ES EU FA FR HE HI HR HU IT LT PL PT RO SL TR"
for i in $list
        do
            echo "Evaluating:  $i"
            python3 validate_cupt.py --input /Users/halsaied/PycharmProjects/MWE.Identification/Results/Evaluation/Data/$$folder/$evalMini.$seed.$date.$i.cupt
            python3 evaluate.py --gold Output/$$folder/$evalMini.$seed.$date.$i.gold.cupt --pred /Users/halsaied/PycharmProjects/MWE.Identification/Results/Evaluation/Data/$$folder/$evalMini.$seed.$date.$i.cupt --train /Users/halsaied/PycharmProjects/MWE.Identification/Results/Evaluation/Data/$$folder/$evalMini.$seed.$date.$i.train.cupt
        done
