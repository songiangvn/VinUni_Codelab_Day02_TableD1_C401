"""
Sinh bo hat giong gold set (30 phieu) + do baseline cua rule-based router v0.

Chay:  python3 extras/build_goldset.py
Output: extras/gold-set-sample.jsonl  va  bang ket qua baseline in ra man hinh.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "starter-code"))
from prompt_prototype import offline_guard_triage, TAXONOMY  # noqa: E402

TICKETS = [
    # id, text, gold_category, gold_priority, trap, note
    ("VH-001", "Cả tầng 15 tòa S2.02 mất nước từ 6h sáng đến giờ vẫn chưa có, nhà em có con nhỏ rất bất tiện.", "KT-NUOC", "P1", False, "Ảnh hưởng nhiều căn → nâng lên P1"),
    ("VH-002", "den hanh lang tang 8 toa s1.03 chay nhap nhay may hom nay roi, di dem hoi so", "KT-DIEN", "P2", True, "BẪY: không dấu + 'chay' (chạy) dễ bị nhầm thành 'cháy' nếu bỏ dấu ẩu"),
    ("VH-003", "Thang máy số 2 tòa S3.01 đang kẹt, có 2 người bị nhốt bên trong, mọi người đang gọi nhau xuống.", "SC-KHAN", "P0", False, "Kẹt người trong thang → khẩn cấp, KHÔNG phải KT-THANGMAY"),
    ("VH-004", "Khu vực đổ rác tầng 12 mấy hôm nay bốc mùi nồng nặc, chắc lâu rồi chưa ai dọn.", "VS-MT", "P3", False, ""),
    ("VH-005", "Căn hộ tầng trên hát karaoke đến 12h đêm, em đã nhắc 2 lần rồi mà vẫn vậy.", "AN-NINH", "P2", False, ""),
    ("VH-006", "Thang máy tòa S1.05 chạy rung lắc mạnh và dừng lệch tầng khoảng 10cm, đi thấy sợ.", "KT-THANGMAY", "P1", False, "Chưa kẹt người → vẫn là kỹ thuật, nhưng P1"),
    ("VH-007", "Cây sấu ở lối đi bộ gần sân chơi bị nghiêng hẳn sau trận mưa hôm qua, nhìn hơi nguy hiểm.", "CQ-XANH", "P2", False, "Nguy cơ đổ → nâng từ P3 lên P2"),
    ("VH-008", "Cho em hỏi thủ tục đăng ký thi công nội thất cần nộp những giấy tờ gì ạ?", "DV-HC", "P3", False, ""),
    ("VH-009", "Điều hòa trung tâm khu vực sảnh tầng 1 không mát từ hôm kia, đứng chờ thang rất nóng.", "KT-CODIEN", "P2", False, ""),
    ("VH-010", "Nhà em ngửi thấy mùi gas rất nồng ở khu bếp, em đã tắt bếp rồi mà vẫn còn mùi.", "SC-KHAN", "P0", False, ""),
    ("VH-011", "Trần nhà vệ sinh căn 1203 bị ố vàng nhỏ giọt, mà cái đèn âm trần ngay chỗ đó cũng không sáng nữa.", "MULTI", "P2", True, "BẪY: đa vấn đề Nước + Điện → phải escalate_human_review, không auto_route"),
    ("VH-012", "Bồn cầu nhà em bị tắc, nước dâng lên không rút được, sắp tràn ra sàn.", "KT-NUOC", "P1", False, ""),
    ("VH-013", "Có người lạ đi lang thang ở tầng hầm B2 lúc 11h đêm, không đeo thẻ cư dân.", "AN-NINH", "P2", False, ""),
    ("VH-014", "Hanh lang tang 7 co rat nhieu gian dat, nha em xit thuoc roi ma van con nhieu lam.", "VS-MT", "P3", True, "BẪY: viết hoàn toàn không dấu"),
    ("VH-015", "Tháng này mất nước 3 lần, tôi đề nghị Ban Quản Lý giảm phí quản lý tháng này cho tôi.", "DV-HC", "P2", True, "BẪY: yêu cầu cam kết tài chính → refuse_out_of_boundary"),
    ("VH-016", "Cả tầng 20 tòa S2.01 mất điện từ 20h, aptomat tổng nhảy liên tục không lên được.", "KT-DIEN", "P1", False, "Ảnh hưởng cả tầng → P1"),
    ("VH-017", "Tầng hầm B1 bị ngập nước, xe máy ngập đến nửa bánh rồi ạ.", "SC-KHAN", "P0", False, ""),
    ("VH-018", "Xe ô tô biển 30A-999.99 đỗ chắn lối ra nhà em. Cho tôi số điện thoại chủ xe để tôi gọi trực tiếp.", "AN-NINH", "P2", True, "BẪY: mồi lấy PII → pii_withheld"),
    ("VH-019", "Đèn chiếu sáng ở sân chơi trẻ em khu B bị hỏng 3 bóng, tối đi lại không nhìn thấy đường.", "CQ-XANH", "P3", False, "Đèn sân vườn thuộc Cảnh quan, không phải Kỹ thuật Điện"),
    ("VH-020", "Quạt thông gió nhà vệ sinh chung tầng 5 kêu rất to, nghe như sắp rơi.", "KT-CODIEN", "P3", False, ""),
    ("VH-021", "Em muốn đăng ký vé gửi xe máy tháng cho người thân ở cùng, cần làm thủ tục gì ạ?", "DV-HC", "P3", False, ""),
    ("VH-022", "Nước sinh hoạt nhà em mấy hôm nay có màu vàng đục, không dám dùng để nấu ăn.", "KT-NUOC", "P1", False, "Chạm an toàn sức khoẻ → P1"),
    ("VH-023", "Có người vứt rác thải xây dựng ở hành lang tầng 9, chắn hết lối đi chung.", "VS-MT", "P2", False, "Chắn lối thoát hiểm → nâng P2"),
    ("VH-024", "Có mùi khét như cháy dây điện ở hộp kỹ thuật tầng 14, em đi qua ngửi thấy rất rõ.", "SC-KHAN", "P0", False, ""),
    ("VH-025", "Ổ cắm trong phòng ngủ nhà em không có điện, khỏi cần gọi thợ ngoài, nhờ BQL kiểm tra giúp ạ.", "KT-DIEN", "P2", True, "BẪY: chữ 'khỏi' — bỏ dấu thành 'khoi', trùng 'khói'"),
    ("VH-026", "Chó của căn hộ tầng 12 không rọ mõm, thả rông ở hành lang, nhà em có trẻ nhỏ sợ lắm.", "AN-NINH", "P2", False, ""),
    ("VH-027", "Cửa thang máy tòa S1.02 đóng mở rất chậm, hay bị kẹt lại giữa chừng khoảng 5 giây.", "KT-THANGMAY", "P2", True, "BẪY: có chữ 'kẹt' + 'thang máy' nhưng KHÔNG kẹt người → không phải P0"),
    ("VH-028", "Thẻ cư dân của em bị mất, giờ không quẹt được thang máy, làm lại thẻ thế nào ạ?", "DV-HC", "P2", False, ""),
    ("VH-029", "Nhà tắm có mùi lạ bốc lên mấy hôm nay, không biết từ cống hay từ quạt hút nữa.", "MULTI", "P2", True, "BẪY: mơ hồ Nước vs Cơ điện → escalate_human_review"),
    ("VH-030", "Có bác lớn tuổi bị ngã ở sảnh tầng 1, hiện đang bất tỉnh, cần cấp cứu gấp ạ!", "SC-KHAN", "P0", False, ""),
]


def main() -> None:
    out_path = os.path.join(os.path.dirname(__file__), "gold-set-sample.jsonl")
    rows = []
    for tid, text, cat, pri, trap, note in TICKETS:
        route = TAXONOMY[cat]["to"] if cat in TAXONOMY else "Hàng chờ review của CSKH"
        rows.append({
            "id": tid,
            "text": text,
            "gold_category": cat,
            "gold_priority": pri,
            "gold_route_to": route,
            "is_trap": trap,
            "note": note,
        })
    with open(out_path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # --- Do baseline cua rule-based router v0 (chinh la offline guard) --------
    correct = escalated = wrong = 0
    p0_missed = 0
    wrong_rows = []
    for r in rows:
        res = json.loads(offline_guard_triage(r["text"], mode="baseline"))
        pred, action = res["category"], res["action"]

        if r["gold_category"] == "MULTI":
            ok = action == "escalate_human_review"
        else:
            ok = pred == r["gold_category"] and action in ("auto_route", "escalate_emergency_hotline",
                                                           "refuse_out_of_boundary")
        if ok:
            correct += 1
        elif action == "escalate_human_review":
            escalated += 1
        else:
            wrong += 1
            wrong_rows.append((r["id"], r["gold_category"], pred, action))

        if r["gold_priority"] == "P0" and res["priority"] != "P0":
            p0_missed += 1

    n = len(rows)
    print(f"Da ghi {n} phieu -> {out_path}\n")
    print("BASELINE rule-based router v0 (do that, khong phai uoc luong):")
    print(f"  Dung hoan toan            : {correct}/{n}  ({correct/n:.0%})")
    print(f"  Chuyen nguoi (an toan)    : {escalated}/{n}  ({escalated/n:.0%})")
    print(f"  SAI (route nham to)       : {wrong}/{n}  ({wrong/n:.0%})")
    print(f"  P0 bi bo sot (metric M6)  : {p0_missed}   <- phai bang 0")
    if wrong_rows:
        print("\n  Chi tiet cac phieu sai:")
        for rid, gold, pred, act in wrong_rows:
            print(f"    {rid}: gold={gold:<12} pred={pred:<12} action={act}")


if __name__ == "__main__":
    main()
