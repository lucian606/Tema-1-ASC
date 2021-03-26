"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Lock

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
        self.producer_id = 0 # the id of the next producer
        self.cart_id = 0 # the id of the next cart
        self.queues = [] # the list of producer queues
        self.carts = [] # the list of carts
        self.mutex = Lock() # mutex used for operations with non-atomic values
        self.products_dict = {} # when I publish a product I store its producer

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        self.mutex.acquire() # preventing the race condition on producer id
        producer_id = self.producer_id
        self.producer_id += 1 # prepare a new id for the next user
        self.queues.append([]) # add an empty queue for the new producer
        self.mutex.release()
        return str(producer_id)

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        producer_index = int(producer_id) # casting the id to int for index
        if len(self.queues[producer_index]) == self.queue_size_per_producer: # check if queue full
            return False
        self.queues[producer_index].append(product) # add the product in his producer queue
        self.products_dict[product] = producer_index # store the id of the product
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        self.mutex.acquire()
        cart_id = self.cart_id
        self.cart_id += 1
        self.mutex.release()
        self.carts.append([]) # add an empty list for the new cart
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
        # Checking if the product is in the market
        is_product = False
        for queue in self.queues:
            if product in queue:
                is_product = True
                queue.remove(product) # if product exist take it out of the queue
                break
        if not is_product:
            return False
        self.carts[cart_id].append(product)
        return True

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        if product not in self.carts[cart_id]:
            return False
        producer_idx = self.products_dict[product] # getting the idx of the product's queue
        if len(self.queues[producer_idx]) == self.queue_size_per_producer: # check if queue is full
            return False
        self.carts[cart_id].remove(product) # remove from cart
        self.queues[producer_idx].append(product) # put back in queue
        return True

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        cart_content = self.carts[cart_id] # store the cart's content
        self.carts[cart_id] = [] # empty the cart
        return cart_content # return the contents of the cart
