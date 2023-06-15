# Nikhil Kagalwala
# Suyash Tewari
# Nick Project

# imports
import csv
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime 
from datetime import date
from calendar import monthrange
import math
from flask import Flask, request, Response, render_template, jsonify
import io

df = pd.read_csv("September 2021 Count Report.csv")

days_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
times = ["6:00 AM", "7:00 AM", "8:00 AM", "9:00 AM", "10:00 AM", "11:00 AM",
         "12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM",
         "6:00 PM", "7:00 PM", "8:00 PM", "9:00 PM", "10:00 PM", "11:00 PM"]


#get month and year from csv
date_arr = (df["Date"][0]).split("/")

year = int(date_arr[2][:4])

month = int(date_arr[0])

#get (first day of month, num of days in month)
monthData = monthrange(year,month)

#create 2D array for each day of the week (starting with monday), initialize it
# [i,j] = day of the week -> all dates of month that are on this day
# [0,0] = sep_6 (first monday of the month)
daysOfWeekData = [None, None, None, None, None, None, None]

for i in range(1, monthData[1] + 1):

    strDate = str(month) + "/" + str(i) + "/" + str(year) + " 0:00"
    data = df[df["Date"] == strDate]
    index = ((i + monthData[0]) % 7) - 1

    #define each first day of day of week
    if (i < 8):
        if (index == -1):
            index = 6
        daysOfWeekData[index] = [data]

    else:
        if (index == -1):
            index = 6
        daysOfWeekData[index].extend([data])


class Room:
    def __init__(self, name, max_capacity):
        self.name = name
        self.max_capacity = max_capacity
    
    def display_graph(self, day):

        counts = [0.0] * 18
        sums = [0.0] * 18
        avgs = [0.0] * 18
        day_data = daysOfWeekData[days_week.index(day)]        

        try:        
            for days in day_data:
                
                try:
                    curr_ind = days.index[days["Location"] == self.name].tolist()[0]

                except:
                    curr_ind = -1
                
                if (curr_ind != -1):                
                    for i in range(len(times)):
                        if (str(df.iloc[curr_ind][times[i]]) != "nan" and str(df.iloc[curr_ind][times[i]]) != "C"):
                            sums[i] += float(df.iloc[curr_ind][times[i]])
                            counts[i] += 1
            
            
            for i in range(len(counts)):
                # we have to stop this calculation if counts[i] = 0 and somehow show that there is not enough data for this graph
                if (counts[i] != 0.0):
                    avgs[i] = math.ceil(sums[i] / counts[i])
                else:
                    avgs[i] = 0
                
            return times, avgs
        
        except IndexError:
            return [], []
        except Exception as e:
            print(f"Error: {str(e)}")
            return [], []

app = Flask(__name__)

@app.route("/")
def home():
    default_room = "Nick Power House"
    default_day = "Monday"
    room = Room(default_room, 100)
    labels, values = room.display_graph(default_day)
    return render_template("index.html", days=days_week, default_room=default_room, default_day=default_day, labels=labels, values=values)

@app.route("/room_data", methods=["POST"])
def room_data():
    room_name = request.json.get("room")
    selected_day = request.json.get("day")

    room = Room(room_name, 100)
    labels, values = room.display_graph(selected_day)

    if len(labels) == 0 or len(values) == 0:
        print("handled error")
        return {'labels': [], 'values': []}

    return {'labels': labels, 'values': values}

        
        
