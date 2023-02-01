import re

from modules import scripts
splitSign = [',','(',')','[',']','（','）','，']

def promptFilter(promptStr):
    inBlock = False
    prompt = ''
    setPrompt = []
    prompts = []
    for str in promptStr:
        if not inBlock and str == '<':
            if prompt not in setPrompt and prompt.strip():
                setPrompt.append(prompt)
                prompts.append(' ')
                prompts.append(prompt.strip())
            inBlock = True
            prompts.append(str)
            prompt = ''
        elif inBlock:
            if str == '>':
                inBlock = False
                prompts.append(prompt)
                prompts.append(str)
                prompt = ''
            elif str != ' ':
                prompt += str
        elif not inBlock and str in splitSign:
            if prompt not in setPrompt and prompt.strip():
                setPrompt.append(prompt)
                prompts.append(' ')
                prompts.append(prompt.strip())
            str = str.replace('，', ',').replace(', ', ',').replace('（', '(').replace('）', ')')
            if str == ',' and len(prompts) and prompts[-1] in [',','(','']:
                str = ''
            elif str == ')' and len(prompts) and prompts[-1] == ',':
                prompts[-1] = ')'
            elif str == ')' and len(prompts) and prompts[-1] == '(':
                prompts[-1] = ''
            else:
                prompts.append(str)
            prompt = ''
        else:
            prompt += str
    return re.sub(r',$|^,','',''.join(prompts))

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

