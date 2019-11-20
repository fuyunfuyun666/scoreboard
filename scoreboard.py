from copy import deepcopy


def issue_transfer(
    id,clock,
    instructions,instruction_status_table,functional_status_table,register_status_table
    ):
    # 发射指令并更改寄存器状态、功能部件状态和指令状态，这里已经解除了WAW相关
    instruction_status_table[id][0]=clock # 发射的时间
    op=instructions[id][0] # 操作名称
    des=instructions[id][1] # 目标寄存器
    src1=instructions[id][2] # 源寄存器1
    src2=instructions[id][3] # 源寄存器2
    if op=='LD':#如果操作是load
        register_status_table[des]='Integer'#占用目标寄存器
        functional_status_table[0][0]=1
        functional_status_table[0][1]=op
        functional_status_table[0][2]=des
        functional_status_table[0][4]=src2
        if src2 not in register_status_table or register_status_table[src2]=='':#源寄存器空闲
            functional_status_table[0][8]='yes'
        else:#源寄存器不空闲
            functional_status_table[0][6]=register_status_table[src2]
            functional_status_table[0][8]="no"

    elif op=='MULT':# 如果操作是multiple
        if functional_status_table[1][0]==0:#乘法器有两个，找到空闲的一个
            register_status_table[des]='Mult1'#占用目标寄存器
            functional_status_table[1][0]=1
            functional_status_table[1][1]=op
            functional_status_table[1][2]=des
            functional_status_table[1][3]=src1
            functional_status_table[1][4]=src2
            if register_status_table[src1]=='':#源寄存器空闲
                functional_status_table[1][7]="yes"
            else:#源寄存器不空闲
                functional_status_table[1][5]=register_status_table[src1]
                functional_status_table[1][7]="no"
            if register_status_table[src2]=='':#源寄存器空闲
                functional_status_table[1][8]='yes'
            else:#源寄存器不空闲
                functional_status_table[1][6]=register_status_table[src2]
                functional_status_table[1][8]="no"
        else:
            register_status_table[des]='Mult2'#占用目标寄存器
            functional_status_table[2][0]=1
            functional_status_table[2][1]=op
            functional_status_table[2][2]=des
            functional_status_table[2][3]=src1
            functional_status_table[2][4]=src2
            if register_status_table[src1]=='':#源寄存器空闲
                functional_status_table[2][7]="yes"
            else:#源寄存器不空闲
                functional_status_table[2][5]=register_status_table[src1]
                functional_status_table[2][7]="no"
            if register_status_table[src2]=='':#源寄存器空闲
                functional_status_table[2][8]='yes'
            else:#源寄存器不空闲
                functional_status_table[2][6]=register_status_table[src2]
                functional_status_table[2][8]="no"
    elif op=='SUBD' or op=='ADDD':#如果操作是减法或者加法
        register_status_table[des]='Add'#占用目标寄存器
        functional_status_table[3][0]=1
        functional_status_table[3][1]=op
        functional_status_table[3][2]=des
        functional_status_table[3][3]=src1
        functional_status_table[3][4]=src2
        if register_status_table[src1]=='':#源寄存器空闲
            functional_status_table[3][7]="yes"
        else:#源寄存器不空闲
            functional_status_table[3][5]=register_status_table[src1]
            functional_status_table[3][7]="no"
        if register_status_table[src2]=='':#源寄存器空闲
            functional_status_table[3][8]='yes'
        else:#源寄存器不空闲
            functional_status_table[3][6]=register_status_table[src2]
            functional_status_table[3][8]="no"
    elif op=='DIVD':#如果操作是除法
        register_status_table[des]='Divide'#占用目标寄存器
        functional_status_table[4][0]=1
        functional_status_table[4][1]=op
        functional_status_table[4][2]=des
        functional_status_table[4][3]=src1
        functional_status_table[4][4]=src2
        if register_status_table[src1]=='':#源寄存器空闲
            functional_status_table[4][7]="yes"
        else:#源寄存器不空闲
            functional_status_table[4][5]=src1
            functional_status_table[4][7]="no"
        if register_status_table[src2]=='':#源寄存器空闲
            functional_status_table[4][8]='yes'
        else:#源寄存器不空闲
            functional_status_table[4][6]=src2
            functional_status_table[4][8]="no"


def update_src_state(
        unit, loc, functional_status_table, register_status_table
    ):#在读取之前更新源操作数的最新状态
    register=functional_status_table[unit][loc]
    if functional_status_table[unit][loc+4]=='yes':
        pass
    elif register_status_table[register]=='':
        functional_status_table[unit][loc+2]=''
        functional_status_table[unit][loc+4]='yes'


def read_transfer(
    id,clock,
    instructions,instruction_status_table,functional_status_table,register_status_table
    ):
    # 读取操作数，首先更新最新的源寄存器状态，如果源寄存器可用就直接读入，如果源寄存器不可用就不读入，解除RAW相关
    success=0
    op=instructions[id][0]
    des=instructions[id][1]
    src1=instructions[id][2]
    src2=instructions[id][3]
    if op=='LD':
        update_src_state(0, 4, functional_status_table, register_status_table)#在读取之前寻找源操作数的最新状态
        if functional_status_table[0][8]=='yes':#源操作数可用，那么就成功
            success=1

    elif op=='MULT':
        if functional_status_table[1][2]==des and  functional_status_table[1][3]==src1 and functional_status_table[1][4]==src2:
            update_src_state(1, 3, functional_status_table, register_status_table)#在读取之前寻找源操作数的最新状态
            update_src_state(1, 4, functional_status_table, register_status_table)
            if functional_status_table[1][7]=='yes' and functional_status_table[1][8]=='yes':#源操作数可用，那么就成功
                success=1
        else:
            update_src_state(2, 3, functional_status_table, register_status_table)#在读取之前寻找源操作数的最新状态
            update_src_state(2, 4, functional_status_table, register_status_table)
            if functional_status_table[2][7]=='yes' and functional_status_table[2][8]=='yes':#源操作数可用，那么就成功
                success=1
    elif op=='SUBD' or op=='ADDD':
        update_src_state(3, 3, functional_status_table, register_status_table)#在读取之前寻找源操作数的最新状态
        update_src_state(3, 4, functional_status_table, register_status_table)
        if functional_status_table[3][7]=='yes' and functional_status_table[3][8]=='yes':#源操作数可用，那么就成功
            success=1
    elif op=='DIVD':
        update_src_state(4, 3, functional_status_table, register_status_table)#在读取之前寻找源操作数的最新状态
        update_src_state(4, 4, functional_status_table, register_status_table)
        if functional_status_table[4][7]=='yes' and functional_status_table[4][8]=='yes':#源操作数可用，那么就成功
            success=1
    if success:
        instruction_status_table[id][1]=clock


def execution_transfer(
    id,clock,
    instructions,instruction_status_table,functional_status_table,register_status_table
    ):
    # 执行指令，指令需要的执行周期减一，直到执行周期为0时，执行完毕，更新指令状态表
    instructions[id][4]-=1
    if instructions[id][4]==0:
        instruction_status_table[id][2]=clock


def write_transfer(
    id,clock,
    instructions,instruction_status_table,functional_status_table,register_status_table,
    need_clear
    ):
    # 写回寄存器，再写回之前，需要保证没有WAR相关，也就是前面执行的指令已经读完该操作目的寄存器里面的内容了
    stall=0
    for i in range(id):
        if instructions[i][5]==1 and (instruction_status_table[i][1]==0 or instruction_status_table[i][1]==clock):# 如果前面执行的指令有没有读源操作数的，就可能有WAR相关
            if instructions[i][2]==instructions[id][1] or instructions[i][3]==instructions[id][1]:
                # 出现了WAR相关，那么就不能写回寄存器，需要stall
                # 注意，在本时钟周期前面指令读入的话，本周期不能写回
                stall=1
    if stall==0:
        instruction_status_table[id][3]=clock#写回
        instructions[id][5]=2#执行完毕
        need_clear.append(id)#需要清理的指令id


def scoreboard(instructions):
    """

    :return:
    """
    # 每条指令格式：list(op, des, src1, src2, clock, state)
    # state=0,1,2(not run,running,done)
    # clock指令执行所需的周期数
    instructions=instructions
    # instructions.append(['LD','F6','34','R2',1,0])
    # instructions.append(['LD','F2','45','R3',1,0])
    # instructions.append(['MULT','F0','F2','F4',10,0])
    # instructions.append(['SUBD','F8','F6','F2',2,0])
    # instructions.append(['DIVD','F10','F0','F6',40,0])
    # instructions.append(['ADDD','F6','F8','F2',2,0])

    # 指令状态表格式为一个矩阵，矩阵大小为：(指令条数,4)
    instruction_status_table=[[0 for _ in range(4)] for i in range(len(instructions))]

    # 功能部件状态表为一个list，每一行代表一个功能部件
    # 功能部件依次是Integer，Mult1，Mult2，Add，Divide
    functional_status_table=[
            [0,'','','','','','','',''], # Integer
            [0,'','','','','','','',''], # Mult1
            [0,'','','','','','','',''], # Mult2
            [0,'','','','','','','',''], # Add
            [0,'','','','','','','','']  # Divide
        ]

    # 寄存器状态表是一个list，长度为寄存器的个数
    register_status_table={
        'F0': '', 'F2': '', 'F4': '', 'F6': '', 'F8': '', 'F10': '', 'F12': '', 'F14': '',
        'F16': '', 'F18': '', 'F20': '', 'F22': '', 'F24': '', 'F26': '', 'F28': '', 'F30': ''
    }

    table1=[]
    table2=[]
    table3=[]

    clock=1
    finish_all_instructions=0
    while not finish_all_instructions:
        finish_all_instructions=1
        need_clear=[] # 需要清理的functional_status_table和register_status_table,但是这里不能清理，要等这个clock完了才能清理

        issue_id=0
        for instruction in instructions:#找到发射指令
            if instruction[5]==0:
                break
            else:
                issue_id+=1

        if issue_id<len(instructions):
            op=instructions[issue_id][0]
            des=instructions[issue_id][1]
            if op=='LD':
                #判断是否可以发射
                if not functional_status_table[0][0] and register_status_table[des]=='':
                    instructions[issue_id][5]=1
            elif op=='MULT':
                #判断是否可以发射
                if (not functional_status_table[1][0] or not functional_status_table[2][0]) \
                        and register_status_table[des]=='':
                    instructions[issue_id][5]=1
            elif op=='SUBD':
                #判断是否可以发射
                if not functional_status_table[3][0] and register_status_table[des]=='':
                    instructions[issue_id][5]=1
            elif op=='ADDD':
                #判断是否可以发射
                if not functional_status_table[3][0] and register_status_table[des]=='':
                    instructions[issue_id][5]=1
            elif op=='DIVD':
                #判断是否可以发射
                if not functional_status_table[4][0] and register_status_table[des]=='':
                    instructions[issue_id][5]=1


        running=0
        while running<len(instructions):#更新每个running指令的状态

            if instructions[running][5]==1:#如果指令在运行之中，那么进行状态转移
                if instruction_status_table[running][0]==0:#如果指令在发射状态
                    issue_transfer(
                        running,clock,instructions,
                        instruction_status_table,functional_status_table,
                        register_status_table
                    )

                elif instruction_status_table[running][1]==0:#如果指令在读取阶段
                    read_transfer(
                        running,clock,instructions,
                        instruction_status_table,functional_status_table,
                        register_status_table
                        )

                elif instruction_status_table[running][2]==0:#如果指令在执行阶段
                    execution_transfer(
                        running,clock,instructions,
                        instruction_status_table,functional_status_table,
                        register_status_table
                    )

                elif instruction_status_table[running][3]==0:#如果指令在写回阶段
                    write_transfer(
                        running,clock,instructions,
                        instruction_status_table,functional_status_table,
                        register_status_table,need_clear
                    )
            running+=1

        for i in need_clear: #清理已经执行完成的指令占用的资源，包括运算器的资源和寄存器的资源
            op=instructions[i][0]
            des=instructions[i][1]
            src1=instructions[i][2]
            src2=instructions[i][3]
            if op=='LD':
                functional_status_table[0]=[0,'','','','','','','','']
                register_status_table[des]=''
            elif op=='MULT':
                if functional_status_table[1][2]==des and  functional_status_table[1][3]==src1 and \
                        functional_status_table[1][4]==src2:
                    functional_status_table[1]=[0,'','','','','','','','']
                    register_status_table[des]=''
                else:
                    functional_status_table[2]=[0,'','','','','','','','']
                    register_status_table[des]=''
            elif op=='SUBD' or op=='ADDD':
                functional_status_table[3]=[0,'','','','','','','','']
                register_status_table[des]=''
            elif op=='DIVD':
                functional_status_table[4]=[0,'','','','','','','','']
                register_status_table[des]=''


        for i in instructions:
            if i[5]!=2:
                finish_all_instructions=0


        clock+=1
        # print(instruction_status_table)

        # 记录每个时间步的状态表
        table1.append(deepcopy(instruction_status_table))
        table2.append(deepcopy(functional_status_table))
        table3.append(deepcopy(register_status_table))
    return table1,table2,table3


if __name__=="__main__":
    t1,t2,t3=scoreboard()
    # print(t1[-1])
    # print(t2[-1])
    # print(t3[-1])
    for i in t1[-1]:
        print(i)