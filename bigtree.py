class BgNode:
    def __init__(self, d, l, r, n):
        self.data = d
        self.left = l
        self.right = r
        self.mid = n
        self.mult = 0

    # prints the node and all its children in a string
    def __str__(self):
        st = "(" + str(self.data) + ", " + str(self.mult) + ") -> ["
        if self.left != None:
            st += str(self.left)
        else:
            st += "None"
        if self.mid != None:
            st += ", " + str(self.mid)
        else:
            st += ", None"
        if self.right != None:
            st += ", " + str(self.right)
        else:
            st += ", None"

        return st + "]"


class BigTree:
    def __init__(self):
        self.root = None
        self.size = 0

    # print tree using __str__ of bgnodes

    def __str__(self):
        return str(self.root)

    def add(self, st):
        if st == "":
            return None
        if self.root == None:
            self.root = BgNode(st[0], None, None, None)
        ptr = self.root
        for i in range(len(st)):
            d = st[i]
            while True:
                if d == ptr.data:
                    break
                elif d < ptr.data:
                    if ptr.left == None:
                        ptr.left = BgNode(d, None, None, None)
                    ptr = ptr.left
                else:
                    if ptr.right == None:
                        ptr.right = BgNode(d, None, None, None)
                    ptr = ptr.right
            if i < len(st) - 1 and ptr.mid == None:
                ptr.mid = BgNode(st[i + 1], None, None, None)
            if i < len(st) - 1:
                ptr = ptr.mid

        ptr.mult += 1
        self.size += 1

    def addAll(self, A):
        for x in A: self.add(x)

    def printAll(self):
        def printFrom(ptr, s):
            if ptr == None: return
            s0 = s + ptr.data
            if ptr.left != None: printFrom(ptr.left, s)
            for i in range(ptr.mult): print(s0, end=" ")
            if ptr.mid != None: printFrom(ptr.mid, s + ptr.data)
            if ptr.right != None: printFrom(ptr.right, s)

        printFrom(self.root, "");
        print()

        # print the nodes in the tree in level order

    def printTree(self):
        if self.root == None:
            return
        q = [self.root]
        while len(q) > 0:
            ptr = q.pop(0)
            print(ptr, end=" ")
            if ptr.left != None:
                q.append(ptr.left)
            if ptr.mid != None:
                q.append(ptr.mid)
            if ptr.right != None:
                q.append(ptr.right)
        print()

    def count(self, st):
        if st == "":
            return 0
        ptr = self.root
        for i in range(len(st)):
            d = st[i]
            while ptr != None and d != ptr.data:
                if d < ptr.data:
                    ptr = ptr.left
                else:
                    ptr = ptr.right
            if ptr == None:
                return 0
            if i < len(st) - 1:
                ptr = ptr.mid
        return ptr.mult



    def toIncArray(self):    ##prints all the strings present in the tree in the form of an arrayin an increasing order
        def incRec(ptr, s, A, c):
            if ptr == None:
                return c
            s0 = s + ptr.data
            if ptr.left != None:
                c = incRec(ptr.left, s, A, c)
            for i in range(ptr.mult):
                A[c] = s0
                c += 1
            if ptr.mid != None:
                c = incRec(ptr.mid, s + ptr.data, A, c)
            if ptr.right != None:
                c = incRec(ptr.right, s, A, c)
            return c

        A = [None for _ in range(self.size)]
        incRec(self.root, "", A, 0)
        return A

    def toDecArray(self):     ##prints all the strings present in the tree in the form of an array in decreasing order
        def reverse(A):
            for i in range(len(A) // 2):
                A[i], A[len(A) - 1 - i] = A[len(A) - 1 - i], A[i]
            return A

        def incRec(ptr, s, A, c):
            if ptr == None:
                return c
            s0 = s + ptr.data
            if ptr.left != None:
                c = incRec(ptr.left, s, A, c)
            for i in range(ptr.mult):
                A[c] = s0
                c += 1
            if ptr.mid != None:
                c = incRec(ptr.mid, s + ptr.data, A, c)
            if ptr.right != None:
                c = incRec(ptr.right, s, A, c)
            return c

        A = [None for _ in range(self.size)]
        incRec(self.root, "", A, 0)

        return reverse(A)

    def remove(self, st):
        if st == "":
            return None
        ptr = self.root
        for i in range(len(st)):
            d = st[i]
            while ptr != None and d != ptr.data:
                if d < ptr.data:
                    ptr = ptr.left
                else:
                    ptr = ptr.right
            if ptr == None:
                return 0
            if i < len(st) - 1:
                ptr = ptr.mid
        if ptr.mult > 0:
            ptr.mult -= 1
            self.size -= 1
            if self.size == 0:
                self.root = None
            return 1

        return 0