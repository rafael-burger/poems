import os

# Where your text files are
poem_folder = 'poems-txt'
output_folder = 'poem-pages'

# Make sure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Template for each HTML file
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
</head>
<style>
    body {{
        font-family: "Ubuntu";
        background-color: white;
        color: black;
        font-family: 'Courier New';
    }}
</style>
<body>
    <div id="poem"></div>
                <script>
            fetch('../{poem_page_dir}/{poem_page_file}')
            .then(response => response.text())
            .then(data => {{
                document.getElementById('poem').innerText = data;
            }})
            .catch(error => console.error('Error loading poem:', error));
        </script>
</body>
</html>
"""

# Go through each .txt file and make a page
for filename in os.listdir(poem_folder):
    if filename.endswith('.txt'):
        poem_name = os.path.splitext(filename)[0]
        title = poem_name.replace('-', ' ').split('_')[-1].title()
        html_content = html_template.format(title=title, poem_page_dir=poem_folder, poem_page_file=filename)
        output_path = os.path.join(output_folder, poem_name + '.html')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

print("Done! All HTML files created.")
