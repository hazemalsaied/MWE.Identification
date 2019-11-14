

/Users/halsaied/PycharmProjects/MWE.Identification/ressources/DepParsers/
    /Users/halsaied/Downloads/udpipe/bin-osx/udpipe --tagger=none --tokenizer=none --parser use_gold_tags=1 --train --heldout=/Users/halsaied/PycharmProjects/MWE.Identification/ressources/sharedtask.2/TR/dev.conll TR.model.output   /Users/halsaied/PycharmProjects/MWE.Identification/ressources/sharedtask.2/TR/train.conll

/Users/halsaied/Downloads/udpipe/bin-osx/udpipe --tagger=none --tokenizer=none --parser use_gold_tags=1 --train TR.model.noheldout.output   /Users/halsaied/PycharmProjects/MWE.Identification/ressources/sharedtask.2/TR/train.conll
/Users/halsaied/Downloads/udpipe/bin-osx/udpipe --accuracy --tagger=none --tokenizer=none --parser use_gold_tags=1 /Users/halsaied/PycharmProjects/MWE.Identification/Reports/TR.model.udpipe /Users/halsaied/PycharmProjects/MWE.Identification/ressources/sharedtask.2/TR/dev.conll