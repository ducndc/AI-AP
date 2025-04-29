# AI-AP
Access Point

# TensorFlow Lite C API Build Instructions

This guide shows how to **clone and build TensorFlow Lite's C API** using CMake, which is suitable for embedding in systems like OpenWRT or MediaTek SDK where C is preferred over C++.

---

## 1. Clone TensorFlow

```bash
git clone https://github.com/tensorflow/tensorflow.git
cd tensorflow
git checkout v2.14.0  

cd tensorflow/lite
mkdir build && cd build

cmake .. \
  -DTFLITE_ENABLE_XNNPACK=OFF \
  -DTFLITE_ENABLE_RUY=OFF \
  -DCMAKE_BUILD_TYPE=Release

make -j4

