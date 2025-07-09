# EPS to SVG/PNG Converter Collection | EPS 转 SVG/PNG 转换器集合

A comprehensive collection of Python scripts for converting EPS (Encapsulated PostScript) files to SVG or high-quality PNG formats with various conversion strategies and diagnostic tools.

一套全面的 Python 脚本集合，用于将 EPS（封装 PostScript）文件转换为 SVG 或高质量 PNG 格式，提供多种转换策略和诊断工具。

## 📋 Scripts Overview | 脚本概览

| Script | Purpose | 脚本 | 用途 |
|--------|---------|------|------|
| `eps_to_high_quality_png.py` | Convert EPS to ultra-high quality PNG | 高质量 PNG 转换器 | 将 EPS 转换为超高质量 PNG |
| `eps_to_svg_diagnostic.py` | Diagnostic tool with detailed error reporting | 诊断工具 | 带详细错误报告的诊断工具 |
| `eps_to_svg_robust.py` | Multi-method SVG conversion with fallbacks | 强健 SVG 转换器 | 多方法 SVG 转换，带备用方案 |
| `eps_to_svg_ghostscript.py` | Direct Ghostscript-based SVG conversion | Ghostscript SVG 转换器 | 基于 Ghostscript 的直接 SVG 转换 |

## 🚀 Quick Start | 快速开始

### Prerequisites | 系统要求

- **Python 3.6+** | Python 3.6 或更高版本
- **Ghostscript** (Required for all scripts) | Ghostscript（所有脚本必需）
- **Additional tools** (Optional, see individual script requirements) | 其他工具（可选，详见各脚本要求）

### Installation | 安装

1. **Install Ghostscript | 安装 Ghostscript**
   ```bash
   # Windows (using Chocolatey)
   choco install ghostscript
   
   # Windows (using winget)
   winget install GNU.Ghostscript
   
   # Or download from: https://www.ghostscript.com/download/gsdnld.html
   # 或从官网下载：https://www.ghostscript.com/download/gsdnld.html
   ```

2. **Clone this repository | 克隆此仓库**
   ```bash
   git clone https://github.com/excniesNIED/EPS_Converter_Toolkit.git
   cd EPS_Converter_Toolkit
   ```

3. **Install optional dependencies | 安装可选依赖**
   ```bash
   pip install Pillow  # For PIL support | PIL 支持
   ```

## 📖 Detailed Script Documentation | 详细脚本文档

### 1. `eps_to_high_quality_png.py` | 高质量 PNG 转换器

**Purpose | 用途**: Convert EPS files to ultra-high quality PNG images with customizable DPI settings.
将 EPS 文件转换为可自定义 DPI 设置的超高质量 PNG 图像。

**Features | 功能**:
- Multiple quality presets (300-900 DPI) | 多种质量预设（300-900 DPI）
- 24-bit true color output | 24位真彩色输出
- Anti-aliasing support | 抗锯齿支持
- Automatic file size estimation | 自动文件大小估算

**Usage | 使用方法**:
```bash
python eps_to_high_quality_png.py
```

**Requirements | 环境要求**:
- Ghostscript (必需)
- Python 3.6+ (必需)

**Quality Options | 质量选项**:
- **Standard (300 DPI)**: Good for printing | 标准（300 DPI）：适合打印
- **High (450 DPI)**: 3x scaling, recommended | 高质量（450 DPI）：3倍缩放，推荐
- **Ultra (600 DPI)**: 4x scaling | 超高质量（600 DPI）：4倍缩放
- **Maximum (900 DPI)**: 6x scaling, large files | 极高质量（900 DPI）：6倍缩放，文件较大

### 2. `eps_to_svg_diagnostic.py` | 诊断工具

**Purpose | 用途**: Comprehensive diagnostic tool for troubleshooting EPS conversion issues with detailed error reporting.
全面的诊断工具，用于排查 EPS 转换问题，提供详细的错误报告。

**Features | 功能**:
- File format validation | 文件格式验证
- Multiple conversion method testing | 多种转换方法测试
- Detailed error messages | 详细错误信息
- Individual file testing mode | 单文件测试模式

**Usage | 使用方法**:
```bash
python eps_to_svg_diagnostic.py
```

**Operating Modes | 操作模式**:
1. **Single file diagnostic | 单文件诊断**: Test individual files with detailed analysis
2. **Batch conversion | 批量转换**: Convert all files with diagnostic output
3. **Sample testing | 样本测试**: Test first 5 files for quick assessment

**Requirements | 环境要求**:
- Ghostscript (必需)
- Python 3.6+ (必需)

### 3. `eps_to_svg_robust.py` | 强健 SVG 转换器

**Purpose | 用途**: Multi-method SVG converter with automatic fallback strategies for maximum compatibility.
多方法 SVG 转换器，具有自动备用策略，实现最大兼容性。

**Features | 功能**:
- Multiple conversion engines | 多种转换引擎
- Automatic tool detection | 自动工具检测
- Fallback strategies | 备用策略
- Support for various output formats | 支持多种输出格式

**Conversion Methods | 转换方法**:
1. **Inkscape Direct**: Native SVG conversion | Inkscape 直接转换：原生 SVG 转换
2. **Ghostscript + Inkscape**: Two-step process | Ghostscript + Inkscape：两步处理
3. **Ghostscript Direct**: Direct SVG output | Ghostscript 直接转换：直接 SVG 输出
4. **PIL + Inkscape**: Fallback method | PIL + Inkscape：备用方法

**Usage | 使用方法**:
```bash
python eps_to_svg_robust.py
```

**Requirements | 环境要求**:
- Ghostscript (必需)
- Inkscape (推荐) | Download from: https://inkscape.org/
- PIL/Pillow (可选) | `pip install Pillow`

### 4. `eps_to_svg_ghostscript.py` | Ghostscript SVG 转换器

**Purpose | 用途**: Direct SVG conversion using Ghostscript with optimized parameters for best quality output.
使用 Ghostscript 直接转换 SVG，采用优化参数以获得最佳质量输出。

**Features | 功能**:
- Pure Ghostscript implementation | 纯 Ghostscript 实现
- Optimized SVG parameters | 优化的 SVG 参数
- Automatic EPS boundary detection | 自动 EPS 边界检测
- Scalable output (3x default) | 可缩放输出（默认3倍）

**Usage | 使用方法**:
```bash
python eps_to_svg_ghostscript.py
```

**Requirements | 环境要求**:
- Ghostscript (必需)
- Python 3.6+ (必需)

**Output Settings | 输出设置**:
- Format: SVG | 格式：SVG
- Scaling: 3x (216 DPI) | 缩放：3倍（216 DPI）
- Boundary: Auto-cropped | 边界：自动裁剪

## 🔧 Installation Guide | 安装指南

### Windows

1. **Install Ghostscript | 安装 Ghostscript**:
   - Download from official website | 从官网下载: https://www.ghostscript.com/download/gsdnld.html
   - Choose 64-bit version for 64-bit Windows | 64位 Windows 选择64位版本
   - Install with default settings | 使用默认设置安装

2. **Install Inkscape (Optional) | 安装 Inkscape（可选）**:
   - Download from | 下载地址: https://inkscape.org/release/
   - Required for `eps_to_svg_robust.py` | `eps_to_svg_robust.py` 需要

3. **Install Python packages | 安装 Python 包**:
   ```bash
   pip install Pillow  # Optional, for enhanced compatibility
   ```

### macOS

```bash
# Install Ghostscript
brew install ghostscript

# Install Inkscape (optional)
brew install inkscape

# Install Python packages
pip install Pillow
```

### Linux (Ubuntu/Debian)

```bash
# Install Ghostscript
sudo apt update
sudo apt install ghostscript

# Install Inkscape (optional)
sudo apt install inkscape

# Install Python packages
pip install Pillow
```

## 📊 Comparison Matrix | 对比矩阵

| Feature | PNG Converter | Diagnostic | Robust SVG | Ghostscript SVG |
|---------|---------------|------------|------------|-----------------|
| **Output Format** | PNG only | Multiple | SVG primary | SVG only |
| **输出格式** | 仅 PNG | 多种 | 主要 SVG | 仅 SVG |
| **Quality Options** | 4 levels | N/A | Fixed 3x | Fixed 3x |
| **质量选项** | 4档 | 不适用 | 固定3倍 | 固定3倍 |
| **Error Reporting** | Basic | Detailed | Medium | Basic |
| **错误报告** | 基础 | 详细 | 中等 | 基础 |
| **Tool Dependencies** | GS only | GS only | GS + INK | GS only |
| **工具依赖** | 仅 GS | 仅 GS | GS + INK | 仅 GS |
| **Best For** | High-quality images | Troubleshooting | Compatibility | Simple SVG |
| **最适合** | 高质量图像 | 问题排查 | 兼容性 | 简单 SVG |

*GS = Ghostscript, INK = Inkscape*

## 🚨 Troubleshooting | 故障排除

### Common Issues | 常见问题

1. **"Ghostscript not found" | "未找到 Ghostscript"**
   - Ensure Ghostscript is properly installed | 确保 Ghostscript 正确安装
   - Check if it's in your system PATH | 检查是否在系统 PATH 中
   - Try reinstalling with default settings | 尝试使用默认设置重新安装

2. **"No EPS files found" | "未找到 EPS 文件"**
   - Ensure you're in the correct directory | 确保在正确的目录中
   - Check file extensions (.eps or .EPS) | 检查文件扩展名（.eps 或 .EPS）

3. **"Conversion failed" | "转换失败"**
   - Use the diagnostic script first | 首先使用诊断脚本
   - Check if EPS files are valid | 检查 EPS 文件是否有效
   - Try different conversion methods | 尝试不同的转换方法

4. **Unicode/Encoding errors | Unicode/编码错误**
   - Ensure file paths don't contain special characters | 确保文件路径不包含特殊字符
   - Try moving files to a simple path | 尝试将文件移动到简单路径

### Performance Tips | 性能提示

- **For large batches | 大批量处理**: Use PNG converter for speed | 使用 PNG 转换器以提高速度
- **For vector output | 矢量输出**: Try robust SVG converter first | 首先尝试强健 SVG 转换器
- **For debugging | 调试**: Always start with diagnostic script | 始终从诊断脚本开始

## 📝 Output Examples | 输出示例

### Successful Conversion | 成功转换
```
[1/25] 转换: example.eps -> example.svg
  ✓ 成功: example.svg (45.2 KB, 3x)
```

### Failed Conversion | 转换失败
```
[1/25] 转换: broken.eps -> broken.svg
  ❌ Ghostscript错误: Invalid EPS format
```

### Diagnostic Output | 诊断输出
```
检测EPS文件: example.eps
  文件大小: 196740 字节 (192.1 KB)
  文件头: %!PS-Adobe-2.0 EPSF-2.0
  ✓ 检测到PostScript文件头
  ✓ Ghostscript可以解析此文件
```

## 🤝 Contributing | 贡献

We welcome contributions! Please feel free to submit issues, feature requests, or pull requests.

欢迎贡献！请随时提交问题、功能请求或拉取请求。

### Development Setup | 开发环境设置

1. Fork the repository | 分叉仓库
2. Create a feature branch | 创建功能分支
3. Make your changes | 进行更改
4. Test with various EPS files | 使用各种 EPS 文件测试
5. Submit a pull request | 提交拉取请求

## 📄 License | 许可证

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。

## 🙏 Acknowledgments | 致谢

- **Ghostscript team** for the powerful PostScript interpreter | Ghostscript 团队提供强大的 PostScript 解释器
- **Inkscape project** for excellent SVG support | Inkscape 项目提供优秀的 SVG 支持
- **Python PIL/Pillow** maintainers for image processing capabilities | Python PIL/Pillow 维护者提供图像处理功能

## 📞 Support | 支持

If you encounter any issues or have questions, please:

如果遇到任何问题或有疑问，请：

1. Check the troubleshooting section above | 查看上面的故障排除部分
2. Run the diagnostic script for detailed error information | 运行诊断脚本获取详细错误信息
3. Open an issue on GitHub with your error details | 在 GitHub 上提交包含错误详情的问题

## 🤖 AI Generated | AI 生成

This project was generated with the assistance of AI technology to provide efficient and reliable EPS conversion solutions.

本项目在 AI 技术协助下生成，旨在提供高效可靠的 EPS 转换解决方案。

### Generation Details | 生成详情

- **Generated by | 生成工具**: GitHub Copilot (Claude Sonnet 4)
- **Generation Date | 生成日期**: 2025-07-09
- **User | 用户**: excniesNIED
- **Human Oversight | 人工监督**: Code reviewed and tested by human developer
- **Quality Assurance | 质量保证**: All scripts tested with real EPS files

### AI Contribution | AI 贡献内容

- ✅ **Code Generation**: Python conversion scripts and logic
- ✅ **Documentation**: README, comments, and usage guides  
- ✅ **Error Handling**: Comprehensive exception management
- ✅ **Multi-platform Support**: Windows, macOS, Linux compatibility
- ✅ **Troubleshooting Guide**: Common issues and solutions

- ✅ **代码生成**: Python 转换脚本和逻辑
- ✅ **文档编写**: README、注释和使用指南
- ✅ **错误处理**: 全面的异常管理
- ✅ **多平台支持**: Windows、macOS、Linux 兼容性
- ✅ **故障排除指南**: 常见问题和解决方案

### Human Contribution | 人工贡献内容

- 🔍 **Requirements Definition**: Specific EPS conversion needs
- 🧪 **Testing**: Real-world EPS file testing and validation
- 📝 **Use Case Scenarios**: Academic and technical document processing
- 🎯 **Quality Control**: Code review and functionality verification

- 🔍 **需求定义**: 具体的 EPS 转换需求
- 🧪 **测试验证**: 真实 EPS 文件测试和验证
- 📝 **使用场景**: 学术和技术文档处理
- 🎯 **质量控制**: 代码审查和功能验证

### Disclaimer | 免责声明

While this project was AI-assisted, all code has been reviewed, tested, and validated for functionality. Users should still test the scripts with their specific EPS files before production use.

虽然本项目由 AI 协助生成，但所有代码都经过审查、测试和功能验证。用户在生产环境使用前仍应使用特定的 EPS 文件进行测试。

**Generated with 💡 by GitHub Copilot & 🧠 Human Intelligence**

---

**Happy Converting! | 转换愉快！** 🎉