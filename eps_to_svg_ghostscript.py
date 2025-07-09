#!/usr/bin/env python3
"""
EPS to SVG 转换器 - Ghostscript版
使用Ghostscript专门处理EPS文件转换
"""

import os
import subprocess
import sys
from pathlib import Path
import glob

def find_ghostscript():
    """查找系统中的Ghostscript安装"""
    # Windows系统可能的Ghostscript路径
    possible_paths = [
        # 64位版本
        r"C:\Program Files\gs\gs*\bin\gswin64c.exe",
        r"C:\Program Files (x86)\gs\gs*\bin\gswin64c.exe",
        # 32位版本
        r"C:\Program Files\gs\gs*\bin\gswin32c.exe", 
        r"C:\Program Files (x86)\gs\gs*\bin\gswin32c.exe",
        # 通用名称（如果在PATH中）
        "gs", "gswin64c", "gswin32c"
    ]
    
    for path_pattern in possible_paths:
        if '*' in path_pattern:
            # 处理通配符路径（查找版本号）
            matches = glob.glob(path_pattern)
            if matches:
                # 选择最新版本（按字母排序）
                path = sorted(matches)[-1]
            else:
                continue
        else:
            path = path_pattern
        
        try:
            # 测试Ghostscript是否工作
            result = subprocess.run([path, '--version'], 
                                  capture_output=True, check=True, timeout=10,
                                  encoding='utf-8', errors='ignore')
            version = result.stdout.strip()
            print(f"✓ 找到 Ghostscript: {path}")
            print(f"  版本: {version}")
            return path
        except Exception:
            continue
    
    return None

def convert_eps_to_svg_gs(eps_file, gs_path, scale_factor=3):
    """使用Ghostscript将EPS转换为SVG"""
    svg_file = eps_file.with_suffix('.svg')
    
    print(f"正在转换: {eps_file.name} -> {svg_file.name}")
    
    try:
        # 删除可能存在的输出文件
        if svg_file.exists():
            svg_file.unlink()
        
        # 构建Ghostscript命令
        # 使用更高的分辨率来实现缩放效果
        dpi = int(72 * scale_factor)  # EPS默认是72 DPI
        
        cmd = [
            gs_path,
            '-dNOPAUSE',           # 不暂停等待用户输入
            '-dBATCH',             # 批处理模式
            '-dSAFER',             # 安全模式
            '-dEPSCrop',           # 自动裁剪到EPS边界
            '-sDEVICE=svg',        # 输出SVG格式
            f'-r{dpi}',            # 设置分辨率（实现缩放）
            f'-sOutputFile={svg_file}',  # 输出文件
            str(eps_file)          # 输入EPS文件
        ]
        
        # 执行转换
        result = subprocess.run(cmd,
                              capture_output=True,
                              text=True,
                              check=True,
                              timeout=120,  # 2分钟超时
                              encoding='utf-8',
                              errors='ignore')
        
        # 检查输出文件
        if svg_file.exists() and svg_file.stat().st_size > 0:
            file_size = svg_file.stat().st_size / 1024
            print(f"✓ 转换成功: {svg_file.name} ({file_size:.1f} KB, {scale_factor}x)")
            return True
        else:
            print(f"❌ 转换失败: 输出文件为空或未生成")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Ghostscript错误: {e}")
        if e.stderr:
            # 显示关键错误信息
            error_lines = e.stderr.strip().split('\n')
            for line in error_lines[-3:]:
                if line.strip() and not line.startswith('GPL'):
                    print(f"   错误: {line.strip()}")
        return False
    except subprocess.TimeoutExpired:
        print(f"❌ 转换超时: {eps_file.name}")
        return False
    except Exception as e:
        print(f"❌ 转换失败: {e}")
        return False

def get_eps_files():
    """获取当前目录下所有EPS文件"""
    current_dir = Path.cwd()
    eps_files = list(current_dir.glob("*.eps"))
    eps_files.extend(current_dir.glob("*.EPS"))
    return sorted(list(set(eps_files)))

def install_ghostscript_guide():
    """显示Ghostscript安装指南"""
    print("\n" + "="*60)
    print("Ghostscript 安装指南")
    print("="*60)
    print("1. 访问官方网站: https://www.ghostscript.com/download/gsdnld.html")
    print("2. 下载 Windows 版本:")
    print("   - 64位系统: 下载 'Ghostscript AGPL Release' 64-bit")
    print("   - 32位系统: 下载 'Ghostscript AGPL Release' 32-bit")
    print("3. 运行安装程序，使用默认设置安装")
    print("4. 安装完成后重新运行此脚本")
    print("\n或者使用Chocolatey安装 (如果已安装Chocolatey):")
    print("   choco install ghostscript")
    print("\n或者使用winget安装:")
    print("   winget install GNU.Ghostscript")

def main():
    """主函数"""
    print("EPS to SVG 转换器 - Ghostscript版")
    print("="*60)
    print(f"当前目录: {Path.cwd()}")
    print()
    
    # 查找Ghostscript
    print("检查Ghostscript...")
    gs_path = find_ghostscript()
    
    if not gs_path:
        print("❌ 未找到 Ghostscript")
        install_ghostscript_guide()
        input("\n按回车键退出...")
        return
    
    # 获取EPS文件
    eps_files = get_eps_files()
    
    if not eps_files:
        print("\n❌ 当前目录下没有找到EPS文件")
        print("请确认当前目录包含 .eps 或 .EPS 文件")
        input("按回车键退出...")
        return
    
    print(f"\n找到 {len(eps_files)} 个EPS文件:")
    for i, file in enumerate(eps_files[:10], 1):
        file_size = file.stat().st_size / 1024
        print(f"  {i:2d}. {file.name} ({file_size:.1f} KB)")
    
    if len(eps_files) > 10:
        print(f"  ... 还有 {len(eps_files) - 10} 个文件")
    
    # 确认转换
    print(f"\n转换设置:")
    print(f"- 工具: Ghostscript")
    print(f"- 输出格式: SVG")
    print(f"- 缩放倍数: 3x")
    print(f"- 分辨率: {72 * 3} DPI")
    
    response = input(f"\n是否开始转换? (y/n): ").lower().strip()
    if response not in ['y', 'yes', '是']:
        print("操作已取消")
        return
    
    print("\n开始转换...")
    print("-"*60)
    
    # 转换文件
    success_count = 0
    fail_count = 0
    
    for i, eps_file in enumerate(eps_files, 1):
        print(f"\n[{i}/{len(eps_files)}] ", end="")
        if convert_eps_to_svg_gs(eps_file, gs_path, scale_factor=3):
            success_count += 1
        else:
            fail_count += 1
    
    # 显示结果
    print("\n" + "="*60)
    print("转换完成!")
    print(f"成功: {success_count} 个文件")
    print(f"失败: {fail_count} 个文件")
    print(f"成功率: {success_count/(success_count+fail_count)*100:.1f}%")
    
    if success_count > 0:
        print(f"\nSVG文件已保存在: {Path.cwd()}")
        print("所有SVG文件均为原EPS文件的3倍大小")
    
    if fail_count > 0:
        print(f"\n失败的文件可能原因:")
        print("- EPS文件格式不标准或损坏")
        print("- 文件权限问题")
        print("- 磁盘空间不足")
    
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