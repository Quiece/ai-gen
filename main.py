from random import choice, randint

# spaghetti code? what spaghetti code?
# python good practices good shmacctices

def prompt_cleanup(LLT_description):
    """ LLT provides a somewhat excesively detailed description. This function will first split it in the relevant
      paragraphs (each is properly titled in LLT) and then in their corresponding sentences. We will keep the first 1 or 2"""
    try:
        llt1 = LLT_description.split("\n")
        keys = []
        for n, i in enumerate(llt1):
            # print(n)
            if len(i) < 15:
                keys.append(n)
                # print(i)
        # make a dict with the extracted keywords as keys
        descrip_dict = {}
        for n, i in enumerate(keys):
            if n < len(keys)-1:
                descrip_dict[llt1[i]] = llt1[i+1:keys[n+1]]
            else:
                descrip_dict[llt1[i]] = llt1[i+1:]
        

        clean_prompt_list = []
        name = None
        parsed_personality = False
        for k, v in descrip_dict.items():
            k = k.replace("\r", "")
            if len(v) > 0:
                v = v[0].replace("\u200b", "")
                if k == "Personality": parsed_personality = True
                if not parsed_personality: 
                    if len(k) > 0: name = k.replace(" ", "")
                    continue #skip all the relationships
                
                if k == "Mouth:":
                    sentences = v.split(".")
                    v = "".join(sentences[0:2])
                elif k == "Tail:":
                    sentences = v.split(".")
                    v = "".join(sentences[0:1])
                elif k == "Ass:":
                    sentences = v.split(".")
                    v = "".join(sentences[0])
                elif k == "Vagina:":
                    # sentences = v.split(".")
                    # v = "".join(sentences[0])
                    v = ""
                    k = ""
                elif k == "Overview:":
                    # print("overview")
                    parag = v.split(" ")
                    if name is None: name = parag[0] if len(parag[0]) > 2 else parag[1]
                    # print("------------------name: " + name)
                clean_prompt_list.append("\n")
                clean_prompt_list.append("\n")
                clean_prompt_list.append(k)
                clean_prompt_list.append("\n")
                # print("\n")
                # print("\n")
                # print(k)
                # print("\n")
                # print("\n")
                clean_prompt_list.append(" ")
                clean_prompt_list.append(v)
                # print(v)
            # print("\n")
        
        clean_prompt = "".join(clean_prompt_list)
        # print(clean_prompt)
    
    except Exception as e:
        if debug: print(e)
        print("There is probably nothing on the clipboard")
        clean_prompt = ""
        name = None

    return (name, clean_prompt)
    
def gen_name_if_necesary(_name, prompt):
    name = _name
    if name is None: 
        name = ""
        name+=str(randint(0, 999999999))
    # if name[0:5] == "Thanks": 
    animals = ["mon", "poke", "pokemon", "eevee", "dog", "cat", "wolf", "fox", "bunny", "rabbit", "horse", "cow", "pig", "sheep", "goat", "deer", "elk", "moose", "bear", "panda", "polar bear", "grizzly", "lion", "tiger", "cheetah", "leopard", "panther", "jaguar", "cougar", "lynx", "bobcat", "ocelot", "serval", "caracal", "leopard", "snow leopard",
                "dragon", "shark", "otter", "bird", "hyena", "spotted hyena"]
    sex = "boy" if "male" in prompt else "girl"
    if name == "Thanks": 
        for animal in animals:
            if animal in prompt.lower():
                name = animal
                break
    for animal in animals:
        if animal in prompt.lower():
            name += "_" + animal
    name += "_" + animal


    
    return name.replace(" ", "_")

def get_description_from_xml(xml_paste):
    pass

if __name__ == "__main__":
    import threading
    import win32clipboard
    import repaint
    
    config = repaint.load_config()
    debug = config["debug"]
    

    # get clipboard data
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    if debug: 
        print(f"Clipboard data: {data}")
    win32clipboard.CloseClipboard()
    prompt = data

    name, prompt = prompt_cleanup(prompt)
    name = gen_name_if_necesary(name, prompt)

    savepath = ""
    clothes = config["CLOTHES"]
    if clothes != "": clothes = "wearing " + clothes
    if debug: 
        print(f"Name: {name}")
        # print(f"Prompt: {prompt}")
    
    extra = "" + clothes
    savepath = None
    High_priority = False
    
    try:
        # threading.Thread(target=repaint.text2image, args=(prompt, "pet", name, savepath, extra, High_priority)).start()
        
        # extra = "(giving oral), (face focus), (fellatio)" + clothes
        # threading.Thread(target=repaint.text2image, args=(prompt, "oral", name+"oral", savepath, extra, High_priority)).start()
        
        # extra = "(ass), (from behind)" + clothes
        # threading.Thread(target=repaint.text2image, args=(prompt, "behind", name+"behind", savepath, extra, High_priority)).start()

        extra = "(sex: 1.3), (ahegao: 1.3), ahegao, blush, rolling eyes, (orgasm: 1.2),  saliva, drooling"
        repaint.text2image(prompt, lorakey="general_furry", optionalExtras=extra,  name=name+"moan", savepath=savepath)
    except Exception as e:
        print(e)
        # Should probably trigger if you don't have enough credits for high priority.
        # Not sure what exception is raised
        if High_priority: repaint.text2image(prompt,lorakey="behind", optionalExtras=extra, high_priority=False, name=name, savepath=savepath)

    
    


    # placeholder


#     prompt = """ Personality
# Serena has a well-rounded personality, with no exceptionally good nor bad traits.​
# Appearance
# Overview:
# Serena is a feminine greater glaceon-girl female.​ Due to her feminine appearance and large breasts, everyone assumes that she's a female.​ Standing at full height, she measures 1.56 metres.​ She appears to be in her early thirties.​
# Face:
# She has a feminine, anthropomorphic, eevee-like face covered in light blue, fluffy fur .​ She is wearing pink blusher.​ She has a head of long, dark blue, eevee-like hair.​, which is unstyled.​ Serena has a pair of eevee-like eyes.​ They have round, dark blue irises, round, dark blue pupils, and light blue sclerae.​ Around her eyes, she's got a layer of black eye liner.​ She's wearing a tasteful amount of pink, matte eye shadow.​ She has a pair, pierced, eevee-like ears and are covered in light blue, fluffy fur .​
# Mouth:
# She has plump, pale lips , which are currently covered in pink, glossy lipstick.​ Her throat is fleshy-pink in colour.​ Her mouth holds a long, fleshy-pink, eevee-like tongue.​ It is both a lot flatter and wider than what would be considered normal.​ Serena has lost her oral virginity.​ It is slightly loose, and can comfortably accommodate objects of up to 5cm in diameter.​ Her throat is of an average depth, allowing her to comfortably accommodate 15cm of a penetrative object, and uncomfortably accommodate 40cm.​ Her mouth and throat are of a typical wetness, and she produces an average amount of saliva.​ Her throat is somewhat resistant to being stretched out, and after being used, it slowly recovers all of its original capacity.​
# Torso:
# Her torso has a girly appearance, and is covered in light blue, fluffy fur .​ She has an average, muscular body, giving her a fit body shape.​
# Chest:
# She has one pair of large mammaries, which fit comfortably into a D-cup bra.​ On each of her perky breasts, she has one large, light blue teat, with large, circular areolae.​
# She is not producing any milk.​
# Arms:
# She has a pair of arms, which are covered in light blue, fluffy fur .​ Her hands are formed into anthropomorphic, eevee-like hands.​ Her fingernails have been painted in blue, smooth nail polish.​ Her arms are muscular, and are feminine in appearance.​
# Legs:
# Her legs are covered in light blue, fluffy fur .​ Her legs and paws are digitigrade, meaning that she naturally walks on her toes.​ Her toenails have been painted in blue, smooth nail polish.​
# Her legs are toned, and have a feminine shape to them.​
# Tail:
# Growing out from just above her ass, she has	a dark blue eevee tail.​ Her tail is of an average thickness and fluffiness in proportion to the rest of her body.​ It measures 78 centimetres in length and, at the base, it measures 12 centimetres in diameter (39 centimetres in circumference).​ It does not taper off from the base, and is a constant diameter all the way to the tip.​ It is not suitable for penetrating orifices.​
# Ass:
# Her womanly hips and small rump are covered in light blue, fluffy fur .​ She has a eevee-like, light blue-rimmed anus, with fleshy-pink internal walls, the rim being slightly darker than the fur around it.​ It is slightly loose, and when lubricated can comfortably accommodate objects of up to 5cm in diameter.​ Her ass is spacious, allowing her to comfortably accommodate 28cm of a penetrative object, and uncomfortably accommodate 56cm.​ Serena has retained her anal virginity.​ It is completely dry, and would need lubricating before sex.​ It reluctantly stretches out when used as a sexual orifice, and after being used, it slowly recovers all of its original capacity.​
# Vagina:
# Between her legs, She has a eevee-pussy, with large, light blue labia and fleshy-pink inner-walls.​ Due to the configuration of her reproductive organs, she gives birth to live young.​
# She has a small clit, which measures less than 1 centimetre in length and less than 1 centimetre in diameter (less than 1 centimetre in circumference).​
# Serena has lost her virginity.​ As is to be expected of someone who is no longer a virgin, her hymen has been torn.​ Her pussy is slightly loose and when lubricated can comfortably accommodate objects of up to 6.5cm in diameter.​ Her pussy is spacious, allowing her to comfortably accommodate 23cm of a penetrative object, and uncomfortably accommodate 51cm.​ It's of an average wetness, and she only needs a small amount of foreplay before she's wet enough for a pleasurable penetration.​ It is somewhat resistant to being stretched out, and after being used, it slowly recovers all of its original capacity.​ Her labia have swollen up into big, extra-puffy pussy lips.​ Her transparent girlcum, much to nobody's surprise, tastes like ordinary girlcum.​ It has a slimy, oily texture.​
# She has a wild, bushy mass of ginger, fluffy fur around her eevee-pussy.​ """
    # name, prompt = prompt_cleanup(prompt)
    # print(name)
    
