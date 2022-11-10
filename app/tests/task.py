from unittest.mock import MagicMock

from currency.models import Rate
from currency.tasks import parse_privatbank, parse_vkurse, parse_monobank


def test_parse_privatbank(mocker):
    response_json_privat = [
        {"ccy": "USD", "base_ccy": "UAH", "buy": "411.00000", "sale": "411.50000"},
        {"ccy": "EUR", "base_ccy": "UAH", "buy": "39.90000", "sale": "40.90000"},
        {"ccy": "BTC", "base_ccy": "USD", "buy": "17668.2920", "sale": "19528.1122"},
    ]

    initial_rate_count = Rate.objects.count()
    patch = mocker.patch('requests.get', return_value=MagicMock(json=lambda: response_json_privat), )
    requests_get_mock = patch  # noqa: F841
    parse_privatbank()
    assert Rate.objects.count() == initial_rate_count + 3


def test_parse_monobank(mocker):
    response_json_monobank = [
        {"currencyCodeA": 840, "currencyCodeB": 980, "date": 1666818609, "rateBuy": 36.65, "rateSell": 37.4406},
        {"currencyCodeA": 978, "currencyCodeB": 980, "date": 1666857010, "rateBuy": 36.8, "rateSell": 37.9003},
        {"currencyCodeA": 978, "currencyCodeB": 840, "date": 1666848609, "rateBuy": 0.994, "rateSell": 1.01},

    ]

    initial_rate_count = Rate.objects.count()
    requests_get_mock = mocker.patch(  # noqa: F841
        'requests.get',
        return_value=MagicMock(json=lambda: response_json_monobank),
    )
    parse_monobank()
    assert Rate.objects.count() == initial_rate_count + 3


def test_parse_vkurse(mocker):
    response_json_vkurse = {
        "Dollar": {"buy": "39.70", "sale": "39.95"},
        "Euro": {"buy": "39.10", "sale": "39.50"},
        "Pln": {"buy": "7.90", "sale": "8.40"},
    }

    initial_rate_count = Rate.objects.count()
    requests_get_mock = mocker.patch(  # noqa: F841
        'requests.get',
        return_value=MagicMock(json=lambda: response_json_vkurse),
    )
    parse_vkurse()
    assert Rate.objects.count() == initial_rate_count + 2
