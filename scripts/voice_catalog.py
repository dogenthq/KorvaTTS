"""Catalog of bundled voices with a distinct demo sentence per voice.

Each sentence is a realistic Vietnamese use case with natural English code-switching, so the
model-card samples show different registers (podcast, support, e-learning, news, dev talk…).
Keep stems in sync with ``assets/voice_styles/*.json``.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Voice:
    stem: str
    display_name: str
    gender: str
    sample_text: str


VOICES: list[Voice] = [
    Voice("bao_kim", "Bảo Kim", "female",
          "Chào mừng bạn đến với podcast Công nghệ mỗi ngày. Hôm nay chúng ta sẽ nói về cách AI "
          "đang thay đổi ngành marketing và những skill mà người làm content cần có."),
    Voice("khanh_vy", "Khánh Vy", "female",
          "Dạ, đơn hàng của anh đã được xác nhận và sẽ ship trong vòng hai ngày. Anh có thể track "
          "đơn hàng qua app hoặc website của bên em bất cứ lúc nào ạ."),
    Voice("ngoc_huyen", "Ngọc Huyền", "female",
          "Trong bài học hôm nay, các em sẽ học cách dùng hàm filter và map trong JavaScript "
          "để xử lý dữ liệu. Mở file bài tập lên và chúng ta bắt đầu nhé."),
    Voice("phuong_linh", "Phương Linh", "female",
          "Bản tin buổi sáng: thị trường chứng khoán mở cửa trong sắc xanh, nhóm cổ phiếu công "
          "nghệ và các startup fintech tiếp tục dẫn dắt dòng tiền. Quý vị có thể theo dõi update "
          "trực tiếp trên app của chúng tôi."),
    Voice("quynh_nhu", "Quỳnh Như", "female",
          "Bạn có mười phút không? Mình muốn demo tính năng voice cloning mới, feedback của bạn "
          "rất quan trọng với team trước khi release."),
    Voice("gia_bao", "Gia Bảo", "male",
          "Chào cả nhà, hôm nay mình review chiếc laptop mới: màn hình OLED, pin trâu, "
          "và hiệu năng thì khỏi bàn. Bấm subscribe để không bỏ lỡ video tiếp theo nhé."),
    Voice("hoang_nam", "Hoàng Nam", "male",
          "Thưa quý khách, chuyến bay VN một hai ba đi Đà Nẵng sẽ bắt đầu boarding tại cửa số bảy "
          "trong vài phút nữa. Xin vui lòng chuẩn bị sẵn thẻ lên máy bay."),
    Voice("huu_dat", "Hữu Đạt", "male",
          "Sprint này team cần hoàn thành phần login bằng OAuth, còn phần dashboard sẽ dời sang "
          "sprint sau. Ai có blocker thì báo trong daily standup nhé."),
    Voice("quang_huy", "Quang Huy", "male",
          "Nhớ backup dữ liệu trước khi update hệ điều hành, nếu không lỡ mất file thì khó "
          "khôi phục lắm đấy. Tốt nhất là sync lên cloud rồi hãy bấm cài đặt."),
    Voice("thanh_phong", "Thanh Phong", "male",
          "Trận đấu tối nay giữa Việt Nam và Thái Lan sẽ được livestream lúc bảy giờ rưỡi "
          "trên kênh chính thức. Anh em nhớ đặt lịch để không bỏ lỡ highlight nhé."),
]
