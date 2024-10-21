### How to optimize the Convolutional Neural network

First tried to borrow the code from handwriting examples, and diretly use its configuration, the result was so bad, the accuracy is about 0.0598 after 10 Epoch. the loss is as high as 3.489.

So I am considering do some experiemnts by modifying the configurations of the neural network. Here are the modification and its result:

#### Experiment 1: additional convolutional layer
Add 2nd Convolutional layer, with similar configure to the previous convolutional layer, also add a Max Pooling layer after each Convolutional layer

The accuracy improved, but still a lot of space to improve:
accuracy: 0.8656, loss:0.4332

#### Experiment 2: increase the size of the filters
Increase the size of the 2nd convolutional layer from 32 to 64. 

The accuracy imporved, that means increase the size of size of the filters improve the accuracy

accuracy: 0.9136, loss: 0.2901

#### Experiment 3: additional convolutional layer
Add additional Convolutional layer, with increased number of filters.

accuracy: 0.9499, loss: 0.2032

#### Experiment 4: increase pooling size
Increase the pool size to (3, 3), the accuracy dropped.

Conclusion: keep the original (2, 2) pooling size
accuracy: 0.9149, loss: 0.2980


#### Experiment 5: Additional hidden layer with dropout

ADd additional hidden layer in the neural network, with same drop out rate.

Add additional hidden layer, doesn't help on the accuracy

accuracy: 0.8935, loss:0.3593


#### Experiment 6: adding BactchNormalization
Add batch Normalization for each layers

accuracy: 0.9587, loss: 0.1363


#### Experiement 7: remove additional hidden layer

Keep one hidden layer, the accuracy improved

accuracy: 0.9903, loss:0.0313

#### Experiment 8: Inicrease the Epochs:

Increase the epochs to 20 from 10.

The accuracy further imporved, and the loss dropped.

accuraacy: 0.9961, loss:0.0145