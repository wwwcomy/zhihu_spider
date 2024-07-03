
def append_to_file(filename, content):
    with open(filename, 'a') as f:
        f.write(content)
        f.write('\n')
        f.close()