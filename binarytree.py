from abc import ABCMeta, abstractmethod


class Node(object):
    """
    BaseNode will be the abstract class which will make up the tree. The basic elements of a node are
    root, left branch, and right branch.

    Is it appropriate to extend object?


    """

    def __init__(self, data, left, right):
        self.data = data
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return self.data


class Tree:

    def __init__(self, root: Node = None, left_tree: Node = None, right_tree: Node = None):

        self.root = root

        if left_tree:
            self.root.left = left_tree
        if right_tree:
            self.root.right = right_tree

    def get_left(self):
        if self.root and self.root.left:
            return Tree(self.root.left)
        else:
            return None

    def get_right(self):
        if self.root and self.root.right:
            return Tree(self.root.right)
        else:
            return None

    def is_leaf(self):
        return self.root.left and self.root.right

    def pre_order_traverse(self, node: Node, depth=1):
        """

        :param node: starting node
        :param depth: nodes to traverse. 1 if not specified
        :return: string representation of added elements

        TODO: add print object argument
        """
        output = ''

        for i in range(depth):
            if not node:
                output += f'empty\n'
            else:
                output += f'{node.__str__()}'
                self.pre_order_traverse(self.root.left, depth + 1)
                self.pre_order_traverse(self.root.right, depth + 1)

    def post_order_traverse(self):
        pass

    def in_order_traverse(self):
        pass

    def __str__(self):
        return self.root


class BaseTreeSearch:
    """
    Abstract class which all Tree Searches are based?

    Representation of interface in typed-OO languages
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def add(self, item):
        pass

    @abstractmethod
    def contains(self, target):
        pass

    @abstractmethod
    def find(self, target):
        pass

    @abstractmethod
    def delete(self, target):
        pass

    @abstractmethod
    def remove(self, target):
        pass


class BaseCompare(AttributeError, TypeError):
    """
    BaseCompare class
    """
    __metaclass__ = ABCMeta

    def compare_to(self, o) -> int:
        """

        :param o: object to be compared to
        :return: negative integer for less than,
                 zero for equal
                 positive integer for greater than
        """
        pass


class BinarySearchTree(Tree, BaseTreeSearch, BaseCompare):
    _add_return = None
    _delete_return = None

    def add(self, item):
        """
        Object item needs to extend BaseCompare
        :param item: Object to insert
        :return: True if inserted. False if the object is contained in the tree
        """
        self.root = self._private_add(self.root, item)
        return self._add_return

    def _private_add(self, local_root, item):
        """

        :param local_root: local root of the subtree
        :param item: object to insert
        :return: local root that was inserted
        """
        if not local_root:
            self._add_return = True
            return Node(item)
        elif item.compare_to(local_root.data) == 0:
            self._add_return = False
            return local_root
        elif item.compare_to(local_root.data) < 0:
            local_root.left = self._private_add(local_root.left, item)
            return local_root
        else:
            local_root.right = self._private_add(local_root.right, item)
            return local_root

    def contains(self, target):
        self.root = self._private_add(self.root, target)
        return True if self.root else False

    def find(self, target: BaseCompare):
        """
        :param target: Comparable object to find
        :return: Node object ?
        """
        return self._private_find(self.root, target)

    def _private_find(self, local_root: Node, target: BaseCompare):
        """

        :param local_root: local subtree root
        :param target: Object to find
        :return: Object or null
        """
        if not local_root:
            return None
        else:
            compare_result = target.compare_to(self.root.data)
            if compare_result == 0:
                return local_root.data
            elif compare_result < 0:
                self._private_find(local_root.left, target)
            else:
                self._private_find(local_root.right, target)

    def delete(self, target):
        """

        :param target:
        :return:
        """
        self.root = self._private_delete(self.root, target)
        return self._delete_return

    def _private_delete(self, local_root, target):
        """

        :param local_root:
        :param target:
        :return:
        """
        if not local_root:
            self._delete_return = None
            return local_root

        compare_result = target.compare_to(local_root.data)
        if compare_result < 0:
            local_root.left = self._private_delete(local_root.left, target)
            return local_root
        elif compare_result > 0:
            local_root.right = self._private_delete(local_root.right, target)
            return local_root
        else:
            # item is at the root node
            self._delete_return = local_root.data
            if not local_root.left:
                # no left child return right child
                return local_root.right
            elif not local_root.right:
                # no right child return left child
                return local_root.left
            else:
                # node has left and right child
                # replace with inorder predecessor
                if not local_root.left.right:
                    # check left child node to see if there is no right node
                    # if there is not replace the data
                    local_root.data = local_root.left.data
                    # update the reference
                    local_root.left = local_root.left.left
                    return local_root
                else:
                    # search for the in order predecessor and replace with deleted nodes data
                    local_root.data = self._find_largest_child(local_root.left)
                    return local_root

    def _find_largest_child(self, parent_node: Node):

        if not parent_node.right.right:
            return_node = parent_node.right.data
            parent_node.right = parent_node.right.left
            return return_node
        else:
            return self._find_largest_child(parent_node.right)

    def remove(self, target):
        self.root = self._private_delete(self.root, target)
        return True if self.root else False

