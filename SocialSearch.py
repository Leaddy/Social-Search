import requests
import json
import tkinter as tk
from tkinter import Label, Entry, Button, scrolledtext, ttk
from tkinter import PhotoImage

search_history = set()
history_window = None

def search_username(username):
    websites = {
        "GitHub": f"https://github.com/{username}",
        "Twitter": f"https://twitter.com/{username}",
        "Instagram": f"https://www.instagram.com/{username}",
        "Facebook": f"https://www.facebook.com/{username}",
        "LinkedIn": f"https://www.linkedin.com/in/{username}",
        "Reddit": f"https://www.reddit.com/user/{username}",
        "Tumblr": f"https://{username}.tumblr.com/",
        "Pinterest": f"https://www.pinterest.com/{username}/",
        "Flickr": f"https://www.flickr.com/people/{username}/",
        "SoundCloud": f"https://soundcloud.com/{username}",
        "DeviantArt": f"https://{username}.deviantart.com/",
        "Stack Overflow": f"https://stackoverflow.com/users/{username}/",
        "HackerRank": f"https://www.hackerrank.com/{username}",
        "CodePen": f"https://codepen.io/{username}/",
        "GitLab": f"https://gitlab.com/{username}",
    }

    results = []
    for site, url in websites.items():
        try:
            response = requests.get(url)
            if response.status_code == 200:
                results.append({"site": site, "url": url})
        except requests.exceptions.RequestException as e:
            pass
    
    return results

def clear_results():
    for widget in result_text.winfo_children():
        widget.destroy()

def search_button_clicked():
    username = username_entry.get().strip()
    if not username:
        return
    if username in search_history:
        search_label.config(text="Bunu zaten arattın.")
        return
    
    search_history.add(username)
    search_label.config(text="Araştırılıyor...")
    app.update()
    
    clear_results()  # Önceki sonuçları temizle
    
    results = search_username(username)
    
    for result in results:
        site_label = Label(result_text, text=result['site'], fg='blue', cursor='hand2', bg='#669999')
        site_label.bind("<Button-1>", lambda e, url=result['url']: open_url(url))
        site_label.pack(anchor=tk.W)
    
    result_text.config(state=tk.DISABLED)
    search_label.config(text="Bulundu.")

def open_url(url):
    import webbrowser
    webbrowser.open_new(url)

def open_leaddy_link():
    import webbrowser
    webbrowser.open_new("https://linktr.ee/leaddy")

def show_search_history():
    global history_window  # history_window değişkenini global olarak tanımlayın

    # Arama geçmişi penceresi daha önce açılmamışsa açın
    if history_window is None or not history_window.winfo_exists():
        history_window = tk.Toplevel(app)
        history_window.title("Arama Geçmişi")
        history_window.geometry("270x300")  # Pencere boyutunu ayarlayın (isteğe bağlı)
        history_window.configure(bg="#339999")
        history_window.resizable(width=False, height=False)

        # Arama geçmişi başlığı
        history_label = Label(history_window, text="(Üstüne tıklayıp Ctrl +C) Arama Geçmişi")
        history_label.configure(bg="#339999")
        history_label.pack(pady=10)

        # Arama geçmişini listeleyen bir Liste Kutusu ekleyin
        search_history_listbox = tk.Listbox(history_window)
        search_history_listbox.configure(bg='#669999')
        search_history_listbox.pack(fill=tk.BOTH, expand=True)

        # Arama geçmişini Liste Kutusu'na ekleyin
        for username in search_history:
            search_history_listbox.insert(tk.END, username)


# Ana uygulama penceresini oluşturuyoruz
app = tk.Tk()
app.title("Sosyal Medya Profil Bulucu")
app.geometry("400x400")
app.resizable(width=False, height=False)
app.configure(bg="#339999")

# Kullanıcı adı girişi
username_label = Label(app, text="Aramak istediğiniz kullanıcı adı:")
username_label.pack(pady=10)
username_label.configure(bg="#339999")
username_entry = Entry(app, validate="key", validatecommand=(app.register(lambda P: len(P) <= 30), "%P"))
username_entry.configure(bg='#669999')
username_entry.pack()

# Arama butonu
search_button = ttk.Button(app, text="ara", command=search_button_clicked)
search_button.pack(pady=2)

search_label = Label(app, text="", fg="blue")
search_label.configure(bg="#339999")
search_label.pack()

arama_gecmisi_simge = PhotoImage(file="C:/Windows/System32/@AdvancedKeySettingsNotification.png")

leaddy_label = Label(app, text="Coded By Leaddy", fg="red", cursor="hand2")
leaddy_label.pack(pady=8)
leaddy_label.configure(bg="#339999")
leaddy_label.bind("<Button-1>", lambda e: open_leaddy_link())

# Sonuçları görüntüleme
result_text = scrolledtext.ScrolledText(app, state=tk.DISABLED)
result_text.configure(bg="#669999")
result_text.pack(fill=tk.BOTH, expand=True)

# Arama geçmişi gösterme düğmesi
history_button = tk.Button(app, text="", command=show_search_history, image=arama_gecmisi_simge, compound="left")
history_button.configure(width=50, height=50, bg="#669999")
history_button.place(x=290, y=70)

app.mainloop()
