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

    def getHighest_Value(self):
        try:
            max = 0
            for i in range(len(self.queue)):
                if self.queue[i].priority > self.queue[max].priority:
                    max = i
            item = self.queue[max]
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
        self.children = []
        self.value = value
        self.priority = priority

    def __lt__(self,other):
        return self.priority<other.priority

    def __le__(self,other):
        return self.priority<=other.priority

    def __gt__(self,other):
        return self.priority > other.priority

    def __ge__(self,other):
        return self.priority>=other.priority

    def __eq__(self,other):
        return self.priority == other.priority

    def __ne__(self,other):
        return not(self.__eq__(self,other))

    def add_child(self, obj):
        #self.children.insert(obj)
        self.children.append(obj)
        obj.parent = self

    def getChildren(self):
        self.children.sort(reverse=True)
        #return self.children.getAll()
        return self.children

    '''
    def popHighestValue(self):
        return self.children.delete()

    def getHighestValue(self):
        return self.children.getHighest_Value()

    '''


#Simple example usage of the data structure

tom = Node("DD",1)
tom.add_child(Node("a",0.3))
tom.add_child (Node("b", 0.6))

tom.getChildren()[0].add_child(Node("c",0.3))
tom.getChildren()[1].add_child(Node("d",0.5))
print("testg")
print()
print("test")
#print(tom.popHighestValue().value)
#print(tom.getHighestValue().value)

bigger_tom = Node("A",0.9)
smaller_tom = Node("B",0.7)
medium_tom = Node("C",0.8)
tom_list = [bigger_tom,smaller_tom,medium_tom]

for i in tom_list:
    print(i.priority)

tom_list.sort(reverse=True)
print("!!!!")
for i in tom_list:
    print(i.priority)

print(tom_list)

print(bigger_tom>smaller_tom)


#This gets all the children of the current
def getAll(currentNode):
    print(currentNode.value)
    children_to_process = []
    if(currentNode.getChildren != []):
        for sibling in currentNode.getChildren():
            sibling.priority = 1
            getAll(sibling)

passwords = []
def getPasswords(node):
    if(node.getChildren() != []):
        for sibling in node.getChildren():
            getPasswords(sibling)
    else:
        passwords.append(node.value)

print("sdasdas")
#getPasswords(tom)
print(passwords)