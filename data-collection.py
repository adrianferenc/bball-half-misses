#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 16:54:04 2021

@author: adrianferenc
"""

import requests
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import os
import lxml

'''
This function creates a list of links of every game's play-by-play from basketball-reference.com from the iput season.
'''
def link_lister(year):
    months = ['october', 'november', 'december', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september']
    list_of_links = []
    prefix = 'https://www.basketball-reference.com/boxscores/pbp/'
    suffix = '.html'
    for month in months:
        url = 'https://www.basketball-reference.com/leagues/NBA_'+ year +'_games-' + month + '.html'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        table = [td for td in soup.findAll('td', {'data-stat': 'box_score_text'})]
        rows = len(table)
        for line in range(rows):
            if len(str(table[line])) > 60:
                list_of_links.append(prefix+str(table[line])[66:78]+suffix)
    return list_of_links


'''
This creates a class for each player and adds categories for each player's stats
'''
class Player_stats:
    def __init__(self, name, team):
        self.name = name
        self.team = team
        self.assists = 0 #
        self.fts = 0 #
        self.ftas = 0#
        self.twops = 0#
        self.threeps = 0#
        self.twoas = 0#
        self.threeas = 0#
        self.games = 0#
        self.drebounds = 0
        self.orebounds = 0
        self.turnovers = 0
        self.halfmisses = 0
    def addassist(self):
        self.assists+=1
    def addft(self):
        self.fts+=1
    def addfta(self):
        self.ftas+=1
    def addtwop(self):
        self.twops+=1
    def addtwoa(self):
        self.twoas+=1
    def addthreep(self):
        self.threeps+=1
    def addthreea(self):
        self.threeas+=1
    def addgame(self):
        self.games+=1
    def adddrebound(self):
        self.drebounds+=1
    def addorebound(self):
        self.orebounds+=1
    def addturnover(self):
        self.turnovers+=1
    def addhalfmiss(self):
        self.halfmisses+=1

    def ppg(self):
        if self.games > 0:
            return (self.fts + 2*self.twops + 3*self.threeps)/self.games
        else:
            return 0
    def apg(self):
        if self.games > 0:
            return (self.assists)/self.games
        else:
            return 0
    def bpg(self):
        if self.games > 0:
            return (self.blocks)/self.games
        else:
            return 0
    def ftpg(self):
        if self.games > 0:
            return (self.fts)/self.games
        else:
            return 0
    def twospg(self):
        if self.games > 0:
            return (self.twops)/self.games
        else:
            return 0
    def threespg(self):
        if self.games > 0:
            return (self.threeps)/self.games
        else:
            return 0
    def drpg(self):
        if self.games > 0:
            return (self.drebounds)/self.games
        else:
            return 0
    def orpg(self):
        if self.games > 0:
            return (self.orebounds)/self.games
        else:
            return 0
    def rpg(self):
        return self.orpg + self.drpg
    def tvpg(self):
        if self.games > 0:
            return (self.turnovers)/self.games
        else:
            return 0 


'''
This gives each player a unique id in a list, where a player is defined by their name and their team. 
This is done so as not to confuse multiple players with the same first initial and last name. 
***A current issue with this is if a player is traded they are identified multiple times***
'''
list_of_all_players = []
def player_id(name,team):
    answer = -1
    for player in list_of_all_players:
        if player.name == name and player.team == team:
            answer = list_of_all_players.index(player)
            break
    if answer != -1:
        return answer
    else:
        list_of_all_players.append(Player_stats(name,team))
        return len(list_of_all_players)-1


'''
This parses the data from a game and adds all the stats to each player's class.
'''
def stat_adder(plays,team):
    players = []
    line_number = 0
    for line in plays:
        line = line.split(' ')
        length = len(line)
        if length >=5:
            if line[-4] == '(assist':
                name = line[-2] + ' ' + line[-1][:-1]
                list_of_all_players[player_id(name,team)].addassist()
                players.append(name)
            if line[2] == 'misses':
                name = line[0]+' ' +line[1]
                if line[3][0] == 'f':
                    list_of_all_players[player_id(name,team)].addfta()
                    players.append(name)
                if line[3][0] == '2':
                    list_of_all_players[player_id(name,team)].addtwoa()
                    players.append(name)
                if line[3][0] == '3':
                    list_of_all_players[player_id(name,team)].addthreea()
                    players.append(name)
            if line[2] == 'makes':
                name = line[0]+' ' +line[1]
                if line[3][0] == 'f':
                    list_of_all_players[player_id(name,team)].addft()
                    list_of_all_players[player_id(name,team)].addfta()
                    players.append(name)
                if line[3][0] == '2':
                    list_of_all_players[player_id(name,team)].addtwop()
                    list_of_all_players[player_id(name,team)].addtwoa()
                    players.append(name)
                if line[3][0] == '3':
                    list_of_all_players[player_id(name,team)].addthreep()
                    list_of_all_players[player_id(name,team)].addthreea()
                    players.append(name)
            if line[1] == 'rebound':
                name = line[3] + ' ' + line[4]
                if line[0] == 'Offensive':
                    list_of_all_players[player_id(name,team)].addorebound()
                    players.append(name)
                    hm_line = plays[line_number-1].split(' ')
                    if len(hm_line)>=4:
                        if hm_line[2] == 'misses' and hm_line[3] != 'free':
                            half_misser = hm_line[0] + ' ' + hm_line[1]
                            list_of_all_players[player_id(half_misser,team)].addhalfmiss()
                if line[0] == 'Defensive':
                    list_of_all_players[player_id(name,team)].adddrebound()
                    players.append(name)
            if line[0] == 'Turnover':
                if line[2] != 'Team':
                    name = line[2] + ' ' + line[3]
                    list_of_all_players[player_id(name,team)].addturnover()
                    players.append(name)
        line_number+=1
    players = np.unique(players)
    for name in players:
        list_of_all_players[player_id(name,team)].addgame()
        

'''
This begins to compile the data for each year desired.
'''
start_year =2012
end_year = 2021

years = [str(x) for x in range(start_year,end_year+1)]

for year in years:
    print('starting year {}'.format(year))
    list_of_all_players = []
    game_number = 1
    list_of_links = link_lister(year)
    total_games = len(list_of_links)
    for url in list_of_links:
        print(url)
        game = pd.read_html(url)[0]
        home_team = str(game.columns[5][1])
        away_team = str(game.columns[1][1])
        table_home = pd.read_html(url)[0].dropna(subset=[game.columns[5]]).reset_index()
        home_plays = table_home[table_home.columns[6]]
        table_away = pd.read_html(url)[0].dropna(subset=[game.columns[1]]).reset_index()
        away_plays = table_away[table_away.columns[2]]

        stat_adder(home_plays,home_team)
        stat_adder(away_plays,away_team)
        print('Game '+ str(game_number) + ' out of '+ str(total_games) + ' complete.')
        game_number+=1
    Complete_Stats = pd.DataFrame(data = {'Name': [x.name for x in list_of_all_players], 'Team': [x.team for x in list_of_all_players], 'Assists': [x.assists for x in list_of_all_players], 'Free Throws': [x.fts for x in list_of_all_players], 'Free Throw Attempts': [x.ftas for x in list_of_all_players], 'Two Pointers': [x.twops for x in list_of_all_players], 'Three Pointers': [x.threeps for x in list_of_all_players], 'Two Point Attempts': [x.twoas for x in list_of_all_players], 'Three Point Attempts': [x.threeas for x in list_of_all_players], 'Games Played': [x.games for x in list_of_all_players], 'Defensive Rebounds': [x.drebounds for x in list_of_all_players], 'Offensive Rebounds': [x.orebounds for x in list_of_all_players], 'Turnovers': [x.turnovers for x in list_of_all_players], 'Half Misses': [x.halfmisses for x in list_of_all_players]})
    Complete_Stats.to_csv('/data/Complete_Stats_{}.csv'.format(year))
    print('Finished with year {}'.format(year))


'''
Lastly, this combines all individual years into one complete set of statistics.
'''
years_for_csv = [str(x) for x in range(start_year,end_year)]
CompleteSTATSTEST = pd.DataFrame()
for year in years_for_csv:
    print(year)
    df = pd.read_csv('/data/Complete_Stats_{}.csv'.format(year), header = 0)
    CompleteSTATSTEST = CompleteSTATSTEST.append(df, ignore_index=True)

CompleteSTATSTEST = CompleteSTATSTEST.groupby(['Name','Team'])[CompleteSTATSTEST.columns[3:]].sum()
CompleteSTATSTEST.to_csv('/data/Complete_Stats_{}-{}.csv'.format(start_year,end_year))


