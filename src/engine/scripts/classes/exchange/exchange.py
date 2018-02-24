""" Container for Exchange
"""
from abc import ABC, abstractmethod


class Exchange(ABC):

    def __init__(self):
        self._items = {}
        self._fuel = None

    @abstractmethod
    def __str__(self):
        raise NotImplementedError

    def set_item(self, item, amount=None, cost_per_item=None):
        self._items[item.get_item_type()] = {
            'item': item,
            'amount': amount,
            'cost_per_item': cost_per_item
        }

    def remove_item(self, item):
        self._items.pop(item.get_item_type(), None)

    def set_fuel(self, amount=None, cost_per_fuel=None):
        self._fuel = {
            'amount': amount,
            'cost_per_fuel': cost_per_fuel
        }

    def remove_fuel(self):
        self._fuel = None

    def get_exchange_details(self, amount_phrase='amount'):
        if not self._items and not self._fuel:
            return 'NA'
        details = []
        for item_type, item_details in self._items.items():
            if item_details['cost_per_item'] is not None:
                detail = '{0} CR per {1}'.format(item_details['cost_per_item'], item_type, item_details['amount'])
            else:
                detail = '{0}, amount: {1}'.format(item_type, item_details['amount'])
            if item_details['amount'] is not None:
                detail += ', {0}: {1}'.format(amount_phrase, item_details['amount'])
            details.append(detail)
        return details.join('\n')
