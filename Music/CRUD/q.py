

album = input("Введите название альбома: ")
while '  ' in album:
    album = album.replace('  ', ' ')
print(album)