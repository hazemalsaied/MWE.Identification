#!/bin/sh
# mai 2019
source /home/halsaied/miniconda2/bin/activate
cd /home/halsaied/udpipe-1.2.0-bin
env MKL_THREADING_LAYER=GNU
#list="BG DE EL EN ES EU FA FR HE HI HR HU IT PL PT RO SL TR"
list="SL TR"
for i in $list
        do
            echo "Training:  $i"
            bin-linux64/udpipe --train --tokenizer=none --parser=none --tagger /home/halsaied/NNIdenSys/ressources/POSModel/$i.model.udpipe   /home/halsaied/NNIdenSys/ressources/sharedtask.2/$i/train.conll
            # bin-linux64/udpipe --train --tokenizer=none --parser=none --tagger use_xpostag=0 provide_xpostag=0 /home/halsaied/NNIdenSys/ressources/POSModel/$i.model.udpipe   /home/halsaied/NNIdenSys/ressources/sharedtask.2/$i/train.conll
            echo "Evaluating dev:  $i"
            bin-linux64/udpipe --accuracy --tag /home/halsaied/NNIdenSys/ressources/POSModel/$i.model.udpipe /home/halsaied/NNIdenSys/ressources/sharedtask.2/$i/dev.conll
            echo "Evaluating test:  $i"
            bin-linux64/udpipe --accuracy --tag /home/halsaied/NNIdenSys/ressources/POSModel/$i.model.udpipe /home/halsaied/NNIdenSys/ressources/sharedtask.2/$i/test.conll
        done
