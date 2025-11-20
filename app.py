# app.py - Minimal QUANTUM SMC Offline Version
import gradio as gr
from PIL import Image, ImageDraw
import numpy as np
import cv2
from vision import detect_ob_fvg, try_ocr_read, y_to_price

# --------------------------
# ANNOTATION
# --------------------------
def annotate(img, analysis):
    pil = Image.fromarray(img)
    draw = ImageDraw.Draw(pil)

    for ob in analysis["ob"]:
        draw.rectangle([(0, ob["top"]), (pil.width, ob["bottom"])], outline="red", width=3)

    for fvg in analysis["fvg"]:
        draw.rectangle([(0, fvg["top"]), (pil.width, fvg["bottom"])], outline="blue", width=3)

    return pil

# --------------------------
# MAIN ANALYZER
# --------------------------
def run_smc(img, clicks, top_price, bottom_price):
    if img is None:
        return None, "No image uploaded."

    np_img = np.array(img)
    ob, fvg = detect_ob_fvg(np_img)

    if len(clicks) < 2:
        return None, "Click two points on image."

    y1 = clicks[0]["y"]
    y2 = clicks[1]["y"]

    analysis = {"ob": ob, "fvg": fvg}

    # Suggest Buy/Sell
    bias = "BUY" if len(fvg) > 0 else "SELL"
    analysis["bias"] = bias

    ann = annotate(np_img, analysis)

    report = f"""
QUANTUM SMC REPORT
====================
Bias: {bias}

Order Blocks: {len(ob)}
Fair Value Gaps: {len(fvg)}

Click Mapping:
 Top price: {top_price}
 Bottom price: {bottom_price}
"""

    return ann, report

# --------------------------
# UI
# --------------------------
with gr.Blocks() as app:
    gr.Markdown("# 🔥 QUANTUM SMC AI — Offline Version")

    img = gr.Image(type="pil", label="Upload Chart")
    clicks = gr.Image(type="numpy", tool="points", label="Click 2 points (top & bottom)")

    top_price = gr.Number(label="Top Price")
    bottom_price = gr.Number(label="Bottom Price")

    output_img = gr.Image(label="Annotated Chart")
    output_text = gr.Textbox(lines=15, label="SMC Report")

    btn = gr.Button("Analyze")

    btn.click(
        fn=run_smc,
        inputs=[img, clicks, top_price, bottom_price],
        outputs=[output_img, output_text]
    )

app.launch()
