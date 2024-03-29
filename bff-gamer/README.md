# BFF: gaming UX

[Notion page](https://heather-roarer-0b9.notion.site/BFF-UX-for-gaming-74bacb4ef85a48378cdd4ebdcda98567?pvs=4)

## Why?

- Remember this?
    
    ![Untitled](static/Untitled.png)
    
- And this?
    
    ![Untitled](static/Untitled%201.png)
    
- Or, maybe, this?
    
    ![Untitled](static/Untitled%202.png)
    

### Good times, right?

### What do you think *really* made it special?

### Thats right, this guy:

![Untitled](static/Untitled%203.png)

# Proposal for an AI BFF demo

### How does it work?

- v.A
    - open a web page and press a button to start a call with your BFF. Say yes to share screen and allow mic.
    - you play anything and your BFF “looks over your shoulder” and you can talk to it with the context of the game
    - You finish the game and when you start BFF remembers all the “cool” moments you shared before.
- v.B
    - You open a web page and press a button to start a call with your BFF
    - You play some game and BFF plays that game with you just like it was in middle-school.
    - You finish the game and when you start BFF remembers all the “cool” moments you shared before.

### Requirements from AI

- v0
    - (tbd)
- v1
    - latency →0
    - interruptions (like retell demo)
    - can play that game with you
    - has distinct voice and personality  that is chosen randomly (that is a requirement for authenticity)
    - remember, observe, reflect, and decide on actions

### Building blocks

- Retell API for speech synth
    - [https://docs.retellai.com/integrate-llm/overview](https://docs.retellai.com/integrate-llm/overview)
    - [https://github.com/RetellAI/python-backend-demo/tree/main](https://github.com/RetellAI/python-backend-demo/tree/main)
    - [https://github.com/RetellAI/retell-frontend-reactjs-demo/](https://github.com/RetellAI/retell-frontend-reactjs-demo/)
- some super fast LLM streaming (retell llm is not good beaseu we need dynamic prompts as memory and stuff)
- <some game that has good bots and can be wired on in a simple way (.io games, text based games, etc.)>
- fast vision model that sees what on the screen of the game and puts it into context of *Cognitive architecture*

### Dynamic prompting (rules for how our AI will change prompts)

At any point of time there is a state at which your BFF:
    - a mix of fear, love, happiness, sadness, anger, disgust, surprise and maybe anything else
To reflect that state in AI behavior

### Other ideas to supply context to your BFF though games

- I think Steam or others have a button to “observe” your game - can this be used to make it really simple to connect with your BFF? You just call it and it already sees what Spotify you are listening too, what game you are playing, it can observe your game, it can do smth autonomosly while your are doing smth.

## Contributions

Join "The Orchard" Discord: [https://discord.gg/ghRUkRwA](https://discord.gg/ghRUkRwA) - look for “User Interface” channel. Email holins12@gmail.com if link is expired.

## Job postings

- Some Vercel (or just Node/React) pro. Be active on Discord or email [holins12@gmail.com](mailto:holins12@gmail.com)