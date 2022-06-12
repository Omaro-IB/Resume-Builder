import os
import tkinter as tk
import ResumeBuilder
import json


class Listing:
    def __init__(self, name, startDate, endDate, subtitle, location, details, type_):
        self.name = name
        self.startDate = startDate
        self.endDate = endDate
        self.subtitle = subtitle
        self.location = location
        self.details = details
        self.type_ = type_



class Skills:
    def __init__(self, name, details):
        self.name = name
        self.details = details


class MainWindow():
    ROOT = tk.Tk()

    def __init__(self):
        self.information = [['Resume', 'John Doe', 'example@email.com', '(xxx)xxx-xxxx', 'Location', 'Your description telling your future employer a little about yourself goes here!']]
        self.dir = os.getcwd()
        self.dir = self.dir+"\\data.json"
        self.mainList = []
        self.scrollbar = tk.Scrollbar(MainWindow.ROOT, orient="vertical")

        self.listBox = tk.Listbox(MainWindow.ROOT, width=100)
        self.listBox.grid(row=0, column=1, rowspan=5)
        self.scrollbar.config(command=self.listBox.yview)
        self.scrollbar.grid(row=0, column=2, sticky='ns')

        self.createButt = tk.Button(MainWindow.ROOT, text="Create New", command=self.openCreateWindow)
        self.createButt.grid(row=0, column=3)

        self.editButt = tk.Button(MainWindow.ROOT, text="Edit", command=self.openEditWindow)
        self.editButt.grid(row=1, column=3)

        self.deleteButt = tk.Button(MainWindow.ROOT, text="Delete", command=self.deleteSelection)
        self.deleteButt.grid(row=2, column=3)

        self.upupButt = tk.Button(MainWindow.ROOT, text="/\\/\\", command=self.upupButton)
        self.upButt = tk.Button(MainWindow.ROOT, text="/\\", command=self.upButton)
        self.downButt = tk.Button(MainWindow.ROOT, text="\\/", command=self.downButton)
        self.downdownButt = tk.Button(MainWindow.ROOT, text="\\/\\/", command=self.downdownButton)
        self.upupButt.grid(row=4, column=3)
        self.upButt.grid(row=3, column=3)
        self.downButt.grid(row=3, column=4)
        self.downdownButt.grid(row=4, column=4)

        self.exportButt = tk.Button(MainWindow.ROOT, text="Export", command=self.exportButton)
        self.exportButt.grid(row=5, column=3)

        self.infoButt = tk.Button(MainWindow.ROOT, text="Change Header Information", command=self.openInfoWindow)
        self.infoButt.grid(row=6, column=1)

    def exportButton(self):
        self.workListingsRaw, self.educationListingsRaw, self.skillsRaw, self.information = ResumeBuilder.loadData(self.dir)
        ResumeBuilder.buildDocuments(self.workListingsRaw, self.educationListingsRaw, self.skillsRaw, self.information)

    def addToMainList(self, position, obj):
        self.mainList.insert(position, obj)
        #self.updateData(self.dir)
        #self.updateListBox()

    def deleteFromMainList(self, positions):
        for position in positions:
            del self.mainList[position]
        #self.updateData(self.dir)
        #self.updateListBox()

    def editMainList(self, position, obj):
        self.deleteFromMainList([position])
        self.addToMainList(position, obj)

    def reorderMainList(self, position, up):
        temp_class = self.mainList[position]
        self.deleteFromMainList([position])
        if up:
            self.mainList.insert(position - 1, temp_class)
        elif not up:
            self.mainList.insert(position + 1, temp_class)
        else:
            raise ValueError

    def reorderToEndMainList(self, position, up):
        temp_class = self.mainList[position]
        self.deleteFromMainList([position])
        if up:
            self.mainList.insert(0, temp_class)
        elif not up:
            self.mainList.insert(len(self.mainList), temp_class)
        else:
            raise ValueError

    def openCreateWindow(self):
        newWindow = tk.Toplevel(MainWindow.ROOT)
        newWindow.title("Create New Entry")
        newWindow.geometry("600x200")

        var = tk.IntVar()
        tk.Label(newWindow, text="Type:    ").grid(row=1, column=1)
        tk.Radiobutton(newWindow, text="Work", variable=var, value=1).grid(row=1, column=2)
        tk.Radiobutton(newWindow, text="Education", variable=var, value=2).grid(row=1, column=3)
        tk.Radiobutton(newWindow, text="Skills", variable=var, value=3).grid(row=1, column=4)
        tk.Label(newWindow, text="Name:    ").grid(row=2, column=1)
        nameEntry = tk.Entry(newWindow)
        nameEntry.grid(row=2, column=2)

        tk.Label(newWindow, text="Dates (N/A for Skills):    ").grid(row=3, column=1)
        startDateEntry = tk.Entry(newWindow)
        startDateEntry.grid(row=3, column=2)
        tk.Label(newWindow, text="to").grid(row=3, column=3)
        endDateEntry = tk.Entry(newWindow)
        endDateEntry.grid(row=3, column=4)

        tk.Label(newWindow, text="Subtitle (N/A for Skills):    ").grid(row=4, column=1)
        subtitleEntry = tk.Entry(newWindow)
        subtitleEntry.grid(row=4, column=2)

        tk.Label(newWindow, text="Location (N/A for Skills):    ").grid(row=5, column=1)
        locationEntry = tk.Entry(newWindow)
        locationEntry.grid(row=5, column=2)

        tk.Label(newWindow, text="Details ('|' seperated list):    ").grid(row=6, column=1)
        detailsEntry = tk.Entry(newWindow)
        detailsEntry.grid(row=6, column=2)

        def buttonPress():
            if var.get() == 1:
                self.addToMainList(0, Listing(nameEntry.get(), startDateEntry.get(), endDateEntry.get(), subtitleEntry.get(),
                           locationEntry.get(), (detailsEntry.get()).split("|"), "W"))
                self.updateListBox()
                self.updateData(self.dir)
            elif var.get() == 2:
                self.addToMainList(0, Listing(nameEntry.get(), startDateEntry.get(), endDateEntry.get(), subtitleEntry.get(),
                           locationEntry.get(), (detailsEntry.get()).split("|"), "E"))
                self.updateListBox()
                self.updateData(self.dir)
            elif var.get() == 3:
                self.addToMainList(0, Skills(nameEntry.get(), (detailsEntry.get()).split("|")))
                self.updateListBox()
                self.updateData(self.dir)
            newWindow.destroy()
            newWindow.update()

        tk.Button(newWindow, text="Add", command=buttonPress).grid(row=7, column=3)

    def openEditWindow(self):
        selection = self.listBox.curselection()[0]
        item = self.mainList[selection]
        if isinstance(item, Skills):
            type_ = "S"
            name_ = item.name
            details_ = item.details
            start_ = ''
            end_ = ''
            subtitle_ = ''
            location_ = ''
        elif isinstance(item, Listing):
            type_ = item.type_
            name_ = item.name
            details_ = item.details
            start_ = item.startDate
            end_ = item.endDate
            subtitle_ = item.subtitle
            location_ = item.location

        newWindow = tk.Toplevel(MainWindow.ROOT)
        newWindow.title("Edit Entry")
        newWindow.geometry("600x200")

        var = tk.IntVar()

        tk.Label(newWindow, text="Type:    ").grid(row=1, column=1)
        tk.Radiobutton(newWindow, text="Work", variable=var, value=1).grid(row=1, column=2)
        tk.Radiobutton(newWindow, text="Education", variable=var, value=2).grid(row=1, column=3)
        tk.Radiobutton(newWindow, text="Skills", variable=var, value=3).grid(row=1, column=4)
        tk.Label(newWindow, text="Name:    ").grid(row=2, column=1)
        if type_ == "W":
            var.set(1)
        elif type_ == "E":
            var.set(2)
        elif type_ == "S":
            var.set(3)

        nameEntry = tk.Entry(newWindow)
        nameEntry.grid(row=2, column=2)
        nameEntry.insert(tk.END, name_)

        tk.Label(newWindow, text="Dates (N/A for Skills):    ").grid(row=3, column=1)
        startDateEntry = tk.Entry(newWindow)
        startDateEntry.grid(row=3, column=2)
        tk.Label(newWindow, text="to").grid(row=3, column=3)
        endDateEntry = tk.Entry(newWindow)
        endDateEntry.grid(row=3, column=4)
        startDateEntry.insert(tk.END, start_)
        endDateEntry.insert(tk.END, end_)

        tk.Label(newWindow, text="Subtitle (N/A for Skills):    ").grid(row=4, column=1)
        subtitleEntry = tk.Entry(newWindow)
        subtitleEntry.grid(row=4, column=2)
        subtitleEntry.insert(tk.END, subtitle_)

        tk.Label(newWindow, text="Location (N/A for Skills):    ").grid(row=5, column=1)
        locationEntry = tk.Entry(newWindow)
        locationEntry.grid(row=5, column=2)
        locationEntry.insert(tk.END, location_)

        tk.Label(newWindow, text="Details ('|' seperated list):    ").grid(row=6, column=1)
        detailsEntry = tk.Entry(newWindow)
        detailsEntry.grid(row=6, column=2)
        detailsEntry.insert(tk.END, '|'.join(details_))

        def buttonPress():
            if var.get() == 1:
                self.deleteFromMainList([selection])
                self.addToMainList(selection, Listing(nameEntry.get(), startDateEntry.get(), endDateEntry.get(), subtitleEntry.get(),
                           locationEntry.get(), (detailsEntry.get()).split("|"), "W"))
                self.updateListBox()
                self.updateData(self.dir)
            elif var.get() == 2:
                self.deleteFromMainList([selection])
                self.addToMainList(selection, (nameEntry.get(), startDateEntry.get(), endDateEntry.get(), subtitleEntry.get(),
                           locationEntry.get(), (detailsEntry.get()).split("|"), "E"))
                self.updateListBox()
                self.updateData(self.dir)
            elif var.get() == 3:
                self.deleteFromMainList([selection])
                self.addToMainList(selection, Skills(nameEntry.get(), (detailsEntry.get()).split("|")))
                self.updateListBox()
                self.updateData(self.dir)
            newWindow.destroy()
            newWindow.update()

        tk.Button(newWindow, text="Confirm", command=buttonPress).grid(row=7, column=3)

    def openInfoWindow(self):
        newWindow = tk.Toplevel(MainWindow.ROOT)
        newWindow.title("Edit Heading Information")
        newWindow.geometry("700x200")

        tk.Label(newWindow, text="Other than your Name and Description, keep the number of entries consistent (seperate with '|')").grid(row=1, column=1)
        tk.Label(newWindow, text="Document Names (Seperate with '|')").grid(row=2, column=1)
        documentNamesEntry = tk.Entry(newWindow)
        documentNamesEntry.grid(row=2, column=2)
        tk.Label(newWindow, text="Your Name").grid(row=3, column=1)
        nameNameEntry = tk.Entry(newWindow)
        nameNameEntry.grid(row=3, column=2)
        tk.Label(newWindow, text="Emails (Seperate with '|')").grid(row=4, column=1)
        emailsEntry = tk.Entry(newWindow)
        emailsEntry.grid(row=4, column = 2)
        tk.Label(newWindow, text="Phones (Seperate with '|'").grid(row=5,column=1)
        phonesEntry = tk.Entry(newWindow)
        phonesEntry.grid(row=5,column=2)
        tk.Label(newWindow, text="Locations (Seperate with '|'").grid(row=6,column=1)
        locationsEntry = tk.Entry(newWindow)
        locationsEntry.grid(row=6,column=2)
        tk.Label(newWindow, text = "Description").grid(row=7,column=1)
        descriptionEntry = tk.Entry(newWindow)
        descriptionEntry.grid(row=7,column=2)

        docNames_ = []
        nameName_ = self.information[0][1]
        emails_ = []
        phones_ = []
        locations_ = []
        description_ = self.information[0][5]
        for item in self.information:
            docNames_.append(item[0])
            emails_.append(item[2])
            phones_.append(item[3])
            locations_.append(item[4])

        documentNamesEntry.insert(tk.END, "|".join(docNames_))
        nameNameEntry.insert(tk.END, nameName_)
        emailsEntry.insert(tk.END, "|".join(emails_))
        phonesEntry.insert(tk.END, "|".join(phones_))
        locationsEntry.insert(tk.END, "|".join(locations_))
        descriptionEntry.insert(tk.END, description_)

        def buttonPress():
            docNames = documentNamesEntry.get().split("|")
            nameName = nameNameEntry.get()
            emails = emailsEntry.get().split("|")
            phones = phonesEntry.get().split("|")
            locations = locationsEntry.get().split("|")
            description = descriptionEntry.get()
            self.information = []
            for i in range(len(docNames)):
                self.information.append([docNames[i], nameName, emails[i], phones[i], locations[i], description])
            self.updateData(self.dir)
            newWindow.destroy()
            newWindow.update()

        tk.Button(newWindow, text = "Submit", command = buttonPress).grid(row = 8, column=1)

    def deleteSelection(self):
        self.deleteFromMainList(self.listBox.curselection())
        self.updateData(self.dir)
        self.updateListBox()

    def upButton(self):
        self.reorderMainList(self.listBox.curselection()[0], True)
        self.updateData(self.dir)
        self.updateListBox()

    def downButton(self):
        self.reorderMainList(self.listBox.curselection()[0], False)
        self.updateData(self.dir)
        self.updateListBox()

    def upupButton(self):
        self.reorderToEndMainList(self.listBox.curselection()[0], True)
        self.updateData(self.dir)
        self.updateListBox()

    def downdownButton(self):
        self.reorderToEndMainList(self.listBox.curselection()[0], False)
        self.updateData(self.dir)
        self.updateListBox()

    def updateListBox(self):
        self.listBox.delete(0, tk.END)
        for item in self.mainList:
            if isinstance(item, Skills):
                self.listBox.insert(tk.END, "SKILL    |    " + item.name + "    |    " + str(item.details))
            elif isinstance(item, Listing):
                if item.type_ == "W":
                    self.listBox.insert(tk.END,
                                        "WORK    |    " + item.name + "    |    " + item.startDate + " - " + item.endDate + "    |    " + item.subtitle + "    |    " + item.location + "    |    " + str(
                                            item.details))
                elif item.type_ == "E":
                    self.listBox.insert(tk.END,
                                        "EDUCATION    |    " + item.name + "    |    " + item.startDate + " - " + item.endDate + "    |    " + item.subtitle + "    |    " + item.location + "    |    " + str(
                                            item.details))

    def importData(self, workListings, educationListings, skills, information):
        for work in workListings:
            self.mainList.append(
                Listing(work.name, work.start, work.end, work.subtitle, work.location, work.details, "W"))
        for edu in educationListings:
            self.mainList.append(Listing(edu.name, edu.start, edu.end, edu.subtitle, edu.location, edu.details, "E"))
        for skill in skills:
            self.mainList.append(Skills(skill[0], skill[1:]))
        self.information=information

    def updateData(self, dir):
        dictionary = {"skills": [], "work": [], "education": [], "info": []}
        for item in self.mainList:
            if isinstance(item, Listing):
                if item.type_ == "W":
                    dictionary["work"].append(
                        [item.name, item.startDate, item.endDate, item.subtitle, item.location, item.details])
                elif item.type_ == "E":
                    dictionary["education"].append([item.name, item.startDate, item.endDate, item.subtitle,
                                                   item.location, item.details])
                else:
                    raise ValueError("could not update data- item in mainlist of type Listing has bad type_ value")
            elif isinstance(item, Skills):
                dictionary["skills"].append([item.name, item.details])
            else:
                raise TypeError("could not update data- item in mainlist of not of type Listing or Skills")
        dictionary["info"] = self.information
        json_object = json.dumps(dictionary, indent=4)
        #os.remove(dir)
        file = open(dir, "w")
        file.write(json_object)
        file.close()

    def mainloop(self):
        MainWindow.ROOT.mainloop()

# importData("data.json")
# updateListBox()
