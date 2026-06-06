# knight_tour.py
# 骑士巡游问题（Knight's Tour）
# 在 n×n 的棋盘上，马从某个起点出发，按"日"字规则不重复地走遍所有格子
# 算法：Warnsdorff 启发式 + 回溯法
# 支持 n <= 64 的棋盘大小

import sys
import time

# 马的 8 个可能移动方向
MOVES = [
    (-2, -1), (-2, 1), (-1, -2), (-1, 2),
    (1, -2), (1, 2), (2, -1), (2, 1)
]


def is_valid(x, y, n, board):
    """检查位置 (x, y) 是否合法且未被访问"""
    return 0 <= x < n and 0 <= y < n and board[x][y] == -1


def get_degree(x, y, n, board):
    """计算位置 (x, y) 的可达度（未访问的邻居数）"""
    count = 0
    for dx, dy in MOVES:
        nx, ny = x + dx, y + dy
        if is_valid(nx, ny, n, board):
            count += 1
    return count


def warnsdorff_solve(n, start_x=0, start_y=0):
    """
    Warnsdorff 启发式算法求解骑士巡游
    每次选择可达度最小的下一跳（贪心策略）
    如果失败则回溯
    """
    board = [[-1] * n for _ in range(n)]
    path = [(start_x, start_y)]
    board[start_x][start_y] = 0

    total = n * n

    def solve(pos, step):
        if step == total:
            return True

        x, y = pos
        # 获取所有合法的下一跳，并按可达度排序
        neighbors = []
        for dx, dy in MOVES:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny, n, board):
                degree = get_degree(nx, ny, n, board)
                neighbors.append((degree, nx, ny))

        # 按可达度升序排序（Warnsdorff 规则）
        neighbors.sort()

        for _, nx, ny in neighbors:
            board[nx][ny] = step
            path.append((nx, ny))

            if solve((nx, ny), step + 1):
                return True

            # 回溯
            board[nx][ny] = -1
            path.pop()

        return False

    if solve((start_x, start_y), 1):
        return board, path
    else:
        return None, None


def print_board(board, n):
    """打印棋盘"""
    if board is None:
        print("无解！")
        return

    # 计算最大数字的宽度
    width = len(str(n * n - 1))

    print("+" + ("---" + "-" * width) * n + "+")
    for row in board:
        line = "|"
        for val in row:
            line += f" {val:>{width}} |"
        print(line)
        print("+" + ("---" + "-" * width) * n + "+")


def print_path(path, n):
    """打印路径坐标"""
    print("\n路径顺序：")
    for i, (x, y) in enumerate(path):
        if i % 10 == 0:
            print()
        print(f"  {i+1:>3}. ({x},{y})", end="")
    print()


def main():
    print("=" * 50)
    print("  骑士巡游问题（Knight's Tour）")
    print("  算法：Warnsdorff 启发式 + 回溯法")
    print("=" * 50)

    # 输入棋盘大小
    n = int(input("\n请输入棋盘大小 n（n <= 64）："))
    if n < 1 or n > 64:
        print("错误：n 必须在 1 到 64 之间！")
        return

    # 输入起点
    start_input = input(f"请输入起点坐标（格式：x y，范围 0-{n-1}，默认 0 0）：").strip()
    if start_input:
        start_x, start_y = map(int, start_input.split())
    else:
        start_x, start_y = 0, 0

    if not (0 <= start_x < n and 0 <= start_y < n):
        print("错误：起点坐标超出范围！")
        return

    print(f"\n棋盘大小：{n}×{n}")
    print(f"起点：({start_x}, {start_y})")
    print(f"总格数：{n * n}")
    print("\n正在求解...")

    start_time = time.time()
    board, path = warnsdorff_solve(n, start_x, start_y)
    elapsed = time.time() - start_time

    if board:
        print(f"\n求解成功！耗时：{elapsed:.3f} 秒")

        # 对于小棋盘打印结果
        if n <= 16:
            print_board(board, n)
            print_path(path, n)
        else:
            print(f"（棋盘太大，仅显示路径前 20 步和后 20 步）")
            print("\n前 20 步：")
            for i in range(min(20, len(path))):
                print(f"  {i+1:>3}. ({path[i][0]},{path[i][1]})")
            print("\n后 20 步：")
            for i in range(max(0, len(path)-20), len(path)):
                print(f"  {i+1:>3}. ({path[i][0]},{path[i][1]})")
    else:
        print("\n求解失败！未能找到完整路径。")

    # 导出路径到文件
    if path and n > 16:
        filename = f"knight_tour_{n}x{n}.txt"
        with open(filename, 'w') as f:
            f.write(f"骑士巡游路径 ({n}×{n})\n")
            f.write(f"起点：({start_x}, {start_y})\n\n")
            for i, (x, y) in enumerate(path):
                f.write(f"{i+1}. ({x},{y})\n")
        print(f"\n路径已导出到 {filename}")


if __name__ == "__main__":
    main()
