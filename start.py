import uvicorn


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════╗
║        CRYPTOLYTICS STARTING...        ║
╠════════════════════════════════════════╣
║                                        ║
║  Server: http://127.0.0.1:8000        ║
║  API:    http://127.0.0.1:8000/docs   ║
║                                        ║
║  Mode:   ANALYSIS ONLY                 ║
║  Trading: DISABLED                     ║
║                                        ║
╚════════════════════════════════════════╝
""")

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
