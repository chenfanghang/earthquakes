import json
from datetime import date
from itertools import groupby

import matplotlib.pyplot as plt
import requests


def get_data():
    """Retrieve the data we will be working with."""
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"}
    )

    text = response.text
    return json.loads(text)


def write_data_to_file(data, filename='earthquakes.json'):
    """Write the earthquake data to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(data, f)


def get_year(earthquake):
    """Extract the year in which an earthquake happened."""
    timestamp = earthquake['properties']['time']
    # The time is given in a strange-looking but commonly-used format.
    # To understand it, we can look at the documentation of the source data:
    # https://earthquake.usgs.gov/data/comcat/index.php#time
    # Fortunately, Python provides a way of interpreting this timestamp:
    # (Question for discussion: Why do we divide by 1000?)
    year = date.fromtimestamp(timestamp / 1000).year
    return year


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake['properties']['mag']


# This is function you may want to create to break down the computations,
# although it is not necessary. You may also change it to something different.
def get_magnitudes_per_year(earthquakes):
    """Retrieve the magnitudes of all the earthquakes in a given year.

    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """
    sorted_data = sorted(earthquakes, key=get_year)
    result = {}
    for year, group_iterator in groupby(sorted_data, key=get_year):
        magnitudes = [item['properties']['mag'] for item in group_iterator]
        result[year] = magnitudes
    print(result)
    return result


def plot_average_magnitude_per_year(earthquakes):
    """Plot the average and maximum magnitude of earthquakes per year."""
    if not earthquakes:
        print("No earthquake data available for plotting")
        return

    years = list(earthquakes.keys())
    avg_mags = [sum(earthquakes[year]) / len(earthquakes[year]) for year in years]
    max_mags = [max(earthquakes[year]) for year in years]

    plt.figure(figsize=(10, 6))
    plt.plot(years, avg_mags, marker='o', color='red', label='Average Magnitude', linewidth=2)
    plt.plot(years, max_mags, marker='s', linestyle='--', color='darkorange', label='Maximum Magnitude', linewidth=2)

    plt.title('Earthquake Magnitude Trends by Year', fontsize=16)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Magnitude', fontsize=12)
    plt.xticks(years)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


def plot_number_per_year(earthquakes):
    if not earthquakes:
        print("No earthquake data available for plotting")
        return
    years = list(earthquakes.keys())
    counts = [len(earthquakes[year]) for year in years]

    plt.figure(figsize=(10, 6))
    plt.bar(years, counts, color='skyblue')

    plt.title('Number of Earthquake Events Per Year', fontsize=16)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Number of Events', fontsize=12)
    plt.xticks(years)
    plt.grid(axis='y', linestyle='--')
    plt.show()


if __name__ == '__main__':
    # Get the data we will work with
    quakes = get_data()['features']
    # write_data_to_file(quakes)
    magnitudes = get_magnitudes_per_year(quakes)
    # # Plot the results - this is not perfect since the x axis is shown as real
    # # numbers rather than integers, which is what we would prefer!
    plot_number_per_year(magnitudes)
    plt.clf()  # This clears the figure, so that we don't overlay the two plots
    plot_average_magnitude_per_year(magnitudes)
