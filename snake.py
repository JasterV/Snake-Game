import turtle
import time
import random

delay = 0.1
# Score
actual_score = 0
high_score = 0

# Turtles size
turtle_size = 20

# Set screen
wn = turtle.Screen()
wn.title("Snake Game")
wn.bgcolor("green")
wn.setup(width=600, height=600)
wn.tracer(0)

# Snake head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("black")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Snake food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(random.randint(-100, 100), random.randint(-100, 100))

# Pen Score
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.hideturtle()
pen.penup()
pen.goto(0, wn.window_height() // 2 - 40)
pen.write("Score : %d High Score: %d" % (actual_score, high_score), align='center', font=('courier', 24, 'normal'))


def update_score():
    pen.clear()
    pen.write("Score : %d High Score: %d" % (actual_score, high_score), align='center', font=('courier', 24, 'normal'))


def score_up():
    global actual_score
    global high_score
    global fin
    actual_score += 10
    if actual_score > high_score:
        high_score = actual_score
        fin.truncate(0)
        fin.write(str(high_score))


# Segments
segments = []


# Segments Functions
def new_segment():
    segment = turtle.Turtle()
    segment.speed(0)
    segment.shape("square")
    segment.color("gray")
    segment.penup()
    return segment


def move_all_segments():
    for i in range(len(segments) - 1, 0, -1):
        segments[i].goto(segments[i - 1].xcor(), segments[i - 1].ycor())
    if len(segments) > 0:
        segments[0].goto(head.xcor(), head.ycor())


# Movement functions
def go_up():
    if head.direction != 'down':
        head.direction = 'up'


def go_down():
    if head.direction != 'up':
        head.direction = 'down'


def go_left():
    if head.direction != 'right':
        head.direction = 'left'


def go_right():
    if head.direction != 'left':
        head.direction = 'right'


def move():
    y = head.ycor()
    x = head.xcor()
    if head.direction == 'up':
        head.sety(y + 20)
    if head.direction == 'down':
        head.sety(y - 20)
    if head.direction == 'right':
        head.setx(x + 20)
    if head.direction == 'left':
        head.setx(x - 20)


def move_food():
    height = wn.window_height() // 2 - turtle_size // 2
    width = wn.window_width() // 2 - turtle_size//2
    x = random.randint(-width, width)
    y = random.randint(-height, height)
    food.goto(x, y)


# keyboard bindings
wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")


# Detect collision
def collision():
    width = wn.window_width() // 2 - turtle_size//2
    heigth = wn.window_height() // 2 - turtle_size // 2
    if abs(head.xcor()) > width or abs(head.ycor()) > heigth:
        return True
    for elem in segments:
        if head.distance(elem) < turtle_size:
            return True
    return False


def remove_segments():
    for elem in segments:
        elem.hideturtle()
    segments.clear()


# Reset function
def reset_game():
    time.sleep(1)
    remove_segments()
    head.goto(0, 0)
    head.direction = 'stop'
    global actual_score
    actual_score = 0
    update_score()
    global delay
    delay = 0.1


# Score file
try:
    fin = open("high_score.txt", "a+")
    fin.seek(0)
    high_score = int(fin.readline())
    update_score()
    # Main game loop
    while True:
        wn.update()
        if head.distance(food) < turtle_size:
            score_up()
            update_score()
            move_food()
            segments.append(new_segment())
            delay -= 0.001
        move_all_segments()
        move()
        if collision():
            reset_game()
        time.sleep(delay)
except IOError:
    print("Error opening the score file")
finally:
    fin.close()
wn.mainloop()
