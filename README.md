# ✨ best-hn
Best of HackerNews to save time. It generates summary of top stories reaching > 200 score, so that you don't have to visit hackernews again and again to check top stories.

## Summary Cards - Sample

![Summary Card](sample.png)

## how to use

- use `huey` instance to save summary of top stories every two hours
- use `now.py` to get last 4 hours top stories summary

## installation

clone the project

```bash
$ git clone https://github.com/ksh7/best-hn.git
$ cd best-hn
```

create virtual environment using python3 and activate it

```bash
$ python3 -m venv /path/to/your/virtual/environment
$ source <path/to/venv>/bin/activate
```

install dependencies in virtualenv

```bash
$ pip install -r requirements.txt
```

## Run background scheduler

start `huey` scheduler instance

```bash
$ sudo huey_consumer.py huey_app.huey -w 2 &
```
check summary images in `hn-summary` folder date-wise

## Fetch last 4 hours stories

```bash
$ python now.py
```
check summary images in `hn-summary-now` folder date-wise
