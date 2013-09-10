"""
Define materials and textures. 

Copyright Robbert Bloem, 2013
"""

import bpy
import os

def material_laser(out = False):
    """
    Material for the laser pulse. 'in' is before the block, 'out' is after the block.
    I don't think there is a difference anymore.
    """

    mat = bpy.data.materials.new("mat_laser")
    mat.type = "SURFACE"
    mat.use_transparency = True
    if out:
        mat.alpha = 0.5 
    else:
        mat.alpha = 0.5

    mat.use_raytrace = False
    mat.diffuse_color = (1,0,0)
    mat.diffuse_intensity = 1
 
    return mat


def material_plot(resources_path, transparent = False): 
    """
    Material with plot as texture.
    """
    
    # material
    mat = bpy.data.materials.new("mat_plot")
    
    if transparent:
        path = resources_path + "plot_transparent.png"
    else:
        path = resources_path + "plot_white.png"

    mat.type = "SURFACE"
    mat.diffuse_intensity = 1
    mat.specular_intensity = 0

    mat.use_transparency = True
    if transparent:
        mat.alpha = 0
    else:
        mat.alpha = 0.8
    
    # make texture
    tex = bpy.data.textures.new(name="tex_plot", type='IMAGE')
    
    # for the material, create a new texture slot
    slot = mat.texture_slots.add()
    
    # set the texture
    slot.texture = tex
    
    # load the image and add to the texture
    img = bpy.data.images.load(path)
    slot.texture.image = img
    
    # set some properties
    mat.texture_slots[0].use_map_alpha = True
    mat.texture_slots[0].alpha_factor = 0.5
    
    # no need to return the texture, it is part of the material
    return mat


def material_block():
    """
    Brushed metal look.
    """
    
    # material
    mat = bpy.data.materials.new("mat_block")
    mat.type = "SURFACE"
    mat.diffuse_color = (0.2, 0.2, 0.2)
    mat.alpha = 0.5   
    mat.raytrace_mirror.use = True
    mat.raytrace_mirror.reflect_factor = 0.3
    
    # make it brushed
    tex = bpy.data.textures.new(name="tex_block", type='STUCCI')
    tex.stucci_type = "WALL_IN"
    slot = mat.texture_slots.add()
    slot.texture = tex    
    slot.color = (0,0,0)
    slot.diffuse_color_factor = 0.75
    slot.scale = (1,1,20)
    
    return mat


def material_blue_water():
    return material_water((0,0,1))

def material_green_water():
    return material_water((0.35,1,0.35))

def material_water(color):
    """
    Well... water... it is transparent and it has a color
    """
    
    mat = bpy.data.materials.new("mat_water")
    mat.type = "SURFACE"
    mat.alpha = 0.5
    mat.diffuse_color = color 
    mat.diffuse_intensity = 1
    mat.diffuse_shader = "LAMBERT"
    mat.use_transparency = True
    mat.specular_alpha = 0.5 
    mat.specular_color = color 
    mat.specular_intensity = 0
    mat.specular_shader = "PHONG"
    mat.specular_hardness = 75
    mat.raytrace_mirror.use = True
    mat.raytrace_mirror.reflect_factor = 0.0
    mat.mirror_color = color 
    mat.raytrace_mirror.depth = 20
    mat.raytrace_mirror.distance = 20
    mat.raytrace_mirror.gloss_factor = 1
    mat.raytrace_mirror.fresnel = 0.75
    mat.raytrace_mirror.fresnel_factor = 1
    return mat 


def make_gold_material():
    """
    Shiny!
    """
    mat = bpy.data.materials.new("mat_gold")
    mat.type = "SURFACE"
    mat.alpha = 0.25
    mat.diffuse_color = (1.0,0.8,0.2)
    mat.diffuse_intensity = 1
    mat.diffuse_shader = "LAMBERT"
    mat.specular_color = (1.0,1.0,1.0)
    mat.specular_intensity = 1
    mat.specular_shader = "PHONG"
    mat.specular_hardness = 75
    mat.raytrace_mirror.use = True
    mat.raytrace_mirror.reflect_factor = 0.75
    mat.mirror_color = (1.0,0.8,0.2)
    mat.raytrace_mirror.depth = 100
    mat.raytrace_mirror.distance = 75
    mat.raytrace_mirror.gloss_factor = 1
    mat.raytrace_mirror.fresnel = 0.75
    mat.raytrace_mirror.fresnel_factor = 1
    mat.raytrace_mirror.fade_to = "FADE_TO_MATERIAL"
    return mat


def make_mirror_mount_material():
    # shiny dark grey
    mat = bpy.data.materials.new("mat_mirror_mount")
    mat.type = "SURFACE"
    mat.diffuse_color = (0.2, 0.2, 0.2)
    mat.alpha = 0.5   
    mat.raytrace_mirror.use = True
    mat.raytrace_mirror.reflect_factor = 0.3
    return mat
  

def make_beamblock_material():
    # mat black
    mat = bpy.data.materials.new("mat_beam_block")
    mat.type = "SURFACE"
    mat.diffuse_color = (0.01,0.01,0.01)#
    mat.specular_intensity = 0.01
    mat.alpha = 0.5   
    mat.raytrace_mirror.use = False
    return mat


def material_white_plane():
    mat = bpy.data.materials.new("mat_white_plane")
    mat.type = "SURFACE"
    mat.diffuse_color = (1,1,1)
    mat.specular_intensity = 0.1
    mat.alpha = 0
    mat.raytrace_mirror.use = False
    return mat

### NOT USED, I THINK ###

def make_laserpulse_material():
    # red halo
    mat_light = bpy.data.materials.new("laser_light")
    mat_light.type = "HALO"
    mat_light.alpha = 0.25
    mat_light.diffuse_color = (1,0,0)
    mat_light.halo.size = 0.5#1
    mat_light.halo.add = 0.5
    mat_light.halo.hardness = 100
    return mat_light


def make_signalpulse_material():
    # red halo
    mat_light = bpy.data.materials.new("laser_light")
    mat_light.type = "HALO"
    mat_light.alpha = 0.01
    mat_light.diffuse_color = (1,0,0)
    mat_light.halo.size = 0.5#1
    mat_light.halo.add = 0.5
    mat_light.halo.hardness = 100
    return mat_light


def make_signal(loc, rot, scale, color):
    bpy.ops.mesh.primitive_cylinder_add(location=loc, rotation=rot)
    pulse = bpy.context.active_object
    pulse.active_material = make_signalpulse_material() 
    return pulse


def make_laserpulse():
    bpy.ops.mesh.primitive_uv_sphere_add()
    pulse = bpy.context.active_object
    pulse.active_material = make_laserpulse_material()  
    bpy.ops.object.lamp_add(type="POINT")
    pulse_light = bpy.context.active_object
    pulse_light.data.color = (1,0,0)
    return pulse, pulse_light


def make_signalpulse():
    bpy.ops.mesh.primitive_uv_sphere_add()
    pulse = bpy.context.active_object
    pulse.active_material = make_signalpulse_material()  
    return pulse


def make_path_material():
    # whitish
    mat_path = bpy.data.materials.new("beam_path")
    mat_path.type = "SURFACE"
    mat_path.alpha = 0.25
    mat_path.diffuse_color = (0.8,0.8,0.8)
    return mat_path
    
    
def make_beamsplitter_material():
    # beam splitter
    mat_glass = bpy.data.materials.new("glass")
    mat_glass.type = "SURFACE"
    mat_glass.alpha = 0.5
    mat_glass.diffuse_color = (0.9,1,0.8) #1,1,1)
    mat_glass.diffuse_intensity = 1
    mat_glass.diffuse_shader = "LAMBERT"
    mat_glass.use_transparency = True
    mat_glass.specular_color = (1.0,1.0,1.0)
    mat_glass.specular_intensity = 1
    mat_glass.specular_shader = "PHONG"
    mat_glass.specular_hardness = 75
    mat_glass.raytrace_mirror.use = True
    mat_glass.raytrace_mirror.reflect_factor = 0.5
    mat_glass.mirror_color = (1,1,1)
    mat_glass.raytrace_mirror.depth = 20
    mat_glass.raytrace_mirror.distance = 20
    mat_glass.raytrace_mirror.gloss_factor = 1
    mat_glass.raytrace_mirror.fresnel = 0.75
    mat_glass.raytrace_mirror.fresnel_factor = 1
    return mat_glass 

def make_glass_material():
    # beam splitter
    mat_glass = bpy.data.materials.new("glass")
    mat_glass.type = "SURFACE"
    mat_glass.alpha = 0.1
    mat_glass.diffuse_color = (0.6,1,0.6)#(1,1,1)
    mat_glass.diffuse_intensity = 1
    mat_glass.diffuse_shader = "LAMBERT"
    mat_glass.use_transparency = True
    mat_glass.specular_color = (1.0,1.0,1.0)
    mat_glass.specular_intensity = 1
    mat_glass.specular_shader = "PHONG"
    mat_glass.specular_hardness = 75
    mat_glass.raytrace_mirror.use = True
    mat_glass.raytrace_mirror.reflect_factor = 0.5
    mat_glass.mirror_color = (1,1,1)
    mat_glass.raytrace_mirror.depth = 20
    mat_glass.raytrace_mirror.distance = 20
    mat_glass.raytrace_mirror.gloss_factor = 1
    mat_glass.raytrace_mirror.fresnel = 0.75
    mat_glass.raytrace_mirror.fresnel_factor = 1
    return mat_glass 


def make_box_surface_material():
    # shiny grey
    mat = bpy.data.materials.new("box_surface")
    mat.type = "SURFACE"
    mat.alpha = 0.5   
    mat.raytrace_mirror.use = True
    mat.raytrace_mirror.reflect_factor = 0.3
    mat.specular_intensity = 0.1
    return mat

    
def make_wall_surface_material():
    # shiny black
    mat = bpy.data.materials.new("wall_surface")
    mat.type = "SURFACE"
    mat.diffuse_color = (0.01,0.01,0.01)
    mat.use_transparency = False
    mat.alpha = 0.25   
    mat.raytrace_mirror.use = True
    mat.raytrace_mirror.reflect_factor = 0.05
    mat.specular_intensity = 0.1
    return mat


def make_laserpulse_material_too_new():
    # red halo
    mat_light = bpy.data.materials.new("laser_light")
    mat_light.type = "VOLUME"
    mat_light.volume.density = 0.5
    mat_light.volume.scattering = 0.25
    mat_light.volume.asymmetry = 0.75
    mat_light.volume.emission_color = (1,0,0)
    mat_light.volume.reflection_color = (1,0,0)
    mat_light.volume.transmission_color = (1,0,0)
    mat_light.volume.emission = 1
    mat_light.volume.reflection = 25
    return mat_light


def make_signalpulse_material_original():
    # red halo
    mat_light = bpy.data.materials.new("laser_light")
    mat_light.type = "HALO"
    mat_light.alpha = 0.1
    mat_light.diffuse_color = (1,0,0)
    mat_light.halo.size = 0.5#1
    mat_light.halo.add = 0.5
    mat_light.halo.hardness = 50
    return mat_light