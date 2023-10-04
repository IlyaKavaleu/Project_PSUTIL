class Stack:

    def __init__(self):
        self.array = []

    def return_array(self):
        return self.array

    def add(self, item):
        self.array.append(item)

    def pop(self):
        return self.array.pop()

    def count(self):
        return len(self.array)

    def current_value(self):
        return self.array[self.count() - 1]

    def __iter__(self):
        self.index = self.count() - 1
        return self

    def __next__(self):
        if self.index < 0:
            raise StopIteration
        result = self.array[self.index]
        self.index -= 1
        return result


stack = Stack()
stack.add(1)
stack.add(2)
stack.add(3)
stack.add(4)
print(stack.return_array())
print(stack.pop())
print(stack.__iter__())
