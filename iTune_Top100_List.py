# -*- coding: utf-8 -*-
"""
Python Programming I - Final Project
Created on Mon Sep 02 10:22:50 2019
@author: Chia-Yu Chen
"""


import requests
from bs4 import BeautifulSoup
import pandas as pd


# Let user input what kind of list he/she wants
print('Please enter what kind of top 100 list do you want? (song/album)')
user_input = input()


# Get main website
def get_top100_url():
    itunes_url = 'https://www.apple.com/itunes/charts/'
    res = requests.get(itunes_url)
    res.raise_for_status()  # check the url is fine
    soup = BeautifulSoup(res.text, 'html.parser')   # pass the page into the BeautifulSoup module

    if user_input == 'song':
        type_link = soup.select('a[class="songs"]')[0]
        url = 'https://www.apple.com' + type_link.get('href', 'html.parser')
        return url
    elif user_input == 'album':
        type_link = soup.select('a[class="albums"]')[0]
        url = 'https://www.apple.com' + type_link.get('href', 'html.parser')
        return url


def html_parse():
    url = get_top100_url()
    res2 = requests.get(url)
    res2.raise_for_status()
    # pass the page into the BeautifulSoup module
    soup = BeautifulSoup(res2.text, 'html.parser')

    # Get Position
    getposition = soup.find_all('strong')
    positions = [item.get_text() for item in getposition]

    # Get Track/Album Name
    getkname = soup.find_all('h3')
    names = [item.get_text() for item in getkname[0:100]]

    # Get Artist
    getartist = soup.find_all('h4')
    artists = [item.get_text() for item in getartist]

    # Get Song/Album URL
    getlink = soup.find_all('a', class_ = 'more')
    links = [item.get('href') for item in getlink[1:]]


    # Create dataframe in order to export it to csv file
    my_df = pd.DataFrame({
        "Position": positions,
        "Name": names,
        "Artist": artists,
        "URL": links
    })


    # Create csv file name and columns names
    column_names = ['Position', 'Name', 'Artist', 'URL']
    if user_input == 'song':
        my_df[column_names].to_csv('iTune Top 100 Songs.csv', index = False, sep = ',', header = True, encoding = 'utf-8-sig')
    elif user_input == 'album':
        my_df[column_names].to_csv('iTune Top 100 Albums.csv', index = False, sep = ',', header = True, encoding = 'utf-8-sig')


    # Write all the data into text file
    for position, name, artist, link in zip(positions, names, artists, links):
        position = 'Position: ' + str(position) + '\n'
        name = 'Name: ' + str(name) + '\n'
        artist = 'Artist: ' + str(artist) + '\n'
        link = 'URL: ' + str(link) + '\n'

        data = position + name + artist + link

        # save the data
        txt.writelines(data + "---------------------------------------------------------------------" + '\n')


# Create txt file name
if user_input == 'song':
    txtfilename = 'iTune Top 100 Songs.txt'
elif user_input == 'album':
    txtfilename = 'iTune Top 100 Albumss.txt'

txt = open(txtfilename, 'w', encoding='utf-8')


# Call the function to operate
html_parse()


# Close txt file
txt.close()


print('Downloaded successfully!')


