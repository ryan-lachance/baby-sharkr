import discord
from discord.ext import commands
import re
import traceback



# List of planned features
# Option to split money owed by number of people
# Command to show details of all other commands


client = commands.Bot(command_prefix=".sharkr ", intents=discord.Intents.all())

@client.event
async def on_ready():
    print("Sharkr is active.")

@client.event # When someone becomes interested in an event, they are given that events role.
async def on_scheduled_event_user_add(event,user):
    try:
        member = event.guild.get_member(user.id)
        await member.add_roles(discord.utils.get(event.guild.roles, name = event.name))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)


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
        try:
            debtee = guild.get_member(ctx.author.id)
        except Exception as e:
            await ctx.send("Error: Could not find debtee.")
            traceback.print_exception(type(e), e, e.__traceback__)
            return



        message_text = "This is an automated reminder that you owe " + debtee.name + " " + amount_owed + " for " + loanName + "."
        message = await ctx.send(message_text)
        message_id = message.id
        await ctx.send("Please do not delete the above message, it will be used to manage the loan.")
        message_text += "\nPlease enter '.sharkr payed " + str(message_id) + " " + str(guild.id) + "', without the quotation marks, once you have payed the loan or if you believe you are recieving this message by mistake."


        debtor_role_name = loanName + " Debtor " + str(message_id)
        debtee_role_name = loanName + " Debtee " + str(message_id)
        try:
            await guild.create_role(name= debtee_role_name)
            await debtee.add_roles(discord.utils.get(guild.roles, name = debtee_role_name))
        except Exception as e:
            await ctx.send("Error: Could not create role. Is there already a role of the same name?")
            traceback.print_exception(type(e), e, e.__traceback__)
        
        try:
            await guild.create_role(name= debtor_role_name)
        except Exception as e:
             await ctx.send("Error: Could not create role. Is there already a role of the same name?")
             traceback.print_exception(type(e), e, e.__traceback__)
             return

        debtorList = debtors.split(" ")
        for debtor in debtorList:
            try:
                if guild.get_role(processUserId(debtor)) != None:
                   for member in guild.get_role(processUserId(debtor)).members:
                    await member.add_roles(discord.utils.get(guild.roles, name = debtor_role_name))
                    await member.send(message_text)      
                else:
                    member = guild.get_member(processUserId(debtor))
                    await member.add_roles(discord.utils.get(guild.roles, name = debtor_role_name))
                    await member.send(message_text)
            except Exception as e:
                ctx.send("Could not find member " + debtor + ". Ensure their name was typed correctly.")
                traceback.print_exception(type(e), e, e.__traceback__)
    except Exception as e:
        await ctx.send("Error: Sorry, something unexpected went wrong.")
        traceback.print_exception(type(e), e, e.__traceback__)

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
            debtee = guild.get_member(processUserId(debtee))
        except Exception as e:
            await ctx.send("Error: Could not find debtee.")
            traceback.print_exception(type(e), e, e.__traceback__)
            return



        message_text = "This is an automated reminder that you owe " + debtee.name + " " + amount_owed + " for " + loanName + "."
        message = await ctx.send(message_text)
        message_id = message.id
        await ctx.send("Please do not delete the above message, it will be used to manage the loan.")
        message_text += "\nPlease enter '.sharkr payed " + str(message_id) + " " + str(guild.id) + "', without the quotation marks, once you have payed the loan or if you believe you are recieving this message by mistake."


        debtor_role_name = loanName + " Debtor " + str(message_id)
        debtee_role_name = loanName + " Debtee " + str(message_id)
        try:
            await guild.create_role(name= debtee_role_name)
            await debtee.add_roles(discord.utils.get(guild.roles, name = debtee_role_name))
        except Exception as e:
            await ctx.send("Error: Could not create role. Is there already a role of the same name?")
            traceback.print_exception(type(e), e, e.__traceback__)
        
        try:
            await guild.create_role(name= debtor_role_name)
        except Exception as e:
             await ctx.send("Error: Could not create role. Is there already a role of the same name?")
             traceback.print_exception(type(e), e, e.__traceback__)
             return

        debtorList = debtors.split(" ")
        for debtor in debtorList:
            try:
                if guild.get_role(processUserId(debtor)) != None:
                   for member in guild.get_role(processUserId(debtor)).members:
                    await member.add_roles(discord.utils.get(guild.roles, name = debtor_role_name))
                    await member.send(message_text)      
                else:
                    member = guild.get_member(processUserId(debtor))
                    await member.add_roles(discord.utils.get(guild.roles, name = debtor_role_name))
                    await member.send(message_text)
            except Exception as e:
                ctx.send("Could not find member " + debtor + ". Ensure their name was typed correctly.")
                traceback.print_exception(type(e), e, e.__traceback__)
    except Exception as e:
        await ctx.send("Error: Sorry, something unexpected went wrong.")
        traceback.print_exception(type(e), e, e.__traceback__)

@client.command() #Removes appropriate debtor role.
async def payed(ctx, message_id=None, guild_id=None):
    #await ctx.send("Error: ")
    if message_id == None or guild_id==None:
        await ctx.send("Error: You are missing arguments. Please ensure your enter the command exactly as it was sent to you.")
        return
    try:
        try:
            guild = client.get_guild(int(guild_id))
        except Exception as e:
            await ctx.send("Error: Guild could not be found.")
            traceback.print_exception(type(e), e, e.__traceback__)
        try:
            member = guild.get_member(ctx.author.id)
            roles = member.roles
        except Exception as e:
            await ctx.send("Error: Member could not be found.")
            traceback.print_exception(type(e), e, e.__traceback__)
        
        role = None
        valid = False
        
        for i in range (len(roles)):
            if message_id in roles[i].name and "Debtor" in roles[i].name:
                valid = True
                role = roles[i]
                try:
                    await member.remove_roles(discord.utils.get(guild.roles, name = roles[i].name))
                except Exception as e:
                    await ctx.send("Error: Could not remove role.")
                    traceback.print_exception(type(e), e, e.__traceback__)


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
                            if 'Debtee' in roles[i].name:
                                debtee = discord.utils.get(guild.roles, name = roles[i].name)
                            else:
                                debtor = discord.utils.get(guild.roles, name = roles[i].name)
                        except Exception as e:
                            await ctx.send("Error: Could not find role.")
                            traceback.print_exception(type(e), e, e.__traceback__)
                
                try:
                    await debtee.members[0].send("All debtors of your loan " + debtee.name + " have payed.")
                except Exception as e:
                    await ctx.send("Error: Could not find role.")
                    traceback.print_exception(type(e), e, e.__traceback__)
                
                
                try:
                    await debtee.delete()
                    await debtor.delete()
                except Exception as e:
                    await ctx.send("Error: Could not delete role.")
                    traceback.print_exception(type(e), e, e.__traceback__)
    
    except Exception as e:
        await ctx.send("Error: Sorry, something unexpected went wrong.")
        traceback.print_exception(type(e), e, e.__traceback__)
  
@client.command() 
async def remind(ctx, loan_name=None): # Remind outstanding debtors of their loan
    if loan_name == None:
        await ctx.send("Error: You must provide a loan name.")
        return
    try:
        guild = ctx.guild
        role_id = None
        role = None
        try:
            role_id = re.sub("\D", "", loan_name)
            role = guild.get_role(int(role_id))
        except Exception as e:
            await ctx.send("Error: Could not find role.")
            traceback.print_exception(type(e), e, e.__traceback__)

        bot_message = ""

        if "Debtee" in role.name:
            new_role_name = role.name.replace("Debtee", "Debtor")
            role = discord.utils.get(guild.roles,name=new_role_name)


        if "Debtor" in role.name:
            try:
                message_id = int((role.name.split(" "))[2])
                valid = False

                for i in guild.get_member(ctx.author.id).roles:
                    if str(message_id) in i.name and 'Debtee' in i.name:
                        valid = True
                
                if valid == False:
                    await ctx.send("Error: You are not the debtee of this loan, so you cannot send a reminder for it.")
                    return



                for channel in guild.text_channels:
                    if await channel.fetch_message(message_id) != None:
                        bot_message = await channel.fetch_message(message_id)
            except Exception as e:
                await ctx.send("Error: Could not find loan message. It may have been deleted.")
                traceback.print_exception(type(e), e, e.__traceback__)
        else:
            await ctx.send("Error: You did not input a recognized sharkr debtor loan.")
            return


        
        for member in role.members:
            try:
                await member.send(bot_message.content)
                await member.send("Please enter '.sharkr payed " + str(message_id) + " " + str(guild.id) + "', without the quotation marks, once you have payed the loan or if you believe you are recieving this message by mistake.")
            except Exception as e:
                await ctx.send("Error: Could not find member.")
                traceback.print_exception(type(e), e, e.__traceback__)
    except Exception as e:
        await ctx.send("Error: Sorry, something unexpected went wrong.")
        traceback.print_exception(type(e), e, e.__traceback__)

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
        except Exception as e:
            await ctx.send("Error: Could not find role.")
            traceback.print_exception(type(e), e, e.__traceback__)


        if "Debtee" in role.name:
            new_role_name = role.name.replace("Debtee", "Debtor")
            role = discord.utils.get(guild.roles,name=new_role_name)

            
        if "Debtor" in role.name:
            try:
                message_id = int((role.name.split(" "))[2])
                valid = False

                for i in guild.get_member(ctx.author.id).roles:
                    if str(message_id) in i.name and 'Debtee' in i.name:
                        valid = True
                
                if valid == False:
                    await ctx.send("Error: You are not the debtee of this loan, so you cannot clear it.")
                    return
                else:
                    roles = guild.roles
                    debtee=None
                    debtor=None
                
                    for i in range (len(roles)):
                        if str(message_id) in roles[i].name:
                            try:
                                if 'Debtee' in roles[i].name:
                                    debtee = discord.utils.get(guild.roles, name = roles[i].name)
                                else:
                                    debtor = discord.utils.get(guild.roles, name = roles[i].name)
                            except Exception as e:
                                await ctx.send("Error: Could not find role.")
                                traceback.print_exception(type(e), e, e.__traceback__)
                    
                    try:
                        await debtee.delete()
                        await debtor.delete()
                        await ctx.send("Loan has been cleared")
                    except Exception as e:
                        await ctx.send("Error: Could not delete role.")
                        traceback.print_exception(type(e), e, e.__traceback__)

            except Exception as e:
                await ctx.send("Error: Could not find loan message. It may have been deleted.")
                traceback.print_exception(type(e), e, e.__traceback__)
        else:
            await ctx.send("Error: You did not input a recognized sharkr debtor loan.")
            return
    except Exception as e:
        await ctx.send("Error: Sorry, something unexpected went wrong.")
        traceback.print_exception(type(e), e, e.__traceback__)

@client.command()
async def outstanding(ctx, loan_name=None): # See outstanding debtors
    if loan_name == None:
        await ctx.send("Error: You must provide a loan name.")
        return
    try:
        guild = ctx.guild
        try:
            role_id = re.sub("\D", "", loan_name)
            role = guild.get_role(int(role_id))
        except Exception as e:
            await ctx.send("Error: Could not find role.")
            traceback.print_exception(type(e), e, e.__traceback__)


        if "Debtee" in role.name:
            new_role_name = role.name.replace("Debtee", "Debtor")
            role = discord.utils.get(guild.roles,name=new_role_name)

            
        if "Debtor" in role.name:
            lst = ""
            for member in role.members:
                lst += member.name + ", "
            await ctx.send("The oustanding debtors are: " + lst)

    except Exception as e:
        await ctx.send("Error: Sorry, something unexpected went wrong.")
        traceback.print_exception(type(e), e, e.__traceback__)


def processUserId(user_id):
    user_id = user_id.replace("<", "")
    user_id = user_id.replace(">", "")
    user_id = user_id.replace("@", "")
    user_id = user_id.replace("&", "")
    user_id = int(user_id)
    return user_id


client.run("")