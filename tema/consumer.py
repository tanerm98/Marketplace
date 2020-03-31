"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2020
"""

from threading import Thread
import time


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
        self.name = kwargs['name']

    def run(self):
        for cart in self.carts:
            cart_id = self.marketplace.new_cart()

            for action in cart:
                action_type = action["type"]
                product = action["product"]
                quantity = action["quantity"]

                for piece in range(quantity):
                    if action_type == "add":
                        succesful_action = self.marketplace.add_to_cart(cart_id, product)

                        while succesful_action is False:
                            time.sleep(self.retry_wait_time)
                            succesful_action = self.marketplace.add_to_cart(cart_id, product)

                    elif action_type == "remove":
                        self.marketplace.remove_from_cart(cart_id, product)

            bought_products = self.marketplace.place_order(cart_id)
            for bought_product in bought_products:
                print("{} bought {}".format(self.name, bought_product))