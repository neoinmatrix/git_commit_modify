import os
import shutil
import sys

def create( user):
    raw_path, new_path = user["raw_path"], user["new_path"]
    cmd="#!/bin/bash \n"
    cmd+=f"rm -rf {new_path} \n"
    cmd+=f"mkdir {new_path} \n"
    cmd+=f"cd {new_path} \n"
    cmd+="git init \n"
    cmd+=f"git config user.name \"{user['name']}\" \n"
    cmd+=f"git config user.email \"{user['email']}\" \n"
    if user["gitpush"]:
        cmd+=f"git remote add origin {user['gitremote']} \n"
    
    if user["localtime_modify"]:
        cmd+=f"sudo timedatectl set-ntp false  # 关闭自动更新时间 \n"

    dateinfo=open(user['tmp_path'],"r").readlines()
    for line in dateinfo[::-1]:
        cols=line.split(" ")
        hcode,ctime,cminfo=cols[0],cols[1]," ".join(cols[2:])
        cminfo=cminfo.replace("\n","")
        # print(hcode,ctime,cminfo)
        if user["localtime_modify"]:
            cmd+=f"sudo date --set=\"{ctime}\" \n"
        cmd+=f"cd {raw_path} \n"
        cmd+=f"git checkout {hcode} \n"
        cmd_now=f"git checkout {hcode}"
        os.chdir(raw_path)
        os.system(cmd_now)
        # checkout 到点之后 处理文件
        dirs=[f for f in os.listdir(raw_path) if ".git" not in f]
        for d in dirs:
            cmd+=f"cp -r {raw_path}/{d} {new_path} \n"
            
        cmd+=f"cd {new_path} \n"
        cmd+="git add . \n"
        cmd+=f"git commit -m \"{cminfo}\" --date=\"{ctime}\" \n"
        if user["gitpush"]:
            cmd+=f"git push origin master \n"
            
    if user["localtime_modify"]:
        cmd+=f"sudo timedatectl set-ntp true  # 关闭自动更新时间 \n"
    return cmd
    
    
def main():
    root="./"
    root=os.path.abspath(root)
    user={
        "raw_path":os.path.join(root,"raw"),        # 原始的项目的git
        "new_path":os.path.join(root,"new"),        # 全新的项目的git
        "tmp_path":os.path.join(root,"git.log"),    # 需要修改的commit time & message
        "cmd_path":os.path.join(root,"cmd.sh"),     # False 不设置 本地时间
        "name": "demo",                             # 新项目的用户名
        "email":"demo@demo.com",                    # 新项目的邮箱
        "gitremote":"git@demo.com:demo/demoproj.git",  #为空是不提交
        "gitpush": False,                           # False 不push
        "localtime_modify": False,                  # False 不设置 本地时间
    }
    if len(sys.argv)==1:
        cmd=create(user)
        open(user["cmd_path"],"w").write(cmd)
        print("create cmd.sh is ok")
    else:
        raw_path,tmp_path=user["raw_path"],user["tmp_path"]
        if os.path.exists(raw_path)==False:
            print("not existed of raw proj")
        cmd_tmp=f"cd {raw_path} && git log --pretty='format:%H %cI %s' > {tmp_path} "
        os.system(cmd_tmp) 
        print("create git.log is ok")
   

if __name__ == '__main__':
    main()
    
