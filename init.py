nuke.pluginAddPath("./Gizmos")
nuke.pluginAddPath('./Gizmos/eyecandy/')
nuke.pluginAddPath('./Gizmos/luma/')
nuke.pluginAddPath('./Gizmos/pixelfudger')
nuke.pluginAddPath("./Icons")
nuke.pluginAddPath('./Python/')
#nuke.pluginAddPath('./KeenTools/')
nuke.pluginAddPath('./Python/StartupUI/')
nuke.pluginAddPath('./Python/Startup/')
nuke.pluginAddPath('./Presets')
nuke.pluginAddPath('./Toolsets')
nuke.pluginAddPath('./cragl')

#Hagbarth Tools
nuke.pluginAddPath('./Gizmos/hagbarth')
nuke.pluginAddPath('./Gizmos/hagbarth/icons')
nuke.pluginAddPath('./Gizmos/hagbarth/tools')
nuke.pluginAddPath('./Gizmos/hagbarth/graphics')
nuke.pluginAddPath('./Gizmos/hagbarth/python')

# Add presets to GUI
import cam_presets
cam_presets.nodePresetCamera()

# Scratch2Nuke Pipeline integration
nuke.pluginAddPath('c:\ProgramFiles\Assimilator\Settings\Script')
