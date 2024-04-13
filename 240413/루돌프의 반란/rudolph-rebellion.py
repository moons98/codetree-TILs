# -*- coding: utf-8 -*-
import sys

MAX_DISTANCE = sys.maxsize


def make_map():
    global map_lst

    map_lst = [[0 for _ in range(N)] for _ in range(N)]
    for idx, (r, c) in enumerate(santa):
        if (r, c) != (-1, -1):
            map_lst[r][c] = idx

    return


def move_rudolf():
    global rudolf

    max_r, max_c, max_d = -1, -1, MAX_DISTANCE

    # 루돌프 좌표
    (rx, ry) = rudolf

    # 가장 가까운 산타, r 클수록 >> c 클수록 우선순위
    for r, c in santa:
        if (r, c) == (-1, -1):
            continue

        d = (rx - r) ** 2 + (ry - c) ** 2
        if d < max_d:
            (max_r, max_c) = (r, c)
        elif d == max_d:
            if r > max_r or (r == max_r and c > max_c):
                (max_r, max_c) = (r, c)
        else:
            continue

        max_d = d

    # 루돌프가 움직일 방향 정하기
    dx, dy = 0, 0
    if rx < max_r:
        dx = 1
    elif rx > max_r:
        dx = -1

    if ry < max_c:
        dy = 1
    elif ry > max_c:
        dy = -1

    # 움직임
    nx, ny = rx + dx, ry + dy
    rudolf = (nx, ny)

    # 산타와 충돌 시
    if map_lst[nx][ny]:
        collide(map_lst[nx][ny], (nx, ny), (dx, dy), C)
        make_map()

    return


def move_santa():
    # 루돌프 위치
    rx, ry = rudolf

    for idx in range(1, P + 1):
        (x, y) = santa[idx]

        # 기절한 산타 패스
        if stun_santa[idx]:
            continue

        # 이미 빠져나간 산타는 패스
        if (x, y) == (-1, -1):
            continue

        # 루돌프와의 거리 계산, 움직일 좌표 보관
        distance = (rx - x) ** 2 + (ry - y) ** 2
        tx, ty, ti = -1, -1, -1

        # 4방향 돌면서 짧아지는 곳 찾음
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]

            # 격자 벗어난 경우
            if nx < 0 or nx >= N or ny < 0 or ny >= N:
                continue

            # 다른 산타가 있는 경우
            if map_lst[nx][ny]:
                continue

            # 거리 가까워지면 갱신
            d = (rx - nx) ** 2 + (ry - ny) ** 2
            if d < distance:
                (tx, ty) = (nx, ny)
                ti = i
                distance = d

        # 해당 방향으로 움직임
        if ti != -1:
            santa[idx] = (tx, ty)

            # 루돌프와 충돌 있는지 확인
            if (rx, ry) == (tx, ty):
                collide(idx, (rx, ry), (-dx[ti], -dy[ti]), D)

        # 매 산타 움직임 끝날때마다 map_lst 갱신 필요
        make_map()

    return


def collide(idx, loc, dir, s):
    x, y = loc
    dx, dy = dir

    # 충돌한 산타 점수 증가, 기절
    score[idx] += s
    stun_santa[idx] = 2

    # 바뀐 위치 확인
    nx = x + dx * s
    ny = y + dy * s

    # 격자 벗어난 경우
    if nx < 0 or nx >= N or ny < 0 or ny >= N:
        santa[idx] = (-1, -1)
        return

    # 위치 갱신
    santa[idx] = (nx, ny)

    # 다른 산타와 만난 경우 상호작용
    new_idx = map_lst[nx][ny]
    if new_idx and new_idx != idx:
        interaction((nx, ny), (dx, dy))

    return


def interaction(loc, dir):
    x, y = loc
    dx, dy = dir

    # 해당 위치 산타 idx
    idx = map_lst[x][y]

    # 움직이는 위치
    nx = x + dx
    ny = y + dy

    # 격자 벗어난 경우
    if nx < 0 or nx >= N or ny < 0 or ny >= N:
        santa[idx] = (-1, -1)
        return

    # 움직임
    santa[idx] = (nx, ny)

    # 움직이는 위치에 산타 있는지 확인
    if map_lst[nx][ny]:
        interaction((nx, ny), (dx, dy))

    return


def add_score():
    for i in range(P + 1):
        if santa[i] != (-1, -1):
            score[i] += 1
    return


def check_finish():
    for i in range(P + 1):
        if santa[i] != (-1, -1):
            return True

    return False


def print_map():
    for i in map_lst:
        print(i)
    print()


"""
루돌프의 반란

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

루돌프 -> 산타를 향해 돌진 (전체 산타 순회 필요)
산타 -> 루돌프를 향해 돌진

"""

N, M, P, C, D = map(int, sys.stdin.readline().split())

map_lst = [[0 for _ in range(N)] for _ in range(N)]

rudolf = tuple(i - 1 for i in map(int, sys.stdin.readline().split()))

# 산타 기절 여부
stun_santa = [0] * (P + 1)

# 산타가 얻은 점수
score = [0] * (P + 1)

# 산타 움직이는 방향
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

# 산타 idx는 1번부터 시작, 맵은 (0,0)부터 시작
santa = [(-1, -1)] * (P + 1)
for _ in range(P):
    idx, r, c = map(int, sys.stdin.readline().split())
    santa[idx] = (r - 1, c - 1)
    map_lst[r - 1][c - 1] = idx


# print("santa: ", santa)
# print("rudolf: ", rudolf)
# print_map()

# 게임 진행
for i in range(M):
    move_rudolf()
    move_santa()

    add_score()

    if not check_finish():
        break

    stun_santa = [max(0, i - 1) for i in stun_santa]

    # print("i:", i)
    # print("santa: ", santa)
    # print("rudolf: ", rudolf)
    # print("stun_santa: ", stun_santa)
    # print("score: ", score)
    # print_map()

for i in score[1:]:
    print(i, end=" ")
print()