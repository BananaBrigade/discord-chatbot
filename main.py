from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
import discord

mname = "facebook/blenderbot-400M-distill"
model = BlenderbotForConditionalGeneration.from_pretrained(mname, use_cache=True)
tokenizer = BlenderbotTokenizer.from_pretrained(mname)

# i hope this loads the rest of the model into ram so it doesnt take an eternity
inputs = tokenizer(["test"], return_tensors="pt", max_length=2048)
reply_ids = model.generate(**inputs, do_sample=True, temperature=2.0, max_length=512)
bong = str(tokenizer.batch_decode(reply_ids)).replace("[\'","").replace("[\"","").replace("</s>\']","").replace("<s>","")

# i want to free up what little ram i can
inputs = None
reply_ids = None
bong = None


#DISCORD

with open("very-secret-token","r") as p:
    token = p.readline()


intents = discord.Intents.default()
intents.message_content = True #Need to READ

client = discord.Client(intents=intents) # CLIENENT 

@client.event
async def on_ready():
    print(f'We have {client.user}') # I NEED TO KNOW

@client.event
async def on_message(message):
    if message.content:
        print(f"{message.channel}: {message.author} - {message.content}")


    if message.author == client.user: # WE DO NOT WANT TO MAKE THE ROBOT GO INSANE
        return


    #if client.user.mention in message.content:
    if message.content:
        async with message.channel.typing():
            inputs = tokenizer([message.content.replace(client.user.mention,"")], return_tensors="pt", max_length=2048)
            reply_ids = model.generate(**inputs, do_sample=True, temperature=2.0, max_length=512)
            await message.channel.send(str(tokenizer.batch_decode(reply_ids)).replace("[\'","").replace("[\"","").replace("</s>\']","").replace("<s>",""), reference=message)

client.run(token)