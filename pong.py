import turtle
import winsound
import random

def playSound():
    winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)

MAX_SCORE = 11
DIR = (-1, 1)
BALL_SPEED = 0.5
PADDLE_SPEED = 10

board = turtle.Screen()
board.title("Pong by kirsirinnesalo")
board.bgcolor("black")
board.setup(width=800, height=600)
board.tracer(0)

score_a = 0
score_b = 0

paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.color("white")
paddle_a.shape("square")
paddle_a.shapesize(stretch_wid=5, stretch_len=0.5)
paddle_a.penup()
paddle_a.goto(-350, 0)

paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.color("white")
paddle_b.shape("square")
paddle_b.shapesize(stretch_wid=5, stretch_len=0.5)
paddle_b.penup()
paddle_b.goto(350, 0)

ball = turtle.Turtle()
ball.speed(0)
ball.color("white")
ball.shape("circle")
ball.shapesize(stretch_wid=0.5, stretch_len=0.5)
ball.penup()
ball.goto(0, 0)
ball.dx = random.choice(DIR) * BALL_SPEED
ball.dy = random.choice(DIR) * BALL_SPEED

score = turtle.Turtle()
score.speed(0)
score.color("white")
score.penup()
score.hideturtle()
score.goto(0, 200)

def showScore():
    score.clear()
    score.write("{}       {}".format(score_a, score_b), 
                align="center", font=("Courier", 54, "normal"))

def paddle_a_up():
    if (paddle_a.ycor() < 240):
        y = paddle_a.ycor()
        y += PADDLE_SPEED
        paddle_a.sety(y)

def paddle_a_down():
    if (paddle_a.ycor() > -240):
        y = paddle_a.ycor()
        y -= PADDLE_SPEED
        paddle_a.sety(y)

def paddle_b_up():
    if (paddle_b.ycor() < 240):
        y = paddle_b.ycor()
        y += PADDLE_SPEED
        paddle_b.sety(y)

def paddle_b_down():
    if (paddle_b.ycor() > -240):
        y = paddle_b.ycor()
        y -= PADDLE_SPEED
        paddle_b.sety(y)

def moveBall():
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

def quitGame():
    board.bye()

board.listen()
board.onkeypress(paddle_a_up, "w")
board.onkeypress(paddle_a_down, "s")
board.onkeypress(paddle_b_up, "Up")
board.onkeypress(paddle_b_down, "Down")
board.onkeypress(quitGame, "Escape")

gameover = turtle.Turtle()
gameover.speed(0)
gameover.color("white")
gameover.penup()
gameover.hideturtle()

def isGameOver():
    if score_a >= MAX_SCORE or score_b >= MAX_SCORE:
        ball.dx = 0
        ball.dy = 0
        gameover.goto(0, 100)
        gameover.write("Peli päättyi.",
                align="center", font=("Courier", 24, "bold"))
        gameover.goto(0, 50)
        gameover.write("{} on voittaja!".format("Pelaaja vasemmalla" if score_a > score_b else "Pelaaja oikealla"),
                align="center", font=("Courier", 24, "bold"))

while True:
    board.update()

    showScore()

    isGameOver()

    moveBall()

    #borders    
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1
        playSound()

    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1
        playSound()

    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_a += 1

    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_b += 1

    # collision
    if (ball.xcor() > 340 and ball.xcor() < 350) and (ball.ycor() < paddle_b.ycor() + 50 and ball.ycor() > paddle_b.ycor() - 50):
        ball.setx(340)
        ball.dx *= -1
        playSound()

    if (ball.xcor() < -340 and ball.xcor() > -350) and (ball.ycor() < paddle_a.ycor() + 50 and ball.ycor() > paddle_a.ycor() - 50):
        ball.setx(-340)
        ball.dx *= -1
        playSound()

