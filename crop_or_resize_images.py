# Cropping and/or resizing all images recursively in inputpath and placing the cropped images in outputpath      
dirs = os.listdir(inputpath) #train, validation, display
for d in dirs:
    classes = os.listdir(inputpath + d) #gres, granite, basalt, gneiss ...
    for c in classes:
        print(d + c)
        files = os.listdir(inputpath + d + '/' + c + '/') #image list
        for f in files:
            fullpath = inputpath + d + '/' + c + '/' + f
#             print(fullpath)
            if os.path.isfile(fullpath):
                im = Image.open(fullpath)

                
#                #CROP
#                width, height = im.size 
#                wanted_size = 500
#                left = (width - wanted_size)/2
#                top = (height - wanted_size)/2
#                right = (width + wanted_size)/2
#                bottom = (height + wanted_size)/2

#                imCrop = im.crop((left, top, right, bottom))
                
                #RESIZE
                new_img = im.resize((224,224))

                new_img.save(outputpath + '/' + d + '/' + c + '/' + f, "JPEG", quality=100)
