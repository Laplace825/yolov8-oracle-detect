#include <iostream>
#include <fstream>
#include <opencv2/opencv.hpp>
#include <opencv2/dnn.hpp>
#include <filesystem>

// 常量
const int INPUT_WIDTH = 416;
const int INPUT_HEIGHT = 416;

// 预处理函数
void pre_process(cv::Mat &image, cv::Mat &blob)
{
    // CenterCrop：将图像裁剪为正方形，然后调整大小以匹配网络输入
    int crop_size = std::min(image.cols, image.rows);
    int left = (image.cols - crop_size) / 2, top = (image.rows - crop_size) / 2;
    cv::Mat crop_image = image(cv::Rect(left, top, crop_size, crop_size));
    cv::resize(crop_image, crop_image, cv::Size(INPUT_WIDTH, INPUT_HEIGHT));

    // Normalize：将图像归一化到0-1范围，并减去均值，然后除以标准差
    crop_image.convertTo(crop_image, CV_32FC3, 1. / 255.);
    cv::subtract(crop_image, cv::Scalar(0.406, 0.456, 0.485), crop_image);
    cv::divide(crop_image, cv::Scalar(0.225, 0.224, 0.229), crop_image);

    // 将处理后的图像转换为网络可以接受的blob格式
    cv::dnn::blobFromImage(crop_image, blob, 1, cv::Size(crop_image.cols, crop_image.rows), cv::Scalar(), true, false);
}

// 网络推理函数
void process(cv::Mat &blob, cv::dnn::Net &net, std::vector<cv::Mat> &outputs)
{
    // 设置网络输入
    net.setInput(blob);
    // 进行前向传播，获取输出
    net.forward(outputs, net.getUnconnectedOutLayersNames());
}

// 后处理
const std::string &post_process(std::vector<cv::Mat> &detections, std::vector<std::string> &class_name)
{
    std::vector<float> values;
    for (size_t i = 0; i < detections[0].cols; i++)
    {
        values.push_back(detections[0].at<float>(0, i));
    }
    int id = std::distance(values.begin(), std::max_element(values.begin(), values.end()));

    return class_name[id];
}

// 主函数
int main(int argc, char **argv)
{
    // 读取类别文件，将所有类别存入vector
    std::vector<std::string> class_name;
    std::ifstream ifs("../class_cls.txt");
    std::string line;
    while (getline(ifs, line))
    {
        class_name.push_back(line);
    }

    // 加载预训练的神经网络模型
    cv::dnn::Net net = cv::dnn::readNet("../best-cls.onnx");
    // 设置网络的计算后端和目标为CUDA
    net.setPreferableBackend(cv::dnn::DNN_BACKEND_CUDA);
    net.setPreferableTarget(cv::dnn::DNN_TARGET_CUDA);

    // 遍历输入图片目录，对每张图片进行预处理和网络推理，然后将结果写入文件
    std::filesystem::path path("../input_img");
    std::fstream out_file("../output.txt", std::ios::out);
    std::vector<cv::Mat> outputs;
    cv::Mat image = cv::imread("../input_img/41_E000-4.jpg"), blob;

    for (const auto &entry : std::filesystem::directory_iterator(path))
    {
        image = cv::imread(entry.path().string()), blob;
        pre_process(image, blob);
        process(blob, net, outputs);
        const std::string &result = post_process(outputs, class_name);
        std::cout << entry.path().string() << " : " << result << '\n';
        out_file << entry.path().string() << " : " << result << '\n';
    }

    return 0;
}