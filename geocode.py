#!/usr/bin/env python3

import os
import pandas as pd
import requests
import time
import argparse


def get_coordinates(street: str, where: str) -> tuple[str, str, str]:
    time.sleep(1)  # Nominatim Policy: 1 request per second

    url = f"https://nominatim.openstreetmap.org/search.php?q={street},{where}&format=jsonv2&limit=1"
    try:
        res = requests.get(url, headers={"User-Agent": "hello-world"})
        data = res.json()
        if data and len(data) > 0:
            return data[0]['name'], data[0]['lat'], data[0]['lon']
    except requests.RequestException as e:
        print(f"Error: {e} for {street}")
    return street, "", ""


def process_city_file(city_name: str, country_name: str):
    input_file = f"data/{city_name.replace(' ', '-')}.csv"
    output_file = f"out/{city_name.replace(' ', '-')}.csv"
    if not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' not found.")
        return

    where = f"+{city_name.title()},+{country_name.title()}"

    # Read the CSV file
    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Process the DataFrame and fetch coordinates
    for i, row in df.iterrows():
        street, lat, lon = get_coordinates(row.get("original_street_name"), where)
        if street:
            df.at[i, "original_street_name"] = street
        df.at[i, "street_centre_latitude"] = lat
        df.at[i, "street_centre_longitude"] = lon
        if lat and lon:
            print(f"{street}: {lat}, {lon}")
        else:
            print(f"{row.get('original_street_name')}: Not Found")

    # Save the result to the output file
    os.makedirs("out", exist_ok=True)

    # Check if the output file already exists and rename it if necessary
    if os.path.exists(output_file):
        version = 1
        base_name, extension = os.path.splitext(output_file)
        while os.path.exists(output_file):
            output_file = f"{base_name}_v{version}{extension}"
            version += 1
    df.to_csv(output_file, index=False)
    print(f"Processed file saved to: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a city CSV file.")
    parser.add_argument("city", type=str, help="The name of the city to process.")
    parser.add_argument("country", type=str, help="The name of the country to process.")
    args = parser.parse_args()
    process_city_file(args.city.lower(), args.country.lower())
