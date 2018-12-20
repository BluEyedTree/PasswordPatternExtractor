# A simple implementation of Priority Queue
# using Queue.
class PriorityQueue(object):
	def __init__(self):
		self.queue = []

	def __str__(self):
		return ' '.join([str(i) for i in self.queue])

	# for checking if the queue is empty
	def isEmpty(self):
		return len(self.queue) == []

	# for inserting an element in the queue
	def insert(self, priority, data):
		self.queue.append((priority,data))

	# for popping an element based on Priority
	def delete(self):
		try:
			max = 0
			for i in range(len(self.queue)):
				if self.queue[i] > self.queue[max]:
					max = i
			item = self.queue[max]
			del self.queue[max]
			return item
		except IndexError:
			print()
			exit()




'''
class Tree(object):
    def __init__(self):
        self.children = PriorityQueue()
        self.data = None
    def addChild(self, value):
        self.children.insert(value)
'''

class Node(object):
    def __init__(self, value):
        self.parent = None
        self.children = PriorityQueue()
        self.value = value


    def add_child(self, priority, obj):
        self.children.insert(priority,obj)
        obj.parent = self

    def popHighestValue(self):
        return self.children.delete()


tom = Node("''")
tom.add_child(0.5, Node("a"))
tom.add_child(0.7, Node("b"))
print(tom.popHighestValue())