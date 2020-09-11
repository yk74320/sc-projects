"""
SC101 Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Jerry Liao.

File: babygraphics.py
Name: Ian Kuo
-------------------------
The objective of this program is to create a interface where users can search for baby names within the given time
period as well as their corresponding name rank in that year. A line chart is also plotted on the interfiace
so as to show the trending of the name rank.
"""

import tkinter
import babynames
import babygraphicsgui as gui

FILENAMES = [
    'data/full/baby-1900.txt', 'data/full/baby-1910.txt',
    'data/full/baby-1920.txt', 'data/full/baby-1930.txt',
    'data/full/baby-1940.txt', 'data/full/baby-1950.txt',
    'data/full/baby-1960.txt', 'data/full/baby-1970.txt',
    'data/full/baby-1980.txt', 'data/full/baby-1990.txt',
    'data/full/baby-2000.txt', 'data/full/baby-2010.txt'
]
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600
YEARS = [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]
GRAPH_MARGIN_SIZE = 20
COLORS = ['red', 'purple', 'green', 'blue']
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000


def get_x_coordinate(width, year_index):
    """
    Given the width of the canvas and the index of the current year
    in the YEARS list, returns the x coordinate of the vertical
    line associated with that year.

    Input:
        width (int): The width of the canvas
        year_index (int): The index of the current year in the YEARS list
    Returns:
        x_coordinate (int): The x coordinate of the vertical line associated
                              with the specified year.
    """
    year_count = len(YEARS)
    space = (width - GRAPH_MARGIN_SIZE * 2) / year_count
    x_coordinate = GRAPH_MARGIN_SIZE + space * year_index
    return x_coordinate


def draw_fixed_lines(canvas):
    """
    Erases all existing information on the given canvas and then
    draws the fixed background lines on it.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.

    Returns:
        This function does not return any value.
    """
    canvas.delete('all')            # Delete all existing lines from the canvas

    # Write your code below this line
    #################################
    canvas.create_line(GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE, CANVAS_WIDTH - GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE,
                       width=LINE_WIDTH, fill='black') # Draw upper bound
    canvas.create_line(GRAPH_MARGIN_SIZE, CANVAS_HEIGHT - GRAPH_MARGIN_SIZE, CANVAS_WIDTH - GRAPH_MARGIN_SIZE,
                       CANVAS_HEIGHT - GRAPH_MARGIN_SIZE, width=LINE_WIDTH, fill='black') # Draw lower bound
    for i in range(len(YEARS)):
        x = get_x_coordinate(CANVAS_WIDTH, i)
        year_name = YEARS[i]
        canvas.create_line(x, 0, x, CANVAS_HEIGHT, width=LINE_WIDTH, fill='black') # Draw left bound at x coordinate
        canvas.create_text(x, CANVAS_HEIGHT - GRAPH_MARGIN_SIZE, text=year_name, anchor=tkinter.NW)
        # Add year label at x coordinate


def draw_names(canvas, name_data, lookup_names):
    """
    Given a dict of baby name data and a list of name, plots
    the historical trend of those names onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data
        lookup_names (List[str]): A list of names whose data you want to plot

    Returns:
        This function does not return any value.
    """
    draw_fixed_lines(canvas)        # Draw the fixed background grid

    # Write your code below this line
    #################################
    pixel = (CANVAS_HEIGHT - GRAPH_MARGIN_SIZE * 2) / 1000 # Calculate the pixel margin in the given boundary
    for i in range(len(lookup_names)):
        name = lookup_names[i]
        color = COLORS[i % 4]
        for j in range(len(YEARS) - 1):
            ele1 = str(YEARS[j])
            if ele1 in name_data[name]:
                x1 = get_x_coordinate(CANVAS_WIDTH, j)
                y1 = GRAPH_MARGIN_SIZE + (float(name_data[name][ele1]) * pixel)
                canvas.create_text(x1 + TEXT_DX, y1, text=name + str(name_data[name][ele1]), fill=color,
                                   anchor=tkinter.SW) # Add name:rank label for the first year
            else:
                x1 = get_x_coordinate(CANVAS_WIDTH, j)
                y1 = CANVAS_HEIGHT - GRAPH_MARGIN_SIZE
                canvas.create_text(x1 + TEXT_DX, y1, text='*', fill=color, anchor=tkinter.SW)
                # Add a label '*" if name:rank not found in the first year

            ele2 = str(YEARS[j+1])
            if ele2 in name_data[name]:
                x2 = get_x_coordinate(CANVAS_WIDTH, j+1)
                y2 = GRAPH_MARGIN_SIZE + (float(name_data[name][ele2]) * pixel)
                canvas.create_text(x2 + TEXT_DX, y2, text=name + str(name_data[name][ele2]), fill=color,
                                   anchor=tkinter.SW) # Add name:rank label for the second year
            else:
                x2 = get_x_coordinate(CANVAS_WIDTH, j+1)
                y2 = CANVAS_HEIGHT - GRAPH_MARGIN_SIZE
                canvas.create_text(x2 + TEXT_DX, y2, text='*', fill=color, anchor=tkinter.SW)
                # Add a label '*" if name:rank not found in the first year
            canvas.create_line(x1, y1, x2, y2, width=LINE_WIDTH, fill=color)
            # Draw a line to connect the ranking of first and second year


# main() code is provided, feel free to read through it but DO NOT MODIFY
def main():
    # Load data
    name_data = babynames.read_files(FILENAMES)

    # Create the window and the canvas
    top = tkinter.Tk()
    top.wm_title('Baby Names')
    canvas = gui.make_gui(top, CANVAS_WIDTH, CANVAS_HEIGHT, name_data, draw_names, babynames.search_names)

    # Call draw_fixed_lines() once at startup so we have the lines
    # even before the user types anything.
    draw_fixed_lines(canvas)

    # This line starts the graphical loop that is responsible for
    # processing user interactions and plotting data
    top.mainloop()


if __name__ == '__main__':
    main()
