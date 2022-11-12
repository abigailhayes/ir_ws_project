# Modules


# Create LaTex
with open('report.tex','w') as file:
    
    # Document set up
    file.write('\\documentclass{report}\n')
    file.write('\\usepackage{fullpage}\n')
    file.write('\\usepackage{url}\n')
    file.write('\\author{Multiple}\n')
    file.write('\\title{LILAS rankings}\n')
    
    # Start of document
    file.write('\\begin{document}\n')
    file.write('\\maketitle\n')
    file.write('\\tableofcontents\n')
    
    # Introduction chapter
    file.write('\\chapter{Introduction}\n')
    file.write('\\section{Task}\n')
    file.write('\\section{Approach overview}\n')
    
    # Pre-processing chapter
    file.write('\\chapter{Pre-processing the data}\n')
    file.write('\\section{Accessing the abstracts}\n')
    file.write('\\subsubsection{Initial data}\n')
    file.write('Example citation \cite{latex-help}\n')
    file.write('\\subsubsection{Using the super computer}\n')
    file.write('\\section{Pre-processing the text}\n')
    file.write('\\subsubsection{Pre-processing steps}\n')
    file.write('\\subsubsection{Impact of stopword removal}\n')
    file.write('\\section{Translation}\n')
    file.write('\\subsubsection{Google API}\n')
    file.write('\\subsubsection{Other approach}\n')
    
    # Bibliography
    file.write('\\bibliographystyle{abbrv}\n')
    file.write('\\bibliography{references}\n')
    
    # Finish document
    file.write('\\end{document}')
    

    
