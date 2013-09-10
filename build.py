"""
Build the world. 
To change what is build, use construction.py

Copyright Robbert Bloem, 2013
"""

import imp

import bpy
import mathutils
import math

import materials

imp.reload(materials)


def build_laser(laser, laser_focus, material_laser_in, material_laser_out, scale_in, scale_out):
    """
    This function takes two points (one in laser and the first one of laser_focus) and calculates the position, angle and scale of the element. It is used to calculate beam paths - like it is done here. Strictly speaking, this could/should have been done in construction.py but it is here for historical reasons. It is a pretty cool function. 
    
    'in' are the incoming beams before the block
    'out' are the outgoing beam after the block
    
    INPUT
    - laser: list with starting points
    - laser_focus: list with focus, only 0th element is used
    - material_laser_in, material_laser_out: material
    - scale_in, scale_out (int/float): the size of the non-focus ends
    
    """

    # the focus, the end point
    end = laser_focus[0]["loc"]

    for l in laser:
        # the start point
        start = l["loc"]
    
        # find the rotation
        p1 = mathutils.Vector(start)
        p2 = mathutils.Vector(end)
        v = p2 - p1
        rot = v.rotation_difference(mathutils.Vector((0,0,1)))
        rot = rot.to_euler()
        rot = (rot[0], rot[1], rot[2] + math.pi)

        # find the location
        loc = [0,0,0]
        for j in range(3):
            loc[j] = (start[j] + end[j]) / 2        
        loc = (loc[0], loc[1], loc[2])
        
        # find the scale
        _d = 0
        for j in range(3):
            _d += (start[j] - end[j])**2 

        # assign material and scale
        if l["mat"] == "in":
            mat = material_laser_in
            scale = scale_in
        else:
            mat = material_laser_out
            scale = scale_out

        # make a temporary dictionary and add the primitive
        temp = {"id":l["id"],
                "shape":"cone",
                "loc":loc,
                "rot":rot,
                "scale":(scale, scale, math.sqrt(_d)/2)
            }
        add_primitive(temp, mat)



def make_proteins(proteins):
    """
    Import and place proteins
    """
    
    for p in proteins:
        # import
        bpy.ops.import_scene.x3d(filepath = p["filename"])
        # select object - this is default name
        obj = bpy.data.objects["ShapeIndexedFaceSet"]
        # give new name
        obj.name = p["id"]
        # fix geometry
        obj.location = p["loc"]
        obj.scale = p["scale"]
        if "rot" in p:
            obj.rotation_euler = p["rot"]

    # the proteins come with their own light sources, here I hide them
    # also remove the shadows of the proteins due to other lamps
    for i in range(len(proteins)):
        if i == 0:
            ex = ""
        else:
            ex = ".00" + str(i)
        bpy.data.objects["TODO" + ex].hide_render = True
        bpy.data.objects["TODO" + ex].hide = True
        # no shadows either
        bpy.data.materials["Shape" + ex].use_raytrace = False


def add_primitives(elements, material = False, loc = False, scale = False, rot = False):
    """
    General function that takes a list of primitives that have to be build and build them one by one.
    id and loc(ation) are mandatory.
    Properties can be overridden by the function call.
    Returns a list with all the element-ids so they can be boolean-combined. 
    """
    names = []
    for element in elements:
        add_primitive(element, material, loc, scale, rot)
        names += [element["id"]]
    return names


def add_primitive(p_dic, material = False, loc = False, scale = False, rot = False):
    """
    General function to make a primitive.
    p_dic is a dictionary with properties. It should contain a unique id and a loc(ation). You can also give scale and rotation. You can override the values in p_dic in the function call. 
    You can use different shapes. Some shapes have additional requirements (cylinder needs depth and radius as well). 

    """

    # add to layer 0 - no idea why
    layers = [False] * 20
    layers[0] = True

    # override location
    if not loc:
        loc = p_dic["loc"]

    # make shape
    if "shape" in p_dic:
        if p_dic["shape"] == "cylinder":
            # check if radius and depth are given
            if "radius" in p_dic and "depth" in p_dic:
                bpy.ops.mesh.primitive_cylinder_add(
                    radius = p_dic["radius"], 
                    location = loc, 
                    depth = p_dic["depth"], 
                    layers = layers,
                    end_fill_type = "TRIFAN", 
                    vertices = 40
                )
                # TRIFAN and 40 are set to make the boolean operations work properly.
        elif p_dic["shape"] == "cone":     
            bpy.ops.mesh.primitive_cone_add(
                location = loc, 
                vertices = 64,
                layers = layers
            )
        elif p_dic["shape"] == "plane":
            bpy.ops.mesh.primitive_plane_add(
                location = loc, 
                layers = layers
            )
        elif p_dic["shape"] == "cube":
            bpy.ops.mesh.primitive_cube_add(
                location = loc, 
                layers = layers
            )
    else:
        # if nothing is given, make a cube
        bpy.ops.mesh.primitive_cube_add(
            location = loc, 
            layers = layers
        )

    # select new object
    obj = bpy.context.active_object
    
    # give object name
    obj.name = p_dic["id"]
    
    # give material
    if material:
        obj.active_material = material
    
    # set scale
    if scale:  
        obj.scale = scale
    elif "scale" in p_dic:
        obj.scale = p_dic["scale"]

    # set rotation
    if rot:
        obj.rotation_euler = rot
    elif "rot" in p_dic:
        obj.rotation_euler = p_dic["rot"]
        

def boolean_modifier(name_list, operation = "UNION", hide_after_mod = True):
    """
    Take a list and do a boolean operation. This function is a bit fucked up, partially because of limitations of the Boolean operator in Blender but also because of my misunderstanding. 
    
    A boolean operator takes two objects A and B and takes the union, difference or intersect. This function ASSUMES that object A is already selected and is the last element in name_list. Objects B are the rest of the elements of the name_list. I guess there should be a better way...
        
    In other cases the result looks weird: faces are missing etc. I usually managed to solve it by changing the order of the elements (and thus changing the order of the Boolean operations). It is kind of reproducible in Blender itself, but I don't understand it.  
    """
    
    lastname = name_list[-1]
    names = name_list[:-1]
    
    for n in names:
        # add modifier
        bpy.ops.object.modifier_add(type="BOOLEAN")
        # set the operation: "UNION", "DIFFERENCE" and ""
        bpy.data.objects[lastname].modifiers["Boolean"].operation = operation
        # set the object to work on
        bpy.data.objects[lastname].modifiers["Boolean"].object = bpy.data.objects[n]
        # apply the operation
        bpy.ops.object.modifier_apply(apply_as="DATA", modifier="Boolean")
        # in some cases you want to hide the original
        if hide_after_mod:
            bpy.data.objects[n].hide_render = True
            bpy.data.objects[n].hide = True


def location_camera(camera):
    # select camera
    c = bpy.data.objects["Camera"]
    # location
    c.location = camera[0]["loc"]
    # rotation
    c.rotation_euler = camera[0]["rot"]
    # focal length
    c.data.lens = camera[0]["focus"]
    # clipping distance, don't draw beyond this range
    c.data.clip_end = camera[0]["clip_end"] 


def make_lamps(lamps):
    # make the lamps
    for l in lamps:
        
        # find the type
        if "type" in l:
            type = l["type"]
        else:
            type = "POINT"
        
        # make the lamp
        bpy.ops.object.lamp_add(type = type)
        obj = bpy.context.active_object
        obj.name = l["id"]
        
        # set location and energy (mandatory) 
        obj.location = l["loc"]
        obj.data.energy = l["energy"]

        # set color
        if "color" in l:
            obj.data.color = l["color"]
        else:
            obj.data.color = (1,1,1)
        
        # rotation
        if "rot" in l:
            obj.rotation_euler = l["rot"]
        
        # scale
        if "scale" in l:
            obj.scale = l["scale"]
        
        # the fall-off distance of the light
        if "distance" in l:
            obj.data.distance = l["distance"]

        # for SPOT, the angle of the cone, in radians
        if "spot_size" in l:
            obj.data.spot_size = l["spot_size"]

        # yes, do make shadows
        obj.data.shadow_method = "RAY_SHADOW"
        obj.data.shadow_color = (0.5, 0.5, 0.5)




