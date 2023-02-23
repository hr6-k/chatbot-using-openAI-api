import openai

# u must creat ur own api key, its saved in .hidden.txt as a single line
# we need to provide openai with our api key
# to do that:
with open(".hidden.txt") as file:
    openai.api_key = file.read()

# u can easily write it also like this -> openai.api_key = ""
# print(openai.api_key)


# next we can creat our first function, which gets an api response
# its going to take a prompt of type string as parameter
# and its going to return us either a string or None, depending on what we provided
# maybe there is gonna be an error, when there is an error I want this to return None, not getting an error
# that’s why I wrote an optional type at its return
def get_api_response(prompt:str) -> str | None:
    # then the first thing we need to creat here is a text of type string or None, mean type optional
    # its going to be None initialy, because this can end up being a string or end up being None 
    text: str | None = None

    # so here we are going to start with a try block
    # and it is going to take a response, or we ar going to creat a response of type dictionary
    # and thats going to equel openai.Completion.create() and here we are going to creat a request, which gives us a response
    try:
        response: dict = openai.Completion.create(

            # so first we need to specify a model and it is going to be text-davinchi-003, in my playgorund i account on the write side is written
            model = "text-davinci-003",

            # for the prompt, we are going to just insert the prompt
            prompt = prompt,

            # then we have the temperature, which is a float, and I am going to set that to 0.9
            # and the higher temperature, more random ur bot is going to be
            temperature = 0.9,

            # and there is one called, max_tokens, we are setting that 150 for now
            # it is the legth of the response, max is 4000 which gives very long response
            # I will leave it at 150 because token cost u money, its good u to know that u want to use less token in some scenarios
            # so we want to use 150 token per response
            # if u go back to ur playground u see this adjustment on the right side, max is 4000 which answers very long
            max_tokens = 150,

            # then we have top_p, we write 1, 1  is also its default value
            # the documentation describes that as an alternative to the temperature
            top_p = 1,

            # then there is frequency penalty, we give 0
            # that reduces verbatim line repetitiveness
            frequency_penalty = 0,


            # then we have the presence penalty, we give 0.6
            # this presence penalty determines how often the AI ia going to talk about new subjects
            # if u have lower presence penalty, its going to repeate itself
            presence_penalty = 0.6,


            # and most importantly, we need to prive a stop
            # this would be an array of the stops (first a space and Human followed by a space and AI) 
            # so these are stop words, means once it runs into this, it knows it must not generate any more responces
            stop = [" Human:", " AI:"]
        )
        # in print e inja, marbout e test kardane payine
        #print(response)

        # waghty in ala in response ro print koni wa baad bakhshe test section e payin ro ejra koni
        # mifahmi chetor daram in payin ro migiram
        # hada asli inja ine ke, faghat javabe AI ro print konam na kolle json file ro
        choices: dict = response.get("choices")[0] # in choicese dowom dar in line yek kelid dar json hastesh ke list bar migardoune, eleman e awalesh ro migirim ke yek dict hastesh
        # wa dar in khat az dict e khatte bala, kelide text ro migirim
        text = choices.get("text")

    # and just to get rid of error
    except Exception as e:
        print("ERROR:", e)
    
    # at the very bottom, out of except, we are going to return the text
    return text


############# test section ###################
# here is just to test, every thing works well
#prompt = "Hello"
#get_api_response(prompt)

# test 2
#prompt = "Hello there!"
#print(get_api_response(prompt))
#############  end of test ###################


# here we are going to add function that adds each message that we creat to an array
# and also goes to add each message that bot creates to that array
# so we r gonna have kind of message history
# so we define a function that gets message type string, whether it comes from bot or us
# we also want to have this prompt list(pl), to be passed in. and this is going to be a list of type strings
def update_list(message:str, pl:list[str]):
    # all we are going to do is to append the message to that list
    pl.append(message)

# so now comes second func.
# with that list (pl) we need to create a prompt, since we are going to have an array of messages 
# or list of messages, we r going to consolidate that into a single string. and thats where this function comes into the play
# its going to take a message type of string, followed by prompt list (pl) which is a list of type string(list[str]) and its going to return to us a string 
def create_prompt(message: str, pl: list[str]) -> str:
    # then we r going to have a processed message(p_message) of type string
    # that°s going to be a formatet string with a new line follwed by Human:, and we need to insert the message
    # this new line \n is very important, because thats how this bot is designed, each time that we say new line Human or new line bot, it gives the bot further context on how to processd with answering the question
    p_message: str = f"\nHuman: {message}"

    # with that we can update the list, with the processed message (p_message) and the prompt list(pl)
    update_list(p_message, pl)

    # we want to join every thing in the prompt list(pl)
    prompt: str = "".join(pl) 

    # and we return the prompt
    return prompt

# the last thing we need, is a function for giving us the response from the bot in a clean format
def get_bot_response(message: str, pl: list[str]) -> str:
    # first we want to get the prompt
    prompt: str = create_prompt(message, pl)
    # now bot response
    bot_response: str = get_api_response(prompt)

    # it is also imoirtant that we check the bot response is not None
    if bot_response: # so if there is a bot response, then we can update the list
        # we can insert out bot response to the prompt list
        update_list(bot_response, pl)

        # we need to also get a position of the AI response
        # so here we creat a variable called position (pos) type integer
        pos: int = bot_response.find("\nAI: ") # new line AI colone(:) and a space. we are finding this("\nAI: ") because we want to print what comes after that
        # so the bot response is going to be every thing beyond this "\nAI: "
        bot_response = bot_response[pos + 5:]
    else:
        bot_response = "Something went wrong..."
    
    return bot_response

# main function
# now we have all the functions we want. we need to just glue them all together
def main():
    # here we r going to creat the prompt list.
    # this famous prompt list we were inserting every where, finally we r going to creat it here
    # which will be a list of type string
    # and after =, we need to provide a training data
    # first line I am telling in which way he should talk, and then next lines I am giving him an example, Human asks what time is it and you(boy) must answer like that with ye
    # u can define the prompt(first line) as u like and after that u can make an example, it will understand what u mean
    prompt_list: list[str] = ["You will pretend to be a skater dude that ends every response with \"ye\"",
                              "\nHuman: What time is it?",
                              "\AI: It is 12:00, ye"]

    while True:
        #user input which is us
        user_input:str = input("You: ")

        # we need to get response now
        # it will take user input as the message
        # and the prompt list as the prompt list pl
        response: str = get_bot_response(user_input, prompt_list)

        # and all we need is to print bots response
        print(f"Bot: {response}")

        # one thing u can do to understand what prompt list is
        # print prompt list after each itteration while true
        # and then u can see all the converstation and u will understand better what is happening
        #print(prompt_list)



if __name__ == "__main__":
    main()
    

    


    
