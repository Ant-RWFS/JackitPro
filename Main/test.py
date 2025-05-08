import curses
import time


def combined_loading(stdscr):
    curses.curs_set(0)  # 隐藏光标
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    # 旋转动画字符
    spin_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    # 精细进度块字符
    blocks = [" ", "▏", "▎", "▍", "▌", "▋", "▊", "▉", "█"]

    bar_width = width - 10  # 进度条宽度

    for i in range(101):  # 0-100%
        stdscr.clear()

        # 旋转图标 (左侧)
        spin_index = i % len(spin_chars)
        stdscr.addstr(height // 2, 2, spin_chars[spin_index])

        # 进度条框架
        stdscr.addstr(height // 2, 5, "[")
        stdscr.addstr(height // 2, 5 + bar_width + 1, "]")

        # 计算进度
        filled = i * bar_width / 100
        full_blocks = int(filled)
        partial = int((filled - full_blocks) * (len(blocks) - 1))

        # 绘制进度条
        stdscr.addstr(height // 2, 6, "█" * full_blocks)
        if full_blocks < bar_width:
            stdscr.addstr(height // 2, 6 + full_blocks, blocks[partial])

        # 显示百分比 (右侧)
        stdscr.addstr(height // 2, 6 + bar_width + 1, f"{i}%")

        # 底部状态信息
        if i < 30:
            status = "初始化..."
        elif i < 70:
            status = "处理中..."
        else:
            status = "即将完成..."
        stdscr.addstr(height // 2 + 2, width // 2 - len(status) // 2, status)

        stdscr.refresh()
        time.sleep(0.05)  # 控制速度


if __name__ == "__main__":
    curses.wrapper(combined_loading)
# import curses
# import time
#
#
# def spinning_loader(stdscr):
#     curses.curs_set(0)  # 隐藏光标
#     stdscr.clear()
#
#     # 多种旋转动画字符集可选
#     spinner_sets = {
#         'dots': ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],  # 点状
#         'arrows': ["←", "↖", "↑", "↗", "→", "↘", "↓", "↙"],  # 箭头
#         'circle': ["◐", "◓", "◑", "◒"],  # 圆圈
#         'bouncing': ["[    ]", "[=   ]", "[==  ]", "[=== ]", "[ ===]", "[  ==]", "[   =]", "[    ]"],  # 弹跳条
#         'moon': ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"], # 月相
#         'pwn':["P  ","PW ","PWN"," WN","  N"],
#         'sonar':["    .    ",
#    "    ▫    ",
#    "   [□]   ",
#    "  [[ ]]  ",
#    " [[[ ]]] ",
#    "[[[   ]]]",
#    "[[     ]]",
#    "[       ]",
#    "         "],
#
#     }
#
#     # 选择你喜欢的样式
#     spin_chars = spinner_sets['sonar']
#
#     height, width = stdscr.getmaxyx()
#     message = "加载中..."
#     x_pos = width // 2 - len(message) // 2 - 2
#
#     try:
#         i = 0
#         while True:
#             stdscr.clear()
#
#             # 显示旋转字符和消息
#             stdscr.addstr(height // 2, x_pos, spin_chars[i % len(spin_chars)] + " " + message)
#
#             # 添加按q退出的提示
#             stdscr.addstr(height - 1, 2, "按 q 键退出", curses.A_DIM)
#
#             stdscr.refresh()
#             time.sleep(0.1)  # 控制旋转速度
#
#             # 检查是否按下q键退出
#             stdscr.nodelay(True)
#             if stdscr.getch() == ord('q'):
#                 break
#
#             i += 1
#
#     except KeyboardInterrupt:
#         pass
#
#
# if __name__ == "__main__":
#     curses.wrapper(spinning_loader)
