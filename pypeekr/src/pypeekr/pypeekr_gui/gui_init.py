import GPUtil


class GPUDetecter:

    def detect_gpus(main_window):
        gpus = GPUtil.getGPUs()
        if not gpus:
            main_window.settings["gpu_vendor"] = "None"
            return

        nvidia_keywords = ["NVIDIA", "RTX", "GTX", "Quadro", "nvidia"]
        amd_keywords = ["AMD", "Radeon", "radeon"]
        intel_keywords = ["Intel", "intel"]

        for gpu in gpus:
            gpu_name_lower = gpu.name.lower()

            if any(keyword.lower() in gpu_name_lower for keyword in nvidia_keywords):
                vendor = "NVIDIA"
            elif any(keyword.lower() in gpu_name_lower for keyword in amd_keywords):
                vendor = "AMD"
            elif any(keyword.lower() in gpu_name_lower for keyword in intel_keywords):
                vendor = "Intel"
            else:
                vendor = "None"

            main_window.settings["gpu_vendor"] = vendor
