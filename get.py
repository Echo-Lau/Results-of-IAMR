import getResult
import os
import re
import glob


cases = [  "FlowPastCylinder", "LidDrivenCavity"] #  "Bubble" , ，"Bubble", "ConvectedVortex", "DoubleShearLayer",
cases_res = {}

for case in os.listdir(os.getcwd()):
    res = []
    types = ["case_results_cpu2d", "case_results_gpu2d"]
    for type in types:
        path = f"{case}/{type}"
        if os.path.exists(path):
            folders = os.listdir(path)
            for folder in folders:
                file_path = f"{case}/{type}/{folder}"
                # folder = cpu2d_skip0_Auto_mgs16_1_regrid8
                # name = folder[6:]
                case_res = getResult.Result()

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
                getResult.CheckInput(input_files[0],case_res)




# for case in cases:
#     print("###################################################################################################################")
#     print(f"-----------------------------------------    {case}     -------------------------------------------------")

#     # [Result, Result....., Result32]
#     res = getResult.CollectData(case)
    

#     # 原始数据
#     # print(len(res))
#     # getResult.Print(res)

#     # 按 cpu_time 排序
#     # getResult.AdjustResult(res, "cpu_time")
#     # print("cpu_time 排序")
#     # getResult.Print(res)
#     # # # gpu_time 排序
#     # getResult.AdjustResult(res, "gpu_time")
#     # print("gpu_time 排序")
#     # getResult.Print(res)
#     # # cycling 排序
#     # getResult.AdjustResult(res, "cycling")
#     # print("cycling 排序")
#     # getResult.Print(res)
    
#     getResult.CompareAndShow(res, "max_grid_size")
#     getResult.CompareAndShow(res, "max_grid_size", "gpu")
#     getResult.CompareAndShow(res, "cycling")
#     getResult.CompareAndShow(res, "cycling", "gpu")
#     getResult.CompareAndShow(res, "max_level")
#     getResult.CompareAndShow(res, "max_level", "gpu")
#     getResult.CompareAndShow(res, "regrid_int")
#     getResult.CompareAndShow(res, "regrid_int", "gpu")
#     getResult.CompareAndShow(res, "skip")
#     getResult.CompareAndShow(res, "skip", "gpu")
    
    
#     # getResult.TopFunc(res)

#     cases_res[case] = res






  




# 保存时间, step
# SaveToCsv(cases_res)


# 提取前十个最主要的函数
# TopFunc(res)

# 不同 case 的前十个函数的交集等


# 单个函数, 每个case的调用情况
# GetFuncOnEveryCase(res, "scalar_diffusion_update")


def PrintResult(dictionary):
    for case_res in dictionary.values():
        for res in case_res:
            print(f"{res.skip} {res.cycling} {res.max_level} {res.max_grid_size} {res.regrid_int} {res.cpu_time} {res.cpu_step} {res.gpu_time} {res.gpu_step}")
            # for i in range(len(res.function_name)):
            #     print(f"{res.function_name[i]} : {res.function_percent[i]}")
