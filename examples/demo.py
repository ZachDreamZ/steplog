import time
from steplog import step, output
from steplog.core import Spinner


def demo():
    output.section("steplog feature demo")
    time.sleep(0.2)

    # --- steps ---
    with step("Loading configuration"):
        time.sleep(0.3)

    with step("Validating environment"):
        time.sleep(0.2)

    with step("Connecting to database"):
        time.sleep(0.4)

    # --- failure branch ---
    try:
        with step("Fetching remote data"):
            time.sleep(0.1)
            raise ConnectionError("timeout after 5s")
    except ConnectionError:
        pass

    # --- spinner ---
    output.subheader("background task")
    s = Spinner("Downloading assets ...")
    s.start()
    time.sleep(1.2)
    s.stop()

    # --- output helpers ---
    output.header("Results")
    output.success("Build completed in 1.4s")
    output.info("Listening on http://0.0.0.0:8080")
    output.warn("Rate limit at 80%")
    output.error("Failed to send telemetry")

    # --- table ---
    output.table(
        ["Service", "Status", "Latency"],
        [
            ["Config",   "✓", "120ms"],
            ["Database", "✓", "340ms"],
            ["Cache",    "✓", " 45ms"],
            ["Auth",     "✓", "210ms"],
        ],
    )

    # --- code / json ---
    output.subheader("resolved config")
    output.json({
        "app": {"name": "demo", "port": 8080},
        "features": {"telemetry": False},
    })
    output.divider()

    # --- raw ---
    output.subheader("raw log tail")
    output.raw("2026-07-20 17:29:44 INFO  starting worker pool")
    output.raw("2026-07-20 17:29:44 INFO  4 workers ready")
    output.raw("")

    output.success("Demo complete")

    # --- code block ---
    output.subheader("next steps")
    output.code("pip install steplog")
    output.code("steplog --help")


if __name__ == "__main__":
    demo()
