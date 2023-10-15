# About 
Project was realized for fun and sentiment.
It's an fully automated bot for a webrowser game with a lot of features.

# Features 
- Projected headless with the possiblity to use:
- - GUI written in PyGame,
- - terminal interface,
- - through a remote communication using Discord.

- Item Database -- there is an database implemented, thanks to it the bot is collecting information about the drop rate of every location visited by the bot.
- Command system -- the bot can be used without a need to direct interference the game.


# Discord bot commands
'''
!help
Retrieves the help information about every command.

!reboot
Reboots pokewars process and relogins in case 
something crashed or bot was logged out.

!login
Logins the user, used in case the session expired.

!start
Starts hunting in choosen location with choosen pokemon,
if elm quest detected, then the location accordingly changes.

!stop
Stops the hunting sessions.

!reset
Reconfigures the pokemon and hunt list,
in case someone changed the mentioned lists.

!set
Sets the most important settings in form:
-
- set x y
-
where x - pokemon index, y - hunt location.

!screenshot
Makes a screenshot of the currently working driver.

!show
Gives information about the working bot.
-
- shot x
-
where x can be:
- - list
- and it returns the list of location and pokemons,
- - status
- gives the information about the settings.


!debug
It is for debugging selenium purposes.
-
- debug par
-
where par is the XPATH searched by the app.
'''
