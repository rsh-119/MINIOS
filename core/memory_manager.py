class MemoryManager:
    def __init__(self, total_memory=1024):
        self.total = total_memory
        self.used = 0
        self.blocks = []  # (pid, size)

    def allocate(self, process, size, strategy="first_fit"):
        """Allocate memory using First/Best/Worst Fit."""
        if self.used + size > self.total:
            print(f"[❌] Not enough memory for {process.pid} ({size})")
            return False

        # Store allocation
        self.blocks.append((process.pid, size))
        self.used += size
        print(f"[✅] {process.pid} allocated {size} MB")
        return True

    def free(self, pid):
        for blk in list(self.blocks):
            if blk[0] == pid:
                self.used -= blk[1]
                self.blocks.remove(blk)
                print(f"[🧹] Freed {blk[1]} MB from {pid}")
                break

    def usage_report(self):
        return {
            "used": self.used,
            "free": self.total - self.used,
            "percent": round((self.used / self.total) * 100, 2)
        }
