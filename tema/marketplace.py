"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2020
"""

import threading
import uuid

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer

        self.producers = {}
        self.consumers = {}

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        producer_id = str(threading.current_thread().name)
        if producer_id not in self.producers:
            self.producers[producer_id] = []

        return producer_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        try:
            if len(self.producers[producer_id]) < self.queue_size_per_producer:
                self.producers[producer_id].append(product)
                return True

            return False

        except KeyError:
            print("ERROR finding producer {} when publishing product!".format(producer_id))
            return False

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        consumer_id = str(threading.current_thread().name)
        cart_id = str(consumer_id) + "_" + str(uuid.uuid4())

        if consumer_id not in self.consumers:
            self.consumers[consumer_id] = {}
        self.consumers[consumer_id][cart_id] = []

        return cart_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        consumer_id = str(threading.current_thread().name)

        try:
            for producer in self.producers:
                if product in self.producers[producer]:
                    self.producers[producer].remove(product)
                    self.consumers[consumer_id][cart_id].append((producer, product))
                    return True

            return False

        except KeyError:
            print("ERROR finding cart {} of consumer {} when adding to cart!"
                  .format(cart_id, consumer_id))
            return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        consumer_id = str(threading.current_thread().name)

        try:
            for element in self.consumers[consumer_id][cart_id]:
                (producer, product_to_remove) = element
                if product_to_remove == product:
                    self.consumers[consumer_id][cart_id].remove(element)
                    self.producers[producer].append(product_to_remove)
                    return

        except KeyError:
            print("ERROR finding cart {} of consumer {} when removing from cart!"
                  .format(cart_id, consumer_id))
            return

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        consumer_id = str(threading.current_thread().name)

        try:
            order = []
            for element in self.consumers[consumer_id][cart_id]:
                order.append(element[1])

            return order
        except KeyError:
            print("ERROR finding cart {} of consumer {} when placing order!"
                  .format(cart_id, consumer_id))
            return []
