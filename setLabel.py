#--
#Sven Ahlström
#--

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








