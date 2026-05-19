from gui.windows.main_window import MainWindow

if __name__ == "__main__":
    app = MainWindow()

    # 🚀 TRIK ZA PRESKAKANJE LOGINA:
    # Možeš da izabereš koga želiš da testiraš:

    # OPCIJA A: Klijent (ID: 100)
    #app.show_dashboard(user_id=100, role="Client")

    # OPCIJA B: Freelancer (ID: 200) - otkomentariši liniju ispod ako želiš njega
    app.show_dashboard(user_id=200, role="Freelancer")

    app.mainloop()
