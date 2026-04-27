import re
from collections import defaultdict

# -----------------------------
# File Parsing Utilities
# -----------------------------
def parse_file(filepath):
    classes = set()
    relationships = set()

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    mode = None

    for line in lines:
        if line.lower().startswith("classes"):
            mode = "class"
            continue
        elif line.lower().startswith("relationships"):
            mode = "rel"
            continue
        elif line.startswith("*****") or line.startswith("Subject"):
            continue

        if mode == "class":
            classes.add(line)

        elif mode == "rel":
            parts = re.split(r'\s+', line)
            if len(parts) >= 3:
                subj = parts[0]
                pred = parts[1]
                obj = "_".join(parts[2:])  # handle multi-word objects
                relationships.add((subj, pred, obj))

    return classes, relationships


# -----------------------------
# Kappa Computation
# -----------------------------
def compute_kappa(set1, set2):
    universe = set1.union(set2)

    # Binary labeling: present (1) or absent (0)
    y1 = []
    y2 = []

    for item in universe:
        y1.append(1 if item in set1 else 0)
        y2.append(1 if item in set2 else 0)

    # Confusion matrix
    TP = sum(1 for i in range(len(y1)) if y1[i] == 1 and y2[i] == 1)
    TN = sum(1 for i in range(len(y1)) if y1[i] == 0 and y2[i] == 0)
    FP = sum(1 for i in range(len(y1)) if y1[i] == 1 and y2[i] == 0)
    FN = sum(1 for i in range(len(y1)) if y1[i] == 0 and y2[i] == 1)

    total = len(universe)

    # Observed agreement
    Po = (TP + TN) / total

    # Probabilities
    p1_yes = (TP + FP) / total
    p1_no = (TN + FN) / total
    p2_yes = (TP + FN) / total
    p2_no = (TN + FP) / total

    # Expected agreement
    Pe = (p1_yes * p2_yes) + (p1_no * p2_no)

    # Cohen's Kappa
    if (1 - Pe) == 0:
        kappa = 0
    else:
        kappa = (Po - Pe) / (1 - Pe)

    return {
        "TP": TP, "TN": TN, "FP": FP, "FN": FN,
        "Po": Po,
        "Pe": Pe,
        "kappa": kappa,
        "total": total
    }


# -----------------------------
# Main Execution
# -----------------------------
if __name__ == "__main__":
    file1 = "E1_CP.txt"
    file2 = "E2_CP.txt"

    c1, r1 = parse_file(file1)
    c2, r2 = parse_file(file2)

    print("Classes in EP1: "+str(len(c1)))
    print("**************")
    print(c1)

    print("Relationships in EP1: "+str(len(r1)))
    print("**************")
    print(r1)

    print("Classes in EP2: "+str(len(c2)))
    print("**************")
    print(c2)

    print("Relationships in EP2: "+str(len(r2)))
    print("**************")
    print(r2)

    print("\n===== CLASS AGREEMENT =====")
    class_stats = compute_kappa(c1, c2)
    for k, v in class_stats.items():
        print(f"{k}: {v}")

    print("\n===== RELATIONSHIP AGREEMENT =====")
    rel_stats = compute_kappa(r1, r2)
    for k, v in rel_stats.items():
        print(f"{k}: {v}")