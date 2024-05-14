from fastapi import FastAPI

from app.interactors.waze import LinkType as WazeLinkType, google_maps_link__convert_to__waze_link
from app.interactors.youtube import youtube__get__channel_content

app = FastAPI()


@app.get("/shortcuts/ping")
def read_root():
    return "PONG"


@app.get("/shortcuts/waze/link/from/google/{link_type}")
def read_item(link_type: WazeLinkType, url: str = None):
    return google_maps_link__convert_to__waze_link(
        url=url,
        link_type=link_type
    )


@app.get("/shortcuts/youtube/last_video")
def read_item(channel: str = None):
    return youtube__get__channel_content(
        channel_name=channel
    )
