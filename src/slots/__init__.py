#!/usr/bin/python
# -*- coding: utf-8 -*-
from rasa_core.slots import Slot


class MandantSlot(Slot):

    def feature_dimensionality(self):
        # Three states: None, Even, Odd
        return 2

    def as_feature(self):
        r = [0.0] * self.feature_dimensionality()
        if self.value:
            if self.value % 2 == 0:
                r[0] = 1.0
            else:
                r[1] = 1.0
        return r
