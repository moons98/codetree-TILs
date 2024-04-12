# -*- coding: utf-8 -*-
import sys

MAX_N = 100001
MAX_D = 22


def init(elems):
    global a, p, nx, val, noti

    # 0 ~ N번까지 노드 존재, max depth = 20
    # 채팅의 권한 정보(a), 부모 채팅(p) -> 0번 채팅은 해당 사항 없음
    p, a = [0] + elems[:n], [0] + elems[n:]

    # 권한이 20을 초과하는 경우, 20으로 제한
    for i in range(n + 1):
        if a[i] > 20:
            a[i] = 20

    # nx(해당 노드가 전달할 수 있는 알림 수), val(총 알림 수) 초기화
    nx = [[0 for _ in range(MAX_D)] for _ in range(n + 1)]
    val = [0] * (n + 1)

    # noti : 알림망 꺼진 상태 1, 켜진 상태 0
    noti = [0 for _ in range(n + 1)]

    for i in range(1, n + 1):
        cur_node = i
        x = a[i]
        nx[cur_node][x] += 1

        # 부모 채팅으로 이동하며 nx, val 갱신
        while p[cur_node] and x:
            cur_node = p[cur_node]
            x -= 1
            if x:
                nx[cur_node][x] += 1
            val[cur_node] += 1

    return


def setting(c):
    cur_p = p[c]
    num = 1  # 부모 노드로 타고 올라간 횟수, 이것보다 amp가 커야 전해짐

    # 상위 채팅으로 이동하며 noti 값에 따라 nx, val 갱신
    while cur_p:
        for i in range(num, 22):
            # 현재 꺼짐
            if noti[c]:
                val[cur_p] += nx[c][i]
            else:
                val[cur_p] -= nx[c][i]

            # 타고 올라간 횟수(num)보다 amp가 커서 전달됐던 애들을 내려줌
            if i > num:
                if noti[c]:
                    nx[cur_p][i - num] += nx[c][i]
                else:
                    nx[cur_p][i - num] -= nx[c][i]

        # 부모가 꺼져 있는 경우
        if noti[cur_p]:
            break

        cur_p = p[cur_p]
        num += 1

    # 알림망 설정 토글
    noti[c] = not noti[c]

    return


def change_power(elem):
    c, power = elem

    bef_power = a[c]
    power = min(power, 20)
    a[c] = power

    # 기존 power의 영향을 다 줄여줌
    nx[c][bef_power] -= 1

    # 노드가 켜져서 위쪽 영향이 가는 경우
    if not noti[c]:
        cur_p = p[c]
        num = 1

        while cur_p:
            if bef_power >= num:
                val[cur_p] -= 1  # 기존 영향을 삭제하는 액션

            if bef_power > num:
                nx[cur_p][bef_power - num] -= 1

            if noti[cur_p]:
                break

            cur_p = p[cur_p]
            num += 1

    # 새로운 power의 영향을 더해줌
    nx[c][power] += 1

    if not noti[c]:
        cur_p = p[c]
        num = 1

        while cur_p:
            if power >= num:
                val[cur_p] += 1

            # 같은 경우는 amp=0에 찍히므로 위로 올라갈 채팅은 아님
            if power > num:
                nx[cur_p][power - num] += 1

            if noti[cur_p]:
                break

            cur_p = p[cur_p]
            num += 1

    return


def change_parents(elem):
    c1, c2 = elem

    bef_noti1 = noti[c1]
    bef_noti2 = noti[c2]

    # 켜져 있는 노드를 다 꺼서 영향 없애고 바꾼 뒤에 다시 켬
    if not noti[c1]:
        setting(c1)
    if not noti[c2]:
        setting(c2)

    p[c1], p[c2] = p[c2], p[c1]

    # 원래 켜져 있던 노드는 다시 켜줌
    if not bef_noti1:
        setting(c1)
    if not bef_noti2:
        setting(c2)

    return


def get_info(c):
    p_answer.append(val[c])

    return


"""
코드트리 메신저

1. 사내 메신저 준비
    - 0 ~ N번까지 N+1개 채팅방
    - 각 채팅방의 부모 채팅방 번호 : parents
    - 각 채팅방은 권한 authority를 가짐
    - 0번 채팅방은 parent, authority와 무관
    
2. 알림망 설정
    - 처음 모든 채팅방의 설정은 켜져 있음
    - c번 채팅방의 알림망 설정이 on->off or off->on
    - off 상태면 자기 자신을 포함하여 아래에서 올라온 알림을 올려보내지 않음

3. 권한 세기 변경
    - c번 채팅방의 권한 세기를 power로 변경

4. 부모 채팅방 교환
    - c1번 채팅방과 c2번 채팅방의 부모를 바꿈
    - 두 채팅방은 같은 depth에 존재, 아래 자식들도 다 달고 바뀜
    
5. 알림을 받을 수 있는 채팅방 수 조회
    - c번 채팅방까지 알림이 도달할 수 있는 서로 다른 채팅방의 수 출력
"""

n, q = map(int, sys.stdin.readline().split())

p_answer = []
for _ in range(q):
    ord, *elems = map(int, sys.stdin.readline().split())

    if ord == 100:
        init(elems)
    elif ord == 200:
        setting(elems[0])
    elif ord == 300:
        change_power(elems)
    elif ord == 400:
        change_parents(elems)
    elif ord == 500:
        get_info(elems[0])

for i in p_answer:
    print(i)