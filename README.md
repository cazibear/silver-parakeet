train-times-cli
===============
This program aims to display train times and relevant data to the user via the command line.

Usage
-----
    main.py info <station>
          " departures <station> [<search>]
          " save <function> <argument(s)>
          " load <file> <arguments>

The program is run by providing a function and then 1 or more arguments

Functions
---------
The currently available functions are: `info`, `departures`, `save`, `load`, and `config`.

`info` takes a station name as an argument and returns some information on it. `departures` takes a 
station name, and optionally another station to search for only trains to that station. `save` runs
the a function name given with the arguments given and saves it to a file for later. `load` uses 
some json data from a file created from `save` function, and gets the function from its path with
the option of using the arguments given. `config` takes two parameters: the 

Requirements
------------
This project uses: [Transport API](https://www.transportapi.com/) for all it's data so an account
for that service will be required.
