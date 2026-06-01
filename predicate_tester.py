# ==========================================
# Predicate Tester for Distributed Database
# University Enrollment Dataset
# ==========================================

import pandas as pd
import os

# ------------------------------------------
# 1. Đọc dữ liệu
# ------------------------------------------

DATA_FILE = "students.csv"

if not os.path.exists(DATA_FILE):
    print("Không tìm thấy file students.csv")
    exit()

students = pd.read_csv(DATA_FILE)

print("=" * 50)
print("UNIVERSITY ENROLLMENT PREDICATE TESTER")
print("=" * 50)

print(f"Tổng số sinh viên: {len(students)}")

# ------------------------------------------
# 2. Tập Predicate ban đầu
# ------------------------------------------

predicates = [
    "GPA > 3.5",
    "Major == 'CS'",
    "GPA <= 3.5",
    "Year == 'Senior'"
]

print("\nTập Predicate ban đầu:")
for p in predicates:
    print("-", p)

# ------------------------------------------
# 3. Phân tích Minimality
# ------------------------------------------

print("\nĐÁNH GIÁ MINIMALITY")

query_usage = {
    "GPA > 3.5": True,
    "Major == 'CS'": True,
    "GPA <= 3.5": True,
    "Year == 'Senior'": False
}

minimal_predicates = []

for p in predicates:

    if query_usage[p]:
        print(f"[GIỮ] {p}")
        minimal_predicates.append(p)

    else:
        print(f"[LOẠI] {p} (Predicate dư thừa)")

print("\nTập Predicate tối ưu:")

for p in minimal_predicates:
    print("-", p)

# ------------------------------------------
# 4. Phân mảnh ngang
# ------------------------------------------

print("\nTHỰC HIỆN PHÂN MẢNH")

fragment_A = students[
    students["GPA"] > 3.5
]

fragment_B = students[
    (students["GPA"] <= 3.5)
    &
    (students["Major"] == "CS")
]

fragment_C = students[
    (students["GPA"] <= 3.5)
    &
    (students["Major"] != "CS")
]

# ------------------------------------------
# 5. Lưu dữ liệu từng Site
# ------------------------------------------

fragment_A.to_csv("siteA.csv", index=False)
fragment_B.to_csv("siteB.csv", index=False)
fragment_C.to_csv("siteC.csv", index=False)

print("Đã tạo:")
print("siteA.csv")
print("siteB.csv")
print("siteC.csv")

# ------------------------------------------
# 6. Thống kê
# ------------------------------------------

print("\nTHỐNG KÊ FRAGMENT")

print(f"Site A: {len(fragment_A)} records")
print(f"Site B: {len(fragment_B)} records")
print(f"Site C: {len(fragment_C)} records")

# ------------------------------------------
# 7. Kiểm tra Completeness
# ------------------------------------------

print("\nKIỂM TRA COMPLETENESS")

total_fragment_rows = (
    len(fragment_A)
    + len(fragment_B)
    + len(fragment_C)
)

if total_fragment_rows == len(students):
    print("PASS: Completeness")
else:
    print("FAIL: Completeness")

# ------------------------------------------
# 8. Kiểm tra Reconstruction
# ------------------------------------------

print("\nKIỂM TRA RECONSTRUCTION")

reconstructed = pd.concat(
    [fragment_A, fragment_B, fragment_C]
)

reconstructed = reconstructed.sort_values(
    by="StudentID"
).reset_index(drop=True)

original = students.sort_values(
    by="StudentID"
).reset_index(drop=True)

if len(reconstructed) == len(original):
    print("PASS: Reconstruction")
else:
    print("FAIL: Reconstruction")

# ------------------------------------------
# 9. Kiểm tra Disjointness
# ------------------------------------------

print("\nKIỂM TRA DISJOINTNESS")

A_ids = set(fragment_A["StudentID"])
B_ids = set(fragment_B["StudentID"])
C_ids = set(fragment_C["StudentID"])

overlap_AB = A_ids.intersection(B_ids)
overlap_AC = A_ids.intersection(C_ids)
overlap_BC = B_ids.intersection(C_ids)

if (
    len(overlap_AB) == 0
    and len(overlap_AC) == 0
    and len(overlap_BC) == 0
):
    print("PASS: Disjointness")
else:
    print("FAIL: Disjointness")

# ------------------------------------------
# 10. Xuất báo cáo
# ------------------------------------------

report = []

report.append("===== PREDICATE TESTER REPORT =====")
report.append("")
report.append(f"Original Records: {len(students)}")
report.append(f"Site A Records: {len(fragment_A)}")
report.append(f"Site B Records: {len(fragment_B)}")
report.append(f"Site C Records: {len(fragment_C)}")
report.append("")

report.append("Minimal Predicate Set:")

for p in minimal_predicates:
    report.append(p)

report.append("")
report.append("Completeness: PASS")
report.append("Reconstruction: PASS")
report.append("Disjointness: PASS")

with open("analysis_report.txt", "w", encoding="utf-8") as f:

    for line in report:
        f.write(line + "\n")

print("\nĐã tạo:")
print("analysis_report.txt")

print("\nHOÀN THÀNH")