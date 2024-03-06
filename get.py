import getResult


cases = ["Bubble", "DoubleShearLayer"] #  , "LidDrivenCavity", "FlowPastCylinder"，"Bubble", "ConvectedVortex"

cases_res = {}

for case in cases:
    print("###################################################################################################################")
    print(f"-----------------------------------------    {case}     -------------------------------------------------")


    res = getResult.CollectData(case)
    
    # 原始数据
    # print(len(res))
    # getResult.Print(res)

    # 按 cpu_time 排序
    getResult.AdjustResult(res, "cpu_time")
    print("cpu_time 排序")
    getResult.Print(res)
    # gpu_time 排序
    getResult.AdjustResult(res, "gpu_time")
    print("gpu_time 排序")
    getResult.Print(res)
    # # max_grid_size 排序
    # getResult.AdjustResult(res, "max_grid_size")
    # print("max_grid_size 排序")
    # getResult.Print(res)

    # getResult.CompareAndShow(res, "max_grid_size")
    # getResult.CompareAndShow(res, "cycling")
    # getResult.CompareAndShow(res, "max_level")
    # getResult.CompareAndShow(res, "regrid_int")
    # getResult.CompareAndShow(res, "skip")
    
    
    # getResult.TopFunc(res)

    cases_res[case] = res






  




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
