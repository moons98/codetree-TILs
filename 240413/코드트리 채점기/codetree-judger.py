# -*- coding: utf-8 -*-
import heapq
import sys

MAX_INT = sys.maxsize


def order100(elem):
    global machine, machine_queue, queue, url_set, domain_dict

    n, u0 = elem
    n = int(n)

    # 채점기 채점중인 [시간, 도메인]
    machine = [[]] * (n + 1)

    # 가장 번호 작은 채점기 뽑기 위한 우선순위 큐
    machine_queue = [i for i in range(1, n + 1)]
    heapq.heapify(machine_queue)

    # 채점 대기 큐 : {d0 : [[p, t, u] ...], ...}
    queue = {}

    # 도메인 없으면 만들어주기
    d0 = u0.split("/")[0]
    if d0 not in queue:
        queue[d0] = []

    # 해당 도메인 우선순위 큐에 저장
    heapq.heappush(queue[d0], [1, 0, u0])

    # 대기큐에 존재하는 url set
    url_set = set()
    url_set.add(u0)

    # 도메인을
    # 채점중인 domain의 dict(domain : time+3*gap)
    domain_dict = {}

    return


def order200(elem):
    t, p, u = elem
    t, p = map(int, [t, p])

    # 문제 url 일치 확인
    if u in url_set:
        return

    # 도메인 이미 있는지 확인
    d = u.split("/")[0]
    if d not in queue:
        queue[d] = []

    # 대기 큐에 삽입
    url_set.add(u)
    heapq.heappush(queue[d], [p, t, u])

    return


def compare(a, b):
    if a[0] != b[0]:
        return a[0] < b[0]
    elif a[1] != b[1]:
        return a[1] < b[1]

    return


def order300(t):
    t = int(t)

    # 채점 가능 머신 없는 경우
    if not machine_queue:
        return

    # 채점 가능한 도메인 중 우선순위 가장 높은 문제 찾기 (p 작을수록 >> t 작을수록)
    problem0, d0 = [MAX_INT, MAX_INT, ""], ""
    for d in queue:
        # domain이 채점중 or 시간 안됨
        if (d in domain_dict) and (domain_dict[d] == -1 or t < domain_dict[d]):
            continue

        # domain에 해당하는 채점 가능한 문제가 없음
        if not queue[d]:
            continue

        # 각 도메인의 가장 우선순위 높은 문제 정보 비교
        problem1 = queue[d][0]
        if not compare(problem0, problem1):
            problem0 = problem1
            d0 = d

    # 채점 진행
    if d0:
        # 우선순위 가장 높은 문제 pop
        [_, _, u0] = heapq.heappop(queue[d0])

        # machine 뽑기
        m = heapq.heappop(machine_queue)

        # 대기큐 정보 삭제
        url_set.remove(u0)

        # 채점중 표시
        machine[m] = [t, d0]
        domain_dict[d0] = -1

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
    num = 0
    for d in queue:
        num += len(queue[d])

    p_answer.append(num)

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
    
    
실패 분석 :
    - 의미없는 pop, push 과정이 많았음
    - 도메인이 같거나 현재 시간에 이용 불가능하면 그 도메인은 통째로 날려야 함
    - 즉, 우선순위 큐를 도메인 별로 운영해야 함 [p, t, u]
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