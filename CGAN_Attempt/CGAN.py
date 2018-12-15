'''
This is the beginning of an  attempt to use CGAN's for realistic password generation.

'''


#I'm going to start this next time I come into lab
'''
Use : https://github.com/eriklindernoren/Keras-GAN/blob/master/wgan_gp/wgan_gp.py as the base
And make it a cgan by adding bits from: https://github.com/eriklindernoren/Keras-GAN/blob/master/cgan/cgan.py

Some things that'l have to be cahnges:
row/cols
The generator takes slightly different inputs in the two. work that out


There is some code towards the end it looks like:
      noise = Input(shape=(self.latent_dim,))
        label = Input(shape=(1,), dtype='int32')
        label_embedding = Flatten()(Embedding(self.num_classes, self.latent_dim)(label))

        model_input = multiply([noise, label_embedding])
        img = model(model_input)

return Model([noise, label], img)

See the multipy, and that stuff about the label embedding. 
That is going to multiply the noise by the input. Which allows the input to be taken into account be the generator

'''