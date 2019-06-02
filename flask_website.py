from flask import Flask, render_template, request
import requests
import json

key = *STEAM_API_KEY_HERE*
app = Flask(__name__)
@app.route('/')
def steam_form():
    return render_template("form.html")

@app.route('/', methods=["POST"])
def steam_form_result():
    text = request.form["text"]
    steam_games_pararmeters = {"format": "json", "steamid": text, "include_appinfo": 1, "key": key}
    steam_games_response = requests.get("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/", params=steam_games_pararmeters)
    steam_userinfo_parameters = {"format": "json", "steamids": text, "key": key}
    steam_userinfo_response = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/", params=steam_userinfo_parameters)
    try:
        steam_game_data = steam_games_response.json()
        steam_userinfo_data = steam_userinfo_response.json()
        steam_userinfo_name = steam_userinfo_data["response"]["players"][0]["personaname"]
        steam_games = []
        total_time_played = 0
        for i in range(steam_game_data["response"]["game_count"]):
            steam_game_name = steam_game_data["response"]["games"][i]["name"]
            steam_game_time = steam_game_data["response"]["games"][i]["playtime_forever"]
            if steam_game_time >= 60:
                total_time_played = total_time_played + steam_game_time
                steam_game_time = steam_game_time / 60
                steam_games.append(steam_game_name + " - " + str(round(steam_game_time, 2)) + " Hours")
            elif steam_game_time < 1:
                total_time_played = total_time_played + steam_game_time
                steam_games.append(steam_game_name + " - Never Played")
            else:
                total_time_played = total_time_played + steam_game_time
                steam_games.append(steam_game_name + " - " + str(steam_game_time) + " Minutes")
    except KeyError:
        return "Key Error Encountered: Please try again ( Possibly means account is on private / Games are hidden)"
    except IndexError:
        return "No results found"
    except ValueError:
        return "Invalid Steam64 ID"
    return render_template("steam_data.html",
                            games = steam_games,
                            total_time_played = "Total Time Played - " + str(round((total_time_played / 60), 2)) + " Hours",
                            user = "Username - " + steam_userinfo_name)
