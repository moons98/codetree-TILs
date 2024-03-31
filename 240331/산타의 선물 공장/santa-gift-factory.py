# -*- coding: utf-8 -*-
import sys
from collections import defaultdict


def establish_factory(elems):
    global n, m

    # n개 선물, m개 벨트
    n, m = elems[:2]
    ids, ws = elems[2 : 2 + n], elems[2 + n : 2 + 2 * n]

    # id마다 무게 관리
    for i in range(n):
        weight[ids[i]] = ws[i]

    # 벨트 별로 상자 목록 입력
    size = n // m
    for i in range(m):
        # head, tail 설정 (앞에서부터 size 만큼 벨트에 올려버림)
        head[i] = ids[i * size]
        tail[i] = ids[(i + 1) * size - 1]
        for j in range(i * size, (i + 1) * size):
            # 상자 ID마다 벨트 번호 기입 (해당 belt의 head ~ tail까지)
            belt_num[ids[j]] = i

            # nxt, prv 설정 (head, tail의 경우, 연결되는 노드가 0으로 설정)
            # 연결 리스트라고 해서 노드 하나씩 만드는 개념이 아니라, dict 구조에 다음 id만 놓는 형식
            if j < (i + 1) * size - 1:
                nxt[ids[j]] = ids[j + 1]
                prv[ids[j + 1]] = ids[j]

    return


def remove_id(_id, remove_belt):
    b_num = belt_num[_id]  # 어떤 벨트 위에 올라가있는지

    # 해당 물건을 벨트에서 내림
    if remove_belt:
        belt_num[_id] = -1

    # 하나 남은 원소라면 head, tail 사라짐
    if head[b_num] == tail[b_num]:
        head[b_num] = tail[b_num] = 0

    # head만 삭제라면 head만 변경
    elif _id == head[b_num]:
        n_id = nxt[_id]
        head[b_num] = n_id
        prv[n_id] = 0

    # tail만 삭제
    elif _id == tail[b_num]:
        p_id = prv[_id]
        tail[b_num] = p_id
        nxt[p_id] = 0

    # 중간 id가 삭제되는 경우 nxt, prv만 수선
    else:
        p_id, n_id = prv[_id], nxt[_id]
        nxt[p_id] = n_id
        prv[n_id] = p_id

    # nxt, prv 값 지워줌
    nxt[_id] = prv[_id] = 0

    return


def push_id(target_id, _id):
    nxt[target_id] = _id
    prv[_id] = target_id  # target_id 바로 뒤에 _id 추가

    # target_id가 tail이었다면 tail 변경
    b_num = belt_num[target_id]
    if tail[b_num] == target_id:
        tail[b_num] = _id

    return


def unload_goods(w_max):
    # 각 벨트마다 첫 번째 상자를 확인
    w_sum = 0
    for i in range(m):
        # 망가진 벨트라면 넘어감
        if broken[i]:
            continue

        # 벨트의 head 확인 -> 벨트에 상자 없는 경우 0이 저장되어 있음
        if head[i] != 0:
            _id = head[i]  # 해당 벨트의 가장 앞에 있는 물건 id
            w = weight[_id]  # 물건 weight

            if w <= w_max:
                w_sum += w
                remove_id(_id, True)  # 하차 진행
            elif nxt[_id] != 0:
                remove_id(_id, False)  # 물건이 제거, 벨트에서 내려가지는 않음
                push_id(tail[i], _id)  # 맨 뒤에 push

    print(w_sum)

    return


def remove_goods(r_id):
    # 이미 삭제된 상자면 -1 출력
    if belt_num[r_id] == -1:
        print(-1)
        return

    remove_id(r_id, True)
    print(r_id)

    return


def check_goods(f_id):
    # 이미 삭제된 상자면 -1 출력
    if belt_num[f_id] == -1:
        print(-1)
        return

    # 해당 상자와 위의 상자들을 앞으로 당겨줌, head가 아닐 경우에만 유효
    b_num = belt_num[f_id]
    if head[b_num] != f_id:
        ori_tail = tail[b_num]
        ori_head = head[b_num]

        # tail 갱신
        now_tail = prv[f_id]
        tail[b_num] = now_tail
        nxt[now_tail] = 0

        # 연결 관계 갱신
        nxt[ori_tail] = ori_head
        prv[ori_head] = ori_tail

        # head 갱신
        head[b_num] = f_id
        prv[f_id] = 0

    # 해당 ID 상자의 belt 번호 출력
    print(b_num + 1)

    return


def break_belt(b_num):
    b_num -= 1  # idx화

    if broken[b_num]:
        print(-1)
        return

    # 고장나있지 않은 경우
    broken[b_num] = 1

    # 물건을 오른쪽 정상 벨트로 옮김, 빈 벨트라면 패스
    if head[b_num] == 0:
        print(b_num + 1)
        return

    nxt_num = b_num
    while True:
        nxt_num = (nxt_num + 1) % m
        if not broken[nxt_num]:
            # 해당 벨트가 비어 있으면 그대로 옮김
            if tail[nxt_num] == 0:
                head[nxt_num] = head[b_num]
                tail[nxt_num] = tail[b_num]
            else:
                # head를 tail에 넣어준 뒤, tail만 고치면 됨
                push_id(tail[nxt_num], head[b_num])
                tail[nxt_num] = tail[b_num]

            # head부터 tail까지 belt_num 갱신
            _id = head[b_num]
            while _id != 0:
                belt_num[_id] = nxt_num
                _id = nxt[_id]

            head[b_num] = tail[b_num] = 0
            break

    print(b_num + 1)

    return


"""
### 산타의 선물 공장

순서대로 q개의 명령에 따라 일 진행

1. 공장 설립
    - m개의 벨트 설치, 각 벨트 위에 n/m개의 물건들을 놓아 총 n개의 물건 준비
    - 각 물건에는 고유 번호와 무게가 적힘
    - 번호는 상자마다 다르지만, 무게는 같을 수 있음
    
2. 물건 하차
    - 산타가 원하는 상자의 최대 무게 w_max
    - m번까지 순서대로 벨트를 보며 맨 앞에 있는 선물 중 무게가 w_max 이하면 하차, 아니면 맨 뒤로 보냄
    - 하차된 무게의 총 합인 35 출력
    
3. 물건 제거
    - 제거를 원하는 고유 번호 r_id가 주어짐
    - 해당 고유 번호에 해당하는 상자가 놓인 벨트가 있으면 제거
    - 그러한 상자가 있는 경우 r_id, 없다면 -1 출력
    
4. 물건 확인
    - 산타가 확인을 원하는 고유 번호 f_id가 주어짐
    - 해당 고유 번호에 해당하는 상자가 놓인 벨트가 있으면 벨트의 번호 출력, 없다면 -1 출력
    - 상자가 있는 경우, 해당 상자와 위에 있는 모든 상자를 전부 앞으로 가져옴, 순서 유지
    
5. 벨트 고장
    - 고장이 발생한 벨트 b_num, 고장이 나면 다시는 사용 불가
    - b_num의 오른쪽 벨트부터 순서대로 보며 가장 먼저 만나는 고장나지 않은 벨트 위로 상자를 전부 옮김
    - m번 벨트까지 봤는데도 고장나지 않은 벨트가 없다면 1번부터 확인
    - 하나 이상 정상 상태임을 가정 가능
    - 명령 수행 전 b_num이 이미 망가져 있었으면 -1, 아니면 b_num 출력
"""

# 벨트의 최대 수
MAX_M = 10

# id 별 상자의 무게 관리, dict 구조
weight = {}

# id에 해당하는 상자의 nxt, prv 값 관리 -> 연결 리스트
# 0이면 없다는 의미
prv, nxt = defaultdict(lambda: 0), defaultdict(lambda: 0)  # == defaultdict(int)

# 각 벨트별로 head, tail id 관리
# 0이면 없다는 의미
head = [0] * MAX_M
tail = [0] * MAX_M

# 벨트가 망가졌는지 표시
broken = [False] * MAX_M

# 물건 별로 벨트 번호를 기입
# 벨트 번호가 -1이면 사라진 것
belt_num = defaultdict(lambda: -1)


## ---
q = int(sys.stdin.readline())

for _ in range(q):
    tmp = list(map(int, sys.stdin.readline().split()))
    q_type = tmp[0]

    if q_type == 100:
        establish_factory(tmp[1:])
    elif q_type == 200:
        unload_goods(tmp[1])
    elif q_type == 300:
        remove_goods(tmp[1])
    elif q_type == 400:
        check_goods(tmp[1])
    elif q_type == 500:
        break_belt(tmp[1])