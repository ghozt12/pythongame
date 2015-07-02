



###################################################################
#
#   CSSE1001 - Assignment 2
#
#   Student Number: 43137006
#
#   Student Name: Rhain Dodd
#
###################################################################


#
# Do not change the following import
#

import MazeGenerator


####################################################################
#
# Insert your code below
#
####################################################################

from Tkinter import * # Imports Tkinter
import tkMessageBox # Imports the popup messages
import tkFileDialog # Imports the save and open file


class MazeApp(object):
    """
    Class MazeApp(object)

    This class creates and holds the top level GUI for the Maze Solver.
    """

    def __init__(self, master=None):
        """
        MazeApp.__init__(self, master = none)

        This function Initialises the class MazeApp.

        Sets the minsize of master
        Sets the file menu
        Sets the canvas for the maze_list
        Sets the footer
        Sets the key bindings
        """
        #---------------------------------
        # Master settings
        self.myMaster = master
        # Title of the page
        self.myMaster.title("Maze Solver")
        # Set Min window size (300 as per assignment)
        self.myMaster.minsize(300,300)
        # --------------------------------

        # --------------------------------
        # File - top menu
        topmenu = Menu(master)
        # Set menu
        filemenu = Menu(topmenu, tearoff=0)
            # Dropdown
        topmenu.add_cascade(label="File", menu=filemenu)
                # Seperator
        filemenu.add_separator() 
                # Open 
        filemenu.add_command(label="Open Maze File", command=self.open)
                # Save
        filemenu.add_command(label="Save Maze File", command=self.save)
                # Exit
        filemenu.add_command(label="Exit", command=self.exit)
        # Config (sets menu to our menu bar instead of defualt)
        master.config(menu=topmenu)
        # --------------------------------

        # --------------------------------
        # Maze Canvas
        self._lordCanvas = Canvas(master, bg="black", relief=SUNKEN, bd=2)
        self._lordCanvas.pack(side=TOP, expand=YES)
        # --------------------------------

        # --------------------------------
        # Footer
        # Footer Frame
        footer = Frame(master, padx=20)
        footer.pack(side=BOTTOM, fill=BOTH)
            # Sunken Frame
        footer_sunken = Frame(footer, relief=SUNKEN, bd=2)
        footer_sunken.pack(side=LEFT, expand=True)
                # Spinbox
        self.maze_number = Spinbox(footer_sunken, from_=1, to=15, width=5)
        self.maze_number.pack(side=LEFT)
                # New 
        floor_new = Button(footer_sunken, text="New", command= self.new_maze)
        floor_new.pack(side=LEFT)
            # Reset
        floor_reset = Button(footer, text="Reset", command=self.reset_player)
        floor_reset.pack(side=LEFT, expand=True)
            # Quit
        floor_quit = Button(footer, text="Quit", command = self.exit)
        floor_quit.pack(side=LEFT,expand=True)
        # --------------------------------

        # --------------------------------
        # Binding Keys
            # Binded seperatly to ensure correct key
        master.bind('<Left>',self.move_player)
        master.bind('<Right>',self.move_player)
        master.bind('<Up>',self.move_player)
        master.bind('<Down>',self.move_player)
        # --------------------------------

        # --------------------------------
        # Maze Generator
            # This is the maze generator that is imported.
        self.maze_gen = MazeGenerator.MazeGenerator()
        # --------------------------------
        # set lordCanvas to fill the screen
        self._lordCanvas.configure(width=300, height = 260, bd=2)


    def exit(self):
        """
        MazeApp.exit() -> Closes program

        MazeApp.exit() is used to exit the program.

        """

        # This will end the program/script
        self.myMaster.destroy()

    def open(self):
        """
        MazeApp.open() -> Opens a file and loads the maze

        MazeApp.open() is used to open a file using a Tkinter file explorer
        and it loads the file as a maze if it is valid
        """

        # Set the open_file to the tk file explorer. .txt only
        open_file = tkFileDialog.askopenfilename(defaultextension="txt")
        
        # Check if the maze file is valid
        if open_file:
            # open the file
            opened_file = open(open_file, 'rU')
            try:
                # Try: load maze. It will return an exception if not-valid
                self.maze = Maze(opened_file.read())
                # close the file
                opened_file.close()
                # Set the window size so maze fits
                self.set_window_size()
                # Create the maze elements
                self.create_lordCanvas_elements() 
            except Exception as e:
                # if there is an exception, show this error:
                tkMessageBox.showerror(title='The maze is invalid',message=e)

    def save(self):
        """
        MazeApp.save() -> Saves file in a directory of the users choice

        This is the save function. It takes the current maze and allows 
        you to save it to your local directory. It saves the file as a
        string of characters (.txt)
        """

        # Set up the Tk dialog explorer, defualt is set as txt
        save_file = tkFileDialog.asksaveasfilename(defaultextension="txt")

        # Tkinter creates a file with the above name
        # We open this file and write the maze to it
        # the 'w'meants write

        # The file is opened
        the_file = open(save_file, 'w')
        # The string of the maze is written to the file
        # remember the __str__ of the class maze returns the string of the maze
        the_file.write(str(self.maze)) 
        # The file is closed.
        the_file.close()

        #with open("text.txt", "a") as f:
        #f.write(text)

    def create_lordCanvas_elements(self):
        """
        MazeApp.create_lordCanvas_elements() -> create maze elements

        Draws the maze boxes on the canvas. All boxes start in black.
        As the player moves the boxes will be changed to the correct 
        colour.

        MazeApp.create_lordCanvas_elements() will first clear the canvas,
        it will then get the size of the maze. Using the maze size it will
        create a set of boxes relating to the list of elements in the maze.

        It will then draw the player.
        """
        
        # The canvas is cleared
        self._lordCanvas.delete(ALL)
        # Create an empty list to hold our rectangles
        self.rectangle_holder = []
        # List of rectangles holder
        self.lord_holder = []

            # for each element we create a rectangle
            # We mulitply the x and y coords by 20 so the

            # Understanding tkinter drawing:
            # the first two elements are the top-left coordinates of the square.
            # the new two are the bottom right coordinates (x,y)
            # So we would have to add 1 to the x at the top left
            # bottom right will always be 20,20 more than the top, so if we just add 1 to it should work 

            # How this function works:
            # Firstly we set two variables to 0.
            # We run throught each row of the list of the maze.
            # We run throught each element in each row from the maze.
            # We create a rectangle for each element, we then add this rectangles name into
            # a list.
            # once its run thought the elements in the row
            # it appends the list to the lord list and then resets it to []
            # b is also reset to ensure we draw the rectange in the correct place.

        #set two variables for use with the rectangle creation
        a = 0
        b = 0
        
        # get the maze as a list
        mze = str(self.maze).split('\n')

        # for every row in maze
        for row in mze:
            # set holder to empty, so we get a list of lists
            self.rectangle_holder = []
            # b is set to 0, to ensure that the creation of the rectangles are correct
            # every row starts at (0,0) in the left hand corner, so we set b to 0
            b = 0
            # for every element in the row
            for ele in row:
                # create the rectanges
                rect = self._lordCanvas.create_rectangle(b * 20, a * 20, (b + 1) * 20, (a + 1) * 20, fill='black')
                # appennd the rectangles into a list
                self.rectangle_holder.append(rect)
                # increase b by 1
                b += 1
            # append the list into the total list
            self.lord_holder.append(self.rectangle_holder)
            # increase a by 1. This will bring us to the next row of rectangles
            a += 1
        # Run the draw player function
        self.draw_player()

    def draw_player(self):
        """MazeApp.draw_player()

        Draws the player's positions as a circle. Reveals walls,
        floors and end point as player progresses.

        """

        # Get the current position of the player
        self.maze_pos = self.maze.get_pos()
        # Delete circle if it exists
        if 'player_circle' in self.__dict__:
            self._lordCanvas.delete(self.player_circle)
        
        # Create the circle. These are the circle values

        # top left, x
        top1 = self.maze_pos[0] * 20 + 4
        # top left y
        top2 = self.maze_pos[1] * 20 + 4
        # Bottom right x
        bot1 = (self.maze_pos[0] + 1) * 20 - 4
        # Bottom right y
        bot2 = (self.maze_pos[1] + 1) * 20 - 4

        # Initilise the circle
        self.player_circle = self._lordCanvas.create_oval(top1,top2,bot1,bot2)
        # Set colour to cyan
        self._lordCanvas.itemconfigure(self.player_circle,fill='cyan')

        # Why these circle dimensions: 
        # 1) The circle radius is 6 as stated in the newsgroup csse 1001
        # 2) 20 - (6*2) = 8 (block - diameter of circle)
        # 3) 8/2 = 4. So we use 4px on each side to position the circle in the center
        # 5) We are given cyan as the colour

        # Reveals maze as player progresses in a 3x3 manner
        x = self.maze_pos[0]
        y = self.maze_pos[1]

        # Changes the blocks from black to their correct colours
        def changr(row,col):

            # Colours for easy changing
            floor = "white"
            wall = "red"
            fin = "blue"

            # Set the given values to x and y for ease of use
            x = row
            y = col

            # if it is a floor then change block colour to white
            if self.maze.get_tile(x,y) == " ":
                # takes the item using the current postition, and checks the rectangle holder for the correct value
                # it then configs the colour
                self._lordCanvas.itemconfigure(self.lord_holder[y][x],fill=floor)
            # if it is a wall then change block colour to red
            elif self.maze.get_tile(x,y) == "#":
                    self._lordCanvas.itemconfigure(self.lord_holder[y][x],fill=wall)
            # else it has to be the Finish, therefore 
            else:
                self._lordCanvas.itemconfigure(self.lord_holder[y][x],fill=fin)

        # Player row
        changr(x,y)
        changr(x,y+1)
        changr(x,y-1)

        # Above row
        changr(x-1,y)
        changr(x-1,y-1)
        changr(x-1,y+1)

        # Below Row
        changr(x+1,y)
        changr(x+1,y-1)
        changr(x+1,y+1)


    def new_maze(self):
        '''
        MazeApp.new_maze() -> creates a new maze

        This function runs the maze generator and then sets it as the maze.
        It then sets the window size and draws the maze ( create_maze() )
        '''

        # First we get the number that is in the spinbox. We use get() which returns a string
        user_num = self.maze_number.get() # string
        user_num = int(user_num) # Turn the string into an int

        # Run the maze generation code (imported function)
        maze_gen = self.maze_gen.make_maze(user_num)

        # Set the maze as Maze(class) and run checks
        self.maze = Maze(maze_gen)

        # Set the window size to resize incase the maze is larger or smaller than the window
        self.set_window_size()

        # Create the maze
        self.create_lordCanvas_elements()


    def reset_player(self):
        '''
        MazeApp.reset_player() -> Resets the position of the player

        This function will reset the postion of the player back to poistion (1,1)


        '''
        # Run the reset positon function from maze Class
        self.maze.reset()
        # ReDraw the maze and player
        self.create_lordCanvas_elements()


    def move_player(self, event):
        """
        MazeApp.move_player() -> Moves player position

        This function takes the key input that was binded in the __init__,
        and it attempts to run the maze.move function using the keysuym
        as the direction.

        If successful the player is moved.

        The player is then redrawn.  
        """
        
        # get keypress symbol (it will be Up, Down, Left or Right)
        key = event.keysym
        # Run the maze.move function using key as the direction
        self.maze.move(key)
        # Draw the player with the new position
        # the function will check if we can move in that direction so we dont have to do it here
        self.draw_player()
        # If they have won
        if self.maze.is_solved():
            # tkMessageBox.FunctionName(title, message [, options]) <- format
            # showinfo() shows the info. Popup window
            tkMessageBox.showinfo(title="Congratulations", message="We have a winner")
       
    def set_window_size(self):
        """
        MazeApp.set_maze_size() -> sets canvas size

        MazeApp.set_maze_size() changes the size of the canvas in relation to the size
        of the maze that has been loaded.
        """

        # This function exists solely to change the size of the window and the canvas
        # What happens is that the maze is loaded, we then get the size of the maze using the get_size().
        # Using this we can then change the size of the window so everything fits in perfectly.

        # We run self. maze (maze string) .get_size function() --> returns (width, height)
        maze_size_width = self.maze.get_size()[0]# width
        maze_size_height = self.maze.get_size()[1]# height

        # We know that each block is 20px, (given on the newsgroup), so we can just multiply the width and height by 20
        block_size_width = maze_size_width * 20 # width in blocks
        block_size_height = maze_size_height * 20 # width in blocks

        # We now set the lordCanvas to the exact size of the maze
        self._lordCanvas.configure(width=block_size_width, height = block_size_height, bd=2)

        # Set master size to accomadate the canvas size

        # Geomentry ( width x height) as one input. Convert it to string
        extra_for_footer = block_size_height + 40
        geo = '{0}x{1}'.format(block_size_width, extra_for_footer)
        # Run the function to change the master size
        self.myMaster.geometry(geo)

class Maze(object):
    """
    Class Maze(object) -> string

    This holds the players position and takes the maze as a string and checks that it is valid.
    It can return the position of every element in the maze.

    str(maze) -> returns a string of the maze

    """
    
    def __init__(self,string):
        """
        Maze.__init__(string)

        Initialises Maze.
        
        This runs the maze, where string is a 
        """

        # Take the string and saves it
        self.maze = string
        # Split the maze into a list at the breaks
        self.maze_list = self.maze.split('\n')
        # Set the player starting point
        self.cur_pos = (1,1)
        # We then test the maze to see if it is valid
        testing = self.check_mze() # Test if maze is invalid
        
        # Exception test
        if not testing[0]:
            # Pythonic exception raising. 
            # raise me up 
            raise Exception("Maze is invalid: " + testing[1])


    def check_mze(self):
        """
        check_mze() -> returns True, or False

        Makes sure the maze meets the conditions set forth in the assignment. They are as follows;
        1) Length must be > 3
        2) Rows must be equal
        3) Must contain only valid characters
        4) Only 1 finish character
        5) Outer walls must be complete
        """

        # ** First check number of rows. must be > 3 otherwise there would be no place to spawn **
        # The len of the list will count the number of rows in the list.
        # if < 3 then return a fail


        if 3 > len(self.maze_list):
            return (False, "Too few rows")

        # ** Check that rows are equal length **

        # Save the first len(row), check each row against it.
        checker = len(self.maze_list[0])
        # For each row in the list
        for row in self.maze_list:
            # if the length of the row is not equal to check (which is = len(1st row))
            if len(row) != checker:
                # return false and raise an exception.
                return (False, "Rows not equal")

        #  ** Check maze characters **
        # for every element, if they are not equal to # and not equal to ' ' and != X then return exception
        for row in self.maze_list:
            # for each character in the row check if they are valid characters
            for element in row:
                # check if valid 
                if element != '#' and element != 'X' and  element != ' ':
                    # return false and raise an exception
                    return (False, "Invalid maze character")


        # ** Check Finish character **
        # We will count how many X there are in the list

        # counter is set to 0
        count_finish_character = 0
        # for every row
        for row in self.maze_list:
            # and every element in that row
            for element in row:
                # if the element is an X
                if element == 'X':
                    # Add one to the counter
                    count_finish_character += 1
        # Once the counting is done then run the if statmnet
        if count_finish_character > 1:
            # Return false and raise exception
            return (False, "More than one finishing point")
        # if there are no finish characters then return false.
        if count_finish_character  == 0:
            return (False, "No finishing point")

        # Getting a list of lists of the maze
        nospace = str(self.maze).split('\n')
        grandholder = []


        # for every row in maze
        for row in nospace:
            # set holder to empty, so we get a list of lists
            holz = []
            # for every element in the row
            for element in row:
                # put the letter into a holder
                holz.append(element)
            # append the list into another list, this makes the rows
            grandholder.append(holz)
        
        # Checking the outer walsls

        # Checks the first row
        for z in grandholder[0]:
            if z != "#":
                return(False, "Missing an outer wall on the maze")
        # Checks the last row
        for x in grandholder[-1]:
            if x != "#":
                return(False, "Missing an outer wall on the maze")
        # checks the ends of every row
        for i in self.maze_list:
            if i[0] != '#' or i[-1] != '#':
                return(False, "Missing an outer wall on the maze")




        # Dont need to check maze is solvable :) sweet.

        # Return True if it passes everything
        return (True,None)

    def __str__(self):
        """
        str(mazename) -> string of the maze

        Returns the maze file as a string suitable to be written to file and saved etc 
        """

        # simple, just return the maze
        return self.maze


    def move(self,direction):
        """
        Maze.move(string, direction)

        This is the direction the player moves in.
        
        """

        # First we have to get the direction according to which key it is 
        # set the direction as a tuple. Defualt is (0,0)
        direct = (0,0)
        # if it is up, then (0,-1) and so on -1 on the y value will bring it up
        if direction == 'Up':
            direct = (0,-1)
        if direction == 'Down':
            direct = (0,1)
        if direction == 'Left':
            direct = (-1,0)
        if direction == 'Right':
            direct = (1,0)

        # split it into two values and get the new position
        x,y = direct 
        # set the position as the current position added on with the direction
        # Vector addition, you go: (x1 + x2 , y1 + y2)
        position = self.cur_pos[0] + x, self.cur_pos[1] + y

        # Check if it is valid and then update the player
        # it is valid if it is not a wall
        if self.get_tile(position[0],position[1]) != '#':
            # set the player position to the position
            self.cur_pos = position

    def reset(self):
        """
        Maze.reset()

        Resets the player to the beginning of the maze and turns on the fog of war again (1,1)

        """

        # Simple, Beginning is always (1.1)

        self.cur_pos=(1,1)

    def get_size(self):
        """

        Maze.get_size() -> (width, height)

        Returns the height and width of the maze as a tuple with the (width first, height second)

        """

        # Get the width and height of the maze

        # height is the number of rows 
        height_maze = len(self.maze_list)

        # width is the number of elements in the first row (since all rows are =)
        width_maze = len(self.maze_list[0])

        # Returns the tuple
        return (width_maze,height_maze)

    def get_tile(self,r,c):
        """
        Maze.get_tile(int,int) -> (string)

        Returns tile type at the given position.
        Returns either #, X or " "

        """

        # Well since its just column and row we can just get that straight from the list[row][column]
        # simple list searching, returns #, X or " "
        return self.maze_list[r][c]

    def get_pos(self):
        """
        Maze.get_pos() -> (tuple)

        Returns current position of the player.

        """

        # Return the position of the player which is cur_pos
        return self.cur_pos

    def is_solved(self):
        """
        Maze.is_solved() -> (bool)

        Returns False if maze is not solved, True if maze is solved.

        """

        # We check if our current position is on the X or not
        # Get our current position
        ez_holdr = self.cur_pos

        # Check to see what is at our current position useing get tile
        where = self.get_tile(ez_holdr[0],ez_holdr[1])

        # If we are on an X then we return true, other wise we return false
        if where == 'X':
            return True
        else:
            return False


####################################################################
#
# WARNING: Leave the following code at the end of your code
#
# DO NOT CHANGE ANYTHING BELOW
#
####################################################################

def main():
    root = Tk()
    app = MazeApp(root)
    root.mainloop()

if  __name__ == '__main__':
    main()
