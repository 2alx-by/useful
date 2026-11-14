import math
import turtle


def draw_rainbow():
    colors = ("red", "orange", "yellow", "green", "blue", "indigo", "violet")
    outer_radius = 220
    band_width = 22

    screen = turtle.Screen()
    screen.title("Rainbow")
    screen.bgcolor("white")

    pen = turtle.Turtle()
    pen.hideturtle()
    pen.speed(0)
    pen.pensize(band_width)

    for band, color in enumerate(colors):
        radius = outer_radius - band * band_width
        pen.color(color)
        pen.penup()
        pen.goto(-radius, 0)
        pen.setheading(0)
        pen.pendown()

        for step in range(181):
            angle = math.radians(180 - step)
            pen.goto(radius * math.cos(angle), radius * math.sin(angle))

    pen.penup()
    pen.goto(0, -outer_radius - 35)
    screen.exitonclick()


if __name__ == "__main__":
    draw_rainbow()