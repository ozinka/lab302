extensions = ['.ccd','.dat']
file_list = ['file1.ccd', 'file2.ccd', 'file.sts', 'file.dat']
filtered = []
for file in file_list:
    if any([file.endswith(e) for e in extensions]):
        filtered.append(file)
    print([file.endswith(e) for e in extensions])

print(filtered)


print('file.ccd'.endswith())