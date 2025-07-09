#!/usr/bin/env python3

import os
import subprocess
import sys
from pathlib import Path
import glob

def find_ghostscript():
    """查找Ghostscript"""
    possible_paths = [
        r"C:\Program Files\gs\gs*\bin\gswin64c.exe",
        r"C:\Program Files (x86)\gs\gs*\bin\gswin64c.exe",
        "gs", "gswin64c", "gswin32c"
    ]
    
    for path_pattern in possible_paths:
        if '*' in path_pattern:
            matches = glob.glob(path_pattern)
            if matches:
                path = sorted(matches)[-1]
            else:
                continue
        else:
            path = path_pattern
        
        try:
            result = subprocess.run([path, '--version'], 
                                  capture_output=True, check=True, timeout=10,
                                  encoding='utf-8', errors='ignore')
            version = result.stdout.strip()
            return path, version
        except Exception:
            continue
    
    return None, None

def convert_eps_to_png(eps_file, gs_path, dpi=450):
    """将EPS转换为超高质量PNG"""
    png_file = eps_file.with_suffix('.png')
    
    print(f"转换: {eps_file.name} -> {png_file.name}")
    
    try:
        # 删除可能存在的文件
        if png_file.exists():
            png_file.unlink()
        
        # 使用最高质量设置
        cmd = [
            gs_path,
            '-dNOPAUSE',
            '-dBATCH',
            '-dSAFER',
            '-dEPSCrop',                    # 自动裁剪
            '-sDEVICE=png16m',              # 24位真彩色
            f'-r{dpi}',                     # 超高DPI
            '-dTextAlphaBits=4',            # 文字抗锯齿
            '-dGraphicsAlphaBits=4',        # 图形抗锯齿
            '-dDownScaleFactor=1',          # 不降采样
            '-dColorConversionStrategy=/LeaveColorUnchanged',  # 保持颜色
            f'-sOutputFile={png_file}',
            str(eps_file)
        ]
        
        result = subprocess.run(cmd,
                              capture_output=True,
                              text=True,
                              check=True,
                              timeout=180,  # 3分钟超时
                              encoding='utf-8',
                              errors='ignore')
        
        if png_file.exists() and png_file.stat().st_size > 0:
            file_size = png_file.stat().st_size / (1024 * 1024)  # MB
            print(f"  ✓ 成功: {file_size:.1f} MB, {dpi} DPI")
            return True
        else:
            print(f"  ❌ 失败: 文件未生成")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"  ❌ Ghostscript错误: {e}")
        if e.stderr:
            print(f"  详细错误: {e.stderr[:200]}")
        return False
    except subprocess.TimeoutExpired:
        print(f"  ❌ 转换超时")
        return False
    except Exception as e:
        print(f"  ❌ 异常: {e}")
        return False

def get_eps_files():
    """获取当前目录下所有EPS文件"""
    current_dir = Path.cwd()
    eps_files = list(current_dir.glob("*.eps"))
    eps_files.extend(current_dir.glob("*.EPS"))
    return sorted(list(set(eps_files)))

def main():
    """主函数"""
    print("EPS 转 超高质量 PNG 转换器")
    print("="*60)
    print(f"当前目录: {Path.cwd()}")
    print()
    
    print("💡 策略说明:")
    print("由于EPS直接转SVG困难，我们将生成超高质量的PNG文件")
    print("这些PNG可以在需要时手动转换为SVG或直接使用")
    print()
    
    # 查找Ghostscript
    gs_path, gs_version = find_ghostscript()
    if not gs_path:
        print("❌ 未找到 Ghostscript")
        input("按回车键退出...")
        return
    
    print(f"✓ Ghostscript: {gs_version}")
    
    # 获取EPS文件
    eps_files = get_eps_files()
    
    if not eps_files:
        print("\n❌ 当前目录下没有找到EPS文件")
        input("按回车键退出...")
        return
    
    print(f"\n找到 {len(eps_files)} 个EPS文件:")
    for i, file in enumerate(eps_files[:5], 1):
        file_size = file.stat().st_size / 1024
        print(f"  {i}. {file.name} ({file_size:.1f} KB)")
    
    if len(eps_files) > 5:
        print(f"  ... 还有 {len(eps_files) - 5} 个文件")
    
    # 选择DPI
    print(f"\n质量选项:")
    print(f"1. 标准质量 (300 DPI) - 适合打印")
    print(f"2. 高质量   (450 DPI) - 3倍缩放，推荐")
    print(f"3. 超高质量 (600 DPI) - 4倍缩放")
    print(f"4. 极高质量 (900 DPI) - 6倍缩放，文件很大")
    
    try:
        choice = input(f"\n选择质量 (1-4, 默认2): ").strip()
        if choice == "1":
            dpi = 300
        elif choice == "3":
            dpi = 600
        elif choice == "4":
            dpi = 900
        else:
            dpi = 450  # 默认
    except:
        dpi = 450
    
    scale_factor = dpi / 150  # 150 DPI作为基准
    
    print(f"\n转换设置:")
    print(f"- 输出格式: PNG (24位真彩色)")
    print(f"- 分辨率: {dpi} DPI")
    print(f"- 缩放倍数: {scale_factor:.1f}x")
    print(f"- 抗锯齿: 最高级别")
    print(f"- 预估单文件大小: {dpi/150:.0f}-{dpi/75:.0f} MB")
    
    total_size = len(eps_files) * (dpi/75)  # 粗略估算
    print(f"- 预估总大小: {total_size:.0f} MB")
    
    response = input(f"\n开始转换? (y/n): ").lower().strip()
    if response not in ['y', 'yes', '是']:
        print("操作已取消")
        return
    
    print("\n开始转换...")
    print("-"*60)
    
    # 转换文件
    success_count = 0
    fail_count = 0
    total_size = 0
    
    for i, eps_file in enumerate(eps_files, 1):
        print(f"\n[{i}/{len(eps_files)}] ", end="")
        if convert_eps_to_png(eps_file, gs_path, dpi):
            success_count += 1
            png_file = eps_file.with_suffix('.png')
            if png_file.exists():
                total_size += png_file.stat().st_size
        else:
            fail_count += 1
    
    # 显示结果
    print("\n" + "="*60)
    print("转换完成!")
    print(f"成功: {success_count} 个PNG文件")
    print(f"失败: {fail_count} 个文件")
    print(f"总大小: {total_size/(1024*1024):.1f} MB")
    print(f"成功率: {success_count/(success_count+fail_count)*100:.1f}%")
    
    if success_count > 0:
        print(f"\n✓ PNG文件已保存在: {Path.cwd()}")
        print(f"✓ 质量: {dpi} DPI ({scale_factor:.1f}x)")
        print(f"✓ 格式: 24位真彩色PNG")
        
        print(f"\n💡 后续选项:")
        print(f"1. 直接使用这些高质量PNG文件")
        print(f"2. 使用在线工具将PNG转换为SVG:")
        print(f"   - https://convertio.co/png-svg/")
        print(f"   - https://www.aconvert.com/image/png-to-svg/")
        print(f"3. 使用Adobe Illustrator的图像描摹功能")
        print(f"4. 使用专业矢量化软件如Vector Magic")
    
    input("\n按回车键退出...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n操作被用户中断")
        input("按回车键退出...")
    except Exception as e:
        print(f"\n程序运行出错: {e}")
        input("按回车键退出...")