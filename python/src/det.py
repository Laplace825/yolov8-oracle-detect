import cv2.dnn
import numpy as np
import os
import sys
from ultralytics import YOLO

# 类别
CLASSES = {0: "0"}
# 80个类别对应80中随机颜色
colors = np.random.uniform(0, 255, size=(len(CLASSES), 3))


# 绘制
def draw_bounding_box(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    label = f"{CLASSES[class_id]} ({confidence:.2f})"
    color = colors[class_id]
    # 绘制矩形框
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    # 绘制类别
    # cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


def det(onnx_model, input_image, output_image_dir):
    # 使用opencv读取onnx文件
    model: cv2.dnn.Net = cv2.dnn.readNetFromONNX(onnx_model)
    # 读取原图
    original_image: np.ndarray = cv2.imread(input_image)
    [height, width, _] = original_image.shape
    length = max((height, width))
    image = np.zeros((length, length, 3), np.uint8)
    image[0:height, 0:width] = original_image
    scale = length / 640  # 缩放比例
    # 设置模型输入
    blob = cv2.dnn.blobFromImage(
        image, scalefactor=1 / 255, size=(640, 640), swapRB=True
    )
    model.setInput(blob)
    # 推理
    outputs = model.forward()  # output: 1 X 8400 x 84
    outputs = np.array([cv2.transpose(outputs[0])])
    rows = outputs.shape[1]

    boxes = []
    scores = []
    class_ids = []
    # outputs有8400行，遍历每一行，筛选最优检测结果
    for i in range(rows):
        # 找到第i个候选目标在类别中，最可能的类别
        classes_scores = outputs[0][i][4:]  # classes_scores:80 X 1
        (minScore, maxScore, minClassLoc, (x, maxClassIndex)) = cv2.minMaxLoc(
            classes_scores
        )
        if maxScore >= 0.25:
            box = [
                # cx cy w h  -> x y w h
                outputs[0][i][0] - (0.5 * outputs[0][i][2]),
                outputs[0][i][1] - (0.5 * outputs[0][i][3]),
                outputs[0][i][2],
                outputs[0][i][3],
            ]
            boxes.append(box)  # 边界框
            scores.append(maxScore)  # 置信度
            class_ids.append(maxClassIndex)  # 类别
    # opencv版最极大值抑制
    result_boxes = cv2.dnn.NMSBoxes(boxes, scores, 0.25, 0.45, 0.5)

    for i in range(len(result_boxes)):
        index = result_boxes[i]
        box = boxes[index]
        # 将各个检测到的目标分割裁剪出来
        # 稍微扩大一下边界框，不然裁剪出来的目标会很小
        box[0] -= 0.1 * box[2]
        box[0] = 0 if box[0] < 0 else box[0]
        box[1] -= 0.1 * box[3]
        box[1] = 0 if box[1] < 0 else box[1]
        box[2] += 0.2 * box[2]
        box[3] += 0.2 * box[3]

        x, y, w, h = box
        x = round(x * scale)
        y = round(y * scale)
        w = round(w * scale)
        h = round(h * scale)
        crop = original_image[y : y + h, x : x + w]
        # 將crop 顏色反轉
        crop = cv2.bitwise_not(crop)
        # print(f"{output_image_dir}/{input_image.split('.')[0].split('/')[-1]}_{i}.jpg")
        # 保存裁剪出來的目标
        cv2.imwrite(
            f"{output_image_dir}/{input_image.split('.')[0].split('/')[-1]}_{i}.jpg",
            crop,
        )
        # # 绘制边界框
        # draw_bounding_box(original_image, class_ids[index], scores[index], round(box[0] * scale), round(box[1] * scale),
        #                   round((box[0] + box[2]) * scale), round((box[1] + box[3]) * scale))
    # cv2.imwrite(
    #     "/test/img.jpg", original_image
    # )


def det_yolo(pt_path, input_img_dir, output_img_dir):
    if pt_path.endswith(".onnx"):
        raise ValueError("pt_path must be a .pt file")
    model = YOLO(pt_path)
    for file in os.listdir(input_img_dir):
        if file.endswith(".jpg") or file.endswith(".png"):
            img_path = os.path.join(input_img_dir, file)
            result = model(img_path)
            i = 0
            for res in result:
                res.save_crop(
                    output_img_dir,
                    file_name=img_path.split("/")[-1].split(".")[0] + "_" + str(i),
                )
                i += 1

    # 将检测结果全部反色
    for file in os.listdir(f"{output_img_dir}/0"):
        if file.endswith(".jpg"):
            img_path = os.path.join(f"{output_img_dir}/0", file)
            img = cv2.imread(img_path)
            img = cv2.bitwise_not(img)
            cv2.imwrite(img_path, img)


if __name__ == "__main__":

    pass
