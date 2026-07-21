

Details about the XTEC code

https://github.com/KimGroup/XTEC


==============
example

    def extract_temperature_info(self, path_str: str) -> Optional[int]:
        """Extract temperature from path (e.g., 105, 75)"""
        path_parts = Path(path_str).parts
        for part in path_parts:
            if part.isdigit() and len(part) <= 3:
                return int(part)
        return None
    
    def load_cbf_scan(self, scan_path: Path, num_images: int = 10) -> Dict:
        """Load CBF files from a single scan folder and create summation"""
        print(f"Processing scan: {scan_path}")
        
        # Find CBF files in the scan folder
        cbf_files = sorted(list(scan_path.glob("*.cbf")))
        
        if len(cbf_files) == 0:
            print(f"No CBF files found in {scan_path}")
            return None
            
        # Take first num_images files
        selected_files = cbf_files[:min(num_images, len(cbf_files))]
        print(f"Found {len(cbf_files)} CBF files, using first {len(selected_files)}")
        
        # Load and sum the images
        summed_data = None
        individual_images = []
        
        for i, cbf_file in enumerate(selected_files):
            try:
                img = fabio.open(str(cbf_file))
                data = img.data.astype(np.float64)
                
                individual_images.append({
                    'filename': cbf_file.name,
                    'data': data,
                    'index': i
                })
                
                if summed_data is None:
                    summed_data = data.copy()
                else:
                    summed_data += data
                    
            except Exception as e:
                print(f"Error loading {cbf_file}: {e}")
                continue
        
        if summed_data is not None:
            return {
                'summed_data': summed_data,
                'individual_images': individual_images,
                'num_images_summed': len(individual_images),
                'scan_folder': str(scan_path),
                'cbf_files_found': len(cbf_files)
            }
        
        return None

