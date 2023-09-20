from DeepImageSearch import Load_Data, Search_Setup
import shutil

if __name__ == '__main__':
    shutil.rmtree("/Users/jkalinic-mac/mouseclicker/metadata-files")
    image_list = Load_Data().from_folder(['/Users/jkalinic-mac/mouseclicker/screenshots'])
    st = Search_Setup(image_list=image_list, model_name='vgg19', pretrained=True)
    st.run_index()

    # Get similar images
    images = st.get_similar_images(image_path='/Users/jkalinic-mac/mouseclicker/original/colorTV.png', number_of_images=1)

    for image in images.values():
        most_similar = image


    print(f"Most similar is {most_similar}")