INTRODUCTION
------------

I have done some really cool things with Python scripting in Blender, but when I was stuck with something I found it difficult to find the solution. The information on the internet is either outdated or not complete. This package contains all the material to make this cool figure and I used plenty of comments -- I hope it is useful to others.

The scripts make the complete figure, you only have to load and run the script and press "render". It includes:
- Making primitives
- Calculating the location, rotation and scale of a primitive between two points
- Using Boolean operators
- Making materials and textures, including textures from external images
- Importing and showing PyMol proteins (see http://pymolwiki.org/index.php/Blender for instructions how to make the protein file)
- Camera and lamp location, rotation and other properties
- Manipulating world and rendering properties

Earlier, I used similar scripts to make an animation. This partially explains some of the awkwardness of the scripts (the use of run.py as glue between other files). I hope to post the code of the animation as well, at some point in the future. 

The figure was made using Blender 2.66.1 on Mac OS X 10.8.4.

I made the figure for a colleague. It doesn't matter what it really represents, but there are some laser beams involved, a protein in a sample holder and a plot. It is not secret or anything, but I would appreciate it if there is no speculation about what it really is. The public version of this package has alternate resources (figure and protein file) to reduce the file size. 

I would like to thank the Blender community for all their support. 

-- Robbert Bloem, 10 September, 2013


INSTRUCTIONS
------------

First, set up Blender:
1. Open a new Blender file 
2. Delete the Cube and the Lamp that are present
3. Select Text Editor in one of the panes. I use the one below the Viewport
4. In the Text Editor pane, select Text > Open Text Block
5. Select master.py
6. In the Viewport, select View > Camera
7. Save as a Blender file

This sets up the environment so you can easily iterate your work. My workflow is usually as follows:
1. With the mouse pointer in NOT in the Text Editor pane, click cmd-o and select the Blender file you saved. 
2. With the mouse pointer in the Text Editor pane, click option-p to run the master file. 
3. Do stuff
4. Make changes in the scripts
5. Go back to 1

Ad 3:
- Render the scene
- Teposition stuff

Ad 4:
- You should only make changes in construction.py, materials.py and run.py
- build.py has some general build functions and should be left alone as much as possible
- master.py is only there to make the cmd-o alt-p trick possible

construction.py contains functions that give the information for a certain part of the construction, for example the green channel. It exports a list with dictionaries. The list contains all the individual elements, for example the separate parts of the block. The dictionary contains has an id (which has to be unique) and a loc(ation). It can also contain rot(ation), scale, shape and some other stuff. In some cases the lists are customized for lamps, cameras etc. 

materials.py contains all the materials and textures.

run.py is the glue of the operation. Usually it first calls a function in construction.py, then it calls a material from materials.py and then it calls a function in build.py. This is separated so that materials can be reused. 
Options in run.py:
- flag_no_proteins: don't draw the proteins. This speeds up the loading and is useful for testing.
- flag_use_alternate_resources: the public version has different and less resources to keep the size of the package smaller. 

build.py builds the construction. There are some more and some less general functions. 
