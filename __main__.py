import ResumeBuilder
import ResumeBuilderGUI
import os

#TODO: make sure setting new information works (and make it look nicer with its own window)
#TODO: I know for a fact that reading from data.json["info"] works fine but maybe not writing to it

def main():
    #keeps track of all instances
    workListings, educationListings, skills, info = ResumeBuilder.loadData(os.getcwd()+"\\data.json")

    mainwindow = ResumeBuilderGUI.MainWindow()
    mainwindow.importData(workListings, educationListings, skills, info)
    mainwindow.updateListBox()
    mainwindow.mainloop()

if __name__ == "__main__":
    main()
