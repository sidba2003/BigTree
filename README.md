This project is about an extension of binary search trees that is useful for storing strings.
We define a big tree to be a tree where:

•each node has three children: left, right and mid.
• each node contains a character (the data of the node) and a non-negative integer
(the multiplicity of the stored data).
• the left child of a node, if it exists, contains a character that is smaller
(alphabetically) than the character of the node.
• the right child of a node, if it exists, contains a character that is greater than the
character of the node.
Thus, the use of left and right children follows the same lines as in binary search trees. On
the other hand, the mid child of a node stands for the next character in the string that we
are storing.

I have implemented the following methods:- 
• a constructor (__init__) and a string function (__str__).
• add, addAll : adds a string in the tree, adds an array of strings in the tree.
• printAll : prints all the elements of the tree, with spaces in between.
• count : for counting the number of times that a string is stored in the tree.
• toIncArray : for returning an array with all the elements of the tree in increasing
order.
• toDecArray : for returning an array with all the elements of the tree in decreasing
order. 
• remove : for removing a string from the tree. The function should remove every
node that, after a string removal, has multiplicity 0 and does not have a mid child. 
