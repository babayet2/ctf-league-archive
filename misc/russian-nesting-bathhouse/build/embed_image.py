#!/usr/bin/env python3

import os, sys
import mutagen
from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, COMM, TCOM, TCON, TDRC


def embed_album_art(cover_filepath, audio_filepath):
    """ 
    Embed album art into audio files. 
    https://github.com/desbma/sacad/blob/master/sacad/recurse.py
    """
    with open(cover_filepath, "rb") as f:
        cover_data = f.read()

    mf = mutagen.File(audio_filepath)
    if isinstance(mf.tags, mutagen.id3.ID3) or isinstance(mf, mutagen.id3.ID3FileType):
        mf.tags.add(
            mutagen.id3.APIC(
                mime="image/jpeg",
                type=mutagen.id3.PictureType.COVER_FRONT,
                data=cover_data,
            )
        )
        mf.save()


def tag_song(file):
    # Read ID3 tag or create it if not present
    try:
        tags = ID3(file)
    except ID3NoHeaderError:
        tags = ID3()

    tags["TIT2"] = TIT2(
        encoding=3, text="Why would someone hide a password in mp3 tags?"
    )
    tags["TCOM"] = TCOM(encoding=3, text=u"p4$$w0Rd")
    tags.save(file)


# collect args
if len(sys.argv) == 3:
    mp3_file = sys.argv[2]
    image_file = sys.argv[1]
else:
    mp3_file = "polish_cow.mp3"
    image_file = "post_steg.jpeg"


# embed image in mp3
embed_album_art(
    os.path.join(os.getcwd(), image_file), os.path.join(os.getcwd(), mp3_file)
)

tag_song(os.path.join(os.getcwd(), mp3_file))
