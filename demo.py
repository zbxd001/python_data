import json
import numpy as np
import collections
import matplotlib.pyplot as plt
with open("test_data.json",'r',encoding='UTF-8') as load_f:
    load_dict = json.load(load_f)
    load_dict = load_dict.items()
    i = 0
    allData = {}
    varData = {}
    for key, value in load_dict:
        for data in value['cases']:
            case_id = data['case_id'] # 题号
            finalScore = data['final_score'] # 总分，有些总分是20或40的，需要处理转换为100分制的
            for vars in data['upload_records']:
                if finalScore!=0:
                    score = (float(vars['score'])/float(finalScore))*100 # 分数转化
                else:
                    score = float(vars['score'])
                if case_id in varData.keys():
                    varData[case_id][0]+=1
                    varData[case_id].append(score)
                else:
                    varData[case_id]=[1,score]
    varDict = {}
    avgData = {}
    standardScore = {}
    for avg in varData:
        if varData.get(avg)[0] != 0:
            da = np.array(varData[avg])
            sums = np.sum(da[1:])
            avgScore = sums / float(varData[avg][0])  # 计算平均分
            vars = np.var(da[1:])
            sizeAll = len(da[1:])
            sc = [x for x in da[1:] if x>=60]
            stand = (float(len(sc))/float(sizeAll))*100 # 为之后求相关系数准备
        else:
            avgScore = 0.0
            vars = 0.0
            stand = 0.0
        avgData[avg] = avgScore
        varDict[avg] = vars
        standardScore[avg] = stand

    sortData = sorted(avgData.items(), key=lambda x: x[1], reverse=False)
    sortVar = sorted(varDict.items(), key=lambda x: x[1], reverse=False)
    passData = sorted(standardScore.items(), key=lambda x: x[1], reverse=False)
    print("根据平均成绩看，题号%s的难度最高，题号%s的难度最低" % (sortData[0][0], sortData[-1][0]))
    print("平均成绩如下所示")
    print(sortData)
    print("----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("根据成绩方差看，题号%s的成绩分布最均匀，题号%s的成绩分布最不均匀" % (sortVar[0][0], sortVar[-1][0]))
    print("成绩方差如下所示")
    print(sortVar)
    print("----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("根据通过率看，题号%s的通过率最低，题号%s的通过率最高" % (passData[0][0], passData[-1][0]))
    print("通过率如下所示")
    print(passData)
    print("----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

# 计算相关系数
    avg = sorted(avgData.items(), key=lambda x: x[0], reverse=False)
    var = sorted(varDict.items(), key=lambda x: x[0], reverse=False)
    passS = sorted(standardScore.items(), key=lambda x: x[0], reverse=False)
    avg = collections.OrderedDict(avg) # 转为OrderedDict，之后转为list使得题号一一对应
    avg = list(avg.values())
    avgs = sorted([((x-np.min(avg))/(np.max(avg)-np.min(avg)))*100 for x in avg])
    var = collections.OrderedDict(var)
    var = list(var.values())
    vars = sorted([((x - np.min(var)) / (np.max(var) - np.min(var))) * 100 for x in var ])
    passS = collections.OrderedDict(passS)
    passS = list(passS.values())
    passSc = sorted([((x - np.min(passS)) / (np.max(passS) - np.min(passS))) * 100 for x in passS])
    x = range(1,883)
    print("平均分与方差之间的皮尔逊相关系数为: %f"%np.corrcoef(avg,var)[0,1])
    print("平均分与通过率之间的皮尔逊相关系数为: %f" % np.corrcoef(avg, passS)[0, 1])
    print("方差与通过率之间的皮尔逊相关系数为: %f" % np.corrcoef(var, passS)[0, 1])
    print()

    if np.corrcoef(avg,var)[0,1]> np.corrcoef(avg,passS)[0,1] :
        if np.corrcoef(avg,var)[0,1]> np.corrcoef(var,passS)[0,1]:
            print("可以看出：\n平均分与方差之间的皮尔逊相关系数的绝对值最接近1，所以平均数与方差决定的难度准确率最高。")
        else:
            print("可以看出：\n方差与通过率之间的皮尔逊相关系数的绝对值最接近1，所以方差与通过率决定的难度准确率最高。")
    else:
        if np.corrcoef(avg,passS)[0,1] > np.corrcoef(var, passS)[0, 1]:
            print("可以看出：\n平均分与通过率之间的皮尔逊相关系数的绝对值最接近1，所以平均数与通过率决定的难度准确率最高。")
        else:
            print("可以看出：\n方差与通过率之间的皮尔逊相关系数的绝对值最接近1，所以方差与通过率决定的难度准确率最高。")

    plt.subplot(221)
    plt.rcParams['font.family'] = ['sans-serif']
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.title("平均分与方差相关系数：-0.79 && 平均分与通过率相关系数:0.97\n方差与通过率之间的皮尔逊相关系数:-0.77")
    plt.plot(x,avgs,color = 'red',label='平均分')
    plt.plot(x,vars,color='blue',label='方差')
    plt.plot(x, passSc, color='black',label='通过率')
    plt.legend()
    plt.ylabel('难度')
    plt.xlabel('题号（对应题号请看Console输出）')


#平均分的散点图
    plt.subplot(222)
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.scatter(avg,avgs,c='k',marker='.')
    plt.title("平均分的散点图")
    plt.xlabel('题号（对应题号请看Console输出）')
    plt.ylabel('平均分')

 #方差的散点图
    plt.subplot(223)
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.scatter(var, vars, c='k', marker='.')
    plt.title("方差的散点图")
    plt.xlabel('题号（对应题号请看Console输出）')
    plt.ylabel('方差')

    # 通过率的散点图
    plt.subplot(224)
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.scatter(passS, passSc, c='k', marker='.')
    plt.title("通过率的散点图")
    plt.xlabel('题号（对应题号请看Console输出）')
    plt.ylabel('通过率')
    plt.show()

hard1=[]
medium1=[]
easy1=[]
for i in range(len(sortData)):
    if sortData[i][1]<=60:
        hard1.append(int(sortData[i][0]))
    elif sortData[i][1]>=80:
        easy1.append(int(sortData[i][0]))
    else:
        medium1.append(int(sortData[i][0]))

hard2=[]
medium2=[]
easy2=[]

for j in range(len(passData)):
    if passData[j][1]<=60:
        hard2.append(int(passData[j][0]))
    elif passData[j][1]>=80:
        easy2.append(int(passData[j][0]))
    else:
        medium2.append(int(passData[j][0]))

hard=[]
medium=[]
easy=[]
for k in range(len(hard1)):
    if hard1[k] in hard2:
        hard.append(hard1[k])
    else:
        for m in range(len(sortVar)):
            if hard1[k]==int(sortVar[m][0]):
                if sortVar[m][1]<=500:
                    easy.append(hard1[k])
                elif sortVar[m][1]>2000:
                    hard.append(hard1[k])
                else:
                    medium.append(hard1[k])

for p in range(len(medium1)):
    if medium1[p] in medium2:
        medium.append(medium1[p])
    else:
        for m in range(len(sortVar)):
            if medium1[p]==int(sortVar[m][0]):
                if sortVar[m][1]<=500:
                    easy.append(medium1[p])
                elif sortVar[m][1]>2000:
                    hard.append(medium1[p])
                else:
                    medium.append(medium1[p])


for q in range(len(easy1)):
    if easy1[q] in easy2:
        easy.append(easy1[q])
    else:
        for m in range(len(sortVar)):
            if easy1[q]==int(sortVar[m][0]):
                if sortVar[m][1]<=500:
                    easy.append(easy1[q])
                elif sortVar[m][1]>2000:
                    hard.append(easy1[q])
                else:
                    medium.append(easy1[q])

print("——————————最终难度定为3个层次，分别为hard，medium，easy——————————\n")
print("hard : ")
print(sorted(hard))
print("_______________________________________________________________________________________________________________________________________________________________________________________________________________")
print("medium : ")
print(sorted(medium))
print("___________________________________________________________________________________________________________________________________________________________________________________________")
print("easy : ")
print(sorted(easy))