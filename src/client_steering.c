#include <stdio.h>
#include <stdlib.h>
#include <tensorflow/lite/c/c_api.h>

// Giả lập chuẩn hóa input
void normalize_input(float* input, const float* mean, const float* scale, int len) {
    for (int i = 0; i < len; i++) {
        input[i] = (input[i] - mean[i]) / scale[i];
    }
}

int main() {
    // Load mô hình .tflite
    TfLiteModel* model = TfLiteModelCreateFromFile("client_steering_model_quantized.tflite");
    if (!model) {
        fprintf(stderr, "❌ Không load được mô hình\n");
        return 1;
    }

    // Tạo interpreter
    TfLiteInterpreterOptions* options = TfLiteInterpreterOptionsCreate();
    TfLiteInterpreter* interpreter = TfLiteInterpreterCreate(model, options);

    TfLiteInterpreterAllocateTensors(interpreter);

    // Lấy thông tin tensor
    TfLiteTensor* input_tensor = TfLiteInterpreterGetInputTensor(interpreter, 0);

    // Các đặc trưng AP cần kiểm tra
    float aps[3][8] = {
        {-65, 5, 300, 10, 1, 5, 30, 40},
        {-72, 8, 180, 20, 3, 5, 40, 55},
        {-60, 10, 200, 15, 5, 2, 35, 45}
    };

    float mean[8]  = {-65, 8, 250, 15, 3, 4, 40, 50};
    float scale[8] = {5, 3, 80, 5, 3, 1.5, 15, 20};

    float best_score = -1.0f;
    int best_ap = -1;

    for (int i = 0; i < 3; i++) {
        float input[8];
        for (int j = 0; j < 8; j++) input[j] = aps[i][j];

        normalize_input(input, mean, scale, 8);

        TfLiteTensorCopyFromBuffer(input_tensor, input, sizeof(input));

        if (TfLiteInterpreterInvoke(interpreter) != kTfLiteOk) {
            fprintf(stderr, "❌ Inference lỗi tại AP %d\n", i);
            continue;
        }

        float output;
        TfLiteTensor* output_tensor = TfLiteInterpreterGetOutputTensor(interpreter, 0);
        TfLiteTensorCopyToBuffer(output_tensor, &output, sizeof(output));

        printf("AP%d score: %.3f\n", i + 1, output);

        if (output > best_score) {
            best_score = output;
            best_ap = i;
        }
    }

    printf("✅ Chọn AP tốt nhất: AP%d (score %.3f)\n", best_ap + 1, best_score);

    // Giải phóng
    TfLiteInterpreterDelete(interpreter);
    TfLiteModelDelete(model);
    TfLiteInterpreterOptionsDelete(options);

    return 0;
}

