import pandas as pd
from progressbar import progressbar
import requests


def validateCity(city):
    city = city.lower()
    if city == "jullundur":
        return "jalandar"
    else:
        return city


roadDistance = pd.read_csv("roaddistance.csv")
file = open("distances.pl", "w+")
file2 = open("heuristics.pl", "w+")

roadDistance.dropna(axis=1, how="all", inplace=True)
new_header = roadDistance.iloc[0]
roadDistance = roadDistance[1:]
roadDistance.columns = new_header
roadDistance.set_index("Distance in Kilometres", inplace=True, drop=True)

temp = roadDistance.columns.values.tolist().copy()
temp.extend(roadDistance.index)
cityList = set(temp)

actualDistance = []
heuristics = []

for city1 in progressbar(roadDistance.columns.values):
    for city2 in roadDistance.index:
        distance = roadDistance.loc[city2, city1]
        distance = 0 if distance == "-" else distance
        actualDistance.append(f"road({city1.lower()}, {city2.lower()}, {distance}).\n")
        if city1 != city2:
            actualDistance.append(
                f"road({city2.lower()}, {city1.lower()}, {distance}).\n"
            )

for city1 in cityList:
    print(f"\n{city1}")
    for city2 in progressbar(cityList):
        query = f"https://www.distance24.org/route.json?stops={validateCity(city1)}|{validateCity(city2)}"
        response = requests.get(query)
        try:
            response.raise_for_status()
            data = response.json()
            heuristics.append(
                f"heuristic({city1.lower()}, {city2.lower()}, {data['distance']}).\n"
            )
        except requests.exceptions.HTTPError as e:
            print("Error calculating heuristics. Exiting")
            exit(1)

for i in actualDistance:
    file.writelines(i)

for i in heuristics:
    file2.writelines(i)
