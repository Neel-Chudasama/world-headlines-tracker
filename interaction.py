class HeadlineViewer:
    def __init__(self, final_enhanced_outputs):
        self.root = tk.Tk()
        self.root.title("News Headlines by Category")
        self.root.geometry("1200x800")
        
        # Organize data
        self.category_data = {}
        for category, headline, summary in final_enhanced_outputs:
            if category not in self.category_data:
                self.category_data[category] = []
            self.category_data[category].append({
                'headline': headline if headline else 'No headline',
                'summary': summary if summary else 'No summary available'
            })
        
        # Sort categories by number of headlines (descending)
        self.sorted_categories = sorted(
            self.category_data.keys(), 
            key=lambda x: len(self.category_data[x]), 
            reverse=True
        )
        
        self.setup_ui()
    
    def setup_ui(self):
        # Configure root background
        self.root.configure(bg='#f0f0f0')
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#f0f0f0', padx=10, pady=10)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=3)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="News Headlines by Category", 
            font=('Arial', 20, 'bold'),
            bg='#f0f0f0',
            fg="#000000"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky=tk.W)
        
        # Search box - compact at top
        search_frame = tk.Frame(main_frame, bg='#f0f0f0')
        search_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        tk.Label(search_frame, text="Search:", bg='#f0f0f0', font=('Arial', 14)).pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_categories)
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=('Arial', 14))
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Left panel - Categories list
        left_frame = ttk.Frame(main_frame)
        left_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        ttk.Label(
            left_frame, 
            text="Categories (sorted by count)", 
            font=('Arial', 20, 'bold')
        ).pack(pady=(0, 5))
        
        # Listbox with scrollbar
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.category_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            font=('Arial', 14),
            selectmode=tk.SINGLE,
            width=40
        )
        self.category_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.category_listbox.yview)
        
        # Populate categories
        self.populate_categories()
        
        # Bind selection event
        self.category_listbox.bind('<<ListboxSelect>>', self.on_category_select)
        
        # Right panel - Headlines display
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.headlines_label = ttk.Label(
            right_frame, 
            text="Select a category to view headlines", 
            font=('Arial', 20, 'bold')
        )
        self.headlines_label.pack(pady=(0, 5))
        
        # Text widget for headlines
        self.headlines_text = scrolledtext.ScrolledText(
            right_frame,
            wrap=tk.WORD,
            width=80,
            height=30,
            font=('Arial', 20)
        )
        self.headlines_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for styling
        self.headlines_text.tag_configure('headline', font=('Arial', 15, 'bold'), foreground="#ffffff")
        self.headlines_text.tag_configure('summary', font=('Arial', 15), foreground="#ffffff")
        self.headlines_text.tag_configure('separator', foreground='#cccccc')
        
        # Select first category by default
        if self.sorted_categories:
            self.category_listbox.selection_set(0)
            self.display_headlines(self.sorted_categories[0])
    
    def populate_categories(self, filter_text=''):
        self.category_listbox.delete(0, tk.END)
        
        for category in self.sorted_categories:
            count = len(self.category_data[category])
            display_text = f"{category} ({count})"
            
            if filter_text.lower() in category.lower():
                self.category_listbox.insert(tk.END, display_text)
    
    def filter_categories(self, *args):
        search_text = self.search_var.get()
        self.populate_categories(search_text)
    
    def on_category_select(self, event):
        selection = self.category_listbox.curselection()
        if selection:
            selected_text = self.category_listbox.get(selection[0])
            # Extract category name (remove count)
            category = selected_text.rsplit(' (', 1)[0]
            self.display_headlines(category)
    
    def display_headlines(self, category):
        self.headlines_text.delete('1.0', tk.END)
        
        # Update label
        count = len(self.category_data[category])
        self.headlines_label.config(text=f"{category} - {count} articles")
        
        # Display headlines
        headlines = self.category_data[category]
        for idx, item in enumerate(headlines, 1):
            # Insert headline
            self.headlines_text.insert(tk.END, f"{idx}. ", 'headline')
            self.headlines_text.insert(tk.END, f"{item['headline']}\n", 'headline')
            
            # Insert summary
            self.headlines_text.insert(tk.END, f"   {item['summary']}\n", 'summary')
            
            # Add separator
            #if idx < len(headlines):
            #    self.headlines_text.insert(tk.END, "   " + "─" * 80 + "\n", 'separator')
    
    def run(self):
        self.root.mainloop()

def generate_html_report(final_enhanced_outputs):
    """
        Generates a full HTML report of news articles, categorized and styled.

        Args:
            final_enhanced_outputs (list): A list of tuples/iterables, each containing (category, headline, summary).

        Returns:
            str: A single string containing the complete, formatted HTML report.
        """
    
    category_data = defaultdict(list)
    for category, headline, summary in final_enhanced_outputs:
        category_data[category].append({
            'headline': headline or 'No headline',
            'summary': summary or 'No summary available'
        })

    # Sort by number of headlines
    sorted_categories = sorted(category_data.keys(), key=lambda x: len(category_data[x]), reverse=True)

    html = """
    <html>
    <head>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px; }
        h1 { text-align: center; color: #333; }
        .category {
            background-color: #fff;
            border-radius: 10px;
            margin-bottom: 20px;
            padding: 15px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .category h2 { color: #0056b3; }
        .headline { font-weight: bold; font-size: 16px; margin-top: 10px; color: #333; }
        .summary { color: #555; margin-left: 10px; font-size: 14px; }
    </style>
    </head>
    <body>
        <h1>📰 Morning News Digest</h1>
    """

    for category in sorted_categories:
        html += f"<div class='category'><h2>{category} ({len(category_data[category])})</h2>"
        for item in category_data[category]:
            html += f"<div class='headline'>{item['headline']}</div>"
            html += f"<div class='summary'>{item['summary']}</div>"
        html += "</div>"

    html += "</body></html>"
    return html

def send_email(html_content, to_email):

    """
    Connects to the Gmail SMTP server and sends an HTML-formatted email.

    Args:
        html_content (str): The HTML content to be used as the email body.
        to_email (str): The email address of the recipient.

    Note: The 'app_password' is used for gmail when using external scripts
    """

    from_email = "neelc14@gmail.com"
    app_password = "vhkajmgriskznivc"  # Use Gmail App Password

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Your Morning News Digest"
    msg["From"] = from_email
    msg["To"] = to_email

    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(from_email, app_password)
        server.sendmail(from_email, to_email, msg.as_string())
