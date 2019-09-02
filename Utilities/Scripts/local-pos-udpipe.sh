
echo "Training:  FR"
/Users/halsaied/Downloads/udpipe/bin-osx/udpipe --train --tokenizer=none --parser=none --tagger ressources/POSModel/FR.model.udpipe ressources/sharedtask.2/FR/train.conll
#/Users/halsaied/Downloads/udpipe/bin-osx/udpipe --tokenizer=none --parser=none --tagger --tag ressources/POSModel/FR.model.udpipe   ressources/sharedtask.2/FR/train.conll
echo "Evaluating dev:  FR"
/Users/halsaied/Downloads/udpipe/bin-osx/udpipe --accuracy --tagger ressources/POSModel/FR.model.udpipe ressources/sharedtask.2/FR/dev.conll
echo "Evaluating test:  FR"
/Users/halsaied/Downloads/udpipe/bin-osx/udpipe --accuracy --tagger ressources/POSModel/FR.model.udpipe ressources/sharedtask.2/FR/test.conll
