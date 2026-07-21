import fabio
import os
import re
import numpy as np
from datetime import datetime

def extract_cbf_parameters(file_path):
    """
    Extract key parameters from CBF file headers
    """
    
    if not os.path.exists(file_path):
        print(f"ERROR: File does not exist: {file_path}")
        return None
    
    try:
        # Open CBF file
        img = fabio.open(file_path)
        
        # Get the header content string
        header_content = img.header.get('_array_data.header_contents', '')
        
        # Parse parameters from header
        parameters = {}
        
        # Define parameter patterns (excluding chi)
        patterns = {
            'detector': r'# Detector:\s*(.+)',
            'timestamp': r'# (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+)',
            'pixel_size': r'# Pixel_size\s+([0-9.e-]+)\s*m\s*x\s*([0-9.e-]+)\s*m',
            'sensor_thickness': r'# Silicon sensor, thickness\s+([0-9.]+)\s*m',
            'exposure_time': r'# Exposure_time\s+([0-9.]+)\s*s',
            'exposure_period': r'# Exposure_period\s+([0-9.]+)\s*s',
            'wavelength': r'# Wavelength\s+([0-9.]+)\s*A',
            'detector_distance': r'# Detector_distance\s+([0-9.]+)\s*m',
            'beam_center': r'# Beam_xy\s*\(([0-9.]+),\s*([0-9.]+)\)\s*pixels',
            'start_angle': r'# Start_angle\s+([0-9.-]+)\s*deg',
            'angle_increment': r'# Angle_increment\s+([0-9.-]+)\s*deg',
            'phi': r'# Phi\s+([0-9.-]+)\s*deg',
            'omega': r'# Omega\s+([0-9.-]+)\s*deg',
            'kappa': r'# Kappa\s+([0-9.-]+)\s*deg',
            'oscillation_axis': r'# Oscillation_axis\s+(\w+)',
            'n_oscillations': r'# N_oscillations\s+(\d+)',
            'threshold_setting': r'# Threshold_setting:\s*([0-9]+)\s*eV',
            'flux': r'# Flux\s+([0-9.e+-]+)',
            'count_cutoff': r'# Count_cutoff\s+([0-9]+)\s*counts',
            'gain_setting': r'# Gain_setting:\s*(.+)',
            'n_excluded_pixels': r'# N_excluded_pixels\s*=\s*([0-9]+)',
            'filter_transmission': r'# Filter_transmission\s+([0-9.]+)',
            'detector_2theta': r'# Detector_2theta\s+([0-9.-]+)\s*deg',
            'polarization': r'# Polarization\s+([0-9.]+)',
            'alpha': r'# Alpha\s+([0-9.-]+)\s*deg',
        }
        
        # Extract parameters
        for param_name, pattern in patterns.items():
            match = re.search(pattern, header_content)
            if match:
                if param_name == 'pixel_size':
                    parameters[param_name] = (float(match.group(1)), float(match.group(2)))
                elif param_name == 'beam_center':
                    parameters['beam_center_x'] = float(match.group(1))
                    parameters['beam_center_y'] = float(match.group(2))
                elif param_name in ['exposure_time', 'exposure_period', 'wavelength', 
                                   'detector_distance', 'start_angle', 'angle_increment', 
                                   'phi', 'omega', 'kappa', 'sensor_thickness', 'flux',
                                   'filter_transmission', 'detector_2theta', 'polarization', 'alpha']:
                    parameters[param_name] = float(match.group(1))
                elif param_name in ['n_oscillations', 'threshold_setting', 'count_cutoff', 'n_excluded_pixels']:
                    parameters[param_name] = int(match.group(1))
                else:
                    parameters[param_name] = match.group(1)
        
        # Add image information
        parameters['image_shape'] = img.data.shape
        parameters['data_type'] = str(img.data.dtype)
        parameters['intensity_min'] = int(img.data.min())
        parameters['intensity_max'] = int(img.data.max())
        parameters['mean_intensity'] = float(img.data.mean())
        parameters['file_size_mb'] = os.path.getsize(file_path) / (1024*1024)
        parameters['total_pixels'] = img.data.size
        parameters['std_intensity'] = float(img.data.std())
        
        # Add header objects for detailed analysis
        parameters['full_header'] = img.header
        parameters['pilatus_header'] = img.pilatus_headers if hasattr(img, 'pilatus_headers') else None
        
        return parameters
        
    except Exception as e:
        print(f"Error extracting parameters: {e}")
        return None

def display_detailed_cbf_analysis(file_path):
    """
    Display comprehensive CBF file analysis including both clean summary and detailed headers
    """
    
    params = extract_cbf_parameters(file_path)
    if not params:
        return None
    
    print("=" * 90)
    print("COMPREHENSIVE CBF FILE ANALYSIS")
    print("=" * 90)
    print(f"File: {os.path.basename(file_path)}")
    print(f"Full path: {file_path}")
    print(f"File size: {params.get('file_size_mb', 0):.2f} MB")
    print(f"Analysis time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 90)
    
    # 1. DETECTOR AND HARDWARE INFORMATION
    print("\n1. DETECTOR AND HARDWARE INFORMATION")
    print("-" * 50)
    print(f"Detector: {params.get('detector', 'Unknown')}")
    print(f"Image dimensions: {params.get('image_shape', 'Unknown')} pixels")
    print(f"Total pixels: {params.get('total_pixels', 'Unknown'):,}")
    print(f"Data type: {params.get('data_type', 'Unknown')}")
    if 'pixel_size' in params:
        px, py = params['pixel_size']
        print(f"Pixel size: {px*1e6:.0f} × {py*1e6:.0f} μm ({px:.2e} × {py:.2e} m)")
    print(f"Sensor thickness: {params.get('sensor_thickness', 'Unknown')} m")
    print(f"Threshold setting: {params.get('threshold_setting', 'Unknown')} eV")
    print(f"Count cutoff: {params.get('count_cutoff', 'Unknown'):,} counts" if 'count_cutoff' in params else "Count cutoff: Unknown")
    print(f"Gain setting: {params.get('gain_setting', 'Unknown')}")
    print(f"Excluded pixels: {params.get('n_excluded_pixels', 'Unknown')}")
    
    # 2. BEAM AND EXPERIMENTAL SETUP
    print("\n2. BEAM AND EXPERIMENTAL SETUP")
    print("-" * 50)
    print(f"Wavelength: {params.get('wavelength', 'Unknown')} Å")
    if 'wavelength' in params:
        energy_ev = 12398.4 / params['wavelength']  # Convert wavelength to energy
        print(f"Beam energy: {energy_ev:.1f} eV ({energy_ev/1000:.2f} keV)")
    print(f"Detector distance: {params.get('detector_distance', 'Unknown')} m")
    print(f"Detector 2θ: {params.get('detector_2theta', 'Unknown')}°")
    print(f"Beam center: ({params.get('beam_center_x', 'Unknown')}, {params.get('beam_center_y', 'Unknown')}) pixels")
    print(f"Flux: {params.get('flux', 'Unknown'):.2e}" if 'flux' in params else "Flux: Unknown")
    print(f"Filter transmission: {params.get('filter_transmission', 'Unknown')}")
    print(f"Polarization: {params.get('polarization', 'Unknown')}")
    
    # 3. DATA COLLECTION PARAMETERS
    print("\n3. DATA COLLECTION PARAMETERS")
    print("-" * 50)
    print(f"Exposure time: {params.get('exposure_time', 'Unknown')} s")
    print(f"Exposure period: {params.get('exposure_period', 'Unknown')} s")
    print(f"Start angle: {params.get('start_angle', 'Unknown')}°")
    print(f"Angle increment: {params.get('angle_increment', 'Unknown')}°")
    print(f"Oscillation axis: {params.get('oscillation_axis', 'Unknown')}")
    print(f"Number of oscillations: {params.get('n_oscillations', 'Unknown')}")
    if 'timestamp' in params:
        print(f"Collection time: {params['timestamp']}")
    
    # Calculate total rotation range
    if all(key in params for key in ['angle_increment', 'n_oscillations']):
        total_range = params['angle_increment'] * params['n_oscillations']
        print(f"Total rotation range: {total_range:.1f}°")
    
    # 4. GONIOMETER ANGLES (excluding chi as requested)
    print("\n4. GONIOMETER ANGLES")
    print("-" * 50)
    print(f"Phi: {params.get('phi', 'Unknown')}°")
    print(f"Omega: {params.get('omega', 'Unknown')}°")
    print(f"Kappa: {params.get('kappa', 'Unknown')}°")
    print(f"Alpha: {params.get('alpha', 'Unknown')}°")
    
    # 5. IMAGE STATISTICS AND DATA QUALITY
    print("\n5. IMAGE STATISTICS AND DATA QUALITY")
    print("-" * 50)
    print(f"Intensity range: [{params.get('intensity_min', 'Unknown')}, {params.get('intensity_max', 'Unknown')}]")
    print(f"Mean intensity: {params.get('mean_intensity', 'Unknown'):.3f}")
    print(f"Standard deviation: {params.get('std_intensity', 'Unknown'):.3f}")
    
    # Calculate additional statistics
    if all(key in params for key in ['intensity_max', 'intensity_min', 'mean_intensity', 'std_intensity']):
        dynamic_range = params['intensity_max'] / max(abs(params['intensity_min']), 1)
        snr = params['mean_intensity'] / max(params['std_intensity'], 1e-10)
        print(f"Dynamic range: {dynamic_range:.1f}")
        print(f"Signal-to-noise ratio: {snr:.2f}")
        
        if params['intensity_max'] > 0:
            log_dynamic_range = np.log10(params['intensity_max'] / max(abs(params['intensity_min']), 1))
            print(f"Log dynamic range: {log_dynamic_range:.2f} decades")
    
    # 6. CRYSTALLOGRAPHIC CALCULATIONS
    if all(key in params for key in ['wavelength', 'detector_distance', 'pixel_size', 'image_shape']):
        print("\n6. CRYSTALLOGRAPHIC CALCULATIONS")
        print("-" * 50)
        
        wavelength = params['wavelength'] * 1e-10  # Convert to meters
        distance = params['detector_distance']
        pixel_size = params['pixel_size'][0]  # Assume square pixels
        
        # Calculate resolution at detector corners
        center_x, center_y = params.get('beam_center_x', 0), params.get('beam_center_y', 0)
        max_x, max_y = params['image_shape'][1], params['image_shape'][0]
        
        # Distance from beam center to detector corners
        corner_distances = [
            np.sqrt((center_x - 0)**2 + (center_y - 0)**2),
            np.sqrt((center_x - max_x)**2 + (center_y - 0)**2),
            np.sqrt((center_x - 0)**2 + (center_y - max_y)**2),
            np.sqrt((center_x - max_x)**2 + (center_y - max_y)**2)
        ]
        
        max_pixel_distance = max(corner_distances)
        max_detector_distance = max_pixel_distance * pixel_size
        max_2theta = 2 * np.arctan(max_detector_distance / distance)
        
        # Resolution calculation: d = λ / (2 * sin(θ))
        max_resolution = wavelength / (2 * np.sin(max_2theta / 2))
        
        print(f"Maximum 2θ: {np.degrees(max_2theta):.2f}°")
        print(f"Maximum resolution: {max_resolution * 1e10:.3f} Å")
        print(f"Maximum q-value: {4 * np.pi * np.sin(max_2theta/2) / wavelength / 1e10:.2f} Å⁻¹")
        
        # Calculate some useful distances
        print(f"Beam center to detector edge: {max_detector_distance*1000:.1f} mm")
        print(f"Detector coverage: {np.degrees(2 * np.arctan(max_detector_distance / distance)):.1f}° (2θ)")
    
    # 7. RAW HEADER INFORMATION
    print("\n7. RAW HEADER INFORMATION")
    print("-" * 50)
    
    if params.get('full_header'):
        print("Main CBF header keys:")
        header = params['full_header']
        for key, value in header.items():
            if key != '_array_data.header_contents':  # Skip the long content
                print(f"  {key}: {value}")
    
    # 8. PILATUS HEADER (String representation)
    if params.get('pilatus_header'):
        print(f"\nPilatus header type: {type(params['pilatus_header'])}")
        print("Pilatus header content:")
        pilatus_str = str(params['pilatus_header'])
        # Print first 20 lines of Pilatus header
        lines = pilatus_str.split('\n')[:20]
        for line in lines:
            if line.strip():
                print(f"  {line}")
        if len(pilatus_str.split('\n')) > 20:
            print("  ... (truncated)")
    
    # 9. DATA QUALITY ASSESSMENT
    print("\n9. DATA QUALITY ASSESSMENT")
    print("-" * 50)
    
    # Basic quality indicators
    if 'mean_intensity' in params and 'std_intensity' in params:
        snr = params['mean_intensity'] / max(params['std_intensity'], 1e-10)
        if snr > 10:
            print("✓ Signal-to-noise ratio: EXCELLENT (>10)")
        elif snr > 5:
            print("✓ Signal-to-noise ratio: GOOD (5-10)")
        elif snr > 2:
            print("⚠ Signal-to-noise ratio: MODERATE (2-5)")
        else:
            print("✗ Signal-to-noise ratio: POOR (<2)")
    
    if 'intensity_max' in params:
        if params['intensity_max'] > 1000:
            print("✓ Peak intensity: GOOD (>1000 counts)")
        elif params['intensity_max'] > 100:
            print("⚠ Peak intensity: MODERATE (100-1000 counts)")
        else:
            print("✗ Peak intensity: LOW (<100 counts)")
    
    if 'exposure_time' in params:
        exp_time = params['exposure_time']
        if 0.01 <= exp_time <= 1.0:
            print("✓ Exposure time: OPTIMAL (0.01-1.0 s)")
        elif exp_time > 1.0:
            print("⚠ Exposure time: LONG (>1.0 s) - may have radiation damage")
        else:
            print("⚠ Exposure time: VERY SHORT (<0.01 s) - may be noisy")
    
    # 10. SUMMARY AND RECOMMENDATIONS
    print("\n10. SUMMARY AND RECOMMENDATIONS")
    print("-" * 50)
    
    if 'wavelength' in params:
        if params['wavelength'] < 0.5:
            print("• Short wavelength detected - suitable for PDF/total scattering")
        elif params['wavelength'] < 1.0:
            print("• Medium wavelength - good for protein crystallography")
        else:
            print("• Long wavelength - suitable for small molecules")
    
    if all(key in params for key in ['exposure_time', 'n_oscillations']):
        total_time = params['exposure_time'] * params['n_oscillations']
        print(f"• Total data collection time: {total_time:.1f} seconds ({total_time/60:.1f} minutes)")
    
    if 'intensity_max' in params and 'count_cutoff' in params:
        saturation_percent = (params['intensity_max'] / params['count_cutoff']) * 100
        if saturation_percent > 90:
            print("⚠ WARNING: Detector near saturation - consider shorter exposure")
        else:
            print(f"✓ Detector utilization: {saturation_percent:.1f}% of saturation limit")
    
    print("\n" + "=" * 90)
    print("ANALYSIS COMPLETE")
    print("=" * 90)
    
    return params

def compare_cbf_files(file_paths):
    """
    Compare parameters across multiple CBF files (excluding chi)
    """
    
    all_params = []
    for file_path in file_paths:
        params = extract_cbf_parameters(file_path)
        if params:
            params['filename'] = os.path.basename(file_path)
            all_params.append(params)
    
    if not all_params:
        print("No valid CBF files found")
        return
    
    print("\n" + "=" * 110)
    print("CBF FILE COMPARISON")
    print("=" * 110)
    
    # Compare key parameters (excluding chi)
    print(f"{'File':<35} {'Start°':<8} {'Phi°':<8} {'Omega°':<10} {'Kappa°':<8} {'Exp(s)':<8} {'Max':<8} {'Mean':<8}")
    print("-" * 110)
    
    for params in all_params:
        filename = params['filename'][:33]  # Truncate long filenames
        start_angle = f"{params.get('start_angle', 0):.1f}"
        phi = f"{params.get('phi', 0):.1f}"
        omega = f"{params.get('omega', 0):.1f}"
        kappa = f"{params.get('kappa', 0):.1f}"
        exp_time = f"{params.get('exposure_time', 0):.3f}"
        max_int = f"{params.get('intensity_max', 0)}"
        mean_int = f"{params.get('mean_intensity', 0):.1f}"
        
        print(f"{filename:<35} {start_angle:<8} {phi:<8} {omega:<10} {kappa:<8} {exp_time:<8} {max_int:<8} {mean_int:<8}")

# Main execution
if __name__ == "__main__":
    
    # Single file analysis
    file_path = "/nfs/chess/id4b/2025-2/he-4025-d/raw6M/Ta2NiSeS70/S1/180/Ta2NiSeS70_074/Ta2NiSeS70_PIL10_074_03650.cbf"
    
    print("Enhanced CBF Analysis Tool")
    print("Comprehensive analysis with detailed headers and clean parameter extraction")
    
    # Perform detailed analysis
    params = display_detailed_cbf_analysis(file_path)
    
    # Optional: Compare multiple files (uncomment to use)
    # print("\n" + "="*50)
    # print("MULTIPLE FILE COMPARISON")
    # folder = "/nfs/chess/id4b/2025-2/he-4025-d/raw6M/Ta2NiSeS70/S1/180/Ta2NiSeS70_074/"
    # cbf_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.cbf')][:5]
    # if len(cbf_files) > 1:
    #     compare_cbf_files(cbf_files)
