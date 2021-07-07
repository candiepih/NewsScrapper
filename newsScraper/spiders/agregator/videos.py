class Videos:
    __videos = {
        "category": "Videos",
        "category_id": 9,
        "videos": [],
    }

    @property
    def videos(self):
        return Videos.__videos

    @videos.setter
    def videos(self, videos_dict):
        if not isinstance(videos_dict, dict):
            raise TypeError("A list is needed as instance argument")
        # elif not videos_dict:
        #     return
        Videos.__videos["videos"].append(videos_dict)

