def push_badges_data(data, workflow):
    print("Pushing badge data...")
    configure_git()
    subprocess.run(["git", "fetch"])
    subprocess.run(["git", "checkout", "badges"])

    any_changes = False
    for plugin_name, passed in data.items():
        any_changes |= update_and_commit_badge(plugin_name, passed, workflow)

    if any_changes:
        subprocess.run(["git", "push", "origin", "badges"])
    print("Done.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Plugins completion script')
    parser.add_argument("data", nargs="*", default={}, help="Badges update data")
    parser.add_argument("workflow", type=str, help="Name of the GitHub workflow")
    args = parser.parse_args()

    push_badges_data(args.data, args.workflow)