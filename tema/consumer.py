"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
from time import sleep

class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time

    def run(self):
        # traverse the cart of each consumer
        for cart in self.carts:
            # give it an id for the marketplace functions
            cart_id = self.marketplace.new_cart()
            # traverse the commands from each card
            for command in cart:
                command_type = command["type"]
                product = command["product"]
                quantity = command["quantity"]
                # check the command type and try it until it works
                if command_type == "add":
                    for _ in range(quantity):
                        while True:
                            added = self.marketplace.add_to_cart(cart_id, product)
                            if added:
                                break
                            sleep(self.retry_wait_time)
                elif command_type == "remove":
                    for _ in range(quantity):
                        while True:
                            removed = self.marketplace.remove_from_cart(cart_id, product)
                            if removed:
                                break
                            sleep(self.retry_wait_time)
            products_bought = self.marketplace.place_order(cart_id)
            for product in products_bought:
                print(f"{self.getName()} bought {product}")
