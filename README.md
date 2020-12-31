<p align="center">
<img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge">
<img src="https://img.shields.io/badge/opensource-python-yellow?style=for-the-badge">
<img src="https://img.shields.io/github/issues/Riken-Shah/InstaQuoteBot?style=for-the-badge">
<img src="https://img.shields.io/github/repo-size/Riken-Shah/InstaQuoteBot?style=for-the-badge" >
<img src="https://img.shields.io/github/last-commit/Riken-Shah/InstaQuoteBot?style=for-the-badge">
<img src="https://img.shields.io/github/stars/Riken-Shah/InstaQuoteBot?style=for-the-badge">
</p>
<br />
<p align="center">
  <a href="">
    <img src="./instabot.png" alt="Logo" width="300" height="200">
  </a>
    <h1 align="center"><b>InstaQuoteBot</b></h1>
    <p align="center">
Instagram bot who manages Instagram Quote Page
    </p>
</p>


# About Project
You can check out its live demo [here](https://www.instagram.com/__.i.n.s.p.i.r.e.d.__/).
## Top features
- Create image from raw data
- Post on Instagram
- Like the comments 
- New user can get the greeting message
-  Deployable Ready
- Customized Timming\
and many more features coming soon...

## Installation
Follow this below instruction to properly set up this project

### Step 1

Clone the project to your local device

```bash
git clone https://github.com/Riken-Shah/InstaQuoteBot.git
```

### Step 2
Change your directory 
```bash
cd InstaQuoteBot
```
### Step 3
Download the dependices
```python
pip install -r ./requirements.txt 
```

### Step 4

Install [Chromedriver](https://chromedriver.storage.googleapis.com/index.html?path=84.0.4147.30/)
and **copy it's path**.

### Step 5

Add the .env to your project directory\
Follow the instruction on properly setup this [file](.envTest)
### Step 6
🎉   **Power up the bot...**  🎉 
```bash
python run.py
```


## Your Own Instagram Page Manager:
**You can use this as your boilerplate code and create your own Instagram page which is managed by a bot.**


### Tips:
1. Want to integrate a database? View this [file](Scripts/Database/database.py)
2. Create customized templates for your posts. You can use this as your [base class](Scripts/Instagram/Templates/InstaPost.py) to get different functionalities out of the box...
3. Customzie caption message view [this](Scripts/Instagram/CaptionCreator.py) file
4. Want to customized timing? Go [here](run.py)
5. [Helper Functions](Scripts/Helpers)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
