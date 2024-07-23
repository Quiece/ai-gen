If you have any questions, begin your message with something that rhymes with "Merry", just so I know you actually read the README.
# How to:

## Set-up

+ gonna need python, pillow and threading. May be forgetting something.
+ extract wherever you want the images to generate (you can also set an absolute path changing the savepath variable in main.py).
+ Peruse the code a bit, as well as pixai.art. You might want to change the models, loras, and base prompts.

## Use

+ once you have python, double click setup.bat; should install all dependencies. 
+ In-game; copy the npc's description. Preferably from the top, but as long as you catch what you consider relevant it shooould be fine.
+ Double click run.bat when you wanna generate something (it will use whatever is on your clipboard i.e. ctrl+c) 
  + if that doesn't work for some reason,  try replacing line 112 `data = win32clipboard.GetClipboardData()` with `data=your stuff`
+ images will be generated on the savepath/generated with a semi-descriptive name. Add them to the character as you would any other image.

## Modify
On the config file you can:
+ Change the model, loras and weights. What's in "general_furry" is always included so keep that in mind. Also mind that only 3 loras may be use at a time with the free plan.
+ Set the api key.
+ Set the save path. By default, it saves wherever the script is, in /generated
+ Change the base prompt. This is added to the begining of all prompts.
+ Set worn clothes, if any.

Anything else, such as changing how many images are generated (by default 2 sets of 4), what they are about etc you'll need to go into the code. It shouldn't be too hard unless you want soomething complex.

