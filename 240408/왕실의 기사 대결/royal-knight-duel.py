# -*- coding: utf-8 -*-
import sys
from collections import deque


# i번 기사가 d 방향으로 밀렸을 때 가장 바깥쪽의 좌표들을 반환
def cal_final_loc(i, d):
    r, c, h, w = solders[i]

    # 상
    if d == 0:
        loc = [(r + dx[d], y) for y in range(c, c + w)]
    elif d == 1:
        loc = [(x, c + w - 1 + dy[d]) for x in range(r, r + h)]
    elif d == 2:
        loc = [(r + h - 1 + dx[d], y) for y in range(c, c + w)]
    elif d == 3:
        loc = [(x, c + dy[d]) for x in range(r, r + h)]

    return loc


def check_move_ok(i, d):
    global visited

    visited = [0 for _ in range(n)]

    queue = deque()
    queue.append(i)
    while queue:
        i = queue.popleft()
        visited[i] = 1

        # 확인해야 하는 좌표값 계산
        locs = cal_final_loc(i, d)

        for x, y in locs:
            # 좌표 벗어나면
            if x < 0 or x >= l or y < 0 or y >= l:
                return False

            # 벽이 있으면
            elif map_lst[x][y] == 2:
                return False

            # 안 움직인 다른 기사 만나면 queue에 append
            if solder_map[x][y] >= 0 and not visited[solder_map[x][y]]:
                queue.append(solder_map[x][y])

        # print("queue : ", queue)
        # print("visited : ", visited)
        # print("locs : ", locs)

    return True


def move(i, d):
    global solders, solder_map

    # 움직일 수 없는 경우
    if not check_move_ok(i, d):
        # print("cannot move!!")
        return

    for idx, (r, c, _, _) in enumerate(solders):
        if not visited[idx]:
            continue

        # 움직인 기사들 좌표 조정
        solders[idx][:2] = [r + dx[d], c + dy[d]]

        # 데미지 반영, 움직임 시작한 기사는 데미지 받으면 안됨
        if idx != i:
            damage(idx)

    # 새로운 기사 맵 작성
    next_solder = [[-1 for _ in range(l)] for _ in range(l)]
    for idx, (r, c, h, w) in enumerate(solders):
        for x in range(r, r + h):
            for y in range(c, c + w):
                next_solder[x][y] = idx

    solder_map = next_solder

    return


def damage(idx):
    r, c, h, w = solders[idx]

    cnt = 0
    for x in range(r, r + h):
        for y in range(c, c + w):
            if map_lst[x][y] == 1:
                cnt += 1

    hp[idx] -= cnt
    scores[idx] += cnt
    if hp[idx] <= 0:
        solders[idx][:2] = [-1, -1]

    return


def cal_damage():
    global answer

    for idx, (r, c, _, _) in enumerate(solders):
        if (r, c) == (-1, -1):
            continue
        else:
            answer += scores[idx]

    return


def print_map(target):
    for i in target:
        print(i)
    print()


"""
왕실의 기사 대결

- LxL 크기의 체스판
- 좌상단 (1,1)
- 빈칸, 함정, 벽 상태 존재
- 기사 초기위치 (r,c), 좌상단 기준 hxw 크기를 가짐, 체력 k

1. 기사 이동
    - 상하좌우 이동 가능
    - 이동하려는 위치에 다른 기사가 있으면 연쇄적으로 밀려남
    - 기사가 이동하려는 방향의 끝에 벽이 있으면 모든 기사는 이동할 수 없음

2. 대결 데미지
    - 기사가 다른 기사를 밀치면, 밀쳐난 기사들이 피해를 입음
    - 해당 기사가 이동한 곳에서 wxh 직사각형 내에 놓인 함정의 수만큼 피해
    - 체력 이상의 데미지를 받은 경우, 사라짐
    - 명령을 받은 기사는 피해를 입지 않음
    - 기사들은 밀린 이후에 데미지를 입음
    - 밀쳐진 위치에 함정이 전혀 없으면, 그 기사는 피해를 전혀 입지 않음

Q번에 걸쳐 명령이 주어짐, 대결 이후 생존한 기사들이 받은 총 데미지 합 출력

sol)
    - 기사 맵을 만들어놓고(기사 번호로 영역 구분)
    - 방향에 따라 queue에 확인해야 하는 가장 반대편 좌표들 넣고 갱신
    - map_lst에서 벽의 유무 확인 필요, 밀리는지 확인 필요
"""

l, n, q = map(int, sys.stdin.readline().split())

map_lst = [list(map(int, sys.stdin.readline().split())) for _ in range(l)]

# 기사 맵
solder_map = [[-1 for _ in range(l)] for _ in range(l)]

# 기사 정보 (r, c, h, w, k)
solders = []

# i번 기사의 정보 (받은 데미지 합, 남은 hp)
scores = [0 for _ in range(n)]
hp = [0 for _ in range(n)]

for idx in range(n):
    r, c, h, w, k = map(int, sys.stdin.readline().split())

    # 좌표 조정
    r -= 1
    c -= 1
    solders.append([r, c, h, w])
    hp[idx] = k

    # 기사 맵에 정보 입력
    for x in range(r, r + h):
        for y in range(c, c + w):
            solder_map[x][y] = idx


# i번 기사, d번 방향
order = []
for _ in range(q):
    i, d = map(int, sys.stdin.readline().split())
    order.append([i - 1, d])

# 상 우 하 좌
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

# print("map_lst : ")
# print_map(map_lst)

# print("solders : ", solders)
# print("hp : ", hp)
# print("solder_map : ")
# print_map(solder_map)


answer = 0
for idx, (i, d) in enumerate(order):
    move(i, d)

    # print("idx : ", idx)
    # print("i, d : ", i, d)
    # print()

    # print("solders : ", solders)
    # print("hp : ", hp)
    # print("solder_map : ")
    # print_map(solder_map)


cal_damage()
print(answer)