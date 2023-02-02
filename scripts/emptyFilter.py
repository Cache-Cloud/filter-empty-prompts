import re

from modules import scripts
splitSign = [',','(',')','[',']','（','）','，']

def promptFilter(promptStr:str):
    inBlock = False
    prompt = ''
    setPrompt = []
    prompts = []
    index = -1
    for str in promptStr:
        index += 1
        if not inBlock and str == '<' and '>' in promptStr[index:]:
            if prompt.strip() and prompt not in setPrompt:
                setPrompt.append(prompt.strip().lower())
                prompts.append(' ')
                prompts.append(prompt.strip().lower())
            inBlock = True
            prompts.append(str)
            prompt = ''
        elif inBlock:
            if str == '>':
                inBlock = False
                prompts.append(prompt)
                prompts.append(str)
                prompt = ''
            else:
                prompt += str
        elif not inBlock and str in splitSign:
            if prompt.strip() and prompt.strip() not in setPrompt:
                setPrompt.append(prompt.strip().lower())
                prompts.append(' ')
                prompts.append(prompt.strip().lower())
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
    if prompt.strip() and prompt.strip() not in setPrompt:
        setPrompt.append(prompt.strip().lower())
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

