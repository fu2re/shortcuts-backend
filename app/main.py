from fastapi import FastAPI, Depends

from app.contrib.pw import get_context
from app.interactors.waze import LinkType as WazeLinkType, google_maps_link__convert_to__waze_link
from app.interactors.youtube import youtube__get__channel_content

app = FastAPI()


@app.get("/shortcuts/ping")
def read_root():
    return "PONG"


@app.get("/shortcuts/waze/link/from/google/{link_type}")
async def waze_from_google_link(link_type: WazeLinkType, url: str = None, context=Depends(get_context)):
    return await google_maps_link__convert_to__waze_link(
        url=url,
        link_type=link_type,
        context=context
    )


@app.get("/shortcuts/youtube/last_video")
async def get_latest_video(channel: str = None, context=Depends(get_context)):
    return await youtube__get__channel_content(
        channel_name=channel,
        context=context
    )
