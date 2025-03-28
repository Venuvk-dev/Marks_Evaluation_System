from graphics import *
import datetime
import statistics

# Global variables
range_list = [0, 20, 40, 60, 80, 100, 120]
progression_data = []  # List to store progression data
output = [0, 0, 0, 0]
total_students = 0  # Track total number of students processed

# Error logging functionality
def log_error(error_message):
    """Log errors to a file for tracking and debugging"""
    with open("error_log.txt", "a") as error_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_file.write(f"{timestamp}: {error_message}\n")

def file_creating(result, _pass, _defer, _fail):
    """Save progression results to a file"""
    try:
        with open("Credit outcomes.txt", "a") as file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{timestamp} - {result.upper()}: Pass={_pass}, Defer={_defer}, Fail={_fail}\n")
    except IOError as e:
        log_error(f"File writing error: {e}")

def store_progression_data(_pass, _defer, _fail):
    """Store progression data in the global list"""
    progression_data.append((_pass, _defer, _fail))

def get_credit(credit_input):
    """Get and validate user input for credits"""
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            credit = int(input(credit_input))
            if credit in range_list:
                return credit
            else:
                print(f"Out of range: The credits should be in {range_list}")
        except ValueError:
            print("Integer required")
    return None

def draw_histogram(win):
    """Draw histogram for progression outcomes"""
    colors = ["aqua", "chartreuse", "violet", "moccasin"]
    labels = ["Progress", "Trailing", "Retriever", "Exclude"]
    max_value = max(output) if total_students > 0 else 1  # Avoid division by zero

    bar_width = 80
    bar_spacing = 5
    x = 50

    for i, value in enumerate(output):
        bar_height = (value / max_value) * 200 if max_value > 0 else 0
        bar = Rectangle(Point(x, 250), Point(x + bar_width, 250 - bar_height))
        bar.setFill(colors[i])
        bar.draw(win)

        label = Text(Point(x + bar_width / 2, 260), labels[i])
        label.draw(win)

        percentage = (value / total_students * 100) if total_students > 0 else 0
        count_label = Text(Point(x + bar_width / 2, 250 - bar_height - 10), f"{value} ({percentage:.1f}%)")
        count_label.setTextColor("black")
        count_label.draw(win)

        x += bar_width + bar_spacing

    total_message = Text(Point(220, 320), f"Total Students: {total_students}")
    total_message.setSize(12)
    total_message.setStyle("bold")
    total_message.draw(win)

def generate_statistical_report():
    """Generate a statistical report of progression data"""
    if not progression_data:
        print("No data available for statistical analysis.")
        return

    try:
        with open("progression_report.txt", "w") as report_file:
            report_file.write("Comprehensive Progression Statistical Report\n")
            report_file.write("=" * 50 + "\n")
            report_file.write(f"Total Students Processed: {total_students}\n\n")

            for i, label in enumerate(["Progress", "Trailing", "Retriever", "Exclude"]):
                report_file.write(f"{label} Outcomes: {output[i]} ({output[i]/total_students*100:.1f}%)\n")

            pass_credits = [data[0] for data in progression_data]
            defer_credits = [data[1] for data in progression_data]
            fail_credits = [data[2] for data in progression_data]

            report_file.write("\nCredit Analysis:\n")
            report_file.write(f"Pass Credits - Mean: {statistics.mean(pass_credits):.2f}, Median: {statistics.median(pass_credits)}\n")
            report_file.write(f"Defer Credits - Mean: {statistics.mean(defer_credits):.2f}, Median: {statistics.median(defer_credits)}\n")
            report_file.write(f"Fail Credits - Mean: {statistics.mean(fail_credits):.2f}, Median: {statistics.median(fail_credits)}\n")

        print("Statistical report generated successfully in 'progression_report.txt'")
    except Exception as e:
        log_error(f"Report generation error: {e}")

def main():
    """Main function for handling student progression"""
    global total_students
    while True:
        while True:
            _pass = get_credit("Enter credits for Pass: ")
            _defer = get_credit("Enter credits for Defer: ")
            _fail = get_credit("Enter credits for Fail: ")

            if _pass is None or _defer is None or _fail is None:
                continue

            total_credits = _pass + _fail + _defer
            if total_credits == 120:
                break
            else:
                print("Total Credit should equal to 120")

        total_students += 1
        store_progression_data(_pass, _defer, _fail)

        if _pass == 120 and _defer == 0 and _fail == 0:
            print("Progression outcome: Progress")
            result = "progress"
            output[0] += 1
        elif 100 <= _pass < 120 and _fail <= 20:
            print("Progression outcome: Progress (module trailer)")
            result = "trailer"
            output[1] += 1
        elif (_pass <= 80 and _fail <= 60) or (_pass == 20 and _fail <= 60) or (_pass == 0 and _fail <= 60):
            print("Progression outcome: Module Retriever")
            result = "retriever"
            output[2] += 1
        elif _fail >= 80:
            print("Progression outcome: Exclude")
            result = "exclude"
            output[3] += 1

        file_creating(result, _pass, _defer, _fail)

        while True:
            print("\nWould you like to enter another set of data?\nPress 'y' to continue or 'q' to quit")
            loop = input("y or q : ").lower()
            if loop in ("y", "q"):
                break

        if loop != "y":
            win = GraphWin("Progression Outcomes Histogram", 500, 350)
            draw_histogram(win)
            
            generate_statistical_report()

            try:
                win.getMouse()  
                win.close()
            except GraphicsError:
                pass

            break

        outcome_labels = ["Progress", "Progress (module trailer)", "Module retriever", "Exclude"]
        print("Part 2:")
        for i, outcome in enumerate(progression_data):
            print(f"{outcome_labels[i]} - {outcome[0]}, {outcome[1]}, {outcome[2]}")

if __name__ == "__main__":
    main()
