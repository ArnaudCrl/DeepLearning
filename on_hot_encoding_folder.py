def on_hot_encoding_folder(dir):
    classes = os.listdir(dir) #gres, granite, basalt, gneiss ...
    class_to_int = dict((c, i) for i, c in enumerate(classes))
    
    integer_encoded = []
    for c in classes: 
        files = os.listdir(dir + c + '/') #image list
        integer_encoded += (class_to_int[c] for f in files)
        
    onehot_encoded = []
    for value in integer_encoded:
        c = [0 for _ in range(len(classes))]
        c[value] = 1
        onehot_encoded.append(c)
    
    return onehot_encoded
