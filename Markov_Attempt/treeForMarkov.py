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
    def insert(self, data):
        self.queue.append(data)

    def getAll(self):
        return self.queue

    # for popping an element based on Priority
    def delete(self):
        try:
            max = 0
            for i in range(len(self.queue)):
                if self.queue[i].priority > self.queue[max].priority:
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
    def __init__(self, value, priority):
        self.parent = None
        self.children = PriorityQueue()
        self.value = value
        self.priority = priority


    def add_child(self, obj):
        self.children.insert(obj)
        obj.parent = self

    def popHighestValue(self):
        return self.children.delete()

    def getChildren(self):
        return self.children.getAll()

#Simple example usage of the data structure

tom = Node("DD",1)
tom.add_child(Node("a",0.3))
tom.add_child (Node("b", 0.6))

tom.getChildren()[0].add_child(Node("c",0.2))
tom.getChildren()[1].add_child(Node("d",0.1))
#print(tom.popHighestValue().value)





def getAll(currentNode):
    print(currentNode.value)
    children_to_process = []
    if(currentNode.getChildren != []):
        for sibling in currentNode.getChildren():
            sibling.priority = 1
            getAll(sibling)

