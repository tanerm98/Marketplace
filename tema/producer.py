"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2020
"""

from threading import Thread, Lock
import time
myLock = Lock()

class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)

        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        self.name = kwargs['name']

        self.id = None

    def run(self):
        self.id = self.marketplace.register_producer()
        while True:
            for product_type in self.products:
                product = product_type[0]
                quantity = product_type[1]
                producing_time = product_type[2]

                for piece in range(quantity):
                    time.sleep(producing_time)
                    succesfuly_published = self.marketplace.publish(producer_id=self.id, product=product)

                    while succesfuly_published is False:
                        time.sleep(self.republish_wait_time)
                        succesfuly_published = self.marketplace.publish(producer_id=self.id, product=product)
