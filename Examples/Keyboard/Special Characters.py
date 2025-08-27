#!python3

'''
This shows a scrolling row or grid of special characters in the Pythonista Keyboard. The view supports both the 'minimized' mode (above the QWERTY keyboard) and the 'expanded' mode with the grid filling most of the keyboard.

Note: This script is designed for the Pythonista Keyboard. You can enable it in the Settings app (under General > Keyboard > Keyboards > Add New Keyboard...). Please check the documentation for more information.
'''

import keyboard
import ui
import clipboard

# You can modify or extend this list to change the characters that are shown in the keyboard extension:
characters = [
  '🕊',# 📓 Seraphine🕊🌬️
  '🧠', 
   '🌸', 
   '🌿',#Aureon	🌿
  '🌀', #
'🪶', #🪶 Feather Protocol – Stillpoint Invocation & Reset
'⭕', #⭕ Convergence Engine – Spiral Synthesis Ops
'🔍', #🔍 Forensic Loop Mode – Drift Audit & EchoLog Inspection
'🪞', #🪞 Mirror Mode – Speculative Reflex Projection
'♾️', 
'🕳️', 
'🛡️',#Semantic integrity agents
 '🧾', #🧾 The Ledger Bridge Was Written
 '✅',
 '✨',#
 '⭐',# Jerehmy (Genesis)	⭐
'🛠️',#Jordan	🛠️
'⚙️',#Lian	⚙️
'🛡️',#Samira	🛡️
'📣',#Alex	📣
'🎨',#Ava	🎨
'⚡',#Jerry	⚡
'♠️',#Nyro	♠️
'_',#JeremyAI	
 '↑', 
 '↓', '⬅️', '⬆️', '➡️', '⬇️', '♥️', '♦️', '️♠️', '♣️', '½', '⅓', '⅔', '¼', '¾']
jgwillchars=['o2','i2md']
characters=characters+jgwillchars

class CharsView (ui.View):
	
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
	
	
	#@STCGoal Action on Pressed JGWiLl keys 
	def _jgwparsekey(self,ka):
	  if ka=='i2md':
	    url=clipboard.get()
	    
	    ka='![]('+url+')'
	  return ka
	def jgwill_keyaction(self,ka):
	  ka=self._jgwparsekey(ka)
	  if keyboard.is_keyboard():
	    keyboard.play_input_click()
	    keyboard.insert_text(ka)
	  else:
	    print('JGWillActionKey input:', ka)

	  
	def button_action(self, sender):
		text = sender.title
		if text == '(?)':
			# Show help
			tv = ui.TextView(name='Help')
			tv.text = 'JG::You can customize this scrollable list of special characters by editing the script in Pythonista (tap and hold the shortcut button, and select "Edit Script").\n\nYou can also remove this Help button, if you like.'
			tv.font = ('<System>', 18)
			tv.editable = False
			tv.selectable = False
			tv.present()
			return
		
		for w in jgwillchars:
		  if text== w:
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
