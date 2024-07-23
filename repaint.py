#!/usr/bin/python
# originally based on https://github.com/shidktbw/pixaiAPI
from pixai import PixaiAPI
import io
import os
import sys
import time
from PIL import Image
import xml.etree.ElementTree as ET


# this is an old token
# replace this with your own token. You'll likely have to do this again from time to time
# There should be an image on the Zip of where to get one.
# token = "eyJhbGciOiJFUzUxMiIsInR5cCI6IkpXVCJ9.eyJsZ2EiOjE3MTIyMTEyMzIsImlhdCI6MTcxMjIxMTI1MCwiZXhwIjoxNzEyODE2MDUwLCJpc3MiOiJwaXhhaSIsInN1YiI6IjE3MzI1MDY4MjQyNjUxMTc3MjIiLCJqdGkiOiIxNzMyNTA2ODI0NzI2NDkxMTY3In0.AK2kUNXq3OFrRbrewThx5a80O2LUgx223hmG3wy_Yg7bFl9YJxZ2kTJFSG0ilXSwPbDgrZV4lsjuVvpG3odiEaD6AdsZGm2dLXIjxYc_NNbJ4sCRB6l_dVFCm4D9ja1ppMi4Z5ZW0Qze66Byf8MqyoC_ykfIATUNfUfdvJicL71CoRB5"
token = "eyJhbGciOiJFUzUxMiIsInR5cCI6IkpXVCJ9.eyJsZ2EiOjE3MjE3MDA1NDcsImlhdCI6MTcyMTcwMDU0OSwiZXhwIjoxNzIyMzA1MzQ5LCJpc3MiOiJwaXhhaSIsInN1YiI6IjE3NzIzMDc4OTYyNDQ2NzYzODAiLCJqdGkiOiIxNzcyMzA3ODk2MzcwNTA1NTAyIn0.AFBp_BqCvyQ0L3OQnuC-zj2dcaongh39854MyKOulU0J0G-Llfbq-VXdKLi8eA-yzXDhF5074dIYJ5LYuK53jL4CAXF2foo4IU4kMm1aQEKJdBpuBheN8eJjqMuMksN8ZHiBb_A-PcbTPKzXuvkMpc213o33q2zH5iG93_4lUnniK9B_"

# model url looks like pixai.art/model/12345/67890
# use the second number which refers to the specific version of a model
# model = 1632080534138643945 # epic realism

# model = 1693971202393705839 # western toon style
# model = "1616755841135117178" # Kuroneko model https://pixai.art/model/1616755838777918291
model = "1648918127446573124" # moonbeam model 1648918125777240131
# another model https://pixai.art/model/1641361992274327507
# https://pixai.art/model/1629975574420526965 used with https://pixai.art/model/1632808149867611809?utm_source=copy_web

# lora = {
#     '1742814265811967135': 0.7, # western illustration vector
#     '1638766839267720162': 0.5, # niji-flat
# }
# lora_fur = {
#     '1742814265811967135': 1, 
# }                             
    # furry Anime https://pixai.art/model/1742814265811967135/1742818372916214532
    # shiitakemeshi's furry art style https://pixai.art/model/1701023293348972875/1701023293369944396
    # Bonifasko Style Furry  https://pixai.art/model/1627915094736192892/1627915097135334834
lora_fur = {
    # '1657138408935748616': 0.7, # https://pixai.art/model/1657132792892036111/1657138408935748616
    '1627915097135334834': 0.7, # Bonifasko Style Furry  https://pixai.art/model/1627915094736192892/1627915097135334834
    '1682753525242443076': 0.7, # shiitakemeshi's furry art style https://pixai.art/model/1701023293348972875/1701023293369944396
    # '1701023293369944396': 0.7, # 
    '1610907692942825388': 0.7, # 
# ahegao https://pixai.art/model/1610907690191361905/1610907692942825388
}
lora_fur_back = {
     # https://pixai.art/model/1657132792892036111/1657138408935748616
    '1627915097135334834': 0.7, # Bonifasko Style Furry  https://pixai.art/model/1627915094736192892/1627915097135334834
    '1682753525242443076': 0.7, # shiitakemeshi's furry art style https://pixai.art/model/1701023293348972875/1701023293369944396
    '1647902088062905038': 0.6, #  Pose loooking back https://pixai.art/model/1647902085391133374/1647902088062905038
    # looking_through_legs, looking back, from behind
}
lora_fur_pet = {
     # https://pixai.art/model/1657132792892036111/1657138408935748616
    '1627915097135334834': 0.7, # Bonifasko Style Furry  https://pixai.art/model/1627915094736192892/1627915097135334834
    '1682753525242443076': 0.7, # shiitakemeshi's furry art style https://pixai.art/model/1701023293348972875/1701023293369944396
    # '1642778233577693167': 0.6, #  Pose loooking back https://pixai.art/model/1647902085391133374/1647902088062905038
    "1624371550155784504": 0.7 # "pet" https://pixai.art/model/1624371546670317846/1624371550155784504
    # looking_through_legs, looking back, from behind
}
lora_fur_cowgirl = {
     # https://pixai.art/model/1657132792892036111/1657138408935748616
    '1627915097135334834': 0.7, # Bonifasko Style Furry  https://pixai.art/model/1627915094736192892/1627915097135334834
    '1682753525242443076': 0.7, # shiitakemeshi's furry art style https://pixai.art/model/1701023293348972875/1701023293369944396
    "1635121375775304614": 0.7 # pose 3 https://pixai.art/model/1635121373225167749/1635121375775304614
    
}
lora_fur_oral = {
     # https://pixai.art/model/1657132792892036111/1657138408935748616
    '1627915097135334834': 0.7, # Bonifasko Style Furry  https://pixai.art/model/1627915094736192892/1627915097135334834
    '1682753525242443076': 0.7, # shiitakemeshi's furry art style https://pixai.art/model/1701023293348972875/1701023293369944396
    '1637587748197171654': 0.5, # face https://pixai.art/model/1637587745340850594/1637587748197171654
    # fellatio https://pixai.art/model/1598727108966253229/1598727108978836143
    # "1635121375775304614": 0.7 # pose 3 https://pixai.art/model/1635121373225167749/1635121375775304614
}
# 1642778233577693167 # Pose cowgirl https://pixai.art/model/1642778231090470863/1642778233577693167
# 1701829738810984986 # other pose https://pixai.art/model/1701829738739681816/1701829738810984986
# 1635121375775304614 # pose 3 https://pixai.art/model/1635121373225167749/1635121375775304614
# 1637587748197171654 # face https://pixai.art/model/1637587745340850594/1637587748197171654
# 1624371550155784504 # "pet" https://pixai.art/model/1624371546670317846/1624371550155784504
#Bondage  https://pixai.art/model/1649856588483523361/1649856591348233012
lora_zoro = {
    '1649856591348233012': 0.5, 
    '1668578176082755232': 0.8,  # zoroark
    '1721188615832873078': 0.7,  # muzzle
}
lora_eevo = { #https://pixai.art/model/1755099251992441986?utm_source=copy_web
    '1755099251992441986': 0.8
}

loras_dict = {
    'zoroark': lora_zoro,
    'eevee': lora_eevo,
    'general_furry': lora_fur,
    'behind': lora_fur_back,
    'cowgirl': lora_fur_cowgirl,
    'pet': lora_fur_pet,
    'oral': lora_fur_oral
}




# whether to use high priority tasks, which cost more credits
high_priority = True

def remove_background(image):
    img = image.convert("RGBA")
    datas = img.getdata()
    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    img.putdata(newData)
    return img

def split_image(image):
    width, height = image.size
    half_width = width // 2
    half_height = height // 2
    return (image.crop((0, 0, half_width, half_height)),
            image.crop((half_width, 0, width, half_height)),
            image.crop((0, half_height, half_width, height)),
            image.crop((half_width, half_height, width, height)))

def batch_save(images, filenameRef, folder="./generated", test=False, savepath=None):

    if savepath is not None:
        folder = os.path.join(savepath, "generated")
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

    if test:
        # create blank test image
        Image.new("RGBA", (512, 768), (255, 255, 255, 255)).save(f"{folder}/{filenameRef}.png")

    for i, image in enumerate(images):
        image.save(f"{folder}/{filenameRef[0:-4]}.tmp.png")
        # image.save(f"{folder}/{filenameRef[0:-4]}_{i}.png")
        os.replace(f"{folder}/{filenameRef[0:-4]}.tmp.png", f"{folder}/{filenameRef[0:-4]}_{i}.png") # save then rename to avoid partially-written files
        # image.save(filenameRef + f"temp_{i}.png")
    # images[0].save(filenameRef+".tmp.png")
    # os.replace(filenameRef+".tmp.png", filenameRef) # save then rename to avoid partially-written files



def text2image(text, lorakey = "general_furry", name="noname", savepath=None, optionalExtras = None, high_priority=True):
    """ Lorakey options:
        general_furry
        behind
        cowgirl
        pet
        oral
        squat
        
        """
    prompt = "1girl, fluffy fur, anthro, YIFF, (detailed Fur: 1.3), (furred body:1.5), toned, (NSFW:1.2), adult, chest tuff"
    # base1 = "Furry, posing sexy, animal, anthro, toned, breasts, cleavage, YIFF, "
    # base1 += ", (realistic ultra details), (furred body:1.3)"
    # base1 += choice([", (teasing: 1.3)", ", (sexy: 1.3)", ", (provocative: 1.3)", ", cute, kawaii"])
    # base1 += ", (erotic: 1.3)"
    
    if "pet" in lorakey: 
        prompt += "(Eager_pet_pose:1.6), (all fours)"
        lorakey = "pet"
    if "behind" in lorakey:
        prompt += "pussy, panty pull, uncensored, tail, solo focus, ass, pussy juice, blush, looking back, imminent penetration, from behind, smile"
        lorakey = "behind"
        # lorakey = "pet"
    if "cowgirl" in lorakey: 
        prompt += "(cowgirl position:1.2), (girl on top:1.2), <lora:pose cowgirl:1>, "
        lorakey = "cowgirl"
    if "face" in lorakey: 
        prompt += "Orgasm_Faces, face closeup, ahegao, "
        lorakey = "cowgirl"
    if "squat" in lorakey: prompt += "<lora:pose squating-000006:1>, "
    if "oral" in lorakey: 
        prompt += "(Eager_pet_pose:1.5), 1girl, furry, breasts, furry female, oral, fellatio, nude, solo focus, Orgasm_Faces, "
        lorakey = "oral"
    
    

    prompt = optionalExtras + prompt
    prompt += text

    if len(text) > 4096: 
        print("shortened")
        text = text[0:4095]
    
    client = PixaiAPI(token)
    
    task = client.txt2img( prompts=prompt,
                            size=(512, 768),
                            priority=1000 if high_priority else 0,
                            modelId=model,
                            lora=loras_dict[lorakey],
                            
                            steps=32, # 23
                            batchSize=4,
                            samplingMethod = "Euler a"
                            )
    while True:
            if task.get_data():
                image_full = Image.open(io.BytesIO(task.data))
                image_full = remove_background(image_full)
                images = split_image(image_full)
                batch_save(images, f"{name}.png", savepath=savepath)
                break
            else:
                time.sleep(1)
        
                           

def main():
    # the following will be added to all prompts
    preamble = "1girl, Furry, animal, anthro, chest tuft, toned, breasts, cleavage, YIFF, NSFW, adult"
    client = PixaiAPI(token)
    argv = sys.argv
    if len(argv) == 3:
        filename = argv[1]
        task = client.img2img(filename, preamble + argv[2],
                              size=(512, 768),
                              priority=1000 if high_priority else 0,
                              modelId=model,
                              lora=loras_dict["general_furry"],
                              strength=0.7,
                              steps=23,
                              batchSize=4,
                              samplingMethod = "Euler a"
                              )
        while True:
            if task.get_data():
                image_full = Image.open(io.BytesIO(task.data))
                image_full = remove_background(image_full)
                images = split_image(image_full)
                batch_save(images, filename)
                break
            else:
                time.sleep(1)

if __name__ == "__main__":
    main()
    # print("10091142_479565.png"[0:-4])
    # print(a)
    


