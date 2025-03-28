from graphics import *

range_list = [0, 20, 40, 60, 80, 100, 120]
progression_data = []  # List to store progression data
output = [0, 0, 0, 0]


def file_creating():  # function for creating file as asked in part 3
    global result, _defer, _pass, _fail
    file = open("Credit outcomes", "w")
    file.write(f"Part 03 : \n{result} - {_pass},{_defer},{_fail} \n")
    file.close()


def get_credit(credit_input):  # Function for getting inputs for the user
    while True:
        try:
            credit = int(input(credit_input))
            if credit in range_list:
                return credit
            else:
                print(f"Out of range: The credits should be in {range_list} ")

        except ValueError:
            print("Integer required")


def draw_histogram(win):  # Funtion for display Barchart of outcomes
    colors = ["aqua", "chartreuse", "violet", "moccasin"]
    labels = ["Progress", "Trailing", "Retriever", "Exclude"]
    max_value = max(output)

    bar_width = 80
    bar_spacing = 5
    x = 50

    for i, value in enumerate(output):
        bar_height = (value / max_value) * 200
        bar = Rectangle(Point(x, 250), Point(x + bar_width, 250 - bar_height))
        bar.setFill(colors[i])
        bar.draw(win)

        label = Text(Point(x + bar_width / 2, 260), labels[i])
        label.draw(win)

        # Display outcome count on top of each bar
        count_label = Text(Point(x + bar_width / 2, 250 - bar_height - 10), str(value))
        count_label.setTextColor("black")  # Set text color
        count_label.draw(win)

        x += bar_width + bar_spacing

        # Display a message on the window
        message = Text(Point(220, 320), str(max_value) + " " + "Outcomes in Total")
        message.setSize(15)
        message.setStyle("italic")
        message.draw(win)


def store_progression_data(_pass, _defer, _fail):  # Function for create list for the corresponding credit outcomes
    progression_data.append([_pass, _defer, _fail])


while True:  # Loop for the entire program which have to ask for multiple inputs if needed
    while True:  # Loop for check total credits whether in proper value or not
        _pass = get_credit("Enter credits for Pass: ")
        _defer = get_credit("Enter credits for Defer: ")
        _fail = get_credit("Enter credits for Fail: ")

        total_credits = _pass + _fail + _defer
        if total_credits == 120:
            break
        else:
            print("Total Credit should equal to 120")

    store_progression_data(_pass, _defer, _fail)

    print(_pass)
    print(_defer)
    print(_fail)

    # Conditions for "Outcomes"
    if _pass == 120 and _defer == 0 and _fail == 0:
        print("Progression outcome:Progress")
        result = "progress"
        output[0] += 1
        file_creating()  # calling function for creating the file as above-mentioned
    elif 100 <= _pass < 120 and 0 <= _defer <= 20 and _fail <= 20:
        print("progression outcome:Progress (module trailer)")
        result = "trailer"
        output[1] += 1
        file_creating()  # calling function for creating the file as above-mentioned
    elif 40 <= _pass <= 80 and 0 <= _defer <= 80 and 0 <= _fail <= 60:
        print("Progression outcome: Module Retriever")
        result = "retriever"
        output[2] += 1
        file_creating()  # calling function for creating the file as above-mentioned
    elif 0 <= _pass <= 40 and 0 <= _defer <= 40 and 80 <= _fail <= 120:
        print("Progression outcome: Exclude")
        result = "exclude"
        output[3] += 1
        file_creating()  # calling function for creating the file as above-mentioned
    elif _pass == 20 and 40 <= _defer <= 100 and 0 <= _fail <= 60:
        print("Progression outcome: Module Retriever")
        output[2] += 1
        result = "retriever"
        file_creating()  # calling function for creating the file as above-mentioned
    elif _pass == 0 and 120 >= _defer >= 60 >= _fail >= 0:
        print("Progression outcome: Module Retriever")
        output[2] += 1
        result = "retriever"
        file_creating()  # calling function for creating the file as above-mentioned

    while True:
        print("\nWould you like to enter another set of data?\nPress 'y' for continue or press 'q' to quit"
              "")
        loop = input("y or q : ")
        print()
        if loop.lower() in ("y", "q"):
            break
    if loop.lower() != "y":
        # Draw histogram
        win = GraphWin("Progression Outcomes Histogram", 500, 350)
        # Call the funtion created , to display histogram
        draw_histogram(win)
        try:
            win.getMouse()  # Wait for a mouse click to close the window
            win.close()
        except GraphicsError:
            pass

        break

    # Display stored data
    outcome_labels = ["Progress", "Progress (module trailer)", "Module retriever", "Exclude"]

    print("Part 2:")
    for i, outcome in enumerate(progression_data):
        print(f"{outcome_labels[i]} - {outcome[0]}, {outcome[1]}, {outcome[2]}")
