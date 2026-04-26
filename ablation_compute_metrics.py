import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------------------
# ⚙️ CONFIG
# ---------------------------

SIM_THRESHOLD = 0.70
model = SentenceTransformer('all-MiniLM-L6-v2', cache_folder='./models')


# ---------------------------
# 🧹 NORMALIZATION
# ---------------------------

def normalize(text):
    return str(text).strip().lower()


# ---------------------------
# 🧠 SEMANTIC SIMILARITY
# ---------------------------

def sim(a, b):
    emb = model.encode([a, b])
    return cosine_similarity([emb[0]], [emb[1]])[0][0]


def match_text(a, b):
    a = normalize(a)
    b = normalize(b)

    if a == b:
        return True

    return sim(a, b) >= SIM_THRESHOLD


# ---------------------------
# 📊 CLASS MATCHING
# ---------------------------

def match_classes(pred, gt):
    matched = 0
    used = set()

    for p in pred:
        for i, g in enumerate(gt):
            if i in used:
                continue
            if match_text(p, g):
                matched += 1
                used.add(i)
                break

    return matched


# ---------------------------
# 📊 RELATIONSHIP MATCHING (TRIPLE-LEVEL)
# ---------------------------

# def match_relationships(pred, gt):
#     matched = 0
#     used = set()
#
#     for ps, pr, pt in pred:
#         for i, (gs, gr, gt_) in enumerate(gt):
#             if i in used:
#                 continue
#
#             if (
#                 match_text(ps, gs) and
#                 match_text(pr, gr) and
#                 match_text(pt, gt_)
#             ):
#                 matched += 1
#                 used.add(i)
#                 break
#
#     return matched

def match_relationships(pred, gt):
    matched = 0
    used = set()

    # Convert triples to sentences
    pred_texts = [f"{ps} {pr} {pt}" for ps, pr, pt in pred]
    gt_texts = [f"{gs} {gr} {gt_}" for gs, gr, gt_ in gt]

    for p in pred_texts:
        for i, g in enumerate(gt_texts):
            if i in used:
                continue

            if match_text(p, g):   # semantic similarity
                matched += 1
                used.add(i)
                break

    return matched


# ---------------------------
# 📊 METRICS
# ---------------------------

def compute_metrics(pred, gt, match_func):
    tp = match_func(pred, gt)
    fp = len(pred) - tp
    fn = len(gt) - tp

    precision = tp / (tp + fp) if (tp + fp) else 0
    recall = tp / (tp + fn) if (tp + fn) else 0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0

    return precision, recall, f1


# ---------------------------
# 📥 READ EXCEL
# ---------------------------

def read_sheet(file, sheet):
    df = pd.read_excel(file, sheet_name=sheet)

    # Classes
    classes = [
        normalize(c) for c in df.iloc[:, 0].dropna().tolist()
        if str(c).strip() != ""
    ]

    # Relationships (triples)
    relationships = []
    for _, row in df.iterrows():
        s, r, t = row[2], row[3], row[4]

        if pd.notna(s) and pd.notna(r) and pd.notna(t):
            relationships.append((
                normalize(s),
                normalize(r),
                normalize(t)
            ))

    return classes, relationships


# ---------------------------
# 🧪 EVALUATION
# ---------------------------

def evaluate_file(file):

    sheets = ["Single Prompt", "Multi Step", "No Few Shot", "DMP"]
    results = []

    gt_classes, gt_rels = read_sheet(file, "GoldStandard")

    for method in sheets:

        pred_classes, pred_rels = read_sheet(file, method)

        c_p, c_r, c_f = compute_metrics(pred_classes, gt_classes, match_classes)
        r_p, r_r, r_f = compute_metrics(pred_rels, gt_rels, match_relationships)

        results.append({
            "Dataset": file,
            "Method": method,
            "Class Precision": round(c_p, 3),
            "Class Recall": round(c_r, 3),
            "Class F1": round(c_f, 3),
            "Rel Precision": round(r_p, 3),
            "Rel Recall": round(r_r, 3),
            "Rel F1": round(r_f, 3)
        })

    return results


# ---------------------------
# 🚀 MAIN
# ---------------------------

if __name__ == "__main__":

    files = [
        "domain_model_comparison_CP.xlsx",
        "domain_model_comparison_RMS.xlsx",
        "domain_model_comparison_OPS.xlsx"
    ]

    all_results = []

    for f in files:
        res = evaluate_file(f)
        all_results.extend(res)

    df = pd.DataFrame(all_results)

    # ---------------------------
    # 📤 EXPORT
    # ---------------------------

    df.to_excel("evaluation_results.xlsx", index=False)
    df.to_csv("evaluation_results.csv", index=False)

    print("\n✅ Results exported:")
    print(" - evaluation_results.xlsx")
    print(" - evaluation_results.csv")

    print("\n📊 Preview:")
    print(df)