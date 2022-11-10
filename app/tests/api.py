from rest_framework.reverse import reverse

import pytest


def test_rates_get(api_client_auth):

    response = api_client_auth.get(reverse('api-v1:rates'))
    assert response.status_code == 200
    assert response.json()['count']
    assert response.json()['results']


def test_rates_post_empty(api_client_auth):

    response = api_client_auth.post(reverse('api-v1:rates'), data={})
    assert response.status_code == 400
    assert response.json() == {
        'buy': ['This field is required.'],
        'sale': ['This field is required.'],
        'currency_type': ['This field is required.'],
        'base_currency_type': ['This field is required.'],

    }


def test_contactus_get(api_client_auth):

    response = api_client_auth.get(reverse('api-v1:contact-list'))
    assert response.status_code == 200


def test_contactus_post_empty(api_client_auth):

    response = api_client_auth.post(reverse('api-v1:contact-list'), data={})
    assert response.status_code == 400
    assert response.json() == {
        'email_from': ['This field is required.'],
        'email_to': ['This field is required.'],
        'subject': ['This field is required.'],
        'message': ['This field is required.'],
    }


def test_contactus_post_valid(api_client_auth, mailoutbox):
    data = {
        'email_from': 'example@mail.com',
        'email_to': 'example@mail.com',
        'subject': 'subject example',
        'message': 'Body Example',
    }

    response = api_client_auth.post(reverse('api-v1:contact-list'), data=data)
    assert response.status_code == 200

    assert len(mailoutbox) == 1
    assert mailoutbox[0].subject == 'ContactUs From Currency Project'


@pytest.mark.parametrize('email_from', ('examplemail.com', "17638174.dhfbh", "GdjdjJKd"))
def test_contactus_post_invalid_email(api_client_auth, email_from):
    data = {
        'email_from': email_from,
        'email_to': 'example@mail.com',
        'subject': 'subject example',
        'message': 'Body Example',
    }

    response = api_client_auth.post(reverse('api-v1:contact-list'), data=data)
    assert response.status_code == 400
    assert response.json() == {'email_from': ['Enter a valid email address.']}
