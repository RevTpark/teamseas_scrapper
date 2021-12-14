from flask import Flask, render_template
import TeamSeas

app = Flask(__name__)


@app.route("/")
def home():
    data = {}

    data["count"] = TeamSeas.get_count()

    overall_df = TeamSeas.donation_time()
    team_grp = TeamSeas.team_group()
    hour_grp = TeamSeas.hour_group()
    minute_grp = TeamSeas.minute_group()

    df_labels = [i.strftime("%Y-%m-%d %H:%M:%S") for i in overall_df["created"]]
    df_values = [i for i in overall_df["amount"]]
    data["graph1"] = {"label": df_labels, "value": df_values}

    team_labels = [i for i in team_grp["team_name"].values]
    team_values = [i for i in team_grp["total_donated"].values]
    data["graph2"] = {"label": team_labels, "value": team_values}

    hour_labels = [i for i in hour_grp["hour"]]
    hour_values = [i for i in hour_grp["total_donation"]]
    data["graph3"] = {"label": hour_labels, "value": hour_values}

    minute_labels = [i for i in minute_grp["minute"]]
    minute_values = [i for i in minute_grp["total_donation"]]
    data["graph4"] = {"label": minute_labels, "value": minute_values}

    return render_template("index.html", data=data)


# data -> donation vs time -> label value
#      -> team vs donation -> label value | pie chart
#      -> hourly average -> label value
#      -> minute average -> label value

@app.route("/most")
def teams():
    data = {}

    data["count"] = TeamSeas.get_count()

    overall_df = TeamSeas.single_most_donations()
    overall_labels = [i for i in overall_df["name"]]
    overall_values = [i for i in overall_df["amount"]]
    data["graph1"] = {"label": overall_labels, "value": overall_values}

    sorted_df = TeamSeas.date_sorted()
    date_labels = [i.strftime("%Y-%m-%d %H:%M:%S") for i in sorted_df["created"]]
    date_values = [i for i in sorted_df["amount"]]
    date_name = [i for i in sorted_df["name"]]
    data["graph2"] = {"label": date_labels, "value": date_values, "name": date_name}

    team_donation = TeamSeas.team_donation()
    team_labels = [i for i in team_donation["team_name"]]
    team_values = [i for i in team_donation["donation"]]
    avg_value = [i for i in team_donation["avg"]]
    data["graph3"] = {"label": team_labels, "value1": team_values, "value2": avg_value}
    return render_template("teams.html", data=data)

