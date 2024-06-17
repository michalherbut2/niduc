print(sum(bin(byte).count("1") for byte in b'\x02\x00') % 2)
print(bin(3).count("1"))