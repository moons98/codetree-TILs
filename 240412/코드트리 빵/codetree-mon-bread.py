# -*- coding: utf-8 -*-
import sys
from collections import deque

INT_MAX = sys.maxsize


def bfs(start_loc):
    global visited

    visited = [[0 for _ in range(n)] for _ in range(n)]

    x, y = start_loc

    queue = deque()
    queue.append((x, y))
    visited[x][y] = 1

    while queue:
        x, y = queue.popleft()

        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]

            # 격자 밖, 벽, 이미 방문
            if nx < 0 or nx >= n or ny < 0 or ny >= n:
                continue
            elif map_lst[nx][ny] == -1:
                continue
            elif visited[nx][ny]:
                continue

            # 움직일 수 있는 곳
            queue.append((nx, ny))
            visited[nx][ny] = visited[x][y] + 1

    return


def move():
    # 각 사람별로 움직임 실시
    for p in range(1, m + 1):
        x, y = people[p]
        if (x, y) == (-1, -1):
            continue

        bfs(p_target[p])

        # 사람 기준 상하좌우 보면서 가장 짧은 곳 찾기
        min_x, min_y, min_d = -1, -1, INT_MAX
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if nx < 0 or nx >= n or ny < 0 or ny >= n:
                continue
            elif map_lst[nx][ny] == -1:
                continue

            if visited[nx][ny] < min_d:
                min_x, min_y = nx, ny
                min_d = visited[nx][ny]

        # 움직임
        people[p] = (min_x, min_y)

    return


def arrive():
    # 각 사람별로 편의점 도착했는지 확인
    for i in range(1, m + 1):
        (x, y) = people[i]
        if (x, y) == p_target[i]:
            map_lst[x][y] = -1
            people[i] = (-1, -1)

    return


def bfs_add(start_loc):
    global visited

    visited = [[0 for _ in range(n)] for _ in range(n)]

    x, y = start_loc

    queue = deque()
    queue.append((x, y))
    visited[x][y] = 1

    while queue:
        x, y = queue.popleft()

        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]

            # 격자 밖, 벽, 이미 방문
            if nx < 0 or nx >= n or ny < 0 or ny >= n:
                continue
            elif map_lst[nx][ny] == -1:
                continue
            elif visited[nx][ny]:
                continue

            if map_lst[nx][ny] == 1:
                return (nx, ny)

            # 움직일 수 있는 곳
            queue.append((nx, ny))
            visited[nx][ny] = visited[x][y] + 1

    return


def add_people(t):
    # 가장 가까운 베이스캠프 찾기
    (x, y) = bfs_add(p_target[t])

    # 베이스캠프 입장
    people[t] = (x, y)
    map_lst[x][y] = -1

    return


def check_finish():
    for i in range(1, m + 1):
        if people[i] != (-1, -1):
            return False

    return True


def print_map():
    for i in map_lst:
        print(i)
    print()


"""
코드트리 빵

m명의 사람이 빵 구하고자 함.
m번 사람은 각각 m분에 베이스캠프에서 출발 -> 편의점으로 이동 시작
사람들이 목표로 하는 편의점은 모두 다름

n x n 격자

1. 이동
    - 격자에 있는 사람들이 본인이 가고 싶은 방향을 향해 1칸 움직임
    - 최단거리로 움직임, 여러가지라면 (상 좌 우 하) 우선순위

2. 편의점 도착
    - 편의점 도착 시, 해당 편의점에서 멈춤
    - 다른 사람들은 이 칸은 더이상 이용할 수 없음

3.
    - 현재 시간이 t분, t<=m이라면 t번 사람은 자신이 가고 싶은 편의점과 가장 가까운 베이스캠프로 들어감
    - 행이 작은 >> 열이 작은 우선순위
    - t번 사람이 베이스 캠프로 이동하는 데에는 시간 소요가 없음

    - 해당 베이스 캠프 칸을 지날 수 없음
    - t번 사람이 움직이기 시작해도 절대 지날 수 없음
    - 격자에 있는 사람들이 모두 이동 후에 지나갈 수 없어짐

bfs로 각 편의점과 가장 가까운 베이스캠프를 구함
사람이 이동하고자 하는 방향은??
    - 최단거리이므로 일단 bfs
    - 편의점에서 시작해서 사람 위치 도달하면, 그 이상은 append하지 말고 돌림
    - 이후 상우하좌 보면서 짧은 거리 찾아지면 그 방향으로 움직임

베이스 캠프 칸 1
이동할 수 없는 칸 -1

move()은 목표가 정해져있음
add_people()은 가장 먼저 만나는 베이스캠프

"""

n, m = map(int, sys.stdin.readline().split())

map_lst = []
basecamp = []
for r in range(n):
    tmp = list(map(int, sys.stdin.readline().split()))
    for c in range(n):
        if tmp[c] == 1:
            basecamp.append((r, c))

    map_lst.append(tmp)

dx = [-1, 0, 0, 1]
dy = [0, -1, 1, 0]

people = [(-1, -1) for _ in range(m + 1)]
p_target = [(-1, -1)]
for _ in range(m):
    r, c = map(int, sys.stdin.readline().split())
    p_target.append((r - 1, c - 1))

time = 1
while True:
    if time >= 2:
        move()
        arrive()

    if time <= m:
        add_people(time)

    if time > m:
        if check_finish():
            break

    time += 1

    # print_map()
    # print(people)
    # if time == 3:
    #     break

print(time)