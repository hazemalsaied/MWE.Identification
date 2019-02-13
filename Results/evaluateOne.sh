#!/bin/sh
dataset=ST2 #$1
xp=Linear #$2
date=22.01 #$3
eval=FixedSize
evalMini=fixedsize
lang=FR
python3 bin/validate_cupt.py --input Output/$dataset/$xp/$date.$evalMini.$lang.cupt
python3 bin/evaluate.py --gold Output/$dataset/$xp/$date.$evalMini.$lang.gold.cupt --pred Output/$dataset/$xp/$date.$evalMini.$lang.cupt --train Output/$dataset/$xp/$date.$evalMini.$lang.train.cupt