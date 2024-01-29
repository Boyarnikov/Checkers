class abc:
    def met1(self):
        pass

    def met2(self):
        pass


our_list = []

x = 5
if x == 5:
    our_list.append(abc())
else:
    our_list.append(3)


def iteration(elem: abc):
    elem.met1()


for elem in our_list:
    iteration(elem)