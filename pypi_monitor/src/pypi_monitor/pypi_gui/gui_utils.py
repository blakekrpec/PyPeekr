from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt


# Set the background color for the main window (and other windows as needed)
def set_main_background_color(main_window, color):
    # convert hex to QColor
    q_color = QColor(color)

    # grab the current stylesheets, and append with new color
    main_window.setStyleSheet(main_window.styleSheet() +
                              f'background-color: {q_color.name()};')

    main_window.settings_button.setStyleSheet(
        main_window.settings_button.styleSheet() +
        f'background-color: {q_color.name()};')

    # for some reason in windows this doesn't properly color the tabs
    # but in linux it does
    main_window.settings_controller.settings_dialog.tab_widget.setStyleSheet(
        main_window.settings_controller.settings_dialog.
        tab_widget.styleSheet() +
        f'background-color: {q_color.name()};')

    main_window.settings_controller.settings_dialog.setStyleSheet(
        main_window.settings_controller.settings_dialog.styleSheet() +
        f'background-color: {q_color.name()};')

    main_window.settings_controller.settings_dialog.view_settings_page. \
        displays_dialog.setStyleSheet(
            main_window.settings_controller.
            settings_dialog.view_settings_page.
            displays_dialog.styleSheet() +
            f'background-color: {q_color.name()};')

    main_window.settings_controller.settings_dialog.file_settings_page \
        .ip_dialog.setStyleSheet(
            main_window.settings_controller.settings_dialog.file_settings_page.
            ip_dialog.styleSheet() +
            f'background-color: {q_color.name()};')

    # call pane manager to also update pane colors
    main_window.pane_manager.update_panes()


# Set the font color for entire app
def set_main_font_color(main_window, color):
    # convert hex to QColor
    q_color = QColor(color)

    # first update fonts whose stylesheets of all widgets we know will exist
    # (things that can't be disabled/toggled on/off)
    # grab the current style sheets, and append with new color
    main_window.setStyleSheet(main_window.styleSheet() +
                              f'color: {q_color.name()};')

    main_window.settings_button.setStyleSheet(
        main_window.settings_button.styleSheet() +
        f'color: {q_color.name()};')

    main_window.settings_controller.settings_dialog.setStyleSheet(
        main_window.settings_controller.settings_dialog.styleSheet() +
        f'color: {q_color.name()};')

    main_window.settings_controller.settings_dialog.view_settings_page. \
        displays_dialog.setStyleSheet(
            main_window.settings_controller.
            settings_dialog.view_settings_page.
            displays_dialog.styleSheet() +
            f'color: {q_color.name()};')

    main_window.settings_controller.settings_dialog.file_settings_page \
        .ip_dialog.setStyleSheet(
            main_window.settings_controller.settings_dialog.file_settings_page.
            ip_dialog.styleSheet() +
            f'color: {q_color.name()};')

    # for the actual data panes we just save as a setting and then grab that
    # setting when constructing their style sheets
    # this is because that seemed easier than using logic to see which panes
    # were running, and then updating the appropriate panes
    main_window.settings["font-color"] = q_color.name()

    # # call pane manager to also update pane colors
    main_window.pane_manager.update_panes()


# class that creates a pane for each enabled display
# it also keeps all relevant lists regarding panes, up to date
# update_pane_controller() is only function to call externally
class PaneManager:
    def __init__(self, main_window):
        # define main window, and call update_panes() on startup
        self.main_window = main_window
        self.update_panes()

    # listens to main.window.settings to update list of enabled panes
    def create_pane_lists(self):
        # update panes_status list according to current setting
        if self.main_window.settings["displays"]["CPU"]["enabled"] is True:
            self.panes_status["CPU"] = True
        else:
            self.panes_status["CPU"] = False

        if self.main_window.settings["displays"]["GPU"]["enabled"] is True:
            self.panes_status["GPU"] = True
        else:
            self.panes_status["GPU"] = False

    # function that creates a simple pane with correct title
    def create_pane(self, title):
        # create the pane for "title" and store in panes list
        self.panes[title] = QWidget(self.main_window)

        # Spawn a PaneController for this new pane, and store it in list
        self.panes_controllers[title] = (
            PaneController(title, self.panes[title], self.main_window))

        # define pane color
        color = self.main_window.settings["displays"][title]["color"]
        font_color = self.main_window.settings["font_color"]

        # define pane stylesheet and apply
        settings = (
            f"background-color: {color}; "
            "margin:2px; "
            "border:0px solid rgb(0, 0, 0); "
            "border-radius:20px;"
            f"color: {font_color};"
        )
        self.panes[title].setStyleSheet(settings)

    # function that recursively calls create_pane()
    def create_panes(self):
        # loop over all pane statuses
        for pane_name, is_enabled in self.panes_status.items():
            # if pane is enabled
            if is_enabled:
                # create panes for enabled displays
                self.create_pane(pane_name)
                # add enabled displays pane to central widget layout
                self.main_window.layout.addWidget(self.panes[pane_name])

    # function that wraps all pane management logic.
    # can be called externally when panes need updating
    def update_panes(self):
        # clear existing variable pertaining to panes
        self.panes_controllers = {}
        self.panes = {}
        self.panes_status = {}

        # remove all previous panes (which are QWidgets)
        while self.main_window.layout.count():
            widget_item = self.main_window.layout.takeAt(0)
            if widget_item.widget():
                widget_item.widget().deleteLater()

        # create new list of panes and create them \
        self.create_pane_lists()
        self.create_panes()


# class that will be used once per each pane
# It will control which panels are displayed inside the pane
# update_pane_controller() is only function to call externally
class PaneController():
    def __init__(self, title, pane_widget, main_window):

        self.main_window = main_window
        self.title = title
        # self.name = self.main_window.data[title]["name"]

        # pane_widget is the main widget created by Pane Manager
        # all label and data widgets will be created inside pane_widget
        self.pane_widget = pane_widget

        # define the layout of this pane widget to be vertical
        self.layout = QVBoxLayout()
        self.pane_widget.setLayout(self.layout)

        # all the main update function for the PaneController
        self.update_pane_controller()

    # adds a title widget to the pane according to pane title
    def add_pane_title(self):
        # create a QLabel widget and set its alignment to center top
        self.label = QLabel(self.title)
        self.label.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        # get its color from CPU color settings
        color = self.main_window.settings["displays"][self.title]["color"]

        # define the style sheet and apply it to the label widget
        settings = (
            f"background-color: {color}; "
            "margin:0px; "
            "border:0px solid rgb(0, 0, 0); "
            "border-radius:5px; "
        )
        self.label.setStyleSheet(settings)

        # make it fixed height
        self.label.setFixedHeight(15)

        # add the label widget to pane_widgets layout
        self.layout.addWidget(self.label)

    def create_list_widgets(self):
        # create list of needed widgets in this pane
        if self.title == "CPU" or self.title == "GPU":
            self.widgets_status["temp"] = (
                self.main_window.settings["displays"][self.title]["temp"])
            self.widgets_status["util"] = (
                self.main_window.settings["displays"][self.title]["util"])

    # function that creates the data and stat widgets to the Pane
    # create_stat_widget will be called recursively by add_widgets()
    def create_data_widget(self, title):
        # create the pane for "title" and store in panes list
        self.widgets[title] = QWidget(self.pane_widget)

        # create three layouts that will be nested
        # main_layout=main_layout, secondary_layout=data, tertiary_layout=stats
        # main layout will be a VBox with title, and secondary (data) layout
        self.widgets_main_layouts[title] = QVBoxLayout()
        # secondary layout is an HBox that has current data, tertiary layout
        self.widgets_secondary_layouts[title] = QHBoxLayout()
        # tertiary layout (stats) is a VBox containing min, max, avg
        self.widgets_tertiary_layouts[title] = QVBoxLayout()

        # define pane color
        color = self.main_window.settings["background_color"]

        # define pane stylesheet and apply
        settings = (
            f"background-color: {color}; "
            "margin:0px; "
            "border:1px solid rgb(0, 0, 0); "
            "border-radius:10px;"
        )
        self.widgets[title].setStyleSheet(settings)

        # add fixed height title to each widget in the pane, remove its borders
        widget_title = QLabel(self.title_resolver(title))
        widget_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # set fixed height (determined experimentally)
        widget_title.setFixedHeight(25)
        # set title settings and apply
        # define pane stylesheet and apply
        title_settings = (
            f"background-color: {color}; "
            "margin:2px; "
            "border:1px solid rgb(0, 0, 0); "
            "border-radius:5px;"
        )
        widget_title.setStyleSheet(title_settings)
        # add the tile label to the main VBox layout
        self.widgets_main_layouts[title].addWidget(widget_title)

        # grab the main data of [title] and make label of it
        main_data = str(int(self.main_window.data[self.title][title]))
        main_label = QLabel(main_data)
        main_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_label_settings = (
            f"background-color: {color}; "
            "margin:0px; "
            "border:1px solid rgb(0, 0, 0); "
            "border-radius:5px;"
            "font:60px;"
        )
        main_label.setStyleSheet(main_label_settings)
        # add data to secondary HBox layout
        self.widgets_secondary_layouts[title].addWidget(main_label)

        # grab the min, max, and avg data of [title] and make label of it
        min_data = (
            f"Min: {self.main_window.data[self.title]['min_' + title]:.1f}"
        )
        min_label = QLabel(min_data)
        max_data = (
            f"Max: {self.main_window.data[self.title]['max_' + title]:.1f}"
        )
        max_label = QLabel(max_data)
        avg_data = (
            f"Avg: {self.main_window.data[self.title]['avg_' + title]:.1f}"
        )
        avg_label = QLabel(avg_data)
        min_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        max_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stats_label = (
            f"background-color: {color}; "
            "margin:2px; "
            "border:1px solid rgb(0, 0, 0); "
            "border-radius:5px;"
        )
        min_label.setStyleSheet(stats_label)
        max_label.setStyleSheet(stats_label)
        avg_label.setStyleSheet(stats_label)

        # add data to the tertiary Vbox layout
        self.widgets_tertiary_layouts[title].addWidget(min_label)
        self.widgets_tertiary_layouts[title].addWidget(max_label)
        self.widgets_tertiary_layouts[title].addWidget(avg_label)

        # nest all the layouts and set main layout
        self.widgets_secondary_layouts[title].addLayout(
            self.widgets_tertiary_layouts[title])
        self.widgets_main_layouts[title].addLayout(
            self.widgets_secondary_layouts[title])
        self.widgets[title].setLayout(self.widgets_main_layouts[title])

    # function to convert the short settings keys into full titles
    def title_resolver(self, title):
        if title == "temp":
            return "Temperature (\u00B0C)"
        elif title == "util":
            return "Utilization (%)"
        else:
            return ""

    # function to loop over the list of widgets, and add any that are enabled
    def add_widgets(self):
        # loop over the widgets_status list
        for widget_name, is_enabled in self.widgets_status.items():
            # if widget is enabled
            if is_enabled:
                # create each enabled stat widget (temp, gpu, etc...)
                self.create_data_widget(widget_name)
                # add the new stat widget to layout
                self.layout.addWidget(self.widgets[widget_name])

    # function that wraps all pane controller logic.
    # can be called externally when pane controllers need updating
    def update_pane_controller(self):
        self.widgets = {}
        self.widgets_status = {}
        self.widgets_main_layouts = {}
        self.widgets_secondary_layouts = {}
        self.widgets_tertiary_layouts = {}

        # remove all previous widgets added to the pane_widget
        while self.layout.count():
            widget_item = self.layout.takeAt(0)
            if widget_item.widget():
                widget_item.widget().deleteLater()

        # add title for entire pane
        self.add_pane_title()

        # create list of widgets to be added
        self.create_list_widgets()

        # add widgets according to current state of settings
        self.add_widgets()
