import panel as pn
import json

pn.extension()

# ---------------------------
# 🔧 IMPORT YOUR METHODS
# ---------------------------

# Replace these with your actual implementations
from evaluation import single_prompt, multi_step


# from your_pipeline import run_full_chain, run_no_few_shot


# ---------------------------
# 🧹 FORMATTER
# ---------------------------

def format_json(data):
    try:
        return json.dumps(data, indent=2)
    except:
        return str(data)


# ---------------------------
# 🧠 CALLBACKS
# ---------------------------

def run_single(event):
    stories = input_box.value
    result = single_prompt(stories)
    output_single.value = format_json(result)


def run_multi(event):
    stories = input_box.value
    result = multi_step(stories)
    output_multi.value = format_json(result)


def run_full_chain(event):
    stories = input_box.value
    try:
        # from ui_ablation import run_full_chain
        result = run_full_chain(stories)
        output_full.value = format_json(result)
    except:
        output_full.value = "⚠️ Full chain not connected."


def run_no_few_shot(event):
    stories = input_box.value
    try:
        # from evaluation import run_no_few_shot
        result = run_no_few_shot(stories)
        output_no_few.value = format_json(result)
    except:
        output_no_few.value = "⚠️ No few-shot version not connected."


# ---------------------------
# 🧱 UI COMPONENTS
# ---------------------------

input_box = pn.widgets.TextAreaInput(
    name="User Stories",
    placeholder="Enter user stories here...",
    height=200
)

btn_single = pn.widgets.Button(name="Run Single Prompt", button_type="primary")
btn_multi = pn.widgets.Button(name="Run Multi-Step", button_type="warning")
btn_full = pn.widgets.Button(name="Run Full Chain", button_type="success")
btn_no_few = pn.widgets.Button(name="Run No Few-Shot", button_type="danger")

# Outputs
output_single = pn.widgets.TextAreaInput(name="Single Prompt Output", height=250)
output_multi = pn.widgets.TextAreaInput(name="Multi-Step Output", height=250)
output_full = pn.widgets.TextAreaInput(name="Full Chain Output", height=250)
output_no_few = pn.widgets.TextAreaInput(name="No Few-Shot Output", height=250)

# ---------------------------
# 🔗 BIND EVENTS
# ---------------------------

btn_single.on_click(run_single)
btn_multi.on_click(run_multi)
btn_full.on_click(run_full_chain)
btn_no_few.on_click(run_no_few_shot)

# ---------------------------
# 🎨 LAYOUT
# ---------------------------

layout = pn.Column(
    pn.pane.Markdown("## 🧪 Ablation Study UI - Domain Model Extraction"),

    pn.Row(input_box),

    pn.Row(btn_single, btn_multi, btn_full, btn_no_few),

    pn.Row(
        pn.Column(output_single),
        pn.Column(output_multi)
    ),

    pn.Row(
        pn.Column(output_full),
        pn.Column(output_no_few)
    )
)

layout.servable()