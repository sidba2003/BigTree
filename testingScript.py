## Testing script


from bigtree import BgNode, BigTree

######################################################################
# initialisations and imports
######################################################################

printMark = 0.9
sizeMark = 0.1
printError = "print mismatch; "
sizeError = "size mismatch; "
exceptionError = " E: "
sanityChecking = False


def justError(i):
    return str(i) + "! "


res = ""
nameST = "test"


######################################################################
# main function for running a list of tests
# helper function for converting test results into string
######################################################################

# stripped-down version for Windows signal problems
def tryWithTimeout(thunk):
    (res, error) = (None, "")
    res = thunk()
    return (res, error)


def runTests(tests):
    awarded, total, res = 0, 0, ""
    for (UID, test) in tests:
        (name, mark, msg, grade) = test()
        s = "[" + str(UID) + "]: " + name
        dots = ''.join(map(str, ['.' for i in range(35 - len(s))]))
        res += s + dots
        awarded += grade * mark
        if round(mark, 2) == 0:
            res += "error [" + msg + "], awarded: 0 of " + str(grade)
        elif round(mark, 2) == 1:
            res += "success, awarded: " + str(grade)
        else:
            res += "error/warning [" + msg + "], awarded: " + str(mark * grade) + " of " + str(grade)
        res += "\n"
        total += grade
    (awarded, total) = (round(awarded, 2), round(total, 2))
    res += "\nTotal (sample) testing marks [16]: " + str(awarded)
    return (awarded, total, res)


######################################################################
# code for constructing tree structures from strings
# (for testing count etc, without using add)
######################################################################

def parseST(st):
    A = st.replace(" -> ", "").replace("[", ",").replace("]", "").replace("(", "").replace(")", "").replace(" ",
                                                                                                            "").replace(
        ",,", ",").split(",")
    t = BigTree()
    (t.root, t.size, A) = parseSTSubtree(A, 0)
    return t


def parseSTSubtree(A, size):
    if A[0] == "None": return (None, size, A[1:])
    ptr = BgNode(A[0], None, None, None)
    ptr.mult = int(A[1])
    (ptr.left, size, A) = parseSTSubtree(A[2:], size)
    (ptr.mid, size, A) = parseSTSubtree(A, size)
    (ptr.right, size, A) = parseSTSubtree(A, size)
    return (ptr, size + ptr.mult, A)


def sanity(words, model, testname):
    t = BigTree()
    for w in words: t.add(w)
    if str(t) != model:
        print("something is wrong! " + testname)


def sanity2(words, tree, testname):
    # This could be moved to BgNode
    def equal(t1, t2):
        if t1 == t2 == None: return True
        if t1 == None or t2 == None: return False
        return t1.data == t2.data and t1.mult == t2.mult and equal(t1.left, t2.left) and equal(t1.mid,
                                                                                               t2.mid) and equal(
            t1.right, t2.right)

    t = BigTree()
    for w in words: t.add(w)
    if not equal(t.root, tree.root): print("something is wrong!! " + testname)


## for count, min, max and remove, test using parsing

def oneStageTest(what, nm, words, model, msg, grade, helperFun, helperArgs):
    testName = nameST + " [" + what + " " + nm + "]"
    if sanityChecking: sanity(words, model, testName)
    tree = parseST(model)
    if sanityChecking: sanity2(words, tree, testName)
    (mark, msg) = helperFun(tree, helperArgs)
    return (testName, mark, msg, grade)


###################################
# tests for count
###################################

def countTestST(nm, words, model, nums, sols, msg, grade):
    return oneStageTest("count", nm, words, model, msg, grade, countTestSTHelper, [nums, sols])


def countTestSTHelper(tree, args):
    [nums, sols] = args
    (mark, msg) = (0, "")
    minimark = 1 / len(sols)
    for i in range(len(nums)):
        (toCount, sol) = (nums[i], sols[i])
        (counted, error) = tryWithTimeout(lambda: tree.count(toCount))
        if error != "":
            msg += error
        elif counted == sol:
            mark += minimark
        else:
            msg += justError(i)
    return (mark, msg)


def testST_C_10():  # words in 15 double random words [sample]
    someIn = ["hit", "zath", "dunt", "cofsod", "olne", "sargu", "tam", "wesk", "cats", "gos"]
    words = words30
    model = "(s, 0) -> [(m, 0) -> [(h, 0) -> [(d, 0) -> [(c, 0) -> [None, (o, 0) -> [(a, 0) -> [None, (t, 0) -> [None, (s, 2) -> [None, None, None], None], None], (f, 0) -> [None, (s, 0) -> [None, (o, 0) -> [None, (d, 2) -> [None, None, None], None], None], None], None], None], (o, 0) -> [None, (l, 0) -> [None, (s, 2) -> [None, None, None], None], (u, 0) -> [None, (n, 0) -> [None, (t, 2) -> [None, None, None], None], None]], (g, 0) -> [None, (o, 0) -> [None, (s, 2) -> [None, None, None], None], None]], (i, 0) -> [None, (t, 2) -> [None, None, None], None], None], (e, 0) -> [None, (n, 2) -> [None, None, None], (o, 0) -> [None, (f, 2) -> [None, None, None], None]], (o, 0) -> [None, (l, 0) -> [None, (n, 0) -> [None, (e, 2) -> [None, None, None], None], None], None]], (e, 0) -> [(a, 0) -> [None, (r, 0) -> [None, (g, 0) -> [None, (u, 2) -> [None, None, None], None], None], None], (c, 0) -> [None, (a, 2) -> [None, None, None], None], None], (z, 0) -> [(t, 0) -> [None, (r, 0) -> [(a, 0) -> [None, (m, 2) -> [None, None, None], None], (o, 0) -> [None, (s, 0) -> [None, (s, 0) -> [None, (y, 2) -> [None, None, None], None], None], None], None], (w, 0) -> [None, (e, 0) -> [None, (s, 0) -> [None, (k, 2) -> [None, None, None], None], None], None]], (a, 0) -> [None, (t, 0) -> [None, (h, 2) -> [None, None, None], None], None], None]]"
    sol = [2 for i in range(10)]
    return countTestST("10", words, model, someIn, sol, "counting words (not) in tree", 1)


def testST_C_11():  # words not in 50 random words [sample]
    tenNotIn = ["rot", "cas", "stolb", "ada", "lend", "sake", "umith", "daltha", "jy", "spith"]
    words = words50_1
    model = "(r, 0) -> [(a, 0) -> [None, (r, 1) -> [(i, 0) -> [None, (x, 1) -> [None, None, None], None], (t, 1) -> [(o, 0) -> [None, (b, 1) -> [None, None, None], None], None, None], (s, 0) -> [None, (n, 0) -> [None, (u, 1) -> [None, None, None], (t, 0) -> [None, (l, 0) -> [None, (e, 0) -> [None, (t, 0) -> [None, (w, 0) -> [None, (o, 1) -> [None, None, None], None], None], None], None], None]], None]], (h, 0) -> [(c, 0) -> [(b, 0) -> [None, (o, 0) -> [(a, 0) -> [None, (r, 1) -> [(c, 0) -> [None, (k, 1) -> [None, None, None], None], None, None], None], (b, 0) -> [None, (d, 1) -> [None, None, None], (f, 1) -> [None, None, None]], None], None], (u, 0) -> [(a, 0) -> [None, (s, 0) -> [None, (t, 1) -> [None, None, None], None], (h, 0) -> [None, (o, 1) -> [None, None, None], None]], (s, 0) -> [None, (r, 0) -> [None, (e, 1) -> [None, None, None], None], None], None], (g, 0) -> [(d, 0) -> [None, (r, 0) -> [(e, 0) -> [None, (n, 0) -> [None, (t, 1) -> [None, None, None], None], (i, 0) -> [None, (s, 0) -> [None, (p, 0) -> [None, (a, 1) -> [None, None, None], None], None], None]], (o, 0) -> [None, (u, 0) -> [None, (b, 0) -> [None, (i, 0) -> [None, (c, 0) -> [None, (a, 1) -> [None, None, None], None], None], None], None], None], (u, 1) -> [None, None, (y, 1) -> [None, None, None]]], (e, 0) -> [None, (d, 0) -> [None, (e, 0) -> [None, (n, 0) -> [None, (t, 1) -> [None, None, None], None], None], (h, 0) -> [None, (i, 0) -> [None, (l, 0) -> [None, (l, 0) -> [None, (e, 0) -> [None, (m, 1) -> [None, None, None], None], None], None], None], (l, 0) -> [None, (s, 1) -> [None, None, None], None]]], (f, 0) -> [None, (o, 0) -> [None, (c, 0) -> [None, (l, 0) -> [None, (o, 0) -> [None, (t, 0) -> [None, (e, 0) -> [None, (s, 0) -> [None, (h, 1) -> [None, None, None], None], None], None], None], None], None], None], None]]], (u, 0) -> [(o, 0) -> [None, (d, 1) -> [(c, 0) -> [None, (l, 1) -> [None, None, None], None], None, None], None], (g, 1) -> [None, None, None], None], None]], (a, 0) -> [None, (r, 1) -> [None, None, None], None], (k, 0) -> [(j, 0) -> [None, (a, 0) -> [None, (t, 1) -> [None, None, None], None], None], (n, 0) -> [None, (a, 0) -> [None, (t, 1) -> [None, None, None], None], None], (l, 0) -> [None, (i, 0) -> [None, (r, 0) -> [None, (v, 0) -> [None, (i, 0) -> [None, (n, 0) -> [None, (n, 0) -> [None, (u, 0) -> [None, (n, 1) -> [None, None, None], None], None], None], None], None], None], None], (p, 0) -> [(m, 0) -> [None, (u, 0) -> [None, (t, 0) -> [None, (l, 0) -> [None, (u, 0) -> [None, (n, 0) -> [None, (t, 1) -> [None, None, None], None], None], None], None], None], (o, 0) -> [None, (n, 1) -> [None, None, None], None]], (l, 0) -> [(a, 0) -> [None, (l, 0) -> [None, (l, 0) -> [None, (a, 1) -> [None, None, None], (t, 1) -> [None, None, None]], None], (e, 0) -> [None, (j, 0) -> [None, (o, 0) -> [None, (r, 1) -> [None, None, None], None], None], (i, 0) -> [None, (m, 1) -> [None, None, None], None]]], (i, 1) -> [None, None, None], (o, 0) -> [None, (n, 0) -> [None, (g, 1) -> [None, None, None], None], (r, 0) -> [None, (a, 0) -> [None, (l, 0) -> [None, (i, 0) -> [None, (v, 0) -> [None, (e, 0) -> [None, (a, 0) -> [None, (r, 1) -> [None, None, None], None], None], None], None], None], None], None]]], None]]]]], (u, 0) -> [(i, 0) -> [(a, 0) -> [None, (s, 0) -> [None, (s, 1) -> [None, None, (u, 0) -> [None, (i, 0) -> [None, (m, 0) -> [None, (u, 1) -> [None, None, None], None], None], None]], (t, 0) -> [None, (c, 0) -> [None, (h, 1) -> [None, None, None], None], None]], (e, 0) -> [None, (g, 1) -> [None, None, None], None]], (p, 0) -> [None, (l, 0) -> [None, (y, 1) -> [None, None, None], None], None], None], (o, 0) -> [None, (t, 0) -> [None, (c, 0) -> [None, (h, 1) -> [None, None, None], None], None], None], None], (t, 0) -> [(s, 0) -> [None, (i, 0) -> [(c, 0) -> [None, (a, 0) -> [None, (n, 0) -> [None, (n, 0) -> [None, (a, 1) -> [None, None, None], None], None], None], (h, 0) -> [None, (i, 0) -> [None, (f, 0) -> [None, (f, 0) -> [None, (o, 1) -> [None, None, None], None], None], None], None]], (m, 0) -> [None, (m, 0) -> [None, (o, 1) -> [None, None, None], None], None], (u, 0) -> [None, (t, 0) -> [None, (u, 0) -> [None, (r, 1) -> [None, None, None], None], None], None]], None], (a, 0) -> [None, (l, 0) -> [None, (c, 0) -> [None, (r, 0) -> [None, (u, 1) -> [None, None, None], None], None], None], (r, 0) -> [None, (a, 0) -> [None, (n, 0) -> [None, (g, 0) -> [None, (r, 0) -> [None, (e, 0) -> [None, (d, 0) -> [None, (l, 0) -> [None, (u, 1) -> [None, None, None], None], None], None], None], None], None], None], None]], None]]"
    sol = [0 for i in range(10)]
    return countTestST("11", words, model, tenNotIn, sol, "counting words not in tree", 1)


def testST_C_30():  # similar words [sample]
    someIn = ["hello", "hell"]
    words = ["he", "hello", "hex", "hexagon", "hell", "hell"]
    model = "(h, 0) -> [None, (e, 1) -> [None, (l, 0) -> [None, (l, 2) -> [None, (o, 1) -> [None, None, None], None], (x, 1) -> [None, (a, 0) -> [None, (g, 0) -> [None, (o, 0) -> [None, (n, 1) -> [None, None, None], None], None], None], None]], None], None]"
    sol = [1, 2]
    return countTestST("30", words, model, someIn, sol, "counting words in tree", 1)


countTestsST = [testST_C_10, testST_C_11, testST_C_30]


#######################################
# tests for toIncArray
#######################################

def incTestST(nm, words, model, _, sol, msg, grade):
    return oneStageTest("inc", nm, words, model, msg, grade, incTestSTHelper, sol)


def incTestSTHelper(tree, args):
    sol = args
    (mark, msg) = (0, "")
    (A, error) = tryWithTimeout(lambda: tree.toIncArray())
    if error != "":
        msg += error
    elif A == sol:
        mark += 1
    else:
        msg += "solution is " + str(sol) + ", not " + str(A)
    return (mark, msg)


def testST_Inc_03():  # two words [sample]
    words = ["hello" for i in range(5)] + ["world" for i in range(5)]
    sol = words
    model = "(h, 0) -> [None, (e, 0) -> [None, (l, 0) -> [None, (l, 0) -> [None, (o, 5) -> [None, None, None], None], None], None], (w, 0) -> [None, (o, 0) -> [None, (r, 0) -> [None, (l, 0) -> [None, (d, 5) -> [None, None, None], None], None], None], None]]"
    return incTestST("03", words, model, [], sol, "toIncArray 03", 1)


def testST_Inc_04():  # example from spec [sample]
    words = ["cat", "ca", "can", "cat", "cat"]
    sol = ["ca", "can", "cat", "cat", "cat"]
    model = "(c, 0) -> [None, (a, 1) -> [None, (t, 3) -> [(n, 1) -> [None, None, None], None, None], None], None]"
    return incTestST("04", words, model, [], sol, "toIncArray 04", 1)


def testST_Inc_12():  # 15 double random words [sample]
    words = words30
    sol = words30Inc
    model = "(s, 0) -> [(m, 0) -> [(h, 0) -> [(d, 0) -> [(c, 0) -> [None, (o, 0) -> [(a, 0) -> [None, (t, 0) -> [None, (s, 2) -> [None, None, None], None], None], (f, 0) -> [None, (s, 0) -> [None, (o, 0) -> [None, (d, 2) -> [None, None, None], None], None], None], None], None], (o, 0) -> [None, (l, 0) -> [None, (s, 2) -> [None, None, None], None], (u, 0) -> [None, (n, 0) -> [None, (t, 2) -> [None, None, None], None], None]], (g, 0) -> [None, (o, 0) -> [None, (s, 2) -> [None, None, None], None], None]], (i, 0) -> [None, (t, 2) -> [None, None, None], None], None], (e, 0) -> [None, (n, 2) -> [None, None, None], (o, 0) -> [None, (f, 2) -> [None, None, None], None]], (o, 0) -> [None, (l, 0) -> [None, (n, 0) -> [None, (e, 2) -> [None, None, None], None], None], None]], (e, 0) -> [(a, 0) -> [None, (r, 0) -> [None, (g, 0) -> [None, (u, 2) -> [None, None, None], None], None], None], (c, 0) -> [None, (a, 2) -> [None, None, None], None], None], (z, 0) -> [(t, 0) -> [None, (r, 0) -> [(a, 0) -> [None, (m, 2) -> [None, None, None], None], (o, 0) -> [None, (s, 0) -> [None, (s, 0) -> [None, (y, 2) -> [None, None, None], None], None], None], None], (w, 0) -> [None, (e, 0) -> [None, (s, 0) -> [None, (k, 2) -> [None, None, None], None], None], None]], (a, 0) -> [None, (t, 0) -> [None, (h, 2) -> [None, None, None], None], None], None]]"
    return incTestST("12", words, model, [], sol, "toIncArray 05", 1)


def testST_Inc_13():  # 50 random words [sample]
    words = words50_1
    sol = words50_1Inc
    model = "(r, 0) -> [(a, 0) -> [None, (r, 1) -> [(i, 0) -> [None, (x, 1) -> [None, None, None], None], (t, 1) -> [(o, 0) -> [None, (b, 1) -> [None, None, None], None], None, None], (s, 0) -> [None, (n, 0) -> [None, (u, 1) -> [None, None, None], (t, 0) -> [None, (l, 0) -> [None, (e, 0) -> [None, (t, 0) -> [None, (w, 0) -> [None, (o, 1) -> [None, None, None], None], None], None], None], None]], None]], (h, 0) -> [(c, 0) -> [(b, 0) -> [None, (o, 0) -> [(a, 0) -> [None, (r, 1) -> [(c, 0) -> [None, (k, 1) -> [None, None, None], None], None, None], None], (b, 0) -> [None, (d, 1) -> [None, None, None], (f, 1) -> [None, None, None]], None], None], (u, 0) -> [(a, 0) -> [None, (s, 0) -> [None, (t, 1) -> [None, None, None], None], (h, 0) -> [None, (o, 1) -> [None, None, None], None]], (s, 0) -> [None, (r, 0) -> [None, (e, 1) -> [None, None, None], None], None], None], (g, 0) -> [(d, 0) -> [None, (r, 0) -> [(e, 0) -> [None, (n, 0) -> [None, (t, 1) -> [None, None, None], None], (i, 0) -> [None, (s, 0) -> [None, (p, 0) -> [None, (a, 1) -> [None, None, None], None], None], None]], (o, 0) -> [None, (u, 0) -> [None, (b, 0) -> [None, (i, 0) -> [None, (c, 0) -> [None, (a, 1) -> [None, None, None], None], None], None], None], None], (u, 1) -> [None, None, (y, 1) -> [None, None, None]]], (e, 0) -> [None, (d, 0) -> [None, (e, 0) -> [None, (n, 0) -> [None, (t, 1) -> [None, None, None], None], None], (h, 0) -> [None, (i, 0) -> [None, (l, 0) -> [None, (l, 0) -> [None, (e, 0) -> [None, (m, 1) -> [None, None, None], None], None], None], None], (l, 0) -> [None, (s, 1) -> [None, None, None], None]]], (f, 0) -> [None, (o, 0) -> [None, (c, 0) -> [None, (l, 0) -> [None, (o, 0) -> [None, (t, 0) -> [None, (e, 0) -> [None, (s, 0) -> [None, (h, 1) -> [None, None, None], None], None], None], None], None], None], None], None]]], (u, 0) -> [(o, 0) -> [None, (d, 1) -> [(c, 0) -> [None, (l, 1) -> [None, None, None], None], None, None], None], (g, 1) -> [None, None, None], None], None]], (a, 0) -> [None, (r, 1) -> [None, None, None], None], (k, 0) -> [(j, 0) -> [None, (a, 0) -> [None, (t, 1) -> [None, None, None], None], None], (n, 0) -> [None, (a, 0) -> [None, (t, 1) -> [None, None, None], None], None], (l, 0) -> [None, (i, 0) -> [None, (r, 0) -> [None, (v, 0) -> [None, (i, 0) -> [None, (n, 0) -> [None, (n, 0) -> [None, (u, 0) -> [None, (n, 1) -> [None, None, None], None], None], None], None], None], None], None], (p, 0) -> [(m, 0) -> [None, (u, 0) -> [None, (t, 0) -> [None, (l, 0) -> [None, (u, 0) -> [None, (n, 0) -> [None, (t, 1) -> [None, None, None], None], None], None], None], None], (o, 0) -> [None, (n, 1) -> [None, None, None], None]], (l, 0) -> [(a, 0) -> [None, (l, 0) -> [None, (l, 0) -> [None, (a, 1) -> [None, None, None], (t, 1) -> [None, None, None]], None], (e, 0) -> [None, (j, 0) -> [None, (o, 0) -> [None, (r, 1) -> [None, None, None], None], None], (i, 0) -> [None, (m, 1) -> [None, None, None], None]]], (i, 1) -> [None, None, None], (o, 0) -> [None, (n, 0) -> [None, (g, 1) -> [None, None, None], None], (r, 0) -> [None, (a, 0) -> [None, (l, 0) -> [None, (i, 0) -> [None, (v, 0) -> [None, (e, 0) -> [None, (a, 0) -> [None, (r, 1) -> [None, None, None], None], None], None], None], None], None], None]]], None]]]]], (u, 0) -> [(i, 0) -> [(a, 0) -> [None, (s, 0) -> [None, (s, 1) -> [None, None, (u, 0) -> [None, (i, 0) -> [None, (m, 0) -> [None, (u, 1) -> [None, None, None], None], None], None]], (t, 0) -> [None, (c, 0) -> [None, (h, 1) -> [None, None, None], None], None]], (e, 0) -> [None, (g, 1) -> [None, None, None], None]], (p, 0) -> [None, (l, 0) -> [None, (y, 1) -> [None, None, None], None], None], None], (o, 0) -> [None, (t, 0) -> [None, (c, 0) -> [None, (h, 1) -> [None, None, None], None], None], None], None], (t, 0) -> [(s, 0) -> [None, (i, 0) -> [(c, 0) -> [None, (a, 0) -> [None, (n, 0) -> [None, (n, 0) -> [None, (a, 1) -> [None, None, None], None], None], None], (h, 0) -> [None, (i, 0) -> [None, (f, 0) -> [None, (f, 0) -> [None, (o, 1) -> [None, None, None], None], None], None], None]], (m, 0) -> [None, (m, 0) -> [None, (o, 1) -> [None, None, None], None], None], (u, 0) -> [None, (t, 0) -> [None, (u, 0) -> [None, (r, 1) -> [None, None, None], None], None], None]], None], (a, 0) -> [None, (l, 0) -> [None, (c, 0) -> [None, (r, 0) -> [None, (u, 1) -> [None, None, None], None], None], None], (r, 0) -> [None, (a, 0) -> [None, (n, 0) -> [None, (g, 0) -> [None, (r, 0) -> [None, (e, 0) -> [None, (d, 0) -> [None, (l, 0) -> [None, (u, 1) -> [None, None, None], None], None], None], None], None], None], None], None]], None]]"
    return incTestST("13", words, model, [], sol, "inIncArray 13", 1)


def testST_Inc_20():  # similar words [sample]
    words = ["he", "hello", "hex", "hexagon", "hell"]
    sol = ["he", "hell", "hello", "hex", "hexagon"]
    model = "(h, 0) -> [None, (e, 1) -> [None, (l, 0) -> [None, (l, 1) -> [None, (o, 1) -> [None, None, None], None], (x, 1) -> [None, (a, 0) -> [None, (g, 0) -> [None, (o, 0) -> [None, (n, 1) -> [None, None, None], None], None], None], None]], None], None]"
    return incTestST("20", words, model, [], sol, "toIncArray 20", 1)


incTestsST = [testST_Inc_03, testST_Inc_04, testST_Inc_12, testST_Inc_13, testST_Inc_20]


#######################################
# tests for toDecARray
#######################################

def decTestST(nm, words, model, _, sol, msg, grade):
    return oneStageTest("dec", nm, words, model, msg, grade, decTestSTHelper, sol)


def decTestSTHelper(tree, args):
    sol = args
    (mark, msg) = (0, "")
    (A, error) = tryWithTimeout(lambda: tree.toDecArray())
    if error != "":
        msg += error
    elif A == sol:
        mark += 1
    else:
        msg += "solution is " + str(sol) + ", not " + str(A)
    return (mark, msg)


def testST_Dec_03():  # two words [sample]
    words = ["hello" for _ in range(5)] + ["world" for _ in range(5)]
    sol = ["world" for _ in range(5)] + ["hello" for _ in range(5)]
    model = "(h, 0) -> [None, (e, 0) -> [None, (l, 0) -> [None, (l, 0) -> [None, (o, 5) -> [None, None, None], None], None], None], (w, 0) -> [None, (o, 0) -> [None, (r, 0) -> [None, (l, 0) -> [None, (d, 5) -> [None, None, None], None], None], None], None]]"
    return decTestST("03", words, model, [], sol, "toDecArray 30", 1)


def testST_Dec_04():  # example from spec [sample]
    words = ["cat", "ca", "can", "cat", "cat"]
    sol = ["cat", "cat", "cat", "can", "ca"]
    model = "(c, 0) -> [None, (a, 1) -> [None, (t, 3) -> [(n, 1) -> [None, None, None], None, None], None], None]"
    return decTestST("04", words, model, [], sol, "toDecArray 04", 1)


def testST_Dec_12():  # 30 double random words [sample]
    words = words30
    sol = words30Dec
    model = "(s, 0) -> [(m, 0) -> [(h, 0) -> [(d, 0) -> [(c, 0) -> [None, (o, 0) -> [(a, 0) -> [None, (t, 0) -> [None, (s, 2) -> [None, None, None], None], None], (f, 0) -> [None, (s, 0) -> [None, (o, 0) -> [None, (d, 2) -> [None, None, None], None], None], None], None], None], (o, 0) -> [None, (l, 0) -> [None, (s, 2) -> [None, None, None], None], (u, 0) -> [None, (n, 0) -> [None, (t, 2) -> [None, None, None], None], None]], (g, 0) -> [None, (o, 0) -> [None, (s, 2) -> [None, None, None], None], None]], (i, 0) -> [None, (t, 2) -> [None, None, None], None], None], (e, 0) -> [None, (n, 2) -> [None, None, None], (o, 0) -> [None, (f, 2) -> [None, None, None], None]], (o, 0) -> [None, (l, 0) -> [None, (n, 0) -> [None, (e, 2) -> [None, None, None], None], None], None]], (e, 0) -> [(a, 0) -> [None, (r, 0) -> [None, (g, 0) -> [None, (u, 2) -> [None, None, None], None], None], None], (c, 0) -> [None, (a, 2) -> [None, None, None], None], None], (z, 0) -> [(t, 0) -> [None, (r, 0) -> [(a, 0) -> [None, (m, 2) -> [None, None, None], None], (o, 0) -> [None, (s, 0) -> [None, (s, 0) -> [None, (y, 2) -> [None, None, None], None], None], None], None], (w, 0) -> [None, (e, 0) -> [None, (s, 0) -> [None, (k, 2) -> [None, None, None], None], None], None]], (a, 0) -> [None, (t, 0) -> [None, (h, 2) -> [None, None, None], None], None], None]]"
    return decTestST("12", words, model, [], sol, "toDecArray 12", 1)


def testST_Dec_13():  # 50 random words [sample]
    words = words50_1
    sol = words50_1Dec
    model = "(r, 0) -> [(a, 0) -> [None, (r, 1) -> [(i, 0) -> [None, (x, 1) -> [None, None, None], None], (t, 1) -> [(o, 0) -> [None, (b, 1) -> [None, None, None], None], None, None], (s, 0) -> [None, (n, 0) -> [None, (u, 1) -> [None, None, None], (t, 0) -> [None, (l, 0) -> [None, (e, 0) -> [None, (t, 0) -> [None, (w, 0) -> [None, (o, 1) -> [None, None, None], None], None], None], None], None]], None]], (h, 0) -> [(c, 0) -> [(b, 0) -> [None, (o, 0) -> [(a, 0) -> [None, (r, 1) -> [(c, 0) -> [None, (k, 1) -> [None, None, None], None], None, None], None], (b, 0) -> [None, (d, 1) -> [None, None, None], (f, 1) -> [None, None, None]], None], None], (u, 0) -> [(a, 0) -> [None, (s, 0) -> [None, (t, 1) -> [None, None, None], None], (h, 0) -> [None, (o, 1) -> [None, None, None], None]], (s, 0) -> [None, (r, 0) -> [None, (e, 1) -> [None, None, None], None], None], None], (g, 0) -> [(d, 0) -> [None, (r, 0) -> [(e, 0) -> [None, (n, 0) -> [None, (t, 1) -> [None, None, None], None], (i, 0) -> [None, (s, 0) -> [None, (p, 0) -> [None, (a, 1) -> [None, None, None], None], None], None]], (o, 0) -> [None, (u, 0) -> [None, (b, 0) -> [None, (i, 0) -> [None, (c, 0) -> [None, (a, 1) -> [None, None, None], None], None], None], None], None], (u, 1) -> [None, None, (y, 1) -> [None, None, None]]], (e, 0) -> [None, (d, 0) -> [None, (e, 0) -> [None, (n, 0) -> [None, (t, 1) -> [None, None, None], None], None], (h, 0) -> [None, (i, 0) -> [None, (l, 0) -> [None, (l, 0) -> [None, (e, 0) -> [None, (m, 1) -> [None, None, None], None], None], None], None], (l, 0) -> [None, (s, 1) -> [None, None, None], None]]], (f, 0) -> [None, (o, 0) -> [None, (c, 0) -> [None, (l, 0) -> [None, (o, 0) -> [None, (t, 0) -> [None, (e, 0) -> [None, (s, 0) -> [None, (h, 1) -> [None, None, None], None], None], None], None], None], None], None], None]]], (u, 0) -> [(o, 0) -> [None, (d, 1) -> [(c, 0) -> [None, (l, 1) -> [None, None, None], None], None, None], None], (g, 1) -> [None, None, None], None], None]], (a, 0) -> [None, (r, 1) -> [None, None, None], None], (k, 0) -> [(j, 0) -> [None, (a, 0) -> [None, (t, 1) -> [None, None, None], None], None], (n, 0) -> [None, (a, 0) -> [None, (t, 1) -> [None, None, None], None], None], (l, 0) -> [None, (i, 0) -> [None, (r, 0) -> [None, (v, 0) -> [None, (i, 0) -> [None, (n, 0) -> [None, (n, 0) -> [None, (u, 0) -> [None, (n, 1) -> [None, None, None], None], None], None], None], None], None], None], (p, 0) -> [(m, 0) -> [None, (u, 0) -> [None, (t, 0) -> [None, (l, 0) -> [None, (u, 0) -> [None, (n, 0) -> [None, (t, 1) -> [None, None, None], None], None], None], None], None], (o, 0) -> [None, (n, 1) -> [None, None, None], None]], (l, 0) -> [(a, 0) -> [None, (l, 0) -> [None, (l, 0) -> [None, (a, 1) -> [None, None, None], (t, 1) -> [None, None, None]], None], (e, 0) -> [None, (j, 0) -> [None, (o, 0) -> [None, (r, 1) -> [None, None, None], None], None], (i, 0) -> [None, (m, 1) -> [None, None, None], None]]], (i, 1) -> [None, None, None], (o, 0) -> [None, (n, 0) -> [None, (g, 1) -> [None, None, None], None], (r, 0) -> [None, (a, 0) -> [None, (l, 0) -> [None, (i, 0) -> [None, (v, 0) -> [None, (e, 0) -> [None, (a, 0) -> [None, (r, 1) -> [None, None, None], None], None], None], None], None], None], None]]], None]]]]], (u, 0) -> [(i, 0) -> [(a, 0) -> [None, (s, 0) -> [None, (s, 1) -> [None, None, (u, 0) -> [None, (i, 0) -> [None, (m, 0) -> [None, (u, 1) -> [None, None, None], None], None], None]], (t, 0) -> [None, (c, 0) -> [None, (h, 1) -> [None, None, None], None], None]], (e, 0) -> [None, (g, 1) -> [None, None, None], None]], (p, 0) -> [None, (l, 0) -> [None, (y, 1) -> [None, None, None], None], None], None], (o, 0) -> [None, (t, 0) -> [None, (c, 0) -> [None, (h, 1) -> [None, None, None], None], None], None], None], (t, 0) -> [(s, 0) -> [None, (i, 0) -> [(c, 0) -> [None, (a, 0) -> [None, (n, 0) -> [None, (n, 0) -> [None, (a, 1) -> [None, None, None], None], None], None], (h, 0) -> [None, (i, 0) -> [None, (f, 0) -> [None, (f, 0) -> [None, (o, 1) -> [None, None, None], None], None], None], None]], (m, 0) -> [None, (m, 0) -> [None, (o, 1) -> [None, None, None], None], None], (u, 0) -> [None, (t, 0) -> [None, (u, 0) -> [None, (r, 1) -> [None, None, None], None], None], None]], None], (a, 0) -> [None, (l, 0) -> [None, (c, 0) -> [None, (r, 0) -> [None, (u, 1) -> [None, None, None], None], None], None], (r, 0) -> [None, (a, 0) -> [None, (n, 0) -> [None, (g, 0) -> [None, (r, 0) -> [None, (e, 0) -> [None, (d, 0) -> [None, (l, 0) -> [None, (u, 1) -> [None, None, None], None], None], None], None], None], None], None], None]], None]]"
    return decTestST("13", words, model, [], sol, "toDecArray 13", 1)


def testST_Dec_20():  # similar words [sample]
    words = ["he", "hello", "hex", "hexagon", "hell"]
    sol = ["hexagon", "hex", "hello", "hell", "he"]
    model = "(h, 0) -> [None, (e, 1) -> [None, (l, 0) -> [None, (l, 1) -> [None, (o, 1) -> [None, None, None], None], (x, 1) -> [None, (a, 0) -> [None, (g, 0) -> [None, (o, 0) -> [None, (n, 1) -> [None, None, None], None], None], None], None]], None], None]"
    return decTestST("20", words, model, [], sol, "toDecArray 20", 1)


decTestsST = [testST_Dec_03, testST_Dec_04, testST_Dec_12, testST_Dec_13, testST_Dec_20]


###################################
# tests for remove
###################################

def removeTestST(nm, words, model, nums, sol, size, msg, grade):
    return oneStageTest("remove", nm, words, model, msg, grade, removeTestSTHelper, [nums, sol, size])


def removeTestSTHelper(tree, args):
    [nums, sol, size] = args
    (mark, msg) = (0, "")
    for i in range(len(nums)):
        toRemove = nums[i]
        (_, error) = tryWithTimeout(lambda: tree.remove(toRemove))
        if error != "": return (0, error)
    if str(tree) == sol:
        mark += printMark
    else:
        msg += printError
    if tree.size == size:
        mark += sizeMark
    else:
        msg += sizeError
    return (mark, msg)


def testST_R_01():  # removing one word from one-word tree [sample]
    toremove = ["hello"]
    words = ["hello"]
    model = "(h, 0) -> [None, (e, 0) -> [None, (l, 0) -> [None, (l, 0) -> [None, (o, 1) -> [None, None, None], None], None], None], None]"
    sol = "None"
    return removeTestST("01", words, model, toremove, sol, 0, "removing from one-word tree", 1)


def testST_R_04():  # removing all words from several word tree [sample]
    toremove = ["hello", "world"]
    words = ["hello" for i in range(5)] + ["world" for i in range(5)]
    model = "(h, 0) -> [None, (e, 0) -> [None, (l, 0) -> [None, (l, 0) -> [None, (o, 5) -> [None, None, None], None], None], None], (w, 0) -> [None, (o, 0) -> [None, (r, 0) -> [None, (l, 0) -> [None, (d, 5) -> [None, None, None], None], None], None], None]]"
    sol = "(h, 0) -> [None, (e, 0) -> [None, (l, 0) -> [None, (l, 0) -> [None, (o, 4) -> [None, None, None], None], None], None], (w, 0) -> [None, (o, 0) -> [None, (r, 0) -> [None, (l, 0) -> [None, (d, 4) -> [None, None, None], None], None], None], None]]"
    return removeTestST("04", words, model, toremove, sol, 8, "removing from several-word tree", 1)


def testST_R_20():  # remove string from no-branch ST [sample]
    toremove = ["tar"]
    words = ["tar", "target"]
    model = "(t, 0) -> [None, (a, 0) -> [None, (r, 1) -> [None, (g, 0) -> [None, (e, 0) -> [None, (t, 1) -> [None, None, None], None], None], None], None], None]"
    sol = "(t, 0) -> [None, (a, 0) -> [None, (r, 0) -> [None, (g, 0) -> [None, (e, 0) -> [None, (t, 1) -> [None, None, None], None], None], None], None], None]"
    return removeTestST("20", words, model, toremove, sol, 1, "removing from no-branch ST", 1)


removeTestsST = [testST_R_01, testST_R_04, testST_R_20]


######################################################################
# BigTree tests
######################################################################

def testBigTree():
    allTests = []

    countTestsSTList = list(zip(range(len(allTests), len(countTestsST) + len(allTests)), countTestsST))
    allTests += countTestsSTList

    incTestsSTList = list(zip(range(len(allTests), len(incTestsST) + len(allTests)), incTestsST))
    allTests += incTestsSTList

    decTestsSTList = list(zip(range(len(allTests), len(decTestsST) + len(allTests)), decTestsST))
    allTests += decTestsSTList

    removeTestsSTList = list(zip(range(len(allTests), len(removeTestsST) + len(allTests)), removeTestsST))
    allTests += removeTestsSTList

    return runTests(allTests)


# non-trivial test cases for BigTree tests
#
words15_1 = ["seca", "men", "mof", "hit", "dols", "zath", "dunt", "cofsod", "olne", "sargu", "trossy", "tam", "wesk",
             "cats", "gos"]
words30 = words15_1 + words15_1
words30Inc = words30[:];
words30Inc.sort()
words30Dec = [words30Inc[-i - 1] for i in range(len(words30Inc))]
words50_1 = ["ruotch", "art", "har", "asnu", "riply", "cusre", "knat", "talcru", "gug", "lirvinnun", "god", "droubica",
             "edent", "simmo", "bobd", "rass", "pli", "arob", "palla", "pejor", "palt", "jat", "dent", "astletwo",
             "gocl", "mutlunt", "pong", "on", "trangredlu", "bar", "back", "pim", "cast", "pralivear", "ar", "aix",
             "ehillem", "scanna", "shiffo", "cho", "dispa", "du", "reg", "foclotesh", "ratch", "sutur", "dy", "els",
             "rasuimu", "bof"]
words50_1Inc = words50_1[:];
words50_1Inc.sort()
words50_1Dec = [words50_1Inc[-i - 1] for i in range(len(words50_1Inc))]

######################################################################
# main test script
######################################################################

res = testBigTree()
print(res[2])