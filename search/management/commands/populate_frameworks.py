import datetime
import json
import uuid

from django.conf import settings
from django.core.management import BaseCommand

from search.models import Framework, Cpv, Document, LOT, Supplier


def format_date(string_date):
    datetime_obj = datetime.datetime.strptime(string_date, "%d/%m/%Y")
    return datetime_obj.strftime("%Y-%m-%d")


class Command(BaseCommand):
    help = 'Populate database'

    def handle(self, *args, **options):
        print('Populating ...')
        with open(settings.BASE_DIR / 'search/fixture/frameworks.json', 'r') as f:
            data = json.load(f)
            for block in data:
                if framework_name := block.get('framework_name'):
                    framework = Framework.objects.create(
                        name=framework_name,
                        site_name="_".join(block.get('framework_name').split(' ')) + str(uuid.uuid4())[:10],
                        number=block.get('framework_number'),
                        lot_number=block.get('number_of_lots'),
                        value=block.get('framework_value'),
                        value_number=int(''.join(filter(str.isdigit, block.get('framework_value')))) if block.get('framework_value') else None,
                        start_date=format_date(block.get('start_date')),
                        end_date=format_date(block.get('end_date')),
                        service_type=block.get('service_type'),
                        description=block.get('description') if isinstance(block.get('description'), str) else "\n".join(block.get('description', [])),
                        logo=block.get('logo'),
                        industry_or_category=block.get('category_name'),
                        sub_category=block.get('subcategory'),
                    )

                    for cpv in block.get('cpv_code_details', []):
                        other_cpv_codes = cpv.get('other_cpv_codes')
                        if other_cpv_codes is None:
                            other_cpv_codes = []

                        for code in other_cpv_codes:
                            Cpv.objects.create(
                                code=code,
                                framework=framework,
                            )

                    for doc_name, doc_link in block.get('documents', {}).items():
                        Document.objects.create(
                            framework=framework,
                            name=doc_name,
                            link=doc_link
                        )

                    if isinstance(block.get('lot_name'), str) and isinstance(block.get('lot_description'), str):
                        LOT.objects.create(
                            name=block.get('lot_name')[:250],
                            description=block.get('lot_description'),
                            framework=framework
                        )
                    elif isinstance(block.get('lot_name'), list) and isinstance(block.get('lot_description'), list):
                        length = min(len(block.get('lot_name')), len(block.get('lot_description')))
                        for index in range(length):
                            LOT.objects.create(
                                name=block.get('lot_name')[index],
                                description=block.get('lot_description')[index],
                                framework=framework
                            )

                    for supplier_name, supplier_link in block.get('suppliers', {}).items():
                        Supplier.objects.create(
                            framework=framework,
                            name=supplier_name,
                            link=supplier_link
                        )

            print('Done')
