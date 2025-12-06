# from screeninfo import get_monitors

# def calc_window_position(index: int):
#     # Lấy màn hình chính (monitor đầu tiên)
#     m = get_monitors()[0]
#     screen_width = m.width
#     screen_height = m.height  # nếu cần dùng

#     # Số cột trên 1 hàng (đồng bộ với bước nhảy x = 600)
#     so_luong_cot = screen_width // 600


#     # Tính x, y
#     x = 600 * (index % so_luong_cot) + 10
#     y = (index // so_luong_cot) * 600 + 10

#     return x, y

# def calc_win_pos_str(index: int) -> str:
#     x, y = calc_window_position(index)
#     return f"{x},{y}"

# if __name__ == "__main__":
#     for i in range(0, 11):
#         x, y = calc_window_position(i)
#         print(f"index {i}: ({x}, {y})")



from screeninfo import get_monitors
kichthuoc = ["600,800"]
def calc_window_position(index,kichthuoc):
    width_ui = int(kichthuoc[0].split(",")[0])
    height_ui = int(kichthuoc[0].split(",")[1])
    # Lấy màn hình chính (monitor đầu tiên)
    m = get_monitors()[0]
    screen_width = m.width
    screen_height = m.height  # nếu cần dùng

    # Số cột trên 1 hàng (đồng bộ với bước nhảy x = 600)
    so_luong_cot = screen_width // width_ui


    # Tính x, y khi cho rộng là 600 và cao là 800
    x = width_ui * (index % so_luong_cot) + 10
    y = (index // so_luong_cot) * height_ui + 10

    return x, y

def calc_win_pos_str(index):
    x, y = calc_window_position(index,kichthuoc)
    return f"{x},{y}"

if __name__ == "__main__":
    for i in range(0, 11):
        x, y = calc_window_position(i,kichthuoc)
        print(f"index {i}: ({x}, {y})")