from sentence_transformers import SentenceTransformer, util
from PIL import Image
import glob
import os

if __name__ == '__main__':
    threshold = 0.9
    model = SentenceTransformer('clip-ViT-B-32')
    image_names = ['C:/sftool/images/original/colorTV.png',
                   'C:/sftool/images/screenshots/1.png',]

    encoded_image = model.encode([Image.open(filepath) for filepath in image_names], batch_size=128, convert_to_tensor=True, show_progress_bar=True)
    score, id_1, id2 = util.paraphrase_mining_embeddings(encoded_image)[0]
    near_duplicates = score > threshold
    print(f"{image_names[id_1]} and {image_names[id2]}  ==== Score: {score * 100}, it did pass {near_duplicates}")
