
import os
import eyed3

def test():
    audiofile = eyed3.load("/Users/xingnliu/temp/01－A Private Conversation.mp3")
    print('-------------------')
    print(audiofile.tag.artist)
    print(audiofile.tag.album)
    print(audiofile.tag.title)
    print(audiofile.tag.track_num)
    print(audiofile.tag.genre)
    print(audiofile.tag.album_artist)
    print(audiofile.tag.release_date)
    print(audiofile.tag.comments)
    print(audiofile.tag.lyrics)
    print(audiofile.tag.images)
    print(audiofile.tag.composer)


def list_files_by_ext(folder, ext):
    file_list = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(ext):
                file_list.append((os.path.join(root, file), file))
    return file_list


def main():
    folder = "/Users/xingnliu/Downloads/new_concept/NCE4-美音-(MP3+LRC)"
    mp3_files = list_files_by_ext(folder, ".mp3")
    for mp3_file_tuple in mp3_files:
        mp3_file_path = mp3_file_tuple[0]
        mp3_file = mp3_file_tuple[1]
        audiofile = eyed3.load(mp3_file_path)
        audiofile.tag.artist = "New Concept English"
        audiofile.tag.album_artist = "L. G. Alexander"
        audiofile.tag.composer = "L. G. Alexander"
        audiofile.tag.title = mp3_file.replace(".mp3", "")
        audiofile.tag.save()


if __name__ == "__main__":
    main()
