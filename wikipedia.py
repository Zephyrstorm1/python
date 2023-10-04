import tkinter as tk

# Python Tkinter is Standard GUI toolkit in python for creating interfaces with buttons, labels, menus, etc.

from tkinter import ttk

# This is a submodule of tkinter that provides themed Tkinter widgets

from tkinter import messagebox

# submodule of tkinter is used to create and display message boxes.

import requests

# This library allows to send HTTP requests and handle HTTP responses for this code it make an HTTP GET request to a Wikipedia URL to fetch HTML content.

from bs4 import BeautifulSoup

# BeautifulSoup is a Python library for web scraping and parsing HTML and XML documents.
#  Import the BeautifulSoup class from the bs4

import random

# The random module provides functions for generating random numbers, which is used in the code to randomly select an article link from the Wikipedia page.

import webbrowser

# The webbrowser module is used to interact with the web browser installed on the user's system. In this code, it opens url in default browser.

# Creating a list called valid_topics containing various topic names that the user can select from.

valid_topics = [
    "Science",
    "Literature",
    "History",
    "Technology",
    "Music",
    "Sports",
    "Fashion",
]


# Defining a function called get_random_wikipedia_article that takes a topic as an argument.
def get_random_wikipedia_article(topic):
    # Constructing the URL for the selected topic on Wikipedia.
    topic_url = f"https://en.wikipedia.org/wiki/Portal:{topic}"

    # Sending an HTTP GET request to the topic's URL and store the response.
    response = requests.get(topic_url)

    # In this code it(if response.status_code == 200:) is used to ensure that the web request to the Wikipedia URL was successful.
    # "200" means "OK." It indicates that the HTTP request was successful
    if response.status_code == 200:
        # Creating a BeautifulSoup object to parse the HTML content of the page.
        soup = BeautifulSoup(response.content, "html.parser")

        #  Finding all the anchor (<a>) tags with href attributes on the page.
        article_links = soup.find_all("a", href=True)

        # Filtering out links that lead to non-article pages(ie:those URLs containing "/wiki/" and not containing ":")
        article_links = [
            link
            for link in article_links
            if "/wiki/" in link["href"] and ":" not in link["href"]
        ]
        # to Check if there are any article links found on the topic page
        if article_links:
            # for Randomly selecting one of the article links.
            random_article_link = random.choice(article_links)

            # Getting the text (title) of the selected link.
            article_title = random_article_link.get_text()
            # Creating the full URL of the random article
            article_url = f"https://en.wikipedia.org{random_article_link['href']}"

            # Return the title and URL of the randomly selected article.
            return article_title, article_url
    # if valid articles isnt found returning "None"
    return None, None


def generate_random_article():
    # Get the user's selected topic from the dropdown menu
    user_topic = topic_var.get()

    # Get a random Wikipedia article related to the user's selected topic
    article_title, article_url = get_random_wikipedia_article(user_topic)

    if article_title and article_url:
        result_label.config(
            text=f"Random Wikipedia article on {user_topic}:\nTitle: {article_title}"
        )
        result_url_label.config(text=f"URL: {article_url}", cursor="hand2")
        result_url_label.url = article_url  # Store the URL as an attribute
    else:
        messagebox.showerror("Error", f"No articles found for the topic: {user_topic}")


# Function to open the link in the default web browser
def open_article_url(event):
    if hasattr(result_url_label, "url"):
        webbrowser.open(result_url_label.url)  # Open in the default web browser of user


# Creating the main window
root = tk.Tk()
root.title("Random Wikipedia Article Generator")

# Configuring the window background and text colors
root.configure(bg="black")
style = ttk.Style()
style.configure(
    "TButton", font=("Helvetica", 12), background="white", foreground="black"
)  # Button style
style.configure(
    "TLabel", font=("Helvetica", 14), background="black", foreground="white"
)
style.configure("TFrame", background="black")
style.map("TButton", background=[("active", "blue")])

# Creating a frame for the content
content_frame = ttk.Frame(root, padding=20)
content_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
content_frame.grid_columnconfigure(0, weight=1)

# Creating a label for the title
title_label = ttk.Label(
    content_frame, text="Random Wikipedia Article Generator", font=("Helvetica", 18)
)
title_label.grid(column=0, row=0, columnspan=2, pady=(0, 20))

# Creating a label and dropdown menu for topic selection
topic_label = ttk.Label(content_frame, text="Choose a preferred topic:")
topic_label.grid(column=0, row=1, padx=10)

topic_var = tk.StringVar()
topic_var.set(valid_topics[0])  # Default value
topic_menu = ttk.Combobox(
    content_frame, textvariable=topic_var, values=valid_topics, state="readonly"
)
topic_menu.grid(column=1, row=1)

# Creating a button to generate a random article
generate_button = ttk.Button(
    content_frame, text="Generate Random Article", command=generate_random_article
)
generate_button.grid(column=0, row=2, columnspan=2, pady=(20, 0))

# Creating labels to display the result
result_label = ttk.Label(content_frame, text="", wraplength=400)
result_label.grid(column=0, row=3, columnspan=2, pady=(20, 0))

result_url_label = ttk.Label(
    content_frame, text="", wraplength=400, foreground="blue", cursor="hand2"
)
result_url_label.grid(column=0, row=4, columnspan=2, pady=(10, 20))

# Binding the URL label to open the URL when clicked
result_url_label.bind("<Button-1>", open_article_url)

# Starting the GUI main loop
root.mainloop()
