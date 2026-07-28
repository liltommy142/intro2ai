# - GROUP INFORMATION
#   + NO.: 0
#   + NAME: A-Star
#   + MEMBER: 2
#       - STUDENT ID #1: 19127616
#       - STUDENT ID #2: 19127615
# Phỏng đoán vị trí đối phương khi mất dấu (enemy_position is None) bằng một phân phối xác suất
# trên bản đồ, cập nhật theo 2 pha của bộ lọc Bayes: predict (địch có thể đã đi đâu) rồi update
# (loại các ô mà quan sát hiện tại chứng minh là không có địch).
# Lab 2: tường luôn hiện (1), -1 là ô trống chưa nhìn thấy -> "đi được" là != 1.

import numpy as np


# dịch toàn mảng đi (dr, dc), phần trôi ra ngoài biên bị bỏ, chỗ trống điền 0
def shift(arr, dr, dc):
    h, w = arr.shape
    out = np.zeros_like(arr)
    out[max(0, dr) : h + min(0, dr), max(0, dc) : w + min(0, dc)] = arr[
        max(0, -dr) : h + min(0, -dr), max(0, -dc) : w + min(0, -dc)
    ]
    return out


class EnemyTracker:
    # enemy_speed = số ô đối phương đi được mỗi lượt theo đường thẳng. Ghost phải theo dõi Pacman
    # (2 ô/lượt theo luật đề) nên truyền 2; Pacman theo dõi Ghost (1 ô/lượt) nên để mặc định.
    def __init__(self, enemy_speed=1):
        self.belief = None
        self.enemy_speed = max(1, int(enemy_speed))

    # rải đều xác suất lên các ô CHƯA nhìn thấy (-1): ô đang nhìn được mà không có địch thì
    # chắc chắn địch không ở đó. Chỉ khi không còn ô nào chưa thấy mới rải lên mọi ô đi được.
    def _reset(self, map_state):
        candidates = map_state == -1
        if not candidates.any():
            candidates = map_state != 1

        self.belief = np.zeros(map_state.shape)
        count = np.count_nonzero(candidates)
        if count:
            self.belief[candidates] = 1.0 / count

    # pha 1 - predict: địch đứng yên, hoặc đi thẳng 1..enemy_speed ô theo 1 trong 4 hướng.
    # Nhân với walkable sau MỖI ô để khối lượng đâm vào tường bị triệt tiêu và không đi tiếp
    # được nữa - đúng luật "đi thẳng, bị tường chặn", không phải lan toả đẳng hướng.
    def _predict(self, map_state):
        walkable = map_state != 1
        spread = self.belief.copy()  # đứng yên

        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            moving = self.belief
            for _ in range(self.enemy_speed):
                moving = shift(moving, dr, dc) * walkable
                spread += moving

        # phép cộng trên làm tổng phồng lên; chia lại để belief luôn là phân phối hợp lệ
        total = spread.sum()
        self.belief = spread / total if total else spread

    def update(self, map_state, my_pos, enemy_pos, step):
        try:
            if self.belief is None or self.belief.shape != map_state.shape:
                self._reset(map_state)

            self._predict(map_state)

            # pha 2 - update: thấy địch thì biết chắc, không thấy thì loại mọi ô đang nhìn được.
            # Dựng mảng mới rồi mới gán đè: nếu enemy_pos lỗi thì belief cũ còn nguyên vẹn.
            if enemy_pos is not None:
                spotted = np.zeros(map_state.shape)
                spotted[enemy_pos[0], enemy_pos[1]] = 1.0
                self.belief = spotted
                return

            self.belief[map_state != -1] = 0.0

            total = self.belief.sum()
            if total > 0:
                self.belief /= total
            else:
                self._reset(map_state)  # mâu thuẫn quan sát -> rải lại từ đầu
        except Exception:
            pass  # giữ nguyên belief cũ (vẫn hợp lệ); nếu chưa có thì get_target trả None

    # ô khả nghi nhất; hòa thì numpy lấy ô đầu theo thứ tự hàng-cột nên kết quả ổn định
    def get_target(self, my_pos):
        if self.belief is None or self.belief.size == 0 or self.belief.max() <= 0:
            return None
        row, col = np.unravel_index(self.belief.argmax(), self.belief.shape)
        return int(row), int(col)
