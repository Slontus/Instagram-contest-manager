# Instagram contest manager

This program designed to define all Instagram contest participants who 
accomplished the contest conditions: added at least one friend in a message, 
liked  the post and followed the post's author.

### How to Install

Python3 should be already installed. Then use pip (or pip3,
if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```
To run this program you need to save your Instagram account 
credentials in **.env** file  which you should create
in the same directory with **main.py** file.
Credentials should be saved in the following format:
```
INTSAGRAM_USER=your_instagram_user_name
INSTAGRAM_PASSWORD=your_instagram_password
```
### An example of usage
To run this script please pass url of Instagram contest page
as first argument and nikname of author of the post as second argument:
```
>python main.py https://www.instagram.com/p/CAHroaMDiR8/ mariabelluccii
```
The possible result of script execution presented below:
```
{'0_photo_art_00',
 '311_natalia',
 '_50598008_',
 '___alfia___56',
 '__angelina__food__',
  ...
 'zmeika99',
 'zsfjdexsawf'}
```

### Project Goals
The code is written for educational purposes on online-course 
for web-developers [dvmn.org](https://dvmn.org).