# -*- coding: utf-8 -*-
import heapq
import sys


def order100(elem):
    global machine, machine_queue, queue, url_set, domain_dict

    n, u0 = elem
    n = int(n)

    # 채점기 채점중인 [시간, 도메인]
    machine = [[]] * (n + 1)

    # 가장 번호 작은 채점기 뽑기 위한 우선순위 큐
    machine_queue = [i for i in range(1, n + 1)]
    heapq.heapify(machine_queue)

    # 채점 대기 큐 : [p, t, u]
    queue = []
    heapq.heappush(queue, [1, 0, u0])

    # 대기큐에 존재하는 url set
    url_set = set()
    url_set.add(u0)

    # 채점중인 domain의 dict(domain : time+3*gap)
    domain_dict = {}

    return


def order200(elem):
    t, p, u = elem
    t, p = map(int, [t, p])

    # 문제 url 일치 확인
    if u in url_set:
        return

    # 대기 큐에 삽입
    url_set.add(u)
    heapq.heappush(queue, [p, t, u])

    return


def order300(t):
    t = int(t)

    # 채점 가능 머신 없는 경우
    if not machine_queue:
        return

    # 채점 불가능한 문제 다시 넣기 위한 리스트
    tmp = []

    # 우선순위 높은 문제를 뽑아서 가능할 때까지 확인
    while queue:
        # 가장 우선순위 높은 문제
        [p0, t0, u0] = heapq.heappop(queue)

        # 문제 도메인
        d = u0.split("/")[0]

        # 채점 불가 조건 : domain 채점중(d:-1), domain 재채점 가능 시간이 아직 안된 경우
        if (d in domain_dict) and (domain_dict[d] == -1 or t < domain_dict[d]):
            tmp.append([t0, p0, u0])
            continue

        # 채점 가능
        else:
            m = heapq.heappop(machine_queue)

            # 대기큐 정보 삭제
            url_set.remove(u0)

            # 채점중 표시
            machine[m] = [t, d]
            domain_dict[d] = -1
            break

    # 채점 못했던 문제들 다시 넣어줌
    for i in tmp:
        heapq.heappush(queue, i)

    return


def order400(elem):
    t, j_id = map(int, elem)

    # 쉬고 있으면 그냥 지나감
    if not machine[j_id]:
        return

    else:
        # 채점 종료
        t0, d0 = machine[j_id]

        machine[j_id] = []
        heapq.heappush(machine_queue, j_id)

        # 도메인 채점 가능 시간 갱신
        domain_dict[d0] = t0 + (t - t0) * 3

    return


def order500(t):
    t = int(t)

    p_answer.append(len(queue))

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

5. 채점 대기 큐 조회
    - 대기 큐에 있는 task 수 출력
    
"""

q = int(sys.stdin.readline())

p_answer = []
_log = []
for _ in range(q):
    ord, *elems = sys.stdin.readline().split()

    if ord == "100":
        order100(elems)
    elif ord == "200":
        order200(elems)
    elif ord == "300":
        order300(elems[0])
    elif ord == "400":
        order400(elems)
    elif ord == "500":
        order500(elems[0])

#     _log.append([ord, elems])
#     _log.append(["queue", copy.deepcopy(queue)])
#     _log.append(["machine", copy.deepcopy(machine)])
#     _log.append(["machine_q", copy.deepcopy(machine_queue)])
#     _log.append(["domain_dict", copy.deepcopy(domain_dict)])
#     _log.append("")

# for i in _log:
#     print(i)

for i in p_answer:
    print(i)