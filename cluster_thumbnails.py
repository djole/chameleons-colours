'''
Created on Jun 14, 2013

@author: djordje
'''
import cv2
from codeword_visuals import glue_images
from load_imgs import resize_

input_file = "../chameleons_debugs/2x2_chrom_36_codes/all_chameleons_cluster_dump.txt"
input_imgs_folder = "./Chameleon_segmented/"
img_filename_extension = "jpg"
output_folder = "../chameleons_debugs/2x2_chrom_36_codes/clusters_vis/"
output_text_filename = output_folder + "clusters_text.txt"
num_clusters = 10

with open(input_file, 'r') as fl:
    raw = fl.readlines()
content = []
for st in raw:
    content.append(st.replace('\n', ''))
    
relevant_part = False
relevant_content = []
for line_ in content:
    if not relevant_part:
        if line_.startswith("active nodes:"):
            num_str = line_.replace("active nodes: ","")
            num = int(num_str)
            if num == num_clusters:
                relevant_part = True
    else:
        if line_.startswith("active nodes:"):
            relevant_part = False
            break
        relevant_content.append(line_)

cluster_names = []

ofl = open(output_text_filename, 'w')

for st in relevant_content:
    ofl.write(st+'\n')
    if not st.startswith("Members"):
        names = st.split("', '")
        filenames = []
        for n in names:
            n = n.replace("[","").replace("]","")\
                    .replace("'","").replace('"',"")
            filenames.append(n+"."+img_filename_extension)
        cluster_names.append(filenames)

ofl.flush()
cluster_imgs = []
for cluster_n in cluster_names:
    cluster_container = []
    for img_name in cluster_n:
        im = cv2.imread(input_imgs_folder+img_name)
        im = resize_(500, im)
        if im == None:
            raise IOError("Cannot open image" + im)
        cluster_container.append(im)
    cluster_imgs.append(cluster_container)

for clu, i in zip(cluster_imgs, xrange(len(cluster_imgs))):
    clust_bucket = glue_images(clu)
    clust_bucket = resize_(1500, clust_bucket, inflate=True)
    cv2.imwrite(output_folder+str(i)+".jpg", clust_bucket)
