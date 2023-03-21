#!/usr/bin/env python3
import time
import py_trees
from py_trees.behaviour import Behaviour
from py_trees.common import Status
from enum import Enum


class ChangeLaneBehavior(Behaviour):
    """Change lane behavior"""

    def __init__(self, direction: str, name="ChangeLaneBehavior"):
        super(ChangeLaneBehavior, self).__init__(name)

    def setup(self, timeout):
        print("setup")
        return True

    def initialise(self):
        print("initialise")

    def update(self):
        # check safe to change lane
        if True:
            # if safe, change lane
            return Status.SUCCESS
            # else, return running and wait
            return Status.RUNNING

    def terminate(self, new_status):
        print("terminate")


class ThrottleBehavior(Behaviour):
    """Change throttle value"""

    def __init__(self, val: float, name="ThrottleBehavior"):
        super(ThrottleBehavior, self).__init__(name)

    def update(self):
        # set acc value
        return Status.SUCCESS


class GoodToMerge(Behaviour):
    """Check if good to merge"""

    def __init__(self, direction: str, name="GoodToMerge"):
        super(GoodToMerge, self).__init__(name)

    def update(self):
        if True:  # check if good to merge
            return Status.SUCCESS
        else:
            return Status.FAILURE


if __name__ == "__main__":
    root = py_trees.composites.Sequence(name="passing", memory=True)
    root.add_child(ChangeLaneBehavior("right"))
    root.add_child(GoodToMerge("right"))
    root.add_child(ThrottleBehavior(val=0.1))
    root.add_child(ChangeLaneBehavior("left"))
    root.add_child(GoodToMerge("left"))

    for i in range(1, 5):
        try:
            print("\n--------- Tick {0} ---------\n".format(i))
            root.tick_once()
            print("\n")
            print(py_trees.display.unicode_tree(root=root, show_status=True))
            time.sleep(1.0)
        except KeyboardInterrupt:
            break
    print("\n")
