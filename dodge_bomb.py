import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900


delta = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}

left_total_mv = [(-5, +5), (-5, 0), (-5, -5)] 
right_total_mv = [
    (0,-5), (+5, -5), (+5, 0), 
    (+5, +5),(0, +5),
]

accs = [a for a in range(1, 11)]


def check_bound(obj_rct: pg.Rect):
    """
    引数: 引数はこうかとん、または爆弾のRect
    戻り値: タプル(縦と横の方向の判定結果)
    Rectオブジェクトのleft, right, top, bottomの値から画面内・外を判断する
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    """こうかとん"""    
    kk_img = pg.image.load("fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = (900, 400)
    turn_kk_img = pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), 90, 1.0)
    kk_img_dct = {}
    for i, num in enumerate(left_total_mv, -1):
        kk_img_dct[num] = pg.transform.rotozoom(kk_img, -45*i, 1.0)
    for i, num in enumerate(right_total_mv):
        kk_img_dct[num] = pg.transform.rotozoom(turn_kk_img, -45*i, 1.0)
    kk_img_dct[(0, 0)] = kk_img

    """爆弾"""
    bd_img = pg.Surface((20, 20))#練習1
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)
    bd_img.set_colorkey((0, 0, 0))
    bd_rct = bd_img.get_rect()
    x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    bd_rct.center = (x, y)
    #bb_imgs = []
    #for r in range(1, 11):
    #    bb_img = pg.Surface((20*r, 20*r))
    #    pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
    #    bb_img.set_colorkey((0, 0, 0))
    #    bb_imgs.appned(bb_img)
    #bb_rcts = []
    #for datum in bb_imgs:
    #    bb_rcts.append(datum.get_rect())
    #    datum.center = (x, y)
    #bd_rct.center = (x, y)
    vx, vy = +5, +5 #練習2

    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return

        if kk_rct.colliderect(bd_rct):
            print("ゲームオーバー")
            return

        screen.blit(bg_img, [0, 0])

        """こうかとん"""
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in delta.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv[0], sum_mv[1])
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img_dct[(sum_mv[0], sum_mv[1])], kk_rct)
        """爆弾"""
        bd_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bd_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        #avx, avy = vx*accs[min(tmr//500, 9)], vy*accs[min(tmr//500, 9)]
        #bb_img = bb_imgs[min(tmr//500, 9)]
        screen.blit(bd_img, bd_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()