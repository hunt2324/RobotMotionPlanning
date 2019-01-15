from cs1lib import *


if __name__ == '__main__':

    vx = 1
    x = 200
    y = 200

    def draw():
        global x, vx
        #clear()

        set_clear_color(1, 0, 0)
        #clear()

        set_fill_color(.2, .5, .9)
        set_stroke_color(1, 1, 0)
        draw_rectangle(100, 100, 200, 200)

        set_stroke_color(0, 0, 0)
        set_fill_color(1, 1, 1)
        draw_circle(200, 200, 100)

        draw_circle(x, y, 5)
        print("hello")

        x += vx

        if x + 5 > 300 or x - 5 < 100:
            vx *= -1

        set_font("Times")
        set_font_bold()
        set_font_italic()
        set_font_size(20)

        text = "Hello, world!"
        w = get_text_width(text)

        draw_text("Hello, world!", 200 - w / 2, 277)

        h = get_text_height()
        draw_text(str(mouse_x()), 10, 400)
        draw_text(str(mouse_y()), 10, 400 + h)
        draw_text(str(is_mouse_pressed()), 10, 400 + 2 * h)


    start_graphics(draw, width=500, height=500)
