# Database Project “Tournament Planner” for Udacity Full-Stack Nanodegree

###### Final project for the Udacity course “Intro to Relational Databases” in support of the [Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004). Built a PostgreSQL relational database scheme to store the results of a game tournament. Also provided a number of queries to efficiently report the results of the tournament and determine the winner.

## Quickstart:

This project was created and tested using a Vagrant virtual machine and PostgreSQL. Please see "Step by step instructions for launch" section below.

## What’s included:

/:
   - readme.md 
   - tournament.sql (database schema)
   - tournament_test.py (testing code, provided by course instructor)
   - tournament.py (Python code written by Heather Phelps)
 
  
## Step by step instructions for launch:

* Start the vagrant virtual machine terminal from within the installation folder by typing **vagrant ssh** in the command line.
* Change to the vagrant directory using **cd /vagrant**
* Change to the tournament directory using **cd tournament** 
* Start PostgreSQL using **psql**
* create the necessary tables by running **\i tournament.sql**
* run **python tournament_test.py** to test the database query

## Creator

Created by Heather Phelps
Github: https://github.com/phelpsh

