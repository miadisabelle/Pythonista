
import coaiamodule

def _get_process_name_from_sender_name(sender_name):
  process_name=sender_name.replace('__button','')
  process_name=process_name.replace('button_','')
  process_name=process_name.replace('_button','')
  process_name=process_name.replace('_uibutton','')
  #todo Add more ui possible replacement bellow
  
  return process_name
  
def abstract_process_button_pressed(sender,input_message,default_temperature=0.35,pre=''):
  #todo @STCGoal Abstract UI Button caller. 
  print('   abstract_process_button_pressed')	
  #get sender text
  sender_name = sender.name
  sender_text = sender.title
  print(f"Button '{sender_name}' tapped. Text: '{sender_text}'")
  #process_name=sender_name.replace('_button','')
  process_name=_get_process_name_from_sender_name(sender_name)
  
  #todo abstract_process_send
  return coaiamodule.abstract_process_send(process_name,input_message,default_temperature,pre)
  
  
  #todo Feature Design 2406101532
  """
  it would implies calling an abstract_send request that reads the config for one mandatory value: process_name+'_instructions' and an optional value: process_name+_'temperature' otherwise use default of 0.35.
  
  if the process_name+'_instructions' not found in config, 
   an enhancement would display a 'create new process view' that edits the '../../shared/etc/config.json' by asking what is the input instructions and temperature then save back the config with these two values (ex. of added json keys/values:   "summarizer_instructions" : "[THE INSTRUCTIONS]", "summarizer_temperature": 0.2)
  """
  
