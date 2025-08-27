'''
This script demonstrates how to use the streaming ChatGPT API in Pythonista or other apps, using the PyKeys keyboard.
 
The script presents a list of prompt templates. After a prompt is selected, it gets sent to the ChatGPT API, and the response is either printed to the console, or (when running in the Pythonista keyboard) typed into the current app.

Please note that you need your own OpenAI API key to run this script. For more information on how to get one, please see e.g.
	https://www.howtogeek.com/885918/how-to-get-an-openai-api-key/

You can enable the PyKeys keyboard in the Settings app (under General > Keyboard > Keyboards > Add New Keyboard...). Please check the "Shortcuts..." option in the 'wrench' menu for more information.
'''

import os
from dialogs import list_dialog
import keyboard
import clipboard
import openai

# Enter your OpenAI API key here:
openai.api_key = 'sk-...'


def insert_text(text):
	# When not running in the keyboard, print the generated text to the console.
	if keyboard.is_keyboard():
		keyboard.insert_text(text)
	else:
		print(text, end='')


def main():
	# Feel free to add your own prompt templates here:
	prompts = [
	 {
	  'title': '(Use [clipboard] as prompt)',
	  'prompt': '[clipboard]'
	 }, {
	  'title': '(Use [selection] as prompt)',
	  'prompt': '[selection]'
	 }, {
	  'title': 'Rhyme with [selection]',
	  'prompt': 'Find a word/sentence that rhymes with "[selection]"'
	 }, {
	  'title':
	   'Poem titled [selection]',
	  'prompt':
	   'Write a short, humorous poem titled "[selection]". It should just be a couple of verses long. Pay special attention to the rhythm and flow.'}
	]
	if (r := list_dialog('Prompt', prompts)) is None:
		return
	prompt = r['prompt']
	selection = keyboard.get_selected_text() if keyboard.is_keyboard() else clipboard.get()
	prompt = prompt.replace('[selection]', selection)
	prompt = prompt.replace('[clipboard]', clipboard.get())
	
	messages = [
	 {
	  'role': 'system',
	  'content': 'You are a helpful assistant.'
	 }, {
	  'role': 'user',
	  'content': prompt
	 }
	]
	response = openai.ChatCompletion.create(
	 model='gpt-3.5-turbo', messages=messages, stream=True, temperature=1
	)
	insert_text(selection + '\n\n')
	for chunk in response:
		content = chunk['choices'][0]['delta'].get('content', '')
		insert_text(content)


if __name__ == '__main__':
	main()

