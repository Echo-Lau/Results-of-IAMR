import os
import json
import pandas as pd
import re
from datetime import datetime
import glob

# vec_proc = ["cpu", "gpu"]
# vec_dim = ["2d", "3d"]
# vec_skip  = ["skip0", "skip1"]
# vec_cycling = ["None", "Auto"]
# vec_max_level = ["1", "2"]
# vec_max_grid_size = ["8", "16"]
# vec_regrid_int = ["4", "8"]

class Result:
    def __init__(self) -> None:

        self.skip:int = 0
        self.cycling:str = "None"
        self.max_level:int = 1
        self.max_grid_size:int = 8
        self.regrid_int:int = 4
        self.cpu_time:float = -1
        self.cpu_step:int = 0
        self.cpu_function_name = []
        self.cpu_function_percent = []
        self.gpu_time:float = -1 
        self.gpu_step:int = 0
        self.gpu_function_name = []
        self.gpu_function_percent = []

    def __str__(self):
        return f"{self.skip} {self.cycling} {self.max_level} {self.max_grid_size} {self.regrid_int} {self.cpu_time} {self.gpu_step} {self.gpu_time} {self.cpu_step}"

    def __repr__(self):
        return f"{self.skip} {self.cycling} {self.max_level} {self.max_grid_size} {self.regrid_int} {self.cpu_time} {self.cpu_step} {self.gpu_time} {self.cpu_step}"
    
    def __eq__(self, other):
        if isinstance(other, Result):
            # return self.name == other.name
            return self.skip == other.skip and self.cycling == other.cycling and self.max_grid_size == other.max_grid_size and self.max_level == other.max_level and self.regrid_int == other.regrid_int
        return False
    
    def Update(self, other):
        if self.cpu_time <= 0 or self.cpu_step <= 0:
            self.cpu_time = other.cpu_time
            self.cpu_step = other.cpu_step
            self.cpu_function_name = other.cpu_function_name
            self.cpu_function_percent = other.cpu_function_percent
        if self.gpu_time <=0 or  self.gpu_step <=0:
            self.gpu_time = other.gpu_time
            self.gpu_step = other.gpu_step
            self.gpu_function_name = other.gpu_function_name
            self.gpu_function_percent = other.gpu_function_percent


        # str = cpu2d_skip0_Auto_mgs16_1_regrid8 or gpu2d_skip0_Auto_mgs16_1_regrid8


        
def CheckInput(path_input, case_res):
    with open(path_input, 'r') as file:
        while(True):
            line = file.readline()
            list_para = ["skip", "max_grid_size", "max_level", "cycling", "regrid_int"]
            for para in list_para: 
                if para in line and "=" in line :
                    line.strip()
                    if not line.startswith("#"):
                        pattern = re.compile(r'=(.*?)#')
                        match = pattern.search(line)
                        if match:
                            value = match.group(1).strip()
                        if not value == str(getattr(case_res,para)):
                            # print(case_res)
                            print(f"ERROR: 参数和文件名不同")
                            print(f"path : {path_input}")  
                            print(f"{line}")
                    else:
                        print(f"ERROR: 注释，未生效")
                        print(f"path : {path_input}")
                        print(f"{line}")

                        

            if line == '':
                case_res.gpu_time = -1 
                break            

# 打印列表 [Result1, Result2, ... ]
def Print(list_result):
    header = ["skip_level_projector", "cycling", "max_level", "max_grid_size", "regrid_int", "cpu time", "cpu step", "gpu time", "gpu step"]
    table = []
    for v in list_result:
        # cpu2d_skip0_Auto_mgs16_1_regrid8
        row = []
        row.append(v.skip)
        row.append(v.cycling)
        row.append(v.max_level)
        row.append(v.max_grid_size)
        row.append(v.regrid_int)
        row.append(v.cpu_time)
        row.append(v.cpu_step)
        row.append(v.gpu_time)
        row.append(v.gpu_step)
        table.append(row)
            
    df = pd.DataFrame(table, columns= header, index=range(1, len(table)+1))    
    # print("###################################################################################################################")
    print("-------------------------------------------------------------------------------------------------------------------")
    print(df)    

    # df.to_csv(f'table_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv', index=False)

def PrintFunc(list_result):
    return

def CollectData(case):
        res = []
        types = ["case_results_cpu2d", "case_results_gpu2d"]
        for type in types:
            path = f"{case}/{type}"
            if os.path.exists(path):
                folders = os.listdir(path)
                for folder in folders:
                    file_path = f"{case}/{type}/{folder}"
                    files = os.listdir(file_path)
                    
                    # folder = cpu2d_skip0_Auto_mgs16_1_regrid8
                    # name = folder[6:]
                    case_res = Result()
                    if "128" in folder or "64" in folder or "32" in folder:
                        continue
                    match = re.search(r'skip(\d+)', folder)
                    if match:
                        skip = match.group(1)
                        case_res.skip = int(skip)

                    match = re.search(r'(auto|none)', folder, re.IGNORECASE)
                    if match:
                        cycling = match.group(0)
                        case_res.cycling = cycling
                    match = re.search(r'_(\d+)_', folder)
                    if match:
                        max_level = match.group(1)
                        case_res.max_level = int(max_level)         
                    
                    match = re.search(r'mgs(\d+)', folder)
                    if match:
                        mgs = match.group(1)
                        case_res.max_grid_size = int(mgs)
                    
                    match = re.search(r'regrid(\d+)', folder)
                    if match:
                        regrid = match.group(1)
                        case_res.regrid_int = int(regrid)             
                    
                    pattern = f"{file_path}/input*"
                    input_files = glob.glob(pattern)
                    
                    # CheckInput(input_files[0],case_res)

                    if "cpu" in type:
                        for file in files:
                            step = 0
                            match = re.match(r"chk(\d+)", file)
                            if match:
                                case_res.cpu_step = max(int(match.group(1)), step)
                        

                        with open(f"{file_path}/log.txt", 'r') as file:
                            line = file.readline()
                            while(True):
                                line = file.readline()
                                if "Total Timers" in line:
                                    numbers = [float(s) for s in line.split() if s.replace('.', '', 1).isdigit()]
                                    case_res.cpu_time = numbers[0]
                                    break
                                
                                if line == '':
                                    case_res.cpu_time = -1 
                                    break
                        
                        with open(f"{file_path}/log.txt", 'r') as file:                      
                                found_start = False
                                flag = 2
                                for line in file:
                                    if "Function Name" in line:
                                        flag -= 1 
                                        if flag == 0:
                                            found_start = True
                                        continue
                                    elif "=====" in line: 
                                        break
                                    if found_start:
                                        line_data = line.split()
                                        # temp = {}
                                        # temp[line_data[0]] = line_data[7] # + line_data[8]
                                        
                                        temp = []
                                        case_res.cpu_function_name.append(line_data[0])
                                        case_res.cpu_function_percent.append(line_data[len(line_data)-2])
                    
                    if "gpu" in type:
                        for file in files:
                            step = 0
                            match = re.match(r"chk(\d+)", file)
                            if match:
                                case_res.gpu_step = max(int(match.group(1)), step)
                        
                        with open(f"{file_path}/log.txt", 'r') as file:
                            line = file.readline()
                            while(True):
                                line = file.readline()
                                if "Total Timers" in line:
                                    numbers = [float(s) for s in line.split() if s.replace('.', '', 1).isdigit()]
                                    case_res.gpu_time = numbers[0]
                                    break
                                
                                if line == '':
                                    case_res.gpu_time = -1 
                                    break
                        
                        with open(f"{file_path}/log.txt", 'r') as file:                      
                                found_start = False
                                flag = 2
                                for line in file:
                                    if "Function Name" in line:
                                        flag -= 1 
                                        if flag == 0:
                                            found_start = True
                                        continue
                                    elif "=====" in line: 
                                        break
                                    if found_start:
                                        line_data = line.split()
                                        # temp = {}
                                        # temp[line_data[0]] = line_data[7] # + line_data[8]
                                        
                                        temp = []
                                        case_res.gpu_function_name.append(line_data[0])
                                        case_res.gpu_function_percent.append(line_data[len(line_data)-2])
                                        
                    found = False
                    for item in res:
                        if item == case_res:
                            item.Update(case_res)
                            found = True
                            break
                    if not found:
                        res.append(case_res)
        
        return res
   
# 从所有结果中挑选符合输入参数的结果， 如输入参数factors = {"skip" : [1]} 则会找到所有skip = 1的结果， 本例子中则有16个，并返回该列表
def Get(vec_res, factors = {}):    
    vec_factor = {
        "skip" : [0 , 1],
        "cycling" : ["Auto", "None"],
        "max_level" : [1, 2],
        "max_grid_size" : [8, 16],
        "regrid_int" : [4, 8],
    }    
    for k, v in factors.items():
        vec_factor[k] = v
    # import pdb; pdb.set_trace()
    ans = []

    for skip in vec_factor["skip"]:
        for cycling in vec_factor["cycling"]:
            for max_level in vec_factor["max_level"]:
                for max_grid_size in vec_factor["max_grid_size"]:
                    for regrid_int in vec_factor["regrid_int"]:
                        for item in vec_res:
                            if( item.skip == skip and
                                item.cycling == cycling and
                                item.max_level == max_level  and
                                item.max_grid_size == max_grid_size and 
                                item.regrid_int == regrid_int ):
                                ans.append(item)
    return ans
  
def CompareAndShow(vec_res, factor, processor = "cpu"):
    
    vec = {
        "skip" : [0, 1],
        "cycling": ["Auto", "None"],
        "max_grid_size" : [8, 16],
        "max_level" : [1, 2],
        "regrid_int" : [4, 8]
    }
    
    vec_compare = []
    for x in vec[factor]:
        temp = Get(vec_res, {factor : [x]})
        vec_compare.append(temp)
    
    ans = 0
    error = 0
    items_true = []
    items_false = []
    min_delta_cpu_time = float('inf'); max_delta_cpu_time = 0
    min_delta_gpu_time = float('inf'); max_delta_gpu_time = 0
    for i in range(len(vec_compare[0])):
        v0 = vec_compare[0]
        v1 = vec_compare[1]
        
        min_delta_cpu_time = min(min_delta_cpu_time, abs(v0[i].cpu_time - v1[i].cpu_time))
        max_delta_cpu_time = max(max_delta_cpu_time, abs(v0[i].cpu_time - v1[i].cpu_time))
        
        min_delta_gpu_time = min(min_delta_gpu_time, abs(v0[i].gpu_time - v1[i].gpu_time))
        max_delta_gpu_time = max(max_delta_gpu_time, abs(v0[i].gpu_time - v1[i].gpu_time))

        if processor == "cpu":
            if (v0[i].cpu_time == -1 or v1[i].cpu_time == -1):
                discard += 1
            if (v0[i].cpu_time >  v1[i].cpu_time):
                ans+=1
                temp = []
                temp.append(v0[i])
                temp.append(v1[i])
                items_true.append(temp)
            else:
                temp = []
                temp.append(v0[i])
                temp.append(v1[i])
                items_false.append(temp)
        elif processor == "gpu":
            if (v0[i].gpu_time == -1 or v1[i].gpu_time == -1):
                discard += 1
            if (v0[i].gpu_time >  v1[i].gpu_time):
                ans+=1
                temp = []
                temp.append(v0[i])
                temp.append(v1[i])
                items_true.append(temp)
            else:
                temp = []
                temp.append(v0[i])
                temp.append(v1[i])
                items_false.append(temp)

    
    # 其他参数相同，比较 {factor}, 共有 {total} 种情况，其中 {factor} : {vec[factor][0]} slower than  {vec[factor][1]}  = 共有 {ans} 种
    # error表示该例子没有得到time， time == -1 
    print("####################################################################################################################")
    print(f"{processor} || total : 16, error : {error} || {factor:<{15}} : {vec[factor][0]:>{8}} slower than {vec[factor][1]:<{8}} : {ans:>{8}}  ")
    print(f"min_delta_cpu_time: {min_delta_cpu_time}")
    print(f"max_delta_cpu_time: {max_delta_cpu_time}")
    print(f"min_delta_gpu_time: {min_delta_gpu_time}")
    print(f"max_delta_gpu_time: {max_delta_gpu_time}")


    # 打印详细信息
    # print(f"The following are all examples for {factor} : {vec[factor][0]} slower than {vec[factor][1]}")
    # for items in items_true:
    #     Print(items)

    # print(f"The following are all examples for {factor} : {vec[factor][0]} faster than {vec[factor][1]}")
    # for items in items_false:
    #     Print(items)


def AdjustResult(list_result, para):
    # 按参数调整, 
    if para == 'cpu_time':
        list_result.sort(key=lambda x: x.cpu_time)
    elif para == 'gpu_time':
        list_result.sort(key=lambda x: x.gpu_time)
    elif para == 'max_grid_size':
        # import pdb ; pdb.set_trace()  # 在这里设置一个断点
        list_result.sort(key=lambda x: (x.max_grid_size, x.cpu_time, x.gpu_time))  
    elif para == "cycling":
        list_result.sort(key=lambda x: (x.cycling, x.cpu_time, x.gpu_time))  


def TopFunc(list_result):
    for res in list_result:
        for i in range(3):
            print(f"{res.cpu_function_name[i]} : {res.cpu_function_percent[i]}")

def GetFuncOnEveryCase(dictionary, str):
    for k, v in dictionary.items():
        print(k)
        case_res = []
        for name, ele in v.items():
            funcInfo = ele[2]
            for kv in funcInfo:
                for key, value in kv.items():
                    if str in key:
                        temp = []
                        temp.append(name)
                        temp.append(value)
                        case_res.append(temp)
                        break
        print(case_res)



# def AdjustResult(dictionary, factor):
    
#     return

# # 调整数据 按时间排序, 按max_grid_size排序 相同的max_grid_size 按时间排序
# AdjustResult(cases_res, "skip")



