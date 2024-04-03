# -*- coding: utf-8 -*-
import heapq
import sys


def order100(elems):
    global machine, machine_queue, queue, domain_checker

    n, u0 = elems

    machine = [[]] * (n + 1)
    machine_queue = [i for i in range(1, n + 1)]
    heapq.heapify(machine_queue)

    queue = []
    heapq.heappush(queue, [1, 0, u0])

    domain_checker = {}

    return


def order200(elems):
    t, p, u = elems

    # url 기준으로 같으면 넣지 않음
    for _, _, url in queue:
        if url == u:
            return

    heapq.heappush(queue, [p, t, u])

    return


def order300(elems):
    t = elems[0]

    # 쉬고 있는 기계가 있는지 확인
    if not machine_queue:
        return

    # 만약 뽑은 애가 우선순위가 아닌 경우
    tmp = []
    while True:
        if not queue:
            break

        p, t0, u = heapq.heappop(queue)
        d = u.split("/")[0]

        if d in domain_checker.keys() and (
            domain_checker[d] == -1 or domain_checker[d] > t
        ):
            tmp.append([p, t0, d])
        # task 배정
        else:
            # -1은 채점중
            domain_checker[d] = -1

            num = heapq.heappop(machine_queue)
            machine[num] = [d, t]
            break

    # 우선 순위 아니었던 애들 다시 넣어줌
    for i in tmp:
        heapq.heappush(queue, i)

    return


def order400(elems):
    t, j_id = elems

    if machine[j_id] != []:
        # 도메인 체크
        d, t0 = machine[j_id]
        if d in domain_checker.keys():
            domain_checker[d] = max(domain_checker[d], t0 + 3 * (t - t0))
        else:
            domain_checker[d] = t0 + 3 * (t - t0)

        # 채점기 종료 처리
        machine[j_id] = []
        heapq.heappush(machine_queue, j_id)

    return


def order500(elems):
    print(len(queue))

    return


"""
1. 채점기 준비
    - N개의 채점기, 초기 url에 해당하는 u0
    - url은 도메인/문제ID 형태
    - 도메일 : 알파벳 소문자와 . 으로만 구성
    - ID : 1이상 1억 이하 정수값으로 구성
    - 채점기에는 1~N번 번호 존재
    - 0초에 우선순위가 1이면서 url이 u0인 문제에 대한 채점 요청
    
2. 채점 요청
    - t초, 우선순위 p, url이 u인 문제에 대한 채점 요청이 들어옴
    - 채점 대기 큐에 있는 task 중 u와 일치하는 url이 있으면 큐에 추가하지 않음

3. 채점 시도
    - t초에 채점 대기 큐에서 즉시 채점 불가한 경우 제외, 우선순위가 가장 높은 task를 채점 진행
    - 쉬고 있는 채점기가 없으면 넘어감, 있으면 작은 번호부터 할당
    - 즉시 채점 불가한 경우
        - 해당 task의 도메인이 현재 채점 진행중
        - 도메인에 대해 최근 채점 시작이 start, 종료가 start + gap, 현재 시간 t < start + 3 * gap
    - 우선순위
        - 우선순위 p의 번호가 작을수록
        - 채점 대기 큐에 들어온 시간이 빠를수록 
    
4. 채점 종료
    - J_id번이 진행중인 채점이 종료, 채점중 아니었으면 무시

4. 채점 대기 큐 조회
    - 대기 큐에 있는 task 수 출력
    
"""

q = int(sys.stdin.readline())
answer = []

for _ in range(q):
    order, *elem = list(sys.stdin.readline().split())

    order = int(order)
    if order == 100 or order == 200:
        elem = list(map(int, elem[:-1])) + [elem[-1]]
    else:
        elem = list(map(int, elem))

    if order == 100:
        order100(elem)
    elif order == 200:
        order200(elem)
    elif order == 300:
        order300(elem)
    elif order == 400:
        order400(elem)
    elif order == 500:
        order500(elem)

    # print()
    # print(order, elem)
    # print("queue : ", queue)
    # print("domain_checker : ", domain_checker)