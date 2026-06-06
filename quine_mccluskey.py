# quine_mccluskey.py
# Quine-McCluskey 算法（Q-M 简化法）
# 用于布尔函数的最小化，是卡诺图的系统化方法
# 输入：变量数、最小项列表、无关项列表
# 输出：最简与或表达式（SOP）

from itertools import combinations


def to_binary(num, n):
    """将数字转换为 n 位二进制字符串"""
    return format(num, f'0{n}b')


def count_ones(binary_str):
    """计算二进制字符串中 1 的个数"""
    return binary_str.count('1')


def can_merge(term1, term2):
    """判断两个项是否可以合并（仅有一位不同）"""
    diff = 0
    for i in range(len(term1)):
        if term1[i] != term2[i]:
            diff += 1
            if diff > 1:
                return False
    return diff == 1


def merge_terms(term1, term2):
    """合并两个项，不同位用 '-' 表示"""
    result = []
    for i in range(len(term1)):
        if term1[i] == term2[i]:
            result.append(term1[i])
        else:
            result.append('-')
    return ''.join(result)


def get_decimal_set(term):
    """获取一个项覆盖的十进制数集合"""
    positions = [i for i, c in enumerate(term) if c == '-']
    if not positions:
        return {int(term, 2)}

    result = set()
    base = list(term)
    # 对所有 '-' 位置进行展开
    for combo in combinations(positions):
        for pos in positions:
            base[pos] = '0'
        result.add(int(''.join(base), 2))
        for pos in positions:
            base[pos] = '1'
        result.add(int(''.join(base), 2))

    # 更准确的方法
    result = set()
    n = len(term)
    dash_positions = [i for i in range(n) if term[i] == '-']

    for mask in range(2 ** len(dash_positions)):
        bits = list(term)
        for j, pos in enumerate(dash_positions):
            bits[pos] = '1' if (mask >> j) & 1 else '0'
        result.add(int(''.join(bits), 2))

    return result


def qm_step1(min_terms, dont_cares, n):
    """
    第一步：按 1 的个数分组
    返回初始分组
    """
    all_terms = sorted(set(min_terms + dont_cares))
    groups = {}

    for term in all_terms:
        binary = to_binary(term, n)
        ones = count_ones(binary)
        if ones not in groups:
            groups[ones] = []
        groups[ones].append({
            'binary': binary,
            'minterms': {term},
            'used': False
        })

    return groups


def qm_step2(groups, n):
    """
    第二步：迭代合并
    返回：(prime_implicants, merged_groups)
    """
    prime_implicants = []
    current_groups = groups

    while True:
        new_groups = {}
        used = set()

        # 按相邻组进行合并
        sorted_keys = sorted(current_groups.keys())
        for i in range(len(sorted_keys) - 1):
            k1, k2 = sorted_keys[i], sorted_keys[i + 1]
            if k2 - k1 != 1:
                continue

            for t1 in current_groups[k1]:
                for t2 in current_groups[k2]:
                    if can_merge(t1['binary'], t2['binary']):
                        merged = merge_terms(t1['binary'], t2['binary'])
                        ones = count_ones(merged)
                        if ones not in new_groups:
                            new_groups[ones] = []

                        new_term = {
                            'binary': merged,
                            'minterms': t1['minterms'] | t2['minterms'],
                            'used': False
                        }

                        # 避免重复
                        if not any(e['binary'] == merged for e in new_groups[ones]):
                            new_groups[ones].append(new_term)

                        t1['used'] = True
                        t2['used'] = True

        # 收集未被合并的项（质蕴涵项）
        for key in current_groups:
            for term in current_groups[key]:
                if not term['used']:
                    prime_implicants.append(term)

        # 如果没有新的合并，结束
        if not new_groups:
            break

        current_groups = new_groups

    return prime_implicants


def build_prime_implicant_table(prime_implicants, min_terms):
    """
    第三步：构建质蕴涵项覆盖表
    """
    table = {}
    for pi in prime_implicants:
        key = pi['binary']
        table[key] = {
            'covers': pi['minterms'] & set(min_terms),
            'binary': pi['binary']
        }
    return table


def find_essential_prime_implicants(table, min_terms):
    """
    第四步：寻找本质质蕴涵项
    """
    essential = []
    covered = set()

    # 对每个最小项，检查是否只有一个质蕴涵项覆盖
    for mt in min_terms:
        covering = [key for key, val in table.items() if mt in val['covers']]
        if len(covering) == 1:
            pi_key = covering[0]
            if pi_key not in [e[0] for e in essential]:
                essential.append((pi_key, table[pi_key]))
                covered |= table[pi_key]['covers']

    return essential, covered


def find_minimum_cover(table, min_terms, essential, covered):
    """
    第五步：用贪心法覆盖剩余最小项
    """
    remaining = set(min_terms) - covered
    result = list(essential)

    while remaining:
        # 选择覆盖最多剩余最小项的质蕴涵项
        best = None
        best_cover = set()

        for key, val in table.items():
            if any(key == r[0] for r in result):
                continue
            covers = val['covers'] & remaining
            if len(covers) > len(best_cover):
                best = key
                best_cover = covers

        if best is None:
            break

        result.append((best, table[best]))
        remaining -= best_cover

    return result


def format_term(binary, var_names=None):
    """将二进制项转换为变量表达式"""
    n = len(binary)
    if var_names is None:
        var_names = [chr(65 + i) for i in range(n)]  # A, B, C, ...

    terms = []
    for i, c in enumerate(binary):
        if c == '1':
            terms.append(var_names[i])
        elif c == '0':
            terms.append(var_names[i] + "'")

    return ''.join(terms) if terms else '1'


def solve_qm(min_terms, dont_cares=None, n=None, var_names=None):
    """
    Q-M 算法主函数
    min_terms: 最小项列表
    dont_cares: 无关项列表
    n: 变量数（自动推断）
    var_names: 变量名列表
    """
    if dont_cares is None:
        dont_cares = []

    # 自动推断变量数
    if n is None:
        max_val = max(min_terms + dont_cares) if (min_terms + dont_cares) else 0
        n = max_val.bit_length()

    if var_names is None:
        var_names = [chr(65 + i) for i in range(n)]

    print(f"变量数：{n}")
    print(f"变量名：{', '.join(var_names)}")
    print(f"最小项：{sorted(min_terms)}")
    print(f"无关项：{sorted(dont_cares)}")
    print()

    # 第一步：分组
    groups = qm_step1(min_terms, dont_cares, n)
    print("【第一步】按 1 的个数分组：")
    for key in sorted(groups.keys()):
        print(f"  {key} 个 1：", end="")
        for t in groups[key]:
            print(f" {t['binary']}({','.join(map(str, sorted(t['minterms'])))})", end="")
        print()
    print()

    # 第二步：迭代合并
    prime_implicants = qm_step2(groups, n)
    print("【第二步】质蕴涵项：")
    for pi in prime_implicants:
        print(f"  {pi['binary']}  覆盖: {sorted(pi['minterms'])}")
    print()

    # 第三步：构建覆盖表
    table = build_prime_implicant_table(prime_implicants, min_terms)

    # 第四步：寻找本质质蕴涵项
    essential, covered = find_essential_prime_implicants(table, min_terms)
    print("【第三步】本质质蕴涵项：")
    for key, val in essential:
        print(f"  {key} ({format_term(key, var_names)})  覆盖: {sorted(val['covers'])}")
    print()

    # 第五步：覆盖剩余
    result = find_minimum_cover(table, min_terms, essential, covered)

    # 输出最终结果
    print("【第四步】最简与或表达式：")
    terms = [format_term(key, var_names) for key, val in result]
    print(f"  F = {' + '.join(terms)}")
    print()

    # 验证
    print("验证：")
    all_covered = set()
    for key, val in result:
        all_covered |= val['covers']
    if all_covered >= set(min_terms):
        print("  [OK] 所有最小项已被覆盖")
    else:
        print(f"  [FAIL] 未覆盖的最小项：{set(min_terms) - all_covered}")

    return result, var_names


def main():
    print("=" * 50)
    print("  Quine-McCluskey 算法（Q-M 简化法）")
    print("=" * 50)
    print()

    # 输入变量数
    n = int(input("请输入变量数 n："))
    var_names = [chr(65 + i) for i in range(n)]

    # 输入最小项
    min_input = input("请输入最小项（用逗号分隔，如 0,1,2,5,6,7）：")
    min_terms = [int(x.strip()) for x in min_input.split(',')]

    # 输入无关项（可选）
    dc_input = input("请输入无关项（用逗号分隔，无则直接回车）：").strip()
    dont_cares = [int(x.strip()) for x in dc_input.split(',')] if dc_input else []

    print()
    print("=" * 50)
    solve_qm(min_terms, dont_cares, n, var_names)


if __name__ == "__main__":
    main()
