"""
    Written by Farhad Asadi, f.asadi2002@gmail.com

    This Python/Tkinter application crawls code review data through Gerrit REST API 
    and then uses matplotlib library to visualize the data.
"""
import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests



class CodeReviewData:
    """
        This class contains two functions, get_reviews() which crawls code review
        data through Gerrit REST API and filter_data() which filters the data crawled
        by get_reviews.
    """
    def get_reviews(self, start_date, end_date, platform):
        """
        Summary: This function crawls code review data from Gerrit REST API 
                    and then stores all the data into a list. The function 
                    then returns the list.
        Args:
            start_date (str): This date indicates the start date in the time period.
            end_date (str): This date indicates the end date in the time period.
            platform (str): This indicates what platform you want to crawl data for.
        Returns:
            if everything is successful:
                changes (list): The list contains all the reviews crawled from the Gerrit REST API
            if NOT successful:
                0: If there is a problem while crawling data then return 0.
        """
        changes = []
        start = 0
        url = ""
        max_review = 0
        if platform == "Android":
            android_url = f"https://android-review.googlesource.com/changes/?q=after:{start_date} before:{end_date}"
            url = android_url
            max_review = 2000
        elif platform == "OpenStack":
            openstack_url = f"https://review.opendev.org/changes/?q=after:{start_date} before:{end_date}"
            url = openstack_url
            max_review = 500
        elif platform == "Chromium":
            chromium_url = f"https://chromium-review.googlesource.com/changes/?q=after:{start_date} before:{end_date}"
            url = chromium_url
            max_review = 500
        else:
            return 0
        # Crawl more than max allowed review.
        while True:
            response = requests.get(url + f"&S={start}")
            if response.status_code != 200:
                return 0
            response_data = json.loads(response.content.decode('utf-8')[4:])
            changes.extend(response_data)
            if len(response_data) < max_review:
                break
            start += max_review

        # Check the last review. If the last review does not match the start_date
        # then call the get_reviews function.
        # The start_date is the same, but the end_date is not las_review.
        last_review = changes[-1]["updated"][:10]
        if last_review > start_date:
            new_changes = self.get_reviews(start_date, last_review, platform)
            changes = changes + new_changes
        return changes


    def filter_data(self, reviews_lst):
        """
        Summary: This function gets the list of reviews returned from the get_reviews
                function as an arg, filter the data, and
                then retuns a list that contains these filtered data.
        Args:
            reviews_lst (list): The list contains all code review data retuned from
            the get_review function.
        Returns:
            if successful:
                returned_data (type:list): When the data is filtered, it is stored in a
                                            list called returned_data.
            if NOT successful:
                0: when getting data from the get_reviews function, a problem might occur.
        """
        if reviews_lst == 0:
            return 0

        returned_data = []
        reviews_opened = {}
        reviews_closed = {}
        active_developers = {}
        developers_per_month = {}
        for change in reviews_lst:
            ################ Reviews opened and closed #################
            timestamp_str = change['updated'][:10]
            if timestamp_str not in reviews_opened:
                reviews_opened[timestamp_str] = 0
            if timestamp_str not in reviews_closed:
                reviews_closed[timestamp_str] = 0
            if change.get('status') == 'NEW':
                reviews_opened[timestamp_str] += 1
            elif change.get('status') in ['MERGED', 'ABANDONED']:
                reviews_closed[timestamp_str] += 1

            ############### Active developer per month ################
            timestamp_str = change['updated'][:19]
            timestamp = int(datetime.fromisoformat(timestamp_str).timestamp())
            date_ = datetime.fromtimestamp(timestamp)
            year_month = date_.strftime('%Y-%m')
            if 'owner' in change and '_account_id' in change['owner'] and change['owner']['_account_id'] is not None:
                if year_month not in active_developers:
                    active_developers[year_month] = set()
                active_developers[year_month].add(change["owner"]["_account_id"])
            if 'submitter' in change and '_account_id' in change['submitter'] and change['submitter']['_account_id'] is not None:
                if year_month not in active_developers:
                    active_developers[year_month] = set()
                active_developers[year_month].add(change["submitter"]["_account_id"])

        for year_month, developers in active_developers.items():
            developers_per_month[year_month] = len(developers)

        returned_data.append(reviews_opened)
        returned_data.append(reviews_closed)
        returned_data.append(developers_per_month)

        # Store the file in a JSON file valled data.json
        if os.path.exists("Storage/data.json") is True:
            os.remove("Storage/data.json")
            with open("Storage/data.json", "w") as outfile:
                json.dump(reviews_lst, outfile, indent=4)
        else:
            with open("Storage/data.json", "w") as outfile:
                json.dump(reviews_lst, outfile, indent=4)

        return returned_data

class GerritDataAnalyzer:
    # test is used for unit testing
    def __init__(self, test=False):
        self.root = tk.Tk()
        self.root.title("GerritDataAnalyzer")

        ico = Image.open('icon.png')
        photo = ImageTk.PhotoImage(ico)
        self.root.wm_iconphoto(False, photo)

        # This theme is available on GitHub: https://github.com/rdbende/Azure-ttk-theme.git
        self.root.tk.call("source", "azure.tcl")
        self.root.tk.call("set_theme", "dark")

        self.root.geometry("1498x943")
        self.root.minsize(1498, 943)

        img1 = ImageTk.PhotoImage(Image.open("open.png"))
        #print(type(img1))
        self.home_page(img1)
        if test == False:
            self.root.mainloop()

    def home_page(self, img1):
        """
        Summary: 
            This function creates a frame for the home screen.
        Args:
            img1 (PIL.ImageTk.PhotoImage): This is an image.
        """
        background_label = ttk.Label(self.root,
                                    text="GerritDataAnalyzer",
                                    font=("TkDefaultFont", 60, "bold"),
                                    foreground="grey")

        background_label.place(relx=0.5, rely=0.5, anchor="center")

        #global button_2
        tk.Button(self.root,
                    image=img1,
                    command=self.toggle_sidebar,
                    border=0,
                    bg='#262626',
                    activebackground='#262626').place(x=5,y=8)

    def change_theme(self):
        """
        Summary:
            This funciton is used to chage the theme of the application
        """
        current_theme = self.root.tk.call("ttk::style", "theme", "use")

        if current_theme == "azure-dark":
            self.root.tk.call("set_theme", "light")
            f1.config(bg="#F5F5F5")
            from_label.config(background="#F5F5F5")
            to_label.config(background="#F5F5F5")
            style_radio_frame.configure("Custom.TLabelframe", background="#F5F5F5")
        else:
            self.root.tk.call("set_theme", "dark")
            f1.config(bg="#191818")
            from_label.config(background="#191818")
            to_label.config(background="#191818")
            style_radio_frame.configure('Custom.TLabelframe', background='#191818')

    # When one of the entries are being clicked on, remove the background text.
    def when_entry_clicked(self, event, entry):
        """
        Summary:
            The function removes the background of the two entries when the
            user clicks on them. 

        Args:
            event : the type of event that triggered the function. This argument is
                    not used in the function, but it is included in the method signature
                    because it is required by the event binding system in tkinter.
            entry (ttk.entry): the entry widget that the user clicked on.
        """
        current_theme = self.root.tk.call("ttk::style", "theme", "use")
        if entry.get() == "Ex: 2022-01-01":
            entry.delete(0, "end")
            if current_theme == "azure-dark":
                entry.config(foreground="white")
            else:
                entry.config(foreground="black")
        elif entry.get() == "Ex: 2022-03-31":
            entry.delete(0, "end")
            if current_theme == "azure-dark":
                entry.config(foreground="white")
            else:
                entry.config(foreground="black")

    def validate_date_format(self, date_str1, date_str2):
        """
        Summary:
            This function validates the format of the dates being entered buy the user.
            The function also check if the start date is less (before, eariler) than end date
        Args:
            date_str1 (str): This is the start date
            date_str2 (str): This is the end date
        Returns:
            if everything ok:
                True: boolen
            if NOT ok:
                False: boolen
        """
        try:
            datetime.strptime(date_str1, "%Y-%m-%d")
            datetime.strptime(date_str2, "%Y-%m-%d")
            if date_str1 >= date_str2:
                return False
            return True
        except ValueError:
            return False

    def toggle_sidebar(self):
        """
        Summary:
            This function creates a sidebar for the application
        """
        global f1, from_label, to_label, style_radio_frame
        current_theme = self.root.tk.call("ttk::style", "theme", "use")
        if current_theme == "azure-dark":
            f1 = tk.Frame(self.root, width=500, height=1200, bg='#191818')
        else:
            f1 = tk.Frame(self.root, width=500, height=1200, bg='#f5f5f5')
        f1.place(x=0,y=0)

        # Platform; Creting radiobuttons for the user to choose the desired platform
        radio_frame = ttk.LabelFrame(f1, text="Platforms: ", padding=(40, 20))
        style_radio_frame = ttk.Style()
        current_theme = self.root.tk.call("ttk::style", "theme", "use")
        if current_theme == "azure-dark":
            style_radio_frame.configure("Custom.TLabelframe", background="#191818")
        else:
            style_radio_frame.configure('Custom.TLabelframe', background='#f5f5f5')
        radio_frame.configure(style="Custom.TLabelframe")
        radio_frame.place(relx=0.5, rely=0.35, anchor="center")

        var = tk.StringVar()
        # OpenStack is chosen by default
        var.set("OpenStack")
        android_radio_button = ttk.Radiobutton(radio_frame, text="Android", variable=var,
                                               value="Android", takefocus=False)
        android_radio_button.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        openStack_radio_button = ttk.Radiobutton(radio_frame, text="OpenStack", variable=var,
                                                 value="OpenStack", takefocus=False)
        openStack_radio_button.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        chromium_radio_button = ttk.Radiobutton(radio_frame, text="Chromium ", variable=var,
                                                value="Chromium", takefocus=False)
        chromium_radio_button.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # Creating two entries for the time perid; start and end
        # From date
        from_label = ttk.Label(f1, text="From:", font=("TkDefaultFont", 12), background=f1["bg"])
        from_label.place(relx=0.34, rely=0.51, anchor="center")
        entry1 = ttk.Entry(f1, font=("TkDefaultFont", 12), width=20, background="#2D2A2A")
        entry1.place(relx=0.5, rely=0.535, anchor="center")

        #  To date
        to_label = ttk.Label(f1, text="To: ", font=("TkDefaultFont", 12), background=f1["bg"])
        to_label.place(relx=0.33, rely=0.575, anchor="center")
        entry2 = ttk.Entry(f1, font=("TkDefaultFont", 12), width=20, background="#2D2A2A")
        entry2.place(relx=0.5, rely=0.6, anchor="center")

        entry1.insert("end", "Ex: 2022-01-01")
        entry1.config(foreground="gray")
        entry2.insert("end", "Ex: 2022-03-31")
        entry2.config(foreground="gray")

        entry1.bind("<FocusIn>", lambda event: self.when_entry_clicked(event, entry1))
        entry2.bind("<FocusIn>", lambda event: self.when_entry_clicked(event, entry2))

        def get_user_data_from_gui():
            """
            Summary:
                This funciton is where everything starts. The funciton extracts/gets the dates
                entered in the entries and the platfrom chosen by the user.
                The function then uses the validate_date_format to validate the dates. When
                the date is validated then function then calls the get_reviews function to crawl
                data. The function then passes the data from the get_reviews() to the filter_data()
                function in order to filter the data.The filtered data then is passed to the
                visulize_data() function.
            """
            from_date = entry1.get()
            to_date = entry2.get()
            platfrom = var.get()

            valid_date = self.validate_date_format(from_date, to_date)
            destroy_window()
            if valid_date is False:
                notebook = ttk.Notebook(self.root, width=1400, height=800)
                notebook.place(relx=0.5, rely=0.5, anchor="center")
                error_msg = ttk.Frame(notebook)
                notebook.add(error_msg, text="InputError!")
                the_message = ttk.Label(self.root,
                                    text="InputError: Either Wrong Date format(Expected format: 'YYYY-MM-DD')\nor start date is after the end date. Please try again! ",
                                    font=("TkDefaultFont", 20, "bold"),
                                    foreground="grey")

                the_message.place(relx=0.5, rely=0.5, anchor="center")

            else:
                reviews = CodeReviewData()
                reviews_lst = reviews.get_reviews(from_date, to_date, platfrom)
                returned_data = reviews.filter_data(reviews_lst)
                if returned_data == 0:
                    notebook = ttk.Notebook(self.root, width=1400, height=800)
                    notebook.place(relx=0.5, rely=0.5, anchor="center")
                    error_msg = ttk.Frame(notebook)
                    notebook.add(error_msg, text="Error!")
                    the_message = ttk.Label(self.root,
                                            text="APIError: There was an issue with the API. Please try again!",
                                            font=("TkDefaultFont", 20, "bold"),
                                            foreground="grey")
                    the_message.place(relx=0.5, rely=0.5, anchor="center")
                else:
                    reviews_opened = returned_data[0]
                    reviews_closed = returned_data[1]
                    developer_per_month = returned_data[-1]
                    self.visulize_data(reviews_opened, reviews_closed, developer_per_month)

        # Creating a submit button. When the submit is pressed the get_user_data_from_gui is called.
        submit_button = ttk.Button(f1, text="Submit", command=get_user_data_from_gui)
        submit_button.place(relx=0.5, rely=0.65, anchor="center")

        style = ttk.Style()
        style.configure('Custom.TButton', font=('TkDefaultFont', 9, 'bold'))

        # Creating a button for changing the theme of the application. When the button is pressed
        # the change_theme() function is called.
        change_theme_button = ttk.Button(f1,
                            text="Change Theme",
                            command=self.change_theme)
        change_theme_button.place(relx=0.5, rely=0.75, anchor="center")


        def destroy_window():
            """
            Summary:
                The funciton is used to destroy a frame/window and update the root frame
            """
            f1.destroy()
            self.root.update()

        # create a close button for closing the sidebar. An png file is used to visulize the button.
        global img2
        img2 = ImageTk.PhotoImage(Image.open("close.png"))

        tk.Button(f1,
                image=img2,
                border=0,
                command=destroy_window,
                bg='#262626',
                activebackground='#262626').place(x=450,y=10)

    def visulize_data(self, rev_opened, rev_closed, dev_per_month):
        """
            Summary:
                This function validates the format of the dates being entered buy the user.
                The function also check if the start date is less (before, eariler) than end date

            Args:
                rev_opened (dict): The rev_opened (reviews opened) is a dictionary that contains
                                    days ("YYYY-MM-DD") as keys and the number of reviews opened
                                    in that day as values.
                re_closed (dict): The rev_closed (reviews closed) is a dictionary that contains
                                    days ("YYYY-MM-DD") as keys and the number of reviews closed
                                    in that day as values.
                dev_per_month (dict): The dev_per_month (developers per month) is a ditionary that
                                    contains months ("YYYY-MM") as keys and the number of active
                                    developers in the month as values.
        """

        # The Gerrit REST API start fom the end date and then makes it way to the start date.
        # This is why we have to reverse the keys and values in these dictionaries.
        rev_opened_timestamp = list(rev_opened.keys())
        rev_opened_number = list(rev_opened.values())
        rev_opened_timestamp.reverse()
        rev_opened_number.reverse()

        rev_closed_timestamp = list(rev_closed.keys())
        rev_closed_number = list(rev_closed.values())
        rev_closed_timestamp.reverse()
        rev_closed_number.reverse()

        month = list(dev_per_month.keys())
        devs = list(dev_per_month.values())
        month.reverse()
        devs.reverse()

        # Creating a notebook in the middle of the application that can be used to plece the
        # graphs on
        notebook = ttk.Notebook(self.root, width=1400, height=800)
        notebook.place(relx=0.5, rely=0.5, anchor="center")

        # Creating a tab for each of the graph
        reviews_opened_and_closed_tab = ttk.Frame(notebook)
        active_developers_tab = ttk.Frame(notebook)
        reviews_opened = ttk.Frame(notebook)
        reviews_closed = ttk.Frame(notebook)

        # Adding these tabs on the notebook
        notebook.add(reviews_opened_and_closed_tab, text="Review Opened and Closed: ")
        notebook.add(reviews_opened, text="Reviews Opened: ")
        notebook.add(reviews_closed, text="Reviews Closed: ")
        notebook.add(active_developers_tab, text="Active developers per month: ")

        # Creating the graph using the create_graph() function and then exporting each graph as
        # a PDF file in the Storage/PDF_Files directory
        fig = self.create_graph(rev_opened_timestamp, rev_opened_number,
                                reviews_opened_and_closed_tab, "blue",
                                "Review Closed AND Opened", rev_closed_timestamp,
                                rev_closed_number)
        fig.savefig("Storage/PDF_Files/Rev_opened_closed.pdf")
        fig = self.create_graph(rev_opened_timestamp, rev_opened_number, reviews_opened,
                                "blue", "Review Opened")
        fig.savefig("Storage/PDF_Files/Rev_opened.pdf")
        fig = self.create_graph(rev_closed_timestamp, rev_closed_number, reviews_closed,
                                "red", "Reviews Closed")
        fig.savefig("Storage/PDF_Files/Rev_closed.pdf")
        fig = self.create_graph(month, devs, active_developers_tab,"blue",
                                "Developers per month", pie_chart=1)
        fig.savefig("Storage/PDF_Files/Dev_per_month.pdf")

    def create_graph(self, x1_labels, y1_labels, tab, color, title, x2_labels=None, y2_labels=None, pie_chart=None):
        """
        Summary:
            This function creates a graph. The type of the graph is base on the args sent
            to the function. The function creates two different types of graphs, plot or
            pie char. If the pie_chart is None, then it means the the function is ceating
            just a plot. But if the pie_chart is not None then, the function creates a pie chart. 
            The function can also create a plot for two types of data
            (reviews opened + reviews closed in the same plot). This only works if x2_labels and y2_labels is
            not None.
        Args:
            x1_labels (list): This is a list that contains all the labels for the x axis. These labels
                        are dates in this format: "YYYY-MM-DD"
            y1_labels (list): This is a list than contains all the labels for the y axis. These labels
                        are integers. 
            tab (ttk.Frame): This indicates in which tab should the graph be placed. 
            color (str): This indicates the color of the plot
            title (str): This indictes the title of the graph
            x2_labels (list, optional): Defaults to None. This is a list that contains all the labels
                                for the x axis. These labels are dates in this format: "YYYY-MM-DD"
            y2_labels (list, optional): Defaults to None. This is a list than contains all the labels for 
                                the y axis. These labels are integers. 
            pie_chart (int, optional): Defaults to None. This is use to indicate if the graphs
                                        is a plot or a pie chart.
        Returns:
            plt.Figure
        """
        plt.style.use('classic')
        fig = plt.Figure(figsize=(12, 6), dpi=100)
        ax = fig.add_subplot(111)
        ax.set_title(title)

        ############### Two graphs in one plot ##################
        if x2_labels is not None and y2_labels is not None and pie_chart is None:
            ax.plot(x1_labels, y1_labels, color="blue", label="Reviews Opened")
            ax.plot(x2_labels, y2_labels, color="red", label="Reviews Closed")
            ax.legend()
            ax.grid(which='major', axis='both', linestyle='--', linewidth=1,
                    color='#cfcfcf', alpha=0.2)
            ax.axvline(x=0, color='black', linestyle='-', linewidth=1)
            ax.set_facecolor('#a6a4a4')

        ################ Developers per month #####################
        elif pie_chart is not None:
            total_active_developers = sum(y1_labels)
            percentages = [(developers / total_active_developers) * 100 for developers in y1_labels]
            labels = x1_labels
            sizes = percentages

            colors = [(0.12156862745098039, 0.4666666666666667, 0.7058823529411765, 1.0),
                      (0.6823529411764706, 0.7803921568627451, 0.9098039215686274, 1.0),
                      (1.0, 0.7333333333333333, 0.47058823529411764, 1.0),
                      (0.596078431372549, 0.8745098039215686, 0.5411764705882353, 1.0),
                      (1.0, 0.596078431372549, 0.5882352941176471, 1.0),
                      (0.7725490196078432, 0.6901960784313725, 0.8352941176470589, 1.0),
                      (0.5490196078431373, 0.33725490196078434, 0.29411764705882354, 1.0),
                      (0.8901960784313725, 0.4666666666666667, 0.7607843137254902, 1.0),
                      (0.4980392156862745, 0.4980392156862745, 0.4980392156862745, 1.0),
                      (0.7372549019607844, 0.7411764705882353, 0.13333333333333333, 1.0),
                      (0.09019607843137255, 0.7450980392156863, 0.8117647058823529, 1.0),
                      (0.6196078431372549, 0.8549019607843137, 0.8980392156862745, 1.0)]

            _, _, autopcts = ax.pie(sizes, colors=colors, labels=labels, startangle=90,
                            autopct=lambda pct: f'{pct:.1f}% ({int(round(pct*total_active_developers/100))})',
                            textprops={'fontsize': 14})

            ax.set_title(f'Total Active Developers: {total_active_developers}', fontsize=20)
            for autopct in autopcts:
                autopct.set_fontsize(14)

        ################## Just one graph #########################
        else:
            max_y_value = max(y1_labels)
            if max_y_value < 50:
                ax.set_ylim(0, max_y_value + 1)
            ax.plot(x1_labels, y1_labels, color=color, label="Reviews Opened")
            ax.grid(which='major', axis='both', linestyle='--', linewidth=1,
                    color='#cfcfcf', alpha=0.2)
            ax.axvline(x=0, color='black', linestyle='-', linewidth=1)
            ax.set_facecolor('#a6a4a4')

        ################# Rotate the x labels ####################
        if len(x1_labels) > 12:
            fig.subplots_adjust(left=0.05, right=0.95, bottom=0.15, top=0.9, wspace=0.4, hspace=0.4)
            ax.tick_params(axis='x', labelrotation=90)
        else:
            fig.subplots_adjust(left=0.05, right=0.95, bottom=0.1, top=0.9, wspace=0.4, hspace=0.4)

        ax.spines['top'].set_color('#7d7a7a')
        ax.spines['right'].set_color('#7d7a7a')

        canvas = FigureCanvasTkAgg(fig, master=tab)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        return fig


if __name__ == "__main__":
    gda = GerritDataAnalyzer()
