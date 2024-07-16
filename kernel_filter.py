# 基础示例
#
# 欢迎使用CanMV IDE, 点击IDE左下角的绿色按钮开始执行脚本

import sensor, image, time, lcd

lcd.init()                          # 初始化屏幕显示
lcd.clear(lcd.RED)                  # 将屏幕清空，使用红色填充

sensor.reset()                      # 复位并初始化摄像头
sensor.set_pixformat(sensor.RGB565) # 设置摄像头输出格式为 RGB565（也可以是GRAYSCALE）
sensor.set_framesize(sensor.QVGA)   # 设置摄像头输出大小为 QVGA (320x240)
sensor.skip_frames(time = 2000)     # 跳过2000帧
clock = time.clock()                # 创建一个clock对象，用来计算帧率

while(True):
    clock.tick()                    # 更新计算帧率的clock
    img = sensor.snapshot()         # 拍照，获取一张图像
    lcd.display(img)                # 在屏幕上显示图像
    print(clock.fps())              # 注意，在IDE中预览图像会导致帧率降低
