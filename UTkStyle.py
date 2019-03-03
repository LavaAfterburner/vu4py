
import tkinter as tk
import copy
from vu4py.ULogger import ULogger


class UTkStyle:
    class Style:
        def __init__(self, type, **kwargs):
            self.type = type
            self.kwargs = kwargs

        def set(self, **kwargs):
            self.kwargs = {**self.kwargs, **kwargs}

        def as_list(self):
            kwargs_list = list()
            for key in self.kwargs.keys():
                kwargs_list.append({key: self.kwargs[key]})
            return kwargs_list

        def copy(self):
            return UTkStyle.Style(self.type, **copy.deepcopy(self.kwargs))

        def __str__(self):
            as_string = str()
            as_string += "Style for {} with:\n".format(self.type)
            as_string += "   {}".format(self.kwargs)
            return as_string

        def __repr__(self):
            return self.__str__()

    class Settings:
        LOG_ERRORS = True

    class Theme:
        def __init__(self, name):
            self.name = name
            self.styles = dict()
            self.DEFAULT_STYLE = []

            UTkStyle.THEME_DATA[self.name] = self

        def add_style(self, *styles):
            for style in styles:
                self.styles[style.type] = style.as_list()
            return self

        def set_default_style(self, style):
            self.DEFAULT_STYLE = style.as_list()

        def set_to_default(self):
            UTkStyle.THEME_NAME = self.name

        def __str__(self):
            return str(self.styles)

    THEME_NAME = "DARK"
    THEME_DATA = dict()

    @staticmethod
    def apply_theme(*widgets):
        def apply(widget, style):
            for setting in style:
                try:
                    widget.config(setting)
                except:
                    if UTkStyle.Settings.LOG_ERRORS:
                        ULogger.log("Apply Theme [{}] failed on {}".format(setting, type(widget)),
                                   ULogger.Levels.WARNING)

        theme = UTkStyle.THEME_DATA[UTkStyle.THEME_NAME]
        styles = theme.styles
        style_types = styles.keys()

        for widget in widgets:
            widget_type = type(widget)

            if widget_type in style_types:
                apply(widget, styles[widget_type])
            else:
                apply(widget, theme.DEFAULT_STYLE)

    @staticmethod
    def get_widgets(parent):
        children = list()
        unchecked = list()
        unchecked.extend(parent.winfo_children())
        children.extend(parent.winfo_children())
        discovered = True
        while discovered:
            discovered = False
            for i, widget in enumerate(unchecked):
                if widget.winfo_children():
                    discovered = True
                    del unchecked[i]
                    children.extend(widget.winfo_children())
                    unchecked.extend(widget.winfo_children())

        return children

    @staticmethod
    def load_theme(theme_file):
        with open(theme_file, "r") as file:
            raw_themes = eval("".join(file.readlines()))
            for raw_theme in raw_themes:
                theme_name = raw_theme["name"]
                theme_is_default = raw_theme["is_default_theme"]
                theme_styles = raw_theme["styles"]

                theme = UTkStyle.Theme(theme_name)
                if theme_is_default:
                    theme.set_to_default()

                for style_type in theme_styles.keys():
                    style_settings = theme_styles[style_type]
                    style = UTkStyle.Style(style_type)
                    style.set(**style_settings)

                    if style.type == "DEFAULT":
                        theme.set_default_style(style)
                    else:
                        theme.add_style(style)
