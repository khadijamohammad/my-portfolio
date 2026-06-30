applications = []

try:
    with open("applications.txt", "r") as file:
        for line in file:
            if not line.strip():
                continue

            data = line.strip().split("|")

            if len(data) >= 4:
                applications.append({
                    "company": data[0],
                    "job": data[1],
                    "date": data[2],
                    "status": data[3],
                    "interview_date": data[4] if len(data) > 4 else "",
                    "interview_time": data[5] if len(data) > 5 else "",
                    "priority": data[6] if len(data) > 6 else "Medium"
                })
except FileNotFoundError:
    pass

print("================================")
print("📋 JOB APPLICATION TRACKER")
print("================================")

while True:
    print("\n====================")
    print("📋 MENU")
    print("====================")
    print("1 ➜ Add")
    print("2 ➜ View")
    print("3 ➜ Search")
    print("4 ➜ Update")
    print("5 ➜ Statistics")
    print("6 ➜ Delete")
    print("7 ➜ Upcoming Interviews")

    print("8 ➜ Exit")
    print("====================")

    choice = input("\nChoose: ").strip()

    if choice == "1":
        company = input("Company: ").strip()
        job = input("Job Title: ").strip()
        date = input("Date Applied: ").strip()
        status = input("Status: ").strip()
        interview_date = input("Interview Date (optional): ").strip()
        interview_time = input("Interview Time (optional): ").strip()
        priority = input("Priority [High / Medium / Low]: ").title().strip()

        duplicate = False
        for app in applications:
            if (
                app["company"].strip().lower() == company.lower()
                and app["job"].strip().lower() == job.lower()
            ):
                duplicate = True
                break

        if duplicate:
            print("\n⚠ APPLICATION ALREADY EXISTS!")
        else:
            application = {
                "company": company,
                "job": job,
                "date": date,
                "status": status,
                "interview_date": interview_date,
                "interview_time": interview_time,
                "priority": priority
            }
            applications.append(application)
            with open("applications.txt", "a") as file:
                file.write(f"{company}|{job}|{date}|{status}|{interview_date}|{interview_time}|{priority}\n")
            print("\n✅ Application added and saved!")

    elif choice == "2":
        if not applications:
            print("\nNo applications yet.")
        else:
            print("\n📋 APPLICATIONS")
            for app in applications:
                print("\n==============================")
                print("📋 APPLICATION DETAILS")
                print("==============================")
                print("🏢 Company:", app["company"])
                print("💼 Job:", app["job"])
                print("📅 Applied:", app["date"])
                print("📌 Status:", app["status"])
                print("🗓 Interview:", app.get("interview_date", "-"))
                print("⏰ Time:", app.get("interview_time", "-"))
                print("⭐ Priority:", app.get("priority", "Medium"))
                print("==============================")

    elif choice == "3":
        search = input("Company name: ").strip()

        found = False

        for app in applications:
            if search.lower() == app["company"].lower():
                print("\nFOUND")
                print(app)
                found = True

        if not found:
            print("Not found.")

    elif choice == "4":
        company = input("Company to update: ").strip()

        found = False

        for app in applications:
            if company.lower() == app["company"].lower():
                new_status = input("New Status: ").strip()
                app["status"] = new_status
                print("\n✅ Updated")
                found = True

        if not found:
            print("Company not found.")

    elif choice == "5":
        total = len(applications)

        applied = 0
        interview = 0
        rejected = 0
        offer = 0

        for app in applications:
            status = app["status"].lower()

            if "applied" in status:
                applied += 1
            elif "interview" in status:
                interview += 1
            elif "rejected" in status:
                rejected += 1
            elif "offer" in status:
                offer += 1

        print("\n====================")
        print("📊 JOB STATISTICS")
        print("====================")
        print(f"📋 Total: {total}")
        print(f"📨 Applied: {applied}")
        print(f"🗓 Interview: {interview}")
        print(f"❌ Rejected: {rejected}")
        print(f"🏆 Offer: {offer}")
        print("====================")

    elif choice == "6":
        company = input("\nEnter company to delete: ").strip()

        found = False

        for app in applications[:]:
            if app["company"].strip().lower() == company.lower():
                applications.remove(app)
                found = True
                print("\n🗑 Application deleted!")

        if found:
            with open("applications.txt", "w") as file:
                for app in applications:
                    file.write(
                        f"{app['company']}|"
                        f"{app['job']}|"
                        f"{app['date']}|"
                        f"{app['status']}|"
                        f"{app.get('interview_date', '')}|"
                        f"{app.get('interview_time', '')}|"
                        f"{app.get('priority', 'Medium')}\n"
                    )
        else:
            print("\nCompany not found.")
    elif choice == "7":
        print(
            "\n===================="
        )

        print(
            "🗓 UPCOMING INTERVIEWS"
        )

        print(
            "===================="
        )

        found = False

        for app in applications:
            if (
                app["interview_date"]
                and
                app["interview_time"]
            ):
                found = True

                print()

                print(
                    "🏢",
                    app["company"]
                )

                print(
                    "📅",
                    app["interview_date"]
                )

                print(
                    "⏰",
                    app["interview_time"]
                )

                print(
                    "⭐",
                    app.get(
                        "priority",
                        "Medium"
                    )
                )

                print(
                    "----------------"
                )

        if not found:
            print(
                "\nNo interviews scheduled."
            )
    elif choice == "8":
        print(
            "\nGood luck with applications 🌙"
        )

        break
    else:
        print("\nInvalid choice.")