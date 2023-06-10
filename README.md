# League of Numbers
 
## Project Description
League of Numbers is a Python project that allows you to store and analyze the game statistics over season 13. It provides functionality to save and manipulate the data, calculate various metrics, and generate insights from the collected stats.
 
## Features
* Store and manage the user's game statistics including kills, deaths, assists, vision score, minions killed, gold earned, damage dealt, experience gained, dragons and Barons slain as a team.
* Calculate some of the per minute stats for better accuracy.
* Compare the previously mentioned statistics with the direct lane opponent.
* Calculate the correlation between all of the metrics and the outcome of the game.
* Analyze the correlation between different statistics to identify patterns and trends.
* Generate visualizations of the collected stats.
 
 
## Prerequisites
- Python 3.10
- PiP
## Installation
1. Clone the project repository
2. In the terminal, create a .env file named ".env":
   ```
   touch .env
   ```
3. Copy your API key from [Riot Games' developer portal](https://developer.riotgames.com/).
4. Paste the API key to the .env file in the following format:
   ```
   api_key="YOUR_API_KEY"
   ```
5. Enter the folder of the cloned repository with the shell/terminal.
6. Install the prerequisites with:
   ```
   pip install -r requirements.txt
   ```
7. Once required libraries are installed, you can run the program:
   ```
   python3 league.py
   ```
## Usage
Once the project is set up and running, the application will ask you for your summoner name, server and queue type to be analyzed. **The game information is then parsed at a rate of 100 games per 2 minutes (this is the rate limit set by Riot Games, so if the program freezes, it's probably on cooldown).** After the games are parsed, you will get a choice of either analyzing either a specific position, or all positions. You will then get a list of all of the possible categories for you to inspect. Type in the category name with the underscores but without the single quotes!

## Correlation coefficient
The correlation coefficient is a statistical measure that quantifies the strength and direction of the relationship between two variables. It indicates how closely the data points of the variables align on a scatter plot. The correlation coefficient takes values between -1 and 1. The further from 0 the coefficient lies, the stronger the relationship between that category and the outcome is. 

**The correlation coefficient provides insights into the strength and direction of the relationship between variables but does not imply causation. It is important to consider other factors and conduct further analysis to establish causality between variables.**

## Contact
For any questions, suggestions or inquiries related to the tool, do not hesitate to contact me:  
[![Linkedin Badge](https://img.shields.io/badge/-Arnas%20miklovis-blue?style=for-the-badge&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/arnas-miklovis-1732a51b2/)](https://www.linkedin.com/in/arnas-miklovis-1732a51b2/)
[![Email Badge](https://custom-icon-badges.demolab.com/badge/-miklovisarnas@gmail.com-red?style=for-the-badge&logo=mention&logoColor=white&link=mailto:miklovisarnas@gmail.com)](mailto:miklovisarnas@gmail.com)
