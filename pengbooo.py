import sys
import os
import shutil



# 获取参数
args = sys.argv[1:]


# 开头空行
print()

# ---------------------------- 分界线 ---------------------------- #

# 定义函数区


def check_args_len(need):
    # 确认参数项数是否达到要求

    if len(args) >= need:
        return True

    return False


def log_reporter(log_type, log, running=False, line=None, is_c_project=False):
    if log_type == 'info':
        print('[INFO]: ' + log)

    elif log_type == 'warning':
        print('[WARNING]: ' + log)

    elif log_type == 'error':
        if running:
            if is_c_project == '返回的程序':
                print('[ERROR]: 在dlc返回的程序中，在第' + str(line) + '行，' + log)

            elif is_c_project:
                print('[ERROR]: 在从程序中，在第' + str(line) + '行，' + log)

            else:
                print('[ERROR]: 在第' + str(line) + '行，' + log)
        else:
            print('[ERROR]: ' + log)

        # 报错 --> 停止
        stop(1)

def stop(static):
    # 停止函数
    sys.exit(static)


def remove_dir(path):
    # 删除文件夹函数
    shutil.rmtree(path)


def check_air(text):
    # 判断是否是空格或空文字
    check = True
    for i in text:
        if i != ' ':
            check = False

    return check

def del_air(l):
    # 去除换行

    c = 0

    for i in l:
        l[c] = i.replace('\n', '')

        c += 1

    return l


def cut(text, a, b=None):
    # 字符串切片

    if b == None:
        b = a + 1

    return text[a: b]


def run_project(main_project, v_d, j_d, j_d_run, project_name, is_c_project=False, dlc_list=[]):
    # 运行项目函数

    count_line = 1

    # 遍历每一行
    while count_line <= len(main_project):

        line = main_project[count_line - 1]


        # 首先排除注释
        if cut(line, 0) == '#':
            pass


        # 排除空行
        elif check_air(line):
            count_line += 1

            # 判定是否在节点内
            if j_d_run != []:
                # 在节点内
                if (count_line - 1) >= j_d[j_d_run[-1][0]][1]:
                    # 结束节点运行
                    count_line = j_d_run[-1][1]
                    j_d_run.pop(-1)
            continue


        # 关键词“输出”，作用：输出一个字符串（print）
        elif cut(line, 0, 2) == '输出':

            # 从关键词“变量”，输出变量的值
            if cut(line, 2, 4) == '变量':

                if check_air(cut(line, 4)):
                    # 见报错信息
                    log_reporter('error', '使用输出变量时没有输入要输出的变量名', True, count_line, is_c_project)

                a = 4

                # 排除特殊情况
                if cut(line, 4) == ':' or cut(line, 4) == ' ' or cut(line, 4) == '：':
                    a += 1
                    if cut(line, 4) == ':' and cut(line, 5) == ' ':
                        a += 1

                v_name = line[a:]
                if v_name in v_d:
                    print(v_d[v_name])
                else:
                    # 变量不在变量列表中，未定义
                    log_reporter('error', '变量“' + v_name + '”未定义', True, count_line, is_c_project)

            else:
                a = 2
                # 排除特殊情况
                if cut(line, 2) == ':' or cut(line, 2) == ' ' or cut(line, 2) == '：':
                    a += 1
                    if cut(line, 2) == ':' and cut(line, 3) == ' ':
                        a += 1

                print(line[a:])


        # 关键词“将……定义为”，作用：定义（=）
        elif cut(line, 0) == '将':
            new_line = line[1:].replace(' ', '').split('定义为')

            # 报错处理
            if len(new_line) == 1:
                # 没有关键字
                log_reporter('error', '缺少关键字：定义为', True, count_line, is_c_project)

            if check_air(new_line[0]):
                # 缺少参数
                log_reporter('error', '在定义时没有被定义的变量名', True, count_line, is_c_project)

            if check_air(new_line[1]) == '':
                # 缺少参数
                log_reporter('error', '在定义时没有用来定义变量的值', True, count_line, is_c_project)

            if new_line[0][0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                # 变量名不合法
                log_reporter('error', '变量名“' + new_line[0] + '”不合法', True, count_line, is_c_project)


            # 开始定义

            if new_line[0] in v_d:
                # 在变量列表里，修改变量的值
                v_d[new_line[0]] = new_line[1]

            else:
                # 不在变量列表里，创建新变量
                v_d.update({new_line[0]: new_line[1]})


        # 关键词“新建函数”或“创建函数”，作用：建立函数（def）
        elif cut(line, 0, 4) == '新建函数' or cut(line, 0, 4) == '创建函数':
            a = 4

            if cut(line, 4) == ':' or cut(line, 4) == ' ' or cut(line, 4) == '：':
                a += 1
                if cut(line, 4) == ':' and cut(line, 5) == ' ':
                    a += 1

            new_line = line[a:]

            if check_air(new_line):
                # 没有函数名
                log_reporter('error', '新建函数时没有函数的标签', True, count_line, is_c_project)

            n_c_l = count_line

            a = True

            while a:
                if n_c_l >= len(main_project):
                    # 说明没有新建节点的结束，报错
                    log_reporter('error', '新建函数时没有结束函数的新建', True, count_line, is_c_project)

                elif main_project[n_c_l] == '结束函数的新建' or main_project[n_c_l] == '函数创建结束' or main_project[n_c_l] == '函数新建结束' or main_project[n_c_l] == '结束函数的创建':
                    # 结束函数新建
                    n_c_l -= 1

                    a = False

                else:
                    n_c_l += 1

            j_d.update({new_line: [count_line, n_c_l + 1]})

            count_line = n_c_l + 2

        # 关键词“运行函数”，作用：运行已经建立的函数
        elif cut(line, 0, 4) == '运行函数':
            # 排除特殊情况
            a = 4

            if cut(line, 4) == ':' or cut(line, 4) == ' ' or cut(line, 4) == '：':
                a += 1
                if cut(line, 4) == ':' and cut(line, 5) == ' ':
                    a += 1

            new_line = line[a:]

            if check_air(new_line):
                # 没有函数名
                log_reporter('error', '运行函数时没有函数的标签', True, count_line, is_c_project)

            if not new_line in j_d:
                # 函数没有定义
                log_reporter('error', '函数“' + new_line + '”未被定义', True, count_line, is_c_project)


            j_d_run.append([new_line, count_line + 1])
            count_line = j_d[new_line][0]


        # 关键词“复制变量”，作用：运行已经建立的节点
        elif cut(line, 0, 4) == '复制变量':
            # 排除特殊情况
            a = 4

            if cut(line, 4) == ':' or cut(line, 4) == ' ' or cut(line, 4) == '：':
                a += 1
                if cut(line, 4) == ':' and cut(line, 5) == ' ':
                    a += 1

            new_line = line[a:]

            if check_air(new_line):
                log_reporter('error', '复制变量时没有传入参数', True, count_line, is_c_project)

            if '到' in new_line:
                new_line = new_line.split('到')

            elif '去' in new_line:
                new_line = new_line.split('去')

            elif '-->' in new_line:
                new_line = new_line.split('-->')

            else:
                log_reporter('error', '复制变量时没有指定的关键字，如：到、去、-->', True, count_line, is_c_project)


            # 判断变量是否定义
            if new_line[0] in v_d:
                if check_air(new_line[1]):
                    log_reporter('error', '复制变量时需要被复制的变量没有传入', True, count_line, is_c_project)
                if new_line[1] in v_d:
                    v_d[new_line[1]] = v_d[new_line[0]]
                else:
                    v_d.update({new_line[1]: v_d[new_line[0]]})

            else:
                # 报错
                log_reporter('error', '复制变量时需要复制的变量没有被定义', True, count_line, is_c_project)


        # 关键词“如果”，作用：判断正确就执行函数
        elif cut(line, 0, 2) == '如果':
            # 排除特殊情况
            a = 2

            if cut(line, 2) == ':' or cut(line, 2) == ' ' or cut(line, 2) == '：':
                a += 1
                if cut(line, 2) == ':' and cut(line, 3) == ' ':
                    a += 1

            new_line = line[a:]

            # 没有“那么运行”关键字
            if not '那么运行' in new_line:
                # 报错
                log_reporter('error', '使用如果语句时没有包含指定关键字', True, count_line, is_c_project)

            n = new_line
            n = n.split('那么运行')
            name = n[1]
            new_line = new_line[:0 - (len(name) + 4)]

            # 没有给出指定参数
            if check_air(name):
                # 报错
                log_reporter('error', '使用如果语句时没有给出指定参数', True, count_line, is_c_project)

            # 没有定义的函数
            if not name in j_d:
                # 报错
                log_reporter('error', '使用如果语句时给出的函数没有被定义', True, count_line, is_c_project)

            new_line = new_line.replace(' ', '')

            if '==' in new_line:
                # 等于
                new_line = new_line.split('==')

                if len(new_line) < 2 or check_air(new_line[0]) or check_air(new_line[1]):
                    # 报错
                    log_reporter('error', '使用如果语句时没有给出指定参数', True, count_line, is_c_project)

                # 判断变量是否被定义
                if not new_line[0] in v_d or not new_line[1] in v_d:
                    # 报错
                    log_reporter('error', '使用如果语句时给出的变量没有被定义', True, count_line, is_c_project)

                # 执行判断
                if v_d[new_line[0]] == v_d[new_line[1]]:
                    # 运行函数
                    j_d_run.append([name, count_line + 1])
                    count_line = j_d[name][0]



            elif '=' in new_line:
                # 等于
                new_line = new_line.split('=')
                if len(new_line) < 2 or check_air(new_line[0]) or check_air(new_line[1]):
                    # 报错
                    log_reporter('error', '使用如果语句时没有给出指定参数', True, count_line, is_c_project)

                # 判断变量是否被定义
                if not new_line[0] in v_d or not new_line[1] in v_d:
                    # 报错
                    log_reporter('error', '使用如果语句时给出的变量没有被定义', True, count_line, is_c_project)

                # 执行判断
                if v_d[new_line[0]] == v_d[new_line[1]]:
                    # 运行函数
                    j_d_run.append([name, count_line + 1])
                    count_line = j_d[name][0]


            elif '<' in new_line:
                # 小于
                new_line = new_line.split('<')
                if len(new_line) < 2 or check_air(new_line[0]) or check_air(new_line[1]):
                    # 报错
                    log_reporter('error', '使用如果语句时没有给出指定参数', True, count_line, is_c_project)

                # 判断变量是否被定义
                if not new_line[0] in v_d or not new_line[1] in v_d:
                    # 报错
                    log_reporter('error', '使用如果语句时给出的变量没有被定义', True, count_line, is_c_project)


                # 判断是否为数字
                a = True
                for i in v_d[new_line[0]]:
                    if not i in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                        a = False

                b = True
                for i in v_d[new_line[1]]:
                    if not i in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                        b = False

                if a == False and b == False:
                    # 报错
                    log_reporter('error', '使用如果语句时变量值不为数字', True, count_line, is_c_project)


                # 执行判断
                if v_d[new_line[0]] < v_d[new_line[1]]:
                    # 运行函数
                    j_d_run.append([name, count_line + 1])
                    count_line = j_d[name][0]

            elif '>' in new_line:
                # 大于
                new_line = new_line.split('>')
                if len(new_line) < 2 or check_air(new_line[0]) or check_air(new_line[1]):
                    # 报错
                    log_reporter('error', '使用如果语句时没有给出指定参数', True, count_line, is_c_project)

                # 判断变量是否被定义
                if not new_line[0] in v_d or not new_line[1] in v_d:
                    # 报错
                    log_reporter('error', '使用如果语句时给出的变量没有被定义', True, count_line, is_c_project)

                # 判断是否为数字
                a = True
                for i in v_d[new_line[0]]:
                    if not i in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                        a = False

                b = True
                for i in v_d[new_line[0]]:
                    if not i in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                        b = False

                if a == False and b == False:
                    # 报错
                    log_reporter('error', '使用如果语句时变量值不为数字', True, count_line, is_c_project)


                # 执行判断
                if v_d[new_line[0]] > v_d[new_line[1]]:
                    # 运行函数
                    j_d_run.append([name, count_line + 1])
                    count_line = j_d[name][0]

            else:
                # 没有运行指示符
                log_reporter('error', '在运行如果语句时没有运行指示符', True, count_line, is_c_project)


        # 关键词“运行从程序”，作用：运行从程序文件（_exec）
        elif cut(line, 0, 5) == '运行从程序':
            # 排除特殊情况
            a = 5

            if cut(line, 5) == ':' or cut(line, 5) == ' ' or cut(line, 5) == '：':
                a += 1
                if cut(line, 5) == ':' and cut(line, 6) == ' ':
                    a += 1

            new_line = line[a:]

            if new_line[-3:] != '.pb':
                new_line += '.pb'

            if check_air(new_line):
                # 没有提供从程序名称
                log_reporter('error', '在运行从程序时没有提供从程序名称', True, count_line, is_c_project)

            elif not new_line in os.listdir(project_name + '/从程序'):
                # 没有这个从程序
                log_reporter('error', '在运行从程序时提供的从程序没有在从程序文件夹中', True, count_line, is_c_project)

            c_project = del_air(open(project_name + '/从程序/' + new_line, 'r', encoding='utf-8').readlines())

            run_project(c_project, v_d, j_d, [], project_name, True)


        # 关键词“运行dlc”，作用：运行dlc（_exec）
        elif cut(line, 0, 5) == '运行dlc':
            # 排除特殊情况
            a = 5

            if cut(line, 5) == ':' or cut(line, 5) == ' ' or cut(line, 5) == '：':
                a += 1
                if cut(line, 5) == ':' and cut(line, 6) == ' ':
                    a += 1

            new_line = line[a:]

            if not '中的' in new_line:
                # 没有关键词
                log_reporter('error', '运行dlc时没有关键词', True, count_line, is_c_project)

            new_line = new_line.split('中的')

            if check_air(new_line[0]):
                # 未提供dlc名称
                log_reporter('error', '运行dlc时未提供dlc名称', True, count_line, is_c_project)

            if check_air(new_line[1]):
                # 未提供dlc参数
                log_reporter('error', '运行dlc时未提供dlc参数', True, count_line, is_c_project)


            d = []
            for i in dlc_list:
                d.append(i.replace('\n', ''))

            if not new_line[0] in dlc_list:
                # 没有装载的dlc
                log_reporter('error', '没有装载的dlc“' + new_line[0] + '”', True, count_line, is_c_project)

            # 清空返回的程序
            if 'return.pb' in os.listdir():
                os.remove('return.pb')

            # 运行dlc
            if os.system('python ' + dlc_d + 'dlc/' + new_line[0] + '/main.py ' + new_line[1]) != 0:
                # dlc运行出错
                log_reporter('warning', 'dlc“' + new_line[0] + '”运行出错', True, count_line, is_c_project)

            else:
                if 'return.pb' in os.listdir():
                    # 运行返回的程序
                    c_project = del_air(open('return.pb', 'r').readlines())

                    run_project(c_project, v_d, j_d, [], project_name, '返回的程序')

                    os.remove('return.pb')


        # 关键词“把命令行输入保存到”，作用：将命令行输入保存到变量里（input）
        elif cut(line, 0, 9) == '把命令行输入保存到':
            # 排除特殊情况
            a = 9

            if cut(line, 9) == ':' or cut(line, 9) == ' ' or cut(line, 9) == '：':
                a += 1
                if cut(line, 9) == ':' and cut(line, 10) == ' ':
                    a += 1

            new_line = line[a:]

            if '设置提示词' in new_line:
                # 排除特殊情况
                a = 1

                if cut(line, 1) == ':' or cut(line, 1) == ' ' or cut(line, 1) == '：':
                    a += 1
                    if cut(line, 1) == ':' and cut(line, 2) == ' ':
                        a += 1

                new_line = new_line.split('设置提示词')
                new_line[1] = new_line[1][a:]

            elif '设定提示词' in new_line:
                # 排除特殊情况
                a = 1

                if cut(line, 1) == ':' or cut(line, 1) == ' ' or cut(line, 1) == '：':
                    a += 1
                    if cut(line, 1) == ':' and cut(line, 2) == ' ':
                        a += 1

                new_line = new_line.split('设定提示词')
                new_line[1] = new_line[1][a:]

            else:
                new_line = [new_line, '']

            if check_air(new_line):
                # 没有提供需要保存到的变量名
                log_reporter('error', '使用输入时没有提供需要保存到的变量名', True, count_line, is_c_project)

            a = input(new_line[1])

            if new_line[0] in v_d:
                v_d[new_line[0]] = a

            else:
                v_d.update({new_line[0], a})








        else:
            log_reporter('error', '未知的语句“' + line + '”', True, count_line, is_c_project)




        # 将行数增加1
        count_line += 1

        # 判定是否在节点内
        if j_d_run != []:
            # 在节点内
            if (count_line - 1) >= j_d[j_d_run[-1][0]][1]:
                # 结束节点运行
                count_line = j_d_run[-1][1]
                j_d_run.pop(-1)




# ---------------------------- 分界线 ---------------------------- #


# 获取绝对路径
dlc_d = __file__[:-11]

# 判断是否存在dlc文件夹（没有则创建）
if not 'dlc' in os.listdir(dlc_d):
    os.mkdir(dlc_d + '/dlc')


if len(args) == 0:
    # 没有参数
    print("""
        PengBooo编程语言
  _____                 ____                    
 |  __ \               |  _ \                   
 | |__) |__ _ __   __ _| |_) | ___   ___   ___  
 |  ___/ _ \ '_ \ / _` |  _ < / _ \ / _ \ / _ \ 
 | |  |  __/ | | | (_| | |_) | (_) | (_) | (_) |
 |_|   \___|_| |_|\__, |____/ \___/ \___/ \___/ 
                   __/ |                        
                  |___/                         
    
版本：1.0.0chinese中文版
向着自己的目标前进，将不可能变为可能 
作者：PengBo
网页链接：https://pengbooo.com
""")

else:
    if args[0] == 'new':
        if check_args_len(2):
            # 满足创建新项目的参数要求
            log_reporter('info', '创建新项目“' + args[1] + '”')
            if args[1] in os.listdir():
                # 见报错信息（^ ^)
                log_reporter('error', '该项目已在当前文件夹内存在')
                # 这里报错后直接结束，所以不会往下执行，以后就不注释了。

            log_reporter('info', '创建文件夹“' + args[1] + '”')

            os.mkdir(args[1])

            log_reporter('info', '创建文件夹“' + args[1] + '”完成')

            log_reporter('info', '创建主程序“' + args[1] + '”')

            open(args[1] + '/主程序.pb', 'w', encoding='utf-8').write('# 在这里写程序\n')

            log_reporter('info', '创建主程序“' + args[1] + '”完成')

            log_reporter('info', '创建dlc列表文件“' + args[1] + '”')

            open(args[1] + '/dlc.txt', 'w', encoding='utf-8')

            log_reporter('info', '创建dlc列表文件“' + args[1] + '”完成')

            log_reporter('info', '创建从程序文件夹“' + args[1] + '”')

            os.mkdir(args[1] + '/从程序')

            log_reporter('info', '创建从程序文件夹“' + args[1] + '”完成')

            log_reporter('info', '创建项目“' + args[1] + '”完成')

        else:
            # 报错
            log_reporter('error', '需要填写项目名才能创建新项目')

    elif args[0] == 'del':
        # 删除项目
        if check_args_len(2):
            log_reporter('info', '删除项目“' + args[1] + '”')

            remove_dir(args[1])

            log_reporter('info', '删除项目“' + args[1] + '”完成')
        else:
            # 没有项目名
            log_reporter('error', '需要填写项目名才能删除项目')

    elif args[0] == 'run':
        if check_args_len(2):
            # 至少需要两个参数才能启动

            if args[1] in os.listdir():
                # 需要保证目录完整
                l = os.listdir(args[1])
                if 'dlc.txt' in l and '主程序.pb' in l and '从程序' in l:
                    name = args[1]

                    # 输出信息
                    log_reporter('info', '读取dlc列表文件')

                    # 空行
                    print()

                    # 检录需要用到的dlc
                    can_use_dlc_list = os.listdir(dlc_d + 'dlc')

                    for i in open(name + '/dlc.txt', 'r').readlines():
                        i = i.replace('\n', '')

                        if not check_air(i):
                            if not i in os.listdir(dlc_d + 'dlc'):
                                log_reporter('error', 'dlc“' + i + '”未被安装')


                    log_reporter('info', '运行项目“' + name + '”')

                    # 空行
                    print()

                    # 读取主程序
                    main_project = del_air(open(name + '/主程序.pb', 'r', encoding='utf-8').readlines())

                    run_project(main_project, {}, {}, [], name, dlc_list=open(name + '/dlc.txt', 'r').readlines())
                else:
                    log_reporter('error', '此项目似乎并不完整或不是一个PengBooo（pb）项目，请检查项目')
            else:
                # 需要存在于当前目录中
                log_reporter('error', '此项目似乎并不存在于这个目录中，请检查项目名与目录是否错误')

        else:
            # 缺少项目名称
            log_reporter('error', '需要填写项目名才能运行项目')


    elif args[0] == 'dlc':
        if len(args) < 2:
            # 缺少dlc命令
            log_reporter('error', '缺少dlc编辑命令')

        if args[1] == 'list':
            if os.listdir(dlc_d + 'dlc') == []:
                log_reporter('info', '您还未安装dlc')
            for i in os.listdir(dlc_d + 'dlc'):
                print(i)

        elif args[1] == 'del':
            if len(args) < 3:
                # 缺少dlc名
                log_reporter('error', '缺少需要删除的dlc名称')

            if args[2] in os.listdir(dlc_d + 'dlc'):
                log_reporter('info', '删除dlc“' + args[2] + '”')
                shutil.rmtree(dlc_d + 'dlc/' + args[2])
                log_reporter('info', '删除dlc“' + args[2] + '”完毕')
            else:
                # 没有安装的dlc
                log_reporter('error', 'dlc“' + args[2] + '”没有安装')

        else:
            # 未知的dlc命令
            log_reporter('error', '未知的dlc命令“' + args[1] + '”')


    else:
        # 未知的命令，报错处理
        log_reporter('error', '未知的命令“' + args[0] + '”')

