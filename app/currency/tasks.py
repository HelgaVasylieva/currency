import requests

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


from currency.utils import to_decimal
from currency import model_choices as mch
from currency import consts


@shared_task(autoretry_for=(OSError,), retry_kwargs={'max_retries': 5})
def send_contact_us_email(subject, from_email):
    email_subject = 'ContactUs From Currency Project'
    body = f'''
    Subject From Client: {subject}
    Email: {from_email}
    Wants to contact
    '''

    from time import sleep
    sleep(3)
    # print('send_contact_us_email')
    # raise OSError
    send_mail(
        email_subject,
        body,
        settings.EMAIL_HOST_USER,
        [settings.EMAIL_HOST_USER],
        fail_silently=False,
    )


@shared_task
def parse_privatbank():
    from currency.models import Rate, Source
    url = 'https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11'

    source = Source.objects.get_or_create(code_name=consts.CODE_NAME_PRIVATBANK, defaults={'source_url': url})[0]

    response = requests.get(source.source_url)
    response.raise_for_status()

    response_data = response.json()

    currency_type_mapper = {
        'UAH': mch.CURRENCY_TYPE_UAH,
        'USD': mch.CURRENCY_TYPE_USD,
        'EUR': mch.CURRENCY_TYPE_EUR,
        'BTC': mch.CURRENCY_TYPE_BTC,
    }

    for rate_data in response_data:
        currency_type = rate_data['ccy']
        base_currency_type = rate_data['base_ccy']

        if currency_type not in currency_type_mapper or \
                base_currency_type not in currency_type_mapper:
            continue

        currency_type = currency_type_mapper[rate_data['ccy']]
        base_currency_type = currency_type_mapper[rate_data['base_ccy']]

        buy = to_decimal(rate_data['buy'])
        sale = to_decimal(rate_data['sale'])

        try:
            latest_rate = Rate.objects.filter(
                base_currency_type=base_currency_type,
                currency_type=currency_type,
                source=source,
            ).latest('created')
        except Rate.DoesNotExist:
            latest_rate = None

        if latest_rate is None or \
                latest_rate.sale != sale or \
                latest_rate.buy != buy:
            Rate.objects.create(
                base_currency_type=base_currency_type,
                currency_type=currency_type,
                buy=buy,
                sale=sale,
                source=source,
            )


@shared_task
def parse_monobank():

    from currency.models import Rate, Source

    url_1 = 'https://api.monobank.ua/bank/currency'

    source = Source.objects.get_or_create(code_name=consts.CODE_NAME_MONOBANK, defaults={'source_url': url_1})[0]

    response = requests.get(source.source_url)

    response_data = response.json()

    currency_type_mapper = {
        980: mch.CURRENCY_TYPE_UAH,
        840: mch.CURRENCY_TYPE_USD,
        978: mch.CURRENCY_TYPE_EUR,
    }

    for rate_data in response_data:
        currency_type = rate_data["currencyCodeA"]
        base_currency_type = rate_data["currencyCodeB"]

        if currency_type not in currency_type_mapper or \
                base_currency_type not in currency_type_mapper:
            continue
        if "rateBuy" not in rate_data or "rateSell" not in rate_data:
            continue

        currency_type = currency_type_mapper[rate_data["currencyCodeA"]]
        base_currency_type = currency_type_mapper[rate_data["currencyCodeB"]]

        buy = to_decimal(rate_data["rateBuy"])
        sale = to_decimal(rate_data["rateSell"])

        try:
            latest_rate = Rate.objects.filter(
                base_currency_type=base_currency_type,
                currency_type=currency_type,
                source=source,
            ).latest('created')
        except Rate.DoesNotExist:
            latest_rate = None

        if latest_rate is None or \
                latest_rate.sale != sale or \
                latest_rate.buy != buy:
            Rate.objects.create(
                base_currency_type=base_currency_type,
                currency_type=currency_type,
                buy=buy,
                sale=sale,
                source=source,
            )


@shared_task
def parse_vkurse():

    from currency.models import Rate, Source

    url_2 = 'https://vkurse.dp.ua/course.json'

    source = Source.objects.get_or_create(code_name=consts.CODE_NAME_VKURSE, defaults={'source_url': url_2})[0]

    response = requests.get(source.source_url)
    response.raise_for_status()

    currency_type_mapper = {
        'UAH': mch.CURRENCY_TYPE_UAH,
        'Dollar': mch.CURRENCY_TYPE_USD,
        'Euro': mch.CURRENCY_TYPE_EUR,
    }

    response_data = response.json()
    for rate_data in response_data.items():

        currency_type = rate_data[0]
        base_currency_type = 'UAH'

        if currency_type not in currency_type_mapper or \
                base_currency_type not in currency_type_mapper:
            continue

        buy = to_decimal(rate_data[1]['buy'])
        sale = to_decimal(rate_data[1]['sale'])
        currency_type = currency_type_mapper[rate_data[0]]
        base_currency_type = currency_type_mapper['UAH']

        try:
            latest_rate = Rate.objects.filter(
                base_currency_type=base_currency_type,
                currency_type=currency_type,
                source=source,
            ).latest('created')
        except Rate.DoesNotExist:
            latest_rate = None

        if latest_rate is None or \
                latest_rate.sale != sale or \
                latest_rate.buy != buy:
            Rate.objects.create(
                base_currency_type=base_currency_type,
                currency_type=currency_type,
                buy=buy,
                sale=sale,
                source=source,
            )


@shared_task
def parse_tascombank():

    from currency.models import Rate, Source

    url_3 = 'https://tascombank.ua/api/currencies'

    source = Source.objects.get_or_create(code_name=consts.CODE_NAME_TASCOMBANK, defaults={'source_url': url_3})[0]

    response = requests.get(source.source_url)
    response.raise_for_status()

    currency_type_mapper = {
        'UAH': mch.CURRENCY_TYPE_UAH,
        'USD': mch.CURRENCY_TYPE_USD,
        'EUR': mch.CURRENCY_TYPE_EUR,
    }

    response_data = response.json()
    response_data_list = response_data[0]

    for rate_data in response_data_list:

        currency_type = rate_data['short_name']
        base_currency_type = 'UAH'
        kurs_type_description = rate_data['kurs_type_description']

        if currency_type not in currency_type_mapper or \
                base_currency_type not in currency_type_mapper or \
                'kurs_buy' not in rate_data or \
                'kurs_sale' not in rate_data or \
                kurs_type_description != 'Обменный':
            continue

        buy = to_decimal(rate_data['kurs_buy'])
        sale = to_decimal(rate_data['kurs_sale'])
        currency_type = currency_type_mapper[rate_data['short_name']]
        base_currency_type = currency_type_mapper['UAH']

        try:
            latest_rate = Rate.objects.filter(
                base_currency_type=base_currency_type,
                currency_type=currency_type,
                source=source,
            ).latest('created')
        except Rate.DoesNotExist:
            latest_rate = None

        if latest_rate is None or \
                latest_rate.sale != sale or \
                latest_rate.buy != buy:
            Rate.objects.create(
                base_currency_type=base_currency_type,
                currency_type=currency_type,
                buy=buy,
                sale=sale,
                source=source,
            )


@shared_task
def parse_otpbank():
    from currency.models import Rate, Source

    url_4 = 'https://www.otpbank.com.ua/local/components/otp/utils.exchange_rate_arc/exchange_rate_by_date.php?' \
            'curr_date=18.09.2022&ib_code=otp_bank_currency_rates'

    source = Source.objects.get_or_create(code_name=consts.CODE_NAME_OTPBANK, defaults={'source_url': url_4})[0]

    response = requests.get(source.source_url)
    response.raise_for_status()

    currency_type_mapper = {
        'UAH': mch.CURRENCY_TYPE_UAH,
        'USD': mch.CURRENCY_TYPE_USD,
        'EUR': mch.CURRENCY_TYPE_EUR,
    }

    response_data = response.json()
    response_data_list = response_data['items']

    for rate_data in response_data_list:

        currency_type = rate_data['NAME']
        base_currency_type = 'UAH'

        if currency_type not in currency_type_mapper or \
                base_currency_type not in currency_type_mapper:
            continue

        buy = to_decimal(rate_data['BUY'])
        sale = to_decimal(rate_data['SELL'])
        currency_type = currency_type_mapper[rate_data['NAME']]
        base_currency_type = currency_type_mapper['UAH']

        try:
            latest_rate = Rate.objects.filter(
                base_currency_type=base_currency_type,
                currency_type=currency_type,
                source=source,
            ).latest('created')
        except Rate.DoesNotExist:
            latest_rate = None

        if latest_rate is None or \
                latest_rate.sale != sale or \
                latest_rate.buy != buy:
            Rate.objects.create(
                base_currency_type=base_currency_type,
                currency_type=currency_type,
                buy=buy,
                sale=sale,
                source=source,
            )


@shared_task
def parse_nbu():
    from currency.models import Rate, Source

    url_5 = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json'

    source = Source.objects.get_or_create(code_name=consts.CODE_NAME_NBU, defaults={'source_url': url_5})[0]

    response = requests.get(source.source_url)
    response.raise_for_status()

    currency_type_mapper = {
        'UAH': mch.CURRENCY_TYPE_UAH,
        'USD': mch.CURRENCY_TYPE_USD,
        'EUR': mch.CURRENCY_TYPE_EUR,
    }

    response_data = response.json()

    for rate_data in response_data:

        currency_type = rate_data['cc']
        base_currency_type = 'UAH'

        if currency_type not in currency_type_mapper or \
                base_currency_type not in currency_type_mapper:
            continue

        buy = to_decimal(rate_data['rate'])
        sale = to_decimal(rate_data['rate'])
        currency_type = currency_type_mapper[rate_data['cc']]
        base_currency_type = currency_type_mapper['UAH']

        try:
            latest_rate = Rate.objects.filter(
                base_currency_type=base_currency_type,
                currency_type=currency_type,
                source=source,
            ).latest('created')
        except Rate.DoesNotExist:
            latest_rate = None

        if latest_rate is None or \
                latest_rate.sale != sale or \
                latest_rate.buy != buy:
            Rate.objects.create(
                base_currency_type=base_currency_type,
                currency_type=currency_type,
                buy=buy,
                sale=sale,
                source=source,
            )
