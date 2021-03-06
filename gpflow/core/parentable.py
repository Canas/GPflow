# Copyright 2017 Artem Artemev @awav
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .. import misc


class Parentable:
    """
    Very simple class for organizing GPflow objects in a tree.
    Each node contains a reference to the its parent. Links to children
    established implicitly via attributes.

    The Parentable class stores static variable which is used for assigning unique
    prefix name identificator for each newly created object inherited from Parentable.

    Name is not required at `Parentable` object creation.
    But in this case, unique index identifier will be attached to the hidden name
    (internal representation name). The index is cut off, once node is placed under
    another parent node.

    :param name: String parentable nodes name.
    """

    __index = 0

    def __init__(self, name=None):
        self._parent = None
        self._name = self._define_name(name)

    @property
    def root(self):
        """
        Top of the parentable tree.
        :return: Reference to top parentable object.
        """
        if self._parent is None:
            return self
        return self._parent.root

    @property
    def parent(self):
        """
        Parent for this node.
        :return: Reference to parent object.
        """
        if self._parent is None:
            return self
        return self._parent

    @property
    def name(self):
        """
        Assigned name for the parenable node.
        :return: String name.
        """
        name = self._name.split(sep='/', maxsplit=1)
        if len(name) > 1 and name[0].isdigit():
            return name[1]
        return self._name

    @property
    def hidden_name(self):
        """
        Fully qualified name of the parentable node. Hidden name includes
        names of parents separated by slash, e.g. 'parent0/parent1/node'.

        :return: String hidden name."""
        return self._name

    @property
    def full_name(self):
        """
        Returns full name which respresents the path from top parent to this node.
        For example, the full name with the two parents along the way back to
        the top may look like `parent0/parent1/node`.
        """
        if self._parent is None:
            return self.name
        return misc.tensor_name(self._parent.full_name, self.name)

    @property
    def hidden_full_name(self):
        """
        Returns `full_name` with unique identification prefix, `1/parent0/parent1/node`,
        if such was used.
        """
        if self._parent is None:
            return self._name
        return misc.tensor_name(self._parent.hidden_full_name, self.name)

    def set_name(self, name=None):
        self._name = self._define_name(name)

    def set_parent(self, parent=None):
        self._parent = parent

    def _reset_name(self):
        if self.hidden_name != self.name:
            self._name = self._define_name(None)

    def _define_name(self, name):
        if name:
            return name
        cls_name = self.__class__.__name__
        index = Parentable._read_index(self)
        return '{index}/{name}'.format(index=index, name=cls_name)

    @classmethod
    def _read_index(cls, obj=None):
        """
        Reads index number and increments it.

        # TODO(@awav): index can grow indefinetly,
        # check boundaries or make another solution.
        """
        index = cls.__index
        cls.__index += 1
        return index
