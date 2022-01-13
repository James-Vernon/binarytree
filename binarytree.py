from abc import ABCMeta, abstractmethod


class BaseNode:
    """
    Node will be the abstract class which will make up the tree. The basic elements of a node are
    root, left branch, and right branch.
    """
    __metaclass__ = ABCMeta

    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    def compare_to(self, item) -> int:
        """
       :param value: object to be compared to
       :return: negative integer for less than, zero for equal, positive integer for greater than
       """

    pass

    def is_leaf(self):
        if self.left or self.right:
            return False
        else:
            return True

    def __str__(self) -> str:
        return str(self.data)


class Tree:
    def __init__(self, root: BaseNode = None):
        self.root = root

    def get_node(self):
        yield self.root

    def set_left(self, node):
        self.root.left = node

    def set_right(self, node):
        self.root.right = node

    def move_left(self):
        return self.root.left

    def move_right(self):
        return self.root.right

    def set_children(self, left, right):
        self.root.left = left
        self.root.right = right

    def get_children(self):
        return self.root.left, self.root.right

    def get_left_tree(self):
        if self.root and self.root.left:
            return Tree(self.root.left)
        else:
            return None

    def get_right_tree(self):
        if self.root and self.root.right:
            return Tree(self.root.right)
        else:
            return None

    def pre_order_traverse(self):
        node_stack = [self.root]
        out_stack = []

        while node_stack:
            curr_node = node_stack.pop()
            out_stack.append(curr_node)
            if curr_node.left:
                node_stack.append(curr_node.left)

            if curr_node.right:
                node_stack.append(curr_node.right)

        out_stack.append(self.root)

        while out_stack:
            yield out_stack.pop()

    def post_order_traverse(self):
        """
        left, right, root
        :return:
        """
        node_stack = [self.root]
        out_stack = []

        while node_stack:
            curr_node = node_stack.pop()
            out_stack.append(curr_node)

            if curr_node.left:
                node_stack.append(curr_node.left)

            if curr_node.right:
                node_stack.append(curr_node.right)

        while out_stack:
            yield out_stack.pop()

    def in_order_traverse(self):
        """
        1. Start at the root node. Push it on the stack.
        2. Check:

            If there is a left node and right node
            Move to the left node. Update the root node to the current node

            If there is a left node but not a right node
            Move to the left node. Repeat

            If there is a right node but not a left node
            Push the root. Yield the root and move to the right

            Else there are no child nodes
                Push on to the stack yeild the node

        :param node:
        :return:
        """
        curr_node = self.root
        node_stack = []

        while curr_node or node_stack:
            # go left until null
            if curr_node:
                node_stack.append(curr_node)
                curr_node = curr_node.left
            # once null pop, and print move right
            else:
                curr_node = node_stack.pop()
                yield curr_node

                curr_node = curr_node.right

    def __str__(self):
        return Tree(self.root, self.left_tree, self.right_tree)


class BaseSearchTree:
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


class BinaryTreeSearch(Tree, BaseSearchTree):
    _add_return = None
    _delete_return = None

    def add(self, item):
        """
        Object item needs to extend BaseCompare
        :param item: Object/data to insert
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
            return item
        elif item.compare_to(local_root) == 0:
            self._add_return = False
            return local_root
        elif item.compare_to(local_root) < 0:
            local_root.left = self._private_add(local_root.left, item)
            return local_root
        else:
            local_root.right = self._private_add(local_root.right, item)
            return local_root

    def contains(self, target):
        self.root = self._private_add(self.root, target)
        return True if self.root else False

    def find(self, target):
        """
        :param target: Comparable object to find
        :return: Node object ?
        """
        return self._private_find(self.root, target)

    def _private_find(self, local_root: BaseNode, target):
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

    def _find_largest_child(self, parent_node: BaseNode):
        if not parent_node.right.right:
            return_node = parent_node.right.data
            parent_node.right = parent_node.right.left
            return return_node
        else:
            return self._find_largest_child(parent_node.right)

    def remove(self, target):
        self.root = self._private_delete(self.root, target)
        return True if self.root else False
