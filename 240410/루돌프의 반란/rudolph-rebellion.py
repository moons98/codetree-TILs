# -*- coding: utf-8 -*-
import sys


def interaction(x, y, dx, dy):
    # idx 가져오고, 해당 칸 지우고, 밀고
    idx = map_lst[x][y]

    while True:
        map_lst[x][y] = 0

        x += dx
        y += dy

        # 산타가 밖으로 밀려난 경우
        if x < 0 or x >= N or y < 0 or y >= N:
            santa[idx] = (-1, -1)
            return

        new_idx = map_lst[x][y]
        map_lst[x][y] = idx
        santa[idx] = (x, y)

        # 다시 산타와 충돌
        if new_idx > 0:
            idx = new_idx
        else:
            map_lst[x][y]
            return

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
    map_lst[x][y] = idx

    return


def move_rudolf():
    global rudolf

    tx, ty, distance = -1, -1, 2 * (N**2)
    rx, ry = rudolf

    # 가장 가까운 산타 좌표 구하기, 거리 같으면 r 클수록 >> c 클수록
    for r, c in santa:
        # 이미 빠져나간 산타라면 패스
        if (r, c) == (-1, -1):
            continue

        d = (rx - r) ** 2 + (ry - c) ** 2

        if d < distance:
            tx, ty = r, c
            distance = d
        elif d == distance:
            if r > tx or (r == tx and c > ty):
                tx, ty = r, c

    # 방향 구하기
    dx, dy = 0, 0
    if rx < tx:
        dx = 1
    elif rx > tx:
        dx = -1

    if ry < ty:
        dy = 1
    elif ry > ty:
        dy = -1

    # 충돌
    map_lst[rx][ry] = 0
    rx += dx
    ry += dy
    if map_lst[rx][ry] > 0:
        # 부딪힌 산타 번호
        idx = map_lst[rx][ry]
        collide(idx, rx, ry, dx, dy, C)

    rudolf = (rx, ry)
    map_lst[rx][ry] = -1

    return


def move_santa():
    rx, ry = rudolf

    for idx, (x, y) in enumerate(santa):
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
        if map_lst[tx][ty] == 0:
            # 추가 action 없음
            map_lst[x][y] = 0
            santa[idx] = (tx, ty)
            map_lst[tx][ty] = idx
        elif map_lst[tx][ty] == -1:
            # 루돌프와 충돌
            map_lst[x][y] = 0
            collide(idx, tx, ty, -1 * santa_x[d_loc], -1 * santa_y[d_loc], D)

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


"""
P명의 산타

1. 게임판의 구성 
    - NxN 격자, (r,c) 위치, 좌 상단 : (1,1)
    - M개의 턴에 걸쳐 진행, 매 턴마다 루돌프와 산타들이 한 번씩 움직임
    - 루돌프가 움직인 뒤, 1번 산타부터 P번 산타까지 순서대로 움직임
    - 기절하거나 탈락한 산타는 움직일 수 없음
    - 두 지점 사이 거리는 L2-norm

2. 루돌프의 움직임
    - 가장 가까운 산타를 향해 1칸 돌진
    - 2명 이상이면, r 클수록 >> c 클수록
    - 루돌프는 상하좌우, 대각선을 포함한 8방향 움직임 가능

3. 산타의 움직임
    - 1번부터 P번까지 순서대로 움직임
    - 루돌프에게 가까워지는 방향으로 1칸 이동
    - 다른 산타가 있는 칸이나 밖으로 움직일 수 없음
    - 움직일 수 있는 칸이 있더라도, 루돌프로부터 가까워지지 못하면 움직이지 않음
    - 상하좌우 4방향 중 한 곳으로 움직임
    - 상우하좌 우선순위

4. 충돌
    - 산타와 루돌프가 같은 칸에 있으면 충돌 발생
    - 루돌프가 움직여서 충돌 -> 해당 산타는 C 점수 얻음, 동시에 루돌프가 진행한 방향으로 C칸 밀려남
    - 산타가 움직여서 충돌 -> 산타는 D 점수 얻음, 동시에 산타는 자신이 이동해온 반대로 D칸 밀려남

5. 상호작용
    - 루돌프와의 충돌 후 산타는 밀려나는 칸에서 상호작용 발생
    - 착지 칸에 다른 산타가 있다면 1칸 해당 방향으로 밀려남, 연쇄적으로 1칸 이동

6. 기절
    - 산타는 루돌프와의 충돌 후 기절
    - 현재가 K턴 -> K+1까지 기절 -> K+2부터 정상
    - 기절 도중 충돌이나 상호작용으로 밀려날 수는 있음

7. 게임 종료
    - M번 턴에 걸쳐 루돌프, 산타가 순서대로 움직인 후 게임 종료
    - P명의 산타가 모두 게임에서 탈락하면 게임 즉시 종료
    - 매 턴 이후, 탈락하지 않은 산타들은 1점씩 추가 부여

각 산타가 얻은 최종 점수 출력
"""

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