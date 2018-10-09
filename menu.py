#Import stuff
import nuke
import rendercameraDot
import rendercameraDotChild
import W_hotbox, W_hotboxManager
import pixelfudger
##

#QuickCreate
import h_viewerShortcuts
import channel_hotbox
#import W_scaleTree


#Define stuff

#
def reloadRead(x):
    for i in x:
	if i.Class() == 'Read':
            nuke.Script_Knob.execute(i.knob('reload'))

#
def setLabel():

    '''Quick edit the label for the selected node'''

    noted = 0

    try:
        sn = nuke.selectedNodes()[-1]
        snLabel = sn['label'].value()
        snName = sn.name()
    except:
        sn = None
        return

    p = nuke.Panel( 'Edit Label' )
    p.setTitle( 'Edit label for %s' % snName )
    p.setWidth( 350 )
    p.addNotepad('Label', snLabel)
    result = p.show()

    if result:
        label = p.value('Label')
        try:

            sn['label'].setValue(label)
	    sn['note_font_size'].setValue(15)
	    sn['note_font_color'].setValue(1509949439)
	    noted = 1
        except:
            return
    snf = nuke.selectedNodes()
    for i in snf:
        i['label'].setValue(label)
        i['note_font_size'].setValue(15)
        i['note_font_color'].setValue(1509949439)

#
def framestep(default=0):

    nuke.activeViewer().frameControl(default)

#
def zoomLabel(x):
    for x in x:
        x['note_font_size'].setValue(x['note_font_size'].getValue() + 10)

def unZoomLabel(x):
    for x in x:
        x['note_font_size'].setValue(x['note_font_size'].getValue() - 10)

#
def getScreenSize(node,axis):
    if axis == 'x':
        return node.screenWidth()/2
    else:
        return node.screenHeight()/2

#
def distributeEvenly(axis):
    '''
    Equalize the amount of space between selected nodes.
    '''

    selection = nuke.selectedNodes()

    allPositionsDict = {}

    for node in selection:

        position = float(node.knob(axis+'pos').value() + getScreenSize(node,axis))

        if position in allPositionsDict.keys():
            allPositionsDict[position].append(node)
        else:
            allPositionsDict[position] = [node]

    allPositions = sorted(allPositionsDict.keys())

    amount = len(allPositions)
    if amount < 3:
        return

    minPos = allPositions[0]
    maxPos = allPositions[-1]

    stepSize = (maxPos - minPos) / (amount -1)

    undo = nuke.Undo()
    undo.name("Distribute evenly")
    undo.begin()

    for index, i in enumerate(allPositions):
        newPos = minPos + index * stepSize
        for node in allPositionsDict[i]:

            node.knob(axis+'pos').setValue( newPos- getScreenSize(node,axis))

    undo.end()

## PYTHON

def clear_flat(knob):
   if knob.hasExpression(): return
   if not knob.isAnimated(): return

   for n in range(99):
       if knob.animation(n) and knob.animation(n).constant():
           knob.clearAnimated(n)


def clear_flat_menucmd():
   for node in nuke.selectedNodes():
       for k in node.knobs().values():
           clear_flat(k)

nuke.menu("Nuke").addCommand("Utils/Clear non-animated", clear_flat_menucmd)

#Add Hotkeys
m=nuke.menu('Nuke')
n=m.addMenu('User')
v=nuke.menu('Viewer')
v.addCommand("Step forward", 'framestep(1)', 'f2')
v.addCommand("Step backward", 'framestep(-1)','f1')
n.addCommand("Step forward", 'framestep(1)', 'f2')
n.addCommand("Step backward", 'framestep(-1)','f1')
n.addCommand('misc/rendercameradot', 'rendercameraDot.motherDot()', '')
n.addCommand('misc/rendercamerachild', 'rendercameraDotChild.childDot()', 'Alt+8')
n.addCommand( 'setLabel', "setLabel()", 'shift+d')
n.addCommand( 'zoomLabel', "zoomLabel(nuke.selectedNodes())", 'ctrl+shift+a')
n.addCommand( 'unZoomLabel', "unZoomLabel(nuke.selectedNodes())", 'ctrl+shift+alt+a')
n.addCommand( 'reloadRead', "reloadRead(nuke.selectedNodes())", 'shift+t')
#
n.addCommand('Edit/Node/Align/horizontally', 'alignNodes.alignNodes( nuke.selectedNodes(), direction="x" )', 'alt+d')
n.addCommand('Edit/Node/Align/vertically', 'alignNodes.alignNodes( nuke.selectedNodes(), direction="y" )', 'alt+x')
n.addCommand('Edit/Node/Align/evenlyHorizontally', 'distributeEvenly("x")', 'alt+shift+x')
n.addCommand('Edit/Node/Align/evenlyVertically', 'distributeEvenly("y")', 'alt+shift+d')
n.addCommand('Edit/Node/W_scaleTree', 'W_scaleTree.scaleTreeFloatingPanel()', 'alt+z')
#n.addCommand('Shuffle', "nuke.createNode('Shuffle')", "z")
n.addCommand('Crop', "nuke.createNode('Crop')", "[")
n.addCommand('CornerPin2D', "nuke.createNode('CornerPin2D')", "]")
n.addCommand('TimeWarp', "nuke.createNode('TimeWarp')", "?")
n.addCommand('TimeOffset', "nuke.createNode('TimeOffset')", "/")
n.addCommand('ChannelMerge', "nuke.createNode('ChannelMerge')", "n")
#n.addCommand('Invert', "nuke.createNode('Invert')", "v")
n.addCommand('Multiply', "nuke.createNode('Multiply')", "*")
n.addCommand('Reformat', "nuke.createNode('Reformat')", "e")
##
#n.addCommand('Edit/Node/W_scaleTree', 'W_scaleTree.scaleTreeFloatingPanel()', 'alt+w')
m.findItem("Edit").addCommand("HotBox", 'channel_hotbox.start()', "alt+q")

# Add to existing toolbar
toolbar = nuke.toolbar("Nodes")
toolbar.addCommand("Filter/VectorExtendEdge", "nuke.createNode(\"VectorExtendEdge\")")
toolbar.addCommand("Filter/BS_AlphaGrainEdge", "nuke.createNode(\"BS_AlphaGrainEdge\")")
toolbar.addCommand("Filter/edgeNoise", "nuke.createNode(\"edgeNoise\")")
toolbar.addCommand("Filter/CatsEyeDefocus", "nuke.createNode(\"CatsEyeDefocus\")")
toolbar.addCommand("Filter/fxT_chromaticAberration", "nuke.createNode('fxT_chromaticAberration')", icon='fxT_menu.png')
toolbar.addCommand( "Merge/Merges/Stencil", "nuke.createNode('Merge2','operation stencil')")
toolbar.addCommand( "Merge/Merges/Mask", "nuke.createNode('Merge2','operation mask')")
toolbar.addCommand( "Merge/Merges/From", "nuke.createNode('Merge2','operation from')")
toolbar.addCommand( "Merge/Merges/Divide", "nuke.createNode('Merge2','operation divide')")
toolbar.addCommand( "Merge/Merges/Under", "nuke.createNode('Merge2','operation under')")
toolbar.addCommand( "Merge/Merges/Difference", "nuke.createNode('Merge2','operation difference')")
toolbar.addCommand( "3D/SW_CameraShake3D", "nuke.createNode('SW_CameraShake3D')")
toolbar.addCommand( "3D/SpaceTransform", "nuke.createNode('SpaceTransform')")
toolbar.addCommand( "3D/tracker2Camera2", "nuke.createNode('tracker2Camera2')")
toolbar.addCommand( "3D/ImagePlane", "nuke.createNode('ImagePlane')")
toolbar.addCommand( "3D/V_Render", "nuke.createNode('V_Render')")
toolbar.addCommand( "3D/CardToTrack", "nuke.createNode('CardToTrack')")
toolbar.addCommand( "3D/CProject", "nuke.createNode('CProject')")

## Gizmos and nodes

##Hagbarth Tools
m = toolbar.addMenu("Hagbarth Tools", icon="h_tools.png")
m.addCommand("Silk", "nuke.createNode(\"h_silk\")", icon="h_silk.png")

m = toolbar.addMenu("LumaTools", icon="luma.png")
m.addCommand ("L_Fuse", "nuke.createNode(\"L_Fuse_v06\")")
m.addCommand ("L_Icolor", "nuke.createNode(\"L_Icolor_v02\")")
m.addCommand ("L_SwitchMatte", "nuke.createNode(\"L_SwitchMatte_v04\")")
m.addCommand ("L_Ramp", "nuke.createNode(\"L_Ramp_v01\")")
m.addCommand ("L_AlphaClean", "nuke.createNode(\"L_AlphaClean_v03\")")
m.addCommand ("L_BlurHue", "nuke.createNode(\"L_BlurHue_v01\")")
m.addCommand ("L_ExponBlur", "nuke.createNode(\"L_ExponBlur_v03\")")
m.addCommand ("L_Grain", "nuke.createNode(\"L_Grain_v05\")")
m.addCommand ("L_ChannelSolo", "nuke.createNode(\"L_ChannelSolo_v01\")")
m.addCommand ("L_SpotRemover", "nuke.createNode(\"L_SpotRemover_v03\")")

m = toolbar.addMenu("Nukepedia", icon="utility.png")
m.addCommand ("RealChromaticAberration", "nuke.createNode(\"RealChromaticAberration\")", icon="Chromatic_Ab_Icon.png")
m.addCommand ("RealHeatDistortion", "nuke.createNode(\"RealHeatDistortion\")", icon="RealHeatDistortionIcon.png")
m.addCommand ("X_Tesla", "nuke.createNode(\"X_Tesla\")", icon='X_Tesla.png')
m.addCommand ("Fizzle", "nuke.createNode(\"fizzle\")")
m.addCommand ("CS_HeatDistortion", "nuke.createNode(\"CS_HeatDistortion\")")
m.addCommand ("X_Distort", "nuke.createNode(\"X_Distort\")", icon='X_Distort.png')
m.addCommand ("BokehBlur", "nuke.createNode(\"BokehBlur\")")
m.addCommand ("EdgeExtend", "nuke.createNode(\"EdgeExtend\")")
m.addCommand ("glitch", "nuke.createNode(\"glitch\")")
m.addCommand ("filmburn", "nuke.createNode(\"filmburn\")")
m.addCommand ("pfGlitchy", "nuke.createNode(\"pfGlitchy\")")
m.addCommand ("Twitch", "nuke.createNode(\"Twitch\")")
m.addCommand ("InterferenceFX", "nuke.createNode(\"InterferenceFX\")")
m.addCommand("Twitch", "nuke.createNode(\"Twitch\")", icon="Twitch.png")
m.addCommand("Twitch3D", "nuke.createNode(\"Twitch3D\")", icon="Twitch3D.png")
m.addCommand("TX_Fog", "nuke.createNode(\"TX_Fog\")")

#Knob Defaults
nuke.knobDefault('Tracker4.label','[value reference_frame]')
nuke.knobDefault('In.operation','mask')
nuke.knobDefault('Out.operation','stencil')
nuke.knobDefault('Viewer.hide_input','True')
nuke.knobDefault('PostageStamp.hide_input','True')
nuke.knobDefault('PostageStamp.tile_color',"1073762303")
nuke.knobDefault("RotoPaint.toolbox", '''clone {
{ brush opc .1}
{ clone opc .1}
{ reveal opc .1}
}''')
##
