
from urllib.request import urlopen
from webbrowser import open as urldisplay
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar
from re import findall, finditer, MULTILINE, DOTALL
from sqlite3 import *

#--------------------------------------------------------------------#
#
# A function to download and save a web document. If the
# attempted download fails, an error message is written to
# the shell window and the special value None is returned.
#
# Parameters:
# * url - The address of the web page you want to download.
# * target_filename - Name of the file to be saved (if any).
# * filename_extension - Extension for the target file, usually
#      "html" for an HTML document or "xhtml" for an XML
#      document.
# * save_file - A file is saved only if this is True. WARNING:
#      The function will silently overwrite the target file
#      if it already exists!
# * char_set - The character set used by the web page, which is
#      usually Unicode UTF-8, although some web pages use other
#      character sets.
# * lying - If True the Python function will try to hide its
#      identity from the web server. This can sometimes be used
#      to prevent the server from blocking access to Python
#      programs. However we do NOT encourage using this option
#      as it is both unreliable and unethical!
# * got_the_message - Set this to True once you've absorbed the
#      message above about Internet ethics.
#
def download(url = 'http://www.wikipedia.org/',
             target_filename = 'download',
             filename_extension = 'html',
             save_file = True,
             char_set = 'UTF-8',
             lying = False,
             got_the_message = False):

    # Import the function for opening online documents and
    # the class for creating requests
    from urllib.request import urlopen, Request

    # Import an exception raised when a web server denies access
    # to a document
    from urllib.error import HTTPError

    # Open the web document for reading
    try:
        if lying:
            # Pretend to be something other than a Python
            # script (NOT RELIABLE OR RECOMMENDED!)
            request = Request(url)
            request.add_header('User-Agent', 'Mozilla/5.0')
            if not got_the_message:
                print("Warning - Request does not reveal client's true identity.")
                print("          This is both unreliable and unethical!")
                print("          Proceed at your own risk!\n")
        else:
            # Behave ethically
            request = url
        web_page = urlopen(request)
    except ValueError:
        print("Download error - Cannot find document at URL '" + url + "'\n")
        return None
    except HTTPError:
        print("Download error - Access denied to document at URL '" + url + "'\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to download " + \
              "the document at URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Read the contents as a character string
    try:
        web_page_contents = web_page.read().decode(char_set)
    except UnicodeDecodeError:
        print("Download error - Unable to decode document from URL '" + \
              url + "' as '" + char_set + "' characters\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to decode " + \
              "the document from URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Optionally write the contents to a local text file
    # (overwriting the file if it already exists!)
    if save_file:
        try:
            text_file = open(target_filename + '.' + filename_extension,
                             'w', encoding = char_set)
            text_file.write(web_page_contents)
            text_file.close()
        except Exception as message:
            print("Download error - Unable to write to file '" + \
                  target_filename + "'")
            print("Error message was:", message, "\n")

    # Return the downloaded document to the caller
    return web_page_contents

#
#--------------------------------------------------------------------#



#--------------------------------------------------------------------#
#
# A function to open a local HTML file in your operating
# system's default web browser.  (Note that Python's "webbrowser"
# module does not guarantee to open local files, even if you use a
# 'file://..." address).  The file to be opened must be in the same
# folder as this module.
#
# Since this code is platform-dependent we do NOT guarantee that it
# will work on all systems.
#
def open_html_file(file_name):
    
    # Import operating system functions
    from os import system
    from os.path import isfile
    
    # Remove any platform-specific path prefixes from the
    # filename
    local_file = file_name[file_name.rfind('/') + 1:] # Unix
    local_file = local_file[local_file.rfind('\\') + 1:] # DOS
    
    # Confirm that the file name has an HTML extension
    if not local_file.endswith('.html'):
        raise Exception("Unable to open file " + local_file + \
                        " in web browser - Only '.html' files allowed")
    
    # Confirm that the file is in the same directory (folder) as
    # this program
    if not isfile(local_file):
        raise Exception("Cannot find file " + local_file + \
                        " in the same folder as this program")
    
    # Collect all the exit codes for each attempt
    exit_codes = []
    
    # Microsoft Windows: Attempt to "start" the web browser
    code = system('start ' + local_file)
    if code != 0:
        exit_codes.append(code)
    else:
        return 0
    
    # Apple macOS: Attempt to "open" the web browser
    code = system("open './" + local_file + "'")
    if code != 0:
        exit_codes.append(code)       
    else:
        return 0
    
    # Linux: Attempt to "xdg-open" the local file in the
    # web browser
    code = system("xdg-open './" + local_file + "'")
    if code != 0:
        exit_codes.append(code)       
    else:
        return 0
    
    # Give up!
    raise Exception('Unable to open file ' + local_file + \
                    ' in web browser - Exit codes: ' + \
                    str(exit_codes))



#--------------------------------------------------------------------#
# Window Setup
#--------------------------------------------------------------------#

# Create a window
runners_up = Tk()
runners_up.geometry('500x720')

# Give the window a title
runners_up.title('Second Place?')

# Set the background colour
colour_theme = 'Lemon Chiffon'
runners_up['bg'] = colour_theme


#--------------------------------------------------------------------#
# Variable Storage
#--------------------------------------------------------------------#

# Store html, key, title, attribute
html_store = ['top10_instagram.html',
              'https://youtube.fandom.com/wiki/Most_Subscribed_YouTube_Channels',
              'https://phlanx.com/top/twitch/followers/50',
              'https://en.wikipedia.org/wiki/List_of_most-followed_TikTok_accounts']

key_store = ['</span></td><td><span>',
             '</a>[\n\s]+</td><td>',
             '</a></div><div class="top_lists_followers"> <span class="top_lists_labels">Followers :</span> <span class="plus_count" style="">',
             '[</a>\n\s]+</td>[\n\s]+<td style="text-align:center;">']

title_store = ["Instagram [previous]",
               "Youtube [live]",
               "Twitch TV [live]",
               "TikTok [live]"]

attribute_store = ' Mill Follows'

positions = ['\n1st:  ', '2nd:  ', '\n3rd:  ', '\n4th:  ', '\n5th:  ', '\n6th:  ', '\n7th:  ',
             '\n8th:  ', '\n9th:  ', '\n10th: ']


#--------------------------------------------------------------------#
# Button Functions
#--------------------------------------------------------------------#



# Define button press of top 10 retrieval
def top10_button_press():
    if str(select_box.get(select_box.curselection())) == select_box_entries[0]:
        list_retrieval(0)
    elif str(select_box.get(select_box.curselection())) == select_box_entries[1]:
        list_retrieval(1)
    elif str(select_box.get(select_box.curselection())) == select_box_entries[2]:
        list_retrieval(2)
    elif str(select_box.get(select_box.curselection())) == select_box_entries[3]:
        list_retrieval(3)


# Function to retrieve top 10 list when given the option number
def list_retrieval(num):
    
    # Access the document
    if str(select_box.get(select_box.curselection())) == select_box_entries[0]:
        text_file = open(html_store[num])
        contents = text_file.read()
        text_file.close()
    else:
        try:
            web_page = urlopen(html_store[num])
            web_page_bytes = web_page.read()
            web_page_chars = web_page_bytes.decode()
            contents = web_page_chars
        except:
            attribute_box.delete(1.0, END)
            title_box.delete(1.0, END)
            title_box.insert(END, '\nError in Page Download\nPlease Try Again')
            return

    # Extract search term
    search_term = '>([51A-Za-z\s\.\(\)\-\_\']+)' + key_store[num] + '([\$0-9,\.,]+)[A-Z\n<]'
    title_attribute_list = findall(search_term, contents)
    title_attribute_list = title_attribute_list[0:10]

    # List the results
    global title_list
    global attribute_list
    title_list = []
    attribute_list = []
    for each in title_attribute_list:
        title_list.append(each[0])
        attribute_list.append(each[1])

    # Return results to GUI
    n = 0
    attribute_box.delete(1.0, END)
    title_box.delete(1.0, END)
    title_box.insert(END, positions[1] + str(title_list[1] + '\n'))
    for title in title_list:
        if title != title_list[1]:
            title_box.insert(END, positions[n] + str(title))
        n = n + 1
    attribute_box.insert(END, str(attribute_list[1] + attribute_store + '\n\n'))
    for attribute in attribute_list:
        if attribute != attribute_list[1]:
            attribute_box.insert(END, str(attribute) + attribute_store + '\n')



# Define button press of show source
def source_button_press():
    if str(select_box.get(select_box.curselection())) == select_box_entries[0]:
        open_html_file(html_store[0])
    elif str(select_box.get(select_box.curselection())) == select_box_entries[1]:
        urldisplay(html_store[1])
    elif str(select_box.get(select_box.curselection())) == select_box_entries[2]:
        urldisplay(html_store[2])
    elif str(select_box.get(select_box.curselection())) == select_box_entries[3]:
        urldisplay(html_store[3])



# Define button press of save to db
def db_save():
    
    # Get values
    top10_button_press()
    
    # Delete the old values from the db
    connection = connect(database = 'runners_up.db')
    runners_up_db = connection.cursor()
    sql = "DELETE FROM runner_up;"
    runners_up_db.execute(sql)
    sql = "DELETE FROM others;"
    runners_up_db.execute(sql)

    # Find the relevant list and execute the values into db
    sql = "INSERT INTO runner_up(competitor,property) VALUES('name','attribute');"
    try:
        sql = sql.replace('name', title_list[1])
        sql = sql.replace('attribute',attribute_list[1])
    except:
        attribute_box.delete(1.0, END)
        title_box.delete(1.0, END)
        title_box.insert(END, '\nError in Page Download\nPlease Try Again')
        return
    runners_up_db.execute(sql)
    n = 0
    for title in title_list:
        if n != 1:
            sql = "INSERT INTO others(position,competitor,property) VALUES('place','name','attribute');"
            sql = sql.replace('place', str(n+1))
            sql = sql.replace('name',title_list[n])
            sql = sql.replace('attribute',attribute_list[n])
            runners_up_db.execute(sql)
        n = n + 1
    connection.commit()
    runners_up_db.close()
    connection.close()



#--------------------------------------------------------------------#
# Create Widgets
#--------------------------------------------------------------------#

# Create the selection box
select_box = Listbox(runners_up, width = 44, height = 0, font = ('Arial', 15),
                   justify = CENTER, bg = colour_theme, borderwidth = 2, relief = 'solid',)
select_box_entries = title_store
for selections in select_box_entries:
    select_box.insert(END, selections)

# Create a description label
description_label = Label(runners_up, text = 'Select an option to find the top 10 influencers and their follower counts',
                          font = ('Arial',12),
                          bg = colour_theme)

# Create the buttons
find_second_place_button = Button(runners_up, text = 'Find Top 10', font = ('Arial',12),
                                  command = top10_button_press, bg = colour_theme,
                                  borderwidth = 2, relief = 'solid',
                                  width = 15, height = 2)
source_button = Button(runners_up, text = 'Retrieve Source', command = source_button_press,
                       borderwidth = 2, relief = 'solid', font = ('Arial',12), bg = colour_theme, width = 15, height = 2)
save_button = Button(runners_up, text = 'Save to DB', bg = colour_theme, width = 15,
                     command = db_save, borderwidth = 2, relief = 'solid',
                     font = ('Arial',12), height = 2)

# Create the textboxs
attribute_box = Text(runners_up, width = 20, height = 12,
                     bg = colour_theme, bd = 0)
title_box = Text(runners_up, width = 40, height = 12, bg = colour_theme,
                      bd = 0)

# Create the label image
image_canvas = Canvas(runners_up, width = 475, height = 280, bg = colour_theme,
                      borderwidth = 2, relief = 'solid')
img = PhotoImage(file = 'img.gif')
image_canvas.create_image(0,0, anchor = NW, image = img)

# Arrange the window
margin = 5
description_label.grid(column = 0, row = 2, pady = 5)
find_second_place_button.grid(padx = margin, pady = margin, column = 0, row = 3)
source_button.grid(padx = margin, pady = margin, column = 0, row = 3, sticky = 'w')
save_button.grid(padx = margin, pady = margin, row = 3, column = 0, sticky = 'e')
select_box.grid(padx = margin, pady = margin, row = 1, column = 0)
attribute_box.grid(padx = margin, pady = margin, row = 5, column = 0, sticky = 'e')
title_box.grid(padx = margin, pady = margin, row = 5, column = 0, sticky = 'w')
image_canvas.grid(padx = 10, pady = 10, row = 0, column = 0)



