import sensor,image,lcd,time
import KPU as kpu
from fpioa_manager import fm
lcd.init(freq=15000000)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_hmirror(0)
sensor.set_vflip(1)

from machine import UART

fm.register(6 ,fm.fpioa.UART1_TX,force=True)
fm.register(7,fm.fpioa.UART1_RX,force=True)
uart_out = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)

clock = time.clock()
sensor.run(1)
task = kpu.load('/sd/yolov2.kmodel')
anchor = (2.125, 2.7091, 2.2779, 3.3098, 2.7672, 3.4039, 2.8779, 3.9336, 3.5185, 4.3338)
sensor.set_windowing((224,224))
a = kpu.init_yolo2(task,0.8,0.3,5,anchor)
lable = ["5", "1", "2", "3", "4", "6", "7", "8", "9"]

# 定义帧头和帧尾
frame_head = 0x0a  # 使用十六进制表示法定义帧头
frame_tail = 0x0b  # 使用十六进制表示法定义帧尾

#



# 组合完整的数据包（帧头 + 数据 + 帧尾）

# num1对应左边识别的
# num2对应右边识别的
# 没有就是0x00
def send_detect_pack(num1,num2):
    pack = bytearray([
    0x7b
    0x01,
    num1,
    num2,
    0x7d
    ])
    uart_out.write(pack)


while True:
    img = sensor.snapshot()
    clock.tick()
    code = kpu.run_yolo2(task,img)
    img.draw_string(0,0,"FPS:%.2f"%(clock.fps()),scale=2)
    if code:
        num1 = 0x00;
        num2 = 0x00;
        for i in code:
            a = img.draw_rectangle(i.rect(),(255, 255, 255),1,0)
            a = lcd.display(img)
            list1 = list(i.rect())
            b = (list1[0] + list1[2]) / 2
            c = (list1[1] + list1[3]) / 2
            print("物体是:",lable[i.classid()])
            print("概率为:",100.00*i.value())
            print("坐标为:",b,c)
            #看方框是在左边还是右边，这种写法能够直接克服nms不准确的问题

            if(b<224):
                num1 = lable[i.classid()]
            else:
                num2 = lable[i.classid()]
            for i in code:
                lcd.draw_string(i.x(),i.y(),lable[i.classid()],lcd.RED,lcd.WHITE)
                lcd.draw_string(i.x(),i.y()+12,'%f'%i.value(),lcd.RED,lcd.WHITE)

        send_detect_pack(num1,num2)
    else:
        #uart_out.write(packet)
        a = lcd.display(img)
a = kpu.deinit(task)
