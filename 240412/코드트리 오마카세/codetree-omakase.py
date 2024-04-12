# -*- coding: utf-8 -*-
import sys


class Query:
    def __init__(self, cmd, t, x, name, n):
        self.cmd = cmd
        self.t = t
        self.x = x
        self.name = name
        self.n = n


"""
코드트리 오마카세

원형 형태의 초밥 벨트, L개 의자, 시계 방향으로 idx 증가
초밥 벨트는 1초에 한 칸씩 시계 방향으로 회전

1. 주방장의 초밥 만들기
    - t 시각에 x 앞에 있는 벨트 위에 name을 부착한 초밥 올려놓음
    - 회전이 일어난 직후에 발생
    - 같은 위치에 여러 회전 초밥이 올라갈 수 있음
    
2. 손님 입장
    - 이름이 name인 사람이 t 시각, x 위치에 앉음
    - 회전이 일어난 직후에 발생
    - 이때부터 위치 x로 오는 초밥 중, 자신의 이름이 적힌 초밥 n개를 먹고 떠남
    - 착석 즉시 먹기 시작, 동시에 여러 개 먹을 수 있음

3. 사진 촬영
    - 시각 t에 사진 촬영
    - 초밥 회전 -> 초밥 먹기 -> 사진 촬영 순서
    - 사진 촬영 시 남아 있는 사람 수와 초밥 수 출력
"""

l, q = map(int, sys.stdin.readline().split())

# 명령 관리
queries = []

# 등장한 사람 목록
names = set()

# 각 사람마다 해당되는 초밥 명령
p_queries = {}

# 입장 시간
enter_time = {}

# 손님 위치
position = {}

# 퇴장 시간
exit_time = {}


for _ in range(q):
    cmd, *elems = sys.stdin.readline().split()
    cmd = int(cmd)

    t, x, n = -1, -1, -1
    name = ""

    if cmd == 100:
        t, x, name = elems
        t, x = map(int, [t, x])
    elif cmd == 200:
        t, x, name, n = elems
        t, x, n = map(int, [t, x, n])
    elif cmd == 300:
        t = int(elems[0])

    queries.append(Query(cmd, t, x, name, n))

    # 사람별 주어진 초밥 목록 관리
    if cmd == 100:
        if name not in p_queries:
            p_queries[name] = []

        p_queries[name].append(Query(cmd, t, x, name, n))

    # 입장 시간과 위치 관리
    elif cmd == 200:
        names.add(name)
        enter_time[name] = t
        position[name] = x


# 각 사람마다 초밥 먹는 action이 언제인지 계산해서 추가, cmd == 111
for name in names:
    # 퇴장 시간 관리 -> 마지막으로 먹는 초밥 시간
    exit_time[name] = 0

    for q in p_queries[name]:
        # 초밥이 사람 등장 이전에 주어진 상황
        time_to_removed = 0
        if q.t < enter_time[name]:
            # enter_time 때의 스시 위치를 구함
            t_sushi_x = (q.x + (enter_time[name] - q.t)) % l

            # 만나기까지 걸리는 시간
            time_left = (position[name] - t_sushi_x + l) % l

            # 스시가 최종적으로 사라지는 시간 (절대 시간)
            time_to_removed = enter_time[name] + time_left

        # 입장 이후에 만들어짐
        else:
            time_left = (position[name] - q.x + l) % l
            # 만들어진 시간 기점으로 계산해야 함
            time_to_removed = q.t + time_left

        # 초밥이 사라지는 시간 중 가장 늦은 시간
        exit_time[name] = max(exit_time[name], time_to_removed)

        # 초밥이 사라지는 111번 쿼리 추가
        queries.append(Query(111, time_to_removed, -1, name, -1))


# 떠난 시간에 해당하는 쿼리 추가 (222)
for name in names:
    queries.append(Query(222, exit_time[name], -1, name, -1))

# query 정렬, t >> cmd
# 순서대로 보면서 사람, 초밥 수를 cnt, cmd==300이면 출력
queries.sort(key=lambda q: (q.t, q.cmd))

num_people, num_sushi = 0, 0
for idx, q in enumerate(queries):
    # 스시 추가
    if q.cmd == 100:
        num_sushi += 1
    # 스시 삭제
    elif q.cmd == 111:
        num_sushi -= 1
    # 사람 추가
    elif q.cmd == 200:
        num_people += 1
    # 사람 퇴장
    elif q.cmd == 222:
        num_people -= 1
    # 출력
    elif q.cmd == 300:
        print(num_people, num_sushi)