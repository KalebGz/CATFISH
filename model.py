import os
import openai
import json
import inquirer
from PIL import Image
# import urllib.request
import requests
from io import BytesIO

openai.api_key = "PLACE_OPEN_AI_KEY_HERE"

        # Custom f(n)s

def ConvertImage(imageName, img):
    ''' resizes + formats images as png for submission '''
    image = img
    image = image.resize((1024, 1024),Image.ANTIALIAS) 
    image = image.convert('RGBA')
    image.save(imageName + ".png")
    return image


def option_selector(opt):
  ''' selects option from terminal and generates api call '''
  api_res = ""
  if(opt == 'simmilar image'):
    input_file = input("Insert file name:")
    img_name = input_file.split('.')[0]
    print(input_file + "****" + img_name)
    img = Image.open(input_file)
    ConvertImage(img_name, img)
    api_res = openai.Image.create_variation(
      # image= open("white-min.jpg", "rb"),
      image= open(img_name + ".png",'rb'),
      n=2,
      size="1024x1024"
    )

  elif(opt == 'Facebook post'):
    name = input("Insert your catfish name:")
    occasion = input("What occasion do you want the facebook post to be about:")
    api_res = openai.Completion.create(
      model="text-davinci-003",
      prompt=("Make me a facebook post if my name was " + name + " and i'm positng about " + occasion),
      max_tokens=100,
      temperature=0
    )
  elif(opt == 'random bio'):
    name = input("Insert your catfish name:")
    api_res = openai.Completion.create(
      model="text-davinci-003",
      prompt="Make me a random biography with the name " + name,
      max_tokens=100,
      temperature=0
    )
  elif(opt == 'custom prompt'):
    req = input("Insert request: ")
    api_res = openai.Completion.create(
      model="text-davinci-003",
      prompt=req,
      max_tokens=100,
      temperature=0
    )
  else:
    print("ERROR")
    return 0

  return api_res


          # main prog
print(" ")
print(" ")
print("*************WELCOME TO CATFISH!*************")
print(" ")
print("---HERE IN FRONT OF YOU LIES SIMPLE AND INTUITEVE ACCESS TO OPENAI'S LANGUAGE AND IMAGE MODELS FOR CATFISHING ANYONE ON THE INTERNET")
print("-Select from the options below to generate fake content")

questions = {
  inquirer.List('type',
                message="What kind of information do you want to genreate?",
                choices=['Facebook post', 'simmilar image', 'random bio', 'custom prompt'],
            ),
}
answers = inquirer.prompt(questions)
# print(answers["type"])

api_res = option_selector(answers["type"])

# print("***API RES")
# print(api_res)
 
if(answers["type"] == 'simmilar image'):  
  # print(api_res)
  
  res_url = api_res["data"][0]["url"]
  print("*URL: " + res_url)
  img_data = requests.get(res_url).content
  with open('generated_img.jpg', 'wb') as handler:
    handler.write(img_data)
  dw_img = Image.open("generated_img.jpg")
  dw_img.show()
  response = requests.get(res_url)
  img = Image.open(BytesIO(response.content))

else:
  res = api_res["choices"][0]["text"]
  print(res)