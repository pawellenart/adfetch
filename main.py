from __future__ import annotations

import json
import os
import typing

import requests
import urwid

if typing.TYPE_CHECKING:
    from collections.abc import Iterable

# Global variables to store input values
target_directory = os.getcwd()
cache_url = "https://raw.githubusercontent.com/pawellenart/adfetch-cache/refs/heads/main/amiga_games.json"

def menu(title: str, choices_: Iterable[str]) -> urwid.ListBox:
    title_widget = urwid.Text(("reversed", "ADFetch v0.1"), align='center')
    target_directory_edit = urwid.Edit(caption="Path:", edit_text=target_directory, wrap='clip', multiline=False)
    cache_url_edit = urwid.Edit(caption="URL:", edit_text=cache_url, wrap='clip', multiline=False)

    # Attach signals to capture input changes
    urwid.connect_signal(target_directory_edit, 'change', update_target_directory)
    urwid.connect_signal(cache_url_edit, 'change', update_cache_url)

    body = [
    title_widget,
    urwid.Text("Press F10 to quit", align='center'),
        urwid.Divider(),
        urwid.Text("Target ADF download directory:"),
        urwid.AttrMap(target_directory_edit, 'reversed'),
        urwid.Divider(),
        urwid.Text("ADF cache source:"),
        urwid.AttrMap(cache_url_edit, 'reversed'),
        urwid.AttrMap(
            urwid.Button("Refresh cache", on_press=refresh_cache),
            None,
            focus_map="reversed"
        ),
        urwid.Divider(),
        urwid.Text(title),
        urwid.Divider()
    ]

    columns = 5
    rows = (len(choices_) + columns - 1) // columns
    grid = []
    for row in range(rows):
        buttons = []
        for col in range(columns):
            index = row + col * rows
            if index < len(choices_):
                button = urwid.Button(choices_[index])
                urwid.connect_signal(button, "click", item_chosen, choices_[index])
                buttons.append(urwid.AttrMap(button, None, focus_map="reversed"))
            else:
                buttons.append(urwid.Text(""))
        grid.append(urwid.Columns(buttons))
    body.extend(grid)
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def update_target_directory(edit: urwid.Edit, text: str):
    global target_directory
    target_directory = text

def update_cache_url(edit: urwid.Edit, text: str):
    global cache_url
    cache_url = text

def item_chosen(button: urwid.Button, choice: str) -> None:
    global cache_data
    if 'cache_data' not in globals():
        cache_data = []
    if not cache_data:
        refresh_cache(None)
        if not cache_data:
            return

    filtered_items = [
        item['title'] for item in cache_data 
        if 'title' in item and (
            item['title'].lstrip(r"'\"!@#$%^&*()-_=+[]{};:,<>?/|`~ ").lower().startswith(choice.lower())
            or (choice == "0-9" and item['title'][0].isdigit())
        )
    ]
    if not filtered_items:
        filtered_items = ["No items found."]

    listbox = urwid.ListBox(urwid.SimpleFocusListWalker([
        urwid.AttrMap(urwid.Button("Back to Menu", on_press=lambda btn: setattr(main, 'original_widget', urwid.Padding(menu("Choose a letter:", choices), left=2, right=2))), None, focus_map="reversed")
    ] + [
        urwid.AttrMap(urwid.Button(item, on_press=lambda btn, title=item: download_file(title, listbox, loop)), None, focus_map="reversed") for item in filtered_items
    ]))

    main.original_widget = urwid.Frame(
        body=listbox,
        focus_part='body'
    )

def download_file(title: str, previous_list, loop):
    global cache_data
    if not target_directory:
        show_message("Target directory not set.")
        return

    file_data = next((item for item in cache_data if item['title'] == title), None)

    if not file_data or 'url' not in file_data:
        show_message("URL not found for the selected item.")
        return

    file_url = file_data['url']
    file_name = os.path.join(target_directory, title)

    try:
        with requests.get(file_url, stream=True) as response:
            response.raise_for_status()
            with open(file_name, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)

        main.original_widget = urwid.Frame(
            body=previous_list,
            focus_part='body'
        )

    except Exception as e:
        show_message(f"Download failed: {e}")
        with requests.get(file_url, stream=True) as response:
            response.raise_for_status()
            with open(file_name, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)

        main.original_widget = urwid.Frame(
            body=previous_list,
            focus_part='body'
        )

def show_message(message: str):
    back_to_menu = urwid.Button("Back to Menu")
    urwid.connect_signal(back_to_menu, "click", lambda btn: setattr(main, 'original_widget', urwid.Padding(menu("Choose a letter:", choices), left=2, right=2)))
    main.original_widget = urwid.Filler(
        urwid.Pile([
            urwid.Text(message),
            urwid.Divider(),
            urwid.AttrMap(back_to_menu, None, focus_map="reversed")
        ])
    )

def refresh_cache(button: urwid.Button):
    if not cache_url:
        show_message("Cache URL input not found.")
        return

    try:
        response = requests.get(cache_url)
        response.raise_for_status()
        global cache_data
        cache_data = response.json()
        show_message(f"Cache refreshed successfully. {len(cache_data)} objects loaded.")
    except Exception as e:
        show_message(f"Failed to refresh cache: {e}")

def exit_program(button: urwid.Button):
    raise urwid.ExitMainLoop()

choices = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + ["0-9"]

main = urwid.Padding(menu("Choose a letter:", choices), left=2, right=2)

top = urwid.Overlay(
    main,
    urwid.SolidFill("\N{MEDIUM SHADE}"),
    align=urwid.CENTER,
    width=(urwid.RELATIVE, 60),
    valign=urwid.MIDDLE,
    height=(urwid.RELATIVE, 60),
    min_width=20,
    min_height=9,
)

palette = [("reversed", "standout", "")]
loop = urwid.MainLoop(top, palette=palette, unhandled_input=lambda key: key == "f10" and exit_program(None))
loop.run()
