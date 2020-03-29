from django.core.management.base import BaseCommand, CommandError
from community.models import Community

from bs4 import BeautifulSoup
import urllib.request
import re

url = "http://publichealth.lacounty.gov/media/Coronavirus/locations.htm"


class Command(BaseCommand):
    help = 'Update LA Covid-19 database'

    def handle(self, *args, **options):

        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
        city = (soup.select(
            'html > body > div#content > div.content-padding > table.table.table-striped.table-bordered.table-sm > tbody >tr > th'))
        number = (soup.select(
            'html > body > div#content > div.content-padding > table.table.table-striped.table-bordered.table-sm > tbody >tr > td'))
        num_lst = []
        city_lst = []
        res = {}
        for city, number in zip(city, number):
            city_name = city.get_text()
            num_str = number.get_text()

            # print("{}:\t{}".format(city_name, num_str))

            if not ("City of" in city_name or "Los Angeles - " in city_name or "Unincorporated - " in city_name):
                continue

            num = None
            try:
                num = int(num_str)
            except ValueError as e:
                continue

            parts = city_name.split(" - ")
            if len(parts) > 1:
                city_name = parts[1]

            c, created = Community.objects.get_or_create(
                name=city_name, defaults={"cases": num})
            if not created:
                c.cases = num
                c.save()

            print("{}:\t{}".format(city_name, num))
