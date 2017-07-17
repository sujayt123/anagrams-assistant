# anagrams-assistant
An app to help me train (and/or cheat?) for word games involving the Scrabble dictionary, especially [Anagrams](https://en.wikipedia.org/wiki/Anagrams) and its variants.

Live at https://anagrams-assistant.herokuapp.com/

I didn't bother inserting the results of the computation into a database, so there is no persistence of application data. Because of the
limitations of this free-tier Heroku application (sigh), the user attempting to access the site after process reboot may have to wait several minutes for the server
to compute the application data. After a few minutes, the server should finish preprocessing ready to receive data and all subsequent
users should be served.
