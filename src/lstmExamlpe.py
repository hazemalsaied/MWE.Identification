import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.nn.functional as f
torch.manual_seed(1)
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
lstm = nn.LSTM(3, 3)  # Input dim is 3, output dim is 3
inputs = [torch.randn(1, 3) for _ in range(5)]  # make a sequence of length 5

# initialize the hidden state.
hidden = (torch.randn(1, 1, 3),
          torch.randn(1, 1, 3))
for i in inputs:
    # Step through the sequence one element at a time.
    # after each step, hidden contains the hidden state.
    out, hidden = lstm(i.view(1, 1, -1), hidden)

# alternatively, we can do the entire sequence all at once.
# the first value returned by LSTM is all of the hidden states throughout
# the sequence. the second is just the most recent hidden state
# (compare the last slice of "out" with "hidden" below, they are the same)
# The reason for this is that:
# "out" will give you access to all hidden states in the sequence
# "hidden" will allow you to continue the sequence and backpropagate,
# by passing it as an argument  to the lstm at a later time
# Add the extra 2nd dimension
inputs = torch.cat(inputs).view(len(inputs), 1, -1)
hidden = (torch.randn(1, 1, 3), torch.randn(1, 1, 3))  # clean out hidden state
out, hidden = lstm(inputs, hidden)
print(out)
print(hidden)

def prepare_sequence(seq, to_ix):
    idxs = [to_ix[w] for w in seq]
    return torch.tensor(idxs, dtype=torch.long)


training_data = [
    ("The dog ate the apple".split(), ["DET", "NN", "V", "DET", "NN"]),
    ("Everybody read that book".split(), ["NN", "V", "DET", "NN"])
]
word_to_ix = {}
for sent, tags in training_data:
    for word in sent:
        if word not in word_to_ix:
            word_to_ix[word] = len(word_to_ix)
print(word_to_ix)
tag_to_ix = {"DET": 0, "NN": 1, "V": 2}

# These will usually be more like 32 or 64 dimensional.
# We will keep them small, so we can see how the weights change as we train.
EMBEDDING_DIM = 3
RNN_HIDDEN_DIM = 7
BIDIRECTIONAL = True
RNN_LAYER_NUM = 1
DENSE_1 = 13
DENSE_DROPOUT = 0.3
FOCUSED_ELEM_NUM = 5

global bidireCoeff
bidireCoeff = 1 + int(BIDIRECTIONAL)


class LSTMTagger(nn.Module):

    def __init__(self,   vocab_size, tagset_size):
        super(LSTMTagger, self).__init__()

        self.word_embeddings = nn.Embedding(vocab_size, EMBEDDING_DIM)

        # The LSTM takes word embeddings as inputs, and outputs hidden states
        # with dimensionality hidden_dim.
        self.lstm = nn.LSTM(EMBEDDING_DIM, RNN_HIDDEN_DIM, bidirectional=BIDIRECTIONAL, num_layers=RNN_LAYER_NUM)

        self.linear1 = nn.Linear(FOCUSED_ELEM_NUM * RNN_HIDDEN_DIM * bidireCoeff, DENSE_1)
        # dropout here is very detrimental
        self.dropout1 = nn.Dropout(p=DENSE_DROPOUT)

        # The linear layer that maps from hidden state space to tag space
        self.hidden2tag = nn.Linear(DENSE_1, tagset_size)

    def forward(self, sentence):
        embeds = self.word_embeddings(sentence)
        lstm_out, _ = self.lstm(embeds.view(len(sentence), 1, -1))
        selectedRows =  selectRowsFromTensors(lstm_out)
        out = f.relu(self.linear1(selectedRows.view(FOCUSED_ELEM_NUM* bidireCoeff * RNN_HIDDEN_DIM, )))
        # out = f.relu(self.linear1(lstm_out.view(len(sentence), -1)))
        out = self.dropout1(out)
        out = self.hidden2tag(out)
        print out
        tag_scores = F.log_softmax(out, dim=1)
        return tag_scores

def selectRowsFromTensors(lstmOut):
    """
    extract given rows (= axis 0) from a given 2 dim tensor
    """
    idxss = [1, 3, 1]

    results = torch.zeros((FOCUSED_ELEM_NUM, bidireCoeff * RNN_HIDDEN_DIM), device=device)
    idx = 0
    for selectedIdx in idxss:
        if selectedIdx != -1 and selectedIdx < 100:
            results[idx] = lstmOut[selectedIdx]
        idx += 1
    print 'selected row tensor'
    print results
    return results


model = LSTMTagger(len(word_to_ix), len(tag_to_ix)).to(device)
loss_function = nn.NLLLoss()
optimizer = optim.SGD(model.parameters(), lr=0.1)

# See what the scores are before training
# Note that element i,j of the output is the score for tag j for word i.
# Here we don't need to train, so the code is wrapped in torch.no_grad()
with torch.no_grad():
    inputs = prepare_sequence(training_data[0][0], word_to_ix).to(device)
    tag_scores = model(inputs)
    print(tag_scores)

for epoch in range(300):  # again, normally you would NOT do 300 epochs, it is toy data
    for sentence, tags in training_data:
        # Step 1. Remember that Pytorch accumulates gradients.
        # We need to clear them out before each instance
        model.zero_grad()

        # Step 2. Get our inputs ready for the network, that is, turn them into
        # Tensors of word indices.
        sentence_in = prepare_sequence(sentence, word_to_ix).to(device)
        targets = prepare_sequence(tags, tag_to_ix).to(device)

        # Step 3. Run our forward pass.
        tag_scores = model(sentence_in)

        # Step 4. Compute the loss, gradients, and update the parameters by
        #  calling optimizer.step()
        loss = loss_function(tag_scores, targets)
        loss.backward()
        optimizer.step()

# See what the scores are after training
with torch.no_grad():
    inputs = prepare_sequence(training_data[0][0], word_to_ix).to(device)
    tag_scores = model(inputs)

    # The sentence is "the dog ate the apple".  i,j corresponds to score for tag j
    # for word i. The predicted tag is the maximum scoring tag.
    # Here, we can see the predicted sequence below is 0 1 2 0 1
    # since 0 is index of the maximum value of row 1,
    # 1 is the index of maximum value of row 2, etc.
    # Which is DET NOUN VERB DET NOUN, the correct sequence!
    print(tag_scores)