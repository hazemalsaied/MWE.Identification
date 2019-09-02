#!/bin/sh
# mai 2019
source /home/halsaied/miniconda2/bin/activate
cd /home/halsaied/udpipe-1.2.0-bin
env MKL_THREADING_LAYER=GNU
list="DE ES EU HU IT PL SL TR"
#list="BG DE EL EN ES EU FA FR HE HI HR HU IT PL PT RO SL TR"
for i in $list
        do
            echo "Training:  $i"
            bin-linux64/udpipe --tagger=none --tokenizer=none --parser single_root=0 use_gold_tags=1 --train /home/halsaied/NNIdenSys/ressources/DepParsers/$i.model.udpipe   /home/halsaied/NNIdenSys/ressources/sharedtask.2/$i/train.conll
            echo "Evaluating dev:  $i"
            bin-linux64/udpipe --accuracy --parser single_root=0 use_gold_tags=1 /home/halsaied/NNIdenSys/ressources/DepParsers/$i.model.udpipe /home/halsaied/NNIdenSys/ressources/sharedtask.2/$i/dev.conll
            echo "Evaluating test:  $i"
            bin-linux64/udpipe --accuracy --parser single_root=0 use_gold_tags=1 /home/halsaied/NNIdenSys/ressources/DepParsers/$i.model.udpipe /home/halsaied/NNIdenSys/ressources/sharedtask.2/$i/test.conll
        done
