import discord
from discord.ext import commands
import re

# List of planned features
# Option to split money owed by number of people
# Show the people who haven't payed and have payed


client = commands.Bot(command_prefix=".sharkr ", intents=discord.Intents.all())

@client.event
async def on_ready():
    print("Sharkr is active.")

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

@client.command() #Adds debtor role to those who owe money
async def owesme(ctx, loanName=None, amount_owed=None, *, debtors=None):
    if loanName == None:
         await ctx.send("Error: You must give your loan a name.")
         return
    if amount_owed == None:
         await ctx.send("Error: You must state an amount owed.")
         return
    if loanName == None:
         await ctx.send("Error: You must have atleast one debtor.")
         return
    try:
        guild = ctx.guild
        debtee = guild.get_member_named(ctx.author.name)


        message_text = "This is an automated reminder that you owe " + debtee.name + " " + amount_owed + " for " + loanName + "."
        message = await ctx.send(message_text)
        message_id = message.id
        await ctx.send("Please do not delete the above message, it will be used to manage the loan.")
        message_text += "\nPlease enter '.sharkr payed " + str(message_id) + " " + str(guild.id) + "', without the quotation marks, once you have payed the loan or if you believe you are recieving this message by mistake."


        debtor_role_name = loanName + " Debtor " + str(message_id)
        debtee_role_name = loanName + " Debtee " + str(message_id)
        try:
            await debtee.add_roles(discord.utils.get(guild.roles, name = debtee_role_name))
        except:
            await ctx.send("Error: Could not create role. Is there already a role of the same name?")
        
        try:
            await guild.create_role(name= debtor_role_name)
        except:
             await ctx.send("Error: Could not create role. Is there already a role of the same name?")
             return

        debtorList = debtors.split(" ")
        for debtor in debtorList:
            try:
                member = guild.get_member_named(debtor)
                await member.add_roles(discord.utils.get(guild.roles, name = debtor_role_name))
                await member.send(message_text)
            except:
                ctx.send("Could not find member " + debtor + ". Ensure their name was typed correctly.")
    except:
        await ctx.send("Error: Sorry, something unexpected went wrong.")

@client.command() #Adds debtor role to those who owe money
async def owes(ctx, loanName=None, debtee=None, amount_owed=None, *, debtors=None):
    if loanName == None:
         await ctx.send("Error: You must give your loan a name.")
         return
    if debtee == None:
        await ctx.send("Error: You must state the debtee.")
        return
    if amount_owed == None:
         await ctx.send("Error: You must state an amount owed.")
         return
    if loanName == None:
         await ctx.send("Error: You must have atleast one debtor.")
         return
    try:
        guild = ctx.guild
        try:
            debtee = guild.get_member_named(debtee)
        except:
            await ctx.send("Error: Could not find debtee.")



        message_text = "This is an automated reminder that you owe " + debtee.name + " " + amount_owed + " for " + loanName + "."
        message = await ctx.send(message_text)
        message_id = message.id
        await ctx.send("Please do not delete the above message, it will be used to manage the loan.")
        message_text += "\nPlease enter '.sharkr payed " + str(message_id) + " " + str(guild.id) + "', without the quotation marks, once you have payed the loan or if you believe you are recieving this message by mistake."


        debtor_role_name = loanName + " Debtor " + str(message_id)
        debtee_role_name = loanName + " Debtee " + str(message_id)
        try:
            await debtee.add_roles(discord.utils.get(guild.roles, name = debtee_role_name))
        except:
            await ctx.send("Error: Could not create role. Is there already a role of the same name?")
        
        try:
            await guild.create_role(name= debtor_role_name)
        except:
             await ctx.send("Error: Could not create role. Is there already a role of the same name?")
             return

        debtorList = debtors.split(" ")
        for debtor in debtorList:
            try:
                member = guild.get_member_named(debtor)
                await member.add_roles(discord.utils.get(guild.roles, name = debtor_role_name))
                await member.send(message_text)
            except:
                ctx.send("Could not find member " + debtor + ". Ensure their name was typed correctly.")
    except:
        await ctx.send("Error: Sorry, something unexpected went wrong.")

@client.command() #Removes appropriate debtor role.
async def payed(ctx, message_id=None, guild_id=None):
    #await ctx.send("Error: ")
    if message_id == None or guild_id==None:
        await ctx.send("Error: You are missing arguments. Please ensure your enter the command exactly as it was sent to you.")
        return
    try:
        try:
            guild = client.get_guild(int(guild_id))
        except:
            await ctx.send("Error: Guild could not be found.")
        try:
            member = guild.get_member(ctx.author.id)
            roles = member.roles
        except:
            await ctx.send("Error: Member could not be found.")
        
        role = None
        valid = False
        
        for i in range (len(roles)):
            if message_id in roles[i].name and "debtor" in roles[i].name:
                valid = True
                role = roles[i]
                try:
                    await member.remove_roles(discord.utils.get(guild.roles, name = roles[i].name))
                except:
                    await ctx.send("Error: Could not remove role.")


        if valid:
            await member.send("Thank you, your payment has been noted.")
        else:
            await member.send("There has been an error, please try again.")

        #Logic for when no more debtors remain.
        if role != None:
            debtee = None
            debtor = None
            roles = guild.roles
            if len(role.members)== 0:
                for i in range (len(roles)):
                    if message_id in roles[i].name:
                        try:
                            if 'debtee' in roles[i].name:
                                debtee = await discord.utils.get(guild.roles, name = roles[i].name)
                            else:
                                debtor = await discord.utils.get(guild.roles, name = roles[i].name)
                        except:
                            await ctx.send("Error: Could not find role.")
                
                try:
                    await debtee.members[0].send("All debtors of your loan " + debtee.name + " have payed.")
                except:
                    await ctx.send("Error: Could not find role.")
                
                
                try:
                    await debtee.delete()
                    await debtor.delete()
                except:
                    await ctx.send("Error: Could not delete role.")
    
    except:
        await ctx.send("Error: Sorry, something unexpected went wrong.")
  
@client.command() 
async def remind(ctx, loan_name=None): # Remind outstanding debtors of their loan
    if loan_name == None:
        await ctx.send("Error: You must provide a loan name.")
        return
    try:
        guild = ctx.guild
        try:
            role_id = re.sub("\D", "", loan_name)
            role = guild.get_role(int(role_id))
        except:
            await ctx.send("Error: Could not find role.")

        bot_message = ""


        if "debtor" in role.name:
            try:
                message_id = int((role.name.split(" "))[2])
                valid = False

                for i in guild.get_member_named(ctx.author).roles:
                    if message_id in i.name and 'debtee' in i.name:
                        valid = True
                
                if valid == False:
                    await ctx.send("Error: You are not the debtee of this loan, so you cannot send a reminder for it.")
                    return



                for channel in guild.text_channels:
                    if channel.fetch_message(message_id) != None:
                        bot_message = await channel.fetch_message(message_id)
            except:
                await ctx.send("Error: Could not find loan message. It may have been deleted.")
        else:
            await ctx.send("Error: You did not input a recognized sharkr debtor loan.")
            return


        
        for member in role.members:
            try:
                await member.send(bot_message.content)
                await member.send("Please enter '.sharkr payed " + str(message_id) + " " + str(guild.id) + "', without the quotation marks, once you have payed the loan or if you believe you are recieving this message by mistake.")
            except:
                await ctx.send("Error: Could not find member.")
    except:
        await ctx.send("Error: Sorry, something unexpected went wrong.")

@client.command() 
async def clear(ctx, loan_name=None): # Delete a loan
    if loan_name == None:
        await ctx.send("Error: You must provide a loan name.")
        return
    try:
        guild = ctx.guild
        try:
            role_id = re.sub("\D", "", loan_name)
            role = guild.get_role(int(role_id))
        except:
            await ctx.send("Error: Could not find role.")

        if "debtor" in role.name:
            try:
                message_id = int((role.name.split(" "))[2])
                valid = False

                for i in guild.get_member_named(ctx.author).roles:
                    if message_id in i.name and 'debtee' in i.name:
                        valid = True
                
                if valid == False:
                    await ctx.send("Error: You are not the debtee of this loan, so you cannot send a reminder for it.")
                    return
                else:
                    roles = guild.roles
                    debtee=None
                    debtor=None
                    if len(role.members)== 0:
                        for i in range (len(roles)):
                            if message_id in roles[i].name:
                                try:
                                    if 'debtee' in roles[i].name:
                                        debtee = await discord.utils.get(guild.roles, name = roles[i].name)
                                    else:
                                        debtor = await discord.utils.get(guild.roles, name = roles[i].name)
                                except:
                                    await ctx.send("Error: Could not find role.")
                        
                        try:
                            await debtee.delete()
                            await debtor.delete()
                            await ctx.send("Loan has been cleared")
                        except:
                            await ctx.send("Error: Could not delete role.")

            except:
                await ctx.send("Error: Could not find loan message. It may have been deleted.")
        else:
            await ctx.send("Error: You did not input a recognized sharkr debtor loan.")
            return
    except:
        await ctx.send("Error: Sorry, something unexpected went wrong.")

client.run("") 