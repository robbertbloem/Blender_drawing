"""
The glue between the other files.

Copyright Robbert Bloem, 2013
"""


# system
import imp
import math
import os

# blender
import bpy
import mathutils

# mine
import materials
import construction
import build

# reload to make sure we run the latest version
imp.reload(materials)
imp.reload(construction)
imp.reload(build)


### FLAGS ###

# put the plot on a mirror instead of a plane
# aesthetic choice
flag_use_mirror_instead_of_plane = True

# do not plot the proteins
# speeds up the drawing dramatically - use when testing
flag_no_proteins = False

# transparent background
flag_transparent_background = False

# size of the non-focus end of the laser beams
laser_scale_in = 2
laser_scale_out = 9

# switches between two resources
flag_use_alternate_resources = True


### GENERAL PROPERTIES ###

# thickness of the block and channels
y_scale = 1

# offset of the protein (so it sticks out more)
# negative is more to the front
protein_y_offset = -1

# location and scale for the plot
plot_loc = (31, 40, -6)
plot_scale = 10

# where do the beams focus?
# a little bit before the actual middle of the protein
focus_location = (15, protein_y_offset-1, 0)


### WORLD/RENDER PROPERTIES ###

# world
bpy.data.worlds["World"].horizon_color = (0.8,0.8,0.8)
bpy.data.worlds["World"].zenith_color = (0.5,0.5,0.5)
bpy.data.worlds["World"].exposure = 0.1
bpy.data.worlds["World"].use_sky_blend = True

# rendering size
# this is not the same as changing the focal length of the camera
bpy.context.scene.render.resolution_x = 1000 
bpy.context.scene.render.resolution_y = 400 
bpy.context.scene.render.resolution_percentage = 100

# high quality anti aliasing
bpy.context.scene.render.antialiasing_samples = "16"
bpy.context.scene.render.use_full_sample = True

# if you want a transparent background, do not render the sky. Also set to save the image with an alpha channel. 
if flag_transparent_background:
    bpy.context.scene.render.layers["RenderLayer"].use_sky = False
    bpy.data.scenes["Scene"].render.image_settings.color_mode = "RGBA"

# find the correct resource folder
path = os.path.dirname(bpy.data.filepath)
if flag_use_alternate_resources:
    resources_path = path + "/res_alt/"
else:   
    resources_path = path + "/res/"


### MAKE STUFF ###

# block
block = construction.define_block(
    y_scale = y_scale
)
block_material = materials.material_block() 
name_list = build.add_primitives(
    block, 
    block_material
)
build.boolean_modifier(
    name_list, 
    operation = "UNION"
)

# green channel
green_channel = construction.define_green_channel(
    y_scale = y_scale
)
green_channel_material = materials.material_green_water()
name_list = build.add_primitives(
    green_channel, 
    green_channel_material
)
build.boolean_modifier(
    name_list, 
    operation = "UNION"
)

# blue channel
blue_channel = construction.define_blue_channel(
    y_scale = y_scale
)
blue_channel_material = materials.material_blue_water()
name_list = build.add_primitives(
    blue_channel, 
    blue_channel_material
)
build.boolean_modifier(
    ["green_2m", "block_1m", "blue_1"], 
    operation = "DIFFERENCE", 
    hide_after_mod = False
)

# the plot
if flag_use_mirror_instead_of_plane:
    # mirror
    material_plot = materials.material_plot(
        transparent = True, 
        resources_path = resources_path
    )
    material_black = materials.make_beamblock_material()
    material_gold = materials.make_gold_material()
    material_mirror_mount = materials.make_mirror_mount_material()
    mirror, black, plot, mirror_mount = construction.define_mirror(
        plot_loc = (plot_loc[0]+2, plot_loc[1], plot_loc[2]), 
        plot_scale = plot_scale
    )
    name_list = build.add_primitives(
        mirror, 
        material_gold
    )
    name_list = build.add_primitives(
        plot, 
        material_plot
    )
    name_list = build.add_primitives(
        black, 
        material_black
    )
    name_list = build.add_primitives(
        mirror_mount, 
        material_mirror_mount
    )
else:
    # plane
    material_plot = materials.material_plot(
        resources_path = resources_path
    )
    plot_plane = construction.define_plot_plane(
        loc = (plot_loc[0]+2, plot_loc[1], plot_loc[2]), 
        scale = plot_scale
    )
    name_list = build.add_primitives(
        plot_plane, 
        material = material_plot
    )

# laser pulses
material_laser_in = materials.material_laser(
    out = False
)
material_laser_out = materials.material_laser(
    out = True
)
laser_focus = construction.define_laser_focus(
    focus_location = focus_location
)
laser = construction.define_laser(
    focus_location = focus_location, 
    plot_loc = plot_loc
)
build.build_laser(
    laser = laser, 
    laser_focus = laser_focus, 
    material_laser_in = material_laser_in, 
    material_laser_out = material_laser_out, 
    scale_in = laser_scale_in, 
    scale_out = laser_scale_out
)

# proteins
if not flag_no_proteins:
    proteins = construction.define_proteins(
        y_offset = protein_y_offset,
        resources_path = resources_path
    )
    build.make_proteins(
        proteins = proteins
    )


### POSITION CAMERAS AND LAMPS ###

# camera properties
camera = construction.define_camera()
build.location_camera(
    camera
)

# lamp properties
lamps = construction.define_lamps()
build.make_lamps(
    lamps
)

