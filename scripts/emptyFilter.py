import os
import sys

from modules import scripts

def promptFilter(promptsInput):
    promptsInput = promptsInput.replace('，', ',')
    promptsInput = promptsInput.replace(', ', ',')
    promptsInput = promptsInput.replace('( ', '(')
    promptsInput = promptsInput.replace(') ', ')')
    all_prompts = promptsInput.split(',')
    all_prompts = [prompt for prompt in all_prompts if prompt.strip()]
    new_prompts = []
    prompts = []
    for prompt in all_prompts:
        if prompt.strip() not in new_prompts:
            new_prompts.append(prompt.strip())
            prompts.append(prompt)
    return ', '.join(new_prompts)

class emptyFilter(scripts.Script):
    def title(self):
        return "Empty prompt filter"

    def show(self, is_img2img):
        return scripts.AlwaysVisible
        
    
    def process(self, p):
        for i in range(len(p.all_prompts)):
            p.all_prompts[i] = promptFilter(p.all_prompts[i])

        for i in range(len(p.all_negative_prompts)):
            p.all_negative_prompts[i] = promptFilter(p.all_negative_prompts[i])

