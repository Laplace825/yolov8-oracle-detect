#include <iostream>
#include <vector>
#include <opencv2/opencv.hpp>
#include <filesystem>
#include <fstream>
#include <format>
#include "inference.h"
using namespace std;

void det()
{
    bool runOnGPU = false; // 如果GPU跑结果不对,改用CPU跑试试

    // 1. 读取onnx模型
    // Note that in this example the classes are hard-coded and 'classes.txt' is a place holder.
    Inference inf("../best_det.onnx", cv::Size(640, 640), "classes.txt", runOnGPU); // classes.txt 可以缺失
    int padding = 15;                                                               // 用于扩大矩形框
    // 2. 读取输入图片路径下所有图片
    std::filesystem::path path = "../input_img";
    std::vector<std::string> imageNames;
    std::fstream file("../output_det.txt", std::ios::out); // 将结果写入 output.txt
    // 3. 遍历所有图片，进行推理

    for (auto &p : std::filesystem::directory_iterator(path))
    {
        imageNames.push_back(p.path().string());
    }

    for (int i = 0; i < imageNames.size(); ++i)
    {
        cv::Mat frame = cv::imread(imageNames[i]);

        // Inference starts here...
        std::vector<Detection> output = inf.runInference(frame);

        int detections = output.size();
        std::cout << "Number of detections:" << detections << std::endl;
        file << imageNames[i] << '\n';
        file << "Number of detections:" << detections << std::endl;

        // 若矩形框位置不对，下面这行可能需要
        // cv::resize(frame, frame, cv::Size(480, 640));

        for (int j = 0; j < detections; ++j)
        {
            Detection detection = output[j];

            cv::Rect box = detection.box;
            cv::Scalar color = detection.color;
            // 裁切图片,将识别到的文字保存到output_text_img文件夹
            cv::Rect largeBox(
                std::max(0, box.x - padding),
                std::max(0, box.y - padding),
                std::min(box.width + 2 * padding, frame.cols - std::max(0, box.x - padding)),
                std::min(box.height + 2 * padding, frame.rows - std::max(0, box.y - padding)));
            cv::Mat roi = frame(largeBox);
            cv::imwrite("../output_text_img/" + std::to_string(j) + "_" + imageNames[i].substr(imageNames[i].find_last_of("/") + 1), roi);

            // Detection box
            cv::rectangle(frame, box, color, 2);
            file << std::format("box.x:{} box.y:{} box.width:{} box.height:{}\n", box.x, box.y, box.width, box.height);
            std::cout << "frame:" << frame.cols << " " << frame.rows << std::endl;
            std::cout << "box:" << box.x << " " << box.y << " " << box.width << " " << box.height << std::endl;

            // Detection box text
            std::string classString = detection.className + ' ' + std::to_string(detection.confidence).substr(0, 4);
            cv::Size textSize = cv::getTextSize(classString, cv::FONT_HERSHEY_DUPLEX, 1, 2, 0);
            cv::Rect textBox(box.x, box.y - 40, textSize.width + 10, textSize.height + 20);

            cv::rectangle(frame, textBox, color, cv::FILLED);
            cv::putText(frame, classString, cv::Point(box.x + 5, box.y - 10), cv::FONT_HERSHEY_DUPLEX, 1, cv::Scalar(0, 0, 0), 2, 0);
        }
        cv::imwrite("../output_img/" + imageNames[i].substr(imageNames[i].find_last_of("/") + 1), frame);
    }
}
