import re
import random

import modules.scripts as scripts
import gradio as gr

from modules.processing import process_images

class Script(scripts.Script):
    def title(self):
        return "Alternate prompt"

    def ui(self, is_img2img):
        shuffle = gr.Checkbox(label='Shuffle items', value=False)  
        return [shuffle]

    def run(self, p, shuffle):
        def alternate_prompt(match_obj):
            items = match_obj.group(1).split('|')
            if shuffle:
                random.Random(p.seed).shuffle(items)
            ret = items[(p.steps - 1)%len(items)]
            for step in reversed(range(1, p.steps)):
                ret = f"[{items[(step - 1)%len(items)]}:{ret}:{step}]"
            return ret
        p.prompt = re.sub(r"\[([^\]]+(\|[^\]]+)+)\]", alternate_prompt, p.prompt)
        proc = process_images(p)
        return proc
