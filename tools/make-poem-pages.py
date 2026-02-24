import os

"""
usage: (from ~/poems/website)

python3 "../tools/make-poem-pages.py"
"""


# Where your text files are
poem_folder = '/src'
output_folder = 'poem-pages'

# Make sure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Template for each HTML file
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="/styles.css">
    <title>{title}</title>
</head>
<body>
    <div id="poem"></div>
                <script>
            fetch('{poem_src_dir}/{poem_src_file}')
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
for filename in os.listdir("src"):
    if filename.endswith('.txt'):
        poem_name = os.path.splitext(filename)[0]
        title = poem_name.replace('-', ' ').split('_')[-1].title()
        html_content = html_template.format(title=title, poem_src_dir=poem_folder, poem_src_file=filename)
        output_path = os.path.join(output_folder, poem_name + '.html')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

print("Done! All HTML files created.")
