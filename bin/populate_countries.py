import sys
import csv

from trips.models import Country

def populate_countries(csv_file_path):
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            Country.objects.create(
                name=row['country'],
                alpha2=row['alpha2'],
                alpha3=row['alpha3'],
                numeric=row.get('numeric', '')
            )
        print('Successfully loaded countries')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python populate_countries.py path/to/countries.csv")
        sys.exit(1)
    
    csv_file_path = sys.argv[1]
    populate_countries(csv_file_path)
