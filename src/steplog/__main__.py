from steplog import step, output


def main():
    output.section("steplog demo")

    with step("Loading configuration"):
        import time
        time.sleep(0.2)

    with step("Connecting to database"):
        time.sleep(0.3)

    with step("Running migrations"):
        time.sleep(0.15)

    with step("Starting server"):
        time.sleep(0.1)

    output.success("Application started successfully")
    output.table(
        ["Component", "Status", "Time"],
        [
            ["Config", "✓", "200ms"],
            ["Database", "✓", "300ms"],
            ["Migrations", "✓", "150ms"],
            ["Server", "✓", "100ms"],
        ],
    )


if __name__ == "__main__":
    main()
