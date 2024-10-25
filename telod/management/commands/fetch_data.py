from django.core.management.base import BaseCommand
from django.db import transaction
import requests
from bs4 import BeautifulSoup

from telod.models import Medicine, MedicineName


class Command(BaseCommand):
    help = "Fetches list of medicines and saves it to the database"

    def handle(self, *args, **kwargs):
        MedicineName.objects.all().delete()
        Medicine.objects.all().delete()

        url = "https://encyclopatia.ru/wiki/%D0%A0%D0%B0%D1%81%D1%81%D1%82%D1%80%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9_%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%BF%D1%80%D0%B5%D0%BF%D0%B0%D1%80%D0%B0%D1%82%D0%BE%D0%B2"
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text

            soup = BeautifulSoup(html_content, "lxml")
            list_items = soup.find_all("li")

            lock = True

            for item in list_items:
                full_text = item.get_text(separator=" ", strip=True)

                # Find the first occurrence of either '—' or ':' and split the text accordingly
                if "—" in full_text or ":" in full_text:
                    # Find the index of the first occurrence of either
                    divider_pos = min(
                        full_text.find("—") if "—" in full_text else len(full_text),
                        full_text.find(":") if ":" in full_text else len(full_text),
                    )

                    name = full_text[:divider_pos].strip()
                    description = full_text[divider_pos + 1 :].strip()
                else:
                    name = full_text
                    description = ""

                if not name_is_valid(name):
                    continue
                lock = change_lock(name, lock)
                if lock:
                    continue

                with transaction.atomic():
                    medicine = Medicine.objects.create(
                        main_name=name, description=description
                    )
                    MedicineName.objects.create(name=name, medicine=medicine)

            self.stdout.write(
                self.style.SUCCESS("Successfully parsed and populated data")
            )

        else:
            self.stderr.write("Failed to fetch data")


def name_is_valid(name):
    if not name:
        return False
    if not name[0].isalpha() or not name[0].isupper():
        return False

    return True


def change_lock(name, lock):
    chl = False

    if name == "Агри":
        chl = True

    if name == "Журнал добавления/удаления препаратов ;":
        chl = True

    if chl:
        return not lock

    return lock
