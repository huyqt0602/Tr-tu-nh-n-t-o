"""
DFS Vacuum Cleaner
0 = sàn sạch
1 = sàn bẩn
X = robot hút bụi
"""
room = [
    ['X', 0, 0],
    [1,   1, 0],
    [0,   0, 0]
]

rows = len(room)
cols = len(room[0])

visited = set()

directions = [
    (-1, 0),  # lên
    (1, 0),   # xuống
    (0, -1),  # trái
    (0, 1)    # phải
]

def find_robot():

    for i in range(rows):
        for j in range(cols):

            if room[i][j] == 'X':
                return i, j

def print_room():

    for row in room:
        print(row)

    print()

def is_goal_state():

    for row in room:
        for cell in row:

            if cell == 1:
                return False

    return True

def dfs(x, y):

    visited.add((x, y))

    print(f"Robot đang ở ({x}, {y})")
    print_room()

    # Nếu ô hiện tại bẩn thì hút
    if room[x][y] == 1:
        room[x][y] = 0

    # Kiểm tra goal state
    if is_goal_state():

        print("===== TRẠNG THÁI MỤC TIÊU =====")
        print("Đã đạt trạng thái mục tiêu: tất cả sàn đã sạch!")
        print_room()

        return True

    # Duyệt DFS
    for dx, dy in directions:

        nx = x + dx
        ny = y + dy

        # Kiểm tra hợp lệ
        if (0 <= nx < rows and
            0 <= ny < cols and
            (nx, ny) not in visited):

            # Lưu trạng thái ô mới
            temp = room[nx][ny]

            # Robot rời ô cũ
            room[x][y] = 0

            # Nếu ô mới bẩn thì hút sạch
            if room[nx][ny] == 1:
                room[nx][ny] = 0

            # Robot sang ô mới
            room[nx][ny] = 'X'

            print(f"Di chuyển tới ({nx}, {ny})")
            print_room()

            # DFS đệ quy
            if dfs(nx, ny):
                return True

            # Backtracking
            room[nx][ny] = temp
            room[x][y] = 'X'

    return False

print("===== TRẠNG THÁI BAN ĐẦU =====")
print_room()

start_x, start_y = find_robot()

dfs(start_x, start_y)