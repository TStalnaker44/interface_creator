"""
Author: Trevor Stalnaker
File: declarations.py

Functions that take widgets as input and output
code declarations to recreate the objects.
"""

from polybius.graphics import Button, TextInput, TextBox
from polybius.graphics import MultiLineTextBox, ProgressBar
from polybius.graphics import Panel, Checkbox

def getDeclaration(widget):
    return type2declare[type(widget)](widget)

def getButtonDeclaration(button):
    txt = button.getText()
    pos = button.getPosition()
    pos = ("(%d,%d)" % (pos[0], pos[1]))
    backgroundColor = "backgroundColor=" + str(button._backgroundColor)
    fontColor = "fontColor=" + str(button._fontColor)
    borderColor = "borderColor=" + str(button._borderColor)
    borderWidth = "borderWidth=" + str(button._borderWidth)
    padding = "padding=" + str(button._padding)
    font = ("Font('%s',%s)" % (button.getFont().getFontName(),
                               button.getFont().getFontSize()))
    return ("Button('%s',\n\t%s,\n\t%s,\n\t%s,\n\t%s,\n\t%s,\n\t%s,\n\t%s)" %
            (txt, pos, font, backgroundColor, fontColor, borderColor,
             borderWidth, padding))

def getTextInputDeclaration(tinput):
    dims = (tinput.getWidth(), tinput.getHeight())
    pos = tinput.getPosition()
    pos = ("(%d,%d)" % (pos[0], pos[1]))
    backgroundColor = "backgroundColor=" + str(tinput.getBackgroundColor())
    fontColor = "color=" + str(tinput.getFontColor())
    borderColor = "borderColor=" + str(tinput.getBorderColor())
    borderWidth = "borderWidth=" + str(tinput.getBorderWidth())
    borderHighlight = "borderHighlight=" + str(tinput._borderHighlight)
    backgroundHighlight = "backgroundHighlight=" + str(tinput._backgroundHighlight)
    maxlen = "maxLen=" + str(tinput._maxLen)
    text = "defaultText='" + tinput.getInput() + "'"
    font = ("Font('%s',%s)" % (tinput.getFont().getFontName(),
                               tinput.getFont().getFontSize()))
    template = "TextInput(" + ("%s,\n\t"*11)[:-3] + ")"
    return (template % (pos, font, dims,
                       backgroundColor,
                       fontColor, borderColor,
                       borderWidth, borderHighlight,
                       backgroundHighlight, maxlen,
                       text))

def getTextBoxDeclaration(tbox):
    text = tbox.getText()
    pos = tbox.getPosition()
    pos = ("(%d,%d)" % (pos[0], pos[1]))
    font = ("Font('%s',%s)" % (tbox.getFont().getFontName(),
                               tbox.getFont().getFontSize()))
    fontColor = "fontColor=" + str(tbox.getFontColor())
    return ("TextBox('%s',\n\t%s,\n\t%s)" % (text, pos, font))

def getMultiLineTextBoxDeclaration(tbox):
    text = "'" + tbox.getText() + "'"
    pos = tbox.getPosition()
    pos = ("(%d,%d)" % (pos[0], pos[1]))
    font = ("Font('%s',%s)" % (tbox.getFont().getFontName(),
                               tbox.getFont().getFontSize()))
    fontColor = "fontColor=" + str(tbox.getFontColor())
    backgroundColor = "backgroundColor=" + str(tbox.getBackgroundColor())
    alignment = "alignment='" + str(tbox.getAlignment()) + "'"
    padding = "padding=" + str(tbox.getPadding())
    spacing = "linespacing=" + str(tbox.getLineSpacing())
    template = "MultiLineTextBox(" + ("%s,\n\t"*8)[:-3] + ")"
    return (template % (text, pos, font, fontColor, backgroundColor,
                        padding, spacing, alignment))

def getProgressBarDeclaration(bar):
    pos = bar.getPosition()
    pos = ("(%d,%d)" % (pos[0], pos[1]))
    length = bar.getLength()
    maxStat = bar.getMaxStat()
    actStat = bar.getActiveStat()
    borderWidth = "borderWidth=" + str(bar.getBorderWidth())
    borderColor = "borderColor=" + str(bar.getBorderColor())
    backgroundColor = "backgroundColor=" + str(bar.getBackgroundColor())
    barColor = "barColor=" + str(bar.getBarColor())
    height = "height=" + str(bar.getHeight())
    alignment = "alignment='" + str(bar.getAlignment()) + "'"
    template = "ProgressBar(" + ("%s,\n\t"*10)[:-3] + ")"
    return (template % (pos, length, maxStat, actStat, borderWidth,
                        borderColor, backgroundColor, barColor,
                        height, alignment))

def getPanelDeclaration(pan):
    pos = pan.getPosition()
    pos = ("(%d,%d)" % (pos[0], pos[1]))
    dims = ("dims=(%d,%d)" % (pan.getWidth(), pan.getHeight()))
    color = "color=" + str(pan._backgroundColor)
    borderColor = "borderColor=" + str(pan.getBorderColor())
    borderWidth = "borderWidth=" + str(pan.getBorderWidth())
    template = "Panel(" + ("%s,\n\t"*5)[:-3] + ")"
    return (template % (pos, dims, color, borderColor, borderWidth))

def getCheckboxDeclaration(box):
    pos = box.getPosition()
    pos = ("(%d,%d)" % (pos[0], pos[1]))
    dims = ("dims=(%d,%d)" % (box.getWidth(), box.getHeight()))
    color = "backgroundColor=" + str(box.getBackgroundColor())
    borderColor = "borderColor=" + str(box.getBorderColor())
    borderWidth = "borderWidth=" + str(box.getBorderWidth())
    fontColor = "fontColor=" + str(box.getFontColor())
    font = ("font=Font('%s',%s)" % (box.getFont().getFontName(),
                               box.getFont().getFontSize()))
    isChecked = "isChecked=" + str(box._defaultCheck)
    symbol = "symbol='" + str(box._symbol) + "'"
    template = "Checkbox(" + ("%s,\n\t"*9)[:-3] + ")"
    return (template % (pos, dims, color, borderColor, borderWidth,
                        fontColor, font, isChecked, symbol))
    
type2declare = {Button:getButtonDeclaration,
                TextInput:getTextInputDeclaration,
                TextBox:getTextBoxDeclaration,
                MultiLineTextBox:getMultiLineTextBoxDeclaration,
                ProgressBar:getProgressBarDeclaration,
                Panel:getPanelDeclaration,
                Checkbox:getCheckboxDeclaration}
