# -*- coding: utf-8 -*-
import sys


def make_map():
    global map_lst

    new_map = [[0 for _ in range(N)] for _ in range(N)]

    rx, ry = rudolf
    new_map[rx][ry] = -1

    for idx, (r, c) in enumerate(santa):
        if (r, c) == (-1, -1):
            continue

        new_map[r][c] = idx

    map_lst = new_map

    return


def interaction(x, y, dx, dy):
    # map_lst[x][y]에 있는 산타를 dx, dy 방향으로 한 칸 밀어라
    idx = map_lst[x][y]

    nx = x + dx
    ny = y + dy

    # 산타가 밖으로 밀려난 경우
    if x < 0 or x >= N or y < 0 or y >= N:
        santa[idx] = (-1, -1)
        return

    # 위치 갱신
    santa[idx] = (nx, ny)

    # 다시 산타와 충돌
    if map_lst[nx][ny] > 0:
        idx = interaction(nx, ny, dx, dy)

    return


def collide(idx, x, y, dx, dy, s):
    # 점수 증가, 기절
    scores[idx] += s
    pass_out[idx] += 2

    # 방향 조정
    x += dx * s
    y += dy * s

    if x < 0 or x >= N or y < 0 or y >= N:
        santa[idx] = (-1, -1)
        return

    elif map_lst[x][y] > 0:
        interaction(x, y, dx, dy)

    # 단일 방향으로만 계속 밀려나는 action이므로 나중에 갱신해줘도 됨
    santa[idx] = (x, y)

    return


def move_rudolf():
    global rudolf

    sx, sy, distance = -1, -1, 2 * (N**2)
    rx, ry = rudolf

    # 가장 가까운 산타 좌표 구하기, 거리 같으면 r 클수록 >> c 클수록
    for r, c in santa:
        # 이미 빠져나간 산타라면 패스
        if (r, c) == (-1, -1):
            continue

        d = (rx - r) ** 2 + (ry - c) ** 2

        if d < distance:
            sx, sy = r, c
            distance = d
        elif d == distance:
            if r > sx or (r == sx and c > sy):
                sx, sy = r, c

    # 방향 구하기
    dx, dy = 0, 0
    if rx < sx:
        dx = 1
    elif rx > sx:
        dx = -1

    if ry < sy:
        dy = 1
    elif ry > sy:
        dy = -1

    # 이동
    rx += dx
    ry += dy

    # 충돌한 경우
    if map_lst[rx][ry] > 0:
        idx = map_lst[rx][ry]
        collide(idx, rx, ry, dx, dy, C)

    rudolf = (rx, ry)

    # 맵 갱신
    make_map()

    return


def move_santa():
    rx, ry = rudolf

    for idx, (x, y) in enumerate(santa):
        # 기준 방향 -1
        d_loc = -1

        # 이미 빠져나갔거나 기절중인 산타
        if (x, y) == (-1, -1):
            continue
        elif pass_out[idx]:
            continue

        # 방향 돌면서 거리 짧아지는 방향 구하기
        distance = (rx - x) ** 2 + (ry - y) ** 2
        for i in range(4):
            nx, ny = x + santa_x[i], y + santa_y[i]

            # 움직일 수 없는 좌표 or 다른 산타 존재
            if nx < 0 or nx >= N or ny < 0 or ny >= N:
                continue
            elif map_lst[nx][ny] > 0:
                continue

            # 거리 짧아지면 갱신
            d = (rx - nx) ** 2 + (ry - ny) ** 2
            if d < distance:
                distance = d
                d_loc = i

        # 방향 정해진 이후, 움직임 구현 -> 움직일 수 없는 상태
        if d_loc == -1:
            continue

        # 움직임 가능
        tx, ty = x + santa_x[d_loc], y + santa_y[d_loc]

        # 움직였지만 빈 칸 -> 추가 action 없음
        if map_lst[tx][ty] == 0:
            santa[idx] = (tx, ty)
        # 움직였고, 루돌프와 충돌
        elif map_lst[tx][ty] == -1:
            collide(idx, tx, ty, -1 * santa_x[d_loc], -1 * santa_y[d_loc], D)

        make_map()

    return


def check_finish():
    for loc in santa:
        if loc != (-1, -1):
            return True

    return False


def add_score():
    for idx, loc in enumerate(santa):
        if loc != (-1, -1):
            scores[idx] += 1


def cal_score():
    global answer

    answer = 0
    for loc, s in zip(santa, scores):
        if loc != (-1, -1):
            answer += s

    for i in scores[1:]:
        print(i, end=" ")
    print()


N, M, P, C, D = map(int, sys.stdin.readline().split())

# 전체 맵
map_lst = [[0 for _ in range(N)] for _ in range(N)]

# 루돌프 위치
r, c = map(int, sys.stdin.readline().split())
rudolf = (r - 1, c - 1)
map_lst[r - 1][c - 1] = -1

# 산타 기절 여부, 위치 : 1번 idx부터 시작
pass_out = [0 for _ in range(P + 1)]

santa = [(-1, -1) for _ in range(P + 1)]
for _ in range(P):
    idx, r, c = map(int, sys.stdin.readline().split())
    santa[idx] = (r - 1, c - 1)
    map_lst[r - 1][c - 1] = idx

# 산타 움직임 방향
santa_x = [-1, 0, 1, 0]
santa_y = [0, 1, 0, -1]

# 각 산타의 점수
scores = [0 for _ in range(P + 1)]


for i in range(M):
    move_rudolf()

    if not check_finish():
        break

    move_santa()

    if not check_finish():
        break

    add_score()

    pass_out = [max(0, i - 1) for i in pass_out]

cal_score()