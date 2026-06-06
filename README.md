## 📖 项目简介
本项目用于整理和实现离散数学课程中的经典算法，代码以 Python 为主，包含交互式网页前端。适合课程复习、算法复盘与编程练习。

## 📂 目录结构
```plaintext
discrete-mathematics/
├── README.md
├── .gitignore
├── eight_queens.py          # 八皇后问题（回溯法）
├── quine_mccluskey.py       # Q-M 简化算法（命令行版）
├── qm_solver.html           # Q-M 简化算法（交互式网页版）
├── knight_tour.py           # 骑士巡游问题（命令行版）
└── knight_tour.html         # 骑士巡游问题（动画演示网页版）
```

## 🛠️ 运行方式

### 八皇后问题
```bash
python eight_queens.py
```

### Q-M 简化算法（命令行）
```bash
python quine_mccluskey.py
```

### Q-M 简化算法（网页版）
直接用浏览器打开 `qm_solver.html`

### 骑士巡游问题（命令行）
```bash
python knight_tour.py
```

### 骑士巡游问题（动画演示）
直接用浏览器打开 `knight_tour.html`

---

### ✨ 算法清单

| 算法 | 文件 | 说明 |
|------|------|------|
| **八皇后问题** | `eight_queens.py` | 回溯法求解 N=8 皇后问题，输出全部 92 组解 |
| **Q-M 简化算法** | `quine_mccluskey.py` | Quine-McCluskey 算法，布尔函数最小化 |
| **Q-M 交互式** | `qm_solver.html` | 网页版 Q-M 算法，支持真值表输入和动态求解 |
| **骑士巡游** | `knight_tour.py` | Warnsdorff 启发式 + 回溯法，支持 n≤64 |
| **骑士巡游动画** | `knight_tour.html` | 网页版动画演示，支持 3-20 棋盘大小 |

## 📝 更新日志

- **2026-06-06**：新增骑士巡游问题（Python + 网页动画演示）
- **2026-06-06**：新增八皇后问题、Q-M 简化算法（Python + 网页前端）

---

## 📧 联系方式

- GitHub：[zekunwawawa](https://github.com/zekunwawawa)
- 邮箱：`2847432767@qq.com`
