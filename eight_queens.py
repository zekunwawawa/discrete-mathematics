# eight_queens.py
# 八皇后问题（N-Queens Problem）
# 在 8×8 的棋盘上放置 8 个皇后，使得任意两个皇后都不能互相攻击
# 即：任意两个皇后不在同一行、同一列、同一对角线上
# 算法：回溯法（Backtracking）

N = 8  # 棋盘大小

# 全局变量记录所有解
solutions = []

def is_safe(board, row, col):
    """
    检查在 (row, col) 位置放置皇后是否安全
    board: 一维数组，board[i] 表示第 i 行皇后所在的列
    """
    for i in range(row):
        # 检查同一列：board[i] == col
        # 检查主对角线：board[i] - i == col - row
        # 检查副对角线：board[i] + i == col + row
        if board[i] == col or \
           board[i] - i == col - row or \
           board[i] + i == col + row:
            return False
    return True


def solve(board, row):
    """
    回溯法求解八皇后问题
    board: 当前棋盘状态
    row: 当前正在放置皇后的行
    """
    # 递归出口：所有行都已放置皇后
    if row == N:
        solutions.append(board[:])  # 保存当前解的副本
        return

    # 尝试在当前行的每一列放置皇后
    for col in range(N):
        if is_safe(board, row, col):
            board[row] = col       # 放置皇后
            solve(board, row + 1)  # 递归放置下一行
            board[row] = -1        # 回溯：撤销当前放置


def print_board(solution):
    """
    打印棋盘
    solution: 一维数组，solution[i] 表示第 i 行皇后所在的列
    """
    print("+" + "---+" * N)
    for row in range(N):
        line = "|"
        for col in range(N):
            if solution[row] == col:
                line += " Q |"
            else:
                line += "   |"
        print(line)
        print("+" + "---+" * N)


def print_compact(solution):
    """
    紧凑打印：用坐标表示皇后位置
    """
    print("  行号:  ", end="")
    for i in range(N):
        print(f"{i+1} ", end="")
    print()
    print("  列号:  ", end="")
    for col in solution:
        print(f"{col+1} ", end="")
    print()


def main():
    print("=" * 40)
    print("  八皇后问题（N-Queens, N=8）")
    print("  算法：回溯法")
    print("=" * 40)

    # 初始化棋盘（-1 表示未放置皇后）
    board = [-1] * N

    # 求解
    solve(board, 0)

    # 输出结果
    print(f"\n共找到 {len(solutions)} 组解：\n")

    for idx, sol in enumerate(solutions):
        print(f"{'='*30}")
        print(f"  第 {idx + 1} 组解")
        print(f"{'='*30}")
        print_compact(sol)
        print()
        print_board(sol)
        print()


if __name__ == "__main__":
    main()
