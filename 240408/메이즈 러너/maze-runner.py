# -*- coding: utf-8 -*-
import sys


def move():
    global answer, participant

    ex, ey = exit_loc

    for idx, (x, y) in enumerate(participant):
        # 행이동 먼저 시도
        if ex != x:
            nx, ny = x, y
            if ex > nx:
                nx += 1
            else:
                nx -= 1

            if not map_lst[nx][ny]:
                participant[idx] = (nx, ny)
                answer += 1
                continue

        if ey != y:
            nx, ny = x, y
            if ey > ny:
                ny += 1
            else:
                ny -= 1

            if not map_lst[nx][ny]:
                participant[idx] = (nx, ny)
                answer += 1
                continue

    new_participant = [i for i in participant if i != exit_loc]
    participant = new_participant

    return


def find_square():
    global sx, sy, square_size

    ex, ey = exit_loc
    tx, ty, distance = n, n, 20

    for x, y in participant:
        # 참가자와 출구 사이 사각형 한 변의 길이 구하기
        d = max(abs(ex - x), abs(ey - y))

        lr_x, lr_y = max(ex, x), max(ey, y)
        ul_x, ul_y = max(0, lr_x - d), max(0, lr_y - d)

        # 거리가 작은 경우 lr 갱신 -> max 때리고 d만큼 빼서 ul 구하기
        if d == distance:
            if ul_x < tx:
                tx, ty = ul_x, ul_y
            elif ul_x == tx and ul_y < ty:
                tx, ty = ul_x, ul_y
        elif d < distance:
            tx, ty = ul_x, ul_y
            distance = d

    sx, sy, square_size = tx, ty, distance

    return


def rotate():
    global participant, exit_loc

    # ul, lr 좌표 구하기
    ul_x, ul_y = sx, sy
    lr_x, lr_y = sx + square_size, sy + square_size

    # 내구도 감소
    for x in range(ul_x, lr_x + 1):
        for y in range(ul_y, lr_y + 1):
            if map_lst[x][y] > 0:
                map_lst[x][y] -= 1

    # 정사각형 회전
    for x in range(ul_x, lr_x + 1):
        for y in range(ul_y, lr_y + 1):
            rx, ry = x - ul_x, y - ul_y
            next_patch[ry + ul_x][square_size - rx + ul_y] = map_lst[x][y]

    # map_lst에 next_patch 값 갱신
    for x in range(ul_x, lr_x + 1):
        for y in range(ul_y, lr_y + 1):
            map_lst[x][y] = next_patch[x][y]

    # 사람 회전
    for idx, (x, y) in enumerate(participant):
        # 정사각형 내에 있을 때만 회전 -> 잔차 구해서 더하는 방식
        if ul_x <= x <= lr_x and ul_y <= y <= lr_y:
            rx, ry = x - ul_x, y - ul_y
            participant[idx] = (ry + ul_x, square_size - rx + ul_y)

    # 출구 회전
    ex, ey = exit_loc
    rx, ry = ex - ul_x, ey - ul_y
    exit_loc = (ry + ul_x, square_size - rx + ul_y)

    return


def print_map():
    for i in map_lst:
        print(i)
    print()


n, m, k = map(int, sys.stdin.readline().split())

map_lst = [list(map(int, sys.stdin.readline().split())) for _ in range(n)]
next_patch = [[0 for _ in range(n)] for _ in range(n)]

# 참가자 좌표
participant = []
for _ in range(m):
    x, y = map(int, sys.stdin.readline().split())
    participant.append((x - 1, y - 1))

# 출구 좌표
x, y = map(int, sys.stdin.readline().split())
exit_loc = (x - 1, y - 1)

# 참가자 이동 거리 합 기록
answer = 0

# 회전해야 하는 최소 정사각형 정보
sx, sy, square_size = 0, 0, 0


for _ in range(k):
    move()

    # 모든 사람이 탈출했으면 종료
    if not participant:
        break

    find_square()
    rotate()

print(answer)
print(exit_loc[0] + 1, exit_loc[1] + 1)