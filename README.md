# InstaQuoteBot
Instagram Quote Page which is handled by a **Bot**.

<p align="left">

<img src="https://img.shields.io/badge/build-passing-green">

<img src="https://badges.frapsoft.com/os/v1/open-source.svg?v=103" >

<img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat">

</p>

---

## Installation
Follow this below instruction to properly set up this project

### Step 1

Install the project to your local device

```bash
git clone https://github.com/Riken-Shah/InstaQuoteBot.git
```

### Step 2
Change your directory 
```bash
cd InstaQuoteBot
```
### Step 3
Download the dependices\
For Windows User
```python
pip -r install ./requirements.txt 
```
For Mac/Ubuntu User
```python
pip3 install -r ./requirements.txt 
```

### Step 4

Install chromedriver ([link](https://chromedriver.storage.googleapis.com/index.html?path=84.0.4147.30/))\
and **copy it's path**.

### Step 5

Add the .env to your project directory\
Follow the instruction on this [file](.envTest)\
**Don't forget to change it's name to ```.envTest -> .env```**

## Running

🎉   **Let's power up the bot...**  🎉 \
For Windows Users
```bash
python run.py
```
For Mac/Ubuntu Users
```bash
python3 run.py
```


## Your Own Instagram Page Manager:
**You can use this as your boilerplate code and create your own Instagram page which is managed by a bot.**
### Top Features:
1. Post on Instagram
2. Like the comments
3. New user can get the greeting message
4. Deployable (*Only if you follow the same pattern)
5. Customized Timming\
and many more features coming soon...

### Tips:
1. Want to integrate a database? View this [file](Scripts/Database/database.py)
2. Want to add raw data to your database? Add your scripts [here](Scripts/AddQuotes)
3. Create customized templates for your posts. You can use this as your [base class](Scripts/Instagram/Templates/InstaPost.py) to get different functionalities out of the box...
4. Customized the timing go [here](run.py)
5. [Helper Functions](Scripts/Helpers)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update [tests](Tests) as appropriate.
