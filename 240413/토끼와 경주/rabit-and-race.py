# -*- coding: utf-8 -*-
import copy
import heapq
import sys


class Rabbit:
    def __init__(self, pid, x, y, j):
        self.pid = pid
        self.x = x
        self.y = y
        self.j = j

    def __lt__(self, other):
        if self.j != other.j:
            return self.j < other.j
        elif self.x + self.y != other.x + other.y:
            return self.x + self.y < other.x + other.y
        elif self.x != other.x:
            return self.x < other.x
        elif self.y != other.y:
            return self.y < other.y
        else:
            return self.pid < other.pid


def compare(r1, r2):
    if r1.x + r1.y != r2.x + r2.y:
        return r1.x + r1.y < r2.x + r2.y
    elif r1.x != r2.x:
        return r1.x < r2.x
    elif r1.y != r2.y:
        return r1.y < r2.y

    return r1.pid < r2.pid


def prepare(elem):
    global n, m, p, id_to_idx, pids, distance, loc, jump_cnt, score, total_score, is_runned

    n, m, p, *others = elem

    id_to_idx = {}

    # pid와 이동 거리 저장 리스트
    pids, distance = [], []

    # 각 토끼의 좌표
    loc = [(1, 1) for _ in range(p)]

    # 토끼의 점프 횟수
    jump_cnt = [0 for _ in range(p)]

    # 각 토끼의 점수, 전체 점수 계산 용이하게 하기 위한 score
    score = [0 for _ in range(p)]
    total_score = 0

    # 토끼가 달렸는지 여부
    is_runned = [0 for _ in range(p)]

    for i in range(p):
        pid, d = others[2 * i : 2 * (i + 1)]

        pids.append(pid)
        distance.append(d)

        id_to_idx[pid] = i

    return


def get_up_rabbit(cur_rabbit, dis):
    up_rabbit = cur_rabbit

    # 한 바퀴 왔다갔다 하는 모션 없앰
    dis %= 2 * (n - 1)

    # 올라가는 모션
    if dis >= up_rabbit.x - 1:
        dis -= up_rabbit.x - 1
        up_rabbit.x = 1
    else:
        up_rabbit.x -= dis
        dis = 0

    # 내려가는 모션
    if dis >= n - up_rabbit.x:
        dis -= up_rabbit.x - 1
        up_rabbit.x = n
    else:
        up_rabbit.x += dis
        dis = 0

    # 끝에서부터 올라오는 모션
    up_rabbit.x -= dis
    dis = 0

    return up_rabbit


def get_down_rabbit(cur_rabbit, dis):
    down_rabbit = cur_rabbit

    # 한 바퀴 왔다갔다 하는 모션 없앰
    dis %= 2 * (n - 1)

    # 내려가는 모션
    if dis >= n - down_rabbit.x:
        dis -= n - down_rabbit.x
        down_rabbit.x = n
    else:
        down_rabbit.x += dis
        dis = 0

    # 올라오는 모션
    if dis >= down_rabbit.x - 1:
        dis -= down_rabbit.x - 1
        down_rabbit.x = 1
    else:
        down_rabbit.x -= dis
        dis = 0

    # 처음에서부터 내려가는 모션
    down_rabbit.x += dis
    dis = 0

    return down_rabbit


def get_left_rabbit(cur_rabbit, dis):
    left_rabbit = cur_rabbit

    # 한 바퀴 왔다갔다 하는 모션 없앰
    dis %= 2 * (m - 1)

    # 왼쪽 가는 모션
    if dis >= left_rabbit.y - 1:
        dis -= left_rabbit.y - 1
        left_rabbit.y = 1
    else:
        left_rabbit.y -= dis
        dis = 0

    # 오른쪽 가는 모션
    if dis >= m - left_rabbit.y:
        dis -= left_rabbit.y - 1
        left_rabbit.y = m
    else:
        left_rabbit.y += dis
        dis = 0

    # 오른쪽 -> 왼쪽 모션
    left_rabbit.y -= dis
    dis = 0

    return left_rabbit


def get_right_rabbit(cur_rabbit, dis):
    right_rabbit = cur_rabbit

    # 한 바퀴 왔다갔다 하는 모션 없앰
    dis %= 2 * (m - 1)

    # 오른쪽 가는 모션
    if dis >= m - right_rabbit.y:
        dis -= m - right_rabbit.y
        right_rabbit.y = m
    else:
        right_rabbit.y += dis
        dis = 0

    # 왼쪽 가는 모션
    if dis >= right_rabbit.y - 1:
        dis -= right_rabbit.y - 1
        right_rabbit.y = 1
    else:
        right_rabbit.y -= dis
        dis = 0

    # 왼쪽 -> 오른쪽 모션
    right_rabbit.y += dis
    dis = 0

    return right_rabbit


def race(elem):
    global total_score

    k, s = elem

    # 달린 여부 초기화
    is_runned = [0 for _ in range(p)]

    # Rabbit 구조체 담을 힙
    rabbit_pq = []

    # 토끼 구조체 형성 : (pid, x, y, j)
    for i in range(p):
        x, y = loc[i]
        new_rabbit = Rabbit(pids[i], x, y, jump_cnt[i])
        heapq.heappush(rabbit_pq, new_rabbit)

    # 경주 진행
    for _ in range(k):
        cur_rabbit = heapq.heappop(rabbit_pq)

        # 상하좌우 이동 후 우선순위 높은 곳으로 이동
        idx = id_to_idx[cur_rabbit.pid]
        d = distance[idx]

        # 저장할 토끼 객체 -> 비교 위해서 좌표 수정
        nxt_rabbit = copy.deepcopy(cur_rabbit)
        nxt_rabbit.x = 0
        nxt_rabbit.y = 0

        # 위로 이동
        up_rabbit = get_up_rabbit(copy.deepcopy(cur_rabbit), d)
        if compare(nxt_rabbit, up_rabbit):
            nxt_rabbit = up_rabbit

        # 아래로 이동
        down_rabbit = get_down_rabbit(copy.deepcopy(cur_rabbit), d)
        if compare(nxt_rabbit, down_rabbit):
            nxt_rabbit = down_rabbit

        # 왼쪽으로 이동
        left_rabbit = get_left_rabbit(copy.deepcopy(cur_rabbit), d)
        if compare(nxt_rabbit, left_rabbit):
            nxt_rabbit = left_rabbit

        # 오른쪽으로 이동
        right_rabbit = get_right_rabbit(copy.deepcopy(cur_rabbit), d)
        if compare(nxt_rabbit, right_rabbit):
            nxt_rabbit = right_rabbit

        # 점프 횟수 추가, 바뀐 토끼 픽스
        nxt_rabbit.j += 1
        heapq.heappush(rabbit_pq, nxt_rabbit)

        # 위치, 점프 카운트 배열도 반영
        idx = id_to_idx[nxt_rabbit.pid]
        loc[idx] = (nxt_rabbit.x, nxt_rabbit.y)
        jump_cnt[idx] = nxt_rabbit.j

        # 달림 표시
        is_runned[idx] = 1

        # 점수 반영
        total_score += nxt_rabbit.x + nxt_rabbit.y
        score[idx] -= nxt_rabbit.x + nxt_rabbit.y

        # print("rabbit_state : ")
        # for i in range(p):
        #     print("i:", i, "//", pids[i], loc[i], jump_cnt[i], "//", distance[i])

        # print("score : ", score)
        # print("total_score : ", total_score)
        # print()

    # 우선순위 높은 토끼에게 점수 s 부여, 한 번이라도 달렸던 토끼여야 함
    # 우선순위 계산 방식이 달라졌으므로, 전체 순회를 해야 함
    new_rabbit = Rabbit(0, 0, 0, 0)
    while rabbit_pq:
        cur_rabbit = heapq.heappop(rabbit_pq)
        idx = id_to_idx[cur_rabbit.pid]

        if not is_runned[idx]:
            continue

        if compare(new_rabbit, cur_rabbit):
            new_rabbit = cur_rabbit

    idx = id_to_idx[new_rabbit.pid]
    score[idx] += s

    return


def change_distance(elem):
    pid, l = elem

    # 이동거리 변경
    idx = id_to_idx[pid]
    distance[idx] *= l

    return


def best_rabbit():
    print(max(score) + total_score)

    return


"""
토끼와 경주

1. 경주 시작 준비
    - P 마리의 토끼, N x M 격자
    - 각 토끼는 고유 번호를 가짐, 한 번 움직일 시 이동해야 하는 거리도 정해져 있음
    - i번 토끼의 고유 번호는 pid_i, 이동해야 하는 거리는 d_i
    - 처음 토끼들은 전부 (1,1)에 위치
    
2. 경주 진행
    - 가장 우선순위가 높은 토끼를 뽑아 멀리 보내주는 것을 K번 반복
    - 우선 순위는 (총 점프 횟수가 적은 > 행+열이 작은 > 행이 작은 > 열이 작은 > 고유번호가 작은) 순서
    
    - 우선순위가 높은 토끼가 i일때, 상하좌우로 d_i만큼 이동 시 위치를 구함
    - 이동 도중 격자를 벗어나면 방향을 반대로 바꿔 이동
    - 4개의 위치 중 (행+열이 큰 > 행이 큰 > 열이 큰) 순서로 우선순위를 두고 높은 곳으로 이동
    - 이 위치가 (r_i, c_i)일 때, i 토끼를 제외한 나머지 토끼들은 (r_i + c_i)만큼 점수 얻음
    
    - K번 동안 이 과정을 반복, 동일한 토끼가 여러번 선택도 가능
    - K번의 턴이 모두 진행된 직후에는 (행+열이 큰 > 행이 큰 > 열이 큰 > 고유번호가 큰) 토끼 순으로 우선순위 계산
    - 가장 우선순위가 높은 토끼에게 점수 S점 추가
    - K 턴 동안 한 번이라도 뽑혔던 적 있는 토끼 중 골라야 함!!!
    
3. 이동거리 변경
    - 고유번호가 pid_i인 토끼의 이동거리를 L배
    - 계산 도중 이동거리가 10억을 넘지 않음

4. 최고의 토끼 선정
    - 각 토끼가 얻은 점수 중 가장 높은 점수 출력
    
우선순위를 뽑아서 계산하는 작업을 반복 -> 우선순위 큐 활용 !!!
토끼 클래스 구현, lt으로 토끼 비교 수행
"""

q = int(sys.stdin.readline())

for _ in range(q):
    ord, *elems = map(int, sys.stdin.readline().split())

    if ord == 100:
        prepare(elems)
    elif ord == 200:
        race(elems)
    elif ord == 300:
        change_distance(elems)
    elif ord == 400:
        best_rabbit()