#include "inference.h"
#include "predict_det.h"
#include "predict_cls.h"
#include <opencv2/opencv.hpp>
#include <opencv2/cudaimgproc.hpp>

int main()
{
    det();
    cls();
    // cv::cuda::printCudaDeviceInfo(cv::cuda::getDevice());
    // int count = cv::cuda::getCudaEnabledDeviceCount();
    // std::cout << "Number of CUDA-enabled devices: " << count << std::endl;
    // cv::Mat img = cv::imread("../input_img/h05548.jpg");
    // cv::cuda::GpuMat d_img;
    // d_img.upload(img);
    // cv::Rect roi(10, 10, 100, 100);
    return 0;
}