# from django.core.management.base import BaseCommand
# from staffPortal.models import Country, State, City
# import csv

# class Command(BaseCommand):
#     help = 'Import countries, states, and cities from CSV'

#     def handle(self, *args, **kwargs):
#             import csv
#             # Import countries
#             with open('staffPortal/dataset/countries.csv' , encoding='utf-8', errors='ignore') as f:
#                 reader = csv.DictReader(f)
#                 for row in reader:
#                     Country.objects.create(name=row['name'])

#             # Import states
#             with open('staffPortal/dataset/states.csv' , encoding='utf-8', errors='ignore') as f:
#                 reader = csv.DictReader(f)
#                 for row in reader:
#                     country = Country.objects.get(id=row['country_id'])
#                     State.objects.create(name=row['name'], country=country)

#             # Import cities
#             with open('staffPortal/dataset/cities.csv' , encoding='utf-8', errors='ignore') as f:
#                 reader = csv.DictReader(f)
#                 for row in reader:
#                     state = State.objects.get(id=row['state_id'])
#                     City.objects.create(name=row['name'], state=state)

#         self.stdout.write(self.style.SUCCESS('Import finished successfully'))
