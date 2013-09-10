"""
This file contains the definitions (location, scale etc) for the elements.
Each function defines something specific, although sometimes I combined related items. 
Each list [] contains a dictionary {} for each element. The dictionary contains the properties for one element. Each element needs a UNIQUE id. Usually the location is also needed. 
Angles are always in radians, not degrees. Use the function deg2rad() to convert from degrees to radians.

Copyright Robbert Bloem, 2013
"""

import math

def deg2rad(deg):
    """
    Function to convert degrees to radians
    """
    return (deg / 180) * math.pi


def define_laser(focus_location, plot_loc):
    """
    Defines the laser beams. 
    - The beams focus at focus_location. One beam will end at plot_loc. The other beams will be calculated from that, separated by diff. 
    - Normally, the beams would be just long enough to go from focus_location to plot_loc, this can be extended by factor. 
    - pulse2out will go to the plot. To make sure it doesn't extend to far, the factor is removed. Then, to make sure it does reach the plot, it is extended by 1.15
    - some pulses are commented out
    
    """

    # determine the positions
    factor = 2
    diff = 20

    flx = focus_location[0]
    fly = focus_location[1]
    flz = focus_location[2]

    dx1 = factor * (plot_loc[0] + 0 - flx)
    dx2 = factor * (plot_loc[0] - diff - flx)
    
    dz1 = factor * (plot_loc[2] + diff - flz)
    dz2 = factor * (plot_loc[2] - 0 - flz)

    dy = factor * plot_loc[1]

    # list with dictionaries
    laser = [
        {"id":"pulse1in", "loc":(flx - dx1, fly - dy, flz - dz1), "mat":"in"},
        {"id":"pulse2in", "loc":(flx - dx1, fly - dy, flz - dz2), "mat":"in"},
#        {"id":"pulse3in", "loc":(flx - dx2, fly - dy, flz - dz1), "mat":"in"},
#        {"id":"pulse4in", "loc":(flx - dx2, fly - dy, flz - dz2), "mat":"in"},
        {"id":"pulse2out", "loc":(flx + 1.15*dx1/factor, fly + 1.15*dy/factor, flz + 1.15*dz2/factor), "mat":"out"},
#        {"id":"pulse1out", "loc":(flx + dx1, fly + dy, flz + dz1), "mat":"out"},
#        {"id":"pulse3out", "loc":(flx + dx2, fly + dy, flz + dz1), "mat":"out"},
#        {"id":"pulse4out", "loc":(flx + dx2, fly + dy, flz + dz2), "mat":"out"},        
    ]
    return laser   

 
def define_laser_focus(focus_location):
    """
    Set the location of the focus. 
    """
    laser = [
        {"id":"laser_focus", "loc":focus_location},
    ]
    return laser   


def define_proteins(y_offset, resources_path):

    # scale of the proteins
    scale = 0.15

    # filenames, location, scale
    proteins = [
#        {"id":"prot1", 
#            "filename":resources_path + "prot1.wrl",            
#            "loc":(1,y_offset,0), 
#            "scale":(scale, scale, scale), 
#            "rot":(deg2rad(-90),deg2rad(90),deg2rad(180))},
        {"id":"prot2", 
            "filename":resources_path + "prot2.wrl", 
            "loc":(15.5,y_offset,0), 
            "scale":(scale, scale, scale), 
            "rot":(deg2rad(-90),deg2rad(90),deg2rad(180))},
#        {"id":"prot3", 
#            "filename":resources_path + "prot3.wrl", 
#            "loc":(25,y_offset-1,0), 
#            "scale":(scale, scale, scale), 
#            "rot":(deg2rad(-85),deg2rad(50),deg2rad(180))},
#        {"id":"pep1", 
#            "filename":resources_path + "lig1.wrl", 
#            "loc":(6,y_offset+1,5), 
#            "scale":(scale, scale, scale), 
#            "rot":(deg2rad(-90),deg2rad(90),deg2rad(180))},
#        {"id":"pep2", 
#            "filename":resources_path + "lig2.wrl", 
#            "loc":(6,y_offset+0.5,-5), 
#            "scale":(scale, scale, scale), 
#            "rot":(deg2rad(-90),deg2rad(90),deg2rad(180))}
    ]
    return proteins


def define_block(y_scale = 1, x_offset = -1):
    """
    Define the block
    """
    # make the block slightly bigger so that surfaces of blue and green channel channel are well hidden. 
    y_scale *= 1.01

    # needs a special order for the boolean operator to work
    block = [
        {"id":"block_2m", 
            "loc":(10.5 + x_offset, 0, -5), 
            "scale":(0.5, y_scale, 4)},
        {"id":"block_3m", 
            "loc":(22 + x_offset, 0, -7), 
            "scale":(11.05, y_scale, 2)},
        {"id":"block_4m", 
            "rot":(0, -deg2rad(10), 0), 
            "loc":(11 + x_offset, 0, -4), 
            "scale":(0.5, y_scale, 3)},
        {"id":"block_1", 
            "loc":(2 + x_offset, 0, 6), 
            "scale":(4,y_scale,3)},
        {"id":"block_2", 
            "loc":(10.5 + x_offset, 0, 5), 
            "scale":(0.5, y_scale, 4)},
        {"id":"block_3", 
            "loc":(22 + x_offset, 0, 7), 
            "scale":(11.05, y_scale, 2)},
        {"id":"block_4", 
            "rot":(0, deg2rad(10), 0), 
            "loc":(11 + x_offset, 0, 4), 
            "scale":(0.5, y_scale, 3)},
        {"id":"block_1m", 
            "loc":(2 + x_offset, 0, -6), 
            "scale":(4,y_scale,3)},
    ]
    return block
    

def define_blue_channel(y_scale = 1, x_offset = -1):
    # the blue channel is one big block
    blue = [
        {"id":"blue_1", 
            "loc":(15.5 + x_offset, 0, 0), 
            "scale":(17.49, 0.99 * y_scale, 3)},
    ]
    return blue

def define_green_channel(y_scale = 1, x_offset = -1):
    # the green channel is a composite
    # needs a special order for the boolean operator to work
    green = [
        {"id":"green_1m", 
            "loc":(8 + x_offset, 0, -6), 
            "scale":(2, y_scale, 3)},
        {"id":"green_1", 
            "loc":(8 + x_offset, 0, 6), 
            "scale":(2, y_scale, 3)},
        {"id":"green_3m", 
            "loc":(21.5 + x_offset, 0, -3.5), 
            "scale":(11.5, y_scale, 3)},
        {"id":"green_3", 
            "loc":(21.5 + x_offset, 0, 3.5), 
            "scale":(11.5, y_scale, 3)},
        {"id":"green_2", 
            "shape":"cylinder", 
            "radius":2, 
            "depth":1, 
            "rot":(deg2rad(90), 0, 0), 
            "loc":(10 + x_offset, 0, 3), 
            "scale":(2, 1.25, 2 * y_scale)},
        {"id":"green_2m", 
            "shape":"cylinder", 
            "radius":2, 
            "depth":2, 
            "rot":(deg2rad(90), 0, 0), 
            "loc":(10 + x_offset, 0, -3), 
            "scale":(2, 1.25, y_scale)},  
    ]
    return green


def define_plot_plane(loc, scale):
    """
    Where the plot is going to be plotted.
    """
    plot_plane = [
        {"id":"plotplane", 
            "shape":"plane", 
            "loc":loc, 
            "rot":(deg2rad(90), 0, 0), 
            "scale":(scale, scale, 1)},  
    ]
    return plot_plane


def define_camera():
    # location and angle of camera
    camera = [
        {"id":"camera", "rot":(deg2rad(75), 0, deg2rad(20)), "loc":(50, -72, 21), "focus":55, "clip_end":200}
    ]
    return camera
    
    
def define_lamps():
    y = 35
    z = 50
    lamps = [
        {"id":"lamp1", 
            "loc":(25,-35,z), 
            "energy":50, 
            "distance":40},
        {"id":"lamp3", 
            "type":"SPOT", 
            "loc":(16,1.1,-0.5), 
            "energy":100, 
            "rot":(deg2rad(83), 0, deg2rad(-20)), 
            "scale":(3,3,1), 
            "spot_size":deg2rad(45), 
            "color":(1,0.9,0.9)},     
    ]
    return lamps
  

def define_mirror(plot_loc, plot_scale):
    """
    Defines the mirror. It is centered at plot_loc and has radius plot_scale.
    Be careful with the rotation, it will affect the positions of the other elements. 
    This function is not used anymore.
    """
    mirror = [
        {"id":"mirror", 
            "loc":plot_loc, 
            "radius":plot_scale, 
            "shape":"cylinder", 
            "depth":2, 
            "mat":"gold", 
            "rot":(deg2rad(90),0,0)}
    ]
    black = [
        {"id":"black", 
            "loc":(plot_loc[0], plot_loc[1]+1, plot_loc[2]), 
            "radius":1.01 * plot_scale, 
            "shape":"cylinder", 
            "depth":2, 
            "mat":"black", 
            "rot":(deg2rad(90),0,0)},
    ]
    plot = [
        {"id":"plot", 
            "loc":(plot_loc[0], plot_loc[1]-1.01, plot_loc[2]), 
            "radius":plot_scale, 
            "shape":"cylinder", 
            "depth":0.01, 
            "mat":"black", 
            "rot":(deg2rad(90),0,0)},
    ]
    mirror_mount_height = 20
    mirror_mount = [
        {"id":"mirror_mount", 
            "loc":(plot_loc[0], plot_loc[1]+2, plot_loc[2] - mirror_mount_height), 
            "scale":(1,1,mirror_mount_height)},
    ]
 
    return mirror, black, plot, mirror_mount



    