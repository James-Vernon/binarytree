from binarytree import BinaryTreeSearch, BaseNode


class IntegerNode(BaseNode):

    def compare_to(self, item) -> int:
        if self.data == item.data:
            return 0
        elif self.data < item.data:
            return -1
        else:
            return 1


class IntegerBinarySearchTree(BinaryTreeSearch):

    def add(self, data):
        item = IntegerNode(data)
        return super().add(item)

    def print_tree(self):
        for ele in self.pre_order_traverse():
            print(ele)


int_bt = IntegerBinarySearchTree()
int_bt.add(5)
int_bt.add(2)
int_bt.add(9)
int_bt.add(24)
int_bt.add(6)
int_bt.add(23)
int_bt.add(56)
int_bt.add(58)
int_bt.add(59)
int_bt.add(1)
int_bt.add(3)
int_bt.add(-4)
int_bt.add(0)

int_bt.print_tree()
