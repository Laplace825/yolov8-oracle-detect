#include <iostream>
#include <vector>
#include <opencv2/opencv.hpp>
#include "inference.h"
#include <fstream>
#include <filesystem>
#include <string>

using namespace std;
using namespace cv;

int main(int argc, char **argv)
{
    bool runOnGPU = true;

    // 1. 设置你的onnx模型
    // Note that in this example the classes are hard-coded and 'classes.txt' is a place holder.
    Inference inf("../best.onnx", cv::Size(640, 640), "classes.txt", runOnGPU); // classes.txt 可以缺失

    // 2. 读取 input_img 文件夹下的所有文件名
    std::filesystem::path path("../input_img/");
    std::vector<std::string> imageNames;
    for (const auto &entry : std::filesystem::directory_iterator(path))
    {
        imageNames.push_back(entry.path().string());
    }

    std::cout << "Number of images:" << imageNames.size() << std::endl;

    // 3. 遍历所有图片，对每张图片进行推理

    for (int i = 0; i < imageNames.size(); ++i)
    {
        cv::Mat frame = cv::imread(imageNames[i]);

        // Inference starts here...
        std::vector<Detection> output = inf.runInference(frame);

        int detections = output.size();
        std::cout << "Number of detections:" << detections << std::endl;

        // 若矩形框位置不对，下面这行可能需要
        // cv::resize(frame, frame, cv::Size(480, 640));

        for (int i = 0; i < detections; ++i)
        {
            Detection detection = output[i];

            cv::Rect box = detection.box;
            cv::Scalar color = detection.color;

            // Detection box
            cv::rectangle(frame, box, color, 2);

            // Detection box text
            std::string classString = detection.className + ' ' + std::to_string(detection.confidence).substr(0, 4);
            cv::Size textSize = cv::getTextSize(classString, cv::FONT_HERSHEY_DUPLEX, 1, 2, 0);
            cv::Rect textBox(box.x, box.y - 40, textSize.width + 10, textSize.height + 20);

            cv::rectangle(frame, textBox, color, cv::FILLED);
            cv::putText(frame, classString, cv::Point(box.x + 5, box.y - 10), cv::FONT_HERSHEY_DUPLEX, 1, cv::Scalar(0, 0, 0), 2, 0);
        }
        cv::imwrite(string("../output_img/") + imageNames[i].substr(imageNames[i].find_last_of("/") + 1), frame);
    }
}
