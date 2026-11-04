"""Source-supported wooden club held by the yeti's right hand."""
import bpy,math
import CreatureGeometry as g
from PrimateFamily import limb
from mathutils import Vector
def add_club():
 g.GROUP='yeti';color=(.40,.12,.018);g.COLORS['club_wood']=color
 mat=bpy.data.materials.get('club_wood') or bpy.data.materials.new('club_wood');mat.use_nodes=True;g.MATS['club_wood']=mat
 mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.88
 # One straight metre-long axis, leaning away from the forearm; broad head above.
 start=Vector((-.14,-.27,.15));axis=Vector((.04,-.26,1.0))
 club=limb('wooden_club',[start+axis*t for t in [0,.10,.28,.62,.83,.94,1.0]],[.024,.026,.032,.060,.110,.105,.065],'club_wood')
 club['held_club']=True;club['grip_center']=list(start+axis*.10)
 club['straight_axis']=list(axis);club['club_length_m']=axis.length
 return club
