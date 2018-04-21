#-*- coding:utf-8 -*-
from flask import Flask, render_template, Response,redirect,request,session
from camera import Camera #Import camera.py and create a class called 'Camera'
# from camera_test import Camera

app = Flask(__name__) #Create flask object called 'app' 对象
app.config['SECRET_KEY'] = '\xca\x0c\x86\x04\x98@\x02b\x1b7\x8c\x88]\x1b\xd7"+\xe6px@\xc3#\\'

cache = dict()

@app.route('/',methods=['GET', 'POST'])  #Build a main page route, the method which support it are'GET'and'POST'.
def hell_flask():
        return render_template('login.html')  #User open the main page, server get the request and return login.html


@app.route('/find',methods=['GET','POST'])
def find():
    f=open('1.txt','r')
    a=f.readline()
    a=str(a).split()
    f.close()
    if request.method=='POST':
        print request.form
        u=request.form['username']
        p=request.form['password']
        if a[0]==u and a[1]== p :
            session['username'] = request.form['username']
            cache[session['username']] = False
            return redirect('/show')
        else :
            return '<h3> Wrong user name or password! </h3>'

@app.route('/set', methods=['GET', 'POST'])
def set():
    user_name = session.get('username', '')
    if cache.get(user_name, False):
        cache[user_name] = False
    else:
        cache[user_name] = True
    return "success"

@app.route('/show',methods=['GET', 'POST'])
def index():
    user_name = session.get('username', '')
    save_status = cache.get(user_name, False)
    return render_template('index.html', save_status=save_status)
def gen(camera, user_name):#import Camera from camera
    while True:
        save_status = cache.get(user_name, False)
        frame = camera.get_frame(user_name, save_status) #frame is the picture data
        yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') #Confirm type of data: 'jpeg' 第一层处理，把数据冠上jpeg格式

# Tell leading-end the data is picture 从gen接受到的视频流返回前端
# mimtype,对于具有流式传输的，每个部分替换先前部分必须使用multipart/x-mixed-replace内容类型。

@app.route('/video_feed')#Display, return pictures to leading-end
def video_feed():
    user_name = session.get('username', '')
    return Response(gen(Camera(), user_name), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/reg',methods=['GET', 'POST'])
def xiugai1():
    return render_template('reg1.html')

@app.route('/xiugai',methods=['GET', 'POST'])
def genggai():
    if  request.method == 'POST':
        u=request.form['username']
        p=request.form['passwd']
        #print u,p
        f=open('1.txt','r')
        a=f.readline()
        a=str(a).split()
        f.close()
        s=str(u)+' '+str(p)#新的用户名 密码 加空格组成新的字符串
        print s
        if a[0]==str(u) and p!=None :#只修改密码 a[0] 是原来用户名
            with open('1.txt','w+') as f:
                f.write(s)
        else :
            return '<h3> Unmatched user name! </h3>'
        return redirect('/')
    else :
        return '<h3> Change password failed! </h3>'
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
