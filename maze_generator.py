import sys
import random
import pygame

COLUMNS = 16            # 列数
ROWS = 16               # 行数
CELL_SIZE = 32          # 每个单元格的大小
BORDER_WIDTH = 3        # 外边框的厚度
PADDING = 32            # 留白空间的大小
TEXT_OFFSET = 5         # 偏移量，坐标与边框的距离
THICK_BORDER_WIDTH = 3  # 变粗边框的宽度
DASH_LENGTH = 10        # 虚线每段的长度
GAP_LENGTH = 5          # 虚线间隔的长度

pygame.init()
screen = pygame.display.set_mode((COLUMNS * CELL_SIZE + 2 * PADDING, ROWS * CELL_SIZE + 2 * PADDING))
pygame.display.set_caption("生成迷宫地图")
font = pygame.font.SysFont('Times New Roman', 16)

# 绘制网格
def draw_grid():
    # 绘制竖线
    for x in range(0, COLUMNS * CELL_SIZE + 1, CELL_SIZE):
        draw_dashed_line(screen, "gray", (x + PADDING, PADDING), (x + PADDING, ROWS * CELL_SIZE + PADDING), 1)
    # 绘制横线
    for y in range(0, ROWS * CELL_SIZE + 1, CELL_SIZE):
        draw_dashed_line(screen, "gray", (PADDING, y + PADDING), (COLUMNS * CELL_SIZE + PADDING, y + PADDING), 1)

# 绘制虚线
def draw_dashed_line(screen, color, start_pos, end_pos, width=1):
    if start_pos[0] == end_pos[0]:  # 竖线
        y = start_pos[1]
        while y < end_pos[1]:
            pygame.draw.line(screen, color, (start_pos[0], y), (start_pos[0], y + DASH_LENGTH), width)
            y += DASH_LENGTH + GAP_LENGTH
    elif start_pos[1] == end_pos[1]:  # 横线
        x = start_pos[0]
        while x < end_pos[0]:
            pygame.draw.line(screen, color, (x, start_pos[1]), (x + DASH_LENGTH, start_pos[1]), width)
            x += DASH_LENGTH + GAP_LENGTH

# 绘制外边框
def draw_border():
    # 绘制顶部边框
    pygame.draw.line(screen, "black", (PADDING, PADDING), (COLUMNS * CELL_SIZE + PADDING, PADDING), BORDER_WIDTH)
    # 绘制底部边框，考虑边框厚度
    pygame.draw.line(screen, "black", (PADDING, ROWS * CELL_SIZE + PADDING - BORDER_WIDTH // 2),
                     (COLUMNS * CELL_SIZE + PADDING, ROWS * CELL_SIZE + PADDING - BORDER_WIDTH // 2), BORDER_WIDTH)
    # 绘制左侧边框
    pygame.draw.line(screen, "black", (PADDING, PADDING), (PADDING, ROWS * CELL_SIZE + PADDING), BORDER_WIDTH)
    # 绘制右侧边框，考虑边框厚度
    pygame.draw.line(screen, "black", (COLUMNS * CELL_SIZE + PADDING - BORDER_WIDTH // 2, PADDING),
                     (COLUMNS * CELL_SIZE + PADDING - BORDER_WIDTH // 2, ROWS * CELL_SIZE + PADDING), BORDER_WIDTH)

# 绘制坐标
def draw_coordinates():
    # 绘制 x 轴坐标
    for x in range(COLUMNS):
        text = font.render(str(x), True, "black")
        # 调整 x 轴坐标文字的 y 位置，增加偏移量
        screen.blit(text, (x * CELL_SIZE + PADDING + CELL_SIZE // 2, PADDING // 2 - TEXT_OFFSET))
    # 绘制 y 轴坐标
    for y in range(ROWS):
        text = font.render(str(y), True, "black")
        # 调整 y 轴坐标文字的 x 位置，增加偏移量
        screen.blit(text, (PADDING // 2 - TEXT_OFFSET, y * CELL_SIZE + PADDING + CELL_SIZE // 2))

# 指定单元格的某个方向的边框变粗
def thicken_border(row, col, ori):
    x = col
    y = row

    if ori == 0:  # 上边框
        pygame.draw.line(screen, "black", (x * CELL_SIZE + PADDING, y * CELL_SIZE + PADDING),
                         ((x + 1) * CELL_SIZE + PADDING, y * CELL_SIZE + PADDING), THICK_BORDER_WIDTH)
    elif ori == 1:  # 右边框
        pygame.draw.line(screen, "black", ((x + 1) * CELL_SIZE + PADDING, y * CELL_SIZE + PADDING),
                         ((x + 1) * CELL_SIZE + PADDING, (y + 1) * CELL_SIZE + PADDING), THICK_BORDER_WIDTH)
    elif ori == 2:  # 下边框
        pygame.draw.line(screen, "black", (x * CELL_SIZE + PADDING, (y + 1) * CELL_SIZE + PADDING),
                         ((x + 1) * CELL_SIZE + PADDING, (y + 1) * CELL_SIZE + PADDING), THICK_BORDER_WIDTH)
    elif ori == 3:  # 左边框
        pygame.draw.line(screen, "black", (x * CELL_SIZE + PADDING, y * CELL_SIZE + PADDING),
                         (x * CELL_SIZE + PADDING, (y + 1) * CELL_SIZE + PADDING), THICK_BORDER_WIDTH)

# 将指定行和列的单元格涂成黄色
def color_cell(r, c, color):
    cell_x = c * CELL_SIZE + PADDING
    cell_y = r * CELL_SIZE + PADDING
    pygame.draw.rect(screen, color, (cell_x, cell_y, CELL_SIZE, CELL_SIZE))

# 将两个相邻单元格的中心点进行连线
def connect_cell_centers(r1, c1, r2, c2):
    # 检查两个单元格是否相邻
    if (abs(r1 - r2) == 1 and c1 == c2) or (abs(c1 - c2) == 1 and r1 == r2):
        # 计算第一个单元格的中心点坐标
        center_x1 = c1 * CELL_SIZE + PADDING + CELL_SIZE // 2
        center_y1 = r1 * CELL_SIZE + PADDING + CELL_SIZE // 2
        # 计算第二个单元格的中心点坐标
        center_x2 = c2 * CELL_SIZE + PADDING + CELL_SIZE // 2
        center_y2 = r2 * CELL_SIZE + PADDING + CELL_SIZE // 2
        # 绘制红色连线
        pygame.draw.line(screen, "red", (center_x1, center_y1), (center_x2, center_y2), 2)
    else:
        print("输入的两个单元格不相邻，无法连线。")

# 判断墙壁是否为外边框
def is_outside_wall(row ,col, wall):
    # 检查上边框是否为外边框
    if wall == 0 and row == 0:
        return True
    # 检查右边框是否为外边框
    elif wall == 1 and col == COLUMNS - 1:
        return True
    # 检查下边框是否为外边框
    elif wall == 2 and row == ROWS - 1:
        return True
    # 检查左边框是否为外边框
    elif wall == 3 and col == 0:
        return True
    return False

# 从 matrix 移除 wall
def delete_wall(select_wall):
    row = select_wall[0]
    col = select_wall[1]
    wall = select_wall[2]

    matrix[row][col][wall] = 0
    match wall:
        case 0:
            matrix[row-1][col][2] = 0
        case 1:
            matrix[row][col+1][3] = 0
        case 2:
            matrix[row+1][col][0] = 0
        case 3:
            matrix[row][col-1][1] = 0

# 返回被 wall 分割的两个单元
def find_Node(select_wall):
    row = select_wall[0]
    col = select_wall[1]
    wall = select_wall[2]

    select_nodeA = (row, col)
    match wall:
        case 0:
            select_nodeB = (row-1, col)
        case 1:
            select_nodeB = (row, col+1)
        case 2:
            select_nodeB = (row+1, col)
        case 3:
            select_nodeB = (row, col-1)
    return (select_nodeA, select_nodeB)

# 初始化迷宫矩阵[row][col][wall]
def maze_init(row, col):
    matrix = [[[1 for i in range(4)] for j in range(col)] for k in range(row)]
    matrix_visited.append((ROWS-1, 0))
    cur_to_be_selected.append((ROWS-1, 0, 0))
    return matrix

# 迷宫的生成与求解
def maze_generate():
    global cur_to_be_selected
    global to_be_selected
    global save_flag
    
    global result
    global path
    global solve_flag
    # 先从当前候选列表中选择
    if len(cur_to_be_selected) > 0 :
        rand_index = random.randint(0, len(cur_to_be_selected) - 1)
        select_wall = cur_to_be_selected[rand_index]
        cur_to_be_selected.remove(select_wall)  # 将选中墙壁从候选列表中删除
        # 分割的两个单元
        select_nodeA, select_nodeB = find_Node(select_wall)
    
        # A 已访问, B 未访问
        if select_nodeA in matrix_visited and select_nodeB not in matrix_visited:
            matrix_visited.append(select_nodeB)
            delete_wall(select_wall)

            # 转移当前候选列表
            for wall in cur_to_be_selected:
                to_be_selected.append(wall)
            cur_to_be_selected = [] # 清空当前候选列表
            
            # 将 B 的墙壁加入候选列表
            for i in range(4):
                # 判断是否为合法墙壁，为了排除边界墙壁
                if not is_outside_wall(select_nodeB[0], select_nodeB[1], i):
                    if(matrix[select_nodeB[0]][select_nodeB[1]][i] == 1):
                        cur_to_be_selected.append((select_nodeB[0], select_nodeB[1], i))

    # 从全局候选列表中选择
    elif len(to_be_selected) > 0:
        rand_index = random.randint(0, len(to_be_selected) - 1)
        select_wall = to_be_selected[rand_index]
        to_be_selected.remove(select_wall)  # 将选中墙壁从候选列表中删除
        # 分割的两个单元
        select_nodeA, select_nodeB = find_Node(select_wall)

        # A 已访问, B 未访问
        if select_nodeA in matrix_visited and select_nodeB not in matrix_visited:
            matrix_visited.append(select_nodeB)
            delete_wall(select_wall)

            # 将 B 的墙壁加入候选列表
            for i in range(4):
                # 判断是否为合法墙壁，为了排除边界墙壁
                if not is_outside_wall(select_nodeB[0], select_nodeB[1], i):
                    if(matrix[select_nodeB[0]][select_nodeB[1]][i] == 1):
                        cur_to_be_selected.append((select_nodeB[0], select_nodeB[1], i))

    elif(save_flag):
        maze_destination()
        save_maze()
        save_flag = 0
    elif(solve_flag):
        # 求解迷宫
        path.append((ROWS-1, 0))
        dfs((ROWS-1, 0))
        print("result:", result)
        solve_flag = 0

# DFS 求解迷宫
def dfs(curCell):
    global desRow
    global desCol
    global result
    global path
    curRow = curCell[0]
    curCol = curCell[1]
    visited[curRow][curCol] = True

    # print("path", path)
    if(curRow==desRow and curCol==desCol):
        # print("path:", path)
        result.append(path[:])
        return
    
    dir = [[-1, 0], [0, 1], [1, 0], [0, -1]]
    for i in range(4):
        if(matrix[curRow][curCol][i] == 0):
            nextRow = curRow + dir[i][0]
            nextCol = curCol + dir[i][1]
            # print(nextRow, nextCol)
            if(nextRow<0 or nextRow>=ROWS or nextCol<0 or nextCol>=COLUMNS):
                continue
            if(visited[nextRow][nextCol] == False):
                nextCell = (nextRow,nextCol)
                path.append(nextCell)
                dfs(nextCell)
                path.pop()

# 迷宫的起点与终点标记
def maze_destination():
    global desRow
    global desCol

    # 起点
    color_cell(ROWS-1, 0, "red")
    matrix[ROWS-1][0][0] = 0
    matrix[ROWS-1][0][1] = 1
    matrix[ROWS-1][0][2] = 1
    matrix[ROWS-1][0][3] = 1

    # 左上
    color_cell(ROWS//2-1, COLUMNS//2-1, "yellow")
    matrix[ROWS//2-1][COLUMNS//2-1][0] = 1
    matrix[ROWS//2-1][COLUMNS//2-1][1] = 0
    matrix[ROWS//2-1][COLUMNS//2-1][2] = 0
    matrix[ROWS//2-1][COLUMNS//2-1][3] = 1
    # 右上
    color_cell(ROWS//2-1, COLUMNS//2, "yellow")
    matrix[ROWS//2-1][COLUMNS//2][0] = 1
    matrix[ROWS//2-1][COLUMNS//2][1] = 1
    matrix[ROWS//2-1][COLUMNS//2][2] = 0
    matrix[ROWS//2-1][COLUMNS//2][3] = 0
    # 左下
    color_cell(ROWS//2, COLUMNS//2-1, "yellow")
    matrix[ROWS//2][COLUMNS//2-1][0] = 0
    matrix[ROWS//2][COLUMNS//2-1][1] = 0
    matrix[ROWS//2][COLUMNS//2-1][2] = 1
    matrix[ROWS//2][COLUMNS//2-1][3] = 1
    # 右下
    color_cell(ROWS//2, COLUMNS//2, "yellow")
    matrix[ROWS//2][COLUMNS//2][0] = 0
    matrix[ROWS//2][COLUMNS//2][1] = 1
    matrix[ROWS//2][COLUMNS//2][2] = 1
    matrix[ROWS//2][COLUMNS//2][3] = 0

    # 随机选择终点入口
    rand_gateway = random.randint(0, 7)
    match rand_gateway:
        case 0:
            desRow = ROWS//2-1
            desCol = COLUMNS//2-1
            matrix[ROWS//2-1][COLUMNS//2-1][0] = 0
            matrix[ROWS//2-2][COLUMNS//2-1][2] = 0
        case 1:
            desRow = ROWS//2-1
            desCol = COLUMNS//2
            matrix[ROWS//2-1][COLUMNS//2][0] = 0
            matrix[ROWS//2-2][COLUMNS//2][2] = 0
        case 2:
            desRow = ROWS//2-1
            desCol = COLUMNS//2
            matrix[ROWS//2-1][COLUMNS//2][1] = 0
            matrix[ROWS//2-1][COLUMNS//2+1][3] = 0
        case 3:
            desRow = ROWS//2
            desCol = COLUMNS//2
            matrix[ROWS//2][COLUMNS//2][1] = 0
            matrix[ROWS//2][COLUMNS//2+1][3] = 0
        case 4:
            desRow = ROWS//2
            desCol = COLUMNS//2
            matrix[ROWS//2][COLUMNS//2][2] = 0
            matrix[ROWS//2+1][COLUMNS//2][0] = 0
        case 5:
            desRow = ROWS//2
            desCol = COLUMNS//2-1
            matrix[ROWS//2][COLUMNS//2-1][2] = 0
            matrix[ROWS//2+1][COLUMNS//2-1][0] = 0
        case 6:
            desRow = ROWS//2
            desCol = COLUMNS//2-1
            matrix[ROWS//2][COLUMNS//2-1][3] = 0
            matrix[ROWS//2][COLUMNS//2-2][1] = 0
        case 7:
            desRow = ROWS//2-1
            desCol = COLUMNS//2-1
            matrix[ROWS//2-1][COLUMNS//2-1][3] = 0
            matrix[ROWS//2-1][COLUMNS//2-2][1] = 0

# 使用“standard”格式的典型二进制迷宫文件的十六进制转储
def save_maze():
    with open('maze.txt', 'a') as file:
        for i in range(ROWS-1, -1, -1):
            for j in range(COLUMNS):
                cell = 0b0000
                if matrix[i][j][0]: cell += 0b0001
                if matrix[i][j][1]: cell += 0b0010
                if matrix[i][j][2]: cell += 0b0100
                if matrix[i][j][3]: cell += 0b1000
                hex_str = f"0x{cell:02x}"
                file.write(hex_str + ' ')
            file.write('\n')
    print("output over.")
                
# 绘制迷宫
def draw_maze():
    color_cell(ROWS-1, 0, "red")
    color_cell(ROWS//2-1, COLUMNS//2-1, "yellow")
    color_cell(ROWS//2-1, COLUMNS//2, "yellow")
    color_cell(ROWS//2, COLUMNS//2-1, "yellow")
    color_cell(ROWS//2, COLUMNS//2, "yellow")
    for i in range(ROWS):
        for j in range(COLUMNS):
            for k in range(4):
                if matrix[i][j][k] == 1:
                    thicken_border(i, j , k)

def draw_path():
    if(len(result)==0):
        color_cell(ROWS//2-1, COLUMNS//2-1, "red")
        color_cell(ROWS//2-1, COLUMNS//2, "red")
        color_cell(ROWS//2, COLUMNS//2-1, "red")
        color_cell(ROWS//2, COLUMNS//2, "red")
    else:
        path_result = result[0]
        index = 1
        size = len(path_result)-1
        while(size):
            connect_cell_centers(path_result[index-1][0], path_result[index-1][1], path_result[index][0], path_result[index][1])
            index += 1
            size -= 1

# 生成迷宫
save_flag = 1
matrix_visited = []     # 已访问单元格
cur_to_be_selected = [] # 当前候选列表
to_be_selected = []     # 全局候选列表
matrix = maze_init(ROWS, COLUMNS)

# 终点坐标
desRow = 0
desCol = 0

# 求解迷宫
solve_flag = 1
path = []
result = []
visited = [[False for i in range(COLUMNS)] for j in range(ROWS)]

# 主循环，用于不断更新和显示迷宫
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    
    screen.fill("white")    # 清空屏幕，填充为白色
    draw_grid()             # 绘制网格
    draw_border()           # 绘制外边框
    draw_coordinates()      # 绘制坐标
    maze_generate()         # 生成迷宫
    draw_maze()             # 绘制迷宫
    draw_path()             # 绘制路径
    
    pygame.display.flip()           # 更新整个屏幕的显示
    pygame.time.Clock().tick(240)   # 控制帧率，每秒 60 帧