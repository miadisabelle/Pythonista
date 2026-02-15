import ui
import sound
import sys
sys.path.append("../lib")

#import coaiamodule
from coaiamodule import transcribe_audio
import coaiamodule 
import uuid

import os
import clipboard
import console
import sys
import boto3
import json
#-----------------------
testmode=False
if not testmode:
  dir_base = 'FTS'
  rec_basename_default='jgtml'
  #avec24061413
  dir_base = 'na'
  rec_basename_default='jgtml'
  dir_base = 'nasp'
  rec_basename_default='e01'
  
  dir_base = 'sc';rec_basename_default='lyre'
  dir_base = 'jgtmlmastery';rec_basename_default='mlmastery'
  dir_base = 'CeSaReT';rec_basename_default='lcmastery'
  dir_base = "odysseus";rec_basename_default="modular_platform_python_development_overview"
  dir_base = "orpheus";rec_basename_default="issue49"
  dir_base = "orpheus";rec_basename_default="issue61o1"
  rec_basename_default="scgm_79"
  rec_basename_default="issue190"
  rec_basename_default="story215"
  rec_basename_default="review223"
  
  dir_base = 'CeSaReT'
  rec_basename_default='creating'
  rec_basename_default='creator2audience'
  rec_basename_default='flowisejeremy'
  
  dir_base = 'nasp'
  rec_basename_default='triangulo'
  dir_base = "orpheus";rec_basename_default="nce370"
  dir_base = "orpheus";rec_basename_default="issue417"
  dir_base = "orpheus";rec_basename_default="issue423"
  dir_base = 'CeSaReT'
  rec_basename_default="feedback81"
  rec_basename_default="story89"
  
  dir_base = "orpheus";rec_basename_default="588-CCOT"
  
  
  
else:
  dir_base = 'dummyshare01'
  rec_basename_default='default'
  
  dir_base = 'fritz'
  rec_basename_default='creating'
  
  rec_basename_default='process_by_ui_button'
  dir_base = 'test'
  rec_basename_default='process_name_faction'


seq_dont_increment=False #if manually set the UI seq, we wont increment
rec_seq_default=1

print('PROD_240505beta3')

rec_state=False #track the recording state of the app.  if recording and text is being worked on, ex. we will want to use previous iteration of the one being recorded.

ui_updating=False
#issue with output text 1 which goes somewhere else and it is supposed to be. It could save in the application directory

# Global variables
output_text_subdir='output'

output_rec_subdir='recording'

#dir_base=''# sefault current
store_root='../../shared'

audio_ext_default='.m4a' #record format required by Apple
text_ext_default='.txt'
synt_audio_format="mp3"
synt_text_ext='synt.txt' #each audio synt will have a corresponding file with this ext

txt_out_ext=text_ext_default
md_hist_bn='recording'
text_ext_mdhist='.md' # an historic file with all iterations of the entity story ex: dir_base/rec_basename.md
text_fn_suffix='.c'
dictkore_fn_suffix='.dtk'
synt_audio_ext_prefix=''

#### STOP HERE UNLESS YOU KNOW WHAT YOU ARE DOOOOING

mdprecontent='\n----\n----\n\n'


#legacy audio synt variable and new data steucture to choose from Ui the synt language
fr='Celine'
sp='Mia'
en="Joanna"
turkisk='Filiz'
british='Emma'
india='Raveena'
nz='Amy'
languages = {
    'fr': 'Celine',
    'sp': 'Mia',
    'us': 'Joanna',
    'turkisk': 'Filiz',
    'tk': 'Filiz',
    'british': 'Emma',
    'gb': 'Emma',
    'india': 'Raveena',
    'nz': 'Amy',
    'en': 'Amy'
}
#default language
vid=nz #set variable with above language 
lang='nz' #default language
lang_en_pref='nz' #prefered english  culture, NOT IMPLEMENTED USE THIS INSTEAD OF en in filename



startrec = False

status_label_name = 'status_label'
status_label=None
recorder = None
audio_file_path = None
text_file_path = None
text_file_path_mdhist = None
text_file_path_mdhist_seq = None #md history for the sequence
text_file_path2 = None
text_file_path3 = None #@STCGoal with history suffix increments each time the save button is presses (ex. dictkore )

#ui textfields we use globally
bn_textfield=None
itr_textfield=None
dir_base_textfield=None
text_view=None
changed_text=None
langseg=None #language segment select

last_dictkore_result_message=None
last_synt_audio_file_path=None

text_base =output_text_subdir
audio_base =output_rec_subdir

rec_seq=rec_seq_default

play_button=None
previous_button=None
next_button=None

def setstatus(msg):
  global status_label
  #status_label = sender.superview['status_label']
  status_label.text = msg
  print('@STATUS: ',msg)


output_folder_path=None


def set_dir_base(_dir_base,_store_root=None):
	global audio_base,text_base,output_rec_subdir,output_text_subdir,dir_base,store_root,rec_seq,text_file_path_mdhist,text_ext_mdhist,output_folder_path,md_hist_bn
	
	rec_seq=1 # reset the seq
	
	if _store_root is not None:
		store_root=_store_root
		
	dir_base=_dir_base
	output_folder_path=os.path.join(store_root,dir_base)
	
	audio_base = os.path.join(output_folder_path,output_rec_subdir)
	
	
	
	text_file_path_mdhist= os.path.join(output_folder_path,md_hist_bn + text_ext_mdhist)
	
	
	
	if not os.path.exists(audio_base):
		os.makedirs(audio_base)
	
	text_base = os.path.join(dir_base,output_text_subdir) #old
	text_base = os.path.join(output_folder_path,output_text_subdir)
	
	if not os.path.exists(text_base):
		os.makedirs(text_base)


#initial set of dir_base
set_dir_base(dir_base,store_root)

last_transcribed_text=None

#todo @STCIssue Should run from a function to init
rec_basename=rec_basename_default
rec_seq_pad = str(rec_seq).zfill(3)
audio_ext=audio_ext_default
text_ext=text_ext_default

#@STCIssue is this still relevant ??
rec_filename=rec_basename+'-'+rec_seq_pad+audio_ext
out_textfile=rec_basename+'-'+rec_seq_pad+text_ext


d2s_text=None
d2s_text_src=None


def aclean_bn(oname):
	"""
	clean the basename for good namong convention
	"""
	return oname.replace(' ','_').replace(',','_').replace('/','-').replace(':','__')


def update_fn(_rec_basename='rec-lc-04-intro_chain', _rec_seq=1, _audio_base_dir='cache', _text_base_dir='output', _ext='.m4a', _text_ext='.txt',_dir_base=None,_store_root=None):
  """
  This function does the file naming logic and increments the rec_seq if 'audio_file_path' exists.
  """
  global rec_basename, rec_seq, rec_seq_pad, rec_filename, out_textfile, audio_file_path, audio_base, text_file_path,text_file_path2, text_base, audio_ext, text_ext, itr_textfield, bn_textfield,dir_base,store_root,text_file_path_mdhist,text_file_path_mdhist_seq,output_folder_path,seq_dont_increment
  #todo REC &CORRECT FEATURE REFLEXION 2406101339 :: do we just want to work on the last iteration while it is still recording ? first it could be so but has to be a simple implement (with if rec_state==True ??)
	
  
  if _store_root is not None:
  	store_root=_store_root
  if _dir_base is not None:
  	dir_base=_dir_base
  	set_dir_base(dir_base,store_root)
  
  # Updating our global values
  rec_basename = aclean_bn(_rec_basename)
  rec_seq = _rec_seq
  audio_base = _audio_base_dir
  text_base = _text_base_dir
  audio_ext = _ext
  text_ext = _text_ext
  
  rec_seq_pad = str(rec_seq).zfill(3)
  
  rec_filename = rec_basename + '-' + rec_seq_pad + audio_ext
  out_textfile = rec_basename + '-' + rec_seq_pad + text_ext
  
  print('rec_filename:', rec_filename)
  print('out_textfile:', out_textfile)

  
  # The full path and output dir
  audio_file_path = os.path.join(audio_base, rec_filename)
  text_file_path = os.path.join(text_base, out_textfile)
  text_file_path2=audio_file_path.replace(audio_ext,'')+text_fn_suffix+text_ext
  
  print('  MDHist foreach seq..')
  text_file_path_mdhist_seq= os.path.join(output_folder_path,rec_basename + text_ext_mdhist)
  print('    text_file_path_mdhist_seq')
  
  # --@STCGoal data steuxture for the whole namespace+basename
  ## we read it to have all the sequence in the context, if that is acceptable amount of text !!
  
  
  print('  audio_file_path:', audio_file_path)
  print('  audio_base:',audio_base)
  print('text_file_path:', text_file_path)
  print('  text_base:',text_base)
  #text_file_path_mdhist
  print('text_file_path_mdhist:', text_file_path_mdhist)
  #@STCGoal A master file receives an append of new iterations and variations made by Dictkore.
  
  # Check if audio_file_path exists
  if os.path.exists(audio_file_path) and not seq_dont_increment:
    rec_seq += 1  # Increment rec_seq
    print('Recursive increment:', str(rec_seq))
    
    # Execute recursively
    update_all()
  else:
    if seq_dont_increment:
      print('  seq_dont_increment ACTIVE')
    
  print('update_fn done')
  print('values:', out_textfile, audio_file_path)
  
  #@STCIssue: There might be a better way to update UIs
  if bn_textfield is not None:
    bn_textfield.text = rec_basename
  if itr_textfield is not None:
    itr_textfield.text = str(rec_seq)
    
    
    
# 


_is_updating=False

#wrap the logics that should update all stuffs 
def update_all():
	global rec_basename,rec_seq,audio_base,text_base,text_ext,audio_ext,_is_updating,dir_base
	#if not _is_updating:
		
		#_is_updating=True
	update_fn(_rec_basename=rec_basename,_rec_seq=rec_seq,_audio_base_dir=audio_base,_text_base_dir=text_base, _ext=audio_ext,_text_ext=text_ext,_dir_base=dir_base,_store_root=store_root)
	#_is_updating=False








##############









#todo ReadConfig refacto what goes here and in the common lib ? Where this is used ? is it called a meaningful name ?
def readconfig_polly(_store_root=None,pollyconf_key='pollyconf',_config_fn='config.json'):
	global store_root
	print(  'store_root:'+store_root)
	
	#shared config 
	if _store_root is not None:
		store_root=_store_root
	sharedconfpath=os.path.join(store_root,'etc')
	
	_config=None
	
	#do we have a config in  global.etc dir ?
	_glbalconfpath=os.path.join(sharedconfpath,_config_fn)
	
	try:
		#first load from global
		with open(_glbalconfpath) as json_file:
			_config = json.load(json_file)
	except :
		# otherwise load from the app folder
			
		with open(_config_fn) as json_file:
			_config = json.load(json_file)
	
	if _config is not None:
		pollyconf_data=_config #if we have just polly conf jn the file
		# check if that is a global config, the polly keys are goojng to be in a a subkey
		if pollyconf_key  in _config:
			pollyconf_data=_config[pollyconf_key]
		
		#we should be ready to get authentication data we need to make our polly calls 
		key = pollyconf_data['key']
		secret = pollyconf_data['secret']
		region = pollyconf_data['region']
		
		return key,secret,region
	else:
		print('error reading config')
		print('config.json must be created in current dir or most likely suggested in global config ('+ _glbalconfpath+')')
		print("""  "pollyconf":{
  "key": "__AWSKEY__",
  "secret": "__AWSSECRET__",
  "region":"us-east-1"
}
}""")
		sys.exit(1)


def mk_outfilepath(outfile,dir_base='synthesized',store_root='../../shared'):
	outdir=os.path.join(store_root,dir_base)
	try:
		if not os.path.exists(outdir):
			os.makedirs(outdir)
	except Exception as ex :
		print('ohoh, could not make output path:'+outdir)
		print(ex)
		raise ex
	return os.path.join(outdir,outfile)

def mk_synt_outpath():
  global text_file_path,lang,synt_audio_ext_prefix,synt_audio_format,txt_out_ext,synt_text_ext
  _synt_ext=synt_audio_ext_prefix+'.'+lang+'.'+synt_audio_format
  
  outfilepath=text_file_path.replace(txt_out_ext,_synt_ext)
  outsynttextfile=outfilepath.replace(synt_audio_format,synt_text_ext) #same basename as the .mp3
  
  return outfilepath,outsynttextfile #todo add .synt.txt

review_feature_implemented=False
def load_text_file(file_path):
  global text_view,review_feature_implemented
  try:
    with open(file_path, "r") as file:
      text_content = file.read()
      text_view.text = text_content
      
      if review_feature_implemented:
        file_path_review=file_path.replace('.txt','.review.txt')
        print('  file_path_review:',file_path_review)
        if os.path.exists(file_path_review):
          with open(file_path_review, "r") as rfile:
            text_content_review = rfile.read()
            review_text_field.text = text_content_review
  except :
    pass
      

  

def enable_play_button_if():
  global play_button
  curr_audio_filepath,curr_outsynttextfile=mk_synt_outpath()
  #todo @STCGoal Enable play button if an audio exist with that iteration and lang
  
  if os.path.exists(curr_audio_filepath):
    play_button.enabled=True
    setstatus(' Audio Synt Exist, press play')
    print('  curr_outsynttextfile:',curr_outsynttextfile)
    load_text_file(curr_outsynttextfile)
  else:
    play_button.enabled=False
  
  #todo @STCIssue refresh_ui() for all this in here
  








#in thebUi we can set the basenane and the incrementation would be automatic

def dir_base_textfield_ui_updated(sender):
	global dir_base_textfield,store_root
	_new_dir_base=aclean_bn(dir_base_textfield.text)
	print('   dir base ui updated '+_new_dir_base)
	
	set_dir_base(_new_dir_base,store_root)
	bn_textfield_ui_updated(sender)
	
	update_all()

def ui_clean_views(sender):
  global text_view
  text_view.text=''

# This executes when the UI textfield changes
def bn_textfield_ui_updated(sender):
	global rec_basename, bn_textfield,rec_seq
	#rec_seq, rec_filename, out_textfile, audio_file_path, audio_base,text_file_path,text_base,audio_ext,bn_textfield
	
	ui_clean_views(sender)
	
	
	_newbasename= aclean_bn(bn_textfield.text)
	print(' newbasename:'+_newbasename)
	
	rec_basename=_newbasename
	
	# sequence restarts
	rec_seq=1
	
	
	update_all()
	

	print('  basename_updated done')
	print('  values: ',out_textfile,' ,', audio_file_path)



def itr_textfield_ui_updated(sender):
	global itr_textfield,rec_seq,seq_dont_increment
	rec_seq=int(itr_textfield.text)
	
	update_all()
	enable_play_button_if()
	#seq_dont_increment=False
	


def dir_base_ui_set(_dir_base):
	global dir_base_textfield,dir_base
	dir_base_textfield.text=_dir_base
	dir_base=_dir_base
	set_dir_base(dir_base)

# This sete the UI Basename from an input.  
# It is used to extend the use of this to receive a second arg , the basename
def basename_ui_set(bname):
	global bn_textfield
	bn_textfield.text=bname
	#update_all()
	print(' ...basename_ui_set( '+bname)
	bn_textfield.text=bname
	print(' DONE basename_ui_set( '+bname)
	
	print('      ? did that ran the UI action when we set the .text in code')
	#textfield=sender.superview['textfieldbasename']
	#textfield.text = bname
	#basename_updated(sender)


  
def set_lang(_lang):
  global lang,languages,vid
  lang=_lang
  
  print(lang)
  # update vid
  vid=languages[lang]#a corresponding entry exist in this object with lang
  setstatus(''+ vid+'/'+lang + ' (synt language selected)')
  
  enable_play_button_if()
  

#todo @STCGoal UI Updater
def ui_update_all(sender):
  global ui_updating
  if not ui_updating:
    ui_updating=True
    langseg_ui_changed(sender)
    enable_play_button_if()
  
  ui_updating=False

def langseg_ui_changed(sender):
  global langseg,lang,vid,languages,ui_updating
  

  if langseg is None:
    langseg=sender.superview['langseg']
  try:
    sel_index=sender.selected_index 
  except:
    #todo @STCIssue Nav index issue 24052217
    sel_index=1# each time we navigate it resets 
    #sel_index=langseg.selected_index
    pass
  
  idx=sel_index
  set_lang(langseg.segments[idx])
  
  if not ui_updating:
    ui_update_all(sender)
  #lang=langseg.segments[idx]
  
  
  


def save_mdhist(_text,_suffix='',_header='###',is_new=True,is_text=True):
  global rec_seq,text_file_path_mdhist,rec_basename,rec_seq_pad,mdprecontent,text_file_path_mdhist_seq
  
  print('  text_file_path_mdhist')
  if _text is not None:
    
    #filemd.write('\n## '+rec_basename +'\n')
    #seqstr=str(rec_seq)
    
    # pre content separator 
    e=''
    if is_new:
      _precontent=mdprecontent
      _precontent=_precontent+'\n# '+rec_basename
      _precontent=_precontent+'\n'+ '## '+rec_seq_pad 
    else:
      _precontent='\n'+ '## '+rec_seq_pad 
      
    if is_text:
      e=e+_precontent
      _title=' '  +_suffix+'\n'
      e=e+'\n'+_header+_title
      e=e+_text
    else:
      #it is a content we append such as a link to the synt audio
      e=e+'\n'
      e=e+'\n'+_header+' '+_text
      e=e+'\n'
    with open(text_file_path_mdhist, 'a',encoding='utf-8') as filemd:
      filemd.write(e)
      print('   gbl md written:'+text_file_path_mdhist)
    with open(text_file_path_mdhist_seq, 'a',encoding='utf-8') as filemdseq:
      filemdseq.write(e)
      print('   seq md written:'+text_file_path_mdhist_seq)
      
      
#todo Processed Text is Saved with an extension. ex.  myfile-008.d2s.txt
def save_processed_text(text,processed_suffix='dko',filepath=None,ext='.txt'):
  global text_file_path
  if filepath is None:
    filepath=text_file_path
    
  sext='.'+processed_suffix+ext
  pfilepath=filepath+'.'+sext
  
  pfilepath=pfilepath.replace(ext+'.'+sext,sext)
  
  
  print(' ====save_processed_text===>>> ')
  print('   pfilepath=',pfilepath)
  with open(pfilepath, 'w',encoding='utf-8') as file:
    file.write(text)
		

def save_text1(_text,_suffix='',is_new=False):
	global text_file_path,text_file_path_mdhist,text_file_path2,rec_seq

	print('====save_text1(_text):====')
	with open(text_file_path, 'w',encoding='utf-8') as file:
		file.write(_text)
		
		print(text_file_path)
	print('  _suffix:'+_suffix)
	
	save_mdhist(_text,_suffix,is_new=is_new)

	
def wrap_abstract_process_button_pressed(sender,input_message):
  #MIGRATING IT TO coaiauimodule
  import coaiauimodule
  #todo @STCGoal Abstract UI Button caller. 
  
  #abstract_process_button_pressed(sender,input_message,default_temperature=0.35,pre=''):
  return coaiauimodule.abstract_process_button_pressed(sender,input_message)

def mk_sender_suffix(sender_text:str):
  res=sender_text.lower()
  res=res.replace(' ','')
  return res

def ui_process_button_pressed(sender):
  global text_view
  
  #todo An LLM process is called and we have our new text_view updated and a file saved with that llm process name or acronym.
  """@STCGoal Adequate Architecture 2406111431 (coaia/pyrec-prod/xrec2text03.py)
  * acronym could come from the title used in the button (or _button_ACRONYM) : it would test if an acronym is used in the name of the sender and alternatively use the sender title
  LIMITATIONS: Logics to serialize is in this UI proto, refactoring will create a data layer responsible to store the data (save, load, distribute, publish, etc)
   coaiauimodule would use this data layer wrapper.
   coaiamodule would remain a framework layer we use
   coaiablmodule would be a new module wrapping various action latterns we developped in here and be executable independently of UI components.  example:
     * dkore : text_2_correct(path or content), _dataContext(dir_base,basename,iteration_seq_number): # we would have a .dko.$ext saved, appended markdown to dir_base+basename made file, etc
     * ...
  # Possible definition of these action should eventually comes from various data sources such as :
    * .env in the namespace
    * csv from SNoteURL(global or local to the namespace)
    * csv directly in the namespace
    * list made by routing agent when starting the session (or while in the session based on inputs in the iterations).  It would be able to consider previous iterations on the same namespace when starting a new session.
  """
  input_message=text_view.text
  
  sender_name = sender.name
  sender_text = sender.title
  print('   generic call:')
  print('     ',sender_name,':',sender_text)
  #wrap_abstract_process_button_pressed(sender,input_message):
  out_text=wrap_abstract_process_button_pressed(sender,input_message)
  
  print('    text:')
  print(out_text)
  print('===============')
  save_processed_text(out_text,mk_sender_suffix(sender_text))
  
  text_view.text=out_text

def summarizer_button_pressed(sender):
  global text_view
  
  input_message=text_view.text
  
  print('  summarizer_button_pressed')
  
  #wrap_abstract_process_button_pressed(sender,input_message):
  summarized_text=wrap_abstract_process_button_pressed(sender,input_message)
  
  print('   summarized text:')
  print(summarized_text)
  print('===============')
  save_processed_text(summarized_text,'sum')
  
  text_view.text=summarized_text


def details2shape_pressed(sender):
  global text_view, last_transcribed_text, text_file_path_mdhist, last_dictkore_result_message,d2s_text,d2s_text_src
  print('  details2shape button pressed')
  """
    transform in shapes the content
    much more than just a summary
  """
  #import coaiamodule 
  print('  Sending the request to details2shape:')
  #todo @STCGoal details2shape feature
  d2s_text_src = text_view.text
    
  setstatus('d2s started...')
  try:
    # Send the request to d2s
    d2s_result_message = coaiamodule.d2s_send(d2s_text_src)
        
    if d2s_result_message:
      # Set the completed message to the output element
      print('""" ### d2s:')
      print('' + d2s_result_message)
      print('"""')
      #todo save_processed_text(text,processed_suffix='dko',filepath,ext='.txt')
      save_processed_text(d2s_result_message,'d2s')
            
      # updating the text view ui with dictkore results
            
      text_view.text = d2s_result_message
            
      print('  appending d2s...right away ')
      print('===d2s completed===')
            
      #text_file_path_mdhist
            
      save_mdhist(d2s_result_message, '-d2s',is_new=False,is_text=True)
      setstatus('d2s completed')
      d2s_text=d2s_result_message
    else:
      setstatus('d2s failed. no value')
      d2s_text=None
    
  except Exception as ex:
    setstatus('d2s failed. see console')
    print(ex)
    
    
  

def dictkore_button_pressed(sender):
  global text_view, changed_text, last_transcribed_text, text_file_path_mdhist, last_dictkore_result_message
  
  print('  dictKore button pressed')
  """
    ADD system instruction of dicktkore
    refactor coaia...module chat for global use
    can we use :
    import ..lib.coaiamodule ??
  """
    
  #import coaiamodule 
  print('  Send the request to dictkore:')
  changed_text = text_view.text
  if changed_text != last_transcribed_text:
    print('""" ### CHG:')
    print(changed_text)
    print('"""')
    print('""" ### ORI:')
    print(last_transcribed_text)
    print('"""')
  else:
    print('""" ### ORI:')
    print(last_transcribed_text)
        
  setstatus('dictkore started...')
  try:
    # Send the request to dictkore
        
    dictkore_result_message = coaiamodule.dictkore_send(changed_text)
        
    if dictkore_result_message:
      # Set the completed message to the output element
      print('""" ### Dictkore:')
      print('' + dictkore_result_message)
      print('"""')
            
      # updating the text view ui with dictkore results
            
      text_view.text = dictkore_result_message
      #todo save_processed_text(text,processed_suffix='dko',filepath,ext='.txt')
      save_processed_text(dictkore_result_message,'k')
      
      print('  appending dictkore...right away ')
      print('===dicktore completed===')
            
      #text_file_path_mdhist
            
      save_mdhist(dictkore_result_message, '-dkored',is_new=False,is_text=True)
      setstatus('dictkore completed')
    else:
      setstatus('dictkore failed. no value')
    
  except Exception as ex:
    setstatus('dictkore failed. see console')
    print(ex)
  last_dictkore_result_message = dictkore_result_message



#todo Refactor Abstract to module
def synthesize(text,voice_id,outfile,outformat="mp3"):
	key,secret,region=readconfig_polly()
	
	try:
		polly = boto3.client('polly', aws_access_key_id=key, aws_secret_access_key=secret, region_name=region)
		
		response = polly.synthesize_speech(Text=text,OutputFormat=outformat,VoiceId=voice_id)
	except Exception as ex :
		print(' error with polly service')
		print(ex)
		raise ex 
	
	try:
		file = open(outfile, 'wb')
		file.write(response['AudioStream'].read())
		file.close()
	except Exception as ex :
		print('  error when writing the file '+outfile)
		print(ex)
		raise ex 
		






def synt_button_pressed(sender):
  global vid,text_view,text_file_path,text_file_path2,text_file_path,last_transcribed_text,nz,british,fr,dir_base,rec_basename
  print('  would synthesize an audio and saves it')
  run_audio_synt(vid)
  enable_play_button_if()




#execute our prototype that stnthesize into audio what is in the text view ui
def run_audio_synt(vid):
  global text_file_path,dir_base,store_root,last_transcribed_text,text_view,dir_base,rec_basename,last_synt_audio_file_path,lang,synt_audio_ext_prefix,synt_audio_format,txt_out_ext,synt_text_ext
  text=text_view.text#last_transcribed_text,text_view
  
  
  outfilepath,synt_text_outfilepath=mk_synt_outpath()
  print('   stbt:'+outfilepath  )
  
  
  
  try:
    last_synt_audio_file_path=None #we reset our last path before we do it
    setstatus('Synthesizing audio...')
    
    #todo @STCGoal .synt.txt is created with the synt content text
    
    #synt_text_outfilepath=outfilepath.replace('.mp3',synt_text_ext)
    print('====synt_text_outfilepath(_text):====')
    with open(synt_text_outfilepath, 'w',encoding='utf-8') as file:
      file.write(text)
    
    #todo @STCIssue Too long text wont synt 3000 caracters limits
    synthesize(text,vid,outfilepath,synt_audio_format)
    last_synt_audio_file_path=outfilepath
    setstatus('synt:'+last_synt_audio_file_path)
    
    print('======AudioSynt Completed====')
    
    
    print(' Making links in the history markdown')
    #todo last_synt_audio_file_path in mdhist
    #Relative synt link path
    _relative_synt_filepath='.'+outfilepath.replace(dir_base,'').replace(store_root,'').replace('//','/')
    print('  relative_synt_filepath:'+_relative_synt_filepath)
    
    #todo @STCGoal Transported content has links to synthesized audio
    _text='[AudioSynt]('+_relative_synt_filepath+') ('+lang+')'
    print('  mdhist audio text:'+_text)
    #todo @STCGoal Md2HTML - An HTML is rendered for distribution and viewing purpose
    #html_content=coaiamodule.render_markdown(_text)
    save_mdhist(_text,_header='####',is_new=False,is_text=False)
    print('======AudioSynt added to mdhist====')
    
  except Exception as _ex:
    print('  synthesize failed:')
    print(_ex)
  print('=======================')
    



###############
  
  
  
def save_button_pressed(sender):
	global itr_textfield,text_file_path,text_file_path2,text_file_path_mdhist,text_view
	print('  save button pressed')
	text_view=sender.superview['text_view']
	_text=text_view.text
	try:
	  save_text1(_text,is_new=False)
	  setstatus('Saved text ok')
	except Exception as ex:
	  setstatus('failed saving text')
	  print(ex)
	  

#bn_textfield_ui_updated
    	#itr_textfield_ui_updated
def itr_ui_set(itrval):
	global itr_textfield,rec_seq
	print('   ...itr_ui_set( '+str(itrval))
	rec_seq=itrval
	itr_textfield.text=str(rec_seq)






#todo @STCGoal Track Rec State rec_state=False 



def prerecording(sender):
  global changed_text
  changed_text=None #we reset that
  bn_textfield_ui_updated(sender)
  itr_textfield_ui_updated(sender)
  dir_base_textfield_ui_updated(sender)

def recording_started(sender):
	global recorder, audio_file_path,rec_filename
	print('  Recording in progress')

def recording_already(sender):
  global recorder, audio_file_path,rec_filename,changed_text,rec_state
  print('  Already recording event sequence starts')
  print('   CALL STOP ACTION WE MADE ALREADY THEN WE PLAN TO START RECORDING AGAIN')
  stop_action(sender)
  rec_state=False
  record_action(sender)
  
  
  
def record_action(sender):
  global recorder, audio_file_path,rec_filename,changed_text,rec_state
  
  #todo @STCIssue Press when Recording Delete current without transcribing it
  if rec_state:
    #we are already recording
    #todo Rec button presses while recording already
    recording_already(sender)
  else:
    #@STCIssue That is probably where we did not increment the audio if recroded already
    prerecording(sender)
    rec_state=True
    
    recorder = sound.Recorder(audio_file_path)
    
    recorder.record()
    
    print("Recording started..."+audio_file_path)
    
    setstatus( rec_basename+' itr:'+str(rec_seq) +' recording...')
    
    recording_started(sender)

def recording_stopping(sender):
	global recorder, audio_file_path,text_file_path,text_file_path2,rec_filename,last_transcribed_text
	print(  '   STOP recordint started')
	
def recording_stopped(sender,_recorder=None):
	
	global recorder, audio_file_path,text_file_path,text_file_path2,rec_filename,last_transcribed_text,text_fn_suffix,audio_ext,text_view
	#global recorder,audio_file_path,rec_filename,text_file_path,text_file_path2
	if _recorder is not None:
		recorder=_recorder
	
	print(  '  @Refacto: migrate flow of actions in this ending recording transition.  ')
	"""
	
	1. transcript
	
	  do transfription and update global text
	
	2.serialization
	 execute approriate serialization of content.
	  - we dont really need to keep 
	"""
	print("  transcribing:"+audio_file_path)
	
	print("    text_outifle:"+text_file_path)
	print("    text_outifle2:"+text_file_path2)
	
	setstatus(rec_filename+'->Transcribing')
	
	# Convert audio data to text using coaiaspeech2text module
	try:
	  #todo transcribe_audio lob call
		transcribed_text = transcribe_audio(audio_file_path)
		setstatus('Just Transcribed:'+rec_filename)
		
		print('"""')
		print(transcribed_text)
		print('"""')
		
		last_transcribed_text=transcribed_text
		
		# Set the transcribed text in the text view
		
		
		
		text_view.text = transcribed_text
	except Exception as e:
		setstatus('Failed transcribing..')
		print(e)
	
	
	try:
		
		#write the text file 
		save_text1(last_transcribed_text,'-ori',is_new=True)
		
		
		#possible enhancement to move saving the output to files in a function : later we could 
		
		
		#'ascii' codec can't encode character '\xe7' in position 34: ordinal not in range(128)
		with open(text_file_path2, 'w',encoding='utf-8') as file2:
			file2.write(transcribed_text)
			setstatus(text_file_path2+ ' written ')
		print(' Ending recording of:'+audio_file_path)
		print(' Ending export of:'+text_file_path)
		
	except Exception as e:
		setstatus('Failed writing')
		print(e)

	
def stop_action(sender):  
	global recorder,rec_state
	#, audio_file_path,text_file_path,text_file_path2,rec_filename,last_transcribed_text,text_fn_suffix,audio_ext,text_view
	
	if rec_state:
	  recording_stopping(sender)
	  #if recorder is None:
		  #setstatus('Press record to start')
		  #return
	
	  setstatus('Stopping...')
	
	  recorder.stop()
	  recording_stopped(sender,recorder)
	  rec_state=False
	else: #we might be playing and desire to stop
	  sound.stop_all_effects()

volume=0.5

def volume_slider_changed(sender):
  global volume
  volume=sender.value
  sound.set_volume(volume) 

# Function to play the corresponding audio file
def play_audio_file(file_path):
  print('   we expect to play...')
  sound.stop_all_effects() # we dont want more than one thing playing
  #todo Not playing ??
  cdir=os.getcwd()
  fullpath=os.path.join(cdir,file_path)
  print('  fullpath',fullpath)
  #sound.set_volume(0.5)  # Set the volume to 50%
  sound.play_effect(fullpath)
  #p=sound.Player(file_path)
  #p.play()
  

def play_button_pressed(sender):
  current_synt_file,current_synt_text_file=mk_synt_outpath()
  setstatus('playing:'+current_synt_file)
  
  #sound.play_effect(current_synt_file)#
  play_audio_file(current_synt_file)
  

def test_set_button_pressed(sender):
  global text_view
  txt_test=	"""The Market Facilitation Index (MFI) is a technical indicator that measures the buying and selling pressure behind a security's price movement. It is calculated by comparing the typical price (the average of the high, low, and closing prices) to the volume-weighted average price (VWAP). A high MFI value indicates that there is strong buying pressure, while a low MFI value indicates that there is strong selling pressure."""
  tst_old="""
	1. transcript
	
	  do transfription and update global text
	
	2.serialization
	 execute approriate serialization of content.
	  - we dont really need to keep """
  text_view.text=txt_test
  

def copy_to_clipboard_action(sender):
	global rec_filename,text_view
	
	content = text_view.text
	clipboard.set(content)
	print("Copied")
	# Show a toast message to indicate successful copy
	# show_toast('Copied to clipboard')
	setstatus('Text Copied')

#print(os.getcwd())

# Set up the UI
v = ui.load_view()

status_label=v[status_label_name]

#todo @BUTTONS
# Connect the record button to the record button action function
record_button = v['record_button']
record_button.action = record_action

# Connect the stop button to the stop button action function
stop_button = v['stop_button']
stop_button.action = stop_action

play_button = v['play_button']
play_button.action = play_button_pressed

def next_button_presses(sender):
  global seq_dont_increment,rec_seq
  seq_dont_increment=True
  rec_seq=rec_seq+1
  update_all()
  ui_update_all(sender)
  seq_dont_increment=False

def previous_button_presses(sender):
  global seq_dont_increment,rec_seq
  seq_dont_increment=True
  if rec_seq>0:
    rec_seq=rec_seq-1
  update_all()
  ui_update_all(sender)
  seq_dont_increment=False
 
   
next_button=v['next_button']
next
next_button.action=next_button_presses
previous_button=v['previous_button']
previous_button.action=previous_button_presses

#dir_base_
dir_base_textfield=v['dir_base_textfield']
dir_base_textfield.text=dir_base
#dir_base_ui_set(
	
#bn_textfield
bn_textfield= v['bn_textfield']
bn_textfield.text=rec_basename



#itrtextfield
itr_textfield=v['itr_textfield']
_initial_rec_seq=str(rec_seq)
itr_textfield.text =_initial_rec_seq

text_view = v['text_view']

langseg=v['langseg']
def ui_init(sender):
  global langseg,rec_seq
  update_all()
  langseg.selected_index=rec_seq
  ui_update_all(sender)
  #langseg_ui_changed(langseg)
  #enable_play_button_if()
  update_all()

#todo INIT
ui_init(v)



# Run the UI
v.present('sheet')

#todo ARGV LOGICS
if len(sys.argv) > 1:
    argument = sys.argv[1]
    print("Received Start Record argument:", argument)
    many=argument.split(' ')
    print(many)
    
    if len(many) > 1:
    	bnargument = many[1]
    	print("  Received basename argument:", bnargument)
    	if bnargument == '_':
    		bnargument='def_240427'
    	basename_ui_set(bnargument)
    	rec_basename=bnargument
    itr_argument=str(_initial_rec_seq)
    if len(many) > 2:
    	itr_argument = many[2]
    	print("  Received itr argument:", )
    	if itr_argument == '_':
    		itr_argument=1
    	itr_ui_set(itr_argument)
    	rec_seq=int(itr_argument)
    
    #dir_base
    
    
    if len(many) > 3:
    	dir_base_argument = many[3]
    	print("  Received dir_base argument:", )
    	dir_base_ui_set(dir_base_argument)
    	dir_base=dir_base_argument
    
    	
    update_all()
    startrec = True
    record_action(record_button)
else:
    print("No argument provided.")
