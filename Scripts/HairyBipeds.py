"""Reuse the reviewed primate constructor with independent hairy-biped dimensions."""
import PrimateFamily as family
SPECS={
 'yeti':dict(h=1.43,head=.145,shoulder=.235,hip=.132,arm=.075,face=.065,pose=1),
 'sasquatch':dict(h=1.57,head=.145,shoulder=.240,hip=.140,arm=.080,face=.080,pose=1)}
def build(key):
 family.SPECS.update(SPECS)
 family.build(key)
