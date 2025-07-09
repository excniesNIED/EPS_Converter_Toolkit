#!/usr/bin/env python3

import os
import subprocess
import sys
from pathlib import Path
import tempfile

def check_tools():
    """检查可用的转换工具"""
    tools = {}
    
    # 检查Inkscape
    inkscape_paths = [
        r"C:\Program Files\Inkscape\bin\inkscape.exe",
        r"C:\Program Files (x86)\Inkscape\bin\inkscape.exe",
        "inkscape"
    ]
    
    for path in inkscape_paths:
        try:
            subprocess.run([path, '--version'], 
                          capture_output=True, check=True, timeout=10,
                          encoding='utf-8', errors='ignore')
            tools['inkscape'] = path
            print(f"✓ 找到 Inkscape: {path}")
            break
        except:
            continue
    
    # 检查Ghostscript
    gs_paths = [
        r"C:\Program Files\gs\gs*\bin\gswin64c.exe",
        r"C:\Program Files (x86)\gs\gs*\bin\gswin32c.exe",
        "gs", "gswin64c", "gswin32c"
    ]
    
    for path_pattern in gs_paths:
        if '*' in path_pattern:
            # 处理通配符路径
            import glob
            matches = glob.glob(path_pattern)
            if matches:
                path = matches[0]
            else:
                continue
        else:
            path = path_pattern
            
        try:
            subprocess.run([path, '--version'], 
                          capture_output=True, check=True, timeout=10,
                          encoding='utf-8', errors='ignore')
            tools['ghostscript'] = path
            print(f"✓ 找到 Ghostscript: {path}")
            break
        except:
            continue
    
    # 检查PIL/Pillow
    try:
        from PIL import Image
        tools['pil'] = True
        print("✓ 找到 PIL/Pillow")
    except ImportError:
        print("- PIL/Pillow 未安装")
    
    return tools

def method1_inkscape_direct(eps_file, svg_file, tools, scale_factor=3):
    """方法1: 直接使用Inkscape转换"""
    if 'inkscape' not in tools:
        return False
    
    try:
        # 简化的Inkscape命令
        cmd = [
            tools['inkscape'],
            str(eps_file),
            '--export-type=svg',
            f'--export-filename={svg_file}',
            '--export-area-drawing',
            f'--export-dpi={96 * scale_factor}',  # 使用DPI缩放
        ]
        
        result = subprocess.run(cmd,
                              capture_output=True,
                              text=True,
                              check=True,
                              timeout=120,
                              encoding='utf-8',
                              errors='ignore')
        
        return svg_file.exists()
        
    except Exception as e:
        print(f"   Inkscape直接转换失败: {e}")
        return False

def method2_ghostscript_pdf(eps_file, svg_file, tools, scale_factor=3):
    """方法2: 使用Ghostscript转PDF再用Inkscape转SVG"""
    if 'ghostscript' not in tools or 'inkscape' not in tools:
        return False
    
    try:
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_pdf:
            pdf_file = Path(tmp_pdf.name)
        
        # Step 1: EPS -> PDF (使用Ghostscript)
        gs_cmd = [
            tools['ghostscript'],
            '-dNOPAUSE',
            '-dBATCH',
            '-dSAFER',
            '-sDEVICE=pdfwrite',
            f'-sOutputFile={pdf_file}',
            str(eps_file)
        ]
        
        subprocess.run(gs_cmd,
                      capture_output=True,
                      check=True,
                      timeout=60,
                      encoding='utf-8',
                      errors='ignore')
        
        if not pdf_file.exists():
            return False
        
        # Step 2: PDF -> SVG (使用Inkscape)
        ink_cmd = [
            tools['inkscape'],
            str(pdf_file),
            '--export-type=svg',
            f'--export-filename={svg_file}',
            '--export-area-drawing',
            f'--export-dpi={96 * scale_factor}',
        ]
        
        subprocess.run(ink_cmd,
                      capture_output=True,
                      check=True,
                      timeout=60,
                      encoding='utf-8',
                      errors='ignore')
        
        # 清理临时文件
        try:
            pdf_file.unlink()
        except:
            pass
        
        return svg_file.exists()
        
    except Exception as e:
        print(f"   Ghostscript+Inkscape转换失败: {e}")
        # 清理可能的临时文件
        try:
            if 'pdf_file' in locals():
                pdf_file.unlink()
        except:
            pass
        return False

def method3_ghostscript_svg(eps_file, svg_file, tools, scale_factor=3):
    """方法3: 直接使用Ghostscript转SVG"""
    if 'ghostscript' not in tools:
        return False
    
    try:
        # 使用Ghostscript直接转换为SVG
        cmd = [
            tools['ghostscript'],
            '-dNOPAUSE',
            '-dBATCH',
            '-dSAFER',
            '-sDEVICE=svg',
            f'-r{96 * scale_factor}',  # 设置分辨率
            f'-sOutputFile={svg_file}',
            str(eps_file)
        ]
        
        subprocess.run(cmd,
                      capture_output=True,
                      check=True,
                      timeout=120,
                      encoding='utf-8',
                      errors='ignore')
        
        return svg_file.exists()
        
    except Exception as e:
        print(f"   Ghostscript直接转换失败: {e}")
        return False

def method4_pil_conversion(eps_file, svg_file, tools, scale_factor=3):
    """方法4: 使用PIL转换为PNG再转SVG"""
    if 'pil' not in tools or 'inkscape' not in tools:
        return False
    
    try:
        from PIL import Image
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_png:
            png_file = Path(tmp_png.name)
        
        # Step 1: EPS -> PNG (使用PIL)
        with Image.open(str(eps_file)) as img:
            # 计算新尺寸
            width, height = img.size
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            
            # 调整大小并保存为PNG
            img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            img_resized.save(str(png_file), 'PNG', dpi=(96 * scale_factor, 96 * scale_factor))
        
        if not png_file.exists():
            return False
        
        # Step 2: PNG -> SVG (使用Inkscape)
        cmd = [
            tools['inkscape'],
            str(png_file),
            '--export-type=svg',
            f'--export-filename={svg_file}',
        ]
        
        subprocess.run(cmd,
                      capture_output=True,
                      check=True,
                      timeout=60,
                      encoding='utf-8',
                      errors='ignore')
        
        # 清理临时文件
        try:
            png_file.unlink()
        except:
            pass
        
        return svg_file.exists()
        
    except Exception as e:
        print(f"   PIL转换失败: {e}")
        try:
            if 'png_file' in locals():
                png_file.unlink()
        except:
            pass
        return False

def convert_eps_to_svg(eps_file, tools, scale_factor=3):
    """尝试多种方法转换EPS到SVG"""
    svg_file = eps_file.with_suffix('.svg')
    
    print(f"正在转换: {eps_file.name} -> {svg_file.name}")
    
    # 如果目标文件已存在，先删除
    if svg_file.exists():
        try:
            svg_file.unlink()
        except:
            pass
    
    # 按优先级尝试不同方法
    methods = [
        ("Inkscape直接转换", method1_inkscape_direct),
        ("Ghostscript+Inkscape", method2_ghostscript_pdf),
        ("Ghostscript直接转换", method3_ghostscript_svg),
        ("PIL+Inkscape转换", method4_pil_conversion),
    ]
    
    for method_name, method_func in methods:
        try:
            print(f"   尝试: {method_name}")
            if method_func(eps_file, svg_file, tools, scale_factor):
                file_size = svg_file.stat().st_size / 1024
                print(f"✓ 成功: {svg_file.name} ({file_size:.1f} KB, {scale_factor}x)")
                return True
        except Exception as e:
            print(f"   {method_name} 出错: {e}")
            continue
    
    print(f"❌ 所有方法均失败: {eps_file.name}")
    return False

def get_eps_files():
    """获取当前目录下所有EPS文件"""
    current_dir = Path.cwd()
    eps_files = list(current_dir.glob("*.eps"))
    eps_files.extend(current_dir.glob("*.EPS"))
    return sorted(list(set(eps_files)))

def main():
    """主函数"""
    print("EPS to SVG 转换器 - 强健版")
    print("=" * 60)
    print(f"当前目录: {Path.cwd()}")
    print()
    
    # 检查工具
    print("检查可用工具...")
    tools = check_tools()
    
    if not tools:
        print("❌ 未找到任何可用的转换工具")
        print("请安装以下工具之一:")
        print("1. Inkscape (推荐)")
        print("2. Ghostscript")
        print("3. PIL/Pillow (pip install Pillow)")
        input("按回车键退出...")
        return
    
    print(f"\n可用工具: {', '.join(tools.keys())}")
    
    # 获取EPS文件
    eps_files = get_eps_files()
    
    if not eps_files:
        print("\n❌ 当前目录下没有找到EPS文件")
        input("按回车键退出...")
        return
    
    print(f"\n找到 {len(eps_files)} 个EPS文件:")
    for i, file in enumerate(eps_files[:10], 1):
        file_size = file.stat().st_size / 1024
        print(f"  {i:2d}. {file.name} ({file_size:.1f} KB)")
    
    if len(eps_files) > 10:
        print(f"  ... 还有 {len(eps_files) - 10} 个文件")
    
    # 确认转换
    response = input(f"\n是否转换为3倍大小的SVG? (y/n): ").lower().strip()
    if response not in ['y', 'yes', '是']:
        print("操作已取消")
        return
    
    print("\n开始转换...")
    print("-" * 60)
    
    # 转换文件
    success_count = 0
    fail_count = 0
    
    for i, eps_file in enumerate(eps_files, 1):
        print(f"\n[{i}/{len(eps_files)}] ", end="")
        if convert_eps_to_svg(eps_file, tools, scale_factor=3):
            success_count += 1
        else:
            fail_count += 1
    
    # 显示结果
    print("\n" + "=" * 60)
    print("转换完成!")
    print(f"成功: {success_count} 个文件")
    print(f"失败: {fail_count} 个文件")
    
    if success_count > 0:
        print(f"\nSVG文件已保存在: {Path.cwd()}")
    
    input("\n按回车键退出...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n操作被用户中断")
        input("按回车键退出...")
    except Exception as e:
        print(f"\n程序出错: {e}")
        input("按回车键退出...")