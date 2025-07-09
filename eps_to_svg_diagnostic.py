#!/usr/bin/env python3

import os
import subprocess
import sys
from pathlib import Path
import glob
import tempfile

def find_ghostscript():
    """查找系统中的Ghostscript安装"""
    possible_paths = [
        r"C:\Program Files\gs\gs*\bin\gswin64c.exe",
        r"C:\Program Files (x86)\gs\gs*\bin\gswin64c.exe",
        r"C:\Program Files\gs\gs*\bin\gswin32c.exe", 
        r"C:\Program Files (x86)\gs\gs*\bin\gswin32c.exe",
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
            print(f"✓ 找到 Ghostscript: {path}")
            print(f"  版本: {version}")
            return path
        except Exception:
            continue
    
    return None

def test_eps_file(eps_file, gs_path):
    """测试EPS文件的有效性"""
    print(f"\n检测EPS文件: {eps_file.name}")
    
    # 检查文件大小
    file_size = eps_file.stat().st_size
    print(f"  文件大小: {file_size} 字节 ({file_size/1024:.1f} KB)")
    
    # 检查文件头
    try:
        with open(eps_file, 'rb') as f:
            header = f.read(100)
            print(f"  文件头: {header[:50]}")
            
            # 检查是否是有效的EPS文件
            if header.startswith(b'%!PS-Adobe'):
                print("  ✓ 检测到PostScript文件头")
            elif header.startswith(b'\xC5\xD0\xD3\xC6'):
                print("  ✓ 检测到EPSF二进制文件头")
            else:
                print("  ❌ 未识别的文件格式")
                return False
                
    except Exception as e:
        print(f"  ❌ 读取文件失败: {e}")
        return False
    
    # 使用Ghostscript测试文件
    try:
        cmd = [gs_path, '-dNODISPLAY', '-dBATCH', '-dSAFER', str(eps_file)]
        result = subprocess.run(cmd,
                              capture_output=True,
                              text=True,
                              timeout=30,
                              encoding='utf-8',
                              errors='ignore')
        
        if result.returncode == 0:
            print("  ✓ Ghostscript可以解析此文件")
            return True
        else:
            print("  ❌ Ghostscript无法解析此文件")
            if result.stderr:
                print(f"  错误: {result.stderr.strip()[:200]}")
            return False
            
    except Exception as e:
        print(f"  ❌ Ghostscript测试失败: {e}")
        return False

def convert_method_1_svg(eps_file, gs_path, scale_factor=3):
    """方法1: 直接转换为SVG"""
    svg_file = eps_file.with_suffix('.svg')
    
    try:
        if svg_file.exists():
            svg_file.unlink()
        
        dpi = int(72 * scale_factor)
        cmd = [
            gs_path,
            '-dNOPAUSE',
            '-dBATCH', 
            '-dSAFER',
            '-dEPSCrop',
            '-sDEVICE=svg',
            f'-r{dpi}',
            f'-sOutputFile={svg_file}',
            str(eps_file)
        ]
        
        print(f"    执行命令: {' '.join(cmd)}")
        
        result = subprocess.run(cmd,
                              capture_output=True,
                              text=True,
                              timeout=120,
                              encoding='utf-8',
                              errors='ignore')
        
        print(f"    返回码: {result.returncode}")
        if result.stdout:
            print(f"    输出: {result.stdout[:200]}")
        if result.stderr:
            print(f"    错误: {result.stderr[:200]}")
        
        if svg_file.exists() and svg_file.stat().st_size > 0:
            return True
        else:
            return False
            
    except Exception as e:
        print(f"    异常: {e}")
        return False

def convert_method_2_png(eps_file, gs_path, scale_factor=3):
    """方法2: 转换为高分辨率PNG"""
    png_file = eps_file.with_suffix('.png')
    
    try:
        if png_file.exists():
            png_file.unlink()
        
        dpi = int(150 * scale_factor)  # 使用更高的DPI
        cmd = [
            gs_path,
            '-dNOPAUSE',
            '-dBATCH',
            '-dSAFER',
            '-dEPSCrop',
            '-sDEVICE=png16m',  # 24位PNG
            f'-r{dpi}',
            f'-sOutputFile={png_file}',
            str(eps_file)
        ]
        
        print(f"    执行命令: {' '.join(cmd)}")
        
        result = subprocess.run(cmd,
                              capture_output=True,
                              text=True,
                              timeout=120,
                              encoding='utf-8',
                              errors='ignore')
        
        print(f"    返回码: {result.returncode}")
        if result.stderr:
            print(f"    错误: {result.stderr[:200]}")
        
        if png_file.exists() and png_file.stat().st_size > 0:
            file_size = png_file.stat().st_size / 1024
            print(f"    ✓ PNG生成成功: {file_size:.1f} KB")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"    异常: {e}")
        return False

def convert_method_3_pdf(eps_file, gs_path, scale_factor=3):
    """方法3: 先转PDF再处理"""
    pdf_file = eps_file.with_suffix('.pdf')
    
    try:
        if pdf_file.exists():
            pdf_file.unlink()
        
        cmd = [
            gs_path,
            '-dNOPAUSE',
            '-dBATCH',
            '-dSAFER',
            '-dEPSCrop',
            '-sDEVICE=pdfwrite',
            '-dPDFSETTINGS=/prepress',
            f'-sOutputFile={pdf_file}',
            str(eps_file)
        ]
        
        print(f"    执行命令: {' '.join(cmd)}")
        
        result = subprocess.run(cmd,
                              capture_output=True,
                              text=True,
                              timeout=120,
                              encoding='utf-8',
                              errors='ignore')
        
        print(f"    返回码: {result.returncode}")
        if result.stderr:
            print(f"    错误: {result.stderr[:200]}")
        
        if pdf_file.exists() and pdf_file.stat().st_size > 0:
            file_size = pdf_file.stat().st_size / 1024
            print(f"    ✓ PDF生成成功: {file_size:.1f} KB")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"    异常: {e}")
        return False

def convert_eps_diagnostic(eps_file, gs_path, scale_factor=3):
    """诊断式转换EPS文件"""
    print(f"\n正在转换: {eps_file.name}")
    
    # 首先测试文件有效性
    if not test_eps_file(eps_file, gs_path):
        print("  ❌ 文件测试失败，跳过转换")
        return False
    
    # 尝试不同的转换方法
    methods = [
        ("直接转SVG", convert_method_1_svg),
        ("转PNG", convert_method_2_png),
        ("转PDF", convert_method_3_pdf),
    ]
    
    for method_name, method_func in methods:
        print(f"\n  尝试方法: {method_name}")
        try:
            if method_func(eps_file, gs_path, scale_factor):
                print(f"  ✓ {method_name} 成功")
                return True
            else:
                print(f"  ❌ {method_name} 失败")
        except Exception as e:
            print(f"  ❌ {method_name} 异常: {e}")
    
    print("  ❌ 所有转换方法均失败")
    return False

def get_eps_files():
    """获取当前目录下所有EPS文件"""
    current_dir = Path.cwd()
    eps_files = list(current_dir.glob("*.eps"))
    eps_files.extend(current_dir.glob("*.EPS"))
    return sorted(list(set(eps_files)))

def main():
    """主函数"""
    print("EPS 转换器 - 诊断版")
    print("="*60)
    print(f"当前目录: {Path.cwd()}")
    print(f"Python版本: {sys.version}")
    print()
    
    # 查找Ghostscript
    print("检查Ghostscript...")
    gs_path = find_ghostscript()
    
    if not gs_path:
        print("❌ 未找到 Ghostscript")
        input("按回车键退出...")
        return
    
    # 获取EPS文件
    eps_files = get_eps_files()
    
    if not eps_files:
        print("\n❌ 当前目录下没有找到EPS文件")
        input("按回车键退出...")
        return
    
    print(f"\n找到 {len(eps_files)} 个EPS文件")
    
    # 选择测试模式
    print("\n选择操作模式:")
    print("1. 测试单个文件 (诊断)")
    print("2. 批量转换所有文件")
    print("3. 测试前5个文件")
    
    choice = input("\n请选择 (1-3): ").strip()
    
    if choice == "1":
        # 单文件测试
        print("\n可用文件:")
        for i, file in enumerate(eps_files[:10], 1):
            print(f"  {i}. {file.name}")
        
        try:
            file_num = int(input(f"\n选择文件编号 (1-{min(10, len(eps_files))}): ")) - 1
            if 0 <= file_num < len(eps_files):
                convert_eps_diagnostic(eps_files[file_num], gs_path, scale_factor=3)
            else:
                print("无效的文件编号")
        except ValueError:
            print("请输入有效数字")
            
    elif choice == "2":
        # 批量转换
        response = input(f"\n是否转换所有 {len(eps_files)} 个文件? (y/n): ").lower().strip()
        if response in ['y', 'yes', '是']:
            success_count = 0
            for i, eps_file in enumerate(eps_files, 1):
                print(f"\n[{i}/{len(eps_files)}]", "="*50)
                if convert_eps_diagnostic(eps_file, gs_path, scale_factor=3):
                    success_count += 1
            
            print(f"\n总结: 成功 {success_count}/{len(eps_files)} 个文件")
    
    elif choice == "3":
        # 测试前5个
        test_files = eps_files[:5]
        print(f"\n测试前 {len(test_files)} 个文件:")
        
        success_count = 0
        for i, eps_file in enumerate(test_files, 1):
            print(f"\n[{i}/{len(test_files)}]", "="*50)
            if convert_eps_diagnostic(eps_file, gs_path, scale_factor=3):
                success_count += 1
        
        print(f"\n测试结果: 成功 {success_count}/{len(test_files)} 个文件")
    
    else:
        print("无效选择")
    
    input("\n按回车键退出...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n操作被用户中断")
        input("按回车键退出...")
    except Exception as e:
        print(f"\n程序运行出错: {e}")
        import traceback
        traceback.print_exc()
        input("按回车键退出...")