import sys
from PyQt5.QtWidgets import QApplication, QFileDialog
from gui import GUI
from section import MarkdownSection
import os
import datetime
import json
import pickle
import subprocess

# Pandoc file type conversion
def filetype_convert(md_input):
    filetype = os.path.splitext(md_input)[-1].lower()
    
    accepted_types = { #dict
        '.docx': 'docx',
        '.html': 'html',
        '.txt': 'markdown'
        #Add future filetypes here 
        #Refer to pandoc github readme
    }
    
    file_formats = accepted_types.get(filetype)
    if file_formats is None:
        raise ValueError(f'Invalid file type {filetype}')
    
    try: 
        result = subprocess.run(['pandoc', '--from', file_formats, '--to', 'markdown',
                                 md_input], capture_output = True, text = True)
        converted_markdown = result.stdout
        return converted_markdown
    
    #Error processing
    except FileNotFoundError:
        print("Pandoc execution failed: Is pandoc installed? Try 'pandoc --version'") 
    except Exception as error:
        print(f"Error. File {md_input} failed due to: {error}")
        return None
    

# Function to filter backslashes from Markdown input
def filter_backslash_lines(markdown_input):
    filtered_lines = []
    
    for line in markdown_input:
        if not line.startswith("\\"):
            filtered_lines.append(line)
    return filtered_lines

# Function to wrap file analysis logic
def read_and_analyze_file():
    sections = []
    current_heading = None
    current_content = ""
    all_content = ""
    all_word_count = 0
    heading_level = 0  
    heading_level_count = [0]*7  
    
    filepath, _ = QFileDialog.getOpenFileName(
        filter="Supported Files (*.txt *.md *.docx *.html *.rtf)")

    # Option 1 prints the whole path.@auth ZE
    file_path = filepath, _
    
    # Option 2 just gives you the filename itself @auth ZE
    file_name = os.path.basename(filepath)

    # Create a file Repository @auth ZE
    repo = './repository'
    if not os.path.exists(repo):
        os.makedirs(repo)
        print("Folder %s created." % repo)
    else:
        print("Folder already exists.")

    # If a file has been selected in the GUI...
    if filepath:
        '''
        Read an inputted Markdown file, then every time a header is detected in the file,
        create a Section instance (section.py class) and append that instance to the empty 
        list of Sections
        '''
        markdown_output = os.path.splitext(filepath)[0] + '_converted.md'

        #If the file is NOT markdown
        if not filepath.endswith('.md'):
            try:
                converted_markdown = filetype_convert(filepath)
                if converted_markdown is None:    
                    return
            
                markdown_input = converted_markdown.splitlines()
    
            except ValueError as error:
                print(error)
                return 

        else: 
            with open(filepath, 'r', encoding='utf-8') as file:
                markdown_input = file.readlines()
        
        filtered_input = filter_backslash_lines(markdown_input)

        for line in filtered_input:       # 
            if not line.startswith("#"):
                all_content += line if line.strip() != '' else '\n\n'
        all_word_count =  len(all_content.split())

        for line in filtered_input:
            if line.startswith("#"):
                if current_heading is not None:
                    sections.append(MarkdownSection(current_heading, heading_level, current_content,))
                    current_content = ""  # Reset the content for the next section.
                heading_level = line.count("#")
                heading_level_count[heading_level-1] += 1
                current_heading = line.strip("# \n")
            else:
                current_content += line if line.strip() != '' else '\n\n'

        if current_heading is not None:
            sections.append(MarkdownSection(current_heading, heading_level, current_content))

        header_count_total = sum(section.header_total for section in sections)
        report = f"File Name: {file_name}\n\n"
        report += f"Total Number of Headers: {header_count_total}\n\n"
        report += f"Total Number of Words: {all_word_count}\n\n"
        report += "-------------------------------\n\n"
        for i, section in enumerate(sections):
            report += str(section)  # Convert each section to a string and append it to the report
            if i < len(sections) - 1:
                report += '\n\n'  # Add a newline between sections

        for i in range(len(heading_level_count)):
            report += f'Heading level {i+1} : {heading_level_count[i]}\n'

        gui.text.setText(report)

    #create a text file for the repository
    file_count = 1
    for path in os.listdir("./repository"):
        if os.path.isfile(os.path.join("./repository" , path)):
            file_count +=1
    sn = str(file_count)
    repo_file = "repository-"+ file_name + "-" + sn + ".txt"
    with open (os.path.join( "./repository", repo_file), 'w') as f:
        f.write(report)


def save_report():
    filepath, _ = QFileDialog.getSaveFileName(filter="Text Files (*.txt)")
    if filepath:  
        report = gui.text.toPlainText()  # Get text from the text widget
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)

def retrieve_previous_report():
    sections = []
    filepath, _ = QFileDialog.getPreviousReport(filter="Text Files (*.txt)")
    with open(filepath, "r") as sections_in:
        
    
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = GUI()
    gui.select_button.clicked.connect(read_and_analyze_file)
    gui.save_button.clicked.connect(save_report)
    gui.history_button.clicked.connect(save_report)
    gui.styles()
    gui.show()
    sys.exit(app.exec_())
