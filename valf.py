#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Valf Bağlantı Yönetim Aracı
"""

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk

software_list = [
    ("Firefox", 2002, "C++"),
    ("Eclipse", 2004, "Java"),
    ("Pitivi", 2004, "Python"),
    ("Netbeans", 1996, "Java"),
    ("Chrome", 2008, "C++"),
    ("Filezilla", 2001, "C++"),
    ("Bazaar", 2005, "Python"),
    ("Git", 2005, "C"),
    ("Linux Kernel", 1991, "C"),
    ("GCC", 1987, "C"),
    ("Frostwire", 2004, "Java"),
]


class TreeViewFilterWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Valf")
        self.set_border_width(10)

        # Setting up the self.grid in which the elements are to be positionned
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        # Creating the ListStore model
        self.software_liststore = Gtk.ListStore(str, int, str)
        for software_ref in software_list:
            self.software_liststore.append(list(software_ref))
        self.current_filter_language = None

        # Creating the filter, feeding it with the liststore model
        self.language_filter = self.software_liststore.filter_new()
        # setting the filter function, note that we're not using the
        self.language_filter.set_visible_func(self.language_filter_func)

        # creating the treeview, making it use the filter as a model, and adding the columns
        self.treeview = Gtk.TreeView.new_with_model(self.language_filter)
        self.treeview.connect("button-press-event", self._on_button_press_event)
        for i, column_title in enumerate(
            ["Software", "Release Year", "Programming Language"]
        ):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)
            

        # creating buttons to filter by programming language, and setting up their events
        self.buttons = list()
        for prog_language in ["Java", "C", "C++", "Python", "None"]:
            button = Gtk.Button(prog_language)
            self.buttons.append(button)
            button.connect("clicked", self.on_selection_button_clicked)

        self.label = Gtk.Label()
        self.label.set_text("Boş yer")
        self.label.set_justify(Gtk.Justification.LEFT)
        


        # setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 0, 3, 10)
        self.grid.attach_next_to(
            self.label, self.scrollable_treelist, Gtk.PositionType.RIGHT, 7, 10
        )
        self.grid.attach_next_to(
            self.buttons[0], self.scrollable_treelist, Gtk.PositionType.BOTTOM, 1, 1
        )
        for i, button in enumerate(self.buttons[1:]):
            self.grid.attach_next_to(
                button, self.buttons[i], Gtk.PositionType.RIGHT, 1, 1
            )
        self.scrollable_treelist.add(self.treeview)

        self.show_all()

    def _build_context_menu(self):
        menu = Gtk.Menu()
        menu_item = Gtk.MenuItem("İçerik1")
        menu_item2 = Gtk.MenuItem("İçerik2")
        menu.append(menu_item)
        menu.append(menu_item2)
        menu.show_all()
        return menu

    def _on_button_press_event(self, widget, event):
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 3:
            menu = self._build_context_menu()
            menu.popup( None, None, None,None, event.button, event.get_time()) 
            return True


    def language_filter_func(self, model, iter, data):
        """Tests if the language in the row is the one in the filter"""
        if (
            self.current_filter_language is None
            or self.current_filter_language == "None"
        ):
            return True
        else:
            return model[iter][2] == self.current_filter_language

    def on_selection_button_clicked(self, widget):
        """Called on any of the button clicks"""
        # we set the current language filter to the button's label
        self.current_filter_language = widget.get_label()
        print("%s language selected!" % self.current_filter_language)
        # we update the filter, which updates in turn the view
        self.language_filter.refilter()


win = TreeViewFilterWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
