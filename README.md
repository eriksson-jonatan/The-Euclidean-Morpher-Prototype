# The-Euclidean-Morpher-prototype
This is a prototype program for music production that was developed for a degree project course (HI111X) at KTH Flemingsberg, Stockholm, Sweden.
It was developed by Jonatan Eriksson in 2024.

The Euclidean Morpher inputs one manually rhythmic pattern, one specified Euclidean rhythm, and one parameter named morph.
By pressing "GENERATE" new rhythmic patterns will be appended to a MIDI file, that can then be saved to a specified location.
The morph parameter is used to introduce variations to the rhtymic pattern when outputting to the file.

Python is required to run the program. Python 3.12.3 was used in development.
To install the required packages, open the command prompt in the source code folder and execute the command:
pip install -r requirements.txt
Then run the program with:
python main.py
