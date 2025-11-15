## Installation

**Python 3.12**

 ```bash
   git clone https://github.com/EugeneDanini/geocoder.git 
   cd geocoder
   pip install -r requirements.txt
   ```

## CSV Example

**Sample `data/prague.csv`:**
```csv
original_street_name,referenced_city_name_english,street_centre_latitude,street_centre_longitude
Londýnská,London,50.0714090,14.4352794
Pařížská,Paris,,
Varšavská,Warsaw,,
```

## Usage
```bash
python ./geocode.py Prague Czechia
```