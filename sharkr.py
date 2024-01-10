import discord
from discord.ext import commands
import re

# List of planned features
# Group payment reminder


client = commands.Bot(command_prefix=".sharkr ", intents=discord.Intents.all())

@client.event
async def on_ready():
    print("Bot is running.")

@client.event # When someone becomes interested in an event, they are given that events role.
async def on_scheduled_event_user_add(event,user):
    try:
        member = event.guild.get_member(user.id)
        await member.add_roles(discord.utils.get(event.guild.roles, name = event.name))
    except:
        print("error")


@client.event # When someone loses intrest in an event, they lose that events role.
async def on_scheduled_event_user_remove(event,user):
    member = event.guild.get_member(user.id)
    await member.remove_roles(discord.utils.get(event.guild.roles, name = event.name))
    print("uninterested")

@client.event # When an event is created, so too is a role for that event. The creator is given the role too.
async def on_scheduled_event_create(event):
    guild = event.guild
    member = event.guild.get_member(event.creator.id)
    await guild.create_role(name=event.name)
    await member.add_roles(discord.utils.get(event.guild.roles, name = event.name))
    print("created")


@client.event # When an event is deleted, the associated role is also deleted.
async def on_scheduled_event_delete(event):
    guild = event.guild
    role = discord.utils.get(guild.roles,name=event.name)
    await role.delete()
    print("deleted")

@client.command() # Basic hello world.
async def hello(ctx):
    await ctx.send("Hello, I am Sharkr")

@client.command() # Sends a custom dm to the sepcified user. Can use this for payment reminders.
async def message(ctx, user:discord.Member, *, message=None):
    await user.send(message)

@client.command() #Adds debtor role to those who owe money and debtee to the one who is owed.
async def owesme(ctx, loanName=None, amount_owed=None, *, debtors):
    try:
        guild = ctx.guild
        debtee = ctx.author


        message_text = "This is an automated reminder that you owe " + debtee.name + " " + amount_owed + " for " + loanName + "."
        message = await ctx.send(message_text)
        message_id = message.id
        await ctx.send("Please do not delete the above message, it will be used to manage the loan.")
        message_text += "\nPlease enter '.sharkr payed " + str(message_id) + " " + str(guild.id) + "', without the quotation marks, once you have payed the loan or if you believe you are recieving this message by mistake."


        debtor_role_name = loanName + " Debtor " + str(message_id)
        debtee_role_name = loanName + " Debtee " + str(message_id)
        

        await guild.create_role(name= debtor_role_name)
        await guild.create_role(name= debtee_role_name)
        await debtee.add_roles(discord.utils.get(guild.roles, name = debtee_role_name))


        debtorList = debtors.split(" ")
        for debtor in debtorList:
            try:
                member = guild.get_member_named(debtor)
                await member.add_roles(discord.utils.get(guild.roles, name = debtor_role_name))
                await member.send(message_text)
            except:
                print("Could not find member " + debtor + ". Ensure their name was typed correctly.")
    except Exception as error:
        print(error)

@client.command() #Adds debtor role to those who owe money and debtee to the one who is owed.
async def owes(ctx, loanName=None, debtee=None, amount_owed=None, *, debtors):
    try:
        guild = ctx.guild
        debtee = guild.get_member_named(debtee)


        message_text = "This is an automated reminder that you owe " + debtee.name + " " + amount_owed + " for " + loanName + "."
        message = await ctx.send(message_text)
        message_id = message.id
        await ctx.send("Please do not delete the above message, it will be used to manage the loan.")



        debtor_role_name = loanName + " Debtor " + str(message_id) + " .sharkr"
        debtee_role_name = loanName + " Debtee " + str(message_id) + " .sharkr"
        

        await guild.create_role(name= debtor_role_name)
        await guild.create_role(name= debtee_role_name)
        await debtee.add_roles(discord.utils.get(guild.roles, name = debtee_role_name))


        debtorList = debtors.split(" ")
        for debtor in debtorList:
            try:
                member = guild.get_member_named(debtor)
                await member.add_roles(discord.utils.get(guild.roles, name = debtor_role_name))
                await member.send(message_text)
                await member.send("Please enter '.sharkr payed " + str(message_id) + " " + str(guild.id) + "', without the quotation marks, once you have payed the loan or if you believe you are recieving this message by mistake.")
            except:
                print("Could not find member " + debtor + ". Ensure their name was typed correctly.")
    except Exception as error:
        print(error)

@client.command() #Removes appropriate debtor role.
async def payed(ctx, message_id, guild_id):
    guild = client.get_guild(int(guild_id))
    member = guild.get_member(ctx.author.id)
    roles = member.roles
    valid = False
    
    for i in range (len(roles)):
        if message_id in roles[i].name:
            valid = True
            await member.remove_roles(discord.utils.get(guild.roles, name = roles[i].name))


    if valid:
        await member.send("Thank you, your payment has been noted.")
    else:
        await member.send("There has been an error, please try again.")

    #Add logic for when no more debtors remain.
  
@client.command() 
async def remind(ctx, role_name):
    guild = ctx.guild
    role_id = re.sub("\D", "", role_name)
    role = guild.get_role(int(role_id))

    message_id = int((role.name.split(" "))[2])
    bot_message = ""
    for channel in guild.text_channels:
        if channel.fetch_message(message_id) != None:
            bot_message = await channel.fetch_message(message_id)


    
    for member in role.members:
        await member.send(bot_message.content)
        await member.send("Please enter '.sharkr payed " + str(message_id) + " " + str(guild.id) + "', without the quotation marks, once you have payed the loan or if you believe you are recieving this message by mistake.")

client.run("") 