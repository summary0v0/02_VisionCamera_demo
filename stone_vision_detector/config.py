"""全局配置文件。

将项目中的硬编码参数集中管理，便于后续调整和维护。
"""

# 摄像头配置
CAMERA_INDEX = 0

# 输出目录配置
OUTPUT_IMAGE_DIR = "output/images"
OUTPUT_REPORT_DIR = "output/reports"

# 预处理配置
GAUSSIAN_BLUR_KERNEL = (5, 5)
THRESHOLD_VALUE = 127
