# Life but Make it Art

This is a prototype of an app that will take a user uploaded image and find an artwork that "looks like" it in some, hopefully amusing way. Inspired by the Twitter account [ArtButMakeItSports](https://twitter.com/ArtButSports)

The hashing idea looks like a dead end. It's really not what hashing is for, which is to detect identical images. Images which are merely close to the hash value or even closest among the available artworks (while not really that close). Don't end up being very close at all.

A better idea is probably to use something like [Image2Vec](https://github.com/christiansafka/img2vec) to create feature vectors for each artwork image and then get a vector for the uploaded image and find the closest one via cosine similarity. Start with a pretrained model like Resnet.

[Extract a feature vector for any image with pytorch](https://becominghuman.ai/extract-a-feature-vector-for-any-image-with-pytorch-9717561d1d4c)

More recent method maybe? [Generating image embeddings on a GPU with LLaVA and llama-cpp-python](https://mildbyte.xyz/blog/llama-cpp-python-llava-gpu-embeddings/)

Next steps:
1. Install and configure (pg_vector)[https://github.com/pgvector/pgvector] and add a vector column for ArtworkImage and UserImage.
2. Extract feature vectors for all artwork images
3. modify UserImage upload to extract a feature vector when saving.
   1. Does this take a long time? Should it be done async with celery? (probably)
4. On the UserImage detail page, show the most similar artworks.