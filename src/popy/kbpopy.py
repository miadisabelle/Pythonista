#!python3

#fea issue #149

'''
This shows a scrolling row or grid of special characters in the Pythonista Keyboard. The view supports both the 'minimized' mode (above the QWERTY keyboard) and the 'expanded' mode with the grid filling most of the keyboard.

Note: This script is designed for the Pythonista Keyboard. You can enable it in the Settings app (under General > Keyboard > Keyboards > Add New Keyboard...). Please check the documentation for more information.
'''

import keyboard
import ui
import clipboard

cbfilename='cblast.txt'
# You can modify or extend this list to change the characters that are shown in the keyboard extension:
characters = ['(?)', '★', '⌘', '⌥', '⇧', '⇥', '⏎', '⌫', '⎋', '⌃', '→', '←', '↑', '↓', '⬅️', '⬆️', '➡️', '⬇️', '♥️', '♦️', '️♠️', '♣️', '1⁄2', '1⁄3', '2⁄3', '1⁄4', '3⁄4']
jgwillchars=['o2','i2md','cCb','poA','.o','.R']
jgwillchars2=['dk','dv','d2s','--']
jo={}
jo["dt2"]="don't introduce what you are doing or explaining it, just output results\n----\nREMEMBER: don't introduce, explain nor comments your changes."

jkeys=list(jo.keys())
alljgwillchars=jgwillchars+jkeys+jgwillchars2
characters=alljgwillchars+characters

cbl=[]
filter_out_data=["Here’s the next paragraph","Let me know if you","Let me know if you’d like","Here’s the revised","the revised paragraph with","Here is the first paragraph"]

class CharsView (ui.View):
	#@STCGoal Action on Pressed JGWiLl keys 
	def _jgwparsekey(self,ka):
	  if ka=='i2md':
	    url=clipboard.get()
	    
	    ka='![]('+url+')'
	  elif ka=='poA':
	    self.pop_append_clipboard()
	    ka=''
	  elif ka=='.R':
	    self.reset_last_clipboard()
	    ka=''
	  elif ka=='.o': 
	    #ka=self.pop_append_clipboard(True)
	    ka=self.end_c()
	  elif ka=='cCb':
	    ka=self.paste_clean()
	  else:
	    for k,v in jo.items():
	      if ka==k:
	        ka=v
	        break
	  return ka
	
	def parse_and_filter(self,input_string):
	  global filter_out_data
	  filtered_lines = []
	  for line in input_string.split('\n'):
	    if not any(substring in line for substring in filter_out_data):
	      filtered_lines.append(line)
	  return '\n'.join(filtered_lines)
    
	def paste_clean(self):
	  cb=clipboard.get()
	  ka=self.parse_and_filter(cb)
	  return ka
	  
	def reset_last_clipboard(self):
	  self.save_text('',cbfilename)
	
	def end_c(self):
	  c=self.get_content(cbfilename)
	  self.reset_last_clipboard()
	  return c
	
	def pop_append_clipboard(self):
	  cb=clipboard.get()
	  last=self.get_content(cbfilename)
	  if cb==last:
	    #print('nada es el equales')
	    return ''
	  
	  sep=''
	  
	  if len(last)>1:
	    sep='\n'
	  
	  nval=last + sep + cb
	  
	  self.save_text(nval,cbfilename)
	  #clipboard.set(nval)
	  #clipboard.set(nval)
	  return nval
	
	def get_content(self,file_name):
	  try:
	    with open(file_name, 'r') as file:
	      return file.read()
	  except FileNotFoundError:
	    return ""
	
	def save_text(self,text_string, file_name):
	  if text_string !='':
	    with open(file_name, 'w') as file:
	      file.write(text_string)
       
	def __init__(self, *args, **kwargs):
		super().__init__(self, *args, **kwargs)
		self.background_color = '#333'
		self.scroll_view = ui.ScrollView(frame=self.bounds, flex='WH')
		self.scroll_view.shows_horizontal_scroll_indicator = False
		self.add_subview(self.scroll_view)
		self.buttons = []
		for c in characters:
			button = ui.Button(title=c)
			button.font = ('<System>', 18)
			button.background_color = (1, 1, 1, 0.1)
			button.tint_color = 'white'
			button.corner_radius = 4
			button.action = self.button_action
			self.scroll_view.add_subview(button)
			self.buttons.append(button)
	
	def layout(self):
		rows = max(1, int(self.bounds.h / 36))
		bw = 44
		h = (self.bounds.h / rows) - 4
		x, y = 2, 2
		for button in self.buttons:
			button.frame = (x, y, bw, h)
			y += h + 4
			if y + h > self.bounds.h:
				y = 2
				x += bw + 4
		self.scroll_view.content_size = ((len(self.buttons)/rows + 1) * (bw + 4) + 40, 0)
	
	def jgwill_keyaction(self,ka):
	  ka=self._jgwparsekey(ka)
	  if keyboard.is_keyboard():
	    if ka != '':
	      keyboard.play_input_click()
	      keyboard.insert_text(ka)
	  else:
	    if ka!='':
	      print('===========')
	      print('JGWillActionKey input:', ka)

	  
	def button_action(self, sender):
		text = sender.title
		if text == '(?)':
			# Show help
			tv = ui.TextView(name='Help')
			tv.text = 'PoPy(orpheus)::You can customize this scrollable list of special characters by editing the script in Pythonista (tap and hold the shortcut button, and select "Edit Script").\n\nYou can also remove this Help button, if you like.'
			tv.font = ('<System>', 18)
			tv.editable = False
			tv.selectable = False
			tv.present()
			return
		
		for w in alljgwillchars:
		  if text==w:
		    self.jgwill_keyaction(text)
		    return
		
		if keyboard.is_keyboard():
			keyboard.play_input_click()
			keyboard.insert_text(text)	
		else:
			print('PyKeyboard input:', text)


def main():
	v = CharsView(frame = (0, 0, 320, 40))
	if keyboard.is_keyboard():
		keyboard.set_view(v, 'current')
	else:
		# For debugging in the main app:
		v.name = 'PyKeyboard Preview'
		v.present('sheet')


if __name__ == '__main__':
	main()
	
