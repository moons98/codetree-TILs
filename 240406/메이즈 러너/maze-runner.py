# -*- coding: utf-8 -*-
import copy
import sys


def print_map(patch):
    for i in patch:
        print(i)
    print()


def move():
    global participant, answer

    new_participant = []

    tx, ty = exit_loc
    for x, y in participant:
        map_lst[x][y] += 1

        check_dir = []
        if x > tx:
            check_dir.append(0)
        elif x < tx:
            check_dir.append(2)

        if y > ty:
            check_dir.append(1)
        elif y < ty:
            check_dir.append(3)

        # print(f"p: {(x, y)} d: {check_dir}")

        for d in check_dir:
            nx = x + dx[d]
            ny = y + dy[d]

            # 벽 만난 경우
            if map_lst[nx][ny] > 0:
                continue

            # 움직일 수 있음
            (x, y) = (nx, ny)
            answer += 1
            break

        # 출구
        if (x, y) == exit_loc:
            continue

        # 출구 아니면 새로운 자리 갱신
        map_lst[x][y] -= 1
        new_participant.append((x, y))

    participant = new_participant

    return


def choose():
    people = []
    min_distance = 20

    exit_x, exit_y = exit_loc
    for x, y in participant:
        d = max(abs(x - exit_x), abs(y - exit_y))
        if d < min_distance:
            min_distance = d
            people.append([x, y])
        elif d == min_distance:
            people.append([x, y])

    # 작은 순 정렬
    people.sort(key=lambda x: (x[0], x[1]))

    return people[0], min_distance


def rotate():
    global exit_loc, participant

    # 정사각형 구하기
    [tx, ty], d = choose()
    exit_x, exit_y = exit_loc

    # 좌상단이 0보다 작아지는 경우 처리
    [lr_x, lr_y] = [max(tx, exit_x), max(ty, exit_y)]
    [ul_x, ul_y] = [max(0, lr_x - d), max(0, lr_y - d)]
    if lr_x < d or lr_y < d:
        [lr_x, lr_y] = [ul_x + d, ul_y + d]

    # 돌아갈 patch 떼오기
    # print(f"(tx, ty), d : {(tx, ty), d}")
    # print(f"exit_loc : {exit_loc}")
    # print(f" ul_x, ul_y : {ul_x, ul_y}, lr_x, lr_y: {lr_x, lr_y}")

    new_rec = [map_lst[i][ul_y : lr_y + 1] for i in range(ul_x, lr_x + 1)]

    # print("new_rec :")
    # print_map(new_rec)

    for x in range(d + 1):
        for y in range(d + 1):
            # 내구도 감소
            if new_rec[x][y] > 0:
                new_rec[x][y] -= 1

    # 회전
    rotated_rec = copy.deepcopy(new_rec)
    for x in range(d + 1):
        for y in range(d + 1):
            rotated_rec[y][d - x] = new_rec[x][y]

    # 원본 map에 patch 붙이기
    for x in range(d + 1):
        map_lst[x + ul_x][ul_y : lr_y + 1] = rotated_rec[x]

    # 참가자, 출구 위치 변경 -> 상대 위치 계산 후 ul 좌표 더하기!
    for idx, (x, y) in enumerate(participant):
        if ul_x <= x <= lr_x and ul_y <= y <= lr_y:
            s_x, s_y = (x - ul_x, y - ul_y)
            participant[idx] = (s_y + ul_x, d - s_x + ul_y)

    if ul_x <= exit_x <= lr_x and ul_y <= exit_y <= lr_y:
        s_x, s_y = (exit_x - ul_x, exit_y - ul_y)
        exit_loc = (s_y + ul_x, d - s_x + ul_y)

    return


def cal_answer():
    print(answer)

    ex, ey = exit_loc
    print(ex + 1, ey + 1)
    return


"""
### 메이즈 러너

1. 미로는 NxN 격자, (r,c) 좌표, M명의 참가자

2. 미로의 각 칸은 세 가지 상태 존재
    - 빈 칸 : 참가자가 이동 가능
    - 벽
        이동 불가, 1~9 사이의 내구도
        회전 시, 내구도가 1씩 깎임
        내구도가 0이 되면 -> 빈칸으로 바뀜
    - 출구 : 참가자가 도착하면, 즉시 탈출
   
### 동작 
 
3. 1초마다 참가자는 한 칸씩 움직임
    - 최단 거리는 abs(x) + abs(y)
    - 참가자는 동시에 움직임 -> 한 칸에 2명 이상 존재 가능
    - 상하좌우 움직일 수 있음 -> 상하 움직임 >> 좌우 움직임
    - 움직일 수 없으면 그대로

4. 미로 회전
    - 한 명 이상의 참가자와 출구를 포함한 가장 작은 정사각형을 잡음
    - 2개 이상이라면 r 작을수록 >> c 작을수록 우선 선택 
    - 시계방향으로 정사각형 90도 회전, 회전된 벽은 내구도 1씩 깎임

K초 동안 반복, K초 전에 모든 참가자가 탈출하면 게임 끝
모든 참가자들의 이동 거리 합과 출구 좌표 출력

sol)
    - dfs로 정사각형 잡기

"""

n, m, k = map(int, sys.stdin.readline().split())

map_lst = [list(map(int, sys.stdin.readline().split())) for _ in range(n)]

# 참가자 좌표
participant = []
for _ in range(m):
    x, y = map(int, sys.stdin.readline().split())

    participant.append((x - 1, y - 1))
    map_lst[x - 1][y - 1] -= 1

# 상, 좌, 하, 우
dx = [-1, 0, 1, 0]
dy = [0, -1, 0, 1]

# 출구 좌표
x, y = map(int, sys.stdin.readline().split())
exit_loc = (x - 1, y - 1)
answer = 0

# print_map(map_lst)

for time in range(k):
    # print(f"time: {time}")
    # print()

    move()
    # print("move")
    # print("participant : ", participant)
    # print("exit_loc : ", exit_loc)
    # print_map(map_lst)

    if not participant:
        break

    rotate()
    # print("rotate")
    # print("participant : ", participant)
    # print_map(map_lst)

    # print("answer : ", answer)
    # print("exit_loc : ", exit_loc)
    # print_map(map_lst)
    # print()

cal_answer()