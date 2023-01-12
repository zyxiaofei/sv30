from fastapi import FastAPI
from interfaces.facade import websocket_router, sv30_router, video_router, timer_router, warning_router
from infrastructure.common.initialize import initialize_database, initialize_status_code, initialize_internal_storage, \
    initialize_timer, initialize_limit, plc_program_startup_inspection
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="sv_30")

app.include_router(websocket_router.router)
app.include_router(sv30_router.router, tags=['sv30任务'])
app.include_router(video_router.router, tags=['视频任务'])
app.include_router(timer_router.router, tags=['定时器任务'])
app.include_router(warning_router.router, tags=['报警任务'])

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event('startup')
def initialize_program():
    initialize_database()
    initialize_internal_storage()
    initialize_status_code()
    initialize_timer()
    initialize_limit()
    plc_program_startup_inspection()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run('main:app', host="0.0.0.0", port=8010, reload=True, workers=4)
