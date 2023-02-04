import re
from pathlib import Path

from modules import scripts,shared,script_callbacks


EMB_PATH = Path(shared.cmd_opts.embeddings_dir)
LORA_PATH = Path(shared.cmd_opts.lora_dir)
HYP_PATH = Path(shared.cmd_opts.hypernetwork_dir)

isFilterEmptyPrompt = True
isFilterRepoPrompt = True
isLoadLoraPromptTxt = True
def setVal():
    global isFilterEmptyPrompt
    global isFilterRepoPrompt
    global isLoadLoraPromptTxt
    isFilterEmptyPrompt = shared.opts.data.get('fp_delete_empty_prompts',True)
    isFilterRepoPrompt = shared.opts.data.get('fp_delete_repetition_prompts',True)
    isLoadLoraPromptTxt = shared.opts.data.get('fp_auto_load_prompts',True)


def get_hypernetworks_prompt_text(name:str):
    if HYP_PATH.joinpath(name+'.txt').exists() and HYP_PATH.joinpath(name+'.txt').is_file():
        with HYP_PATH.joinpath(name+'.txt').open() as txt:
          return txt.readline()
    if HYP_PATH.joinpath(name+'.promot.txt').exists() and HYP_PATH.joinpath(name+'.promot.txt').is_file():
        with HYP_PATH.joinpath(name+'.promot.txt').open() as txt:
          return txt.readline()
      
  
def get_lora_prompt_text():
    if LORA_PATH.joinpath(name+'.txt').exists() and LORA_PATH.joinpath(name+'.txt').is_file():
        with LORA_PATH.joinpath(name+'.txt').open() as txt:
          return txt.readline()
    if LORA_PATH.joinpath(name+'.promot.txt').exists() and LORA_PATH.joinpath(name+'.promot.txt').is_file():
        with LORA_PATH.joinpath(name+'.promot.txt').open() as txt:
          return txt.readline()

splitSign = [',','(',')','[',']','（','）','，']
setPrompt = []

def serializePrompt(prompt:str):
    need = True
    prompt = prompt.strip().lower()
    if isFilterEmptyPrompt and not prompt:
        return (False,prompt)
    if isFilterRepoPrompt:
        need = prompt not in setPrompt
        if need:
            setPrompt.append(prompt)
    return (need,prompt)

def promptFilter(promptStr:str):
    setPrompt.clear()
    inBlock = False
    prompt = ''
    prompts = []
    index = -1
    for str in promptStr:
        index += 1
        if not inBlock and str == '<' and '>' in promptStr[index:]:
            need,s_prompt = serializePrompt(prompt)
            if need:
                prompts.append(' ')
                prompts.append(s_prompt)
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
            need,s_prompt = serializePrompt(prompt)
            if need:
                prompts.append(' ')
                prompts.append(s_prompt)
            str = str.replace('，', ',').replace(', ', ',').replace('（', '(').replace('）', ')')
            
            if  isFilterEmptyPrompt :
                if str == ',' and len(prompts) and prompts[-1] in [',','(','']:
                    str = ''
                elif str == ')' and len(prompts) and prompts[-1] == ',':
                    prompts[-1] = ')'
                elif str == ')' and len(prompts) and prompts[-1] == '(':
                    prompts[-1] = ''
            if need:
                prompts.append(str)
            elif str != ',':
                prompts.append(str)
            prompt = ''
        else:
            prompt += str
    need,s_prompt = serializePrompt(prompt)
    if need:
        prompts.append(' ')
        prompts.append(s_prompt)
    return loadPromptsFile(re.sub(r',$|^,','',''.join(prompts)))

def loadPromptsFile(promptStr:str):
    return promptStr

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

def on_ui_settings():
    section = ("fp", "filter prompts")
    shared.opts.add_option("fp_delete_empty_prompts", shared.OptionInfo(True, "删除空标签", section=section))
    shared.opts.add_option("fp_delete_repetition_prompts", shared.OptionInfo(True, "过滤重复标签", section=section))
    # shared.opts.add_option("fp_auto_load_prompts", shared.OptionInfo(True, "加载Lora默认标签文件", section=section))
    shared.opts.onchange('fp_delete_empty_prompts', setVal)
    shared.opts.onchange('fp_delete_repetition_prompts', setVal)
    # shared.opts.onchange('fp_auto_load_prompts', setVal)
script_callbacks.on_ui_settings(on_ui_settings)