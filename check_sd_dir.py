import sensor,image,lcd,time
import KPU as kpu
from fpioa_manager import fm
lcd.init(freq=15000000)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_hmirror(1)
sensor.set_vflip(1)
clock = time.clock()
sensor.run(1)

#f=open("test.txt","r")
task = kpu.load('/sd/yolov2.kmodel')
anchor = (2.125, 2.7091, 2.2779, 3.3098, 2.7672, 3.4039, 2.8779, 3.9336, 3.5185, 4.3338)
sensor.set_windowing((224,224))
a = kpu.init_yolo2(task,0.8,0.3,5,anchor)
lable = ["5", "1", "2", "3", "4", "6", "7", "8", "9"]
while True:
    img = sensor.snapshot()
    clock.tick()
    code = kpu.run_yolo2(task,img)
    img.draw_string(0,0,"FPS:%.2f"%(clock.fps()),scale=2)
    if code:
        for i in code:
            a = img.draw_rectangle(i.rect(),(255, 255, 255),1,0)
            a = lcd.display(img)
            list1 = list(i.rect())
            b = (list1[0] + list1[2]) / 2
            c = (list1[1] + list1[3]) / 2
            print("物体是:",lable[i.classid()])
            print("概率为:",100.00*i.value())
            print("坐标为:",b,c)
            for i in code:
                lcd.draw_string(i.x(),i.y(),lable[i.classid()],lcd.RED,lcd.WHITE)
                lcd.draw_string(i.x(),i.y()+12,'%f'%i.value(),lcd.RED,lcd.WHITE)
    else:
        a = lcd.display(img)
a = kpu.deinit(task)
