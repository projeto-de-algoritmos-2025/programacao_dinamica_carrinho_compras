from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routes import budget_router, items_router, optimization_router, cart_router
import os


def create_app() -> FastAPI:
    app = FastAPI(
        title="Carrinho de Compras Inteligente API",
        description="API para otimização de compras usando Programação Dinâmica",
        version="1.0.0"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(budget_router)
    app.include_router(items_router)
    app.include_router(optimization_router)
    app.include_router(cart_router)

    static_path = os.path.join(os.path.dirname(__file__), "static")
    app.mount("/static", StaticFiles(directory=static_path), name="static")

    @app.get("/")
    async def root():
        return FileResponse(os.path.join(static_path, "index.html"))
    
    @app.get("/api/info", tags=["Root"])
    async def api_info():
        return {
            "message": "API de Carrinho de Compras Inteligente",
            "docs": "/docs",
            "version": "1.0.0"
        }

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    import webbrowser
    import threading
    
    def open_browser():
        import time
        time.sleep(1.5)
        webbrowser.open("http://localhost:8000")
    
    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run(app, host="127.0.0.1", port=8000)