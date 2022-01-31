from tkinter import *
from tkinter import messagebox
from functools import partial
from pathlib import Path
import ttkbootstrap as ttk, requests, os, subprocess, urllib.request, socket, zipfile, threading
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.toast import ToastNotification

categories = {}
programs = {}

MajorRelease = 0.0
MinorRelease = 0
FormattedReleaseVer = '0.0.0'
def opencategory(c):
	print(c)
def update_program():
	try:
		global verdata
		verdata = eval(requests.get('https://lolghuiy4tgfyu4th7tvtg.github.io/gamey/newestVersion.txt').content.decode('UTF-8'))
		if not isinstance(verdata, dict):
			return
		print(verdata)
		if MajorRelease > verdata['MajorRelease'] or MinorRelease > verdata['MinorRelease']:
			ttk.dialogs.Dialog("Do you want to update Gamey?").show()
	except:
		root = Tk()
		root.withdraw()
		messagebox.showerror(None, 'Can\'t connect to update server\n')
		print('Can\'t connect to update server\n')
		root.destroy()
def search_maptxt(url):
        try:
                map_base = requests.get(f'{url}/map.txt')
                m = map_base.content.decode('UTF-8')
                with open('latest_map.info', 'w+') as file:
                        file.write(m)
                print(m)
                m = m.split('\n')
        except:
                m = []
                with open('latest_map.info', 'r+') as file:
                        v = file.readlines()
                for x in v:
                	m.append(x.replace('\n', ''))
                print(m)
                
        l = m
        for x in l:
                if x in [' ', '|end|', '']:
                        del m[m.index(x)]
        print(' ')
        for thing in m:
                current_node = thing.split('|')
                if current_node[2] in ['swf', 'swf_package', 'html']:
                        programs[current_node[0]] = {'url':current_node[1], 'category':current_node[3], 'filetype':current_node[2]}
                        categories[current_node[3]]['proglist'].append(current_node[0])
                        if current_node[4] != 'None':
                        	programs[current_node[0]]['subcategory'] = str(current_node[4])
                        else:
                        	programs[current_node[0]]['subcategory'] = 0
                        try:
                        	if current_node[5] != 'None':
                        		programs[current_node[0]]['description'] = current_node[5].replace('\\n', '\n')
                        	else:
                        		programs[current_node[0]]['description'] = ' '
                        except KeyError:
                        	programs[current_node[0]]['description'] = ' '
                        except IndexError:
                        	programs[current_node[0]]['description'] = ' '

                        try:
                        	if current_node[5] != 'None':
                        		programs[current_node[0]]['author'] = current_node[6].replace('\\n', '\n')
                        	else:
                        		programs[current_node[0]]['author'] = ' '
                        except KeyError:
                        	programs[current_node[0]]['author'] = ' '
                        except IndexError:
                        	programs[current_node[0]]['author'] = ' '
                else:
                        categories[current_node[0]] = {'proglist':[], 'url':current_node[1]}

def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host) #Python 3.x
        return True
    except:
        return False
print('connected' if connect() else 'no internet!')

update_program()
search_maptxt('https://lolghuiy4tgfyu4th7tvtg.github.io/gamey/')

print('Categories: ')
for key, info in programs.items():
	ct = info['category']
	print(f'{key}   {ct}')

print('\nURLs: ')
for key, info in programs.items():
	ct = info['url']
	print(f'{key}       {ct}')

del categories['']
# Where the GUI Starts
try:
	with open('theme.info', 'r+') as f:
		theme_name = f.readlines()[0]
except FileNotFoundError:
	with open('theme.info', 'w+') as f:
		f.write('darkly')
	theme_name = 'darkly'
root = ttk.Window(themename=theme_name, title='Gamey Desktop')
root.geometry('800x215')
root.iconbitmap('ImgLib\\favicon.ico')
autodownload = BooleanVar(value=True)
sortby = StringVar(value='author')

paned = ttk.PanedWindow(root, orient=HORIZONTAL)
paned.pack(expand=1, fill='both')

sf = ScrolledFrame(paned, autohide=True)
sf.pack(fill='both', expand=1)
paned.add(sf.container)

details_paned = Frame(paned)
details_section = Frame(details_paned)
details_section.pack(anchor=CENTER)
paned.add(details_paned)

game_label = ttk.Label(details_section, text='Select a Game', bootstyle='primary')
game_label.grid(row=0, column=0, padx=10, pady=(5, 2))
game_type_label = ttk.Label(details_section, text='')
game_author_label = ttk.Label(details_section, text='', bootstyle='info')
game_desc_label = ttk.Label(details_section, text='')
game_play = ttk.Button(details_section, text='Play!', bootstyle="success", state=DISABLED)
game_play.grid(row=3, column=0, pady=5, padx=15)

'''
category_buttons = []
categories['POPO'] = {'proglist': ['akmvowev'], 'url': 'localhost:8090'}

for num, m in enumerate(categories.keys()):
	x = ttk.Button(sf, text=m, command=lambda:opencategory(lol))

num += 1
category_buttons.append(ttk.Button(sf, text='lol', command=lambda:opencategory(9)))
for t in category_buttons:
	t.pack(pady=5)
'''
button_identities = []
button_game_identities = []
def theme_change(*args):
	global theme_name
	themes = '''Litera
Minty
Lumen
Sandstone
Yeti
Pulse
United
Morph
Journal
Default (darkly)
Superhero
Cyborg
Solar
Vapor
Simplex
Cerculean'''.split('\n')
	def theme_preview():
		if combo.get().lower() == 'default (darkly)':
			ttk.Style().theme_use('darkly')
			return
		ttk.Style().theme_use(combo.get().lower())
	def apply_theme():
		global theme_name
		if combo.get().lower() == 'default (darkly)':
			with open('theme.info', 'w+') as f:
				f.write('darkly')
			ttk.Style().theme_use('darkly')
			theme_name = 'darkly'
			return
		with open('theme.info', 'w+') as f:
			f.write(combo.get().lower())
		ttk.Style().theme_use(combo.get().lower())
		theme_name = combo.get().lower()
	def cancel():
		with open('theme.info', 'r+') as f:
			ttk.Style().theme_use(f.readlines()[0])
		window.destroy()
	window = ttk.Toplevel(root)
	window.title('Gamey Settings - Change Theme')
	window.resizable(False, False)

	ttk.Label(window, text='Choose a New Theme').pack(pady=5)
	combo = ttk.Combobox(window, width=20, values=themes)
	combo.bind('<Button-1>', lambda x:theme_preview())
	if theme_name.title() == 'Darkly':
		combo.current(themes.index('Default (darkly)'))
	else:
		combo.current(themes.index(theme_name.title()))
	combo.pack(pady=10, fill=X, padx=10)

	control_frame = ttk.Frame(window)
	control_frame.pack(pady=5)
	left_controls = ttk.Frame(control_frame)
	left_controls.pack(side=RIGHT, padx=10)
	ttk.Button(control_frame, text='Cancel', command=cancel, bootstyle='danger').pack(side=LEFT, padx=(10, 70))

	ttk.Button(left_controls, text='Preview Theme', command=theme_preview).grid(row=0, column=0, padx=20)
	ttk.Button(left_controls, text='Apply', command=apply_theme, bootstyle='success').grid(row=0, column=1)

	window.wait_window()

def categories_view():
	global button_identities, button_game_identities
	button_identities = []
	for x in button_game_identities:
		x.destroy()
	for widget in sf.winfo_children():
		widget.destroy()
	def change(n):
	    # function to get the index and the identity (bname)
	    print(n)
	    bname = (button_identities[n])
	    cate = bname['text']
	    print(cate)
	    bname.configure(text = "Getting Games")
	    games_in_category(cate)

	if sortby.get() != 'category':
		iterable_thingy = set()
		for g in programs.values():
			if g[sortby.get()] == '' or g[sortby.get()] == ' ' or g[sortby.get()] == '  ':
				continue
			iterable_thingy.add(g[sortby.get()])
	else:
		iterable_thingy = categories.keys()
	for i, string in enumerate(iterable_thingy):
	    # creating the buttons, assigning a unique argument (i) to run the function (change)
	    button = ttk.Button(sf, width=10, text=str(string), command=partial(change, i))
	    button.pack(fill=X)
	    # add the button's identity to a list:
	    button_identities.append(button)
current_game = None
download_thread = None
def download(cate, main_fs_path):
	if programs[cate]['filetype'] == 'swf':
		file = requests.get(programs[cate]['url']).content
		print(main_fs_path)
		Path(f"{programs[cate]['category']}\\{cate}\\").mkdir( parents=True, exist_ok=True )
		with open(f'{programs[cate]["category"]}\\{cate}\\temp.swf', 'wb') as fs:
			fs.write(file)
	elif programs[cate]['filetype'] == 'html':
		file = requests.get(programs[cate]['url']).content
		print(main_fs_path)
		Path(main_fs_path).mkdir( parents=True, exist_ok=True )
		with open(f'HTML Runtime\\{programs[cate]["category"]}\\{cate}\\package.zip', 'wb') as fs:
			fs.write(file)
		with zipfile.ZipFile(f'HTML Runtime\\{programs[cate]["category"]}\\{cate}\\package.zip', 'r') as zip_ref:
			zip_ref.extractall(f'HTML Runtime\\{programs[cate]["category"]}\\{cate}\\')
		os.remove(f'HTML Runtime\\{programs[cate]["category"]}\\{cate}\\package.zip')
		with open('HTML Runtime\\package.json', 'w+') as file:
			bracket = '{'
			bracket2 = '}'
			thing = f'''{bracket}
	"main": "{programs[cate]["category"]}/{cate}/index.html",
	"name": "Gamey HTML Runtime (Based on NW.JS)"
{bracket2}'''
			file.write(thing)
def download_done_check(cate, path):
	global download_thread
	if not download_thread.is_alive():
		game_label['text'] = cate
		game_play['state'] = 'enabled'
		toast = ToastNotification(
		    title="Gamey Desktop",
		    message=f'Download of "{cate}" is complete!',
		    duration=3000,
		)
		toast.show_toast()
		if programs[cate]['filetype'] == 'swf':
			subprocess.Popen(['flashruntime.exe', f'{path}\\temp.swf'])
		elif programs[cate]['filetype'] == 'html':
			subprocess.Popen('HTML Runtime\\nw.exe')
	else:
		root.after(500, lambda: download_done_check(cate, path))
def rungame(cate):
	global download_thread
	if programs[cate]['filetype'] == 'swf':
		main_fs_path = f"{programs[cate]['category']}\\{cate}"
		file_in_question = f'{main_fs_path}\\temp.swf'
		if connect() and autodownload.get() == True:
			game_label['text'] = 'Downloading ...'
			game_play['state'] = DISABLED

			download_thread = threading.Thread(target=lambda: download(cate, main_fs_path))
			download_thread.start()
			download_done_check(cate, main_fs_path)
		elif os.path.isfile(file_in_question):
			subprocess.Popen(['flashruntime.exe', f'{main_fs_path}\\temp.swf'])
		else:
			messagebox.showerror('Gamey Desktop', 'SWF File Not Found.\nTry again when connected to the internet.\n\nError Code: SWF-1')
		
	elif programs[cate]['filetype'] == 'swf_package':
		main_fs_path = f"{programs[cate]['category']}\\{cate}"
		file_in_question = f'{main_fs_path}\\game_link.txt'
		if connect() and autodownload.get() == True:
			file = requests.get(programs[cate]['url']).content
			print(main_fs_path)
			Path(main_fs_path).mkdir( parents=True, exist_ok=True )
			with open(f'{programs[cate]["category"]}\\{cate}\\package.zip', 'wb') as fs:
				fs.write(file)
			with zipfile.ZipFile(f'{programs[cate]["category"]}\\{cate}\\package.zip', 'r') as zip_ref:
				zip_ref.extractall(f'{programs[cate]["category"]}\\{cate}\\')
			key = open(f'{programs[cate]["category"]}\\{cate}\\game_link.txt', 'r+').read().replace('\n', '')
			subprocess.Popen(['flashruntime.exe', f'{programs[cate]["category"]}\\{cate}\\{key}'])
		elif os.path.isfile(file_in_question):
			key = open(f'{programs[cate]["category"]}\\{cate}\\game_link.txt', 'r+').read().replace('\n', '')
			subprocess.Popen(['flashruntime.exe', f'{main_fs_path}\\{key}'])
		else:
			messagebox.showerror('Gamey Desktop', 'SWF Package Not Found.\nTry again when connected to the internet.\n\nError Code: PKG-1')
	
	elif programs[cate]['filetype'] == 'html':
		main_fs_path = f"HTML Runtime\\{programs[cate]['category']}\\{cate}"
		file_in_question = f"HTML Runtime\\{programs[cate]['category']}\\{cate}\\index.html"
		if connect() and autodownload.get() == True:
			game_label['text'] = 'Downloading ...'
			game_play['state'] = DISABLED

			download_thread = threading.Thread(target=lambda: download(cate, main_fs_path))
			download_thread.start()
			download_done_check(cate, main_fs_path)
		elif os.path.isfile(file_in_question):
			with open('HTML Runtime\\package.json', 'w+') as file:
				bracket = '{'
				bracket2 = '}'
				thing = f'''{bracket}
	"main": "{programs[cate]["category"]}/{cate}/index.html",
	"name": "Gamey HTML Runtime (Based on NW.JS)"
{bracket2}'''
				file.write(thing)
				del thing
			subprocess.Popen('HTML Runtime\\nw.exe')
		else:
			messagebox.showerror('Gamey Desktop', 'HTML Application Not Found.\nTry again when connected to the internet.\n\nError Code: NW-1')

def games_in_category(c):
        global button_identities, button_game_identities, current_game
        button_game_identities = []
        if c == 'Other' and sortby.get() == 'author':
        	c == ' '
        for x in button_identities:
                x.destroy()
        def change_c(n):
                global current_game
                # function to get the index and the identity (bname)
                print(n)
                bname = (button_game_identities[n])
                cate = bname['text']
                current_game = cate
                print(cate)

                bname.configure(text = "Getting Game")

                game_play['state'] = 'enabled'
                game_type_label.grid_forget()
                game_type_label.grid(row=2, column=0, pady=5)
                game_author_label.grid_forget()

                game_desc_label.grid_forget()
                game_desc_label.grid(row=4, column=0, pady=5)
                if programs[cate]['description'] != '' and programs[cate]['description'] != ' ':
                	game_desc_label['text'] = f"Desc: {programs[cate]['description']}"
                else:
                	game_desc_label['text'] = f" "

                game_type_label['text'] = f"Category: {programs[cate]['category']}"
                if not programs[cate]["author"] in [' ', '']:
                	game_author_label['text'] = f'by {programs[cate]["author"]}'
                	game_author_label.grid(row=1, column=0, pady=0)
                else:
                	game_author_label['text'] = f''
                game_label['text'] = cate
                game_play['command'] = lambda: rungame(cate)
                bname.configure(text = cate)

        f = 0
        temp_data = []
        for m in programs.keys():
                if not programs[m][sortby.get()] == c:
                        continue
                temp_data.append(m)


        lok = enumerate(temp_data)
        for i, string in lok:
                if programs[string]['subcategory'] and sortby.get() == 'category':
                	ttk.Label(sf, text=programs[string]['subcategory'], bootstyle='secondary').pack(pady=(4, 2))
                	ttk.Separator(sf, orient=HORIZONTAL).pack(fill=X, padx=2, pady=(2, 4))
                # creating the buttons, assigning a unique argument (i) to run the function (change)
                button = ttk.Button(sf, width=10, text=str(string), command=partial(change_c, i))
                button.pack(fill=X)
                # add the button's identity to a list:
                button_game_identities.append(button)
                f = i

        button = ttk.Button(sf, width=10, text='Back ...', command=categories_view)
        button.pack(fill=X)
        button_game_identities.append(button)
        del temp_data

categories_view()

m = Menu(root)
root['menu'] = m

preferences = Menu(m)
m.add_cascade(menu=preferences, label='Settings')
preferences.add_command(label='Change Theme', command=theme_change)
preferences.add_checkbutton(label='Auto-Download Games', variable=autodownload, onvalue=True, offvalue=False)
preferences.add_separator()
preferences.add_radiobutton(label='Sort by Category', variable=sortby, value='category', command=categories_view)
preferences.add_radiobutton(label='Sort by Author', variable=sortby, value='author', command=categories_view)

root.bind('<Configure>', lambda x: root.update_idletasks())
root.mainloop()
