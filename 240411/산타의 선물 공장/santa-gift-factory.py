# -*- coding: utf-8 -*-
import sys
from collections import defaultdict


def build(elem):
    global n, m, num, id_to_weight, id_to_belt, is_broken, prv, nxt, head, tail

    n, m = elem[0], elem[1]
    num = n // m
    ids, weights = elem[2 : 2 + n], elem[2 + n :]

    # id : weight, id : belt
    id_to_weight = defaultdict(lambda: 0)
    id_to_belt = defaultdict(lambda: 0)

    is_broken = [True] + [False for _ in range(m)]

    # 각 id의 prv, nxt node id
    prv = defaultdict(lambda: 0)
    nxt = defaultdict(lambda: 0)

    # 각 belt의 [head, tail] id
    head = [0 for _ in range(m + 1)]
    tail = [0 for _ in range(m + 1)]

    for id, weight in zip(ids, weights):
        id_to_weight[id] = weight

    for b in range(1, m + 1):
        id = ids[(b - 1) * num : b * num]

        head[b] = id[0]
        tail[b] = id[-1]

        for i in range(num):
            id_to_belt[id[i]] = b

            if i < num - 1:
                prv[id[i + 1]] = id[i]
                nxt[id[i]] = id[i + 1]

    return


def remove_action(_id, opt):
    b = id_to_belt[_id]

    # opt = True -> 벨트에서 물건 내리는 경우
    if opt:
        id_to_belt[_id] = 0

    # head == tail -> 벨트 전체 정보 0
    if head[b] == tail[b]:
        head[b] = tail[b] = 0

    # head를 내리는 경우
    elif head[b] == _id:
        n_id = nxt[_id]
        head[b] = n_id
        prv[n_id] = 0

    # tail을 내리는 경우
    elif tail[b] == _id:
        p_id = prv[_id]
        tail[b] = p_id
        nxt[p_id] = 0

    # 중간 id가 삭제되는 경우 -> prv, nxt만 연결
    else:
        p_id = prv[_id]
        n_id = nxt[_id]

        nxt[p_id] = n_id
        prv[n_id] = p_id

    # _id의 nxt, prv 지워줌
    prv[_id] = nxt[_id] = 0

    return


def push_id(t_id, _id):
    # t_id의 뒤에 _id를 붙임
    nxt[t_id] = _id
    prv[_id] = t_id

    # tail일 경우, 갱신 필요
    b = id_to_belt[_id]
    if tail[b] == t_id:
        tail[b] = _id

    return


def unload_obj(w_max):
    answer = 0

    # belt의 head를 바라봐야 함
    for b in range(1, m + 1):
        # 고장난 벨트인지 확인
        if is_broken[b]:
            continue

        # 비어 있는 벨트인지 확인 -> 비어있으면 0
        if not head[b]:
            continue

        _id = head[b]
        weight = id_to_weight[_id]

        # 하차하는 경우
        if weight <= w_max:
            answer += weight
            remove_action(_id, True)

        # 맨 뒤로 보내는 경우 -> _id가 tail이면 그냥 두면 됨
        elif tail[b] != _id:
            remove_action(_id, False)
            push_id(tail[b], _id)

    p_answer.append(answer)

    return


def remove_obj(r_id):
    # 이미 내려간 물건
    if not id_to_belt[r_id]:
        p_answer.append(-1)
    else:
        remove_action(r_id, True)
        p_answer.append(r_id)

    return


def check_obj(f_id):
    # 이미 내려간 물건
    if not id_to_belt[f_id]:
        p_answer.append(-1)
        return

    # head가 아닐 경우에만 유효, 연결 정보만 갱신
    b = id_to_belt[f_id]
    if head[b] != f_id:
        ori_head = head[b]
        ori_tail = tail[b]

        new_tail = prv[f_id]

        head[b] = f_id
        tail[b] = new_tail

        prv[f_id] = 0
        nxt[ori_tail] = ori_head

        prv[ori_head] = ori_tail
        nxt[new_tail] = 0

    p_answer.append(b)

    return


def broken_belt(b_num):
    if is_broken[b_num]:
        p_answer.append(-1)
        return

    # 고장내기
    is_broken[b_num] = 1

    # 고장난 벨트가 빈 벨트면 그냥 패스
    if head[b_num] == 0:
        p_answer.append(b_num)
        return

    # 망가지지 않은 벨트 찾기
    nxt_num = b_num
    while True:
        nxt_num = (nxt_num + 1) % (m + 1)
        if not is_broken[nxt_num]:
            # 비어 있는 벨트에 넣는 경우
            if tail[nxt_num] == 0:
                head[nxt_num] = head[b_num]
                tail[nxt_num] = tail[b_num]
            else:
                # head을 넣어준 뒤, tail 정보만 수정
                push_id(tail[nxt_num], head[b_num])
                tail[nxt_num] = tail[b_num]

            # head부터 tail까지 belt 정보 수정
            _id = head[b_num]
            while _id:
                id_to_belt[_id] = nxt_num
                _id = nxt[_id]

            head[b_num] = tail[b_num] = 0
            break

    p_answer.append(b_num)

    return


def print_state():
    tmp_belt = [[] for _ in range(m + 1)]
    for idx, b in enumerate(head):
        tmp_belt[idx].append(b)

    for idx in range(1, m + 1):
        c_id = tmp_belt[idx][0]
        while True:
            n_id = nxt[c_id]

            if n_id:
                tmp_belt[idx].append(n_id)
                c_id = n_id
            else:
                break
    print()
    for i in tmp_belt[1:]:
        print(i)
    print("///")

    return


"""
산타와 선물 공장

1. 공장 설립
    - m개 벨트, n/m개씩 각 벨트에 배치, 총 n개 물건
    - 물건에는 ID, W 존재

2. 물건 하차
    - 원하는 최대 무게 w_max
    - 1~m번 벨트를 보며 맨 앞에 있는 선물 중 w_max 이하 무게의 선물을 하차, 아니면 맨 뒤로
    - 하차된 상자 무게의 총 합 출력

3. 물건 제거
    - 제거를 원하는 고유 번호 r_id
    - 해당 상자가 놓인 벨트에서 상자 제거
    - 있으면 r_id, 없으면 -1 출력

4. 물건 확인
    - f_id가 놓인 벨트에서, 해당 상자 포함 뒤에 있는 상자들을 전부 맨 앞으로 가져옴
    - 있으면 해당 벨트 번호, 없으면 -1 출력

5. 벨트 고장
    - b_num 벨트가 고장
    - 해당 벨트의 오른쪽부터 하나씩 보면서 고장나지 않은 벨트를 찾고, 그 벨트로 상자 전부 옮김
    - 고장 처리 시 b_num, 이미 고장난 경우 -1 출력

시작 노드의 prev_id와 끝 노드의 next_id만 잘 처리해주면 됨
"""

q = int(sys.stdin.readline())

p_answer = []
for _ in range(q):
    ord, *elems = map(int, sys.stdin.readline().split())

    if ord == 100:
        build(elems)
    elif ord == 200:
        unload_obj(elems[0])
    elif ord == 300:
        remove_obj(elems[0])
    elif ord == 400:
        check_obj(elems[0])
    elif ord == 500:
        broken_belt(elems[0])

for i in p_answer:
    print(i)