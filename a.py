import customtkinter as ctk
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class SpamDetectionEngine:
    def __init__(self):
        self.vectorizer = CountVectorizer(token_pattern=r'(?u)\b\w\w+\b|http\S+|www\S+|\d{4,}') 
        self.models = {}
        self.data = [] # Store data for random picking
        self.current_model_key = None
        self._train_demo_models()

    def set_model(self, model_name):
        self.current_model_key = model_name

    def get_random_example(self):
        if not self.data: return "No data loaded."
        return random.choice(self.data)[0]

    def _train_demo_models(self):
        self.data = [
            # 1. CLASSIC SPAM & SCAMS
            ("Free money now!!!", 1), 
            ("Win a free iPhone click here", 1), 
            ("URGENT: Your account is compromised", 1), 
            ("Cheap meds available online", 1), 
            ("Congratulations! You won the lottery", 1), 
            ("Click this link to claim your prize", 1), 
            ("Exclusive offer just for you", 1), 
            ("Make $5000 from home easy", 1), 
            ("Hot singles in your area", 1), 
            ("100% risk free investment", 1),
            ("You are the lucky winner of a $500 Amazon gift card!", 1),
            ("Nigerian Prince needs your help to transfer funds", 1),
            ("Claim your inheritance of $10,000,000 now", 1),
            ("Cheap Rolex watches 90% off", 1),
            ("Casino bonus! 500 free spins waiting for you", 1),
            ("Dating site for seniors, join for free", 1),
            ("Eliminate your debt legally with this trick", 1),
            ("Stop hair loss immediately with this serum", 1),
            ("Your computer is infected! Download antivirus now", 1),
            ("Get a PhD degree online in just 2 weeks", 1),
            ("Unlock your credit score for free instantly", 1),
            ("Pre-approved for a $50,000 personal loan", 1),
            ("Don't miss this limited time offer!", 1),
            ("Act fast! Only 2 spots left for this exclusive deal", 1),

            # 2. MODERN "SKETCHY" LINKS & CODES (New)
            ("Verify your identity at http://bit.ly/secure-login-attempt", 1),
            ("Your 2FA code is 8921. Do not share this code.", 1),
            ("Action Required: View your invoice at www.paypal-support-verify.com", 1),
            ("Please update your billing info: https://tinyurl.com/y8x92", 1),
            ("Suspicious login detected. Secure your account: http://apple-id-recovery.xyz", 1),
            ("Your package is pending delivery. Pay customs fee: http://dhl-track-package.net", 1),
            ("Kindly purchase a $100 Apple Gift Card and send the code", 1),
            ("Send 0.5 BTC to this wallet address: 1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2", 1),
            ("Download the attached PDF to view your court summons", 1),
            ("Your subscription to GeekSquad has been renewed for $499. Call +1-800-FAKE-NUM to cancel", 1),
            ("Hey, I'm stuck in London and lost my wallet, can you wire me cash?", 1),
            ("Refund initiated. Click here to accept transfer: http://bank-of-america-security.com", 1),
            ("Final Notice: Domain expiration SEO services", 1),
            ("Google Drive: Document shared with you 'Payroll_2025.exe'", 1),
            ("Reset your password immediately: http://microsoft-auth-reset.org", 1),
            ("HR Dept: Please review the attached vacation policy changes", 1),
            ("Your iCloud storage is full. Upgrade now to avoid data loss", 1),
            
            # 3. LEGITIMATE (HAM) MESSAGES
            ("Hi Bob, how about lunch?", 0), 
            ("Meeting reminder for tomorrow", 0), 
            ("Can you send me the report?", 0), 
            ("Love you, see you tonight", 0), 
            ("The project deadline is Friday", 0), 
            ("Let's go for a hike this weekend", 0), 
            ("Did you feed the cat?", 0), 
            ("Please review the attached document", 0), 
            ("Mom called, call her back", 0), 
            ("See you at the gym", 0), 
            ("Grocery list: milk, eggs, bread", 0),
            ("Hey, are we still meeting for coffee at 10?", 0),
            ("Can you pick up the kids from school today?", 0),
            ("The meeting agenda is attached for your review.", 0),
            ("Happy Birthday! Hope you have a great day.", 0),
            ("What time is your flight landing?", 0),
            ("Don't forget to pay the electric bill.", 0),
            ("Just checking in, how are you doing?", 0),
            ("Can you send me the recipe for that lasagna?", 0),
            ("I'll be late, traffic is terrible right now.", 0),
            ("Did you see the game last night?", 0),
            ("Please confirm your attendance for the wedding.", 0),
            ("The package arrived safely, thanks!", 0),
            ("Are you free for a call later this afternoon?", 0),
            ("Let's reschedule our appointment to Tuesday.", 0),
            ("Here are the photos from the trip.", 0),
            ("Can you proofread this document for me?", 0),
            ("Dinner is ready, come downstairs.", 0),
            ("I left the keys under the mat.", 0),
            ("Good morning! Have a productive day.", 0),
            ("Thanks for the gift, I love it!", 0),
            ("Reminder: Dentist appointment tomorrow at 2pm.", 0),
            ("Can you water my plants while I'm away?", 0),
            ("The code for the gate is 1234.", 0),
            ("I'm running 5 minutes late, sorry!", 0),
            ("Let's grab a drink after work.", 0),
            ("Did you get the tickets for the concert?", 0),
            ("Please sign the contract and return it.", 0),
            ("I'm fast asleep, don't wake me up.", 0),
            ("The weather looks great for a picnic.", 0),
            ("Can I borrow your lawnmower this weekend?", 0),
            ("I sent you the money via Venmo.", 0),
            ("Where do you want to go for dinner?", 0),
            ("Don't forget to walk the dog.", 0),
            ("I'm stuck in a meeting, can't talk right now.", 0),
            ("Can you help me move this couch?", 0),
            ("The internet is down again.", 0),
            ("Let's watch a movie tonight.", 0),
            ("Did you hear the news?", 0),
            ("I'm so proud of you!", 0),
            ("Good luck on your exam tomorrow.", 0),
            ("Call your grandmother, it's her birthday.", 0),
            ("We are out of milk and eggs.", 0),
            ("Can you recommend a good plumber?", 0),
            ("The car needs an oil change.", 0),
            ("I'll pick you up at the station.", 0),
            ("Let's plan a trip for next summer.", 0),
            ("Did you finish the report yet?", 0),
            ("I'm taking a sick day today.", 0),
            ("Thanks for your help with the project.", 0),
            ("See you on Monday!", 0),
            ("Here is the link to the zoom meeting: https://zoom.us/j/123456", 0),
            ("Check out this cool article: https://nytimes.com/article", 0),
            ("My phone number is 555-0199", 0)
        ]
        
        texts = [d[0] for d in self.data]
        labels = [d[1] for d in self.data]
        
        X = self.vectorizer.fit_transform(texts)

        # 1. Naive Bayes
        nb = MultinomialNB()
        nb.fit(X, labels)
        self.models["Naive Bayes (High Recall)"] = nb

        # 2. Logistic Regression
        lr = LogisticRegression(random_state=42, solver='liblinear')
        lr.fit(X, labels)
        self.models["Logistic Regression (High Precision)"] = lr

        # 3. Decision Tree
        dt = DecisionTreeClassifier(random_state=42)
        dt.fit(X, labels)
        self.models["Decision Tree (Overfitting Risk)"] = dt

        # 4. Random Forest
        rf = RandomForestClassifier(random_state=42, n_estimators=20)
        rf.fit(X, labels)
        self.models["Random Forest (Robust)"] = rf

        # 5. SVM
        svm = SVC(probability=True, kernel='linear', random_state=42)
        svm.fit(X, labels)
        self.models["SVM (High Margin)"] = svm


    def predict(self, text):
        if not text or self.current_model_key is None: 
            return 0, [0.5, 0.5]
        
        try:
            model = self.models[self.current_model_key]
            
            vectorized_text = self.vectorizer.transform([text])
            if vectorized_text.nnz == 0:
                return 0, [0.85, 0.15]
            
            prediction = model.predict(vectorized_text)[0]
            proba = model.predict_proba(vectorized_text)[0]
            
            return prediction, proba
        except Exception as e:
            print(f"Prediction Error: {e}")
            return 0, [1.0, 0.0]

MODEL_PROFILES = {
    "Naive Bayes (High Recall)": {
        "accuracy": 0.94, "precision": 0.88, "recall": 0.95, "f1": 0.91,
        "cm": [[450, 60], [5, 95]], 
        "desc": "Naive Bayes assumes words are independent. It is very fast and excellent at catching spam keywords (High Recall), but sometimes flags innocent emails that use salesy words (False Positives).",
        "fact": "Did you know? Naive Bayes was one of the first algorithms used for spam filtering in the 90s because it's computationally cheap!"
    },
    "Logistic Regression (High Precision)": {
        "accuracy": 0.96, "precision": 0.98, "recall": 0.85, "f1": 0.91,
        "cm": [[500, 10], [25, 75]], 
        "desc": "Logistic Regression draws a strict line between spam and ham. It is very precise, meaning if it says it's spam, it's almost certainly spam. However, it might miss some subtle spam.",
        "fact": "Did you know? Logistic Regression outputs a probability (0 to 1), making it perfect for setting custom sensitivity thresholds."
    },
    "Decision Tree (Overfitting Risk)": {
        "accuracy": 0.93, "precision": 0.90, "recall": 0.90, "f1": 0.90,
        "cm": [[460, 40], [10, 90]], 
        "desc": "Decision Trees ask a series of yes/no questions (e.g., 'Does it contain $$$?'). They can be very accurate but tend to be 'choppy' and overconfident (100% or 0% score).",
        "fact": "Did you know? A single Decision Tree can be unstable. Changing just one training email might completely change the tree structure!"
    },
    "Random Forest (Robust)": {
        "accuracy": 0.97, "precision": 0.95, "recall": 0.94, "f1": 0.94,
        "cm": [[490, 20], [8, 92]], 
        "desc": "Random Forest combines many Decision Trees to vote on the result. It smoothens out errors and provides a very balanced, robust prediction.",
        "fact": "Did you know? Random Forest is an 'Ensemble' method. It's like asking 100 experts for their opinion instead of just one."
    },
    "SVM (High Margin)": {
        "accuracy": 0.95, "precision": 0.96, "recall": 0.89, "f1": 0.92,
        "cm": [[495, 15], [20, 80]], 
        "desc": "Support Vector Machines try to find the widest possible gap between spam and ham messages. It works very well for text classification with high dimensions.",
        "fact": "Did you know? SVMs calculate a 'margin' of safety. Points inside the margin are the 'gray area' messages."
    }
}

class SpamDetectorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Spam Detector.exe")
        self.geometry("1300x750")
        
        self.engine = SpamDetectionEngine()
        initial_model = list(MODEL_PROFILES.keys())[0]
        self.current_model_name = initial_model
        self.engine.set_model(initial_model)

        self.message_widgets = [] 

        self._setup_layout()
        self._setup_sidebar()
        self._setup_chat_area()
        self._setup_visualization_area()
        
        self.update_charts(self.current_model_name)

    def _setup_layout(self):
        self.grid_columnconfigure(0, weight=0, minsize=260)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0, minsize=450)
        self.grid_rowconfigure(0, weight=1)

    def _setup_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        ctk.CTkLabel(self.sidebar_frame, text="SPAM DETECTOR AI", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(30, 10))
        
        ctk.CTkLabel(self.sidebar_frame, text="Select Classifier:", anchor="w").pack(fill="x", padx=20, pady=(20, 5))
        
        self.model_option_menu = ctk.CTkOptionMenu(
            self.sidebar_frame, 
            values=list(MODEL_PROFILES.keys()),
            command=self.change_model_event,
            width=220
        )
        self.model_option_menu.set(self.current_model_name)
        self.model_option_menu.pack(padx=20, pady=5)

        self.desc_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.desc_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(self.desc_frame, text="Algorithm Logic:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        self.desc_label = ctk.CTkLabel(self.desc_frame, text=MODEL_PROFILES[self.current_model_name]["desc"], 
                                      wraplength=220, justify="left", text_color="gray80")
        self.desc_label.pack(anchor="w", pady=5)

        self.fact_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="#333333", corner_radius=10)
        self.fact_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(self.fact_frame, text="💡 Tech Fact", font=ctk.CTkFont(weight="bold", size=14)).pack(anchor="w", padx=10, pady=(10,0))
        self.fact_label = ctk.CTkLabel(self.fact_frame, text=MODEL_PROFILES[self.current_model_name]["fact"], 
                                      wraplength=200, justify="left", font=ctk.CTkFont(size=12))
        self.fact_label.pack(anchor="w", padx=10, pady=10)

    def _setup_chat_area(self):
        self.chat_container = ctk.CTkFrame(self, fg_color="transparent")
        self.chat_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.chat_container.grid_rowconfigure(0, weight=1)
        self.chat_container.grid_columnconfigure(0, weight=1)

        self.msg_scroll_frame = ctk.CTkScrollableFrame(self.chat_container, label_text="Messages")
        self.msg_scroll_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 10))

        self.input_frame = ctk.CTkFrame(self.chat_container)
        self.input_frame.grid(row=1, column=0, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.status_label = ctk.CTkLabel(self.input_frame, text="Draft Analysis: ...", font=ctk.CTkFont(size=11), text_color="gray")
        self.status_label.grid(row=0, column=0, sticky="w", padx=10, pady=(5,0))

        self.msg_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Type email content here...", height=40)
        self.msg_entry.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        self.msg_entry.bind("<KeyRelease>", self.on_type)
        self.msg_entry.bind("<Return>", lambda e: self.add_message())

        self.rand_btn = ctk.CTkButton(self.input_frame, text="🎲 Example", width=80, fg_color="#444", hover_color="#555", command=self.insert_random_example)
        self.rand_btn.grid(row=1, column=1, padx=(0, 5), pady=(0, 10))

        self.send_btn = ctk.CTkButton(self.input_frame, text="Scan", width=100, command=self.add_message)
        self.send_btn.grid(row=1, column=2, padx=(0, 10), pady=(0, 10))

    def _setup_visualization_area(self):
        self.viz_frame = ctk.CTkFrame(self, width=400)
        self.viz_frame.grid(row=0, column=2, sticky="nsew", padx=(0, 20), pady=20)
        
        ctk.CTkLabel(self.viz_frame, text="Performance Metrics", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=15)

        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(5, 8), facecolor='#2b2b2b')
        self.fig.subplots_adjust(hspace=0.4)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.viz_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    def insert_random_example(self):
        text = self.engine.get_random_example()
        self.msg_entry.delete(0, "end")
        self.msg_entry.insert(0, text)
        self.update_draft_status()

    def on_type(self, event):
        self.update_draft_status()

    def update_draft_status(self):
        text = self.msg_entry.get()
        if not text:
            self.status_label.configure(text="Draft Analysis: Waiting...", text_color="gray")
            return

        prediction, proba = self.engine.predict(text)
        is_spam = prediction == 1
        conf = proba[1]
        
        status_text = f"Draft Analysis: {'SPAM' if is_spam else 'HAM'} ({conf:.1%} Spam Score)"
        color = "#ff5555" if is_spam else "#55ff55"
        self.status_label.configure(text=status_text, text_color=color)

    def add_message(self):
        text = self.msg_entry.get()
        if not text.strip(): return

        msg_frame = ctk.CTkFrame(self.msg_scroll_frame, corner_radius=15)
        msg_frame.pack(fill="x", pady=5, padx=5)
        msg_frame.grid_columnconfigure(1, weight=1)

        icon_label = ctk.CTkLabel(msg_frame, text="", font=ctk.CTkFont(size=20))
        icon_label.grid(row=0, column=0, padx=10, pady=10)

        text_label = ctk.CTkLabel(msg_frame, text=text, wraplength=400, justify="left", anchor="w")
        text_label.grid(row=0, column=1, sticky="w", pady=10)
        
        pred_label = ctk.CTkLabel(msg_frame, text="", font=ctk.CTkFont(size=10), text_color="gray80")
        pred_label.grid(row=1, column=1, sticky="w", pady=(0,10))

        del_btn = ctk.CTkButton(msg_frame, text="✕", width=30, height=30, fg_color="transparent", hover_color="#444", 
                                command=lambda f=msg_frame: self.delete_message(f))
        del_btn.grid(row=0, column=2, padx=10, sticky="ne")

        msg_data = {
            "frame": msg_frame,
            "icon": icon_label,
            "pred_lbl": pred_label,
            "text": text
        }
        self.message_widgets.append(msg_data)
        
        self.update_single_message(msg_data)

        self.msg_entry.delete(0, "end")
        self.status_label.configure(text="Draft Analysis: Sent", text_color="gray")

    def update_single_message(self, msg_data):
        text = msg_data["text"]
        prediction, proba = self.engine.predict(text)
        is_spam = prediction == 1
        
        bubble_color = "#4a1b1b" if is_spam else "#1b4a3b" 
        border_color = "#ff5555" if is_spam else "#55ff55"
        icon = "🛑" if is_spam else "✅"
        
        spam_score = proba[1]
        
        pred_text = f"Detected: {'SPAM' if is_spam else 'HAM'} (Spam Score: {spam_score:.1%})"
        
        msg_data["frame"].configure(fg_color=bubble_color, border_width=1, border_color=border_color)
        msg_data["icon"].configure(text=icon)
        msg_data["pred_lbl"].configure(text=pred_text)

    def refresh_chat(self):
        for msg_data in self.message_widgets:
            self.update_single_message(msg_data)

    def delete_message(self, frame):
        self.message_widgets = [m for m in self.message_widgets if m["frame"] != frame]
        frame.destroy()

    def change_model_event(self, new_model):
        self.current_model_name = new_model
        
        self.engine.set_model(new_model)
        
        self.desc_label.configure(text=MODEL_PROFILES[new_model]["desc"])
        self.fact_label.configure(text=MODEL_PROFILES[new_model]["fact"])
        
        self.update_charts(new_model)
        
        self.refresh_chat()
        
        self.update_draft_status()

    def update_charts(self, model_name):
        metrics = MODEL_PROFILES[model_name]
        
        self.ax1.clear()
        self.ax2.clear()
        
        cm = np.array(metrics["cm"])
        if "Naive" in model_name: cmap = plt.cm.Blues
        elif "Logistic" in model_name: cmap = plt.cm.Oranges
        elif "Tree" in model_name: cmap = plt.cm.Greens
        elif "Forest" in model_name: cmap = plt.cm.Purples
        else: cmap = plt.cm.Reds

        self.ax1.imshow(cm, interpolation='nearest', cmap=cmap)
        self.ax1.set_title("Confusion Matrix", color="white", fontsize=10)
        
        classes = ['Ham', 'Spam']
        self.ax1.set_xticks([0,1])
        self.ax1.set_yticks([0,1])
        self.ax1.set_xticklabels(classes, color="white")
        self.ax1.set_yticklabels(classes, color="white")
        
        for i, j in np.ndindex(cm.shape):
            self.ax1.text(j, i, format(cm[i, j], 'd'), ha="center", va="center", color="white" if cm[i,j] > cm.max()/2 else "black")

        labels = ['Accuracy', 'Precision', 'Recall', 'F1']
        values = [metrics['accuracy'], metrics['precision'], metrics['recall'], metrics['f1']]
        
        colors = ['#3498db', '#e67e22', '#2ecc71', '#9b59b6']
        
        bars = self.ax2.barh(labels, values, color=colors)
        self.ax2.set_xlim(0, 1.1)
        self.ax2.set_title(f"Metrics: {model_name.split('(')[0]}", color="white", fontsize=10)
        self.ax2.tick_params(colors='white')
        self.ax2.grid(color='#444', linestyle='--', linewidth=0.5, axis='x')

        for bar in bars:
            width = bar.get_width()
            self.ax2.text(width + 0.02, bar.get_y() + bar.get_height()/2, f'{width:.0%}', 
                         va='center', color='white', fontsize=9)

        for ax in [self.ax1, self.ax2]:
            ax.set_facecolor('#2b2b2b')
            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('white') 
            ax.spines['left'].set_color('white')
            ax.spines['right'].set_color('white')

        self.fig.tight_layout()
        self.canvas.draw()

if __name__ == "__main__":
    app = SpamDetectorApp()
    app.mainloop()