#!/usr/bin/env python
# coding: utf-8

# # Scraping Team Seas Data for analysis

# In[1]:


import requests
import pandas
from bs4 import BeautifulSoup
from datetime import datetime
# import locale
# import matplotlib.pyplot as plt

def get_count():
    req = requests.get("https://tscache.com/donation_total.json")
    return req.json()["count"]


# locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
headers = {"User-Agent": "Mozilla/5.0"}
# r = requests.get("https://teamseas.org/all-donors/", headers=headers)
r = requests.get("https://tscache.com/lb_recent.json")
# soup = BeautifulSoup(r.content, "html.parser")
donations = r.json()
# donations.keys()
# donations["recent"]

df_li = []
for recents in donations["recent"]:
    d = {}
    d["name"] = recents["name"]
    if recents["team_name"]:
        d["team_name"] = recents["team_name"]
    else:
        d["team_name"] = "Anonymous"
    d["created"] = datetime.strptime(datetime.utcfromtimestamp(int(recents["created_at"])).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
    d["amount"] = int(recents["pounds"].replace(",", ""))
    df_li.append(d)

df = pandas.DataFrame(df_li)

# ## Plot of Donations vs Time


def donation_time():
    return df
# plt.figure(figsize=(25, 10))
# # plt.yticks(range(min(df["amount"]), max(df["amount"])))
# plt.ylim(0, df["amount"].max())
# plt.plot(df["created"], df["amount"])


# ## Grouping according to teams

def team_group():
    grouped_data = df.groupby(df["team_name"])["amount"].sum()

    teams_df = pandas.DataFrame({"team_name": grouped_data.index, "total_donated": grouped_data.values})

    teams_df.sort_values(by=["total_donated"], ascending=False, inplace=True)
    return teams_df

# plt.figure(figsize=(25, 3))
# plt.pie(teams_df["total_donated"], labels=teams_df["team_name"])


# ## Hourly Average
def hour_group():
    df["hour"] = df["created"].dt.strftime("%H")

    hourly_grp = df.groupby(df["hour"])["amount"].sum()

    hourly_df = pandas.DataFrame({"hour": hourly_grp.index, "total_donation": hourly_grp.values})
    return hourly_df

# plt.figure(figsize=(25, 3))
# plt.plot(hourly_df["hour"], hourly_df["total_donation"])


# ## Minute Average 
def minute_group():
    df["minute"] = df["created"].dt.strftime("%H-%M")

    minute_grp = df.groupby(df["minute"])["amount"].sum()

    minute_df = pandas.DataFrame({"minute": minute_grp.index, "total_donation": minute_grp.values})
    return minute_df

# plt.figure(figsize=(30, 3))
# plt.plot(minute_df["minute"], minute_df["total_donation"])

df_li2 = []
for mst in donations["most"]:
    d = {}
    d["name"] = mst["name"]
    d["amount"] = int(mst["pounds"].replace(",", ""))
    d["created"] = datetime.strptime(datetime.utcfromtimestamp(int(mst["created_at"])).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
    df_li2.append(d)

df2 = pandas.DataFrame(df_li2)

# plt.figure(figsize=(25, 10))
# plt.bar(df["name"], df["amount"], width=0.4)


def single_most_donations():
    return df2


# plt.figure(figsize=(20,3))
# plt.plot(date_sorted["created"], date_sorted["amount"])


def date_sorted():
    sorted_df = df2.sort_values(by=["created"])
    return sorted_df


df_li3 = []
for i in donations["teams_most_donations"]:
    d = {}
    if not i["team"]:
        d["team_name"] = "Anonymous"
    else:
        d["team_name"] = i["team"]
    d["donation"] = int(i["total_donation"].replace(",", ""))
    d["members"] = int(i["total_members"])
    df_li3.append(d)

df3 = pandas.DataFrame(df_li3)
df3["avg"] = df3["donation"]/df3["members"]

# plt.figure(figsize=(25, 3))
# plt.plot(df["team_name"], df["donation"])


def team_donation():
    return df3

# plt.figure(figsize=(25, 3))
# plt.plot(df["team_name"], df["avg"])


# %%
