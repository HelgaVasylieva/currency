from rest_framework.throttling import AnonRateThrottle


class AnonCurrencyModelThrottle(AnonRateThrottle):
    scope = 'currency'
