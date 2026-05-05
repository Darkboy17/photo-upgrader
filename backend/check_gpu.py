import subprocess
import sys

print("=" * 50)
print("🔍 GPU + CUDA DIAGNOSTIC TOOL")
print("=" * 50)

# -----------------------------
# 1. Check PyTorch + CUDA
# -----------------------------
try:
    import torch

    print("\n🧠 PyTorch Info")
    print("-" * 30)
    print("PyTorch version:", torch.__version__)
    print("CUDA available:", torch.cuda.is_available())
    print("CUDA version (PyTorch):", torch.version.cuda)

    if torch.cuda.is_available():
        print("GPU count:", torch.cuda.device_count())

        for i in range(torch.cuda.device_count()):
            props = torch.cuda.get_device_properties(i)
            print(f"\nGPU {i}: {props.name}")
            print(f"  VRAM: {round(props.total_memory / (1024**3), 2)} GB")
            print(f"  Compute capability: {props.major}.{props.minor}")

        # Test GPU computation
        print("\n⚡ Running test tensor on GPU...")
        x = torch.rand(3, 3).to("cuda")
        y = torch.rand(3, 3).to("cuda")
        z = x + y
        print("GPU computation successful ✅")

    else:
        print("⚠️ CUDA NOT available in PyTorch")

except ImportError:
    print("\n❌ PyTorch not installed")

# -----------------------------
# 2. Check nvidia-smi
# -----------------------------
print("\n🖥️ NVIDIA-SMI Info")
print("-" * 30)

try:
    result = subprocess.run(
        ["nvidia-smi"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode == 0:
        print(result.stdout)
    else:
        print("⚠️ nvidia-smi error:")
        print(result.stderr)

except FileNotFoundError:
    print("❌ nvidia-smi not found (NVIDIA drivers missing or not in PATH)")

# -----------------------------
# 3. System Info
# -----------------------------
print("\n💻 System Info")
print("-" * 30)
print("Python version:", sys.version)

print("\n" + "=" * 50)
print("✅ Check complete")
print("=" * 50)